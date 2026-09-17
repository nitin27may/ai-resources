# Official Docs Research: Tool and Agent Discovery at Scale
SOURCE_TYPE: official-docs
CONFIDENCE: HIGH
GENERATED: 2026-09-17T00:00:00+05:30

## Summary

As tool/agent catalogues grow past roughly 10-20 entries, every major vendor now documents the same failure mode: full tool-definition JSON schemas are re-sent on every turn (MCP and Responses APIs are stateless), which inflates token cost and measurably degrades selection accuracy — Anthropic, Microsoft Foundry, and independent benchmarks (RAG-MCP, LiveMCPBench, MCP-Bench) all report this with concrete numbers. The documented fix pattern, converging across Anthropic, OpenAI and Microsoft Foundry under different names ("Tool Search Tool"/`defer_loading`, hosted-MCP `tool_search`/`allowed_tools`, Foundry `toolbox_search`), is deferred/on-demand tool loading: give the model a lightweight search/discovery meta-tool instead of the full catalogue, and load full schemas only for what's selected. A second, complementary pattern — "code execution with MCP" — has agents write code against MCP servers exposed as filesystem/code APIs rather than making natural-language tool calls, keeping both definitions and intermediate results out of context. For agent-level (not tool-level) discovery, the A2A protocol (now v1.0.0) standardizes machine-readable Agent Cards at a well-known URI, and Microsoft (Entra Agent ID / Agent 365 / M365 admin center Agent Registry) and Azure API Center each ship enterprise registries for inventorying and governing agents and MCP servers, while the official MCP Registry (still preview) centralizes server metadata for downstream aggregators.

## Key Findings

### 1. Evidence that accuracy/cost degrade as tool count grows

- FINDING: Anthropic's own internal MCP evaluations show accuracy dropping as full tool catalogues grow, and recovering with Tool Search: Opus 4 went from 49% → 74% accuracy, and Opus 4.5 from 79.5% → 88.1%, when Tool Search (on-demand discovery) was enabled instead of loading full definitions. Token consumption for tool definitions on real catalogs dropped ~85% (from ~77K to ~8.7K tokens), preserving ~95% of the context window for other tasks.
  SOURCE: https://www.anthropic.com/engineering/advanced-tool-use
- FINDING: Anthropic's separate "code execution with MCP" case study: a Google Drive-to-Salesforce workflow dropped from 150,000 tokens to 2,000 tokens (98.7% reduction) by presenting MCP servers as code APIs instead of loading all tool definitions and passing intermediate results through context.
  SOURCE: https://www.anthropic.com/engineering/code-execution-with-mcp
- FINDING: Microsoft Foundry documents the same problem directly: "When a toolbox contains many tools, passing all tool definitions to the model on every turn creates three compounding problems: token costs grow with every tool added to the context, the context window fills with definitions the current task doesn't need, and the model picks the wrong tools from an overcrowded list." In an internal evaluation with 600+ tools, enabling Tool Search cut input tokens per call from 313K+ to 18K (94% reduction) and raised tool-selection accuracy from 48.2% to 52.4%.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search
- FINDING (research paper, non-vendor but directly on-point): RAG-MCP (arXiv:2505.03275) shows that as the number of available MCP tools grows, a baseline LLM's tool-selection success rate drops markedly; retrieval-augmented tool selection cuts prompt tokens by over 50% and more than triples baseline tool-selection accuracy (43.13% vs 13.62%) on their benchmark, restoring accuracy to near small-toolset baseline even at large catalogue scale.
  SOURCE: https://arxiv.org/abs/2505.03275
- FINDING (research paper): LiveMCPBench (arXiv:2508.01780) — a benchmark of 95 real-world tasks across 70 MCP servers / 527 tools — found retrieval errors account for nearly half of all task failures, and that "active tool composition" (which tools are actually surfaced) strongly correlates with task success. Claude-Sonnet-4 reached 78.95% task success; most other evaluated models scored only 30-50%.
  SOURCE: https://arxiv.org/abs/2508.01780
- FINDING (research paper): MCP-Bench (arXiv:2508.20453) — 28 live MCP servers, 250 tools — found low-level capabilities like schema compliance and tool-name validity have "largely converged" across models (>95% accuracy even for mid-scale models), but multi-step planning/coordination is the actual bottleneck at scale, with many models scoring below 0.30 on planning effectiveness.
  SOURCE: https://arxiv.org/abs/2508.20453
- FINDING: OpenAI's function-calling guidance gives an explicit, if soft, upper bound: "Aim for fewer than 20 functions available at the start of a turn at any one time, though this is just a soft suggestion," and recommends developers empirically evaluate performance at different tool counts.
  SOURCE: https://developers.openai.com/api/docs/guides/function-calling
