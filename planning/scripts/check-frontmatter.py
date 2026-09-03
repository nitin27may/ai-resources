import glob, re, sys, yaml
bad = []
for p in sorted(glob.glob("docs/**/*.md", recursive=True)):
    s = open(p, encoding="utf-8").read()
    if not s.startswith("---\n"):
        bad.append((p, "no front matter")); continue
    try:
        fm = s[4:s.index("\n---\n", 3)]
    except ValueError:
        bad.append((p, "unterminated front matter")); continue
    try:
        d = yaml.safe_load(fm)
    except Exception as e:
        bad.append((p, f"YAML error: {str(e).splitlines()[0]}")); continue
    if not isinstance(d, dict):
        bad.append((p, "front matter is not a mapping")); continue
    if d.get("description") is not None and not isinstance(d["description"], str):
        bad.append((p, "description is not a string (unquoted colon?)"))
    t = d.get("tags")
    if t is not None and (not isinstance(t, list) or not all(isinstance(x, str) for x in t)):
        bad.append((p, "tags is not a list of strings"))
print(f"front matter: {len(glob.glob('docs/**/*.md', recursive=True))} pages checked, {len(bad)} broken")
for p, why in bad: print("  ", p, "->", why)
sys.exit(1 if bad else 0)
