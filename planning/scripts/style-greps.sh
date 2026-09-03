#!/usr/bin/env bash
# Phase 3 and 5 done-checks. All counts should be 0 when the phase is complete.
cd "$(dirname "$0")/../.."
echo -n "double-hyphen dashes in prose:    "; grep -rn ' -- ' docs --include=*.md | wc -l
echo -n "foreign mermaid hex values:       "; grep -rniE '#057398|#00A0DF|#004987|#38bdf8|#632C4F|#853175|#9e57a2|#259638' docs | wc -l
echo -n "\\n inside mermaid labels:         "; grep -rn '\\n' docs --include=*.md | wc -l
echo -n "org-internal voice:               "; grep -rniE "\\bour organization|in the organization|\\bour stack|what we use in \\bour|we invest in|co-op|reach out to the team|\\bour enterprise|everyone in the organization" docs | wc -l
echo -n "unicode emojis:                   "; grep -rnP --include=*.md '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' docs | wc -l
echo -n "bare '## References' sections:    "; grep -rl '^## References' docs | wc -l
echo -n "Title Case H2s (approx):          "; grep -rhE '^## [A-Z][a-z]+ [A-Z][a-z]' docs | wc -l
echo -n "pages without a level tag:        "; for f in $(find docs -name '*.md'); do grep -qE '^\s+- (Start here|Understand|Build|Go deeper|Tools|Reference)$' "$f" || echo "$f"; done | wc -l
echo -n "'eleven' module claims:           "; grep -rni 'eleven' docs | wc -l
