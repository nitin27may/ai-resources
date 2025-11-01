# Blog Structure

This directory contains the blog feature for AI Resources documentation.

## Blog Purpose

The blog section focuses on **latest news and updates** in the AI ecosystem:

- Latest news and announcements
- New tools and framework releases
- MCP (Model Context Protocol) updates
- AI agents developments
- Emerging coding tools
- Framework version releases

**Note**: For in-depth, structured learning, refer to the main documentation sections. The blog keeps you current with what's new.

## Directory Structure

```
blog/
├── index.md              # Blog landing page
├── .authors.yml          # Author profiles
├── posts/                # Blog posts directory
│   ├── welcome.md       # Welcome post (published)
│   └── rag-tutorial.md  # RAG tutorial (draft)
└── README.md            # This file
```

## Creating a New Blog Post

1. Create a new `.md` file in the `posts/` directory
2. Add frontmatter with metadata:

```yaml
---
draft: false              # Set to true for drafts
date: 2025-10-31         # Publication date
authors:
  - nitin                # Author slug from .authors.yml
categories:
  - Tutorial             # Post categories
tags:
  - rag                  # Post tags
  - tutorial
---
```

3. Write your post content
4. Use `<!-- more -->` to separate excerpt from full content

## Blog Post Template

```markdown
---
draft: false
date: 2025-10-31
authors:
  - nitin
categories:
  - Category Name
tags:
  - tag1
  - tag2
---

# Your Post Title

Brief introduction paragraph that appears in the post listing.

<!-- more -->

## Main Content

Your detailed blog post content goes here...

### Subsections

Add sections as needed.

## Conclusion

Wrap up your post.
```

## Adding Authors

Edit `.authors.yml` to add new authors:

```yaml
authors:
  username:
    name: Full Name
    description: Brief bio
    avatar: https://github.com/username.png
    url: https://github.com/username
```

## Categories

Use these approved categories for blog posts:

- **News & Announcements** - Industry news and important announcements
- **Models & LLMs** - New model releases and updates (GPT, Claude, Llama, etc.)
- **AI Agents** - Agent framework updates and new orchestration patterns
- **MCP Updates** - Model Context Protocol servers and tools
- **Framework Updates** - LangChain, AutoGen, CrewAI, LangGraph releases
- **Tool Releases** - New development tools and libraries
- **Prompt Engineering** - New prompting techniques and best practices
- **Research Highlights** - Important AI research papers and findings
- **Platform Updates** - Azure OpenAI, AWS Bedrock, Google Vertex AI updates
- **Developer Tools** - IDE extensions, debugging tools, productivity tools
- **Observability** - Monitoring and observability tool updates

## Tags

Use relevant tags for better organization:

**By Technology:**
- langchain, autogen, crewai, langgraph
- openai, anthropic, azure-ai
- chromadb, pinecone, weaviate
- mcp, tools, agents

**By Type:**
- release, update, news
- tool, framework, server
- breaking-change, feature
- announcement, preview

**By Topic:**
- ai-agents, multi-agent, orchestration
- rag, vector-database, embeddings
- mcp-server, integration
- ide, vscode, cursor

## Markdown Features

All standard MkDocs Material features are supported:

- Code blocks with syntax highlighting
- Mermaid diagrams
- Admonitions (info, warning, success, etc.)
- Tabs
- Tables
- Images and media

## Preview Drafts

To preview draft posts during development:

```bash
mkdocs serve
```

Draft posts will only appear in serve mode, not in production builds.

## Publishing

1. Set `draft: false` in the frontmatter
2. Set the appropriate `date`
3. Commit and push changes
4. Blog will be automatically updated on next deployment
