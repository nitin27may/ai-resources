# Official Docs Research: Recognised Standards, Frameworks and Vendor Guidance for Secure Enterprise Agents and MCP
SOURCE_TYPE: official-docs
CONFIDENCE: MEDIUM
GENERATED: 2026-09-17T00:00:00+05:30

## Summary
There is now a genuine, citable standards baseline for enterprise agent and MCP security: OWASP's GenAI Security Project has shipped three complementary artifacts (LLM Top 10 2025, Agentic AI Threats and Mitigations / Top 10 for Agentic Applications 2026, and a beta MCP Top 10), NIST has both a voluntary risk-management baseline (AI RMF 1.0 + Generative AI Profile) and an in-flight concrete standards track for agent identity (NCCoE concept paper, Feb 2026), and CSA has produced an agent-specific threat-modeling framework (MAESTRO) plus MCP and IAM taxonomies. Government guidance moved from generic secure-development guidelines (CISA/NCSC 2023) to agent-specific operational guidance (Five Eyes "Careful Adoption of Agentic AI Services," May 2026). Vendor design guidance (Anthropic, OpenAI, Google) and academic work (Beurer-Kellner et al.'s six design patterns, Google DeepMind's CaMeL, Meta's Agents Rule of Two) converge on the same handful of controls: least privilege, human confirmation for irreversible actions, provenance/data-flow separation between trusted control and untrusted content, and observability. Identity/authorization standardization is the least mature area — IETF drafts (OAuth for AI agents, OpenID Connect agent identity claims) and RFC 8693 token exchange are being repurposed for agent delegation, but nothing is yet an approved RFC or final OpenID spec, and NIST's own agent-identity work is still a concept paper open for comment as of April 2026.

## Key Findings

### 1. OWASP GenAI Security Project

- FINDING: "OWASP Top 10 for LLM Applications 2025" (published 17 November 2024) is the current, citable version. Exact 10 entries: LLM01:2025 Prompt Injection; LLM02:2025 Sensitive Information Disclosure; LLM03:2025 Supply Chain; LLM04:2025 Data and Model Poisoning; LLM05:2025 Improper Output Handling; LLM06:2025 Excessive Agency; LLM07:2025 System Prompt Leakage; LLM08:2025 Vector and Embedding Weaknesses; LLM09:2025 Misinformation; LLM10:2025 Unbounded Consumption.
  SOURCE: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- FINDING: LLM01 (Prompt Injection) explicitly distinguishes direct injection (jailbreaking) from indirect injection via external/retrieved content — directly relevant to agents consuming tool output and MCP resources.
  SOURCE: https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/
- FINDING: LLM06 Excessive Agency covers agents granted overly broad permissions, autonomy, or functionality — e.g., delete permission where read-only would suffice, unscoped file access, or command execution without human approval. This is the single most agent-relevant entry in the LLM Top 10.
  SOURCE: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- FINDING: LLM10 Unbounded Consumption (expanded from the older "Model Denial of Service" entry) covers uncontrolled resource usage, cost, and availability risk from unrestricted LLM/agent invocation loops.
  SOURCE: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- FINDING: "Agentic AI — Threats and Mitigations" is the first guide in the OWASP GenAI Security Project's Agentic Security Initiative (ASI). It provides a threat-model-based taxonomy structured across Agent Design, Agent Memory, Planning & Autonomy, Tool Use, and Deployment & Operations, and underpins the later Top 10 for Agentic Applications.
  SOURCE: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- FINDING: "Securing Agentic Applications Guide 1.0" (published 27 July 2025) gives concrete, implementation-level controls (as opposed to the theoretical threat taxonomy) for builders/defenders of agentic systems.
  SOURCE: https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/
- FINDING: "OWASP Top 10 for Agentic Applications for 2026" was published 9 December 2025, developed with 100+ industry experts. Exact 10 entries: ASI01 Agent Goal Hijack; ASI02 Tool Misuse & Exploitation; ASI03 Identity & Privilege Abuse; ASI04 Agentic Supply Chain Vulnerabilities; ASI05 Unexpected Code Execution (RCE); ASI06 Memory & Context Poisoning; ASI07 Insecure Inter-Agent Communication; ASI08 Cascading Failures; ASI09 Human-Agent Trust Exploitation; ASI10 Rogue Agents.
  SOURCE: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- FINDING: ASI04 (Agentic Supply Chain Vulnerabilities) explicitly names malicious or vulnerable components in agent frameworks, tools, and **MCP servers** as compromise vectors — the clearest OWASP linkage between agent risk and MCP.
  SOURCE: https://cycode.com/blog/owasp-top-10-agentic-applications/
