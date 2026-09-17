# Official Docs Research: MCP Authorization and Security (2026-07-28 spec revision)
SOURCE_TYPE: official-docs
CONFIDENCE: HIGH
GENERATED: 2026-09-17T16:45:00+05:30

## Summary

The MCP authorization model in the 2026-07-28 revision is OAuth 2.1 plus a defined subset of
IETF/OIDC specs (RFC 9728, RFC 8414, RFC 8707, RFC 9207, RFC 7591, OIDC Discovery/DCR, and the
draft Client ID Metadata Document spec). Authorization remains OPTIONAL and transport-scoped:
HTTP-based servers SHOULD implement it, stdio servers SHOULD NOT (they take credentials from the
environment instead). The headline security posture is unchanged in spirit from 2025-06-18 but
materially hardened: Dynamic Client Registration is now formally deprecated in favor of
Client ID Metadata Documents (CIMD), authorization-response `iss` validation (RFC 9207,
mix-up-attack defense) moves from advisory to normatively required client-side behaviour, and a
new "Enterprise-Managed Authorization" extension (ID-JAG / Identity Assertion JWT Authorization
Grant) formalizes IdP-mediated, zero-touch enterprise access. Token passthrough remains explicitly
forbidden and confused-deputy mitigation is now a MUST for MCP proxy servers. Separately, the
protocol core itself changed shape in this revision (stateless, no `initialize`/`Mcp-Session-Id`,
new `server/discover`, `Mcp-Method`/`Mcp-Name` request headers) — this materially changes how a
gateway would enforce authorization and route/meter traffic. Tool annotations
(readOnlyHint/destructiveHint/idempotentHint/openWorldHint) are explicitly documented as
untrusted, spoofable hints, not security guarantees. The MCP Registry is explicitly in **preview**,
not GA.

## Key Findings

### 1. Authorization spec basis, discovery, resource indicators, client registration, scopes, PKCE

- FINDING: Authorization is OPTIONAL for MCP implementations. "Implementations using an HTTP-based
  transport SHOULD conform to this specification. Implementations using an STDIO transport
  SHOULD NOT follow this specification, and instead retrieve credentials from the environment.
  Implementations using alternative transports MUST follow established security best practices
  for their protocol."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

- FINDING: The spec is explicitly built on a named subset of specs: OAuth 2.1 IETF draft
  (draft-ietf-oauth-v2-1-13), RFC 6750 (Bearer Token Usage), RFC 8414 (AS Metadata), RFC 7591
  (Dynamic Client Registration — now deprecated), RFC 8707 (Resource Indicators), RFC 9728
  (Protected Resource Metadata), RFC 9207 (AS Issuer Identification), the draft Client ID
  Metadata Document spec (draft-ietf-oauth-client-id-metadata-document-00), OpenID Connect
  Discovery 1.0, and OIDC Dynamic Client Registration 1.0.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

- FINDING: "Authorization servers MUST implement OAuth 2.1 with appropriate security measures for
  both confidential and public clients." "Authorization servers and MCP clients SHOULD support
  OAuth Client ID Metadata Documents." "Authorization servers and MCP clients MAY support the
  OAuth 2.0 Dynamic Client Registration Protocol (RFC7591). Note that Dynamic Client Registration
  is deprecated and retained for backwards compatibility with authorization servers that do not
  support Client ID Metadata Documents." "MCP servers MUST implement OAuth 2.0 Protected Resource
  Metadata (RFC9728). MCP clients MUST use OAuth 2.0 Protected Resource Metadata for authorization
  server discovery." "MCP authorization servers MUST provide at least one of the following
  discovery mechanisms: OAuth 2.0 Authorization Server Metadata (RFC8414) [or] OpenID Connect
  Discovery 1.0 ... MCP clients MUST support both discovery mechanisms."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

- FINDING: Protected Resource Metadata discovery is required via one of two mechanisms: the
  `WWW-Authenticate` header's `resource_metadata` parameter on a 401, or a well-known URI
  (`/.well-known/oauth-protected-resource{/path}` or root). "MCP clients MUST support both
  discovery mechanisms." Multiple authorization servers may be listed; the client picks one per
  RFC 9728 §7.6, and "Clients MUST maintain separate registration state (client credentials,
  tokens) per authorization server and MUST NOT assume that credentials valid for one
  authorization server will be accepted by another."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery

- FINDING: AS metadata discovery uses the standard `oauth-authorization-server` well-known suffix
  (RFC 8414 §3.1) — MCP defines no MCP-specific suffix — and clients MUST try OAuth AS Metadata
  and OIDC Discovery endpoints in a defined priority order (with path-insertion and
  path-appending variants for issuers with path components). After fetching, "the `issuer` value
  in the document MUST be identical to the issuer identifier used to construct the well-known
  URL. If they differ, the client MUST NOT use the metadata" — an explicit anti-spoofing check.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery

