# Official Docs Research: Containing Agents — Code Execution Sandboxing and Runtime Guardrails
SOURCE_TYPE: official-docs
CONFIDENCE: HIGH
GENERATED: 2026-09-17T00:00:00+05:30

## Summary
Every major vendor now ships a layered containment model for agent code execution: OS-level process sandboxes (Seatbelt/bubblewrap/seccomp/Landlock) for developer-machine agents, and hardware-virtualized isolation (Firecracker microVMs, Hyper-V, Kata/gVisor) for cloud-hosted untrusted code execution. The consistent pattern across Anthropic, OpenAI, AWS, Microsoft, and Google is: default-deny network egress with explicit allowlists, credentials brokered/proxy-injected rather than placed inside the sandbox, ephemeral per-session environments that are destroyed and memory-sanitized after use, and metadata-endpoint protections (IMDS/MMDS) treated as a first-class threat. Runtime controls that do not rely on the model itself — deny/allow rule layers evaluated before any classifier, policy engines (Cedar in AWS Bedrock AgentCore), and two-stage classifiers (Anthropic's auto-mode classifier) — are now documented as necessary because human approval alone degrades under volume ("approval fatigue"/"confirmation fatigue" is documented in both industry blogs and arXiv research, and Anthropic's own published numbers show users approve ~93% of prompts). Observability is converging on OpenTelemetry's GenAI semantic conventions (`invoke_agent`, `execute_tool` spans), still in experimental/development status. Red-teaming tooling (Microsoft PyRIT/AI Red Teaming Agent, NVIDIA garak, promptfoo) and agent-lifecycle governance (Microsoft Entra Agent ID/Agent 365, AWS agent registries, Google Cloud API Registry/Agent Registry) are documented but several pieces (Agent 365, Cloud API Registry, AgentCore Policy Dogwood temporal policies) are explicitly preview-stage as of this research date.

## Key Findings

### 1. Isolation tiers

- FINDING: Anthropic's Claude Code sandbox is an OS-level, non-container sandbox: Seatbelt (`sandbox-exec`) on macOS, bubblewrap (bwrap) + Landlock/seccomp-style filtering on Linux/WSL2. It is built into Claude Code (no separate install needed on macOS); on Linux it needs bubblewrap + optional seccomp filter packages, discoverable via `/sandbox`.
  SOURCE: https://code.claude.com/docs/en/sandboxing
- FINDING: The underlying engine is open-sourced as `@anthropic-ai/sandbox-runtime` (npm) / `anthropic-experimental/sandbox-runtime` (GitHub) — "a lightweight sandboxing tool for enforcing filesystem and network restrictions on arbitrary processes at the OS level, without requiring a container."
  SOURCE: https://github.com/anthropic-experimental/sandbox-runtime
- FINDING: Anthropic runs three distinct containment tiers across its products: claude.ai uses a gVisor container on isolated infrastructure with an ephemeral per-session filesystem and no local code execution; Claude Code uses the OS-level sandbox described above (reads allowed, writes allowed only in-workspace, network denied by default); Claude Cowork uses full VM isolation via platform hypervisors (Apple Virtualization on macOS, HCS on Windows).
  SOURCE: https://www.anthropic.com/engineering/how-we-contain-claude
- FINDING: Moving Claude Code from per-action approval to sandboxed execution produced "an 84% reduction in permission prompts," and Anthropic states the sandbox boundary is auditable because the runtime is open source.
  SOURCE: https://www.anthropic.com/engineering/how-we-contain-claude
- FINDING: OpenAI Codex sandboxes every command from the start, with constraints propagating to the full descendant process tree. It translates a `SandboxPolicy` into OS-native primitives: Seatbelt (`sandbox-exec`, deny-by-default) on macOS; a dedicated `codex-linux-sandbox` helper combining Bubblewrap (filesystem namespace isolation) + Landlock (filesystem access control) + seccomp (syscall/network filtering) on Linux; Restricted Tokens/ACLs on Windows. Codex Cloud runs in isolated OpenAI-managed containers, "preventing access to your host system or unrelated data."
  SOURCE: https://github.com/openai/codex/blob/main/docs/sandbox.md
- FINDING: Codex exposes three sandbox modes — Read-Only, Workspace-Write (default: read/edit/run inside the workspace, approval required for out-of-workspace or network actions), and Full-Access (bypasses sandboxing; requires `--dangerously-bypass-approvals-and-sandbox` and is explicitly "not recommended"). Approval policies are On-Request, Never, or a granular per-category mix; the older `untrusted` policy is deprecated in favor of `on-request`.
  SOURCE: https://learn.chatgpt.com/docs/agent-approvals-security