- FINDING: "OWASP MCP Top 10" exists as a dedicated, MCP-specific list, currently in Beta / Phase 3 (pilot testing) under project lead Vandana Verma Sehgal, with IDs formatted MCP0X:2025. Exact 10 entries: MCP01:2025 Token Mismanagement & Secret Exposure; MCP02:2025 Privilege Escalation via Scope Creep; MCP03:2025 Tool Poisoning; MCP04:2025 Software Supply Chain Attacks & Dependency Tampering; MCP05:2025 Command Injection & Execution; MCP06:2025 Prompt Injection via Contextual Payloads; MCP07:2025 Insufficient Authentication & Authorization; MCP08:2025 Lack of Audit and Telemetry; MCP09:2025 Shadow MCP Servers; MCP10:2025 Context Injection & Over-Sharing.
  SOURCE: https://owasp.org/www-project-mcp-top-10/
  SOURCE: https://github.com/OWASP/www-project-mcp-top-10
- FINDING: The OWASP MCP Top 10 project page frames itself explicitly as a living document (beta status, no fixed publication date given on the project page as of the research date) — treat version/date as provisional and re-check before citing in a final deliverable.
  SOURCE: https://nest.owasp.org/projects/mcp-top-10

### 2. NIST

- FINDING: NIST AI Risk Management Framework 1.0 (NIST AI 100-1) was published 26 January 2023. It is voluntary, sector/technology-agnostic, and structured around four core functions: GOVERN, MAP, MEASURE, MANAGE.
  SOURCE: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- FINDING: NIST AI 600-1, "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile," published July 2024, cross-walks the AI RMF's four functions onto 12 generative-AI-specific risk categories (200+ suggested actions), developed under Executive Order 14110 Section 4.1(a)(i)(A). It is voluntary for the private sector but increasingly referenced in federal procurement.
  SOURCE: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- FINDING: NIST's National Cybersecurity Center of Excellence (NCCoE) published a concept paper, "Accelerating the Adoption of Software and AI Agent Identity and Authorization," on 5 February 2026, with public comment open through 2 April 2026. It proposes adapting existing identity/authorization frameworks so AI agents are treated as identifiable enterprise entities (not anonymous automation under shared credentials), and aims to produce a practical implementation guide from an NCCoE lab demonstration. This is a concept/pre-standard stage document, not a finished SP.
  SOURCE: https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization
  SOURCE: https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd
- FINDING: NIST SP 800-207, "Zero Trust Architecture," is the authoritative US ZTA standard and already generalizes "identity" as the primary trust signal for both human and Non-Person Entities (NPEs) — a foundation being explicitly reused by agent-identity commentary ahead of a dedicated NIST agent standard. It predates the agentic-AI wave, so any "applied to agents" framing is industry interpretation, not a NIST-authored agent profile.
  SOURCE: https://csrc.nist.gov/pubs/sp/800/207/final
- FINDING: Industry analysis (not NIST-authored) reports that only ~22% of security practitioners currently treat agents as independent identities rather than shared API keys/inherited sessions — cited as the gap the NCCoE concept paper and CAISI work are trying to close. Treat this figure as third-party research, not a NIST statistic.
  SOURCE: https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ai-agent-standards-federal-framework/

### 3. CoSAI, CSA MAESTRO, ISO/IEC 42001

- FINDING: CoSAI (Coalition for Secure AI), launched at the Aspen Security Forum in 2024, published a taxonomy and practical guide dedicated to MCP security — "Securing the AI Agent Revolution: A Practical Guide to Model Context Protocol Security" — plus a companion Agentic Identity and Access Management framework, positioned as a layered blueprint: principles → MCP security (protocol layer) → agentic IAM (trust layer).
  SOURCE: https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/
  SOURCE: https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/
- FINDING: CoSAI released an "extensive taxonomy for Model Context Protocol security" (announced 27 January 2026) and unveiled new agentic identity/security research around RSAC 2026 (announced 6 May 2026).
  SOURCE: https://www.oasis-open.org/2026/01/27/coalition-for-secure-ai-releases-extensive-taxonomy-for-model-context-protocol-security/
  SOURCE: https://www.oasis-open.org/2026/05/06/coalition-for-secure-ai-unveils-new-agentic-identity-and-security-research-following-high-profile-sessions-at-rsac-2026/