- FINDING: Resource Indicators (RFC 8707) are mandatory and used for audience binding. "MCP
  clients MUST implement Resource Indicators for OAuth 2.0 as defined in RFC 8707 ... The
  `resource` parameter: 1. MUST be included in both authorization requests and token requests.
  2. MUST identify the MCP server that the client intends to use the token with. 3. MUST use the
  canonical URI of the MCP server." "MCP clients MUST send this parameter regardless of whether
  authorization servers support it." Server-side: "MCP servers MUST validate that access tokens
  were issued specifically for them as the intended audience, according to RFC 8707 Section 2."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

- FINDING: Client registration has three mechanisms with a defined priority order: (1)
  pre-registered client info if available, (2) Client ID Metadata Documents (CIMD) if the AS
  advertises `client_id_metadata_document_supported`, (3) Dynamic Client Registration as fallback,
  (4) prompt the user. CIMD uses an HTTPS URL as the `client_id`; the AS fetches and validates
  the JSON document (must include at least `client_id`, `client_name`, `redirect_uris`; the
  document's `client_id` must match the URL exactly). DCR (RFC 7591) is formally flagged deprecated
  in the client-registration page and in the changelog's Deprecated section, "retained for
  backwards compatibility with authorization servers that do not support Client ID Metadata
  Documents."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/changelog

- FINDING: Client credentials are now issuer-bound. "Clients that use pre-registered credentials,
  or persist client credentials obtained via Dynamic Client Registration, MUST associate those
  credentials with the specific authorization server that issued them, keyed by the authorization
  server's `issuer` identifier ... clients MUST NOT reuse client credentials from a different
  authorization server and MUST re-register with the new authorization server." CIMD-based
  client IDs are exempt from this (they are portable, self-hosted URLs resolved on demand).
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration

- FINDING: Scope handling: servers SHOULD advertise required scopes via `WWW-Authenticate:
  scope="..."` on 401s; clients MUST treat challenge scopes as authoritative for the current
  operation and follow a priority order (challenge scope → `scopes_supported` → nothing). For
  runtime `insufficient_scope` (403) errors: "the server SHOULD respond with HTTP 403 Forbidden
  ... `WWW-Authenticate` header with the Bearer scheme and ... `error="insufficient_scope"`,
  `scope="required_scope1 required_scope2"`, `resource_metadata` ..." Clients then run a
  **step-up authorization flow**: compute the union of previously requested and newly challenged
  scopes, re-authorize, and retry "no more than a few times" before treating it as a permanent
  failure. "Servers MUST account for scope hierarchies, where a broader scope implies narrower
  ones, when deciding whether a token is sufficient for an operation."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

- FINDING: PKCE is mandatory. "To mitigate this, MCP clients MUST implement PKCE ... and MUST
  verify PKCE support before proceeding with authorization ... MCP clients MUST use the S256 code
  challenge method when technically capable ... If `code_challenge_methods_supported` is absent,
  the authorization server does not support PKCE and MCP clients MUST refuse to proceed."
  (Same rule applies to OIDC discovery documents that omit the field.)
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations

- FINDING (new vs. 2025-06-18/2025-11-25 — normative upgrade): Authorization-response `iss`
  validation, based on RFC 9207, is now a required client-side check against mix-up attacks: "On
  receiving the authorization response, MCP clients MUST apply the validation in RFC9207 Section
  2.4 before transmitting the authorization code to any token endpoint" — including rejecting the
  response outright if the AS advertises `authorization_response_iss_parameter_supported: true`
  but omits `iss`. The changelog explicitly attributes this to SEP-2468 as a change in this
  revision: "Authorization servers SHOULD include the `iss` parameter in authorization responses
  per RFC 9207, and MCP clients MUST validate a present `iss` against the recorded issuer before
  redeeming the authorization code." The spec also flags this as still evolving: "A future
  revision of this specification is expected to upgrade authorization server inclusion of `iss`
  from SHOULD to MUST."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/changelog

- FINDING (new in this revision): Refresh token guidance was added/tightened: clients "MUST keep
  refresh tokens confidential in transit and storage," "MUST NOT assume refresh tokens will be
  issued," and servers "SHOULD NOT include `offline_access` in `WWW-Authenticate` scope or
  Protected Resource Metadata `scopes_supported`, as refresh tokens are not a resource
  requirement."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

### 2. Token passthrough prohibition, confused deputy, and downstream API calls

- FINDING: Token passthrough is explicitly and unconditionally forbidden. "Token passthrough is
  explicitly forbidden in the authorization specification." "MCP servers MUST NOT accept any
  tokens that were not explicitly issued for the MCP server." The spec body itself states: "MCP
  servers MUST only accept tokens that are valid for use with their own resources. MCP servers
  MUST NOT accept or transit any other tokens" and "MCP clients MUST NOT send tokens to the MCP
  server other than ones issued by the MCP server's authorization server."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

- FINDING: The spec is explicit that a server calling upstream APIs performs its own separate
  OAuth client role and issues/uses a different token — the spec does **not** name a specific
  token-exchange grant (e.g., RFC 8693) to use for this, leaving the mechanism to the
  implementer: "If the MCP server makes requests to upstream APIs, it may act as an OAuth client
  to them. The access token used at the upstream API is a separate token, issued by the upstream
  authorization server. The MCP server MUST NOT pass through the token it received from the MCP
  client."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations

- FINDING: Token passthrough is described as having two dimensions — audience-validation failure
  (accepting tokens not intended for the server) and passthrough proper (forwarding those tokens
  downstream unmodified) — and the risks are enumerated in detail: security-control
  circumvention, accountability/audit-trail loss, trust-boundary violation (a compromised
  downstream service can replay the token elsewhere), and future-compatibility risk. "Mitigation:
  MCP servers MUST NOT accept any tokens that were not explicitly issued for the MCP server."
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

- FINDING: Confused deputy is defined specifically for the "MCP Proxy Server" pattern (a server
  acting as a single OAuth client to a third-party AS on behalf of many MCP clients). The attack
  requires: static client ID at the third-party AS + client-side dynamic registration + a
  consent cookie set by the third-party AS + no per-client consent check by the proxy. Mitigation
  is normative: "MCP proxy servers using static client IDs MUST obtain user consent for each
  dynamically registered client before forwarding to third-party authorization servers (which may
  require additional consent)." Detailed sub-requirements (all MUST): per-client consent registry
  checked before forwarding; consent UI must name the client, list scopes, show the redirect URI,
  implement CSRF/state protection, and prevent clickjacking; consent cookies must use `__Host-`
  prefix, `Secure`/`HttpOnly`/`SameSite=Lax`, be signed/server-side, and bound to `client_id`;
  redirect URIs must be exact-matched; OAuth `state` must be generated per request, stored only
  **after** consent is approved, single-use, and short-lived.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations

- FINDING: URL-mode elicitation (used e.g. for server-managed third-party OAuth) reiterates the
  same rule from the elicitation angle: "The MCP server MUST NOT use the client's credentials for
  the third-party service: That would be token passthrough, which is forbidden," and "Credentials
  obtained via URL mode elicitation are distinct from the MCP server credentials used by the MCP
  client. The MCP server MUST NOT transmit credentials obtained through URL mode elicitation to
  the MCP client."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation

### 3. Enterprise-Managed Authorization / ID-JAG — status

- FINDING: Enterprise-Managed Authorization is an **official, named MCP extension**
  (`io.modelcontextprotocol/enterprise-managed-authorization`), documented directly on
  modelcontextprotocol.io under `/extensions/auth/`, with its normative spec published in the
  `stable/` directory of the `modelcontextprotocol/ext-auth` GitHub repo — i.e. it has graduated
  from proposal to a stable extension spec, distinct from experimental/draft extensions. It
  originated as SEP-990 ("Enable Enterprise IdP Policy Controls during MCP OAuth").
  SOURCE: https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization
  SOURCE: https://github.com/modelcontextprotocol/ext-auth/blob/main/specification/stable/enterprise-managed-authorization.mdx

- FINDING: The mechanism is ID-JAG (Identity Assertion JWT Authorization Grant): the MCP client
  authenticates the user via corporate SSO, obtains an ID Token from the enterprise IdP, exchanges
  that ID Token for an ID-JAG from the IdP (policy is evaluated at this step), then presents the
  ID-JAG to the MCP server's own Authorization Server in a token request to get an MCP access
  token — the client never redirects to the MCP AS's own authorize endpoint. "Do not redirect the
  user to the MCP Authorization Server's authorization endpoint." Revocation is centralized at the
  IdP and takes effect immediately across all clients.
  SOURCE: https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization

- FINDING: Extensions generally (including this one) are explicitly opt-in and never silently
  active: "Extensions are opt-in and never active by default" and support "varies by client" —
  check the published client support matrix before relying on it.
  SOURCE: https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization

- FINDING: The core authorization spec formally hooks extensions in as a defined, versioned
  layer: "There are several authorization extensions to the core protocol ... These extensions
  are: Optional ... Additive ... Composable ... Versioned independently ... A list of supported
  extensions can be found in the MCP Authorization Extensions repository
  (github.com/modelcontextprotocol/ext-auth)." This is new machinery in 2026-07-28 vs. earlier
  revisions, which had no formal extensions framework for auth.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
  SOURCE: https://blog.modelcontextprotocol.io/posts/2026-07-28/

### 4. Security Best Practices page — attack catalogue

- FINDING: The Security Best Practices document (companion to, not part of, the normative
  authorization spec) enumerates these attacks/mitigations as of the 2026-07-28 doc set:
  Confused Deputy Problem, Token Passthrough, Server-Side Request Forgery (SSRF) during metadata
  discovery, State Handle Hijacking (new name/reframing, replacing "Session Hijacking" now that
  MCP is stateless), Local MCP Server Compromise, OAuth Authorization URL Validation (XSS/RCE via
  malicious `javascript:`/shell-injected authorization URLs), stdio Transport Security in Proxy
  Scenarios, Mix-Up Attacks, Localhost Redirect URI Impersonation, CIMD Trust Policies, and Scope
  Minimization.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

- FINDING (SSRF): During OAuth metadata discovery, a malicious MCP server can populate
  `resource_metadata`, `authorization_servers`, `token_endpoint`, etc. with URLs pointing at
  internal IPs or cloud metadata endpoints (`169.254.169.254`). "MCP clients deployed to a server
  MUST consider SSRF risks and implement appropriate mitigations when fetching OAuth-related
  URLs." Mitigations listed as SHOULD: enforce HTTPS (reject `http://` except loopback), block
  private/reserved IP ranges per RFC 9728 §7.7 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16,
  127.0.0.0/8, 169.254.0.0/16, fc00::/7, fe80::/10), validate redirect targets the same way, use
  an egress proxy (example: Stripe's Smokescreen), and account for DNS-rebinding/TOCTOU. The same
  SSRF risk is called out symmetrically for authorization servers that fetch CIMD client metadata
  documents (server-side fetch of an attacker-controlled URL).
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

- FINDING (State Handle Hijacking, replaces "session hijacking" concept): "MCP is stateless and
  has no protocol-level sessions. Servers that need state spanning multiple requests mint an
  explicit handle ... State handle hijacking is an attack vector where an unauthorized party
  obtains or guesses such a handle." Mitigation: "MCP servers that implement authorization MUST
  verify all inbound requests. MCP servers MUST NOT treat possession of a state handle as
  authentication." Servers SHOULD use non-deterministic, expiring handles and SHOULD bind handles
  server-side to the authenticated user (e.g. `<user_id>:<handle>` keyed off the verified token's
  subject, never a client-supplied user ID). The page explicitly links out to the *prior*
  revision's page for the old "Session Hijacking" guidance tied to `Mcp-Session-Id`, which no
  longer exists in this revision's transport.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

- FINDING (Local server compromise): Clients doing one-click local server configuration "MUST
  implement proper consent mechanisms prior to executing commands" — showing the exact
  unabridged command, warning on dangerous patterns (`sudo`, `rm -rf`, network/filesystem access),
  and SHOULD sandbox spawned processes (containers, chroot, restricted FS/network access, kept
  up to date). Servers meant to run locally SHOULD "Use the `stdio` transport to limit access to
  just the MCP client" and, if using HTTP locally, require an auth token or use Unix domain
  sockets/other restricted IPC.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

- FINDING (Scope minimization — 2026 addition): This section gives concrete scope-issuance
  guidance not present in earlier revisions: minimal baseline scope (e.g., `mcp:tools-basic`),
  incremental elevation via targeted `WWW-Authenticate scope="..."` challenges, and explicit
  "Common Mistakes" to avoid: publishing every possible scope in `scopes_supported`, wildcard/
  omnibus scopes (`*`, `all`, `full-access`), bundling unrelated privileges preemptively,
  returning the entire scope catalog on every challenge, silent scope semantic changes without
  versioning, and trusting claimed token scopes without server-side authorization logic.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

### 5. stdio vs remote servers — auth model

- FINDING: The core authorization spec draws the line explicitly at the transport level (quoted
  fully in Finding 1): HTTP-based transports SHOULD conform to the OAuth 2.1-based spec; stdio
  transports SHOULD NOT — they "retrieve credentials from the environment" instead (e.g.
  environment variables, OS keychain, CLI-supplied secrets), and any other/custom transport MUST
  follow established security best practices for its own protocol rather than trying to reuse the
  HTTP-oriented OAuth flow.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

- FINDING: The stdio transport page itself has no OAuth content; it defines process lifecycle
  (client spawns server as subprocess, newline-delimited JSON-RPC over stdin/stdout, `stderr` for
  logs only) and states there is no header layer — "All request metadata for the stdio transport
  is carried inline in the JSON-RPC message body ... There is no header layer." This reinforces
  that stdio has no protocol-native place to carry bearer tokens; auth is entirely an
  out-of-band, environment-level concern.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio

- FINDING: Local/stdio-adjacent risk is instead handled under the Security Best Practices "Local
  MCP Server Compromise" and "stdio Transport Security in Proxy Scenarios" sections (see Finding
  4), which frame the stdio transport itself as "not inherently vulnerable" but flag proxy
  architectures that spawn stdio child processes on behalf of a remote/web client as a privilege-
  escalation path when combined with client-side XSS.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

