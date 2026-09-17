# Official Docs Research: Microsoft/Azure Identity, Authorization and Governance for Agents and MCP Servers
SOURCE_TYPE: official-docs
CONFIDENCE: HIGH
GENERATED: 2026-09-17T00:00:00+05:30

## Summary

Microsoft has built a purpose-built identity layer for AI agents — **Microsoft Entra Agent ID** — that is distinct from ordinary app registrations/service principals, plus a growing set of governance and runtime-protection products (**Microsoft Agent 365**, **Microsoft Purview DSPM for AI**, **Microsoft Defender for Cloud AI threat protection**) that sit on top of it. Agents authenticate either autonomously (client-credentials/app-only, using an **agent identity** created from an **agent identity blueprint**) or on behalf of a signed-in user (a formal **OBO flow with agent-specific impersonation**, not user-token forwarding). **Azure API Management** is Microsoft's recommended AI/MCP gateway — it can expose existing REST APIs as MCP servers, front existing MCP servers, validate Entra tokens, inject downstream OAuth credentials via credential manager, and enforce token-limit/content-safety policies. **Azure API Center** is the recommended private MCP/tool registry, with its own MCP registry endpoint and (as of Build 2026) a GA "data-plane MCP server" for unified discovery. **Microsoft Foundry Agent Service** (GA March 2026) authenticates MCP tools via key-based, Microsoft Entra (agent identity or project managed identity), or OAuth identity passthrough, and explicitly blocks forwarding Microsoft-audience tokens to untrusted third-party MCP endpoints. Governance is unified conceptually by the Cloud Adoption Framework's AI agents guidance, which recommends a single agent registry, one identity per agent, least privilege, mandatory AI threat protection, and adversarial (red-team) testing before production.

## Key Findings

### 1. Microsoft Entra Agent ID

- FINDING: An **agent identity** is a specialized Microsoft Entra ID identity construct (not a plain service principal) designed for the dynamic, ephemeral, bulk-created nature of AI agents; it enables autonomous access, delegated (OBO) access, and authenticating incoming requests from other agents/clients.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities
- FINDING: Agent ID is available to all Microsoft Entra customers at no extra license for the base identity object; however, extending Microsoft Entra security features (Agent 365 integration, Conditional Access for agents, ID Protection for agents) to agents requires a **Microsoft Agent 365** license per user (included in Microsoft 365 E7; add-on for E5/A5/Business Premium or Defender+Purview suites).
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities
- FINDING: An **agent identity blueprint** is the Entra object that acts as a template: it defines credentials, permissions (required resource access, inheritable permissions), and auth-protocol settings for all agent identities created from it. A blueprint can only provision/deprovision agent identities (via the `AgentIdentity.CreateAsManager` Graph permission) — it cannot itself act as an agent. Disabling a blueprint blocks all its child agent identities (a kill switch).
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-blueprint
- FINDING: Existing agents created before Entra Agent ID rolled out (May 2026) continue to use plain app registrations; new agents should use the Agent ID framework and never `az ad app create` / `New-MgApplication` / `New-AzADApplication` / `POST /applications` to represent an agent.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id
- FINDING: **Agent's user accounts** are special Entra user accounts paired 1:1 with an agent identity, used only when an agent must act like a human (mailbox, Teams presence, group membership). Best practice: create them only when strictly necessary; prefer app credentials alone.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities ; https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id
- FINDING: Three agent access patterns exist, each with different Conditional Access targeting: (1) **agent acting on behalf of a user** (OBO/delegated — CA policies target users/groups, not the agent identity), (2) **agent acting as an application** (client-credentials/app-only — CA targets the agent identity or its blueprint), (3) **agent acting as a user** (agent's user account — CA targets the agent's user account, treated as an autonomous agent even though it has a user identity).
  SOURCE: https://learn.microsoft.com/en-us/entra/identity/conditional-access/agent-id
