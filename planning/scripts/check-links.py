#!/usr/bin/env python3
"""Internal link check, inbound-link floor, header-block count, optional external sweep.

Usage:  python3 planning/scripts/check-links.py [--external] [--min-inbound N]
Exit 1 on any broken internal link or anchor, or (after Phase 4) any page below the inbound floor.
"""
import glob, os, re, sys, subprocess
from concurrent.futures import ThreadPoolExecutor

DOCS = "docs"
pages = sorted(glob.glob(f"{DOCS}/**/*.md", recursive=True))
rel = {p[len(DOCS)+1:] for p in pages}

def anchors(path):
    ids = set()
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^#{1,6}\s+(.*?)\s*(\{#([\w-]+)\})?\s*$", line)
        if not m: continue
        if m.group(3): ids.add(m.group(3)); continue
        text = re.sub(r":[\w-]+:", "", m.group(1))       # strip material icons
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        ids.add(re.sub(r"[\s]+", "-", text))
    return ids

ANCH = {p[len(DOCS)+1:]: anchors(p) for p in pages}
broken, inbound, external, headers = [], {r: 0 for r in rel}, set(), 0
for p in pages:
    src = p[len(DOCS)+1:]
    txt = open(p, encoding="utf-8").read()
    h1 = re.search(r"(?m)^#\s+.*$", txt)
    if h1 and txt[h1.end():].lstrip("\n").startswith('!!! abstract "') and re.match(
            r'!!! abstract "(Start here|Understand|Build|Go deeper|Tools|Reference) ·',
            txt[h1.end():].lstrip("\n")): headers += 1
    for m in re.finditer(r"\]\(([^)\s]+?)(#[^)\s]*)?\)", txt):
        t, frag = m.group(1), m.group(2)
        if t.startswith(("http://", "https://")): external.add(t.rstrip(".,;:")); continue
        if t.startswith("mailto:"): continue
        if t.endswith(".md"):
            tgt = os.path.normpath(os.path.join(os.path.dirname(src), t))
            if tgt not in rel: broken.append((src, t)); continue
            if tgt != src: inbound[tgt] += 1
            if frag and frag[1:] not in ANCH[tgt]: broken.append((src, t + frag + "  (anchor)"))
        elif t.startswith("#"):
            pass
        elif frag is None and t.startswith("#") is False and not os.path.exists(os.path.join(DOCS, os.path.dirname(src), t)):
            broken.append((src, t))
    for m in re.finditer(r"\]\((#[^)\s]+)\)", txt):
        if m.group(1)[1:] not in ANCH[src]: broken.append((src, m.group(1) + "  (in-page anchor)"))

print(f"pages: {len(pages)}   header blocks: {headers}   unique external URLs: {len(external)}")
if broken:
    print("BROKEN:"); [print(f"  {s} -> {t}") for s, t in broken]
floor = int(sys.argv[sys.argv.index("--min-inbound")+1]) if "--min-inbound" in sys.argv else 0
low = [(r, c) for r, c in sorted(inbound.items(), key=lambda x: x[1]) if c < floor and r != "index.md"]
if low:
    print(f"BELOW INBOUND FLOOR ({floor}):"); [print(f"  {c:3d} {r}") for r, c in low]

if "--external" in sys.argv:
    def hit(u):
        try:
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "--max-time", "20", "-A", "Mozilla/5.0 (X11; Linux x86_64) Chrome/128", "-w", "%{http_code} %{url_effective}", u], capture_output=True, text=True, timeout=30)
            return r.stdout.strip() + " <- " + u
        except Exception as e:
            return f"000 {e} <- {u}"
    skip = ("127.0.0.1", "localhost", "example.com", "api.openai.com/v1")
    urls = sorted(u for u in external if not any(s in u for s in skip))
    with ThreadPoolExecutor(8) as ex: res = sorted(ex.map(hit, urls))
    bad = [r for r in res if not r.startswith("200")]
    print(f"external: {len(urls)} checked, {len(bad)} non-200"); [print("  " + b) for b in bad]

sys.exit(1 if broken or low else 0)