### 6. Tool annotations as untrusted hints; elicitation/consent security

- FINDING: `ToolAnnotations` defines four boolean hints: `readOnlyHint` (default false — "Does the
  tool modify its environment?"), `destructiveHint` (default true — "If it does modify things, is
  the change destructive?"), `idempotentHint` (default false — "Can you safely call it with the
  same arguments?"), `openWorldHint` (default true — "Does the tool interact with an open world of
  external entities?"). Defaults are pessimistic: an unannotated tool is assumed destructive and
  open-world.
  SOURCE: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/

- FINDING: The MCP project is explicit that these are not security guarantees: "annotations are
  not guaranteed to faithfully describe tool behavior, and clients must treat them as untrusted
  unless they come from a trusted server," illustrated with "A server can claim `readOnlyHint:
  true` and delete your files anyway." Guidance for clients is graduated trust: a
  `readOnlyHint: true` tool from a *trusted* server may be auto-approved, while
  `destructiveHint: true` should get a confirmation step; for *untrusted* servers, annotations
  should be treated as informational only, with real safety enforced through deterministic
  controls rather than the hints themselves.
  SOURCE: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/

- FINDING: Elicitation now has two modes with distinct security rules. Form mode is for
  structured, in-band data collection; URL mode is for out-of-band interactions that must not
  pass through the MCP client. The spec draws a hard line: "Servers MUST NOT use form mode
  elicitation to request sensitive information such as passwords, API keys, access tokens, or
  payment credentials. Servers MUST use URL mode for interactions involving such sensitive
  information."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation

- FINDING: URL-mode elicitation carries a detailed, explicitly normative client-side "Safe URL
  Handling" section. Servers: MUST NOT embed sensitive end-user info (credentials, PII) in the
  elicitation URL; MUST NOT provide a pre-authenticated URL (impersonation risk); SHOULD NOT make
  URLs clickable inside a *form*-mode request; SHOULD use HTTPS outside dev. Clients: MUST NOT
  pre-fetch the URL or its metadata; MUST NOT open the URL without explicit user consent; MUST
  show the full URL before consent; MUST open it in a way that prevents the client/LLM from
  inspecting page content or user input (example given: iOS `SFSafariViewController` is
  acceptable, `WKWebView` is not); SHOULD highlight the domain (subdomain-spoofing mitigation) and
  SHOULD warn on Punycode/ambiguous URIs.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation

- FINDING: URL-mode elicitation phishing/account-takeover risk is explicitly documented with a
  worked attack (attacker "Alice" tricks victim "Bob" into completing Alice's third-party OAuth
  flow via a shared elicitation link, binding Bob's authorization to Alice's session). Mitigation
  is normative: "the server MUST ensure that the user who started the elicitation request ... is
  the same user who completes the authorization flow," typically by binding the "connect" page to
  the MCP session cookie/subject and comparing it against the authenticated `sub` claim before
  forwarding to the third-party AS. "In all implementations, the server MUST ensure that the
  mechanism to determine the user's identity is resilient to attacks where an attacker can modify
  the elicitation URL."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation

- FINDING: User identity for elicitation/state must come from verified auth, not client claims:
  "Servers MUST NOT rely on client-provided user identification without server verification, as
  this can be forged ... Correct: Rely on authorization to identify the user."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation

- FINDING: OAuth-URL client-side handling has its own hardening section (new/expanded vs. earlier
  revisions), driven by real XSS/RCE risk from malicious authorization URLs: clients "MUST only
  allow `http://` and `https://` schemes" (http only for loopback in dev), "MUST reject
  `javascript:`, `data:`, `file:`, `vbscript:`," "MUST NOT use shell commands ... to open URLs,"
  and SHOULD use allowlist-based validation and CSP (`script-src 'self'`) for web-based clients.
  SOURCE: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

### 7. Official MCP Registry

- FINDING: The registry is explicitly **preview**, not GA: "The MCP Registry is currently in
  preview. Breaking changes or data resets may occur before general availability."
  SOURCE: https://modelcontextprotocol.io/registry/about

- FINDING: It is "the official centralized metadata repository for publicly accessible MCP
  servers, backed by major trusted contributors ... such as Anthropic, GitHub, PulseMCP, and
  Microsoft." It stores `server.json` metadata (schema linked from the registry repo) — unique
  reverse-DNS name (`io.github.user/server-name`), location (npm package, remote URL, etc.),
  execution instructions, and discovery metadata. It hosts metadata only, not code — actual
  packages live on npm/PyPI/Docker Hub etc.
  SOURCE: https://modelcontextprotocol.io/registry/about

- FINDING: Namespace/authenticity verification is DNS/GitHub-account based: "Server names follow a
  reverse DNS format ... that ties them to verified GitHub accounts or domains. This namespace
  system ensures that only the legitimate owner of a GitHub account or domain can publish servers
  under that namespace." Security scanning of the actual server code is explicitly *not* done by
  the registry itself — it is delegated: "The MCP Registry delegates security scanning to:
  Underlying package registries ... Downstream aggregators ... The MCP Registry focuses on
  namespace authentication and metadata hosting, while relying on the broader ecosystem for
  security scanning of actual server code."
  SOURCE: https://modelcontextprotocol.io/registry/about

- FINDING: The registry explicitly does **not** support private/internal servers ("private
  servers are those only accessible to a narrow set of users" — internal hostnames, private
  package registries) and recommends self-hosting a private registry for that case. It defines an
  OpenAPI spec that other registries — including enterprise "subregistries" — can implement:
  "Private MCP registries can implement it as well to benefit from existing host application
  support," and separately, host applications are told not to consume the official registry
  directly: "The MCP Registry is not intended to be directly consumed by host applications.
  Instead, host applications should consume other MCP registries, such as downstream marketplaces,
  via a REST API conforming to the official MCP Registry's OpenAPI spec." The official codebase
  is explicitly **not** designed for self-hosting/forking with support: "the official MCP Registry
  codebase is not designed for self-hosting, and the registry maintainers cannot provide support
  for this use case."
  SOURCE: https://modelcontextprotocol.io/registry/about

### 8. Gateway-relevant protocol items: headers, discovery, statelessness

- FINDING: The 2026-07-28 revision removed the `initialize`/`notifications/initialized` handshake
  and the `Mcp-Session-Id` header/protocol-level sessions entirely (SEP-2575, SEP-2567). "Every
  request now carries its protocol version and client capabilities in `_meta`." List endpoints
  (`tools/list`, etc.) "no longer vary per-connection." Any server-side state that spans requests
  must now be an explicit, server-minted handle passed back as an ordinary tool argument — see
  Finding 4's "State Handle Hijacking" mitigation, which is the direct authorization-relevant
  consequence of this change (no session, so no implicit per-connection auth context either — the
  server must independently authenticate/authorize every single request).
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/changelog

- FINDING: A new optional-to-call, mandatory-to-implement discovery RPC was added: "Add
  `server/discover`: servers MUST implement this RPC to advertise their supported protocol
  versions, capabilities, and identity. Clients MAY call it before any other request for
  up-front version selection, or use it as a backward-compatibility probe on STDIO."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/changelog

- FINDING: Standard HTTP request headers `Mcp-Method` and `Mcp-Name` are now REQUIRED on every
  Streamable HTTP POST: "`Mcp-Method` [required for] All requests" and "`Mcp-Name` [required for]
  `tools/call`, `resources/read`, `prompts/get` requests ... These headers are REQUIRED for
  compliance." Their explicit purpose is intermediary routing/inspection without body parsing:
  "The Streamable HTTP transport mirrors selected JSON-RPC body fields into HTTP headers so that
  intermediaries (load balancers, gateways, observability tooling) can route and inspect requests
  without parsing the body." An additional `x-mcp-header` mechanism lets a tool's `inputSchema`
  designate specific parameters to be mirrored into `Mcp-Param-{Name}` headers (e.g. a `region`
  parameter used for gateway routing), with a mandatory Base64 sentinel encoding
  (`=?base64?...?=`) for non-ASCII/unsafe values.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

- FINDING: Header/body consistency is a hard security requirement for any component that trusts
  the headers, precisely because of split-brain gateway risk: "Servers that process the request
  body MUST reject requests where the values specified in the headers do not match the
  corresponding values in the request body. This prevents potential security vulnerabilities when
  different components in the network rely on different sources of truth (e.g., a load balancer
  routing on the header value while the MCP server executes based on the body value)." Mismatches
  return HTTP 400 with JSON-RPC error `-32020` (`HeaderMismatch`). There is also an explicit
  warning for gateways enforcing policy off these headers: "Intermediaries that enforce policy
  based on mirrored headers (e.g., routing or rate-limiting by tenant) SHOULD verify that the
  `MCP-Protocol-Version` header indicates a version that requires header–body validation. If the
  version is older or the header is absent, the intermediary SHOULD reject the request rather than
  trusting unvalidated header values." This is directly relevant to any enterprise gateway that
  wants to do AuthZ/metering by header alone — it must not trust `Mcp-Method`/`Mcp-Name`/
  `Mcp-Param-*` from older-protocol clients where no such validation exists.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

- FINDING: Statelessness/no-session design also changes DNS-rebinding and Origin-validation
  guidance, which remains from earlier revisions: "Servers MUST validate the Origin header on all
  incoming connections to prevent DNS rebinding attacks ... If the Origin header is present and
  invalid, servers MUST respond with HTTP 403 Forbidden." "When running locally, servers SHOULD
  bind only to localhost (127.0.0.1) rather than all network interfaces (0.0.0.0)." "Servers
  SHOULD implement proper authentication for all connections."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

## Code / Config

Example 401 challenge with scope guidance (Scope Selection Strategy):

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         scope="files:read"
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

Example runtime insufficient-scope (step-up) challenge:

```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
                         scope="files:write",
                         resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         error_description="File write permission required for this operation"
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

Client ID Metadata Document example:

```json
{
  "client_id": "https://app.example.com/oauth/client-metadata.json",
  "client_name": "Example MCP Client",
  "client_uri": "https://app.example.com",
  "logo_uri": "https://app.example.com/logo.png",
  "redirect_uris": [
    "http://127.0.0.1:3000/callback",
    "http://localhost:3000/callback"
  ],
  "grant_types": ["authorization_code"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none"
}
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration

AS advertising CIMD support:

```json
{ "client_id_metadata_document_supported": true }
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration

`tools/call` request showing `Mcp-Method`/`Mcp-Name` headers plus stateless `_meta`:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_weather

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": { "location": "Seattle, WA" },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": { "name": "ExampleClient", "version": "1.0.0" },
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

`x-mcp-header`-annotated tool parameter mirrored into a gateway-routable header:

```json
{
  "name": "execute_sql",
  "description": "Execute SQL on Google Cloud Spanner",
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "x-mcp-header": "Region" },
      "query": { "type": "string" }
    },
    "required": ["region", "query"]
  }
}
```
producing `Mcp-Param-Region: us-west1` on the wire.
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

Header-mismatch error shape (gateway/server MUST reject on divergence):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": { "code": -32020, "message": "Header mismatch: Mcp-Name header value 'foo' does not match body value 'bar'" }
}
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

Enterprise-Managed Authorization client capability declaration:

```jsonc
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "...",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/enterprise-managed-authorization": {}
        }
      }
    }
  }
}
```
SOURCE: https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization

URL-mode elicitation request/response for a sensitive value (API key):

```json
{
  "method": "elicitation/create",
  "params": {
    "mode": "url",
    "url": "https://mcp.example.com/ui/set_api_key",
    "message": "Please provide your API key to continue."
  }
}
```
```json
{ "action": "accept" }
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation

