#!/usr/bin/env python3
"""Render every diagram page in BOTH colour schemes and check two things:

1. The light theme is actually reachable. A script in overrides/main.html used
   to force slate on every page load by reading a localStorage key Material
   never writes, so clicking the light toggle worked until you navigated and
   then snapped back. Nothing in a --strict build catches that.
2. Diagram label text has enough contrast against the shape it sits on, in both
   schemes. White-on-teal is fine; white-on-white is the failure this catches.

    mkdocs build -d /tmp/site
    (cd /tmp/site && python3 -m http.server 8899 &)
    python3 planning/scripts/check-themes.py

Needs playwright with chromium. Exit 1 on any failure.
"""
import asyncio, glob, os, sys
from playwright.async_api import async_playwright

BASE = os.environ.get("SITE_BASE", "http://localhost:8899")
MIN_CONTRAST = 3.0


def diagram_pages():
    out = []
    for f in sorted(glob.glob("docs/**/*.md", recursive=True)):
        if "```mermaid" in open(f, encoding="utf-8").read():
            rel = f[len("docs/"):-len(".md")]
            rel = rel[:-len("index")] if rel.endswith("index") else rel + "/"
            out.append(f"{BASE}/{rel}")
    return out


PROBE = """() => {
  const lum = c => {
    const m = (c||'').match(/[\\d.]+/g); if (!m) return null;
    const [r,g,b] = m.slice(0,3).map(Number);
    const f = v => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b);
  };
  const out = [];
  document.querySelectorAll('div.mermaid svg').forEach(svg => {
    const pageBg = getComputedStyle(document.body).backgroundColor;
    svg.querySelectorAll('text, span.nodeLabel, span.edgeLabel').forEach(t => {
      const txt = (t.textContent||'').trim();
      if (!txt) return;
      const fg = getComputedStyle(t).color;
      let bg = '';
      // Walk out to the real node/cluster group, never stopping at the
      // foreignObject: its first rect is the label's own background, which is
      // near-white in every theme and would fake a white-on-white failure.
      const holder = t.closest('g.node, g.cluster') || t.closest('g.edgeLabel');
      if (holder) {
        const shape = holder.querySelector(':scope > path, :scope > rect, :scope > polygon, '
                                         + ':scope > circle, :scope > ellipse, '
                                         + ':scope > g > path, :scope > g > rect, '
                                         + ':scope > g > polygon');
        if (shape) bg = getComputedStyle(shape).fill;
      }
      if (!bg || bg === 'none' || bg.includes('rgba(0, 0, 0, 0)')) bg = pageBg;
      const l1 = lum(fg), l2 = lum(bg);
      if (l1 === null || l2 === null) return;
      const ratio = (Math.max(l1,l2) + 0.05) / (Math.min(l1,l2) + 0.05);
      out.push({txt: txt.slice(0,40), fg, bg, ratio: Math.round(ratio*100)/100});
    });
  });
  return out;
}"""


async def main():
    urls = diagram_pages()
    failures = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for scheme, toggle in (("slate", False), ("default", True)):
            pg = await b.new_page(viewport={"width": 1400, "height": 1100})
            await pg.goto(BASE + "/", wait_until="networkidle")
            if toggle:
                await pg.click("label[for='__palette_1']")
                await pg.wait_for_timeout(600)
            for u in urls:
                await pg.goto(u, wait_until="networkidle")
                await pg.wait_for_timeout(1800)
                actual = await pg.evaluate("document.body.getAttribute('data-md-color-scheme')")
                if actual != scheme:
                    failures.append(f"{u}: expected scheme {scheme}, got {actual} "
                                    f"(is something forcing the palette on load?)")
                    continue
                blocks = await pg.evaluate("document.querySelectorAll('div.mermaid').length")
                svgs = await pg.evaluate("document.querySelectorAll('div.mermaid svg').length")
                if svgs < blocks:
                    failures.append(f"{u} [{scheme}]: {blocks} diagram(s), {svgs} rendered")
                for r in await pg.evaluate(PROBE):
                    if r["ratio"] < MIN_CONTRAST:
                        failures.append(f"{u} [{scheme}]: contrast {r['ratio']} "
                                        f"text={r['txt']!r} fg={r['fg']} bg={r['bg']}")
            await pg.close()
        await b.close()
    print(f"checked {len(urls)} diagram pages in 2 schemes")
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures[:40]: print("  ", f)
    else:
        print("light and dark both render, all label contrast >= %.1f:1" % MIN_CONTRAST)
    return 1 if failures else 0

sys.exit(asyncio.run(main()))