- FINDING: Azure Container Apps dynamic sessions run each code-interpreter/custom-container session inside its own Hyper-V isolation boundary, described as ensuring "complete isolation from other sessions and resources," with optional network controls; sessions are ephemeral (drawn from prewarmed session pools, auto-deprovisioned after use or a configurable cooldown).
  SOURCE: https://learn.microsoft.com/en-us/azure/container-apps/sessions
- FINDING: AKS Pod Sandboxing is built on the open-source Kata Containers project running on the Azure Linux container host; it provides VM-based isolation and a separate kernel per pod via `runtimeClassName: kata-vm-isolation`, using Microsoft's Hyper-V hypervisor and the open-source Cloud-Hypervisor VMM. Requires Kubernetes 1.27+; documented limitations include no Kata host-network access and reduced IOPS vs. `runc` on Azure Files/local SSD. Microsoft Defender for Containers does not assess Kata-runtime pods.
  SOURCE: https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing
- FINDING: AKS Confidential Containers (preview) build on Kata Confidential Containers plus hardware memory encryption: each pod runs in a dedicated "child VM" with its own AMD SEV-SNP memory-encryption key, on specific Azure confidential-computing (ACC) VM sizes.
  SOURCE: https://learn.microsoft.com/en-us/azure/aks/confidential-containers-overview
- FINDING: Google Cloud Run uses a dedicated gVisor sandbox to run user code; gVisor intercepts application syscalls and acts as a guest kernel, giving each sandboxed application its own kernel and virtualized devices distinct from the host and other sandboxes. Google Cloud Run sandboxes (a separate, newer capability layered for AI/agent workloads) are documented as public preview.
  SOURCE: https://gvisor.dev/ ; https://cloud.google.com/blog/topics/developers-practitioners/google-cloud-run-sandboxes-are-in-public-preview/
- FINDING: Google Cloud Run sandboxes "do not have access to the Cloud Run service's environment variables nor... the ability to call the Google Cloud metadata server," and have zero outbound network access by default — egress must be explicitly enabled via `--allow-egress`.
  SOURCE: https://docs.cloud.google.com/run/docs/securing/security
- FINDING: GKE Sandbox (gVisor) and Agent Sandbox on GKE isolate AI code-execution workloads; the default GKE network policy blocks access to the Google Cloud metadata server (169.254.169.254).
  SOURCE: https://docs.cloud.google.com/kubernetes-engine/docs/concepts/sandbox-pods ; https://docs.cloud.google.com/kubernetes-engine/docs/how-to/agent-sandbox
- FINDING: AWS Bedrock AgentCore Runtime implements a strict one-session-one-microVM model on Firecracker: each user session gets a dedicated microVM with isolated CPU, memory, and filesystem; the microVM is terminated and its memory sanitized after the session ends, eliminating cross-session contamination.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- FINDING: E2B's proprietary runtime is built on Firecracker microVMs, achieving sub-200ms sandbox startup; each sandbox runs in its own cgroup and network namespace with a per-sandbox nftables egress firewall and SNI/Host-inspecting domain allow/deny lists. The runtime (`e2b-dev/runtime`) is Apache-2.0 and self-hostable.
  SOURCE: https://github.com/e2b-dev/runtime
- FINDING: Comparative defenses by isolation tier (synthesized from the above official sources, not a single vendor statement): process sandboxes (Seatbelt/bubblewrap/Landlock/seccomp) constrain syscalls and filesystem/network reachability within a shared kernel — they defend against accidental scope escalation and casual data exfiltration but do not provide kernel-level isolation from a determined sandbox-escape exploit; gVisor intercepts syscalls in userspace to shrink host kernel attack surface without a full VM; Kata Containers/Confidential Containers and Firecracker microVMs (AgentCore Runtime, E2B) give each workload its own kernel/hardware-virtualized boundary, defending against kernel exploits and cross-tenant escape; Hyper-V isolation (Azure Container Apps dynamic sessions) is Microsoft's equivalent VM-per-session boundary for its managed offering.
  SOURCE: https://gvisor.dev/ ; https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html ; https://learn.microsoft.com/en-us/azure/container-apps/sessions

### 2. Sandbox policy essentials

- FINDING: Anthropic's sandbox-runtime enforces default-deny network: "By default, all network access is denied. You must explicitly allow domains," configured via `network.allowedDomains` / `network.deniedDomains` (with optional port suffixes). All traffic is routed through host-side HTTP/SOCKS5 proxies; on Linux the sandbox's network namespace is removed entirely so all traffic must transit the proxy over a Unix domain socket.
  SOURCE: https://github.com/anthropic-experimental/sandbox-runtime