- FINDING: For o3/o4-mini specifically, OpenAI states "any setup with fewer than ~100 tools and fewer than ~20 arguments per tool is considered in-distribution and should perform within expected reliability bounds" (as of the guide's May 2025 publication) — but adds that even in-distribution setups can suffer from ambiguity as tool count grows.
  SOURCE: https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide

### 2. Deferred / on-demand tool loading

- FINDING: Anthropic ships three beta "advanced tool use" features (header `betas=["advanced-tool-use-2025-11-20"]`, published 2025-11-24): (1) **Tool Search Tool** — mark tools `"defer_loading": true`; Claude calls a `tool_search_tool_regex_20251119` (or similarly named BM25/regex search tool) to discover schemas on demand instead of receiving them all upfront; recommended when tool definitions exceed ~10K tokens, there are 10+ tools, or multiple MCP servers are connected. (2) **Programmatic Tool Calling** (`code_execution_20250825`) — Claude writes code in a code-execution environment to orchestrate tool calls (`allowed_callers: ["code_execution_20250825"]` opts a tool in), keeping intermediate results out of the visible context; measured 37% average token reduction (43,588 → 27,297 tokens) on complex tasks and eliminated 19+ inference passes on complex workflows. (3) **Tool Use Examples** — an `input_examples` field alongside `input_schema` to demonstrate concrete usage patterns; internal testing showed accuracy improving from 72% to 90% on complex parameter handling.
  SOURCE: https://www.anthropic.com/engineering/advanced-tool-use
- FINDING: Anthropic's "code execution with MCP" pattern presents MCP servers as filesystem-based code APIs (e.g., `./servers/google-drive/getDocument.ts`) that the agent explores and reads on demand, then writes code against, rather than receiving all tool JSON schemas and making natural-language tool calls turn by turn. Cloudflare has published a related independent approach under the name "Code Mode."
  SOURCE: https://www.anthropic.com/engineering/code-execution-with-mcp
- FINDING: OpenAI's hosted MCP tool in the Responses API supports `allowed_tools` to restrict which tools from a connected MCP server are imported/exposed to the model, and a `defer_loading: true` flag on an MCP server entry that enables "tool search": the model uses the server's label/description to decide when to search it, and individual function definitions load only when needed.
  SOURCE: https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- FINDING: OpenAI's hosted MCP tool defaults to requiring per-call approval (`require_approval`); options are `"always"`, `"never"`, or a filtered object such as `{"require_approval": {"never": {"tool_names": ["ask_question", "read_wiki_structure"]}}}` naming specific tools exempt from approval.
  SOURCE: https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- FINDING: OpenAI documents tool-search as gated to newer models — "Only gpt-5.4 and later models support tool_search" — and recommends, as an alternative pattern, splitting large tool surfaces into role-specific sub-agents of 4-6 tools each when tool-search isn't available/used.
  SOURCE: https://developers.openai.com/api/docs/guides/tools-connectors-mcp (feature gating); general guidance corroborated by https://developers.openai.com/api/docs/guides/function-calling
- FINDING: Microsoft Foundry's **Tool Search** (toolbox feature, doc dated 2026-08-19, updated 2026-09-01) works by adding `{"type": "toolbox_search"}` to a toolbox's tool list. This hides all other toolbox tools from the initial `tools/list` response and injects two meta-tools: `tool_search` (natural-language query, BM25 ranking over tool name/description/params, `limit` param default 5 max 10) and `call_tool` (invoke any discovered tool by name). Supports `tool_configs` per tool: `pin: true` (always visible, skips search) and `additional_search_text` (extra ranking keywords, never shown to the model). Foundry also does automatic **auto-pinning**: it tracks per-user tool-call frequency and promotes frequently used tools into `tools/list` after a warmup period, without configuration. Recommended threshold: "toolbox has more than 10-15 tools" or when different tasks need different tool subsets. `tool_search`/`call_tool` do not count toward the "unnamed-tool-per-type" limit.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search
- FINDING: A companion Foundry doc extends the same deferred-loading concept to the Azure OpenAI Responses API ("request-scoped discovery of deferred tool definitions").
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/tool-search (referenced from tool-search.md; not independently fetched — verify directly before citing details)

### 3. Tool design guidance

- FINDING: Anthropic's "Writing Effective Tools for Agents — with Agents" (Anthropic engineering blog, published 2025-09-11) lays out a full evaluation-driven design methodology: (1) choose the right tools to build — "More tools don't always lead to better outcomes"; consolidate multi-step API sequences into a single workflow tool (e.g., one `schedule_event` tool instead of separate `list_users`/`list_events`/`create_event`) rather than wrapping every endpoint 1:1. (2) Namespace tools when agents access hundreds of tools across many servers, grouping by service or resource (`asana_search`, `jira_search`, or `asana_projects_search`, `asana_users_search`); the choice of prefix vs. suffix namespacing has "non-trivial effects on tool-use evaluations." (3) Return "high-signal" meaningful context — prefer semantic identifiers (`name`, `file_type`) over raw UUIDs/mime types, and expose a `ResponseFormat` enum (e.g., `"concise"` vs `"detailed"`) so the agent can control verbosity (concise responses shown using ~1/3 the tokens of detailed). (4) Optimize for token efficiency via pagination, range selection, filtering, and sensible truncation defaults (Claude Code tool responses default to a 25,000-token limit), with truncation messages steering the agent toward narrower follow-up queries. (5) Give actionable, specific error messages instead of opaque codes/tracebacks, showing the agent the corrected input format. (6) Prompt-engineer tool descriptions as if onboarding a new employee, with unambiguous parameter names (`user_id` not `user`); Anthropic reports human-written tools scored ~60-70% on internal Slack/Asana evaluations vs. 80-90% for Claude-optimized tool descriptions on the same held-out tasks.
  SOURCE: https://www.anthropic.com/engineering/writing-tools-for-agents
- FINDING: MCP tool-naming rules were formalized via SEP-986 ("Specify Format for Tool Names"), status **Final**, created 2025-07-16, authored by kentcdodds: names SHOULD be 1-64 characters, case-sensitive, allowed characters `A-Z a-z 0-9 _ - . /`, no spaces/commas, SHOULD be unique within namespace. Example valid names: `getUser`, `user-profile/update`, `DATA_EXPORT_v2`, `admin.tools.list`.
  SOURCE: https://modelcontextprotocol.io/seps/986-specify-format-for-tool-names
- FINDING: The current MCP specification (2026-07-28) has since tightened/updated the naming rule text (superseding SEP-986's literal wording): tool names SHOULD be 1-128 characters (not 64), case-sensitive, allowed characters `A-Z a-z 0-9 _ - .` (note: **forward slash `/` is no longer in the allowed set** in the live spec, differing from the original SEP-986 text), SHOULD be unique **within a server** (not globally); the spec explicitly warns that clients/proxies aggregating tools across multiple servers may hit name collisions (e.g., two `search` tools) and SHOULD disambiguate, e.g., by prefixing with a server identifier — and explicitly notes the server's `serverInfo.name` is NOT guaranteed unique and SHOULD NOT be relied on for disambiguation.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- FINDING: MCP tool objects support `title` (optional human-readable display name, distinct from the machine `name`), `description`, `inputSchema` (JSON Schema, defaults to 2020-12, MUST NOT be null; for no-arg tools the spec recommends `{"type": "object", "additionalProperties": false}`), and optional `outputSchema` (JSON Schema for `structuredContent`). If `outputSchema` is defined, servers MUST return conforming `structuredContent` and clients SHOULD validate it; for backward compatibility a tool returning structured content SHOULD also serialize it as a `TextContent` block. Structured content is unrelated to LLM "structured outputs" — it's server-produced result data.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- FINDING: MCP tool results distinguish **Protocol Errors** (malformed request/unknown tool — standard JSON-RPC errors, models are less likely to self-correct from these) from **Tool Execution Errors** (`isError: true` in the result, with actionable text such as "Invalid departure date: must be in the future. Current date is 08/08/2025.") — clients SHOULD feed execution errors back to the model to enable self-correction.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- FINDING (worked official example): GitHub's official MCP server implements **toolsets** — logical groupings of related tools (e.g., `context`, `repos`, `issues`, `pull_requests`, `actions`, `code_security`, `code_quality`, `discussions`, `gists`, `git`, `governance`, `notifications`, `orgs`, `projects`, `secret_protection`, `security_advisories`, `stargazers`, `users`, plus remote-only `copilot_spaces`, `github_support_docs_search`) — configurable via `--toolsets repos,issues,...` CLI flag or `GITHUB_TOOLSETS` env var (env var takes precedence), with special `all` and `default` keywords (`default` = `context, repos, issues, pull_requests, users`). Docs state directly: "enabling only the toolsets that you need can help the LLM with tool choice and reduce the context size." A `--read-only` flag takes priority over toolset selection, skipping write tools even if explicitly requested.
  SOURCE: https://github.com/github/github-mcp-server
- FINDING (gap): community/GitHub-issue references to a `GITHUB_DYNAMIC_TOOLSETS` env var / `--dynamic-toolsets` flag ("beta" runtime toolset discovery) turned up in search results but were **not found** in the current official README — treat this as either deprecated, renamed, or not yet merged; verify directly against the live repo before citing it as current.
  SOURCE: https://github.com/github/github-mcp-server (absence noted)

### 4. MCP server scoping and server-side filtering

- FINDING: The MCP 2026-07-28 spec explicitly sanctions per-caller filtering of `tools/list`: "This set MAY be empty and MAY change over time... but MUST NOT vary per-connection or as a side effect of other requests on the connection. The set MAY vary by the authorization presented on the request — for example, returning only the tools the caller's granted scopes permit — since credentials are per-request input, not connection state." This is the direct normative basis for "only list tools the caller may use."
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- FINDING: Servers SHOULD return tools in **deterministic order** across requests (same ordering when the underlying set hasn't changed) specifically to let clients cache the tool list reliably and improve LLM prompt-cache hit rates when tool definitions are included in model context.
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- FINDING: `tools/list` supports pagination via an opaque `cursor` parameter and `nextCursor` in the response (plus, in the 2026-07-28 spec, response-level `ttlMs`/`cacheScope` fields for caching semantics and a `resultType: "complete"` envelope).
  SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- FINDING: The 2026-07-28 spec introduces `server/discover` — a sessionless capability-discovery method (per SEP-2575) that responds before `initialize` and without an `Mcp-Session-Id`, letting a client learn a server's supported versions/capabilities/identity in one exchange without creating a session; the same spec release retires the old `initialize`/`initialized` handshake and `Mcp-Session-Id` header as mandatory, moving to per-request protocol version/client identity in `_meta`. A "Server Card Working Group" is separately working through `.well-known` metadata conventions so a server can be reasoned about without even connecting.
  SOURCE: https://blog.modelcontextprotocol.io/posts/2026-07-28/ ; https://modelcontextprotocol.io/specification/2026-07-28/server/discover (page exists per search results; verify content directly before quoting further specifics)
- FINDING: Enterprise "one server per bounded context vs. mega-server" — no single normative MCP-spec ruling was found; this is effectively a synthesis of (a) GitHub's own toolset-scoping design (single server, but curated sub-groups) and (b) the naming-collision warning in the spec, which implies smaller, well-scoped servers reduce cross-server disambiguation burden on clients. Treat "prefer bounded-context servers" as **vendor-pattern/derived guidance**, not an explicit MCP MUST/SHOULD.
  SOURCE: (derived from) https://modelcontextprotocol.io/specification/2026-07-28/server/tools and https://github.com/github/github-mcp-server — GAP, no single authoritative statement found.
- FINDING: Azure API Center functions as an enterprise MCP-server registry: "Azure API Center can maintain an inventory (or registry) of remote or local MCP servers and help stakeholders discover them through the API Center portal," positioned explicitly for private/internal review before servers become accessible to developers or agent runtimes (Copilot Studio, Foundry): "A private registry empowers your organization to thoroughly review and verify every MCP server before it becomes accessible."
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server
- FINDING: Azure API Center also exposes its own catalog as an MCP server itself ("the Azure API Center MCP server exposes your organization's API catalog as a native tool surface for AI agents"), and can register MCP servers hosted in Azure Functions directly.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/discover-catalog-mcp-server ; https://learn.microsoft.com/en-us/azure/azure-functions/register-mcp-server-api-center

### 5. Agent discovery (A2A, registries)

- FINDING: The Agent2Agent (A2A) protocol's current released version is **1.0.0** (per the official spec index; note A2A "joined the Agentic AI Foundation" as of August 2026, so governance has moved to a foundation-hosted project).
  SOURCE: https://a2a-protocol.org/latest/specification/
- FINDING: A2A's primary public discovery mechanism is the well-known URI pattern per RFC 8615: an Agent Card is published at `https://{agent-server-domain}/.well-known/agent-card.json`. The Agent Card is described as "a digital business card for an A2A Server" and contains identity (`name`, `description`, `provider`), service `url`, `capabilities` (`streaming`, `pushNotifications`, `extendedAgentCard` booleans), `securitySchemes`/`security` (authentication mechanisms such as Bearer, OAuth2, mutual TLS), `skills` (array of `{id, name, description, inputModes, outputModes, examples}` describing discrete agent capabilities/tasks), `interfaces` (supported protocol bindings/endpoints), `extensions` (supported extension URIs), and an optional `signature` field.
  SOURCE: https://a2a-protocol.org/latest/specification/ ; https://a2a-protocol.org/latest/topics/agent-discovery/
- FINDING: Agent Cards MAY be cryptographically signed using JSON Web Signatures (JWS) via an `AgentCardSignature` object; clients SHOULD verify signatures when present. Canonicalization rules exist to distinguish explicitly-set fields from omitted ones so a card can be reconstructed to match its signature.
  SOURCE: https://a2a-protocol.org/latest/topics/agent-discovery/ (verify the JWS/canonicalization mechanics directly against the spec before quoting field-level detail)
- FINDING: A2A supports "authenticated extended agent cards" — a more detailed card returned only to authenticated/authorized clients — plus "registry selective disclosure," where a registry can return different card contents depending on client identity/permissions. The spec explicitly states it does **not** prescribe a standard API for curated registries — registries are an ecosystem pattern, not a normative A2A component.
  SOURCE: https://a2a-protocol.org/latest/topics/agent-discovery/
- FINDING: The official **MCP Registry** (registry.modelcontextprotocol.io) is explicitly **in preview** ("Breaking changes or data resets may occur before general availability"), backed by Anthropic, GitHub, PulseMCP, Microsoft. It is a metadata-only registry (`server.json` format: unique reverse-DNS-style server name, package/remote-server location, execution instructions, description/capabilities) — it does **not** host code, does **not** support private/internal servers, and is explicitly "not intended to be directly consumed by host applications" — it's designed to feed downstream aggregators/marketplaces (which poll it, e.g., hourly) via a REST API and a published OpenAPI spec that other (including private, org-internal) registries can implement for a standardized interface.
  SOURCE: https://modelcontextprotocol.io/registry/about
- FINDING: Microsoft's enterprise agent-discovery/governance stack has two converging but distinct layers: **Microsoft Entra Agent ID** (identity/security framework extending Entra to AI agents — auth, permissions, lifecycle) and **Microsoft Agent 365** / the **Microsoft 365 admin center Agent Registry** (inventory/discovery/governance surface). Per Microsoft's own convergence doc: "Agent 365 becomes the unified registry and control plane for agents, while Microsoft Entra continues to provide the identity foundation through Agent ID." The M365 admin center Agent Registry (doc updated 2026-08-27) classifies agents into four types (Microsoft agents, external partner-built agents, published-by-org, shared-by-creator), tracks "agents without owners" and "unmanaged agents" (created outside Agent 365, lacking its risk protection/observability) as governance risk signals, supports filtering by status/publisher type/channel/platform/data source, and flags a "Shadow agent" risk type specifically when "Agent has no registry entry, no owner, or no Microsoft Entra Agent ID" — i.e., registry presence + Entra Agent ID are treated as the baseline discoverability/governance signal.
  SOURCE: https://learn.microsoft.com/en-us/entra/agent-id/agent-registry-convergence ; https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry
- FINDING: A Microsoft Graph API for the Agent Registry (list all agents in inventory, get agent details) is in **preview**, intended for programmatic/bulk governance workflows rather than only the admin UI.
  SOURCE: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry
- FINDING: Azure API Center separately supports registering and managing A2A-style agents ("Register and Manage Agents in Azure API Center") as a companion capability to its MCP-server registry, aimed at making agents discoverable and centrally inventoried for an organization.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/agent-to-agent-overview
- CAVEAT/GAP: No official vendor documentation was found for a standalone "Agent Name Service" as a shipped product; this appears to be a research/community proposal, not an official spec. Do not present it as vendor-backed without further verification.

### 6. Routing patterns (semantic retrieval, gateways, virtual servers)

- FINDING: Anthropic's Tool Search Tool is itself a form of built-in semantic/lexical tool retrieval (BM25/regex-based per the growthmethod summary of Anthropic's docs) operating over deferred tool schemas — i.e., "semantic tool retrieval" is now a first-class, vendor-shipped primitive rather than only a custom RAG layer developers build themselves.
  SOURCE: https://www.anthropic.com/engineering/advanced-tool-use
- FINDING: Microsoft Foundry's `toolbox_search` is explicitly BM25-based lexical/semantic retrieval over tool name + description + parameter metadata, with an explicit escape hatch (`pin`, `additional_search_text`) for tuning retrieval precision without touching the underlying MCP server — this is a documented "gateway curates a virtual, per-context subset of a larger tool catalogue" pattern at the toolbox level.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search
- FINDING: Amazon Bedrock AgentCore Gateway is AWS's official "virtual server" / tool-federation gateway pattern: "An AgentCore gateway is a central access point that serves as a unified interface for AI agents to discover and interact with tools. It handles authentication, request routing, and protocol translation between MCP and your APIs." It federates targets (Lambda functions, OpenAPI specs, Smithy models, or other MCP servers) behind one MCP-compliant endpoint, performs "intelligent tool discovery," and acts as an OAuth resource server for inbound authorization (compatible with Cognito, Okta, Auth0, or custom OAuth providers).
  SOURCE: https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/ ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-MCPservers.html
- FINDING: Azure API Center's MCP-server registry plus its own "expose the catalog as an MCP server" capability together implement a curated-subset gateway pattern at the org level: developers/agents discover a governed, pre-reviewed set of MCP servers through the API Center portal or its MCP endpoint rather than reaching arbitrary servers directly.
  SOURCE: https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server ; https://learn.microsoft.com/en-us/azure/api-center/discover-catalog-mcp-server
- FINDING: OpenAI's documented fallback to full tool-search is architectural sub-agent decomposition — "split into role-specific sub-agents (4 to 6 tools each)" — i.e., hierarchical/supervisor routing where a top-level orchestrator delegates to narrowly-scoped sub-agents, each with a small enough tool surface to avoid the accuracy degradation documented in section 1.
  SOURCE: https://developers.openai.com/api/docs/guides/tools-connectors-mcp

## Code / Config

Anthropic — enabling Tool Search Tool with `defer_loading`:
```json
{
  "tools": [
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {
      "name": "github.createPullRequest",
      "defer_loading": true
    }
  ]
}
```
SOURCE: https://www.anthropic.com/engineering/advanced-tool-use

Anthropic — Programmatic Tool Calling opt-in and code-execution pattern:
```json
{ "type": "code_execution_20250825", "name": "code_execution" }
```
```json
{ "name": "get_team_members", "allowed_callers": ["code_execution_20250825"] }
```
```python
team = await get_team_members("engineering")
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])
# Only final results return to Claude's context
```
SOURCE: https://www.anthropic.com/engineering/advanced-tool-use

OpenAI — hosted MCP `allowed_tools` and `defer_loading`:
```json
{
  "type": "mcp",
  "server_label": "dmcp",
  "server_url": "https://dmcp-server.deno.dev/mcp",
  "allowed_tools": ["roll"]
}
```
```json
{
  "type": "mcp",
  "server_label": "dmcp",
  "defer_loading": true
}
```
```json
{
  "require_approval": {
    "never": { "tool_names": ["ask_question", "read_wiki_structure"] }
  }
}
```
SOURCE: https://developers.openai.com/api/docs/guides/tools-connectors-mcp

Microsoft Foundry — enabling `toolbox_search` (REST):
```http
POST {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Content-Type: application/json

{
  "description": "Large toolbox with tool search enabled",
  "tools": [
    { "type": "toolbox_search" },
    {
      "type": "mcp",
      "server_label": "github",
      "server_url": "https://api.githubcopilot.com/mcp",
      "require_approval": "never",
      "project_connection_id": "github-mcp-conn"
    }
  ]
}
```
Pinning a critical tool and adding search keywords:
```json
{
  "type": "mcp",
  "server_label": "analytics",
  "server_url": "https://db-mcp.internal/sse",
  "tool_configs": {
    "execute_query": {
      "pin": true,
      "additional_search_text": "SQL database analytics reporting dashboard queries"
    }
  }
}
```
SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search

GitHub MCP server — scoping toolsets:
```bash
github-mcp-server --toolsets repos,issues,pull_requests,actions,code_security
# or
GITHUB_TOOLSETS="repos,issues,pull_requests,actions,code_security" ./github-mcp-server
```
SOURCE: https://github.com/github/github-mcp-server

MCP spec — tool with `outputSchema` and `structuredContent` response:
```json
{
  "name": "get_weather_data",
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": { "type": "number" },
      "conditions": { "type": "string" },
      "humidity": { "type": "number" }
    },
    "required": ["temperature", "conditions", "humidity"]
  }
}
```
```json
{
  "result": {
    "content": [{ "type": "text", "text": "{\"temperature\": 22.5, ...}" }],
    "structuredContent": { "temperature": 22.5, "conditions": "Partly cloudy", "humidity": 65 }
  }
}
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools

MCP spec — tool execution error (actionable, self-correctable):
```json
{
  "result": {
    "content": [{ "type": "text", "text": "Invalid departure date: must be in the future. Current date is 08/08/2025." }],
    "isError": true
  }
}
```
SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools

A2A — well-known Agent Card location:
```
GET https://{agent-server-domain}/.well-known/agent-card.json
```
SOURCE: https://a2a-protocol.org/latest/topics/agent-discovery/

## Caveats / Gaps

- The MCP spec version cited throughout (2026-07-28) is very recent; the blog post announcing it is titled with "spec-ga," but section 4's `server/discover` content was captured from search-engine summaries plus a partial fetch — the full normative text of `/specification/2026-07-28/server/discover` was not independently fetched in this pass and should be re-verified before quoting SHOULD/MUST language from it.
- GitHub MCP server's previously-reported "dynamic toolset discovery" beta (`GITHUB_DYNAMIC_TOOLSETS` / `--dynamic-toolsets`) could not be confirmed in the current official README — it may be deprecated, renamed, or simply undocumented at present. Flag as unverified/possibly stale rather than citing it as a live feature.
- "One MCP server per bounded context vs. mega-server" has no single normative MCP-spec statement; the position here is synthesized from the naming-collision warning and GitHub's own toolset design, not a direct vendor recommendation. Label any best-practice rule built on this as **derived/vendor-pattern**, not spec-mandated.
- "Agent Name Service" (section 5 of the brief) — no official/vendor source found; treat as out of scope for a vendor-doc-grounded best-practices document unless a primary source surfaces later.
- A2A Agent Card **JWS signing / canonicalization** mechanics were summarized from a secondary fetch of the agent-discovery topic page, not the full AgentCardSignature schema in the specification — re-fetch `https://a2a-protocol.org/latest/specification/` (JSON schema section) before citing exact signature field names in the final best-practices doc.
- RAG-MCP, LiveMCPBench, and MCP-Bench are arXiv research papers, not vendor documentation — they are cited here as evidence per the task brief's explicit request, but are lower-authority than vendor docs; treat any numbers from them as "reported by independent researchers," not vendor-verified benchmarks. None have been independently reproduced by this research pass.
- OpenAI's "fewer than 20 functions" and "~100 tools in-distribution for o3/o4-mini" guidance are both explicitly framed by OpenAI itself as soft/approximate ("soft suggestion," "as of May 2025") — do not present as hard limits.
- Microsoft Foundry Tool Search is a Foundry-specific (Azure AI Foundry Agent Service) feature at the toolbox layer; it is distinct from, and should not be conflated with, Anthropic's or OpenAI's tool-search primitives even though the pattern and even some field names (`tool_search`) are similar — verify which product a reader is targeting before reusing sample code across vendors.
- The Microsoft Entra Agent ID "what-is-agent-registry" URL initially targeted did not resolve to the expected Entra-specific page in this pass; the M365 admin center Agent Registry page was fetched instead and is a close but not identical surface (Copilot/M365 agent inventory vs. Entra Agent ID's programmatic agent identity registry). Re-verify `https://learn.microsoft.com/en-us/entra/agent-id/what-is-agent-registry` directly if the final doc needs Entra-specific (rather than M365-admin-specific) registry language.

## Sources

- https://www.anthropic.com/engineering/advanced-tool-use — Introducing advanced tool use on the Claude Developer Platform
- https://www.anthropic.com/engineering/code-execution-with-mcp — Code execution with MCP: Building more efficient agents
- https://www.anthropic.com/engineering/writing-tools-for-agents — Writing Effective Tools for Agents — with Agents
- https://arxiv.org/abs/2505.03275 — RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation
- https://arxiv.org/abs/2508.01780 — LiveMCPBench: Can Agents Navigate an Ocean of MCP Tools?
- https://arxiv.org/abs/2508.20453 — MCP-Bench: Benchmarking Tool-Using LLM Agents with Complex Real-World Tasks via MCP Servers
- https://developers.openai.com/api/docs/guides/function-calling — Function calling (OpenAI API guide)
- https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide — o3/o4-mini Function Calling Guide
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp — MCP and Connectors (OpenAI Responses API guide)
- https://modelcontextprotocol.io/seps/986-specify-format-for-tool-names — SEP-986: Specify Format for Tool Names
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools — MCP Specification 2026-07-28: Tools
- https://blog.modelcontextprotocol.io/posts/2026-07-28/ — The 2026-07-28 Specification (MCP blog)
- https://modelcontextprotocol.io/registry/about — The MCP Registry
- https://github.com/github/github-mcp-server — GitHub MCP Server (README: toolsets, read-only mode)
- https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search — Enable tool search in a toolbox (Microsoft Foundry)
- https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server — Inventory and Discover MCP Servers in Your API Center
- https://learn.microsoft.com/en-us/azure/api-center/discover-catalog-mcp-server — Discover APIs With Azure API Center MCP Server
- https://learn.microsoft.com/en-us/azure/api-center/agent-to-agent-overview — Register and Manage Agents in Azure API Center
- https://learn.microsoft.com/en-us/azure/azure-functions/register-mcp-server-api-center — Register MCP servers hosted in Azure Functions in Azure API Center
- https://learn.microsoft.com/en-us/entra/agent-id/agent-registry-convergence — Agent Registry convergence with Microsoft Agent 365
- https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry — Agent Registry in Microsoft 365 admin center
- https://a2a-protocol.org/latest/specification/ — Agent2Agent (A2A) Protocol Specification (v1.0.0)
- https://a2a-protocol.org/latest/topics/agent-discovery/ — Agent Discovery (A2A Protocol)
- https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/ — Introducing Amazon Bedrock AgentCore Gateway
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-MCPservers.html — MCP servers targets (Amazon Bedrock AgentCore)

## Implications for a best-practices doc

Candidate rules, each traced to a source and marked evidence-backed vs. vendor opinion:

1. **Keep the live/exposed tool count per request small (rule of thumb ~10-20 for general tool-calling models; hard-check against ~100 for o-series-class models); measure, don't assume.**
   Evidence-backed (vendor-stated numeric guidance) — SOURCE: https://developers.openai.com/api/docs/guides/function-calling ; https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide. Anthropic and Microsoft Foundry both independently converge on "10-15+ tools" as the threshold where deferred loading/tool-search becomes worthwhile.
   SOURCE: https://www.anthropic.com/engineering/advanced-tool-use ; https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search

2. **Above that threshold, use vendor-native deferred/on-demand tool loading (Anthropic `defer_loading` + Tool Search Tool; OpenAI hosted-MCP `defer_loading`/`allowed_tools`/`tool_search`; Foundry `toolbox_search`) instead of hand-rolled RAG-over-tools where a vendor primitive exists.**
   Evidence-backed with quantified gains (accuracy +25-38pp, tokens −85-94%) — SOURCE: https://www.anthropic.com/engineering/advanced-tool-use ; https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search. Where no vendor primitive is available, semantic retrieval over a tool index (RAG-MCP pattern) is a documented, evidence-backed fallback.
   SOURCE: https://arxiv.org/abs/2505.03275

3. **For heavy multi-step / data-shuttling workflows, prefer code-execution-based tool orchestration over chained natural-language tool calls to keep intermediate results out of context.**
   Evidence-backed (98.7% token reduction case study; 37% average reduction across a broader eval) — SOURCE: https://www.anthropic.com/engineering/code-execution-with-mcp ; https://www.anthropic.com/engineering/advanced-tool-use

4. **Every tool MUST have a clear, non-vague description; treat description quality as the primary lever for both selection accuracy and search-based discoverability.**
   Evidence-backed — Foundry: "A tool without a description, or with a vague one, is unlikely to be returned even for relevant queries" (SOURCE: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search); Anthropic: description refinements alone drove accuracy from ~60-70% to 80-90% on held-out evals (SOURCE: https://www.anthropic.com/engineering/writing-tools-for-agents); OpenAI: "Write clear and detailed function names, parameter descriptions, and instructions" (SOURCE: https://developers.openai.com/api/docs/guides/function-calling).

5. **Namespace tools consistently (prefix or suffix by service/resource) once an agent spans multiple servers/toolsets; pick one convention and note that the choice itself measurably affects eval results.**
   Evidence-backed (Anthropic explicitly measured non-trivial effects from prefix-vs-suffix choice) — SOURCE: https://www.anthropic.com/engineering/writing-tools-for-agents. Reinforced by the MCP spec's collision-disambiguation-by-server-prefix guidance.
   SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools

6. **Follow the MCP tool-naming character/length rules exactly as published in the live spec (1-128 chars, `A-Z a-z 0-9 _ - .`, case-sensitive, unique within a server) — do not rely on the older SEP-986 text (64 chars, includes `/`), which the current spec has superseded.**
   Evidence-backed, spec-normative (SHOULD-level) — SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools (current) vs. https://modelcontextprotocol.io/seps/986-specify-format-for-tool-names (historical/superseded).

7. **Consolidate multi-step API sequences into single workflow-shaped tools rather than exposing raw CRUD/API-wrapper endpoints 1:1.**
   Vendor opinion, but explicitly and repeatedly stated as Anthropic's top design principle ("More tools don't always lead to better outcomes") — SOURCE: https://www.anthropic.com/engineering/writing-tools-for-agents

8. **Return token-efficient, semantically meaningful tool output (named fields over raw IDs; pagination/truncation with sane defaults; a response-verbosity switch where feasible); give actionable, self-correctable error text, not raw codes/tracebacks.**
   Vendor opinion (design guidance), but backed by the MCP spec's own error-handling distinction (protocol vs. execution errors) as the normative hook — SOURCE: https://www.anthropic.com/engineering/writing-tools-for-agents ; https://modelcontextprotocol.io/specification/2026-07-28/server/tools

9. **Design MCP servers to filter `tools/list` by the caller's authorization — only advertise tools the caller may actually invoke — rather than relying solely on deny-at-call-time.**
   Evidence-backed, spec-normative (MAY-level, explicitly sanctioned) — SOURCE: https://modelcontextprotocol.io/specification/2026-07-28/server/tools

10. **Scope MCP servers to a bounded context (toolset/domain) rather than building a single mega-server exposing everything; use toolset-style sub-grouping (GitHub's model) even within one server if a true split isn't practical.**
    Derived/vendor-pattern, not spec-mandated — SOURCE: https://github.com/github/github-mcp-server (worked example) — flagged as a synthesis in this research, not a direct MCP-spec rule.

11. **For agent-level (not tool-level) discovery, publish a well-known Agent Card (A2A `.well-known/agent-card.json`) with accurate `skills`, `securitySchemes`, and (where trust matters) a JWS signature; register agents in an enterprise registry (Entra Agent ID/Agent 365, Azure API Center) so ownership, risk, and discoverability are tracked centrally rather than left as "shadow agents."**
    Evidence-backed for the mechanics (spec-normative for A2A; product-documented for Microsoft's registries) — SOURCE: https://a2a-protocol.org/latest/topics/agent-discovery/ ; https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry (explicit "Shadow agent" risk = no registry entry/owner/Entra Agent ID).

12. **At the platform/org level, front large or federated tool/server catalogues with a governed gateway that exposes only a curated, per-team/per-use-case subset (virtual server pattern) rather than letting every agent reach every registered server directly.**
    Evidence-backed as a shipped pattern across two vendors (AWS AgentCore Gateway, Azure API Center) — SOURCE: https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/ ; https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server

13. **Treat the official MCP Registry as a public-metadata discovery layer only — do not expect it to host or vet private/internal servers; stand up an internal registry (e.g., Azure API Center, or a registry implementing the same OpenAPI spec) for enterprise governance.**
    Evidence-backed, explicitly stated by the registry's own docs (preview status; "does not support private servers") — SOURCE: https://modelcontextprotocol.io/registry/about
