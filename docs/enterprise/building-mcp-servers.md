---
title: Building MCP servers in the enterprise
description: Framework-neutral best practices for designing, securing, publishing and operating MCP servers in an enterprise, including tool design, large tool catalogues, integrity and supply chain. With Azure mappings.
tags:
  - Go deeper
  - MCP
  - Safety
  - Azure
---

# Building MCP servers in the enterprise

!!! abstract "Go deeper · 45 min · no code"
    **Before this:** [Building agents in the enterprise](building-agents.md)  ·  **After this:** [Architecture patterns](../patterns/index.md)
    **Hands-on version:** [1 Tool calling](../02-agents/tool-calling.md)  ·  **In depth:** [Model Context Protocol](../ai-dev-tools/mcp.md)

!!! abstract
    An MCP server is an API whose caller is a model. That changes three things. The
    caller chooses tools by reading their descriptions, so descriptions are part of
    the interface. The caller can be manipulated by anything it reads, so the server
    cannot trust what it is asked to do. And every tool definition is text that goes
    straight into a model's context, so the server is also a prompt-injection
    surface for every agent that connects. These practices cover all three.

**Verified as of 2026-09-17** against MCP specification revision `2026-07-28`.
Rule levels (**MUST**, **SHOULD**, **AVOID**) are defined on
[Identity and authorization](identity-and-authorization.md#how-to-read-these-pages),
which also holds the AUTH-xx rules referred to here.

## Should this be an MCP server at all?

Build an MCP server when a capability will be used by **more than one** agent or AI
client, or by clients you do not control, such as developers' coding assistants or
Copilot. If one agent calls one internal function, an ordinary tool inside that
agent is simpler, faster and has a smaller attack surface.

An MCP server is also not a replacement for your API. Put it in front of an
existing, already-secured API, and keep business rules and authorization in that
API (AUTH-16), so they hold for every caller, AI or not.

## Scope and tool design

### MCP-01 One server per bounded context — SHOULD

A server covers one business domain, owned by the team that owns that domain:
claims, policy administration, document management. Avoid a single "enterprise
MCP server" that exposes everything. If a server must stay broad, group its tools
into toolsets that clients can switch on individually.

**Why:** small servers are easier to authorize, review, version and retire, and
they keep tool lists short (MCP-08). GitHub's official MCP server takes the toolset
approach and says so directly: enabling only the toolsets you need helps the model
choose and reduces context size.

This rule is a recommended pattern, not a requirement of the MCP specification.

### MCP-02 Tools are shaped around tasks, not endpoints — SHOULD

Design tools around what an agent is trying to do, not as one tool per REST
endpoint. One `schedule_inspection` tool that checks availability and books a slot
is better than separate `list_inspectors`, `list_slots` and `create_booking` tools
the model has to chain correctly.

**Why:** Anthropic's tool-design guidance puts it plainly: more tools do not always
lead to better outcomes. Each extra step is another chance to pick the wrong tool or
pass the wrong ID.

### MCP-03 Reads and writes are separate tools — MUST

A tool either reads or changes state, never both depending on an argument. Write
tools are clearly named as such. The server can run in a read-only mode that does
not register write tools at all.

**Why:** clients and policies decide approval per tool (AGT-18). A `manage_claim`
tool with an `action` parameter makes that impossible.

### MCP-04 Tool names follow the specification and are namespaced — MUST

Names follow the rules in the `2026-07-28` specification: 1 to 128 characters,
case-sensitive, using only letters, digits, underscore, hyphen and dot, and unique
within the server. The specification states these as SHOULDs; treat them as a
MUST internally, so every client accepts your tools. Use a consistent domain
prefix, such as `claims.get_status` or `claims_get_status`, so tools stay
distinguishable when a client loads several servers.

**Avoid:** following older guides that allow `/` in names or cap them at 64
characters. That was an earlier proposal, and the current specification replaced
it.

**Why:** clients that combine servers have to disambiguate collisions such as two
`search` tools, and the specification warns that a server's own name is not
guaranteed unique enough to do it. Anthropic also found that the naming convention
you choose measurably changes tool-selection results, so pick one and keep it.

### MCP-05 Descriptions are written for the model — MUST

Every tool has a description that says what it does, when to use it, when **not**
to use it, what each parameter means with units and formats, and what it returns.
Treat descriptions as the most important part of the interface, and test changes to
them (MCP-28).

**Why:** Anthropic reports that tools written by people scored roughly 60 to 70% on
its internal evaluations, and descriptions refined against evaluations scored 80
to 90% on the same held-out tasks. Microsoft's tool search documentation notes that
a tool with a vague description is unlikely to be found at all.

**Avoid:** instructions to the model inside descriptions ("always call this tool
first", "do not tell the user"). That is the exact shape of a tool-poisoning attack,
and scanners flag it.

### MCP-06 Schemas are strict — MUST

Every tool has an `inputSchema` with types, formats, enumerations, required fields
and `additionalProperties: false` where possible, and the server validates input
against it before doing anything. Declare an `outputSchema` for structured results
so clients can validate them.

**Why:** the schema is the only part of a tool call that is not free text. Anything
it does not constrain, the model will eventually get creative with.

### MCP-07 Responses are compact and errors are actionable — SHOULD

Return what the agent needs to take the next step, not the raw backend payload:
names alongside IDs, pagination with sensible defaults, and truncation that says
how to narrow the query. Report failures as tool execution errors (`isError: true`)
with text that tells the model how to correct the call, such as *"Invalid date:
must be in the future"*, not a stack trace.

**Why:** every token a tool returns is paid for and competes for context. The
specification notes models can self-correct from execution errors, and are less
likely to recover from protocol errors.

## Large tool catalogues

Tool selection gets worse, and more expensive, as the number of tools in front of a
model grows. That is documented by every major vendor and by independent
benchmarks, so plan for it from the start.

| Evidence | Source |
|---|---|
| Accuracy rose from 49% to 74% on one model, and from 79.5% to 88.1% on another, when tools were searched on demand instead of all loaded; tool-definition tokens fell by about 85% | Anthropic, advanced tool use |
| With 600+ tools, on-demand search cut input tokens per call from over 313K to 18K | Microsoft Foundry, tool search |
| "Aim for fewer than 20 functions available at the start of a turn", explicitly a soft suggestion | OpenAI, function calling guide |
| Retrieving relevant tools more than tripled selection accuracy on a large catalogue (43% against 14%) | RAG-MCP, arXiv 2505.03275 |
| On a 527-tool benchmark, retrieval errors caused nearly half of all task failures | LiveMCPBench, arXiv 2508.01780 |
| GitHub's MCP server alone used about 42,000 tokens of tool definitions | Practitioner measurement |

### MCP-08 Keep the tools in front of the model small — MUST

Design so that an agent sees a small set of relevant tools at any one time. Treat
around 20 as a practical ceiling, and start using the techniques in MCP-10 once a
client would load more than 10 to 15. Measure selection accuracy on your own tasks
rather than trusting any number, including these.

### MCP-09 List only the tools the caller may use — SHOULD

Filter `tools/list` by the caller's authorization, so a user without write access
never sees write tools. The `2026-07-28` specification explicitly allows the list to
*"vary by the authorization presented on the request"*. Still enforce authorization
on every call (MCP-12); filtering is about accuracy and exposure, not a substitute
for checks.

### MCP-10 Use on-demand discovery for large catalogues — SHOULD

When the combined tools across an agent's servers exceed what MCP-08 allows, use
one of these, in rough order of preference:

1. **Toolsets:** the client enables only the groups a task needs.
2. **Tool search:** tools are marked for deferred loading, and the model searches
   for them by description. Anthropic, OpenAI and Microsoft Foundry all ship a
   version.
3. **Sub-agents:** a router hands work to sub-agents that each hold a handful of
   tools. OpenAI suggests four to six.
4. **Code execution over tools:** the agent writes code against tools presented as
   an API, keeping intermediate data out of context. Anthropic's example cut one
   workflow from 150,000 tokens to 2,000. It needs a sandbox (AGT-12), so it moves
   the risk rather than removing it.

**On Azure:** Foundry toolboxes support `toolbox_search`, with `pin` for tools that
must always be visible.

### MCP-11 Tool lists are stable and ordered — SHOULD

Return tools in a deterministic order, and do not change the list from one request
to the next without a reason. The specification recommends this so clients can
cache the list and model providers can reuse prompt caches.

## Authorization

The rules on [Identity and authorization](identity-and-authorization.md) apply in
full. These are the ones specific to MCP servers.

### MCP-12 Remote servers implement the specification's authorization — MUST

A server on an HTTP transport:

- publishes OAuth 2.0 Protected Resource Metadata (RFC 9728) so clients can discover
  its authorization server;
- validates on every request that the token was issued for this server as its
  audience (RFC 8707), along with issuer, expiry and scopes (AUTH-06);
- responds `401` with a `WWW-Authenticate` challenge when unauthenticated, and `403`
  with `insufficient_scope` when a tool needs more, naming the scope required;
- never accepts or forwards a token issued for anything else (AUTH-05).

A local server on the stdio transport takes credentials from its environment
instead, so the rules for that environment apply: no long-lived personal tokens in
client configuration files (AUTH-14).

### MCP-13 Authorization is checked per tool and per resource — MUST

A valid token gets a caller into the server. It does not authorize every tool, or
every record. Each tool checks the scope it requires and the caller's right to the
specific resource, including tenant ownership (AUTH-17).

### MCP-14 Downstream calls use the server's own delegated token — MUST

To call a backend API for the user, the server exchanges the token it received for
a new token issued for that backend, or uses a token held in a managed credential
store. It never forwards the client's token. The specification does not say which
exchange to use; the on-behalf-of flow (RFC 8693 token exchange) is the usual
choice on an enterprise identity provider.

**On Azure:** the Entra on-behalf-of flow, or API Management credential manager
injecting the backend token so the server code never holds it.

### MCP-15 Scopes are designed, not accumulated — MUST

Define a small set of scopes that match real permission boundaries, starting with a
minimal baseline and adding narrower ones for sensitive operations. The MCP
security guidance lists the common mistakes: publishing every scope in
`scopes_supported`, wildcard scopes, bundling unrelated privileges, and changing
what a scope means without versioning it.

### MCP-16 Secrets are never collected through the model — MUST

When a server needs a user to supply a credential, API key or payment detail, it
uses URL-mode elicitation, which opens a page the server hosts, outside the
client and the model. The specification says servers *"MUST NOT use form mode
elicitation to request sensitive information"*. The page confirms that the person
completing it is the user who started the request.

### MCP-17 Protect against server-side request forgery — MUST

Any server or client component that fetches a URL it did not choose, including
OAuth metadata URLs, resource links and user-supplied addresses, allows only
`https`, blocks private, loopback and link-local ranges including cloud metadata
addresses, and re-checks after redirects. The MCP security guidance names OAuth
metadata discovery specifically as a path for this attack.

## Trust and integrity

### MCP-18 Annotations are accurate, and never trusted blindly — MUST

Server authors set `readOnlyHint`, `destructiveHint`, `idempotentHint` and
`openWorldHint` honestly on every tool. Client owners treat them as hints: the MCP
project states that clients *"must treat them as untrusted unless they come from a
trusted server"*. Unannotated tools are assumed destructive and open-world.

### MCP-19 Tool definitions are pinned and changes are reviewed — MUST

When a server is approved, record a hash of each tool's name, description and
schemas. Re-review when any of them change, and block the changed tool until then.
Pin server versions; do not let clients update automatically.

**Why:** a *rug pull* is a server that passes review and then changes its tool
descriptions afterwards. The protocol has no built-in way to notice. Invariant
Labs showed in April 2025 that a single poisoned description can make an agent
exfiltrate files while showing the user a normal answer.

### MCP-20 Tool output that carries outside content is marked as untrusted — SHOULD

A tool that returns text from outside the organisation, such as emails, web
pages, tickets or public issues, returns it as clearly delimited data, with its
source, and never mixes it into text that reads as instructions. This does not stop
prompt injection (AGT-09), but it helps clients and filters treat it correctly.

**Why:** in the GitHub MCP exploit, the injection arrived as the body of a public
issue returned by an ordinary read tool.

### MCP-21 The server holds the least privilege it can — MUST

The server's own identity reaches only what its tools need. It does not connect to
databases with owner or superuser credentials, or with keys that bypass row-level
security. File tools enforce real path boundaries, resolving symbolic links and
comparing whole path segments, not string prefixes.

**Why:** the Supabase MCP leak used a `service_role` key that bypassed row-level
security. Anthropic's own reference filesystem server had two CVEs (CVE-2025-53109
and CVE-2025-53110) in 2025 because its allow-list compared path prefixes and did
not handle symbolic links.

## Supply chain and registry

### MCP-22 Clients connect only to approved servers from a private registry — MUST

The organisation keeps a registry of reviewed MCP servers, and clients and gateways
are configured to connect only to servers in it. Installing an arbitrary server
from a public list is treated like installing arbitrary software, because it is.

**Why:** the public MCP Registry is still in preview, does not list private servers,
and delegates security scanning to package registries. It checks who published a
server name, not whether the server is safe.

**On Azure:** Azure API Center provides an MCP registry with a standard discovery
endpoint that VS Code and GitHub Copilot can point at, and it can sync from API
Management. GitHub Copilot also supports an enterprise MCP allow-list.

### MCP-23 Verify the publisher and pin the package — MUST

Before approval, confirm the package comes from the vendor it claims to, by
checking the vendor's own documentation, and pin an exact version. Review the diff
before approving an upgrade.

**Why:** in September 2025 a fake `postmark-mcp` package on npm, which Postmark never
published, built trust over fifteen clean releases and then added one line that
blind-copied every email it sent to the attacker.

### MCP-24 Scan servers, and treat the result as a signal — SHOULD

Run an MCP scanner on candidate servers and on every version change, to catch
poisoned descriptions, hidden instructions and risky tool combinations. Current
scanners describe their own output as unstable, so use them to inform review, not
as the only gate.

**Tools:** Snyk Agent Scan (formerly Invariant's `mcp-scan`) and Cisco's
`mcp-scanner` are open source.

## Deployment

### MCP-25 Remote servers sit behind a gateway — SHOULD

Put remote MCP servers behind a gateway that validates tokens, applies rate and
quota limits, logs every call, and blocks servers not in the registry. The gateway
adds a layer; the server still validates tokens itself (AUTH-06).

The `2026-07-28` specification requires `Mcp-Method` and `Mcp-Name` headers so
gateways can route and apply policy without parsing the body. Servers must reject
requests where the headers and the body disagree, and gateways that enforce policy
on those headers should reject requests from protocol versions that do not require
that check.

**On Azure:** API Management can govern an existing MCP server or expose a REST API
as one, with `validate-azure-ad-token`, rate limits and content safety policies.
agentgateway and IBM ContextForge are open-source gateways with per-tool
authorization rules.

### MCP-26 Local servers are locked down — MUST

A server that runs on a user's machine uses the stdio transport where possible. If it
uses HTTP, it binds to `127.0.0.1`, never `0.0.0.0`, validates the `Origin` header,
and requires authentication. Clients show the exact command before launching a
server for the first time.

**Why:** Anthropic's MCP Inspector (CVE-2025-49596) let any website a developer
visited launch commands on their machine, because the local proxy had no
authentication. `mcp-remote` (CVE-2025-6514) passed an authorization URL from a
malicious server straight to the operating system shell.

### MCP-27 Servers run in containers with no more than they need — SHOULD

Remote servers run as non-root containers with read-only file systems where
possible, egress limited to their backends, resource limits, and health checks.
Servers that execute code or commands follow the sandbox rules in AGT-12 to AGT-15.

## Operations

### MCP-28 Tool changes are tested like API changes — MUST

A change to a tool's name, description, schema or behaviour runs the evaluation
suite of the agents that use it before release (AGT-31). Description wording
changes selection accuracy, so a "documentation-only" change is still a
behavioural change.

### MCP-29 Tools are versioned and deprecated deliberately — SHOULD

Do not change what an existing tool does or means in place. Add a new tool or
version, mark the old one deprecated in its description, and remove it after a
published window. Consumers are agents you may not know about.

### MCP-30 Every tool call is audited — MUST

Each call records the caller's agent identity, the user it acted for, the tool, the
arguments with sensitive values redacted, the result status and duration, and the
correlation ID from the calling agent (AGT-28). OWASP's MCP Top 10 lists missing
audit and telemetry as MCP08.

## The incidents behind the rules

| Incident | What went wrong | Rules that would have stopped it |
|---|---|---|
| Tool poisoning demonstration (Invariant Labs, Apr 2025) | Hidden instructions in a tool description | MCP-05, MCP-19, MCP-24 |
| GitHub MCP private repository leak (May 2025) | Broad personal token plus injection through a public issue | MCP-15, MCP-20, AUTH-13 |
| Asana MCP cross-organisation exposure (Jun 2025) | Tenant context not re-checked | MCP-13, AUTH-17 |
| Supabase MCP database leak (Jul 2025) | Server key bypassed row-level security | MCP-21, AGT-03 |
| Filesystem MCP server CVEs (Jul 2025) | Path prefix check and symbolic links | MCP-21 |
| `mcp-remote` RCE, CVE-2025-6514 (Jul 2025) | Untrusted authorization URL passed to a shell | MCP-17, MCP-26 |
| MCP Inspector RCE, CVE-2025-49596 (2025) | Unauthenticated local proxy | MCP-26 |
| Malicious `postmark-mcp` package (Sep 2025) | Impersonated publisher, trojanised update | MCP-22, MCP-23 |

## Where to do this on Azure

| Control | Azure service or feature | Rules |
|---|---|---|
| Private MCP registry | Azure API Center MCP registry, synced from API Management | MCP-22 |
| Gateway, token validation, rate limits | API Management: govern an existing MCP server, or expose a REST API as one | MCP-12, MCP-25 |
| Downstream credentials | API Management credential manager; Entra on-behalf-of flow | MCP-14 |
| Content safety on tool traffic | API Management `llm-content-safety`, which also covers MCP tools | MCP-20 |
| Tool search for large catalogues | Foundry toolboxes with `toolbox_search` | MCP-10 |
| Hosting | Azure Container Apps, Azure Functions or AKS, with managed identity | MCP-27 |
| Audit | API Management logging to Azure Monitor and Microsoft Sentinel | MCP-30 |

## Gotchas

- **Old tutorials are wrong in structural ways.** The `2026-07-28` specification
  removed the `initialize` handshake and protocol sessions, and deprecated Dynamic
  Client Registration. Check the revision date of anything you copy.
- **API Management's MCP support covers tools only**, not MCP resources or prompts.
  Check the current status of exposing a REST API as an MCP server before you
  design around it.
- **The public MCP Registry is in preview.** Its own documentation warns that
  breaking changes and data resets may happen before general availability, and it
  is not meant to be consumed by clients directly.
- **Filtering tools does not authorize them.** A tool hidden from `tools/list` can
  still be called by name. MCP-09 never replaces MCP-13.
- **There is no portable policy engine for tool calls yet.** OPA and Cedar are
  general-purpose. Today, per-tool policy lives in gateway configuration or in the
  server's own code.
- **A read-only server can still leak data.** If its results reach an agent that can
  write or send anywhere, the agent completes the exfiltration path (AGT-03).

!!! question "Take this to your architecture team"
    - The server will be reachable from outside your network, or by clients you do
      not control.
    - The server will run commands or code, or accept file paths or URLs as input.
    - A tool needs write access to a system of record, or access across tenants.
    - You want to adopt a third-party or open-source MCP server that is not in your
      registry.
    - The backend can only be called with the original user's token.

## Go deeper

- [MCP specification: tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) — naming rules, schemas, error handling and per-caller tool lists, in the revision this page was checked against.
- [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) — every attack in the authorization section, with its mitigation.
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — the best single guide to tool design, including how to evaluate a description change.
- [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) — the accuracy and token numbers for tool search, and when it pays off.
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) — MCP-specific risks from token mismanagement to shadow servers. Still in beta, so IDs may change.
- [Secure access to MCP servers in API Management](https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers) — inbound token validation and outbound credential injection, with policy examples.
- [Inventory and discover MCP servers in API Center](https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server) — running a private registry that clients can point at.
- [Tool poisoning attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) — the original demonstration. Read it once and tool descriptions will never look harmless again.

## Next

[Model Context Protocol](../ai-dev-tools/mcp.md) — the protocol itself: primitives,
transports and what changed in `2026-07-28`.