- FINDING: Filesystem policy is asymmetric by design: read access is allow-by-default with explicit deny/re-allow lists (`filesystem.denyRead`/`filesystem.allowRead`), while write access is deny-by-default (`filesystem.allowWrite`/`filesystem.denyWrite`, with `denyWrite` taking precedence inside allowed zones). A mandatory deny-list auto-protects shell configs (`.bashrc`, `.zshrc`), git internals (`.gitconfig`, `.git/hooks/`), and IDE directories (`.vscode/`, `.idea/`).
  SOURCE: https://github.com/anthropic-experimental/sandbox-runtime
- FINDING: Claude Cowork's credential model keeps secrets out of the sandboxed VM: "credentials stay in the host keychain, the VM gets a per-session scoped-down token, and that token can be revoked independently of the user's." API calls are intercepted by a man-in-the-middle proxy inside the VM that only forwards requests carrying the VM's own provisioned session token, rejecting an attacker-embedded key.
  SOURCE: https://www.anthropic.com/engineering/how-we-contain-claude
- FINDING: AWS Bedrock AgentCore Runtime explicitly documents metadata-endpoint credential exposure as a risk to manage, not eliminate: "Any code or actor running inside the microVM can access execution role credentials by calling the metadata endpoint (MMDS)," so execution-role permissions must be scoped tightly (least privilege) since anything inside the sandbox can reach them.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- FINDING: AWS requires MMDSv2 (the microVM metadata-service token-based protocol) on AgentCore Runtime starting **June 30, 2026** — runtimes without MMDSv2 enabled cannot be invoked and return a `ValidationException`; enable via `UpdateAgentRuntime` with `requireMMDSV2: true` in `metadataConfiguration`. This mirrors EC2's IMDSv2 hardening (token-required PUT/GET, configurable hop limit — AWS recommends a hop limit of 2–3 in container environments to avoid IMDSv1 fallback).
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html ; https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html
- FINDING: AgentCore recommends AgentCore Identity to broker outbound OAuth credentials and API keys, "preventing credential exposure in agent code or logs," and separating user-delegated (Authorization Code Grant) from autonomous (Client Credentials Grant) credential paths.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- FINDING: AgentCore Runtime enforces header limits (4KB/header value, 20 headers per runtime) and requires TLS 1.2+ (recommends TLS 1.3) for all traffic; `InvokeAgentRuntimeCommandShell` is WSS-only, plaintext `ws://` is unsupported. It recommends running custom containers as non-root and setting command timeouts "to prevent resource waste from runaway processes."
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- FINDING: Google Cloud Run sandboxes default to zero outbound network access, require explicit `--allow-egress`, and are documented as unable to reach the Cloud Run service's own environment variables or the Cloud metadata server.
  SOURCE: https://docs.cloud.google.com/run/docs/securing/security
- FINDING: Azure Container Apps dynamic sessions are "designed to run untrusted code in isolated environments" and are managed-lifecycle: "Sessions are automatically deprovisioned after use or after a configurable cooldown period."
  SOURCE: https://learn.microsoft.com/en-us/azure/container-apps/sessions
- CAVEAT/GAP: None of the vendor docs reviewed state an explicit, universal "output size limit" policy for sandboxed tool/command output; this appears to be left to the calling application/agent framework rather than the sandbox layer itself.

### 3. Runtime controls that do not rely on the model

- FINDING: Claude Code's permission system runs two rule layers *before* any model-based classifier is consulted: `permissions.deny` rules block outright ("neither the classifier nor your stated intent can override them"), and `permissions.ask` rules force a prompt. Only after these hard rules does auto mode route the action through a separate classifier model.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode
- FINDING: The Claude Code auto-mode classifier is a two-stage pipeline: Stage 1 is "a fast single-token filter (deciding 'yes' to block or 'no' to allow)"; Stage 2 applies chain-of-thought reasoning only if Stage 1 flags the action — reducing false-positive rate from 8.5% to 0.4% on real traffic while catching scope escalation, credential exploration, agent-inferred high-stakes parameters, data exfiltration, and safety-check bypass ("overeager behavior"). The classifier is deliberately shown only user messages and the agent's tool calls — not the agent's own reasoning or tool outputs — "to prevent agents from generating persuasive rationalizations and reduce prompt-injection vulnerabilities." Anthropic publishes the honest failure rate: 17% false-negative rate on real "overeager" actions.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode
- FINDING: A companion input-layer defense — a server-side prompt-injection probe — scans tool outputs before the agent reads them; suspicious content triggers a warning added to the agent's context rather than a hard block.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode
- FINDING: Anthropic's own baseline metric motivating auto mode: users "approve 93% of permission prompts" under manual approval, which the design explicitly frames as evidence that per-action approval alone is not a reliable control.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode
- FINDING: When the classifier blocks, Claude Code does not halt the session — it treats a block as "a single retry where the agent gets a nudge, reconsiders, and usually finds an alternative path"; only after 3 consecutive denials or 20 total denials in a run does it escalate to human review, an explicit design choice to avoid overwhelming humans with routine blocks while still gating on persistent anomalies.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode
- FINDING: OpenAI Codex layers "automatic review agents" over the sandbox/approval system that evaluate actions for "data exfiltration, credential probing, persistent security weakening, and destructive actions"; high-risk actions require user authorization, critical-risk actions are denied automatically rather than escalated.
  SOURCE: https://learn.chatgpt.com/docs/agent-approvals-security