- FINDING: CSA's MAESTRO (Multi-Agent Environment, Security, Threat, Risk, & Outcome) threat-modeling framework was introduced 6 February 2025. It layers agentic architecture into seven layers: (1) Foundation Models, (2) Data Operations, (3) Agent Frameworks, (4) Deployment and Infrastructure, (5) Evaluation and Observability, (6) Security and Compliance (cross-cutting), (7) Agent Ecosystem. It builds on STRIDE/PASTA/LINDDUN and adds agent-specific threat classes tied to non-determinism, autonomy, and absent trust boundaries; "Agent Tool Misuse" is called out explicitly at Layer 7, and Layer 3 covers compromised/vulnerable agent-framework and supply-chain components (the closest MAESTRO layer to MCP-server risk, though the framework doesn't name MCP directly).
  SOURCE: https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro
  SOURCE: https://github.com/CloudSecurityAlliance/MAESTRO
- FINDING: CSA's "Agentic AI Identity and Access Management" paper proposes decentralized, verifiable agent identities (DIDs/Verifiable Credentials), an Agent Naming Service for discovery, attribute/policy-based dynamic access control, and zero-trust-based session management with real-time revocation — a CSA design proposal, not a ratified standard.
  SOURCE: https://cybercompliancewatch.org/csa-agentic-ai-iam/
- FINDING: ISO/IEC 42001:2023 is the first international, certifiable AI management-system standard (published December 2023). It requires an organization to run a Plan-Do-Check-Act management system covering AI risk management, system-lifecycle management, impact assessment, and third-party/supplier oversight; it is a governance/process standard, not a technical control catalogue, so it should be cited for organizational accountability (audit trail, management commitment, supplier due diligence for MCP/tool providers) rather than for specific agent or MCP technical controls.
  SOURCE: https://www.iso.org/standard/42001

### 4. UK NCSC / CISA / Five Eyes joint guidance

- FINDING: CISA and the UK NCSC, joined by agencies from 17 other nations, published "Guidelines for Secure AI System Development" (announced 26 November 2023). It structures security controls across four AI development-lifecycle stages: secure design, secure development, secure deployment, secure operation and maintenance, and is explicitly Secure-by-Design-aligned. This predates the agentic-AI wave and is general-purpose AI-system guidance, not agent-specific.
  SOURCE: https://www.cisa.gov/news-events/alerts/2023/11/26/cisa-and-uk-ncsc-unveil-joint-guidelines-secure-ai-system-development
  SOURCE: https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development
- FINDING: "Careful Adoption of Agentic AI Services" — the first Five Eyes joint guidance specifically on agentic AI — was published 1 May 2026 by CISA, NSA, Australian Cyber Security Centre (ASD ACSC), Canadian Centre for Cyber Security, and UK/NZ NCSCs. It defines five agentic-deployment risk categories with concrete mitigations: privilege escalation, design and configuration flaws, behavioral misalignment, structural cascading failures, and accountability opacity. Explicit recommendations: do not grant agents broad/unrestricted access; start with low-risk, non-sensitive use cases; fold agentic AI into the existing security model rather than treating it as a separate experimental track. Document runs to 30 pages, covers the full adoption lifecycle.
  SOURCE: https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services
  SOURCE: https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF

### 5. Vendor design guidance (Anthropic, OpenAI, Google)

- FINDING: Anthropic, "Building Effective Agents" (December 2024) — core recommendation is to prefer simple, composable patterns (prompt chaining, routing, parallelization, orchestrator-worker, evaluator-optimizer) over complex agentic frameworks, and to add autonomy only when workflow patterns are insufficient.
  SOURCE: https://www.anthropic.com/engineering/building-effective-agents