- FINDING: **Conditional Access for agents** requires Microsoft Entra ID P1/P2 **and** an Agent 365 license per user (enforcement of the Agent 365 licensing requirement is "coming soon" as of the doc's last update); network controls for agents additionally require Microsoft Entra Internet Access. Policies can target an agent identity blueprint (covers all agents created from it, including future ones) or use custom security attributes for attribute-driven targeting.
  SOURCE: https://learn.microsoft.com/en-us/entra/identity/conditional-access/agent-id
- FINDING: Conditional Access boundaries/limitations: it does **not** apply when a blueprint acquires a token to create an agent identity/agent user account, when a token exchange happens against the `AAD Token Exchange Endpoint: Public` (resource ID `fb60f99c-7a34-4190-8149-302f77469936`), when Security Defaults are enabled, or when an agent authenticates via an API key instead of Entra tokens. Policies targeting "all users" do **not** include agent's user accounts; group-based scoping of agent's user accounts isn't supported yet.
  SOURCE: https://learn.microsoft.com/en-us/entra/identity/conditional-access/agent-id
- FINDING: **Microsoft Entra ID Protection for agents** (Risky Agents) automatically detects and flags risky agent behavior (e.g., accessing unfamiliar resources, high sign-in volume) with risk levels (e.g., High = strong confidence of compromise), surfaced in a **Risky Agents (Preview)** report; a "Learning Mode" suppresses false positives for agents without sufficient activity history. Conditional Access can block agents flagged as high risk. This capability is in **preview**.
  SOURCE: https://learn.microsoft.com/en-us/entra/id-protection/concept-risky-agents
- FINDING: **Sign-in logs** include a new `agentSignIn` event type and filters for **Agent type**: "Agent ID user", "Agent Identity", "Agent Identity Blueprint", "Not Agentic", plus an "Is Agent" Yes/No filter, in Entra ID > Monitoring & health > Sign-in logs. Equivalent queries are available on Microsoft Graph `/beta` (`GET /beta/auditLogs/signIns?$filter=...agent/agentType eq 'AgentIdentity'`).
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/sign-in-audit-logs-agents
- FINDING: **Audit logs** log agent activity under the base identity type: blueprint activity as application events, agent identity activity as service principal events, agent's user account activity as user events. A new `agentType` property (`notAgentic`, `agenticApp`=blueprint, `agenticAppInstance`=agent identity, `agentIdentityBlueprintPrincipal`, `agentIDuser`) and `blueprintId` property (correlating an instance to its template) appear on `auditAppIdentity`, `auditUserIdentity`, `targetResource`, and the new `auditActivityPerformer` resource type. Retrieving `agentIdentityBlueprintPrincipal`/`agentIDuser` values requires the `Prefer: include-unknown-enum-members` header (evolvable enumeration).
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/sign-in-audit-logs-agents
- FINDING: **Owners and sponsors**: every blueprint and agent identity should have an **owner** (technical admin — setup, configuration, credential management) and a **sponsor** (business owner accountable for purpose and lifecycle decisions, e.g. access reviews/retention, without technical admin access). If a sponsor leaves, Entra automatically reassigns sponsorship to the sponsor's manager. Sponsors/owners manage agent enable/disable lifecycle from the My Account portal.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/manage-owners-sponsors-agents ; https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id
- FINDING: Official best practices (selected, verbatim intent): plan blueprints before deploying agents; provision a unique identity per agent instance (never share); assign sponsor+owner at creation; apply Conditional Access/permissions at the blueprint level (a "kill switch"); use managed identities/federated credentials or certificates in production, not client secrets; store certificate keys in Azure Key Vault/HSM; align OAuth flow to scenario (client-credentials for autonomous, OBO for delegated); segment agents with custom security attributes; block high-risk agents automatically via ID Protection; include agents in periodic access reviews (sponsor attestation every 6–12 months); register every agent (no shadow AI) — treat agent configuration as code.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id

### 2. OBO flow for agents and MCP servers; what not to do

- FINDING: The agent OBO flow is a **formal protocol extension**, not simple token forwarding. Agent identity blueprints cannot initiate interactive `/authorize` flows; only supported grant types are `client_credentials`, `jwt-bearer`, and `refresh_token`. The flow: (1) user authenticates with the client, gets user token Tc; (2) client sends Tc to the agent identity blueprint; (3) blueprint exchanges its client credential (secret/certificate/**federated identity credential via managed identity**, preferred) for token T1, using `fmi_path=<AgentIdentity client id>` to specify which child agent identity it's impersonating; (4) the **agent identity** (not the blueprint) performs the actual OBO exchange, sending both T1 (as `client_assertion`) and Tc (as `assertion`) with `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer` and `requested_token_use=on_behalf_of`; (5) Entra validates and returns the resource-scoped token.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow
- FINDING: **Token audience rules** enforced by Entra: `Tc.aud` must equal the agent identity blueprint's client ID — a user token audienced to another resource (e.g., Microsoft Graph directly) is rejected with `AADSTS50013`. `T1` is obtained with `scope=api://AzureADTokenExchange/.default` (its `aud` is the token-exchange resource, not the blueprint); Entra separately validates that `T1.azp` is the blueprint and that `T1.sub` (the FMI path) resolves to the child agent identity performing the exchange. Child agent identities cannot receive interactive user consent directly (`AADSTS82014` if attempted) — permissions must be **pre-authorized as inheritable permissions on the parent blueprint**.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow
- FINDING: **What NOT to do**: don't use client secrets as blueprint credentials in production (use FIC with managed identities, or certificates); don't manually reimplement the OBO/FIC protocol — Microsoft explicitly recommends approved SDKs (Microsoft.Identity.Web, Entra ID Auth SDK/sidecar) because manual implementation is "complex and error-prone."
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow
- FINDING: Foundry Agent Service explicitly forbids forwarding a Microsoft-audience token to a third-party/custom MCP server: "Agent Service restricts tokens scoped to a known Microsoft audience from being sent to custom or third-party MCP servers" and returns the error `Cannot pass Microsoft token to untrusted MCP endpoint.` Custom MCP servers must be registered under an audience you control (bring-your-own Entra app registration / custom OAuth), i.e. an MCP server must never rely on passthrough of a Microsoft-issued token to a downstream Microsoft service.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication
- FINDING: Entra/APIM-specific MCP server guidance covers securing **inbound** access (key-based subscription key, or `validate-azure-ad-token` policy validating an Entra-issued OAuth 2.1 token in the `Authorization` header against configured client application IDs) and **outbound** access (APIM **credential manager** with `get-authorization-context` + `set-header` policies to inject a securely stored OAuth token when the MCP server tool calls a downstream API, rather than forwarding the caller's raw token).
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers
- FINDING: Microsoft references community/lab samples (not core product docs, but linked from official docs) for **Protected Resource Metadata (PRM)** authorization patterns and MCP client authorization with APIM: "MCP server authorization with Protected Resource Metadata (PRM) sample" and "Lab: MCP with protected resource metadata (PRM) authorization." These are cited from the official secure-mcp-servers page as supplementary guidance for scenarios beyond the core validate-azure-ad-token approach (e.g., where full OAuth 2.1 Dynamic Client Registration (DCR) isn't natively supported by Entra and a workaround via PRM + APIM policy is used).
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers (links to https://github.com/blackchoey/remote-mcp-apim-oauth-prm and https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/mcp-prm-oauth)
- FINDING: For **individual/delegated authentication to an MCP server from Foundry Agent Service**, use **OAuth identity passthrough**: the platform issues a per-user consent link (`oauth_consent_request` response item with `consent_link`), the user signs in and consents once per tool+project, and Agent Service securely stores and reuses the resulting credential (`offline_access` scope recommended for auto-refresh). Two sub-modes: **managed OAuth** (Microsoft or the MCP publisher manages the OAuth app) and **custom OAuth** (bring your own Entra app registration — required if you want to call a downstream Microsoft service, per the audience restriction above).
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication

### 3. Managed identity / workload identity federation; avoiding secrets

- FINDING: Managed identities are the **preferred credential type** for agent identity blueprints; the managed identity token serves as the federated credential for the blueprint, giving automatic credential rotation and secure storage without a stored secret. Protocol detail: the blueprint requests a token with `scope=api://AzureADTokenExchange/.default` using the managed-identity token as `client_assertion` (`TUAMI`), then exchanges that for the FIC used in the OBO flow.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow
- FINDING: Best practice reiterated across Entra Agent ID docs and CAF: "Standardize authentication — mandate the use of managed identities for authentication to eliminate credential management risks... removes the need for developers to handle secrets." Where certificates must be used (non-MI scenarios), store private keys in **Azure Key Vault** or an HSM and rotate at least annually.
  SOURCE: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization ; https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id
- FINDING: In Foundry Agent Service, Microsoft Entra authentication for MCP connections comes in two managed-identity flavors: **agent identity** (scoped per published agent — before publishing, all agents in a project share one agent identity; after publishing, each gets a unique one) and **project managed identity** (shared across all agents in a project, or required when the underlying MCP server needs a managed identity rather than an agent identity). Both eliminate secret management and provide automatic token rotation; role assignments (RBAC) are made on the underlying service.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication

### 4. Azure API Management as AI/MCP gateway

- FINDING: APIM can **expose an existing REST API (managed in APIM) as a remote MCP server** without rebuilding/rehosting it — API operations become MCP "tools," discoverable/callable over JSON-RPC via HTTP or SSE. Currently APIM supports MCP **tools** only (not MCP resources or prompts).
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server
- FINDING: APIM can also **front/govern an existing MCP server hosted elsewhere** ("Connect and Govern Existing MCP server"), applying the same policy pipeline (auth, rate limiting, content safety, logging) in front of a server you didn't build in APIM.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/expose-existing-mcp-server
- FINDING: Inbound MCP security options: (a) subscription-key auth (`Ocp-Apim-Subscription-Key` header); (b) **OAuth 2.1 with Microsoft Entra ID** via the `validate-azure-ad-token` policy, validating tokens against a `tenant-id` and a list of `client-application-ids`; (c) automatic forwarding of most request headers to tool invocations, with an explicit pattern to forward/re-set the `Authorization` header if needed.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers
- FINDING: **Credential manager** (APIM's OAuth token vault) securely injects OAuth 2.0 access tokens for the *outbound* calls MCP tools make to backend APIs — configured via a credential provider linked to the identity provider, connections, and the `get-authorization-context`/`set-header` policy pair (`identity-type="managed"` uses APIM's own managed identity to retrieve the stored token).
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers
- FINDING: **`validate-jwt`** enforces existence/validity of any supported JWT (generic identity provider); **`validate-azure-ad-token`** is the Entra-specific policy that validates a token issued by Microsoft Entra ID for a specified set of principals in the directory.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/validate-jwt-policy ; https://learn.microsoft.com/en-us/azure/api-management/validate-azure-ad-token-policy
- FINDING: **`llm-token-limit`** policy caps LLM token consumption per key (rate per minute and/or quota over a period), using actual token usage returned by the model endpoint; exceeding the rate returns `429`, exceeding the quota returns `403`.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy
- FINDING: **`llm-content-safety`** policy sends LLM prompts/completions — and, per the current doc, **MCP tool and A2A Agent API requests/responses** — to Azure AI Content Safety; on detection it returns `403`. Configurable: `shield-prompt` (jailbreak/prompt-injection shielding via Prompt Shields), per-category severity `threshold` (Hate/SelfHarm/Sexual/Violence, 4- or 8-level output), and `blocklists`. Requires an APIM backend pointed at the Content Safety resource with APIM's managed identity granted **Cognitive Services User** on it.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/llm-content-safety-policy
- FINDING: GA/preview status: AI Gateway capabilities (LLM policies including token-limit, content-safety) reached **GA**; at Build 2026 Microsoft added **JSON-RPC-based Agent-to-Agent (A2A) API support** and extended content-safety policies to MCP tools/A2A, and the **Azure API Center data-plane MCP server reached GA** as a unified discovery endpoint. Exposing REST APIs as MCP servers via APIM+API Center was announced "now in preview" in an earlier 2026 Community blog post; treat exact GA date for "export REST API as MCP server" as needing reverification against the live APIM feature-availability table before publishing (see Caveats).
  SOURCE: https://techcommunity.microsoft.com/blog/integrationsonazureblog/whats-new-in-azure-api-management-at-microsoft-build-2026/4524683 ; https://techcommunity.microsoft.com/blog/integrationsonazureblog/expose-rest-apis-as-mcp-servers-with-azure-api-management-and-api-center-now-in-/4415013

### 5. Azure API Center as MCP registry / private tool catalogue

- FINDING: Azure API Center maintains an **inventory (registry)** of remote and local MCP servers, alongside APIs and other AI assets, browsable/filterable in the API Center **portal**, which includes a built-in **test console** (MCP Inspector-style) so developers can try tools before wiring them in.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server
- FINDING: You can register **remote MCP servers** (by runtime URL + API Center environment), **local MCP servers** (by package registry/name/version, e.g. npm/pypi, with runtime hint like `npx`), or **partner MCP servers** from a curated Microsoft list (GitHub, Azure Logic Apps, etc.) with one click. API Center auto-generates OpenAPI-style SSE and Streamable definitions for remote MCP servers.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server
- FINDING: API Center exposes a standards-based **MCP registry endpoint** — `https://<api-center-name>.data.<region>.azure-apicenter.ms/workspaces/default/v0.1/servers` — that tools like VS Code/GitHub Copilot can point at directly for discovery; metadata can be extended via custom properties surfaced in the `_meta` section of MCP responses.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server
- FINDING: **Automatic synchronization** keeps the registry current from two upstream sources: an Azure API Management instance (auto-sync of MCP servers/APIs managed there) and a Git repository of MCP/AI assets.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server
- FINDING: Access to registered MCP servers is governed using API Center's existing "Authorize access to APIs" capability (role-based access to view/consume catalogue entries). MCP servers registered in API Center can be integrated with **Microsoft Foundry's tool catalog** and **private tool catalogs for Foundry agents**, connecting the registry directly to agent tool governance.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server

### 6. Foundry Agent Service: tool/MCP authentication, approvals, guardrails

- FINDING: **Foundry Agent Service reached GA on March 16, 2026** (production SDKs for Python/JS/Java/.NET, full VNet isolation with no public egress for model or tool calls including MCP servers). Voice Live integration and related capabilities have separately moved GA through July–August 2026.
  SOURCE: https://devblogs.microsoft.com/foundry/foundry-agent-service-ga/
- FINDING: Five supported MCP authentication methods, selected per goal: **key-based** (shared API key/PAT, no user context), **Microsoft Entra – agent identity** (scoped per agent, shared credential), **Microsoft Entra – project managed identity** (shared across all agents in a project), **OAuth identity passthrough** (per-user identity persists, consent-based), and **unauthenticated access** (only for MCP servers that require no auth). Guidance: "start with Microsoft Entra authentication if the MCP server supports it" — it avoids secret management and gives automatic rotation; for private MCP servers on the same VNet as the agent, Entra auth is called "a natural fit."
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication
- FINDING: **Approval requirements for MCP tools**: the `mcp` tool definition's `require_approval` field controls whether a human must approve each call — supported values: `always` (default), `never`, or per-tool allow/deny lists (`{"never":[...]}` / `{"always":[...]}`). A pending approval surfaces as an `mcp_approval_request` response item that the calling application must resolve before the agent continues.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication
- FINDING: OAuth identity passthrough requires the calling user to hold at least the **Foundry Agent Consumer** role on the project (preferred, least-privilege) — the broader **Foundry User** role also works but is meant for agent builders, not consumers. Cross-tenant token exchange is **not supported** — the user's tenant must match the Foundry project's tenant. (Note: Foundry RBAC roles were recently renamed — Foundry User/Owner/Account Owner/Project Manager were previously Azure AI User/Owner/Account Owner/Project Manager; IDs and permissions unchanged.)
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication
- FINDING: **Agent 365 MCP servers** (Outlook Mail, Calendar, Teams, M365 profile, SharePoint/OneDrive, SharePoint Lists, Word, M365 Copilot search, M365 Admin Center, Dataverse) are gated: usable via custom OAuth with a bring-your-own Entra app registration, scoped permissions under the `Agent 365 Tools` API (app ID `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1`), and are "only available to Frontier tenants" (Microsoft's early-access adoption program) as of this doc's date.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication
- FINDING: The **AI Red Teaming Agent** in Microsoft Foundry combines Microsoft's open-source PyRIT (Python Risk Identification Tool) with Foundry Risk and Safety Evaluations to run automated adversarial probing (content-safety and security risk categories: violence, hate/unfairness, sexual, self-harm) against models, tools, and full agentic systems, producing scorecards with metrics like Attack Success Rate; it can run locally via the Azure AI Evaluation SDK or in the cloud via the Foundry SDK.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent ; https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent ; https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-ai-red-teaming-cloud

### 7. Governance: Purview, Defender for Cloud, Agent 365

- FINDING: **Microsoft Purview DSPM for AI** (current, non-classic version) provides an **AI observability** page in the Purview portal — a dashboard of active agents and their risk (based on Insider Risk Management signals), recommendations for remediation, and per-agent detail (Entra-enabled status, owner, agent user ID, activities). The **classic** DSPM for AI does **not** support Agent 365; must use the current DSPM experience.
  SOURCE: https://learn.microsoft.com/en-us/purview/ai-agent-365
- FINDING: Purview capabilities supported for AI/Agent 365 interactions: Auditing, Data classification, Sensitivity labels, Data Loss Prevention, Insider Risk Management (with a dedicated "Risky AI usage" policy template covering prompt injection and protected-material access), Communication Compliance, eDiscovery, Data Lifecycle Management, Compliance Manager (including "Assessments for AI regulations"). Notably, **encryption without sensitivity labels is not supported** for AI interactions.
  SOURCE: https://learn.microsoft.com/en-us/purview/ai-agent-365
- FINDING: Sensitivity-label enforcement for agents: an encrypted file's label must explicitly grant the agent instance both **VIEW and EXTRACT** usage rights for the agent to read it — broad grants like "Add any authenticated users" are insufficient; newly created content from Agent 365 does **not** inherit sensitivity labels from source items (so new agent output isn't automatically protected).
  SOURCE: https://learn.microsoft.com/en-us/purview/ai-agent-365
- FINDING: **Microsoft Defender for Cloud AI threat protection** is **Generally Available (GA)**. It provides real-time security alerts for generative-AI/agentic threats (data leakage, data poisoning, jailbreak, credential theft), works with Azure AI Content Safety Prompt Shields and Microsoft threat intelligence, and integrates with Defender XDR for alert correlation. Supported AI services: Azure OpenAI and Azure AI Model Inference service (text tokens only — image/audio not scanned currently). Billing includes a 30-day free trial capped at 75 billion tokens scanned; requires Owner role (or equivalent data actions) at subscription scope to enable. Not available in Azure Government or Azure operated by 21Vianet.
  SOURCE: https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection
- FINDING: Defender for Cloud added **preview support for threat protection of Foundry Agent Service agents** starting February 2, 2026 (OWASP LLM/agentic-AI risk coverage), and in July 2026 **unified Defender posture + runtime protection for cloud agents under Microsoft Agent 365**, consolidating coverage across Foundry, Copilot Studio, and third-party agents. Effective July 1, 2026, AI agent discovery and security posture for Foundry agents and third-party cloud agents **require a Microsoft Agent 365 license**. Threat protection for Foundry Agent Service itself is currently free (doesn't consume tokens), but Microsoft notes pricing/terms may change.
  SOURCE: https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/extending-defender%E2%80%99s-ai-threat-protection-to-microsoft-foundry-agents/4491927
- FINDING: **Microsoft Agent 365** provides the **Agent Registry** — a unified inventory of Microsoft and non-Microsoft agents (including agents without an Entra agent identity) — in the Microsoft 365 admin center, with cross-platform sync from AWS Bedrock and Google Cloud, an "Agent Map" visualization, hero adoption/impact metrics, and Graph API programmatic access for bulk lifecycle governance. Requires **AI Reader** or **AI Administrator** role to view the inventory; enforcing security/governance controls requires Entra Agent ID licensing.
  SOURCE: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry ; https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-actions
- FINDING: Agent 365's Entra integration page (part of the Agent 365 admin docs) frames Entra Agent ID as *the* identity platform underneath Agent 365, extending Conditional Access, ID Protection, and lifecycle management to agents once Agent 365 is licensed.
  SOURCE: https://learn.microsoft.com/en-us/microsoft-agent-365/admin/capabilities-entra

### 8. Content safety controls for agents

- FINDING: **Prompt Shields** (part of Azure AI Content Safety) detect both direct user jailbreak attempts and **indirect/document-based (cross-domain) prompt injection**; enabled in APIM via `shield-prompt="true"` on the `llm-content-safety` policy, and consumed directly by Defender for Cloud's AI threat protection for jailbreak alerts.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-management/llm-content-safety-policy ; https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection
- FINDING: **Spotlighting** (preview) strengthens Prompt Shields against **indirect prompt injection** by tagging input documents with special formatting to distinguish trusted instructions from untrusted external content — directly relevant to MCP tool outputs and RAG content fed to an agent.
  SOURCE: search-derived from Microsoft Community Hub blog "Enterprise-grade controls for AI apps and agents built with Azure AI Foundry and Copilot Studio" — reverify exact GA/preview wording on learn.microsoft.com/azure/ai-services/content-safety before quoting (see Caveats).
- FINDING: **Task adherence** is a Content Safety control that evaluates (and can enforce) whether an agent stays within its intended scope — it can block tool use, pause execution, or trigger human review if the agent drifts off-task; paired with real-time evaluation.
  SOURCE: search-derived, same source as above — verify against https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new before final publication.
- FINDING: **Groundedness detection** (Azure AI Content Safety) flags LLM responses that are not supported by the provided source material — used to catch fabricated/ungrounded output in RAG/enterprise-knowledge scenarios.
  SOURCE: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new (confirm exact API name/status directly — see Caveats)
- FINDING: The Well-Architected Framework's Responsible AI guidance operationalizes content safety end-to-end: PII detection/redaction on ingestion (Azure AI Language PII detection), real-time content-safety API calls on both requests and responses, centralizing safety checks at a gateway when multiple model invocations serve one client request (an explicit architectural argument for putting content safety at APIM rather than per-call in application code), and multimodal inspection (text/image) for hidden/adversarial content.
  SOURCE: https://learn.microsoft.com/en-us/azure/well-architected/ai/responsible-ai

### 9. Microsoft's published principles for securing agents/MCP

- FINDING: **Cloud Adoption Framework — AI agent governance and security baseline** (the single most load-bearing CAF page for this topic) states the core recommendation: "Establish a centralized and enforceable governance and security baseline for all AI agents that aligns with existing identity, data governance, and security practices." It structures governance into four domains: **control plane** (ownership, identity, lifecycle, observability), **data governance & compliance**, **security**, and **development standards** (approved frameworks/protocols only).
  SOURCE: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- FINDING: CAF's ten numbered "Agent security" best practices (verbatim intent): mandate agent-specific security training; require AI threat protection (Defender for Cloud); enforce infrastructure security baselines equal to customer-facing systems; mandate adversarial/red-team testing before production and after major updates; filter all inputs/outputs as potentially hostile (multimodal); standardize authentication on **managed identities** to eliminate secrets; enforce least privilege (agent tools inherit the calling user's permissions or use tightly scoped service accounts, with DLP restricting output); integrate AI alerts into the SOC (Azure Monitor → Log Analytics → Microsoft Sentinel); govern external integrations by restricting agents to **trusted MCP servers only** and validating all external agent (A2A) communications; and establish an incident-response/disaster-recovery plan specific to disabling a malfunctioning agent.
  SOURCE: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- FINDING: CAF's control-plane guidance explicitly recommends: maintain a **single agent registry** (Agent 365's Agent Registry if adopted; otherwise Entra Agent ID as the authoritative identity/ownership source); require **one distinct agent identity per agent** bound to organizational identity policy; enforce policy consistently across first-party, custom, and third-party agents (not team-level rules); and continuously observe agent activity/tools for behavioral drift.
  SOURCE: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- FINDING: The Well-Architected Framework's "Implement agentic AI safeguards" section defines three foundational aspects for agentic systems — robust data ingress/egress control, data validation/integrity assurance, and **independent** guardrails (oversight mechanisms that run separately from the agent itself, with human-override capability at any point) — and scales required oversight by agent capability: **retrieval agents (read-only)** need data-access controls + audit logging; **task-based agents (read/write)** need comprehensive authorization + transaction monitoring; **fully autonomous multi-turn agents** need all three safeguard categories at the highest oversight level. It also recommends "circuit breaker"/escape-hatch patterns: coordinator agents that escalate anomalies, human-in-the-loop checkpoints before high-risk actions, and interception points at routing, resource-allocation, and external-system-integration junctures.
  SOURCE: https://learn.microsoft.com/en-us/azure/well-architected/ai/responsible-ai
- FINDING: Microsoft's Windows-focused MCP security architecture (Windows 11, previewed at Build 2025, still the canonical statement of Microsoft's MCP security principles going into 2026) establishes a baseline: every MCP server needs security requirements met, a unique identity, and code signing for provenance/revocation; the core principle is **"the user is in control for all security sensitive operations done on their behalf."** By default, MCP servers reached through the Windows on-device agent registry run contained in a separate agent session with access limited to approved resources, mitigating cross-prompt injection.
  SOURCE: https://blogs.windows.com/windowsexperience/2025/05/19/securing-the-model-context-protocol-building-a-safer-agentic-future-on-windows/ ; https://learn.microsoft.com/en-us/windows/ai/mcp/servers/mcp-containment
- FINDING: Microsoft Security Blog guidance on MCP implementation risk recommends: centralized logging/monitoring of AI applications routed to a SIEM for anomaly detection, and a zero-trust architecture that isolates MCP components via network and identity controls (consistent with APIM/API Center + Entra + Defender for Cloud pattern documented above).
  SOURCE: https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667

## Code / Config

OBO token exchange — step 3 (blueprint exchanges managed-identity token for T1):
```
POST /oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

client_id=AgentBlueprint
&scope=api://AzureADTokenExchange/.default
&fmi_path=AgentIdentity
&client_assertion=TUAMI
&grant_type=client_credentials
```
SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow

OBO token exchange — step 4 (agent identity performs the actual OBO exchange):
```
POST /oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

client_id=AgentIdentity
&scope=https://resource.example.com/scope1
&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer
&client_assertion={T1}
&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer
&assertion={Tc(aud=AgentIdentity Blueprint, oid=User)}
&requested_token_use=on_behalf_of
```
SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow

APIM — validate an Entra token on an MCP server (inbound):
```xml
<validate-azure-ad-token tenant-id="your-entra-tenant-id" header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="Unauthorized. Access token is missing or invalid.">
    <client-application-ids>
        <application-id>your-client-application-id</application-id>
    </client-application-ids>
</validate-azure-ad-token>
```
SOURCE: https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers

APIM — inject a downstream OAuth token from credential manager (outbound to MCP tool's backend):
```xml
<!-- Add to inbound policy. -->
<get-authorization-context
    provider-id="your-credential-provider-id"
    authorization-id="auth-01"
    context-variable-name="auth-context"
    identity-type="managed"
    ignore-error="false" />
<!-- Attach the token to the backend call -->
<set-header name="Authorization" exists-action="override">
    <value>@("Bearer " + ((Authorization)context.Variables.GetValueOrDefault("auth-context"))?.AccessToken)</value>
</set-header>
```
SOURCE: https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers

APIM — `llm-content-safety` policy (blocks Hate/Violence severity ≥4, shields prompts):
```xml
<policies>
    <inbound>
        <llm-content-safety backend-id="content-safety-backend" shield-prompt="true">
            <categories output-type="EightSeverityLevels">
                <category name="Hate" threshold="4" />
                <category name="Violence" threshold="4" />
            </categories>
        </llm-content-safety>
    </inbound>
</policies>
```
SOURCE: https://learn.microsoft.com/en-us/azure/api-management/llm-content-safety-policy

Foundry Agent Service — create an MCP connection with agent-identity auth:
```bash
azd ai connection create my-mcp-connection \
  --kind remote-tool \
  --target https://<mcp-server-endpoint> \
  --auth-type agentic-identity \
  --audience "<entra-audience>"
```
SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication

Foundry Agent Service — create an MCP connection with project managed-identity auth:
```bash
azd ai connection create my-mcp-connection \
  --kind remote-tool \
  --target https://<mcp-server-endpoint> \
  --auth-type project-managed-identity \
  --audience "<entra-audience>"
```
SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication

Foundry Agent Service — OAuth identity passthrough, Python, handling the consent link:
```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_endpoint = "https://<resource>.services.ai.azure.com/api/projects/<project>"
agent_name = "<agent-name>"
user_input = "Use the MCP tool to complete my request."

project = AIProjectClient(
   endpoint=project_endpoint,
   credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

response = openai.responses.create(
   input=user_input,
   tool_choice="required",
   extra_body={
      "agent_reference": {"name": agent_name, "type": "agent_reference"}
   },
)

for item in response.output:
   if item.type == "oauth_consent_request":
      print(f"Open this URL to authorize access: {item.consent_link}")
```
SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication

API Center — MCP registry discovery endpoint format:
```
https://<your-api-center-name>.data.<region>.azure-apicenter.ms/workspaces/default/v0.1/servers
```
SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server

## Caveats / Gaps

- **Everything in this document is time-sensitive and preview surfaces are moving fast.** Verify current GA/preview status directly on learn.microsoft.com immediately before publishing the enterprise best-practices doc — several features (ID Protection "Risky Agents (Preview)", Spotlighting, task adherence, Agent 365-gated MCP servers being "Frontier tenants" only, enforcement of Agent 365 licensing for Conditional Access "coming soon") are explicitly called out as preview or pending enforcement in the docs themselves as of their last-updated dates (ranging April–September 2026 in this research).
- Two source findings under section 8 (Spotlighting, task adherence) were derived from WebSearch summaries of a Microsoft Community Hub blog post rather than a directly fetched learn.microsoft.com page; the underlying Content Safety "what's new" page (https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new) should be fetched directly to get exact wording/status before quoting in the final best-practices document.
- The **PRM (Protected Resource Metadata) and DCR (Dynamic Client Registration) workaround** for MCP servers is documented only via community/lab samples linked from the official APIM "secure-mcp-servers" page (a GitHub sample and an AI-Gateway lab), not as first-party prescriptive Microsoft Learn guidance. Treat this as an official-adjacent pattern, not a fully first-party spec.
- Exact GA date/status for "expose REST API as MCP server" in Azure API Management was reported inconsistently across sources (a mid-2026 Community blog called it "preview"; Build 2026 coverage implies broader AI Gateway GA). Confirm the current `APPLIES TO` tier table and any preview banners on https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server directly before publishing.
- Agent 365-branded MCP servers (Outlook, Teams, SharePoint, etc.) are explicitly restricted to "Frontier tenants" (an early-access program) — not broadly GA — as of the Foundry MCP authentication doc's September 2026 update.
- Copilot Studio-specific agent governance (item 7's "if relevant") was only lightly touched (linked from CAF and from the Entra Agent ID "in practice" example) — a dedicated pass over https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance and https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-use-entra-agent-identities is recommended if Copilot Studio needs deeper coverage in the final document.
- The MCP specification's own workload-identity proposals (DPoP / SEP-1932, Workload Identity Federation / SEP-1933) are noted by third-party sources as still-open pull requests, not Microsoft documentation — included only as context that "no MCP-native workload identity is standardized yet," not as an Azure product claim.
- Microsoft Graph API references (e.g., `agentIdentityBlueprint` resource schema) are on the **beta** Graph endpoint in several places (sign-in/audit log queries) — expect schema and endpoint-path changes before v1.0 promotion.

## Sources

- https://learn.microsoft.com/en-us/entra/agent-id/ — Microsoft Entra Agent ID documentation home
- https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities — What are agent identities?
- https://learn.microsoft.com/en-us/entra/agent-id/agent-blueprint — Agent identity blueprints in Microsoft Entra Agent ID
- https://learn.microsoft.com/en-us/entra/agent-id/manage-agent-identities-admin — Manage agent identities in your organization
- https://learn.microsoft.com/en-us/entra/agent-id/manage-owners-sponsors-agents — Add and manage owners and sponsors for agent identities and blueprints
- https://learn.microsoft.com/en-us/entra/agent-id/agent-owners-sponsors-managers — Administrative relationships in Microsoft Entra Agent ID
- https://learn.microsoft.com/en-us/entra/agent-id/sign-in-audit-logs-agents — Microsoft Entra Agent ID logs
- https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id — Best practices for Microsoft Entra Agent ID
- https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow — Agent OAuth flows: On-behalf-of flow
- https://learn.microsoft.com/en-us/entra/agent-id/whats-new-agent-id — What's new in Microsoft Entra Agent ID
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/agent-id — Conditional Access for Agents in Microsoft Entra
- https://learn.microsoft.com/en-us/entra/id-protection/concept-risky-agents — ID Protection for Agents
- https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview — Governing Agent Identities (Microsoft Entra ID Governance)
- https://learn.microsoft.com/en-us/microsoft-agent-365/admin/capabilities-entra — Protect agent identities with Microsoft Entra
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-use-entra-agent-identities — Manage Entra Agent IDs (Copilot Studio)
- https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers — Secure access to MCP servers in Azure API Management
- https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server — Expose REST API as MCP server (Azure API Management)
- https://learn.microsoft.com/en-us/azure/api-management/expose-existing-mcp-server — Connect and govern existing MCP server (Azure API Management)
- https://learn.microsoft.com/en-us/azure/api-management/validate-jwt-policy — Azure API Management policy reference: validate-jwt
- https://learn.microsoft.com/en-us/azure/api-management/validate-azure-ad-token-policy — Azure API Management policy reference: validate-azure-ad-token
- https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy — Azure API Management policy reference: llm-token-limit
- https://learn.microsoft.com/en-us/azure/api-management/llm-content-safety-policy — Azure API Management policy reference: llm-content-safety
- https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities — AI gateway capabilities in Azure API Management
- https://learn.microsoft.com/en-us/azure/api-management/ai-gateway-govern-secure-assets — Govern, secure, and operate AI Gateway tier (preview)
- https://learn.microsoft.com/en-us/azure/api-management/credentials-overview — Credential manager overview
- https://techcommunity.microsoft.com/blog/integrationsonazureblog/whats-new-in-azure-api-management-at-microsoft-build-2026/4524683 — What's new in Azure API Management at Build 2026
- https://techcommunity.microsoft.com/blog/integrationsonazureblog/expose-rest-apis-as-mcp-servers-with-azure-api-management-and-api-center-now-in-/4415013 — Expose REST APIs as MCP servers (preview announcement)
- https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server — Inventory and discover MCP servers in your API Center
- https://learn.microsoft.com/en-us/azure/api-center/discover-catalog-mcp-server — Discover APIs with Azure API Center MCP server
- https://techcommunity.microsoft.com/blog/integrationsonazureblog/build-secure-launch-your-private-mcp-registry-with-azure-api-center-/4438016 — Build/secure/launch a private MCP registry with API Center
- https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication — Set up MCP server authentication (Microsoft Foundry Agent Service)
- https://learn.microsoft.com/en-us/azure/foundry/agents/overview — What is Microsoft Foundry Agent Service?
- https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-identity — Agent identity concepts in Microsoft Foundry
- https://devblogs.microsoft.com/foundry/foundry-agent-service-ga/ — Foundry Agent Service is GA
- https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent — AI Red Teaming Agent (Microsoft Foundry)
- https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent — Run AI Red Teaming Agent locally
- https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-ai-red-teaming-cloud — Run AI Red Teaming Agent in the cloud
- https://learn.microsoft.com/en-us/purview/ai-agent-365 — Use Microsoft Purview to manage data security & compliance for Microsoft Agent 365
- https://learn.microsoft.com/en-us/purview/data-security-posture-management-learn-about — Learn about Microsoft Purview DSPM
- https://learn.microsoft.com/en-us/purview/dspm-for-ai-considerations — Considerations for deploying DSPM for AI
- https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection — AI threat protection in Microsoft Defender for Cloud
- https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-security-posture — AI security posture management overview
- https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-onboarding — Enable threat protection for AI services
- https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/extending-defender%E2%80%99s-ai-threat-protection-to-microsoft-foundry-agents/4491927 — Extending Defender's AI threat protection to Foundry agents
- https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry — Agent Registry in Microsoft 365 admin center
- https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-actions — Governance and lifecycle actions for agents (M365 admin center)
- https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-365-overview — Agent overview in Microsoft 365 admin center
- https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations/ — Microsoft Agent 365 GA announcement
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new — What's new in Azure AI Content Safety
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/ — AI agent adoption guidance for organizations (Cloud Adoption Framework)
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization — Govern and secure AI agents across the organization (CAF)
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/integrate-manage-operate — Manage AI agents across your organization (CAF)
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/build-secure-process — Process to build agents with Foundry and Copilot Studio (CAF)
- https://learn.microsoft.com/en-us/azure/well-architected/ai/responsible-ai — Responsible AI in Azure workloads (Well-Architected Framework)
- https://learn.microsoft.com/en-us/azure/well-architected/ai/architecture-pattern — Architecture pattern for AI workloads on Azure
- https://blogs.windows.com/windowsexperience/2025/05/19/securing-the-model-context-protocol-building-a-safer-agentic-future-on-windows/ — Securing the Model Context Protocol on Windows
- https://learn.microsoft.com/en-us/windows/ai/mcp/servers/mcp-containment — Securely containing MCP servers on Windows
- https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667 — Understanding and mitigating security risks in MCP implementations
- https://techcommunity.microsoft.com/blog/appsonazureblog/mcp-enterprise-authorization-is-here-%E2%80%94-what-entra-and-app-service-can-do-today/4537433 — MCP enterprise authorization: Entra and App Service today

## Where to do this on Azure

| Control | Azure service / feature | Status | Source URL |
| --- | --- | --- | --- |
| Give each agent its own identity | Microsoft Entra Agent ID (agent identity + agent identity blueprint) | GA (framework); Agent 365 features extending it vary | https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities |
| Autonomous (app-only) agent auth | Entra Agent ID client-credentials flow, managed-identity-backed blueprint credential | GA | https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow |
| Delegated (user-context) agent auth | Entra Agent ID on-behalf-of flow with agent identity blueprint + FMI path | GA | https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow |
| Conditional Access for agents | Entra Conditional Access (agent identity / blueprint / agent's user account targeting) | Requires Entra P1/P2 + Agent 365 license; licensing enforcement "coming soon" | https://learn.microsoft.com/en-us/entra/identity/conditional-access/agent-id |
| Risk-based blocking of compromised agents | Microsoft Entra ID Protection — Risky Agents report | Preview | https://learn.microsoft.com/en-us/entra/id-protection/concept-risky-agents |
| Agent sign-in / audit visibility | Entra sign-in logs (`agentSignIn`) and audit logs (`agentType`, `blueprintId`) | GA | https://learn.microsoft.com/en-us/entra/agent-id/sign-in-audit-logs-agents |
| No secrets in agent/MCP server credentials | Managed identity + workload identity federation (federated identity credentials) | GA | https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow |
| Certificate/secret storage | Azure Key Vault | GA | https://learn.microsoft.com/en-us/entra/agent-id/best-practices-agent-id |
| Expose an existing REST API as an MCP server | Azure API Management — Export REST API as MCP server | Verify current status (reported preview mid-2026, AI Gateway broadly GA) | https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server |
| Front/govern an existing MCP server | Azure API Management — Connect and govern existing MCP server | GA (AI Gateway tier) | https://learn.microsoft.com/en-us/azure/api-management/expose-existing-mcp-server |
| Validate MCP client tokens (Entra) | APIM `validate-azure-ad-token` policy | GA | https://learn.microsoft.com/en-us/azure/api-management/validate-azure-ad-token-policy |
| Validate MCP client tokens (generic JWT) | APIM `validate-jwt` policy | GA | https://learn.microsoft.com/en-us/azure/api-management/validate-jwt-policy |
| Inject downstream OAuth tokens for MCP tool backends | APIM Credential manager (`get-authorization-context`) | GA | https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers |
| Rate-limit / cap LLM token consumption | APIM `llm-token-limit` policy | GA | https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy |
| Content-safety checks on prompts/completions/MCP/A2A | APIM `llm-content-safety` policy (backed by Azure AI Content Safety) | GA | https://learn.microsoft.com/en-us/azure/api-management/llm-content-safety-policy |
| Private MCP/tool registry | Azure API Center (inventory, MCP registry endpoint, portal test console) | GA (data-plane MCP server GA'd at Build 2026) | https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server |
| Connect registry to agent tool governance | API Center integration with Microsoft Foundry tool catalog / private tool catalog | GA/Preview mix — verify per sub-feature | https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server |
| Agent MCP tool authentication in Foundry | Foundry Agent Service — key-based / Entra agent identity / Entra project managed identity / OAuth identity passthrough | GA (Foundry Agent Service GA March 2026) | https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication |
| Require human approval on MCP tool calls | Foundry `mcp` tool `require_approval` parameter | GA | https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication |
| Adversarial/red-team testing of agents | Microsoft Foundry AI Red Teaming Agent (PyRIT + Risk and Safety Evaluations) | GA/Preview mix — verify current state | https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent |
| Data security posture for AI agents | Microsoft Purview DSPM for AI (current, non-classic) — AI observability | GA (current version); classic version excluded from Agent 365 | https://learn.microsoft.com/en-us/purview/ai-agent-365 |
| Runtime threat detection for AI/agent workloads | Microsoft Defender for Cloud — AI threat protection | GA (Foundry Agent Service coverage added Feb 2026 preview → unified under Agent 365 July 2026) | https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection |
| Org-wide agent inventory / control plane | Microsoft Agent 365 — Agent Registry | GA (May 2026) | https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations/ |
| Prompt injection defense (direct + indirect) | Azure AI Content Safety — Prompt Shields (+ Spotlighting) | Prompt Shields GA; Spotlighting preview (verify) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new |
| Agent scope/task-drift control | Azure AI Content Safety — task adherence | Verify current status | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new |
| Ungrounded/fabricated response detection | Azure AI Content Safety — groundedness detection | Verify current status | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new |
| Organization-wide agent governance blueprint | Cloud Adoption Framework — AI agents (govern and secure) | Living guidance (non-versioned) | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization |
| Architectural responsible-AI/agent safeguard patterns | Well-Architected Framework — AI workloads, Responsible AI | Living guidance (non-versioned) | https://learn.microsoft.com/en-us/azure/well-architected/ai/responsible-ai |