- FINDING: AWS Bedrock AgentCore Policy uses Cedar — "an open-source policy language developed by AWS for writing and enforcing authorization policies" that recently joined the CNCF — to gate every tool invocation through an AgentCore Gateway. The policy engine "enforces default-deny and forbid-wins semantics automatically": every Cedar policy specifies principal (who), action (tool), resource (gateway), and optional conditions; forbid policies always override permit policies.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- FINDING: AgentCore also supports "Dogwood," an open-source policy language that is a strict superset of Cedar (every valid Cedar policy is valid Dogwood), adding *temporal* policies — conditions that depend on prior events in the same session (e.g., "requiring a prior approval, limiting how often an action runs, or keeping a running total under a threshold") evaluated against a "policy session" grouped by an `x-amzn-bedrock-agentcore-policy-session-id` header. Guardrails (content-filter/prompt-attack/sensitive-info scoring) can be consulted inline as "information providers" within a Dogwood policy.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- FINDING: AgentCore's Cedar schema is auto-generated from the Gateway's tool definitions (mapping each tool to a Cedar action), validated at policy-creation time, and can be authored from natural language via a "policy authoring service" that generates, validates, and runs automated-reasoning analysis on the resulting Cedar code to catch always-allow/always-deny policies before deployment.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- FINDING: AgentCore Runtime security best practices explicitly recommend command-execution timeouts, non-root containers, least-privilege IAM scoped to specific runtime ARNs (no wildcards), explicit `Deny` statements for `InvokeAgentRuntimeForUser`/`GetWorkloadAccessTokenForUserId` where user-id delegation isn't needed, and confused-deputy prevention via `aws:SourceArn`/`aws:SourceAccount` conditions on execution-role trust policies.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- FINDING: "Approval fatigue" is a named, documented phenomenon: "Approval fatigue is when an AI agent sends so many approval requests that the human starts approving without real review. The control still exists on paper but stops working in practice." Researchers propose a three-stage evaluation — DENY rules (unconditional block), ALLOW rules (auto-approve low-risk), HUMAN gate (residual only) — as the alternative to blanket approval, mirroring the Claude Code deny/ask/classifier layering above.
  SOURCE: https://workos.com/blog/approval-fatigue-agent-governance
- FINDING: Peer-reviewed research on this same dynamic ("Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human") formalizes human oversight as a finite, fatiguing resource and argues guard/approval systems must be calibrated to reviewer capacity, not assumed infinite.
  SOURCE: https://arxiv.org/html/2606.08919
- CAVEAT/GAP: Microsoft's direct equivalent to Cedar-based policy engines for agent tool authorization (an OPA/Cedar-style engine specifically for Copilot Studio/Foundry agent actions) was not found as a named, GA product in this research pass — Microsoft's governance story centers on Entra Agent ID / Purview / Defender for Cloud rather than a published policy-language engine; treat this as a gap to verify directly with Microsoft Foundry docs before publishing a MUST claim.

### 4. Observability and audit for agents

- FINDING: OpenTelemetry's GenAI semantic conventions define span, metric, and event schemas for the "four pillars of agent execution: Orchestration, LLM, Tool, and Memory," with a span tree of a top-level `invoke_agent` span containing child `chat`/LLM-call spans and `execute_tool` spans per tool invocation.
  SOURCE: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md
- FINDING: Exact span definitions (as of the current spec revision): `create_agent {gen_ai.agent.name}` (operation `create_agent`) and `invoke_agent {gen_ai.agent.name}` (operation `invoke_agent`) are both CLIENT-kind spans, status **Development** (experimental) — required attributes include `gen_ai.operation.name` and `gen_ai.provider.name`; conditionally required attributes include `gen_ai.agent.name`, `gen_ai.agent.id`, `gen_ai.agent.version`, `gen_ai.conversation.id`; recommended attributes include `gen_ai.usage.input_tokens`/`gen_ai.usage.output_tokens`. Tool calls use operation name `execute_tool`.
  SOURCE: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md
