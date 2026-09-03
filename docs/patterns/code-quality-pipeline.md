---
description: Using AI in a code quality pipeline — linting, review, duplication detection and CI.
tags:
  - Go deeper
  - Operations
  - Copilot
---

# AI-generated code quality pipeline

!!! abstract "Go deeper · 40 min · hands-on"
    **Before this:** [Design principles](design-principles.md)  ·  **After this:** [Frameworks and platforms](../tools-and-frameworks/index.md)

AI coding assistants can accelerate delivery, but they can also introduce dead code, duplicate logic, inconsistent patterns, and over-complex implementations. This page outlines a practical quality pipeline that helps teams review AI-generated code with the same rigor as any other production change.

---

## Why AI-generated code needs extra guardrails

AI tools are good at producing complete-looking solutions quickly. That speed is valuable, but it also makes it easier to accumulate code that is never used, hard to maintain, or insufficiently tested.

The most common risks are:

| Risk | What Happens | Why AI Makes It Worse |
|------|--------------|-----------------------|
| Dead code | Functions, classes, or files exist but are never used | AI often generates supporting code "just in case" |
| Unused dependencies | Packages are added but not actually imported or required | AI may speculate on libraries while exploring solutions |
| Code duplication | Similar logic is repeated across multiple files | Separate prompts can recreate helpers rather than reuse them |
| High complexity | Methods grow too many branches and special cases | AI tends to satisfy edge cases by nesting more logic |
| Unused exports | Public functions or APIs are exposed without consumers | AI commonly exports more surface area than needed |
| Missing tests | Features are added without meaningful validation | Code generation often outpaces test generation |
| Inconsistent patterns | Error handling, naming, and structure drift across the codebase | Different sessions can produce different styles and abstractions |

---

## Tool selection by language

### TypeScript / Next.js / Angular

| Concern | Tool | How It Helps |
|---------|------|--------------|
| Dead code, unused exports, unused files | `knip` | Finds files, exports, and dependencies that are not actually used |
| Code duplication | `jscpd` | Detects copy-pasted blocks across the repository |
| Cyclomatic complexity | ESLint `complexity` rule | Flags functions with too many branches |
| Cognitive complexity | `eslint-plugin-sonarjs` | Highlights logic that is difficult to reason about |
| Type safety gaps | `tsc --noEmit`, `oxlint` | Strengthens correctness and static analysis |
| Naming consistency | `eslint-plugin-unicorn` | Helps enforce shared code conventions |

### Python

| Concern | Tool | How It Helps |
|---------|------|--------------|
| Dead code | `vulture` | Identifies likely unused Python functions, classes, and code paths |
| Unused imports and variables | `ruff` | Catches common cleanup issues quickly |
| Code duplication | `jscpd` | Finds duplicated blocks in Python code |
| Cyclomatic complexity | `radon` | Measures code complexity and helps define thresholds |
| Cognitive complexity | `ruff` rule `C901` | Flags functions that are too complex to maintain |
| Dependency hygiene | `deptry` | Compares imports against declared dependencies |
| Type checking | `pyright` or `mypy` | Improves confidence in refactors and generated code |

### C# / .NET

| Concern | Tool | How It Helps |
|---------|------|--------------|
| Dead code and unused members | Roslyn analyzers (`IDE0051`, `IDE0052`, `CS0219`) | Surfaces unused fields, variables, and private members |
| Commented-out code | `dead-csharp` | Detects stale commented code that should be deleted |
| Cyclomatic complexity and maintainability | .NET Code Metrics | Produces maintainability and complexity signals for review |
| Code duplication | `jscpd` | Detects repeated implementation patterns |
| Dependency hygiene | `dotnet-unused` | Finds package references that are no longer needed |
| Naming and style | `StyleCop.Analyzers` | Keeps generated code aligned with project standards |

### Cross-language

| Concern | Tool | How It Helps |
|---------|------|--------------|
| Cross-language duplication | `jscpd` | Detects duplicated logic across multiple languages |
| Complexity | `lizard` | Evaluates cyclomatic complexity across a mixed stack |
| Typos | `typos` | Finds spelling issues in source and docs |
| Documentation quality | `vale` | Helps maintain consistent writing quality |

---

## GitHub Actions pipeline

The pipeline should combine fast pull request checks with deeper scheduled scans. Pull request checks keep quality visible during review, while scheduled scans help catch slow-growing code health problems.

### Workflow 1: pull request quality gate

```yaml
name: Code Quality Gate

on:
  pull_request:
    branches: [main, develop]

jobs:
  knip-check:
    runs-on: ubuntu-latest
    if: hashFiles('package.json') != ''
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx knip --reporter json --no-exit-code > knip-report.json

  python-dead-code:
    runs-on: ubuntu-latest
    if: hashFiles('requirements.txt') != '' || hashFiles('pyproject.toml') != ''
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install vulture ruff deptry radon
      - run: vulture src/ --min-confidence 80
      - run: ruff check . --select F401,F841 --output-format github
      - run: deptry .

  duplication:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: |
          npx jscpd . \
            --min-tokens 50 \
            --reporters "json,consoleFull" \
            --ignore "node_modules,bin,obj,dist,.next,__pycache__"
```