## Caveats / Gaps

- The MCP spec version referenced throughout is **2026-07-28**, confirmed live at
  modelcontextprotocol.io alongside a companion blog release post and an explicit release-
  candidate post that preceded it (https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/).
  This is materially different from the 2025-06-18 and 2025-11-25 revisions I would otherwise
  default to from training data; every quote in this document was pulled live from the
  `/specification/2026-07-28/...` and `/docs/2026-07-28/...` paths, not from memory.
- Enterprise-Managed Authorization / ID-JAG is a **stable extension**, not core protocol — it is
  optional, opt-in, and client support varies (check the client support matrix referenced on its
  page, which I did not fetch directly: https://modelcontextprotocol.io/extensions/client-matrix).
  Treat any "MUST" language inside the extension spec as scoped to implementers who choose to
  adopt the extension, not as a core-spec requirement.
- The MCP Registry is explicitly **preview**, not GA — "Breaking changes or data resets may occur
  before general availability." Any best-practices guidance built on it should flag this and
  recommend enterprise consumers build on/behind a downstream subregistry or aggregator rather
  than depending on the public registry's API stability directly.
- Token exchange / OBO for downstream calls: the spec states an MCP server "may act as an OAuth
  client" to upstream APIs and must mint a separate token, but it does **not** mandate a specific
  grant type (e.g., RFC 8693 Token Exchange, client-credentials, or a stored refresh token per
  user). This is a documented gap — the best-practices doc should recommend a concrete pattern
  (e.g., OBO/token exchange, or per-user stored upstream credentials via URL-mode elicitation) as
  guidance beyond what the spec itself prescribes, and should label it explicitly as
  recommendation, not spec quote.
- DCR (Dynamic Client Registration, RFC 7591) is "deprecated," not removed — it remains valid for
  backward compatibility. The changelog is explicit only about deprecation, not a removal date;
  the client-registration page says CIMD is preferred and DCR should not be adopted by new
  implementations.
- `iss` validation (RFC 9207) is currently SHOULD on the authorization-server side but MUST on the
  client side once present; the spec text itself flags this as a transitional state ("A future
  revision of this specification is expected to upgrade authorization server inclusion of `iss`
  from SHOULD to MUST"). Best-practices guidance should treat AS-side `iss` emission as a strong
  SHOULD today, trending to MUST.
- URL-mode elicitation is flagged in-spec as young/evolving: "New feature: URL mode elicitation is
  introduced in the `2025-11-25` version of the MCP specification. Its design and implementation
  may change in future protocol revisions." Treat detailed URL-mode elicitation guidance as
  correct for 2026-07-28 but subject to change.
- I did not independently fetch/verify: the MCP Authorization Extensions repository's full list of
  extensions (only Enterprise-Managed Authorization was verified in depth), the client support
  matrix, the `server.json` JSON Schema file itself, or the registry's moderation-policy page. Any
  claim in this document about "which clients support X" beyond what's quoted above should be
  treated as unverified and re-checked before publishing.
- Tool annotations (readOnlyHint etc.) content was sourced from the MCP blog's dedicated post
  (https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/) rather than the core
  JSON schema/spec page for `ToolAnnotations` itself; the core schema page was not independently
  fetched in this research pass, so exact default-value wording should be cross-checked against
  `/specification/2026-07-28/schema` before quoting it as normative spec text rather than blog
  explainer text.

## Implications for a best-practices doc

- MUST-candidate: "An MCP server MUST reject any bearer token not issued specifically for it
  (audience-bound via RFC 8707), and MUST NOT forward client-supplied tokens to any downstream
  API — including its own upstream integrations." Traced to: MCP servers MUST NOT accept or
  transit any other tokens (authorization spec) + Token Passthrough mitigation (security best
  practices), both at modelcontextprotocol.io/specification/2026-07-28/basic/authorization and
  .../docs/2026-07-28/tutorials/security/security_best_practices.
- MUST-candidate: "Any MCP server acting as a proxy to a third-party API MUST perform its own
  independent OAuth flow / token exchange to obtain the upstream token, and MUST implement
  per-client user consent before forwarding to a third-party AS if it uses a static client ID
  there." Traced to: Confused Deputy Problem mitigation, security best practices page.
- SHOULD-candidate: "Enterprises deploying MCP clients/servers at scale SHOULD evaluate the
  Enterprise-Managed Authorization extension (ID-JAG) for centralized IdP-driven access control
  and revocation, rather than building custom per-app SSO integration, but treat it as an opt-in
  extension requiring explicit client support, not a core-spec guarantee." Traced to:
  modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization.
- MUST-candidate: "MCP clients deployed server-side MUST apply SSRF protections (HTTPS
  enforcement, private-IP-range blocking, egress proxying) to every URL fetched during OAuth
  metadata discovery, because these URLs are attacker-influenced by definition (they originate
  from an untrusted MCP server's metadata)." Traced to: SSRF section, security best practices
  page.
- MUST-candidate: "Servers MUST NOT treat possession of any application-level state handle (cart
  ID, workflow ID, session token minted by the server) as proof of identity; every request MUST
  be independently authenticated and the handle MUST be bound server-side to the authenticated
  subject." Traced to: State Handle Hijacking, security best practices page — directly a
  consequence of the 2026-07-28 statelessness change.
- MUST-candidate: "Servers MUST NOT collect credentials, API keys, or payment data via form-mode
  elicitation; such data collection MUST use URL-mode elicitation directed to a server-hosted,
  HTTPS page that independently verifies the requesting user's identity before accepting input."
  Traced to: Elicitation spec, Form Mode Security + Phishing subsections.
- SHOULD-candidate: "Enterprise gateways that enforce authorization/rate-limiting/tenant policy
  using the `Mcp-Method`/`Mcp-Name`/`Mcp-Param-*` headers SHOULD verify `MCP-Protocol-Version`
  indicates a revision that mandates header/body validation before trusting those headers, and
  MUST reject requests where header and body diverge if they process the body themselves." Traced
  to: Streamable HTTP transport spec, Server Validation section.
- SHOULD-candidate: "Best-practices guidance SHOULD instruct implementers to design scope
  taxonomies for least privilege from day one (no wildcard/omnibus scopes, minimal baseline scope,
  incremental step-up), because MCP's step-up-authorization flow is a first-class, normative
  mechanism (403 + `insufficient_scope` + `WWW-Authenticate scope=`), not a workaround." Traced
  to: Scope Selection Strategy / Scope Challenge Handling (authorization spec) + Scope
  Minimization (security best practices).
- SHOULD-candidate: "Treat the public MCP Registry as a discovery/metadata layer only — not a
  trust or vulnerability-scanning authority — and prefer an internal/enterprise subregistry (built
  on the same OpenAPI contract) for governed server catalogs, since the official registry
  explicitly does not support private servers and delegates security scanning to package
  registries/aggregators." Traced to: modelcontextprotocol.io/registry/about.
- MUST NOT-candidate: "Clients MUST NOT treat tool annotations (`readOnlyHint`, `destructiveHint`,
  `idempotentHint`, `openWorldHint`) as security guarantees from untrusted servers; human
  confirmation for destructive/open-world operations MUST be enforced independently of what a
  server claims about itself." Traced to: MCP blog, Tool Annotations as Risk Vocabulary.