- FINDING: The OpenTelemetry project itself states the GenAI conventions are under active, rapid revision ("Every release from v1.37 to v1.41 has touched GenAI conventions"), reinforcing that these are not yet a stable/GA spec.
  SOURCE: https://opentelemetry.io/blog/2026/genai-observability/
- FINDING: AWS Bedrock AgentCore's documented audit trail: enable CloudTrail for API-level audit (records `InvokeAgentRuntime`, `InvokeAgentRuntimeCommand`, `InvokeAgentRuntimeCommandShell`, plus control-plane ops, each with caller identity, timestamp, source IP, response status); use CloudWatch Logs for command-level audit (request ID + input command sent to the agent's log group); correlate CloudTrail (who called) with CloudWatch Logs (what command ran) via request ID; log the relationship between the authenticated IAM principal and any `X-Amzn-Bedrock-AgentCore-Runtime-User-Id` delegation value; enable VPC Flow Logs for network-level audit.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- CAVEAT/GAP: No vendor doc reviewed specified a concrete field-level redaction policy (e.g., "always redact these attribute keys") for GenAI telemetry; this is left to the implementer. Treat redaction guidance in the best-practices doc as a SHOULD synthesized from general logging hygiene, not a specific vendor mandate.

### 5. Evaluation and release gating for agents

- FINDING: Microsoft's AI Red Teaming Agent (Azure AI Foundry / "Microsoft Foundry") "leverages Microsoft's open-source framework for Python Risk Identification Tool's (PyRIT) AI red teaming capabilities along with Microsoft Foundry's Risk and Safety Evaluations to help you automatically assess safety issues," running automated adversarial-probing scans, scoring each attack-response pair (e.g., Attack Success Rate), and producing a scorecard to inform go/no-go deployment decisions. Requires Python 3.10–3.13.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent
- FINDING: Microsoft documents both a local-run path (Azure AI Evaluation SDK) and a cloud-run path (Microsoft Foundry SDK) for the AI Red Teaming Agent.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent ; https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-ai-red-teaming-cloud
- FINDING: NVIDIA's garak is an open-source (Apache 2.0) LLM vulnerability scanner with 50+ probe modules covering prompt injection, jailbreaks, hallucination, toxicity, data leakage, encoding-based attacks, and package hallucination; it works against any LLM exposing an API (OpenAI, Hugging Face, AWS Bedrock, Cohere, Groq, Ollama, custom REST endpoints).
  SOURCE: https://github.com/NVIDIA/garak
- FINDING: promptfoo is an open-source CLI/library for evaluating and red-teaming LLM apps, with a dedicated agent red-teaming workflow: it ingests OpenTelemetry traces (LLM calls, guardrail decisions, tool executions, shell commands, reasoning steps, errors) and normalizes them into a time-ordered "agent trajectory" for vulnerability analysis, covering "50+ vulnerability types" across injection, jailbreaks, business logic, RAG, agents, and integrations.
  SOURCE: https://www.promptfoo.dev/docs/red-team/agents/
- CAVEAT/GAP: None of the official docs reviewed prescribe a specific "regression eval gate" threshold or CI-blocking policy for tool-use correctness pre-production; this is left to the adopting organization. Treat as a SHOULD, not a documented vendor MUST.

### 6. Agent lifecycle governance

- FINDING: Microsoft Entra Agent ID gives every AI agent a governed identity, with agent-specific Identity Governance features: agent sponsorship/ownership assignment after creation, lifecycle workflows to ensure "an agent doesn't have access to resources for longer than needed," and access-package-based resource assignment for both on-behalf-of (OBO) and autonomous agent scenarios.
  SOURCE: https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview
- FINDING: Microsoft Agent 365 is positioned as the broader control plane — inventory, observation, governance, and security for enterprise agent fleets — built on Entra Agent ID as the identity foundation.
  SOURCE: https://learn.microsoft.com/en-us/microsoft-agent-365/admin/capabilities-entra
