# 08 - Primary-source verification of key claims

Verified 2026-09-17 against the original documents (raw HTML, PDFs, GitHub source), not summaries. Quotes are verbatim from the source.

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Beurer-Kellner et al., six design patterns | CONFIRMED |
| 2 | OWASP Agentic Top 10 (2026), ASI01-ASI10 | CONFIRMED (two titles use "and", not "&") |
| 3 | OWASP MCP Top 10 status and IDs | CONFIRMED beta; CORRECTED MCP06 title (site and repo disagree) |
| 4 | Meta Agents Rule of Two | CONFIRMED |
| 5 | Google secure AI agents, three principles | CONFIRMED (they come from the agents paper, not SAIF itself) |
| 6 | Azure AI Content Safety feature status | CONFIRMED with detail (only Prompt Shields is GA) |
| 7 | GitHub MCP server dynamic toolsets | CORRECTED: removed on 2026-05-20 |
| 8 | MCP 2026-07-28: discover, tool names, token passthrough, annotations | CONFIRMED |
| 9 | Enterprise-Managed Authorization extension (ID-JAG) | CONFIRMED: Stable, official extension |
| 10 | Anthropic numbers (84%, 93%, 17%, 49%->74%) | CONFIRMED (84% wording differs slightly) |
| 11 | OpenAI "fewer than 20" functions | CONFIRMED |
| 12 | Entra CA / ID Protection for agents need Agent 365 | CONFIRMED; Agent ID is GA |
| 13 | OTel GenAI agent spans stability | CONFIRMED: Development; conventions moved to a new repo |

---

## 1. Design Patterns for Securing LLM Agents against Prompt Injections

**CONFIRMED.** arXiv:2506.08837, first submitted 10 Jun 2025, now at v3. Section 3.1 names the patterns like this:

1. **"The Action-Selector Pattern."** "The agent acts merely as an action selector, which translates incoming requests (presumably expressed in natural language) to one or more predefined tool calls." It stops tool output from feeding back into the agent.
2. **"The Plan-Then-Execute Pattern."** The agent sets a fixed plan before it touches untrusted data. "A prompt injection cannot force the LLM into executing a tool that is not part of the defined plan."
3. **"The LLM Map-Reduce Pattern."** "Untrusted documents are processed independently, to ensure that a malicious document cannot impact the processing of another document."
4. **"The Dual LLM Pattern"**: "A privileged LLM has access to tools but never processes untrusted data. This LLM can call a quarantined LLM to process untrusted data, but without any tool access."
5. **"The Code-Then-Execute Pattern."** "The LLM writes a piece of code that can call tools and make calls to other LLMs. The code is then run on untrusted data."
6. **"The Context-Minimization pattern."** "The user's prompt informs the actions of the LLM agent (e.g., a call to a specific tool), but is removed from the LLM's context thereafter."

Gotcha: pattern 3 is "LLM Map-Reduce", not just "Map-Reduce". The paper's summary table uses short labels: Action-selector, Plan-then-exec., Map-reduce, Dual LLM, Code-then-exec., Context-min.

Source: https://arxiv.org/abs/2506.08837 (HTML: https://arxiv.org/html/2506.08837)

## 2. OWASP Top 10 for Agentic Applications for 2026

**CONFIRMED.** The resource page is dated December 9, 2025. These titles come from the table of contents in the official PDF:

- ASI01: Agent Goal Hijack
- ASI02: Tool Misuse and Exploitation
- ASI03: Identity and Privilege Abuse
- ASI04: Agentic Supply Chain Vulnerabilities
- ASI05: Unexpected Code Execution (RCE)
- ASI06: Memory & Context Poisoning
- ASI07: Insecure Inter-Agent Communication
- ASI08: Cascading Failures
- ASI09: Human-Agent Trust Exploitation
- ASI10: Rogue Agents

Gotcha: the PDF uses "and" in ASI02 and ASI03 but "&" in ASI06. The announcement blog post shortens ASI02 to "Tool Misuse" and writes ASI03 as "Identity & Privilege Abuse". Cite the PDF titles.

Sources:
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- PDF: https://genai.owasp.org/download/52117/
- https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/

## 3. OWASP MCP Top 10

**Status CONFIRMED as beta.** Roadmap wording: "Phase 3 – Beta Release and Pilot Testing - We are here right now. Release a "beta" version of MCP Top 10." The GitHub repo adds: "Phase 5 – Continuous Improvement & Next Release in October 2026". IDs carry a `:2025` suffix.

**MCP06 is CORRECTED: the live site and the source repo don't match.**

