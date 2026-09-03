#!/usr/bin/env python3
"""Render every page containing a Mermaid diagram in a headless browser and
assert an SVG actually appeared.

A MkDocs build passing --strict says nothing about whether a diagram rendered:
Material shipped empty diagrams on this site for months without a single
warning. This is the check that catches that class of failure.

    mkdocs build -d /tmp/site
    (cd /tmp/site && python3 -m http.server 8899 &)
    python3 planning/scripts/check-diagrams.py

Needs playwright with chromium. Exits non-zero if any page renders no SVG.
"""
import asyncio, sys
from playwright.async_api import async_playwright

import glob, os, subprocess
BASE = os.environ.get("SITE_BASE", "http://localhost:8899")
def diagram_pages():
    out = []
    for f in sorted(glob.glob("docs/**/*.md", recursive=True)):
        if "```mermaid" in open(f, encoding="utf-8").read():
            rel = f[len("docs/"):-len(".md")]
            rel = rel[:-len("index")] if rel.endswith("index") else rel + "/"
            out.append(f"{BASE}/{rel}")
    return out
urls = diagram_pages()

async def main():
    bad = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width":1280,"height":900})
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        for u in urls:
            errs.clear()
            await pg.goto(u, wait_until="networkidle")
            await pg.wait_for_timeout(1200)
            n_pre = await pg.evaluate("document.querySelectorAll('pre.mermaid, .mermaid').length")
            n_svg = await pg.evaluate("document.querySelectorAll('.mermaid svg, svg[id^=mermaid]').length")
            err_txt = await pg.evaluate("!!document.querySelector('.mermaid [id^=flowchart] text, .error-text') && document.body.innerText.includes('Syntax error')")
            name = u.rstrip('/').split('/')[-1] or 'home'
            
            status = "ok" if n_svg >= 1 and not err_txt else "PROBLEM"
            if status != "ok": bad.append((u, n_pre, n_svg, errs[:2]))
            print(f"{status:8s} svg={n_svg:2d} blocks={n_pre:2d}  {u}")
        await b.close()
    print("\nPAGES WITH RENDER PROBLEMS:", len(bad))
    for x in bad: print("  ", x)
asyncio.run(main())