- FINDING: Microsoft's Cloud Adoption Framework states the governance thesis directly: "Every agent must be observable, governed, and secure... Leaders must know which agents exist, who owns them, what they can access, and how to intervene when behavior falls outside policy," and recommends "a centralized agent governance layer to enforce consistent identity, ownership, access control, and continuous monitoring for all agents," with every agent recorded in a single organizational inventory tracking ownership, purpose, platform, and access scope.
  SOURCE: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- FINDING: Amazon Bedrock AgentCore's security best practices assign a shared-responsibility split for lifecycle-relevant concerns: AWS is responsible for microVM-level isolation, OS kernel patching, and network infrastructure security; the customer is responsible for agent code/dependency management, IAM policy scoping, session-to-user mapping enforcement, container image updates, and input validation — an explicit lifecycle/ownership boundary rather than a registry product per se.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- FINDING: Google Cloud's Agent Registry is described as "a centralized catalog for discovering, tracking, and managing all agents, tools, and MCP servers across the organization," with the related Cloud API Registry integration (in **Preview** as of December 18, 2025) letting administrators manage which tools/MCP servers are available to developers directly from the Vertex AI Agent Builder console.
  SOURCE: https://discuss.google.dev/t/tool-governance-in-vertex-ai-agent-builder-with-the-new-cloud-api-registry-integration/298148
- FINDING: Google states each agent registered on its platform "gets a verifiable identity through cryptographic IDs and is registered as an IAM Principal — creating a clear audit trail tied to defined access policies."
  SOURCE: https://docs.cloud.google.com/agent-builder/overview
- CAVEAT/GAP: Precise GA/preview status for Microsoft Agent 365 pricing/availability, and for AWS's own "Agent Registry" product (referenced in secondary coverage but not directly confirmed on a primary AWS URL in this pass), should be re-verified against docs.aws.amazon.com before citing a specific GA date in the final best-practices doc.

## Code / Config

Cedar policy default-deny / forbid-wins semantics (conceptual, from AWS docs — no single runnable snippet published on the core-concepts page):
```
# Cedar policy shape (AgentCore Policy)
permit(
  principal == AgentCore::OAuthUser::"user-id",
  action == AgentCore::Action::"toolName",
  resource == AgentCore::Gateway::"gateway-id"
) when { <conditions> };
# forbid policies always override permit policies; default is deny.
```
SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html

IAM deny for user-id delegation (verbatim from AWS docs):
```json
{
   "Statement": [
      {
         "Sid": "DenyUserIdDelegation",
         "Effect": "Deny",
         "Action": "bedrock-agentcore:InvokeAgentRuntimeForUser",
         "Resource": "arn:aws:bedrock-agentcore:REGION:ACCOUNT_ID:runtime/*"
      }
   ]
}
```
SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html

Confused-deputy trust policy condition (verbatim from AWS docs):
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "bedrock-agentcore.amazonaws.com" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": { "aws:SourceAccount": "123456789012" },
        "ArnLike": { "aws:SourceArn": "arn:aws:bedrock-agentcore:us-east-1:123456789012:*" }
      }
    }
  ]
}
```
SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html

AKS Kata VM-isolated pod spec (verbatim from Microsoft docs):
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: isolated-pod
spec:
  runtimeClassName: kata-vm-isolation
  containers:
  - name: kata
    image: mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11
    command: ["/bin/sh", "-ec", "while :; do echo '.'; sleep 5 ; done"]
```
SOURCE: https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing

AKS cluster creation with Pod Sandboxing (verbatim from Microsoft docs):
```azurecli
az aks create \
    --name myAKSCluster \
    --resource-group myResourceGroup \
    --os-sku AzureLinux \
    --workload-runtime KataVmIsolation \
    --node-vm-size Standard_D4s_v3 \
    --node-count 3 \
    --generate-ssh-keys
```
SOURCE: https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing

Codex sandbox network access opt-in (verbatim config key from OpenAI docs):
```
[sandbox_workspace_write]
network_access = true
```
SOURCE: https://learn.chatgpt.com/docs/agent-approvals-security

## Caveats / Gaps

- The OpenTelemetry GenAI semantic conventions are explicitly in "Development"/experimental status and under active revision release-to-release; do not present span/attribute names as a frozen contract in the best-practices doc — frame as "converging standard, verify current version before implementing."
- Microsoft does not appear (in this research pass) to publish a named Cedar/OPA-equivalent policy-engine product for agent tool authorization comparable to AWS Bedrock AgentCore Policy; Microsoft's governance emphasis is identity-centric (Entra Agent ID) rather than a declarative authorization-policy language. Verify directly with Microsoft Foundry/Copilot Studio docs before asserting a MUST that names a Microsoft product parity claim.
- AWS's Dogwood policy language (temporal policies, session-aware conditions, Guardrails-as-information-providers) is newer and its GA/preview status was not explicitly stated on the fetched page — verify current status before citing.
- Google Cloud Run "sandboxes" (the newer, AI-agent-oriented capability, distinct from the long-standing gVisor-based Cloud Run container runtime) were described in an official Google Cloud blog as "public preview" — reconfirm GA status before publishing.
- Microsoft Agent 365 GA date/pricing (~$15/user/month cited in secondary coverage) was not independently confirmed against a primary Microsoft Learn/pricing page in this pass; re-verify before citing a number.
- No official vendor doc reviewed specifies a concrete, universal sandbox output-size limit or a specific redaction field list for agent logs — these should be framed as SHOULD-level implementer guidance, not vendor-mandated specifics.
- "Approval fatigue" research cited (WorkOS blog, arXiv 2606.08919) is not vendor documentation but is included because the architect explicitly asked for evidence that blanket human approval degrades; treat these as MEDIUM-confidence supporting evidence rather than official product docs.