### Workflow 2: scheduled deep scan

```yaml
name: Nightly Code Health

on:
  schedule:
    - cron: '0 2 * * 1-5'
  workflow_dispatch:

jobs:
  dead-code-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: |
          npx knip --reporter json > knip-full.json
          npx knip --reporter markdown > knip-full.md

  coverage-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx jest --coverage --coverageReporters json-summary

  bundle-audit:
    runs-on: ubuntu-latest
    if: hashFiles('next.config.*') != ''
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx next build
```

### Workflow 3: catch-all lint aggregation

```yaml
name: MegaLinter

on:
  pull_request:
    branches: [main]

jobs:
  megalinter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: oxsecurity/megalinter@v8
        env:
          VALIDATE_ALL_CODEBASE: false
          ENABLE_LINTERS: >-
            CSHARP_DOTNET_FORMAT,
            CSHARP_ROSLYNATOR,
            TYPESCRIPT_ES,
            PYTHON_RUFF,
            YAML_YAMLLINT,
            MARKDOWN_MARKDOWNLINT,
            SPELL_CSPELL,
            COPYPASTE_JSCPD
```

---

## Branch protection and repository settings

Quality checks only matter if they are enforced consistently.

Recommended branch protection settings:

- Require pull request reviews
- Require conversation resolution before merging
- Require passing status checks for quality gates
- Require linear history where it fits the team's workflow

Recommended status checks:

- `knip-check`
- `duplication`
- `python-dead-code`
- `dotnet-quality`
- `typos`
- `megalinter`

---

## GitHub-native features to pair with the pipeline

GitHub Actions should be complemented by the native capabilities already available in the platform:

- **Copilot code review** for additional review coverage on pull requests
- **Code scanning and dependency review** for security-focused analysis
- **Secret scanning** to reduce the risk of committed credentials
- **Dependabot** for dependency maintenance and update hygiene
- **Code quality features and repository rulesets** where available in your environment

These features do not replace language-specific analyzers, but they make the overall review loop stronger.

---

## What this pipeline catches beyond default checks

| Concern | Native Platform Coverage | Added Value From This Pipeline |
|---------|--------------------------|--------------------------------|
| Unused exported functions in TypeScript | Limited | `knip` catches cross-file dead exports |
| Unused files | Limited | `knip` identifies files not imported anywhere |
| Unused Python dependencies | Limited | `deptry` compares actual imports with declarations |
| Dead Python functions | Limited | `vulture` highlights unreachable or likely unused code |
| Commented-out C# code | Limited | `dead-csharp` finds stale commented implementations |
| Copy-pasted blocks | Limited | `jscpd` makes duplication visible and measurable |
| High complexity | Partial | `lizard`, ESLint, and `radon` provide clearer thresholds |
| Documentation and spelling drift | Partial | `vale` and `typos` keep content cleaner |

---

## Licensing and security notes

When selecting code quality tools for AI-heavy repositories, confirm the following before standardizing on them:

- The tools run locally in CI and do not transmit source code to external services
- Their licenses are acceptable for internal engineering use
- Their output is machine-readable so it can be surfaced in GitHub Actions summaries or artifacts
- Their versions can be pinned for reproducible builds

For the tools listed on this page, good operational practices include:

- Pin exact versions in workflow files when stability matters
- Prefer `npm ci` over `npm install` for deterministic Node.js installs
- Enable dependency review on workflow changes
- Keep analyzer configuration in version control alongside application code

---

## Suggested rollout path

1. Start with non-blocking warnings for dead code, duplication, and typos.
2. Add language-specific analyzers for the stacks you actively ship.
3. Convert high-signal checks into required status checks once teams trust the output.
4. Add scheduled deep scans, coverage reporting, and trend dashboards for ongoing maintenance.
5. Maintain explicit allowlists for intentionally unused APIs, plugin interfaces, or extension points.

---

## Go deeper

- [GitHub Actions](https://docs.github.com/en/actions) — the runner, the cache and the permissions model this pipeline depends on.
- [Ruff](https://docs.astral.sh/ruff/) — the Python linter fast enough to run on every save, not just in CI.
- [Knip](https://knip.dev/) — dead files, exports and dependencies in TypeScript. The check that catches what an assistant left behind.
- [Vulture](https://github.com/jendrikseipp/vulture) — the Python equivalent, with a confidence score you should tune before trusting.
- [jscpd](https://github.com/kucherenko/jscpd) — copy-paste detection. Generated code duplicates more than hand-written code does.
- [Lizard](https://github.com/terryyin/lizard) — cyclomatic complexity across a dozen languages, which is the cheapest proxy for "this needs review".
- [Deptry](https://deptry.com/) — dependency drift: declared but unused, used but undeclared.