- FINDING: Anthropic, "Writing Effective Tools for AI Agents" (11 September 2025) — key controls: choose the right tools to implement (don't wrap every API endpoint 1:1), namespace tools for clear boundaries, return meaningful/high-signal context rather than raw payloads, optimize for token efficiency (pagination, filtering, truncation with sensible defaults, response-format enums), and prompt-engineer tool descriptions with the same rigor as human-facing docs.
  SOURCE: https://www.anthropic.com/engineering/writing-tools-for-agents (referenced via https://laxmikumars.medium.com/writing-effective-tools-for-ai-agents-lessons-from-anthropic-25b85bf74f5d)
- FINDING: Anthropic, "Effective Context Engineering for AI Agents" — recommends "just-in-time" context loading (lightweight identifiers/references resolved to full content only at the point of use) over front-loading full context, to control token growth and reduce the attack surface of context poisoning in long-running agents.
  SOURCE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- FINDING: Anthropic, "How We Contain Claude Across Products" (25 May 2026) — three containment layers: Environment layer (ephemeral containers for claude.ai, human-in-the-loop OS-enforced sandboxes for Claude Code, sealed VMs for Claude Cowork), Model layer (system prompts/classifiers/behavioral training/pre-execution approval), and Content-access layer (tool permission granularity, external connector auditing, network egress control with inspection). Core design rule: "design for containment at the environment layer first, then steer behavior at the model layer" — prefer battle-tested primitives (hypervisors, syscall filters, containers) over custom-built isolation. Addresses three risk sources: user misuse, model misbehavior, external attack.
  SOURCE: https://www.anthropic.com/engineering/how-we-contain-claude
- FINDING: Anthropic, "Code Execution with MCP: Building More Efficient AI Agents" — discusses letting agents write and execute code against MCP tools rather than only issuing direct tool calls, trading token/latency efficiency against the need for a secure execution sandbox with resource limits and monitoring.
  SOURCE: https://www.anthropic.com/engineering/code-execution-with-mcp
- FINDING: OpenAI, "A Practical Guide to Building Agents" (PDF, 34 pages) defines an agent as "a system that uses an LLM to manage workflow execution and dynamically select tools within defined guardrails," and provides frameworks for use-case selection, orchestration design, and guardrails for safe/predictable operation.
  SOURCE: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- FINDING: OpenAI Platform docs, "Safety Best Practices" and "Safety in Building Agents" — recommend guardrails and tool-call confirmations, sanitizing inputs to redact PII and detect jailbreak attempts, enabling tool approvals so users review/confirm every MCP tool operation, using a human-approval node in Agent Builder, and red-teaming against adversarial input across a wide range of behaviors. Explicit caveat in the docs: agents "won't be perfect and can still make mistakes or be tricked" — access granted to agents must be scoped accordingly.
  SOURCE: https://platform.openai.com/docs/guides/safety-best-practices
  SOURCE: https://platform.openai.com/docs/guides/agent-builder-safety
- FINDING: Google SAIF (Secure AI Framework) — "An Introduction to Secure AI Agents" / "Focus on Agents" defines two primary agent risk categories (Rogue Actions — accidental/misaligned or malicious e.g. via indirect prompt injection, poisoning, evasion; and Sensitive Data Disclosure) and three core security principles: (1) agents must have well-defined human controllers, with explicit human confirmation required for critical/irreversible actions; (2) agent powers must be dynamically and narrowly constrained via least privilege, scoped OAuth tokens, and sandboxing; (3) agent actions and planning must be observable via robust logging and transparent UIs.
  SOURCE: https://saif.google/focus-on-agents
  SOURCE: https://saif.google/secure-ai-framework/risks
  SOURCE: https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents
- FINDING: Google Cloud also publishes a "SAIF Agent Risk Self-Assessment" tool for organizations to score their agent deployments against these principles.
  SOURCE: https://saif.google/agent-risk-self-assessment

### 6. Academic design patterns

- FINDING: Beurer-Kellner, Buesser, Creţu, Debenedetti, Dobos, Fabian, Fischer, Froelicher, Grosse, Naeff, Ozoani, Paverd, Tramèr, Volhejn, "Design Patterns for Securing LLM Agents against Prompt Injections" (arXiv:2506.08837, first posted June 2025, revised v2). Proposes six design patterns that restrict agent actions to prevent them from being repurposed toward arbitrary attacker goals, with a systematic utility/security trade-off analysis and case studies. (Note: this research pass could not confirm the six patterns' exact names against the primary PDF within the available fetch budget — the paper is widely summarized as covering patterns such as the Action-Selector, Plan-Then-Execute, LLM Map-Reduce, Dual LLM, Code-Then-Execute, and Context-Minimization patterns; treat the exact pattern names as a GAP to verify directly against arXiv:2506.08837 before quoting them in the final deliverable.)
  SOURCE: https://arxiv.org/abs/2506.08837
- FINDING: Google DeepMind, "Defeating Prompt Injections by Design" (CaMeL) (arXiv:2503.18813, 2025) — proposes an architecture-level defense (not a model-tuning or input-filtering approach) that explicitly extracts control flow and data flow from a trusted user query using a custom Python interpreter, enforcing "capabilities" so untrusted tool/retrieved data can never influence program control flow or exfiltrate data over unauthorized paths. Claimed as the first architecture-level defense with formal security guarantees against prompt injection; evaluated against the AgentDojo benchmark. Explicitly builds on Simon Willison's "Dual LLM" pattern.
  SOURCE: https://arxiv.org/pdf/2503.18813
  SOURCE: https://github.com/google-research/camel-prompt-injection
- FINDING: Meta, "Agents Rule of Two: A Practical Approach to AI Agent Security" (published 31 October 2025 on Meta's AI blog). Structural rule: within a single agent session (until robustness research can reliably detect/refuse prompt injection), an agent must satisfy no more than two of three properties: (A) processes untrustworthy/attacker-influenceable input, (B) has access to sensitive systems or private data, (C) can change state or communicate externally (send data, execute writes). If a task genuinely requires all three, the agent must not run fully autonomously — it requires human-in-the-loop approval or another reliable validation mechanism before proceeding.
  SOURCE: https://ai.meta.com/blog/practical-ai-agent-security/

### 7. IETF / OpenID identity and authorization work

- FINDING: RFC 8693, "OAuth 2.0 Token Exchange," is a finalized IETF RFC that defines the `act` (actor) claim — expressing that delegation has occurred and identifying the acting party — and the `may_act` claim, which an authorization server uses to pre-authorize which parties may act on behalf of a subject. Industry consensus (not an RFC amendment) is converging on RFC 8693 token-exchange semantics as the mechanism for agent delegation chains (On-Behalf-Of tokens carrying both the delegating agent's and the original user's identity as separate claims).
  SOURCE: https://www.rfc-editor.org/rfc/rfc8693.xml
  SOURCE: https://www.rfc-editor.org/info/rfc8693/
- FINDING: IETF Internet-Draft "OAuth 2.0 Extension: On-Behalf-Of User Authorization for AI Agents" (draft-oauth-ai-agents-on-behalf-of-user, latest revision -02, last updated 26 February 2026; per IETF datatracker, an earlier revision expired) introduces `requested_actor` (identifies the specific agent requiring delegation in the authorization request) and `actor_token` (authenticates the agent during the code-for-token exchange). Resulting access tokens carry claims documenting the full delegation chain from user → client application → agent. This is a draft, not an approved standard — status and expiry must be re-checked before citing a specific revision.
  SOURCE: https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user-02
- FINDING: IETF Internet-Draft "draft-klrc-aiagent-auth" ("AI Agent Authentication and Authorization," revision -03) and "draft-sharif-openid-agent-identity" ("OpenID Connect Agent Identity Claims for Autonomous AI Agents," revision -00) are further early-stage individual drafts extending OIDC to carry agent-identity claims. Both are pre-working-group individual submissions — cite as "work in progress," not settled protocol.
  SOURCE: https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/
  SOURCE: https://datatracker.ietf.org/doc/draft-sharif-openid-agent-identity/00/
- FINDING: OpenID Foundation whitepaper, "Identity Management for Agentic AI: The New Frontier of Authorization, Authentication, and Security for an AI Agent World" (published October 2025 by the OpenID Foundation's Artificial Intelligence Identity Management Community Group; also mirrored on arXiv as 2510.25819). Identifies token-exchange-based delegation as a foundational building block, and sets out an agenda covering scalable access control, agent-centric identity, differentiating AI workloads from human/service identities, and delegated authority chains.
  SOURCE: https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf
  SOURCE: https://openid.net/new-whitepaper-tackles-ai-agent-identity-challenges/

## Code / Config
No runnable code samples were captured; the sources in this research pass are standards documents, threat models, and design-pattern papers rather than SDK/API reference material. (Runnable MCP/agent code samples should be sourced separately from vendor SDK docs, e.g. Anthropic's MCP spec repo or the Claude Agent SDK docs, if needed for the companion best-practices documents.)

## Caveats / Gaps
- OWASP MCP Top 10 is explicitly in Beta (Phase 3 pilot testing) as of this research pass; entry names/IDs (MCP01–MCP10:2025) may still change before a final release. Re-verify immediately before publication.
- OWASP Top 10 for Agentic Applications 2026 was fetched via a third-party summary (Cycode) cross-checked against a WebSearch snippet from genai.owasp.org's own December 2025 announcement; the ASI01–ASI10 titles and one-line descriptions should ideally be re-verified against the primary OWASP PDF download before quoting verbatim in the final document, since the WebFetch tool could not extract the list directly from the OWASP landing page (image/PDF-gated content).
- The exact names of the "six design patterns" in Beurer-Kellner et al. 2025 could not be confirmed against the primary arXiv PDF text within this session (WebFetch was not used directly on the PDF); the names given in the Key Findings section are a best-effort characterization from secondary summaries and MUST be verified against https://arxiv.org/pdf/2506.08837 (or arXiv HTML rendering) before being asserted as exact in a downstream document.
- NIST's NCCoE "Software and AI Agent Identity and Authorization" work is a concept paper with a comment period that closed 2 April 2026; as of the "today" date given for this task (17 September 2026) there may be a follow-on draft NIST Special Publication or demonstration announcement not captured in this pass — recommend a fresh check on https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization before finalizing the best-practices documents.
- All three IETF drafts cited (on-behalf-of-user, aiagent-auth, openid-agent-identity) are individual Internet-Drafts, not IETF-working-group or IESG-approved documents; drafts expire every 6 months and renumber. Cite the datatracker "latest" URL rather than a pinned revision number in the final deliverable, and note explicitly that none of this identity/authorization work is a ratified standard as of the research date.
- Google's SAIF "secure AI agents" paper content was only reachable via secondary summaries and a corrupted-PDF fetch attempt (services.google.com/fh/files/misc/ociso_2025_saif_cloud_paper.pdf did not extract cleanly); the three-principle framing is corroborated across three independent sources (saif.google/focus-on-agents, saif.google/secure-ai-framework/risks, Google Cloud CISO Perspectives blog) so confidence is reasonable, but the primary PDF should be fetched directly (not via this tool's PDF handling) if verbatim quotes are needed.
- CSA MAESTRO's seven-layer names are corroborated from the CSA blog post (Feb 2025) but the canonical MAESTRO GitHub repo (github.com/CloudSecurityAlliance/MAESTRO) was not directly fetched in this pass — recommend a direct check if layer names need to be quoted exactly in a final publication.
- ISO/IEC 42001 section is intentionally kept to a governance-level paragraph per the task's own scope instruction ("one paragraph only") and should not be expanded into technical control claims — it is a management-system (process/audit) standard, not a technical security-control catalogue.
- "NIST/CAISI work on agent hijacking" specifically (as distinct from the NCCoE identity/authorization concept paper) was not separately confirmed as a distinct named publication in this pass; only secondary references to a "CAISI initiative" were found. Flag as unverified/GAP — do not assert a specific NIST CAISI agent-hijacking publication exists without a direct primary-source check.

## Cross-Walk Table

| Best-practice theme | Standards / frameworks that cover it | Exact control / risk IDs |
|---|---|---|
| **Identity** (agent has a real, non-shared identity; delegation is traceable) | NIST NCCoE concept paper; CSA Agentic IAM; OpenID Foundation whitepaper; IETF drafts; RFC 8693; OWASP Agentic Top 10; OWASP MCP Top 10 | NCCoE "Software and AI Agent Identity and Authorization" (concept paper, Feb 2026); RFC 8693 `act`/`may_act` claims; draft-oauth-ai-agents-on-behalf-of-user (`requested_actor`, `actor_token`); ASI03 Identity & Privilege Abuse; ASI07 Insecure Inter-Agent Communication; MCP07:2025 Insufficient Authentication & Authorization |
| **Least privilege** (agent powers scoped and dynamically constrained) | OWASP LLM Top 10; OWASP Agentic Top 10; OWASP MCP Top 10; Google SAIF; NIST SP 800-207 (ZTA "enforce least privilege" principle); CSA Agentic IAM | LLM06:2025 Excessive Agency; ASI03 Identity & Privilege Abuse; MCP02:2025 Privilege Escalation via Scope Creep; Google SAIF Principle 2 (dynamically constrained powers / scoped OAuth tokens / sandboxing) |
| **Prompt injection** (untrusted content altering agent behavior) | OWASP LLM Top 10; OWASP Agentic Threats & Mitigations; OWASP MCP Top 10; Beurer-Kellner et al. 2025; Google DeepMind CaMeL; Meta Agents Rule of Two | LLM01:2025 Prompt Injection; ASI01 Agent Goal Hijack; MCP06:2025 Prompt Injection via Contextual Payloads; MCP10:2025 Context Injection & Over-Sharing; Beurer-Kellner six design patterns (arXiv:2506.08837); CaMeL control/data-flow separation (arXiv:2503.18813); Meta "Rule of Two" (untrusted input + sensitive access + state change ≤ 2 of 3) |
| **Excessive agency** (over-broad autonomy/decision authority) | OWASP LLM Top 10; OWASP Agentic Top 10; Google SAIF; Five Eyes CISA/NSA guidance; Anthropic containment guidance | LLM06:2025 Excessive Agency; ASI01 Agent Goal Hijack; ASI09 Human-Agent Trust Exploitation; ASI10 Rogue Agents; Google SAIF Principle 1 (well-defined human controllers, explicit confirmation for critical/irreversible actions); Five Eyes "behavioral misalignment" risk category |
| **Sandboxing / containment** (execution isolation, resource limits) | OWASP Agentic Top 10; MAESTRO (CSA); Anthropic "How We Contain Claude" / "Code Execution with MCP"; OWASP MCP Top 10 | ASI05 Unexpected Code Execution (RCE); MAESTRO Layer 4 (Deployment and Infrastructure); MCP05:2025 Command Injection & Execution; Anthropic environment-layer containment (ephemeral containers, OS-enforced sandboxes, sealed VMs, network egress control) |
| **Observability** (agent actions/planning logged, auditable) | OWASP LLM/Agentic/MCP Top 10s; Google SAIF; Five Eyes CISA/NSA guidance; Anthropic containment guidance | ASI08 Cascading Failures (requires monitoring to detect); MCP08:2025 Lack of Audit and Telemetry; Google SAIF Principle 3 (observable actions via robust logging and transparent UIs); Five Eyes "accountability opacity" risk category |
| **Human oversight** (approval gates for high-impact/irreversible actions) | Google SAIF; OpenAI Agent Builder safety guidance; Meta Agents Rule of Two; OWASP Agentic Top 10; Five Eyes guidance | Google SAIF Principle 1; OpenAI "human approval node" / MCP tool-approval guidance; Meta Rule of Two (mandatory HITL when all 3 properties present); ASI09 Human-Agent Trust Exploitation |
| **Supply chain** (framework, tool, and MCP-server provenance) | OWASP LLM Top 10; OWASP Agentic Top 10; OWASP MCP Top 10; MAESTRO; ISO/IEC 42001 (supplier oversight, governance-level) | LLM03:2025 Supply Chain; ASI04 Agentic Supply Chain Vulnerabilities; MCP04:2025 Software Supply Chain Attacks & Dependency Tampering; MCP09:2025 Shadow MCP Servers; MAESTRO Layer 3 (Agent Frameworks); ISO/IEC 42001 third-party/supplier oversight clause |
| **Discovery** (safe/authenticated tool and agent discovery) | OWASP MCP Top 10; CSA Agentic IAM (Agent Naming Service); OWASP Agentic Top 10 | MCP09:2025 Shadow MCP Servers; MCP03:2025 Tool Poisoning; CSA Agentic IAM "Agent Naming Service" concept; ASI07 Insecure Inter-Agent Communication |

## Sources
- https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ — OWASP Top 10 for LLM Applications 2025
- https://genai.owasp.org/llm-top-10/ — LLMRisks Archive (OWASP Gen AI Security Project)
- https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ — OWASP LLM10:2025 Unbounded Consumption
- https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ — Agentic AI — OWASP Lists Threats and Mitigations
- https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/ — Securing Agentic Applications Guide 1.0
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ — OWASP Top 10 for Agentic Applications for 2026
- https://cycode.com/blog/owasp-top-10-agentic-applications/ — OWASP Top 10 for Agentic Applications 2026 Explained (secondary, ASI01–ASI10 list)
- https://genai.owasp.org/initiatives/agentic-security-initiative/ — Agentic Security Initiative
- https://owasp.org/www-project-mcp-top-10/ — OWASP MCP Top 10 (project page)
- https://nest.owasp.org/projects/mcp-top-10 — OWASP MCP Top 10 — OWASP Nest
- https://github.com/OWASP/www-project-mcp-top-10 — OWASP MCP Top 10 GitHub repo
- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10 — NIST AI RMF 1.0 (NIST AI 100-1)
- https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf — NIST AI 600-1 Generative AI Profile
- https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization — NCCoE: Software and AI Agent Identity and Authorization
- https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd — NCCoE concept paper (initial public draft)
- https://csrc.nist.gov/pubs/sp/800/207/final — NIST SP 800-207 Zero Trust Architecture
- https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/ — CoSAI: Securing the AI Agent Revolution (MCP Security guide)
- https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/ — CoSAI Principles for Secure-by-Design Agentic Systems
- https://www.oasis-open.org/2026/01/27/coalition-for-secure-ai-releases-extensive-taxonomy-for-model-context-protocol-security/ — CoSAI MCP security taxonomy release
- https://www.oasis-open.org/2026/05/06/coalition-for-secure-ai-unveils-new-agentic-identity-and-security-research-following-high-profile-sessions-at-rsac-2026/ — CoSAI agentic identity/security research at RSAC 2026
- https://cybercompliancewatch.org/csa-agentic-ai-iam/ — CSA Agentic AI Identity and Access Management
- https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro — CSA: Agentic AI Threat Modeling Framework MAESTRO
- https://labs.cloudsecurityalliance.org/maestro/ — CSA MAESTRO Lab Space
- https://github.com/CloudSecurityAlliance/MAESTRO — MAESTRO GitHub repository
- https://www.iso.org/standard/42001 — ISO/IEC 42001:2023
- https://www.cisa.gov/news-events/alerts/2023/11/26/cisa-and-uk-ncsc-unveil-joint-guidelines-secure-ai-system-development — CISA/NCSC Guidelines for Secure AI System Development
- https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development — NCSC: Guidelines for secure AI system development
- https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services — CISA: Careful Adoption of Agentic AI Services
- https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF — Careful Adoption of Agentic AI Services (Five Eyes, PDF)
- https://www.anthropic.com/engineering/building-effective-agents — Building Effective Agents (Anthropic)
- https://www.anthropic.com/engineering/writing-tools-for-agents — Writing Effective Tools for AI Agents (Anthropic)
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — Effective Context Engineering for AI Agents (Anthropic)
- https://www.anthropic.com/engineering/how-we-contain-claude — How We Contain Claude Across Products (Anthropic)
- https://www.anthropic.com/engineering/code-execution-with-mcp — Code Execution with MCP (Anthropic)
- https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf — A Practical Guide to Building Agents (OpenAI, PDF)
- https://platform.openai.com/docs/guides/safety-best-practices — Safety Best Practices (OpenAI API docs)
- https://platform.openai.com/docs/guides/agent-builder-safety — Safety in Building Agents (OpenAI API docs)
- https://saif.google/focus-on-agents — Components of Generative AI Systems / Focus on Agents (Google SAIF)
- https://saif.google/secure-ai-framework/risks — Top Risks of Generative AI Systems (Google SAIF)
- https://saif.google/agent-risk-self-assessment — SAIF Agent Risk Self-Assessment
- https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents — Cloud CISO Perspectives: How Google secures AI Agents
- https://arxiv.org/abs/2506.08837 — Design Patterns for Securing LLM Agents against Prompt Injections (Beurer-Kellner et al., 2025)
- https://arxiv.org/pdf/2503.18813 — Defeating Prompt Injections by Design (CaMeL, Google DeepMind, 2025)
- https://github.com/google-research/camel-prompt-injection — CaMeL reference implementation
- https://ai.meta.com/blog/practical-ai-agent-security/ — Agents Rule of Two: A Practical Approach to AI Agent Security (Meta)
- https://www.rfc-editor.org/rfc/rfc8693.xml — RFC 8693: OAuth 2.0 Token Exchange
- https://www.rfc-editor.org/info/rfc8693/ — RFC 8693 info page
- https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user-02 — OAuth 2.0 Extension: On-Behalf-Of User Authorization for AI Agents (IETF Internet-Draft)
- https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/ — AI Agent Authentication and Authorization (IETF Internet-Draft)
- https://datatracker.ietf.org/doc/draft-sharif-openid-agent-identity/00/ — OpenID Connect Agent Identity Claims for Autonomous AI Agents (IETF Internet-Draft)
- https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf — Identity Management for Agentic AI (OpenID Foundation whitepaper, PDF)
- https://openid.net/new-whitepaper-tackles-ai-agent-identity-challenges/ — New whitepaper tackles AI agent identity challenges (OpenID Foundation)