## Sources
- https://code.claude.com/docs/en/sandboxing — Configure the sandboxed Bash tool (Claude Code Docs)
- https://github.com/anthropic-experimental/sandbox-runtime — anthropics/sandbox-runtime (GitHub)
- https://www.anthropic.com/engineering/how-we-contain-claude — How we contain Claude across products (Anthropic Engineering)
- https://www.anthropic.com/engineering/claude-code-auto-mode — How we built Claude Code auto mode: a safer way to skip permissions (Anthropic Engineering)
- https://github.com/openai/codex/blob/main/docs/sandbox.md — codex/docs/sandbox.md (OpenAI GitHub)
- https://learn.chatgpt.com/docs/agent-approvals-security — Agent approvals & security (OpenAI/ChatGPT Learn)
- https://learn.microsoft.com/en-us/azure/container-apps/sessions — Dynamic sessions in Azure Container Apps (Microsoft Learn)
- https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing — Pod Sandboxing with Azure Kubernetes Service (AKS) (Microsoft Learn)
- https://learn.microsoft.com/en-us/azure/aks/confidential-containers-overview — Confidential Containers (preview) with AKS (Microsoft Learn)
- https://gvisor.dev/ — The Container Security Platform (gVisor)
- https://cloud.google.com/blog/topics/developers-practitioners/google-cloud-run-sandboxes-are-in-public-preview/ — Google Cloud Run sandboxes are in public preview (Google Cloud Blog)
- https://docs.cloud.google.com/run/docs/securing/security — Security design overview (Cloud Run docs)
- https://docs.cloud.google.com/kubernetes-engine/docs/concepts/sandbox-pods — GKE Sandbox (GKE security docs)
- https://docs.cloud.google.com/kubernetes-engine/docs/how-to/agent-sandbox — Isolate AI code execution with Agent Sandbox (GKE AI/ML docs)
- https://github.com/e2b-dev/runtime — e2b-dev/runtime (GitHub)
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html — Security best practices for AgentCore Runtime (AWS docs)
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html — Core concepts — Policy (Amazon Bedrock AgentCore docs)
- https://aws.amazon.com/blogs/security/why-policy-in-amazon-bedrock-agentcore-chose-cedar-for-securing-agentic-workflows/ — Why Policy in Amazon Bedrock AgentCore chose Cedar (AWS Security Blog)
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html — Use the Instance Metadata Service to access instance metadata (AWS EC2 docs)
- https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md — GenAI agent spans (OpenTelemetry semantic-conventions-genai)
- https://opentelemetry.io/blog/2026/genai-observability/ — Inside the LLM Call: GenAI Observability with OpenTelemetry (OpenTelemetry blog)
- https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent — AI Red Teaming Agent (Microsoft Foundry docs)
- https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent — Run AI Red Teaming Agent Locally (Microsoft Foundry docs)
- https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-ai-red-teaming-cloud — Run AI Red Teaming Agent in the cloud (Microsoft Foundry docs)
- https://github.com/NVIDIA/garak — garak: the LLM vulnerability scanner (NVIDIA GitHub)
- https://www.promptfoo.dev/docs/red-team/agents/ — How to red team LLM Agents (Promptfoo docs)
- https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview — Governing Agent Identities (Microsoft Entra ID Governance docs)
- https://learn.microsoft.com/en-us/microsoft-agent-365/admin/capabilities-entra — Protect agent identities with Microsoft Entra (Microsoft Agent 365 docs)
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization — Govern and secure AI agents across the organization (Cloud Adoption Framework)
- https://docs.cloud.google.com/agent-builder/overview — Agent Platform overview (Gemini Enterprise Agent Platform / Vertex AI Agent Builder docs)
- https://discuss.google.dev/t/tool-governance-in-vertex-ai-agent-builder-with-the-new-cloud-api-registry-integration/298148 — Tool governance in Vertex AI Agent Builder with Cloud API Registry integration (Google Developer forums, referencing official announcement)
- https://workos.com/blog/approval-fatigue-agent-governance — Approval fatigue is agent governance's next attack surface (WorkOS blog)
- https://arxiv.org/html/2606.08919 — Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human (arXiv)

## Implications for a best-practices doc