- MUST-candidate for stdio deployments: "stdio-transport MCP servers MUST source credentials from
  the process environment (env vars, OS keychain, injected secrets) rather than implementing the
  OAuth 2.1 flow, and clients performing one-click local server setup MUST show the full launch
  command and obtain explicit consent before execution." Traced to: core authorization spec
  (stdio SHOULD NOT follow the OAuth flow) + Local MCP Server Compromise, security best practices.

## Sources

- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization — Authorization (core spec)
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations — Authorization Security Considerations
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery — Authorization Server Discovery
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration — Client Registration
- https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices — Security Best Practices
- https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation — Elicitation (form/URL modes)
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports — Transports overview
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http — Streamable HTTP transport
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio — stdio transport
- https://modelcontextprotocol.io/specification/2026-07-28/changelog — Key Changes (2025-11-25 → 2026-07-28)
- https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization — Enterprise-Managed Authorization extension
- https://github.com/modelcontextprotocol/ext-auth/blob/main/specification/stable/enterprise-managed-authorization.mdx — EMA stable specification
- https://modelcontextprotocol.io/registry/about — The MCP Registry
- https://blog.modelcontextprotocol.io/posts/2026-07-28/ — The 2026-07-28 Specification (release blog post)
- https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ — 2026-07-28 Release Candidate post
- https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ — Tool Annotations as Risk Vocabulary
- https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/ — Enterprise-Managed Authorization: Zero-touch OAuth for MCP (blog)
