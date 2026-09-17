# GitHub Repos Research: Open-source reference implementations and tooling for enterprise MCP and agent controls
SOURCE_TYPE: github-repos
CONFIDENCE: HIGH
GENERATED: 2026-09-17T00:00:00+05:30

## Summary
The enterprise MCP/agent control landscape has consolidated fast in 2026: two credible general-purpose gateways lead (agentgateway, CNCF-adjacent/Linux-Foundation-style community project with 4.9k stars and Rust core; IBM's mcp-context-forge with 4.5k stars and the broadest feature surface — registry, RBAC, SSO, plugins). Microsoft ships its own Kubernetes-native gateway (microsoft/mcp-gateway) that is narrower in scope (routing/lifecycle, not full AuthZ/virtual-server policy). Auth reference material for MCP is strongest inside Azure-Samples/AI-Gateway (actively maintained, updated within the last week) rather than the now-stale standalone remote-mcp-apim-functions-python sample. Security scanning for MCP/agents is a genuinely three-way, all-active field (Snyk Agent Scan — formerly Invariant Labs' mcp-scan, Cisco AI Defense mcp-scanner, and prompt-based red-teaming via promptfoo/garak), but all vendors flag their CLI output as "experimental, subject to change" — none of this tooling is stable enough to hard-wire into CI gates yet. Sandboxing has real production-grade options (gVisor, Kata, E2B, Anthropic's sandbox-runtime) rather than roll-your-own. Policy engines (OPA, Cedar) are general-purpose and not agent-native — no widely-adopted "agent policy DSL" exists yet, so teams are bolting OPA/Cedar or gateway-embedded CEL expressions onto tool calls. A2A protocol tooling (a2aproject) is healthy and Linux-Foundation-governed with 25.8k stars on the spec repo. One notable dead end: Microsoft's own PyRIT red-teaming tool moved from `Azure/PyRIT` (now archived, redirect only) to `microsoft/PyRIT` — cite the new location.

## Key Findings

### 1. MCP Gateways / Proxies

- FINDING: **microsoft/mcp-gateway** — reverse proxy + control plane for MCP servers in Kubernetes; session-aware stateful routing, adapter/tool CRUD, bearer-token/RBAC auth on both data and control planes, optional "Agents & Sessions" preview tied to Azure AI Foundry. C#, MIT license, 837 stars, 91 forks, last push 2026-09-11 (12 days before this report — active). Maturity: beta — "Agents (Preview)" is explicitly gated behind a Foundry endpoint config flag; no mention of an out-of-the-box audit/SIEM export.
  SOURCE: https://github.com/microsoft/mcp-gateway

- FINDING: **agentgateway/agentgateway** — "Next Generation Agentic Proxy for AI Agents and MCP servers," Rust core, Kubernetes Gateway API-native, part of the Solo.io-driven agentgateway.dev project (positioning itself as an Envoy-adjacent, CNCF-style community effort). Apache-2.0, 4,894 stars, 853 forks, last push 2026-09-17 (today — most actively developed of the group). Ships CEL-based `mcpAuthorization` rules for per-tool access control, JWT auth, backend auth passthrough, mTLS, rate limiting, and a large `examples/` tree (auth, authz, cross-app-access, A2A traffic, LLM routing). Maturity: production-track — used as the reference implementation in multiple vendor workshops (Solo.io's own enterprise-agentgateway-workshop).
  SOURCE: https://github.com/agentgateway/agentgateway

- FINDING: **docker/mcp-gateway** — the `docker mcp` CLI plugin's gateway; wraps MCP servers as Docker Desktop/Docker Engine-managed containers with a catalog-driven trust model (Docker Hub MCP Catalog). Go, MIT, 1,570 stars, 277 forks, last push 2026-09-16. High open-issue count (144) relative to maturity signals — consumer/dev-desktop oriented rather than enterprise K8s control plane. Maturity: beta, strongest fit for local/dev trust boundaries, not a drop-in enterprise AuthZ layer.
  SOURCE: https://github.com/docker/mcp-gateway

- FINDING: **IBM/mcp-context-forge** — "AI Gateway, registry, and proxy" in front of MCP, A2A, and REST/gRPC APIs: unified endpoint, centralized discovery, guardrails, plugin framework, JWT auth, federation, SSO (dedicated `docker-compose.sso.yml`), and OpenTelemetry/Phoenix/Langfuse observability integrations. Apache-2.0, Python (recently added a Rust component per `Cargo.toml`), 4,484 stars, 869 forks, last push 2026-09-17 (today). Largest open-issue count of the group (915) — reflects both popularity and surface area. Maturity: most feature-complete of the OSS gateways; explicit `plugins/` architecture makes it the closest thing to a policy/guardrail integration point among the gateways.
  SOURCE: https://github.com/IBM/mcp-context-forge

- FINDING: **Azure-Samples/AI-Gateway** — not a gateway product but Microsoft's canonical lab collection for Azure API Management as an AI/MCP gateway: includes `mcp-client-authorization`, `mcp-prm-oauth` (OAuth Protected Resource Metadata), `mcp-registry-apic` (API Center as MCP registry), and `ai-foundry-private-mcp` labs, each with bicep IaC + Jupyter notebook walkthroughs. MIT, 987 stars, last push 2026-09-16 (yesterday) — far more current than the narrower `remote-mcp-apim-functions-python` sample below. Maturity: reference/lab-grade, Microsoft-maintained, closest thing to an official "MCP + Entra + APIM" enterprise pattern.
  SOURCE: https://github.com/Azure-Samples/AI-Gateway

- FINDING: **kagent-dev/kagent** — "Cloud Native Agentic AI," CNCF-sandbox-adjacent project for running/observing agents on Kubernetes with agentgateway integration. Apache-2.0, 3,751 stars, last push 2026-09-17 (today). Complementary to agentgateway rather than a competing gateway — relevant for the "agent runtime governance" angle, not tool-call-level MCP auth.
  SOURCE: https://github.com/kagent-dev/kagent

### 2. MCP auth reference implementations

- FINDING: **modelcontextprotocol/python-sdk** and **modelcontextprotocol/typescript-sdk** — official SDKs include the reference OAuth 2.1 client/server auth flows (Protected Resource Metadata, dynamic client registration) that the MCP spec itself defines. Python SDK: MIT, 24,322 stars, pushed 2026-09-17 (today). TypeScript SDK: 13,417 stars, pushed 2026-09-17 (today). Both actively maintained by the modelcontextprotocol org (Anthropic-backed, now community-governed). Maturity: production — this is the spec's own reference auth code, not a third-party sample.
  SOURCE: https://github.com/modelcontextprotocol/python-sdk
  SOURCE: https://github.com/modelcontextprotocol/typescript-sdk

- FINDING: **Azure-Samples/mcp-auth-servers** — "Reference MCP servers that demo how authentication works with the current Model Context Protocol spec." MIT, 50 stars, last push 2026-01-07 — over 8 months stale relative to this report. Maturity: reference/experimental, worth checking against the current spec before reuse since MCP auth semantics changed multiple times through 2025–2026.
  SOURCE: https://github.com/Azure-Samples/mcp-auth-servers

- FINDING: **Azure-Samples/remote-mcp-apim-functions-python** — "Azure API Management as AI Gateway to Remote MCP servers," bicep-deployed APIM + Azure Functions MCP server with OAuth client authorization flow (screenshot: `mcp-client-authorization.gif`). MIT, 129 stars, last push 2025-10-02 — nearly a year stale versus AI-Gateway's labs, which cover the same ground and are updated weekly. Maturity: superseded in practice by the `mcp-client-authorization` and `mcp-prm-oauth` labs inside Azure-Samples/AI-Gateway; still fine as a minimal single-purpose starting point.
  SOURCE: https://github.com/Azure-Samples/remote-mcp-apim-functions-python

- FINDING: agentgateway ships dedicated `traffic-cross-app-access`, `traffic-oidc`, `traffic-oauth2-proxy`, `traffic-jwt-sign`, and `traffic-token-exchange` examples covering Entra/Okta-style cross-app access token exchange patterns — the closest OSS equivalent to a vendor-neutral "cross-app access" reference (no dedicated Keycloak/Auth0/Okta-branded sample repo found with meaningful adoption; most `keycloak-mcp*` repos on GitHub are single-author, near-zero-star personal projects, not enterprise references).
  SOURCE: https://github.com/agentgateway/agentgateway/tree/main/examples

- FINDING: There is no widely-adopted, vendor-neutral **Entra On-Behalf-Of (OBO) MCP sample** as a standalone repo; the pattern is instead embedded in Azure-Samples/AI-Gateway's `mcp-prm-oauth` and `ai-foundry-private-mcp` labs (bicep files named `mcp-entra-app.bicep` register the Entra app registration for the MCP server). Direct GitHub code search for "entra mcp obo" and "dynamic sessions azure" as standalone repos returned no meaningful hits beyond these labs.
  SOURCE: https://github.com/Azure-Samples/AI-Gateway/blob/main/labs/mcp-prm-oauth/src/bicep/identity/mcp-entra-app.bicep

### 3. Registries

- FINDING: **modelcontextprotocol/registry** — the official community-driven MCP server registry service (spec org, not a vendor). Custom "other" license (spec-org license, check terms before enterprise redistribution), 7,259 stars, last push 2026-09-16 (yesterday) — actively developed. This is the closest thing to a canonical registry implementation and the natural base for self-hosting a private subregistry.
  SOURCE: https://github.com/modelcontextprotocol/registry

- FINDING: **Azure-Samples/mcp-registry** — "MCP Registry Demo - A reference implementation on Azure API Center," demonstrates using Azure API Center as an enterprise MCP registry/catalog. No license file declared, 13 stars, last push 2025-05-17 — over a year stale. Maturity: superseded by the actively-maintained `mcp-registry-apic` lab inside Azure-Samples/AI-Gateway, which covers the same API Center registry pattern with current tooling (`uv`, current bicep).
  SOURCE: https://github.com/Azure-Samples/mcp-registry
  SOURCE: https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/mcp-registry-apic

### 4. Scanners and security testing

- FINDING: **Invariant Labs' mcp-scan is dead as a name — it was acquired/rebranded as Snyk Agent Scan.** The GitHub search for `invariantlabs-ai/mcp-scan` resolves to `snyk/agent-scan`. Apache-2.0, 3,059 stars, last push 2026-09-17 (today). Scans MCP servers, agent harnesses, and agent skills for prompt injection and malware; explicitly documents that raw CLI output (issue codes, field names, severity labels) is "experimental and subject to change without notice" through v0.5.x and v0.6+; also warns that scanning stdio MCP configs *executes the commands* and recommends running scans inside a sandbox/disposable environment. Maturity: active but explicitly not stable for CI-gate automation; treat as an assisted-review tool, not a pass/fail gate.
  SOURCE: https://github.com/snyk/agent-scan

- FINDING: **cisco-ai-defense/mcp-scanner** — Python tool combining YARA rules, LLM-based analysis, and Cisco AI Defense's inspect API to scan MCP tools/prompts/resources/server instructions; also does vulnerable-dependency scanning (pip-audit/CVE/PYSEC/GHSA), "readiness scanning" for production issues (timeouts, retries, error handling), and VirusTotal binary scanning. Apache-2.0, 1,074 stars, last push 2026-09-17 (today). Maturity: actively developed, broadest scanning-engine combination of the three tools, but ties best results to a paid Cisco AI Defense backend.
  SOURCE: https://github.com/cisco-ai-defense/mcp-scanner

- FINDING: **promptfoo/promptfoo** — general LLM/agent/RAG red-teaming and eval framework with declarative YAML configs and CI/CD integration; used internally by OpenAI and Anthropic per its own README claim. MIT, 25,223 stars, last push 2026-09-17 (today). Maturity: production-grade for prompt/agent evaluation; MCP-specific red-teaming is a plugin within the broader tool, not a standalone MCP scanner.
  SOURCE: https://github.com/promptfoo/promptfoo

- FINDING: **NVIDIA/garak** — "the LLM vulnerability scanner," probe-based red-teaming framework (jailbreaks, prompt injection, data leakage). Apache-2.0, 9,281 stars, last push 2026-09-16 (yesterday). Maturity: active, widely cited academically and in industry red-team writeups; general-LLM focused, not MCP/tool-call specific.
  SOURCE: https://github.com/NVIDIA/garak

- FINDING: **Microsoft's PyRIT moved and its old location is dead.** `Azure/PyRIT` is now **archived** (read-only). The live project is **microsoft/PyRIT**, MIT, 4,489 stars, actively developed — do not cite or fork the Azure/ path. `microsoft/PyRIT-Ship` (70 stars) also exists as a companion/packaging repo. No dedicated OSS "Microsoft AI red teaming agent" repo beyond PyRIT itself was found; the "AI Red Teaming Agent" capability referenced in Microsoft docs is delivered as an Azure AI Foundry *service* built on PyRIT, not a separate standalone open-source repo.
  SOURCE: https://github.com/microsoft/PyRIT
  SOURCE: https://github.com/Azure/PyRIT

### 5. Sandboxes for code execution

- FINDING: **anthropics/sandbox-runtime** (referenced by parent org as anthropic-experimental) — "lightweight sandboxing tool for enforcing filesystem and network restrictions on arbitrary processes at the OS level, without requiring a container." Apache-2.0, 5,260 stars, last push 2026-09-16 (yesterday). Maturity: active, positioned as a lighter-weight alternative to full container/VM isolation for agent code execution — worth flagging that "without a container" means it relies on OS-level (seccomp/landlock-style) controls, a different trust boundary than gVisor/Kata.
  SOURCE: https://github.com/anthropics/sandbox-runtime

- FINDING: **e2b-dev/E2B** — "Open-source, secure environment with real-world tools for enterprise-grade agents"; hosted+self-hostable Firecracker-microVM-backed code execution sandboxes purpose-built for AI agents. Apache-2.0, 13,853 stars, last push 2026-09-17 (today). Maturity: production, the most agent-specific and most-starred of the sandbox options; has a commercial hosted tier alongside the OSS core.
  SOURCE: https://github.com/e2b-dev/E2B

- FINDING: **google/gvisor** — "Application Kernel for Containers," user-space kernel providing an isolation boundary between containers and the host. Apache-2.0, 19,340 stars, last push 2026-09-17 (today). Maturity: production, battle-tested (backs Google Cloud Run/GKE Sandbox), the default answer for "run untrusted container workloads" independent of AI use cases.
  SOURCE: https://github.com/google/gvisor

- FINDING: **kata-containers/kata-containers** — lightweight-VM-backed container runtime giving VM-grade isolation with container-like UX; CNCF project. Apache-2.0, 8,741 stars, last push 2026-09-17 (today). Maturity: production, CNCF-graduated-tier community governance — the VM-isolation alternative to gVisor's user-space-kernel approach.
  SOURCE: https://github.com/kata-containers/kata-containers

- FINDING: **vndee/llm-sandbox** — "Lightweight and portable LLM sandbox runtime (code interpreter) Python library," wraps Docker/Kubernetes/subprocess backends behind one API for agent code-interpreter tool calls. MIT, 1,121 stars, last push 2026-09-14 (3 days ago). Maturity: active but single-maintainer (personal GitHub account, not an org) — treat as a convenience wrapper library, not an enterprise-governed project; the underlying isolation guarantee is only as strong as whichever backend (Docker vs gVisor vs Kata) it's configured to use.
  SOURCE: https://github.com/vndee/llm-sandbox

- FINDING: **Azure-Samples/container-apps-dynamic-sessions-samples** — official Microsoft samples for Azure Container Apps' managed "dynamic sessions" code-interpreter sandbox (per-session Hyper-V isolation, sub-second cold start, managed by Azure rather than self-hosted). MIT, 26 stars, last push 2026-09-10 (7 days ago) — actively maintained despite the low star count (a managed-service sample, not a framework). Maturity: production (backs a GA Azure service), but scope is narrow (Python/code-interpreter templates only).
  SOURCE: https://github.com/Azure-Samples/container-apps-dynamic-sessions-samples

### 6. Policy engines applied to agents/tools

- FINDING: **open-policy-agent/opa** — general-purpose policy engine (Rego), CNCF-graduated. Apache-2.0, 12,244 stars, last push 2026-09-17 (today). No agent/MCP-specific OPA distribution or bundle was found as a maintained, notable repo — teams embedding OPA in agent tool-call authorization are doing so generically (OPA as a sidecar/library), not via a published agent-specific integration.
  SOURCE: https://github.com/open-policy-agent/opa

- FINDING: **cedar-policy/cedar** — AWS-originated policy language/engine (used by AWS Verified Permissions), designed for fine-grained, auditable authorization. Apache-2.0, 1,737 stars, last push 2026-09-16 (yesterday). Same gap as OPA: no notable, actively-maintained "Cedar for AI agents" reference repo found (searches for AWS-samples "verified permissions agent" integrations returned nothing with adoption signal as of this report).
  SOURCE: https://github.com/cedar-policy/cedar

- FINDING: The closest thing to "agent-native" policy today lives **inside the gateways, not as a separate policy engine**: agentgateway's `mcpAuthorization` block uses CEL expressions evaluated per tool-call (`mcp.tool.name`, `jwt.sub`, `jwt.<custom-claim>`) — see Code section below. IBM mcp-context-forge exposes a `plugins/` framework for the same purpose. Neither is OPA/Cedar-compatible; there is no cross-gateway standard policy language for MCP tool authorization as of 2026-09-17.
  SOURCE: https://github.com/agentgateway/agentgateway/blob/d376b9e1e3e254f1da5016033c60ec9dcba3bc98/examples/mcp-authorization/config.yaml

- FINDING: **NVIDIA-NeMo/Guardrails** (formerly NVIDIA/NeMo-Guardrails, org migrated to NVIDIA-NeMo) — "open-source toolkit for easily adding programmable guardrails to LLM-based conversational systems," "other" license (check terms), 7,155 stars, last push 2026-09-17 (today). Maturity: active, the most established dedicated LLM/agent guardrails project, though conversational-flow-centric rather than a general tool-call authorization engine.
  SOURCE: https://github.com/NVIDIA-NeMo/Guardrails

- FINDING: **openai/openai-guardrails-python** — OpenAI's own guardrails SDK. MIT, 248 stars, last push 2026-09-14 (3 days ago). Maturity: young/beta relative to NeMo Guardrails (far fewer stars, narrower scope), OpenAI-model-oriented.
  SOURCE: https://github.com/openai/openai-guardrails-python

- FINDING: No standalone "Microsoft agent governance toolkit" repo was found; `microsoft/azure-trust-agents` (84 stars, last push 2026-04-01, ~5.5 months stale) is a hackathon/workshop repo for building multi-agent *financial compliance workflows* with Microsoft Agent Framework — illustrates a governance *pattern*, not a reusable governance *toolkit*.
  SOURCE: https://github.com/microsoft/azure-trust-agents

### 7. A2A protocol reference repos

- FINDING: **a2aproject/A2A** — the Agent2Agent protocol specification itself, "opaque agentic applications" interoperability, governed under a `GOVERNANCE.md`/`MAINTAINERS.md` multi-org model (Google-originated, now broader community/Linux-Foundation-style governance). Apache-2.0, 25,813 stars, last push 2026-09-16 (yesterday). Maturity: production-track spec, the most-starred repo in this entire research set.
  SOURCE: https://github.com/a2aproject/A2A

- FINDING: **a2aproject/a2a-python** — official Python SDK for A2A. Apache-2.0, 2,145 stars, last push 2026-09-17 (today).
  SOURCE: https://github.com/a2aproject/a2a-python

- FINDING: **a2aproject/a2a-samples** — multi-language sample agents (Python, .NET) implementing agent cards and A2A auth flows, including a `headless_agent_auth` sample and an `a2a_mcp` sample bridging A2A and MCP. Apache-2.0, 1,769 stars, last push 2026-09-09 (8 days ago).
  SOURCE: https://github.com/a2aproject/a2a-samples

- FINDING: agentgateway ships first-class A2A support (`traffic-a2a`, `mcp-a2a-agents`-style examples) and Azure-Samples/AI-Gateway has an `mcp-a2a-agents` lab — both gateways treat A2A agent-card discovery and MCP tool routing as the same authorization surface, reinforcing that enterprise controls should be designed to cover both protocols under one policy layer rather than bolting on A2A separately.
  SOURCE: https://github.com/agentgateway/agentgateway/tree/main/examples/traffic-a2a
  SOURCE: https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/mcp-a2a-agents

## Code / Config

Per-tool authorization using CEL expressions against JWT claims, from agentgateway's official example (the pattern closest to a de-facto standard for MCP tool-call authorization at the gateway layer):

```yaml
# yaml-language-server: $schema=https://agentgateway.dev/schema/config
mcp:
  port: 3000
  policies:
    cors:
      allowOrigins:
      - "*"
      allowHeaders:
      - "*"
      exposeHeaders:
      - "Mcp-Session-Id"
    backendAuth:
      passthrough: {}
    jwtAuth:
      issuer: agentgateway.dev
      audiences: [test.agentgateway.dev]
      jwks:
        # Relative to the folder the binary runs from, not the config file
        file: ./manifests/jwt/pub-key
    mcpAuthorization:
      rules:
      # Allow anyone to call 'echo'
      - 'mcp.tool.name == "echo"'
      # Only the test-user can call 'get-sum'
      - 'jwt.sub == "test-user" && mcp.tool.name == "get-sum"'
      # Any authenticated user with the claim `nested.key == value` can access 'get-env'
      - 'mcp.tool.name == "get-env" && jwt.nested.key == "value"'
  targets:
  - name: mcp2
    mcp:
      host: http://localhost:3001/mcp
```
SOURCE: https://github.com/agentgateway/agentgateway/blob/d376b9e1e3e254f1da5016033c60ec9dcba3bc98/examples/mcp-authorization/config.yaml

## Caveats / Gaps

- **PyRIT link rot**: `Azure/PyRIT` is archived; anything citing that URL should be repointed to `microsoft/PyRIT`. This is a real trap because the archived repo still renders normally and doesn't obviously announce the move.
- **mcp-scan rebrand**: Invariant Labs' `mcp-scan` no longer exists under that name/org — it is `snyk/agent-scan` post-acquisition. Both the v0.5.x and v0.6+ output formats are explicitly marked experimental by the maintainers themselves; do not build CI gates on specific field names.
- **Scanning executes untrusted code**: Snyk Agent Scan's own README warns that scanning a stdio MCP config *starts the server process*, i.e., the scanner itself needs to run inside a sandbox — this is a control requirement to document in the MCP servers best-practices doc, not just a scanner footnote.
- **Azure-Samples fragmentation**: There are at least three overlapping-but-different Azure-Samples repos for "MCP + APIM/registry" (`remote-mcp-apim-functions-python`, `mcp-registry`, `mcp-auth-servers`) that are all stale (6–13 months) relative to the actively-maintained `Azure-Samples/AI-Gateway` labs collection, which covers the same ground with current bicep/SDK versions. Point readers at AI-Gateway first; treat the standalone repos as historical/narrower.
- **No agent-native policy DSL**: OPA and Cedar are both general-purpose and neither has a notable, actively-maintained "for AI agents/MCP" integration repo. What exists instead is policy logic embedded directly in gateway config (agentgateway's CEL rules, IBM mcp-context-forge's plugin framework) — these are gateway-specific, not portable across vendors. This is a real gap worth calling out explicitly in the best-practices doc rather than implying OPA/Cedar are drop-in solutions.
- **License note**: `modelcontextprotocol/servers`, `modelcontextprotocol/registry`, and `modelcontextprotocol/typescript-sdk` all report license `"other"` (not a standard SPDX MIT/Apache) via the GitHub API — verify the actual LICENSE file terms before enterprise redistribution rather than assuming permissive OSS terms. NVIDIA-NeMo/Guardrails also reports `"other"`.
- **Single-maintainer risk**: `vndee/llm-sandbox` is a personal-account project, not an org-backed one — fine for prototyping, but don't present it as an "enterprise" sandbox choice on par with gVisor/Kata/E2B without flagging the bus-factor difference.
- **Keycloak/Auth0/Okta MCP samples are not enterprise-grade**: every `keycloak-mcp*` repo found is a low-star (0–47), single-author project; none carries organizational backing. If the best-practices doc needs a cross-app-access pointer, use agentgateway's `traffic-cross-app-access`/`traffic-oidc` examples instead, or Azure-Samples/AI-Gateway's Entra-based labs.
- **Star/activity counts are a snapshot at 2026-09-17T00:00:00+05:30** (queried live via `gh api`/`gh search`); several of the most relevant repos (agentgateway, IBM mcp-context-forge, modelcontextprotocol SDKs, promptfoo, garak, gvisor, kata, E2B, cedar) show commits on the day of this report — this is a genuinely fast-moving space and numbers will already be stale within weeks.

## Sources
- https://github.com/microsoft/mcp-gateway — MCP Gateway (Microsoft, K8s reverse proxy/control plane)
- https://github.com/docker/mcp-gateway — docker mcp CLI plugin / MCP Gateway
- https://github.com/agentgateway/agentgateway — Next Generation Agentic Proxy for AI Agents and MCP servers
- https://github.com/IBM/mcp-context-forge — AI Gateway, registry, and proxy for MCP/A2A/REST
- https://github.com/Azure-Samples/AI-Gateway — Labs for AI Models, MCP servers, and Agents with APIM
- https://github.com/kagent-dev/kagent — Cloud Native Agentic AI
- https://github.com/modelcontextprotocol/python-sdk — Official Python SDK for MCP
- https://github.com/modelcontextprotocol/typescript-sdk — Official TypeScript SDK for MCP
- https://github.com/Azure-Samples/mcp-auth-servers — Reference MCP auth servers
- https://github.com/Azure-Samples/remote-mcp-apim-functions-python — APIM as AI Gateway to Remote MCP servers
- https://github.com/Azure-Samples/AI-Gateway/blob/main/labs/mcp-prm-oauth/src/bicep/identity/mcp-entra-app.bicep — Entra app registration bicep for MCP
- https://github.com/modelcontextprotocol/registry — Community-driven MCP server registry service
- https://github.com/Azure-Samples/mcp-registry — MCP Registry Demo on Azure API Center
- https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/mcp-registry-apic — MCP Registry with API Center lab
- https://github.com/snyk/agent-scan — Snyk Agent Scan (formerly Invariant Labs mcp-scan)
- https://github.com/cisco-ai-defense/mcp-scanner — Cisco AI Defense MCP Scanner
- https://github.com/promptfoo/promptfoo — Prompt/agent/RAG red-teaming and eval framework
- https://github.com/NVIDIA/garak — LLM vulnerability scanner
- https://github.com/microsoft/PyRIT — Python Risk Identification Tool (current, live)
- https://github.com/Azure/PyRIT — PyRIT old location (archived, do not use)
- https://github.com/anthropics/sandbox-runtime — OS-level filesystem/network sandboxing for agent processes
- https://github.com/e2b-dev/E2B — Secure sandboxed environments for AI agents
- https://github.com/google/gvisor — Application Kernel for Containers
- https://github.com/kata-containers/kata-containers — Lightweight VM-isolated container runtime
- https://github.com/vndee/llm-sandbox — Portable LLM sandbox runtime (code interpreter) library
- https://github.com/Azure-Samples/container-apps-dynamic-sessions-samples — Azure Container Apps dynamic sessions samples
- https://github.com/open-policy-agent/opa — Open Policy Agent
- https://github.com/cedar-policy/cedar — Cedar Policy Language
- https://github.com/agentgateway/agentgateway/blob/d376b9e1e3e254f1da5016033c60ec9dcba3bc98/examples/mcp-authorization/config.yaml — CEL-based MCP tool authorization example
- https://github.com/NVIDIA-NeMo/Guardrails — NeMo Guardrails toolkit
- https://github.com/openai/openai-guardrails-python — OpenAI Guardrails Python SDK
- https://github.com/microsoft/azure-trust-agents — Multi-agent financial compliance workflow workshop
- https://github.com/a2aproject/A2A — Agent2Agent protocol specification
- https://github.com/a2aproject/a2a-python — Official Python SDK for A2A
- https://github.com/a2aproject/a2a-samples — A2A sample agents (Python, .NET)
- https://github.com/agentgateway/agentgateway/tree/main/examples/traffic-a2a — agentgateway A2A traffic example
- https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/mcp-a2a-agents — MCP+A2A agents lab

## Control -> Project -> Maintainer -> Maturity -> URL

| Control | Project | Maintainer | Maturity | URL |
|---|---|---|---|---|
| MCP gateway (K8s-native) | mcp-gateway | Microsoft (org) | Beta | https://github.com/microsoft/mcp-gateway |
| MCP/agent gateway | agentgateway | agentgateway org (Solo.io-driven, community) | Production-track | https://github.com/agentgateway/agentgateway |
| MCP gateway (Docker Desktop) | mcp-gateway | Docker (org) | Beta | https://github.com/docker/mcp-gateway |
| MCP/A2A gateway + registry + plugins | mcp-context-forge | IBM (org) | Production-track, most feature-complete | https://github.com/IBM/mcp-context-forge |
| APIM + Entra + MCP registry labs | AI-Gateway | Azure-Samples (Microsoft) | Reference/lab, actively updated | https://github.com/Azure-Samples/AI-Gateway |
| MCP auth (spec-level) | python-sdk / typescript-sdk | modelcontextprotocol org | Production (spec reference) | https://github.com/modelcontextprotocol/python-sdk |
| MCP auth (APIM-specific, narrow) | remote-mcp-apim-functions-python | Azure-Samples | Stale/superseded | https://github.com/Azure-Samples/remote-mcp-apim-functions-python |
| MCP registry (official) | registry | modelcontextprotocol org | Active | https://github.com/modelcontextprotocol/registry |
| MCP registry (API Center pattern) | mcp-registry-apic (lab) | Azure-Samples | Reference, active | https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/mcp-registry-apic |
| MCP/agent security scanner | agent-scan (was mcp-scan) | Snyk (acquired Invariant Labs) | Active, output explicitly experimental | https://github.com/snyk/agent-scan |
| MCP security scanner | mcp-scanner | Cisco AI Defense | Active, ties to paid backend for full features | https://github.com/cisco-ai-defense/mcp-scanner |
| Agent/LLM red-teaming | promptfoo | promptfoo (org) | Production | https://github.com/promptfoo/promptfoo |
| LLM vulnerability scanning | garak | NVIDIA | Active | https://github.com/NVIDIA/garak |
| AI red-team framework | PyRIT | Microsoft | Active (old Azure/PyRIT path is archived — dead) | https://github.com/microsoft/PyRIT |
| Code sandbox (OS-level) | sandbox-runtime | Anthropic | Active | https://github.com/anthropics/sandbox-runtime |
| Code sandbox (microVM, agent-native) | E2B | e2b-dev | Production | https://github.com/e2b-dev/E2B |
| Container isolation kernel | gVisor | Google | Production | https://github.com/google/gvisor |
| VM-isolated containers | Kata Containers | CNCF/kata-containers | Production | https://github.com/kata-containers/kata-containers |
| Code interpreter wrapper lib | llm-sandbox | Single maintainer (vndee) | Active but bus-factor-1 | https://github.com/vndee/llm-sandbox |
| Managed code-interpreter sandbox | container-apps-dynamic-sessions-samples | Azure-Samples | Production (backs GA Azure service) | https://github.com/Azure-Samples/container-apps-dynamic-sessions-samples |
| General policy engine | OPA | CNCF/open-policy-agent | Production (not agent-native) | https://github.com/open-policy-agent/opa |
| General policy engine | Cedar | AWS/cedar-policy | Production (not agent-native) | https://github.com/cedar-policy/cedar |
| Tool-call authorization (gateway-embedded) | agentgateway CEL rules | agentgateway org | Active, vendor-specific | https://github.com/agentgateway/agentgateway/blob/d376b9e1e3e254f1da5016033c60ec9dcba3bc98/examples/mcp-authorization/config.yaml |
| Conversational guardrails | NeMo Guardrails | NVIDIA-NeMo | Active, most established | https://github.com/NVIDIA-NeMo/Guardrails |
| Guardrails SDK | openai-guardrails-python | OpenAI | Beta/young | https://github.com/openai/openai-guardrails-python |
| Agent governance pattern (not a toolkit) | azure-trust-agents | Microsoft | Workshop-grade, stale (5.5mo) | https://github.com/microsoft/azure-trust-agents |
| A2A protocol spec | A2A | a2aproject | Production-track | https://github.com/a2aproject/A2A |
| A2A Python SDK | a2a-python | a2aproject | Active | https://github.com/a2aproject/a2a-python |
| A2A sample agents/auth | a2a-samples | a2aproject | Active | https://github.com/a2aproject/a2a-samples |