- MUST: Run any agent-executed, LLM-generated, or untrusted code inside an isolation boundary stronger than a bare process — at minimum an OS-level sandbox with default-deny network and filesystem write policy (Seatbelt/bubblewrap/Landlock class), and prefer VM-grade isolation (Firecracker microVM, Kata/Hyper-V, gVisor) for any multi-tenant or internet-facing execution path.
  SOURCE: https://code.claude.com/docs/en/sandboxing ; https://github.com/openai/codex/blob/main/docs/sandbox.md ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- MUST: Default network egress to deny-all; require an explicit allowlist per domain/host, and terminate egress through a proxy the sandbox cannot bypass (not a direct network namespace).
  SOURCE: https://github.com/anthropic-experimental/sandbox-runtime ; https://docs.cloud.google.com/run/docs/securing/security ; https://github.com/e2b-dev/runtime
- MUST: Never place long-lived or broadly-scoped credentials inside the sandboxed execution environment; broker credentials via a host-side proxy or identity service that injects a scoped, revocable, per-session token, and scope any execution-role/IAM permissions reachable via a metadata endpoint to least privilege because code inside the sandbox can always reach it.
  SOURCE: https://www.anthropic.com/engineering/how-we-contain-claude ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- MUST: Treat the cloud metadata/instance-metadata endpoint (IMDS/MMDS/GCE metadata server) as an explicit threat surface — require the token-based protocol version (IMDSv2/MMDSv2), constrain hop limits in containerized deployments, and block metadata-server reachability by default for sandboxed workloads.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html ; https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html ; https://docs.cloud.google.com/run/docs/securing/security
- MUST: Make execution environments ephemeral and per-session — destroy and sanitize memory/filesystem after each session rather than reusing a warm environment across trust boundaries (users, tenants, or tasks).
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html ; https://www.anthropic.com/engineering/how-we-contain-claude
- MUST: Enforce a deny/allow rule layer that runs before any model- or classifier-based decision, and make deny rules non-overridable by the model, by stated user intent, or by a classifier's judgment.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- SHOULD: Where a declarative, analyzable policy language is available (e.g., Cedar), prefer it over ad hoc if/else authorization logic for tool-invocation gating, and default the policy engine to deny with forbid-wins semantics.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- SHOULD NOT rely on blanket human approval-per-action as the primary control for a high-volume agent — design a tiered control (hard deny rules, auto-approved low-risk allowlist, and a classifier or policy engine for the middle tier) and reserve human approval for a small, well-defined set of irreversible/high-stakes actions, because published evidence shows human approval rates saturate near-total under volume (documented ~93% approval rate) and independent research formalizes human oversight as a finite, fatiguing resource.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode ; https://workos.com/blog/approval-fatigue-agent-governance ; https://arxiv.org/html/2606.08919
- SHOULD: When an automated classifier/reviewer blocks an action, prefer "recover and retry with a narrower action" over hard session termination, but escalate to a human after a bounded number of consecutive or total denials rather than looping indefinitely.
  SOURCE: https://www.anthropic.com/engineering/claude-code-auto-mode
- SHOULD: Instrument agents with OpenTelemetry GenAI semantic conventions (`invoke_agent`, `execute_tool` spans, `gen_ai.*` attributes) for cross-vendor traceability, while treating the spec as evolving/experimental and pinning a spec version rather than assuming stability.
  SOURCE: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md ; https://opentelemetry.io/blog/2026/genai-observability/
- SHOULD: Log, per tool call, the authenticated principal (and, if delegated, on-behalf-of-whom), the tool name/arguments, and the outcome, and correlate an API-level audit trail (e.g., CloudTrail-equivalent) with an execution-level log (e.g., CloudWatch-equivalent) via a shared request ID, to support forensic reconstruction.
  SOURCE: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- SHOULD: Run automated adversarial red-teaming (PyRIT/AI Red Teaming Agent, garak, or promptfoo) as a pre-production gate producing a quantitative scorecard (e.g., Attack Success Rate), not a one-time manual review.
  SOURCE: https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent ; https://github.com/NVIDIA/garak ; https://www.promptfoo.dev/docs/red-team/agents/
- MUST: Maintain a single organizational inventory of every agent recording owner, purpose, platform, access scope, and lifecycle state (provisioned, active, recertified, retired), rather than allowing agents to be created and run without central registration.
  SOURCE: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization ; https://docs.cloud.google.com/agent-builder/overview
- SHOULD: Assign every agent identity a governed, revocable credential/identity object (not a shared or embedded static credential) with explicit sponsorship/ownership and time-bounded access, mirroring identity-governance patterns already applied to human accounts.
  SOURCE: https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview
