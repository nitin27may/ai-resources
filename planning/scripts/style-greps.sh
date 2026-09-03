#!/usr/bin/env bash
# Phase 3 and 5 done-checks. Every count should be 0 when those phases are complete.
# Fence-aware: Mermaid edge labels (`A -- Yes --> B`) and code blocks are not prose,
# so they are excluded rather than counted as style violations.
cd "$(dirname "$0")/../.."
python3 - <<'PY'
import glob, re

def prose_lines():
    for p in sorted(glob.glob("docs/**/*.md", recursive=True)):
        fence = False
        for i, l in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            if l.lstrip().startswith("```"):
                fence = not fence; continue
            if not fence: yield p, i, l

def mermaid_lines():
    for p in sorted(glob.glob("docs/**/*.md", recursive=True)):
        inm = False
        for i, l in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            st = l.strip()
            if st.startswith("```mermaid"): inm = True; continue
            if st.startswith("```"): inm = False; continue
            if inm: yield p, i, l

# House palette (CLAUDE.md). #0f766e replaced #14b8a6 for fills that carry
# white label text: #14b8a6 measures 2.49:1, below the 3:1 bar. #14b8a6 stays
# valid as a stroke, where no text sits on it.
APPROVED = {"#0d9488","#0b7a72","#16a34a","#15803d","#0284c7","#0270a8",
            "#d97706","#b86005","#0f766e","#14b8a6","#119b91","#dc2626","#b91c1c",
            "#ffffff","#fff","#121212","#374151","#555659","#3d3d40"}
PROPER = ("Claude","GraphRAG","GitHub","Azure","Microsoft","OpenAI","Google","Copilot",
           "RAG","MCP","AI","LLM","Anthropic","Meta","Naive","Semantic","Agent","Foundry",
           "Kernel","GenAI","Code","Skills","Actions","Framework","Search","Studio")
ORG = re.compile(r"\bour organization|in the organization|\bour stack|what we use in \bour|"
                 r"we invest in|co-op|reach out to the team|\bour enterprise|"
                 r"everyone in the organization", re.I)

checks = {
 "double-hyphen dashes in prose": sum(l.count(" -- ") for _,_,l in prose_lines()),
 "non-palette mermaid colours":   sum(1 for _,_,l in mermaid_lines()
                                      for c in re.findall(r"#[0-9a-fA-F]{3,6}", l)
                                      if c.lower() not in APPROVED),
 "styled nodes missing color:#fff": sum(1 for _,_,l in mermaid_lines()
                                        if re.search(r"(fill:#|style \w+ fill)", l)
                                        and "color:#" not in l),
 "\\n inside mermaid labels":     sum(l.count("\\n") for _,_,l in mermaid_lines()),
 "org-internal voice":            sum(1 for _,_,l in prose_lines() if ORG.search(l)),
 "unicode emojis":                sum(1 for _,_,l in prose_lines()
                                      if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", l)),
 "bare '## References' sections": sum(1 for _,_,l in prose_lines() if l.strip() == "## References"),
 "Title Case admonition titles": sum(1 for _,_,l in prose_lines()
                                      if (m := re.match(r'^\s*(?:!!!|\?\?\?\+?)\s+\w+\s+"([A-Z][a-z]+ [A-Z][a-z][^"]*)"', l))
                                      and m.group(1).split()[1] not in PROPER),
 "Title Case H2s":                sum(1 for _,_,l in prose_lines()
                                      if re.match(r"^## [A-Z][a-z]+ [A-Z][a-z]", l)
                                      and l.split()[2] not in PROPER),
 "'eleven' module claims":        sum(1 for _,_,l in prose_lines() if re.search(r"\beleven\b", l, re.I)),
}
for k, v in checks.items(): print(f"{k:34s} {v}")
untagged = [p for p in glob.glob("docs/**/*.md", recursive=True)
            if not re.search(r"(?m)^\s+- (Start here|Understand|Build|Go deeper|Tools|Reference)$",
                             open(p, encoding="utf-8").read())]
print(f"{'pages without a level tag':34s} {len(untagged)}")
for p in untagged: print("   ", p)
PY