| ID | Published owasp.org page (fetched 2026-09-17) | GitHub `main` index.md (last change 2026-07-29) |
|----|---|---|
| MCP01:2025 | Token Mismanagement & Secret Exposure | same |
| MCP02:2025 | Privilege Escalation via Scope Creep | same |
| MCP03:2025 | Tool Poisoning | same |
| MCP04:2025 | Software Supply Chain Attacks & Dependency Tampering | same |
| MCP05:2025 | Command Injection & Execution | same |
| MCP06:2025 | Prompt Injection via Contextual Payloads | **Intent Flow Subversion** (renamed in commit "add-intent-flow-subversion", 2026-01-12) |
| MCP07:2025 | Insufficient Authentication & Authorization | same |
| MCP08:2025 | Lack of Audit and Telemetry | same |
| MCP09:2025 | Shadow MCP Servers | same |
| MCP10:2025 | Context Injection & Over-Sharing | same |

Recommendation: use "MCP06:2025 – Intent Flow Subversion" and add a note that the owasp.org page still shows the older name. The published site hasn't been rebuilt, and the new MCP06 detail page returns 404 on owasp.org.

Sources:
- https://owasp.org/www-project-mcp-top-10/
- https://github.com/OWASP/www-project-mcp-top-10/blob/main/index.md

## 4. Meta "Agents Rule of Two"

**CONFIRMED.** Published October 31, 2025.

> "At a high level, the Agents Rule of Two states that until robustness research allows us to reliably detect and refuse prompt injection, agents must satisfy no more than two of the following three properties within a session to avoid the highest impact consequences of prompt injection.
> [A] An agent can process untrustworthy inputs
> [B] An agent can have access to sensitive systems or private data
> [C] An agent can change state or communicate externally"

> "If an agent requires all three without starting a new session (i.e., with a fresh context window), then the agent should not be permitted to operate autonomously and at a minimum requires supervision — via human-in-the-loop approval or another reliable means of validation."

Source: https://ai.meta.com/blog/practical-ai-agent-security/

## 5. Google's approach for secure AI agents

**CONFIRMED, with a note on where the principles come from.** They are in the May 2025 paper "Google's Approach for Secure AI Agents: An Introduction" by Santiago Díaz, Christoph Kern and Kara Olive. The research page lists it as "An Introduction to Google's Approach for Secure AI Agents". The paper builds on SAIF ("Secure AI Framework (SAIF)"), but the three principles belong to the agents paper. SAIF's own elements are different. Don't label these "the SAIF principles".

- "Principle 1: Agents must have well-defined human controllers"
- "Principle 2: Agent powers must have limitations"
- "Principle 3: Agent actions and planning must be observable"

The paper introduces them with: "we propose that agentic product developers should adopt three core principles for agent security."

Sources:
- https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/
- PDF: https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf

## 6. Azure AI Content Safety: feature status

**CONFIRMED.** Only Prompt Shields is GA. The other three features are still preview.

| Feature | Status | Verified wording |
|---|---|---|
| Prompt Shields | **GA** | What's new, August 2024: "The Prompt Shields API and Protected Material for text API are now generally available (GA)." |
| Spotlighting | **Preview** | Foundry page (updated 2026-09-08): "Spotlighting (preview) Spotlighting provides enhanced protection against indirect attacks when your application processes third-party documents..." and "Spotlighting is only available for models used via the Chat Completions API." It's a Foundry guardrail setting, not a standalone Content Safety API. It isn't mentioned on the Content Safety pages. |
| Task adherence | **Preview** | What's new, November 2025: "Task Adherence public preview". The concept page is titled "Agent Workflows: Task Adherence (preview)". |
| Groundedness detection | **Preview** | The overview lists "Groundedness detection (preview)". "Groundedness correction (preview)" is a separate preview sub-feature. |

Gotcha: turning on spotlighting base-64 encodes documents. That adds tokens and cost, can push large documents over input limits, and the model sometimes mentions the encoding in its answer.

Sources:
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/whats-new
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/task-adherence
- https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields

## 7. GitHub MCP server: dynamic toolsets

**CORRECTED. Dynamic toolset discovery no longer exists.** PR #2512, "refactor: remove dynamic toolsets and deprecated closure constructor", merged 2026-05-20:

> "Removes the dynamic toolset discovery feature (the `--dynamic-toolsets` / `GITHUB_DYNAMIC_TOOLSETS` switch and the meta-tools `enable_toolset`, `list_available_toolsets`, `get_toolset_tools`)... Dynamic mode was local-only — never offered by the remote server."

The current README and `cmd/github-mcp-server/main.go` don't mention "dynamic" anywhere. Tools are now selected with these flags:

