# 05 — URL fixes and voice fixes

Data from the 2026-09-02 sweep of 208 unique external URLs (curl, 20 s timeout, browser user agent). Re-run `planning/scripts/check-links.py --external` before acting; hosts move.

## Non-200 results

| Status | URL in docs | Lands on | Verdict |
|---|---|---|---|
| 400 | https://llama.meta.com/ | https://developer.meta.com/ai/ | dead: Meta moved Llama to https://www.llama.com/ (verify 200, then replace) |
| 403 | https://openai.com/research/ | https://openai.com/research/ | bot-block, leave |
| 403 | https://platform.openai.com/docs/overview | https://platform.openai.com/ | bot-block, leave |
| 429 | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/product_discovery/tools.py | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/product_discovery/tools.py | GitHub rate limit during the sweep, recheck singly, expected fine |
| 429 | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/shared/http_resilience.py | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/shared/http_resilience.py | GitHub rate limit during the sweep, recheck singly, expected fine |
| 429 | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/shared/idempotency.py | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/shared/idempotency.py | GitHub rate limit during the sweep, recheck singly, expected fine |
| 429 | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/shared/tool_inputs.py | https://github.com/nitin27may/e-commerce-agents/blob/main/agents/python/shared/tool_inputs.py | GitHub rate limit during the sweep, recheck singly, expected fine |

## Redirects worth acting on (Phase 6)

Replace the docs URL with the final URL unless the note says otherwise. Where the redirect signals a renamed or retired product, the surrounding sentence needs the new name too.

| URL in docs | Final URL | Note |
|---|---|---|
| https://ai.google/responsibility/responsible-ai-practices/ | https://ai.google/principles/#our-ai-principles-in-action | cosmetic, update anyway |
| https://aistudio.google.com/ | https://aistudio.google.com/welcome | cosmetic, update anyway |
| https://blog.google/technology/ai/ | https://blog.google/innovation-and-ai/technology/ai/ | cosmetic, update anyway |
| https://docs.anthropic.com/en/docs/claude-code | https://code.claude.com/docs | Claude Code docs moved host |
| https://deepmind.google/technologies/gemini/ | https://deepmind.google/models/gemini/ | cosmetic, update anyway |
| https://docs.llamaindex.ai/ | https://developers.llamaindex.ai/python/framework/ | LlamaIndex docs moved |
| https://docs.llamaindex.ai/en/stable/ | https://developers.llamaindex.ai/python/framework/ | LlamaIndex docs moved |
| https://platform.openai.com/docs/ | https://developers.openai.com/api/docs | OpenAI docs re-platformed |
| https://platform.openai.com/docs/assistants/overview | https://developers.openai.com/api/docs/assistants/migration | Assistants API deprecated: replace with Responses API / Agents SDK link |
| https://platform.openai.com/docs/guides/embeddings | https://developers.openai.com/api/docs/guides/embeddings | OpenAI docs re-platformed |
| https://platform.openai.com/docs/guides/function-calling | https://developers.openai.com/api/docs/guides/function-calling | OpenAI docs re-platformed |
| https://platform.openai.com/docs/guides/fine-tuning | https://developers.openai.com/api/docs/guides/model-optimization | OpenAI docs re-platformed |
| https://platform.openai.com/docs/guides/prompt-engineering | https://developers.openai.com/api/docs/guides/prompt-engineering | OpenAI docs re-platformed |
| https://platform.openai.com/docs/models | https://developers.openai.com/api/docs/models | OpenAI docs re-platformed |
| https://docs.ag-ui.com/ | https://docs.ag-ui.com/introduction | cosmetic, update anyway |
| https://cloud.google.com/vertex-ai/docs | https://docs.cloud.google.com/gemini-enterprise-agent-platform | Product renamed to Gemini Enterprise Agent Platform |
| https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent | Copilot coding agent renamed cloud agent |
| https://python.langchain.com/docs/tutorials/rag/ | https://docs.langchain.com/oss/python/deepagents/rag | LangChain docs moved; this now lands on the deepagents RAG page, pick the langchain RAG tutorial instead |
| https://python.langchain.com/docs/ | https://docs.langchain.com/oss/python/langchain/overview | LangChain docs moved |
| https://docs.pinecone.io/ | https://docs.pinecone.io/guides/get-started/overview | cosmetic, update anyway |
| https://pytorch.org/docs/ | https://docs.pytorch.org/docs/ | cosmetic, update anyway |
| https://docs.ragas.io/ | https://docs.ragas.io/en/stable/ | cosmetic, update anyway |
| https://weaviate.io/developers/weaviate | https://docs.weaviate.io/weaviate | cosmetic, update anyway |
| https://huggingface.co/docs/peft/ | https://huggingface.co/docs/peft/index | cosmetic, update anyway |
| https://huggingface.co/learn/agents-course | https://huggingface.co/learn/agents-course/unit0/introduction | cosmetic, update anyway |
| https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/ | https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-4.0.0 | cosmetic, update anyway |
| https://learn.microsoft.com/en-us/azure/bot-service/ | https://learn.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0 | cosmetic, update anyway |
| https://learn.microsoft.com/en-us/azure/ai-services/agents/ | https://learn.microsoft.com/en-us/azure/foundry/ | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-services/openai/ | https://learn.microsoft.com/en-us/azure/foundry/ | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-studio/ | https://learn.microsoft.com/en-us/azure/foundry/ | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-services/agents/overview | https://learn.microsoft.com/en-us/azure/foundry/agents/overview | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models | https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-generative-ai-app | https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning | Azure AI Foundry consolidation: rename 'Azure OpenAI Service' / 'Azure AI Studio' in prose |
| https://learn.microsoft.com/en-us/azure/machine-learning/ | https://learn.microsoft.com/en-us/azure/machine-learning/?view=azureml-api-2 | cosmetic, update anyway |
| https://learn.microsoft.com/en-us/microsoft-365-copilot/ | https://learn.microsoft.com/en-us/microsoft-365/copilot/ | cosmetic, update anyway |
| https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/ | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/ | cosmetic, update anyway |
| https://learn.microsoft.com/en-us/training/paths/get-started-with-artificial-intelligence-on-azure/ | https://learn.microsoft.com/en-us/training/paths/get-started-ai-apps-agents/ | Original MS Learn path retired; confirm the replacement path is the right level |
| https://modelcontextprotocol.io/ | https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro | MCP site now serves the dated 2026-07-28 docs; fine as is |
| https://modelcontextprotocol.io/docs/learn/architecture | https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | MCP site now serves the dated 2026-07-28 docs; fine as is |
| https://modelcontextprotocol.io/specification | https://modelcontextprotocol.io/specification/2026-07-28 | MCP site now serves the dated 2026-07-28 docs; fine as is |
| https://blogs.microsoft.com/ai/ | https://news.microsoft.com/source/topics/ai/ | cosmetic, update anyway |
| https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | cosmetic, update anyway |
| https://docs.anthropic.com/ | https://platform.claude.com/docs/en/home | cosmetic, update anyway |
| https://docs.anthropic.com/en/docs/about-claude/models | https://platform.claude.com/docs/en/models/overview | cosmetic, update anyway |
| https://platform.claude.com/docs/en/about-claude/models/overview | https://platform.claude.com/docs/en/models/overview | cosmetic, update anyway |
| https://www.anthropic.com/news/contextual-retrieval | https://www.anthropic.com/engineering/contextual-retrieval | cosmetic, update anyway |
| https://www.deeplearning.ai/short-courses/evaluating-ai-agents/ | https://www.deeplearning.ai/courses/evaluating-ai-agents | cosmetic, update anyway |
| https://www.deeplearning.ai/courses/deep-learning-specialization/ | https://www.deeplearning.ai/specializations/deep-learning | cosmetic, update anyway |
| https://www.nature.com/articles/s41598-019-41695-z | https://www.nature.com/articles/s41598-019-41695-z?error=cookies_not_supported&code=cec4e27b-e1f3-4a6b-a513-9d9ba6ee0291 | cosmetic, update anyway |

