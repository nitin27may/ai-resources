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
 # A styled node must carry white label text. This catches both the missing
 # case and the wrong case: three subgraph styles carried color:#121212 on a
 # dark teal fill, invisible in dark mode, and the rendered-contrast check did
 # not see them because subgraph labels sit outside g.node.
 "styled nodes without color:#fff": sum(1 for _,_,l in mermaid_lines()
                                        if re.search(r"fill:#[0-9a-fA-F]{3,6}", l)
                                        and not re.search(r"color:#(fff|ffffff)\b", l, re.I)),
 "\\n inside mermaid labels":     sum(l.count("\\n") for _,_,l in mermaid_lines()),
 "org-internal voice":            sum(1 for _,_,l in prose_lines() if ORG.search(l)),
 "unicode emojis":                sum(1 for _,_,l in prose_lines()
                                      if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", l)),
 "bare '## References' sections": sum(1 for _,_,l in prose_lines() if l.strip() == "## References"),
 "headings ending in a colon": sum(1 for _,_,l in prose_lines()
                                      if re.match(r"^#{2,6} .*:\s*$", l)),
 "site name lower-cased": sum(1 for _,_,l in prose_lines()
                                      if "AI knowledge hub" in l),
 "numbered headings lowercased": sum(1 for _,_,l in prose_lines()
                                      if re.match(r"^#{2,6} [0-9]+[.)] [a-z]", l)),
 "Title Case admonition titles": sum(1 for _,_,l in prose_lines()
                                      if (m := re.match(r'^\s*(?:!!!|\?\?\?\+?)\s+\w+\s+"([A-Z][a-z]+ [A-Z][a-z][^"]*)"', l))
                                      and m.group(1).split()[1] not in PROPER),
 "Title Case H2s":                sum(1 for _,_,l in prose_lines()
                                      if re.match(r"^## [A-Z][a-z]+ [A-Z][a-z]", l)
                                      and l.split()[2] not in PROPER),
 # The build path has eleven modules (0-10). Guard against the previous count
 # reappearing, which is how the last miscount survived for months.
 # whats-new is a changelog: its August entry correctly records that ten
 # modules shipped then. Everywhere else, "ten modules" is now stale.
 "stale 'ten modules' claims":    sum(1 for f,_,l in prose_lines()
                                      if re.search(r"\bten modules\b", l, re.I)
                                      and "whats-new" not in f),
}
for k, v in checks.items(): print(f"{k:34s} {v}")
untagged = [p for p in glob.glob("docs/**/*.md", recursive=True)
            if not re.search(r"(?m)^\s+- (Start here|Understand|Build|Go deeper|Tools|Reference)$",
                             open(p, encoding="utf-8").read())]
print(f"{'pages without a level tag':34s} {len(untagged)}")
for p in untagged: print("   ", p)
PY