- `--toolsets` / `GITHUB_TOOLSETS`: "The GitHub MCP Server supports enabling or disabling specific groups of functionalities via the `--toolsets` flag." "The environment variable `GITHUB_TOOLSETS` takes precedence over the command line argument if both are provided." The `default` toolset is context, repos, issues, pull_requests and users. `all` and `default,<extra>` are also accepted.
- `--tools` / `GITHUB_TOOLS` picks individual tools and can be combined with toolsets. `--exclude-tools` is also available ("Comma-separated list of tool names to disable regardless of other settings").
- `--read-only` / `GITHUB_READ_ONLY=1`: "This will only offer read-only tools". "Read-only mode takes priority: write tools are skipped if `--read-only` is set, even if explicitly requested via `--tools`".
- Other flags now present: `--lockdown-mode`, `--insiders`, `--features`.

Sources:
- https://github.com/github/github-mcp-server/blob/main/README.md
- https://github.com/github/github-mcp-server/pull/2512
- https://github.com/github/github-mcp-server/blob/main/cmd/github-mcp-server/main.go

## 8. MCP specification 2026-07-28

**CONFIRMED.** The repo source matches the live site.

**`server/discover`** (server/discover):
> "`server/discover` lets a client query a server's supported protocol versions, capabilities, and identity before sending any other requests. Servers **MUST** implement it."

> "Calling `server/discover` is optional for clients — a client may invoke any RPC inline and handle `UnsupportedProtocolVersionError` if the server does not support the requested version."

> On stdio: "A client that supports both modern (per-request `_meta`) and legacy (`initialize` handshake) servers **SHOULD** send `server/discover` first"

> "`serverInfo` is self-reported by the server and is not verified by the protocol... Clients **SHOULD NOT** use it to change their behavior, and **SHOULD NOT** rely on it for security decisions."

Changelog: "Add `server/discover`: servers MUST implement this RPC ... (SEP-2575)". The response can be cached (`ttlMs`, `cacheScope`).

**Tool names** (server/tools, "Tool Names"). Every rule is a SHOULD, not a MUST:
> "Tool names **SHOULD** be between 1 and 128 characters in length (inclusive)."
> "Tool names **SHOULD** be considered case-sensitive."
> "The following **SHOULD** be the only allowed characters: uppercase and lowercase ASCII letters (A-Z, a-z), digits (0-9), underscore (_), hyphen (-), and dot (.)"
> "Tool names **SHOULD NOT** contain spaces, commas, or other special characters."
> "Tool names **SHOULD** be unique within a server."

It also says aggregating clients "**SHOULD** implement a disambiguation strategy such as prefixing tool names with a server identifier", and that serverInfo `name` "**SHOULD NOT** be relied upon for disambiguation."

**Tool annotations are untrusted** (server/tools):
> "For trust & safety and security, clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers."

**Token passthrough / audience** (basic/authorization/security-considerations):
> "MCP servers **MUST** only accept tokens specifically intended for themselves and **MUST** reject tokens that do not include them in the audience claim or otherwise verify that they are the intended recipient of the token."
> "The MCP server **MUST NOT** pass through the token it received from the MCP client."

From basic/authorization (Token Handling):
> "MCP servers **MUST** validate that access tokens were issued specifically for them as the intended audience, according to RFC 8707 Section 2."
> "MCP clients **MUST NOT** send tokens to the MCP server other than ones issued by the MCP server's authorization server."

The Security Best Practices page says "token passthrough is explicitly forbidden" and defines it as "an anti-pattern where an MCP server accepts tokens from an MCP client without validating that the tokens were properly issued _to the MCP server_ and passes them through to the downstream API."

Sources:
- https://modelcontextprotocol.io/specification/2026-07-28/server/discover
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations
- https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
- https://modelcontextprotocol.io/specification/2026-07-28/changelog

## 9. Enterprise-Managed Authorization extension (ID-JAG)

**CONFIRMED: official extension, marked Stable.**

- Extension ID: `io.modelcontextprotocol/enterprise-managed-authorization`
- The spec lives at `specification/stable/` in the ext-auth repo and starts with "**Status**: Stable".
- Wording: "The MCP Client requests a special type of token from the enterprise IdP called an Identity Assertion JWT Authorization Grant, or ID-JAG. The MCP Client then exchanges the ID-JAG for an access token from the MCP server's Authorization Server". The spec "defines an application of the "Identity Assertion JWT Authorization Grant" [draft-ietf-oauth-identity-assertion-authz-grant] for use within enterprise deployments of the Model Context Protocol (MCP)."
- It's an extension, not part of the core spec. Client support is tracked separately in the extensions client matrix.

Sources:
- https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization
- https://github.com/modelcontextprotocol/ext-auth/blob/main/specification/stable/enterprise-managed-authorization.mdx
- https://modelcontextprotocol.io/extensions/auth/overview

## 10. Anthropic engineering posts

