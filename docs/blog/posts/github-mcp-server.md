---

date: 2025-11-03
authors:
  - nitin
categories:
  - MCP Updates
  - Tool Releases
tags:
  - mcp
  - mcp-server
  - github
  - integration
comments: true
---

# New MCP Server: GitHub Integration Now Available

A new Model Context Protocol server for GitHub has been released, enabling AI agents to interact with repositories, issues, pull requests, and more.

<!-- more -->

## Overview

The GitHub MCP server provides seamless integration between AI applications and GitHub's API, allowing agents to:

- Read and search repository contents
- Create and manage issues
- Review and comment on pull requests
- Access commit history and diffs
- Manage project boards

## Key Features

### Repository Operations
- Clone and browse repository contents
- Search code across repositories
- Access file contents and history
- List branches and tags

### Issue Management
- Create, update, and close issues
- Add labels and assignees
- Search issues with filters
- Comment on existing issues

### Pull Request Workflow
- List and review pull requests
- Add review comments
- Request changes or approve
- Merge pull requests

### Code Search
- Semantic code search across repositories
- Search by language, path, or content
- Filter by organization or user

## Installation

Install via npm:

```bash
npm install -g @modelcontextprotocol/server-github
```

Or use with npx:

```bash
npx @modelcontextprotocol/server-github
```

## Configuration

Add to your MCP settings:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Authentication

Generate a GitHub Personal Access Token with required permissions:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create new token with scopes:
   - `repo` - Full control of private repositories
   - `read:org` - Read organization data
   - `read:user` - Read user profile data

3. Set as environment variable:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

## Usage Examples

### Search Code

```
Find all TypeScript files that use the useState hook in my repositories
```

The agent will use the GitHub MCP server to search and return results.

### Create Issue

```
Create an issue in my-repo titled "Add authentication" with label "enhancement"
```

### Review Pull Request

```
Review pull request #123 in my-org/my-repo and check for security issues
```

## Use Cases

**Code Review Automation**
- Automatically review PRs for common issues
- Generate review comments
- Check coding standards compliance

**Project Management**
- Triage and categorize issues
- Update project boards
- Generate status reports

**Documentation**
- Generate documentation from code
- Update README files
- Create release notes

**Security Scanning**
- Scan for security vulnerabilities
- Check dependency updates
- Audit access permissions

## Security Considerations

!!! warning "Token Security"
    - Never commit tokens to version control
    - Use environment variables or secure vaults
    - Rotate tokens regularly
    - Use minimum required permissions

## Resources

- [GitHub MCP Server Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [MCP Documentation](/mcp/)
- [GitHub API Documentation](https://docs.github.com/rest)

## Related Servers

Check out other MCP servers:
- **GitLab MCP Server** - Similar functionality for GitLab
- **Azure DevOps MCP Server** - Azure Repos integration
- **Bitbucket MCP Server** - Bitbucket Cloud integration

---

*Last updated: November 3, 2025*