## Org-voice lines to rewrite (Phase 3 and 5)

| File:line | Current | Replace with |
|---|---|---|
| docs/index.md:12 | Built for everyone in the organization, regardless of technical background | Written for readers and builders, whatever their technical background |
| docs/index.md:72 | What we use in our organization -- Semantic Kernel, LangChain, Azure AI, and more | The framework and platform landscape, with what has been superseded |
| docs/index.md:98 | Co-op Students & New Joiners | Students and new joiners |
| docs/getting-started/index.md:97 | ## How AI Fits Into Our Organization | delete section |
| docs/getting-started/index.md:111 | our enterprise data ... our actual documents and policies | (section deleted) |
| docs/getting-started/index.md:117 | AI embedded in our daily tools | (section deleted) |
| docs/getting-started/index.md:125 | View Our Stack | (section deleted) |
| docs/getting-started/index.md:145 | Co-op Student / New Joiner | Student / new joiner |
| docs/getting-started/index.md:155 | for what we invest in | for the current landscape |
| docs/whats-new/index.md:52 | to serve everyone in the organization -- from business analysts to software engineers to co-op students | for readers and builders alike |
| docs/whats-new/index.md:60 | What we use | The framework landscape |
| docs/whats-new/index.md:64 | Reach out to the team or submit a pull request | Open an issue or a pull request on GitHub |

Lines in claude-code.md about 'your team' and CLAUDE.md are correct as written (they describe the reader's team) and stay.

## Dash sweep

`grep -rn ' -- ' docs --include=*.md` currently returns 74 lines, all in March-era pages. Replace with an em dash in prose only; skip anything inside a fenced code block.

## Mermaid palette map (Phase 5)

| Foreign value | Replace with | Role |
|---|---|---|
| #057398, #00A0DF, #004987 | #0284c7 | processing / logic |
| #38bdf8 | #14b8a6 | data / storage (light) |
| #632C4F, #853175, #9e57a2 | #0d9488 (primary) or #d97706 (warning), by role | maroon / purple, banned |
| #259638 | #16a34a | success |

Every styled node ends with `color:#fff`. Stroke colours: one shade darker than the fill (see CLAUDE.md classDef examples in the-path.md).