**CONFIRMED.** The first quote differs slightly from how the claim was worded.

- **Sandboxing** (published Oct 20, 2025): "In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%." Quote it as "reduces permission prompts by 84%", not "84% fewer permission prompts".
  https://www.anthropic.com/engineering/claude-code-sandboxing
- **Auto mode** (published Mar 25, 2026):
  - "Claude Code users approve 93% of permission prompts." Also: "in practice users accept 93% of them anyway."
  - 17%: from Table 1, full pipeline (Stage 1->Stage 2) on "Real overeager n=52": "0.4% FPR 17% FNR". The text says: "The 17% false-negative rate on real overeager actions is the honest number." Real traffic (n=10,000) has 0.4% FPR, and synthetic exfil (n=1,000) has 5.7% FNR.
  - Gotcha: 17% is measured on a small set (n=52) of real overeager actions. It isn't a miss rate across all traffic.
  https://www.anthropic.com/engineering/claude-code-auto-mode
- **Tool Search Tool** (published Nov 24, 2025): "Opus 4 improved from 49% to 74%, and Opus 4.5 improved from 79.5% to 88.1% with Tool Search Tool enabled." These are "MCP evaluations when working with large tool libraries". The same post reports an "85% reduction in token usage".
  https://www.anthropic.com/engineering/advanced-tool-use

## 11. OpenAI: number of functions

**CONFIRMED.**
> "Keep the number of initially available functions small for higher accuracy. Evaluate your performance with different numbers of functions. Aim for fewer than 20 functions available at the start of a turn at any one time, though this is just a soft suggestion. Use tool search to defer large or infrequently used parts of your tool surface instead of exposing e[verything]..."

Note: the current wording is "at the start of a turn" and points to tool search. platform.openai.com now redirects to developers.openai.com.

Source: https://developers.openai.com/api/docs/guides/function-calling (redirected from https://platform.openai.com/docs/guides/function-calling)

## 12. Microsoft Entra: Agent 365 licence for CA / ID Protection

**CONFIRMED.** Enforcement is announced but not yet active.

- Conditional Access for agents (page updated 2026-07-01): "Conditional Access for agents requires Microsoft Entra ID P1 or P2 and a Microsoft Agent 365 license for each user. Enforcement of Agent 365 licensing is coming soon."
- Licensing page: "Conditional Access for agents requires a Microsoft Agent 365 license to apply policies to agents through Microsoft Entra Agent ID. This can be with one of the following license plans: - Microsoft 365 E7, which includes Agent 365 and Microsoft Entra Suite, ..."
- ID Protection for agents: "Starting soon, ID Protection for agents will require a Microsoft Agent 365 license to extend protection to agents through Microsoft Entra Agent ID."
- What is Agent ID: "Agent ID is available for all Microsoft Entra customers." and "Extending Microsoft Entra security features to agents requires Microsoft Agent 365. Agent 365 is included with Microsoft 365 E7 and is available as an add-on to Microsoft E5/A5/Business Premium (or Microsoft Defender Suite + Microsoft Purview Suite)."
- **Agent ID is GA.** The What's new page (ms.date 2026-05-01) says: "Microsoft Entra Agent ID is now generally available." Secondary sources put GA in April 2026, but the Microsoft page doesn't give the date. Some sub-features are still preview, such as the "Create an agent identity (Preview)" wizard and the CA condition "Agent execution environments (Preview)".

Sources:
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/agent-id
- https://learn.microsoft.com/en-us/entra/fundamentals/licensing
- https://learn.microsoft.com/en-us/entra/id-protection/concept-risky-agents
- https://learn.microsoft.com/en-us/entra/agent-id/what-is-microsoft-entra-agent-id
- https://learn.microsoft.com/en-us/entra/agent-id/whats-new-agent-id

## 13. OpenTelemetry GenAI semantic conventions

**CONFIRMED: Development (not stable).** New finding: the GenAI conventions have moved out of the main semconv repo. The old pages now say: "GenAI semantic conventions have moved to the OpenTelemetry GenAI semantic conventions repository. This page has moved and is no longer maintained in this repository."

In `open-telemetry/semantic-conventions-genai` (which references semconv v1.44.0):
- gen-ai-agent-spans.md: document "**Status**: Development"
- "Create agent span", "Invoke agent client span", "Invoke agent internal span" and "Invoke workflow span" are each "Status: Development".
- "Execute tool span" (gen-ai-spans.md): "Status: Development"
- `gen_ai.operation.name` values `create_agent`, `execute_tool` and `invoke_agent` are all Development.

Update any links that point at `open-telemetry/semantic-conventions/docs/gen-ai/`.

Sources:
- https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md
- https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md
- https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/README.md (moved notice)
