#!/usr/bin/env python3
"""Prüft, dass HKF-Base-V1.0.md §3 und das Bundle dasselbe sagen.

Die elf Typdefinitionen stehen zweimal: als eingebetteter Markdown-Block in
der Spezifikation und als ausgelieferte Datei im Bundle-Repository. Die
Spezifikation ist die normative Fassung; das Bundle muss ihr entsprechen.

Das Bundle wird als Geschwisterverzeichnis erwartet, weil es ein eigenes
Repository ist:

    HKF/
      HenniHKF-Spec/   <- hier
      HenniHKF-Base/   <- geprüft

    python3 tools/check-base.py [pfad-zum-bundle]
"""
import os, re, sys, difflib

TYPEN = 11          # §3 der Spezifikation

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, os.pardir, "HenniHKF-Base")
BLOCK = re.compile(r"^## 3\.\d+ `(\w+)`\n\n```markdown\n(.*?)\n```", re.S | re.M)
# created/modified/modified_by führt nur die Datei, nicht die Spezifikation
STAMP = re.compile(r"^(created|modified|modified_by):.*\n", re.M)

if not os.path.isdir(os.path.join(BUNDLE, "typedefs")):
    sys.exit("Bundle nicht gefunden: %s\n%s" % (os.path.abspath(BUNDLE), __doc__))

spec = open(os.path.join(HERE, "HKF-Base-V1.0.md"), encoding="utf-8").read()
blocks = BLOCK.findall(spec)
if len(blocks) != TYPEN:
    sys.exit("§3 enthält %d Typdefinitionen, erwartet %d" % (len(blocks), TYPEN))

bad = 0
for typ, block in blocks:
    p = os.path.join(BUNDLE, "typedefs", typ + ".md")
    if not os.path.exists(p):
        print("%-14s fehlt im Bundle" % typ); bad += 1; continue
    a = block.strip().splitlines()
    b = STAMP.sub("", open(p, encoding="utf-8").read()).strip().splitlines()
    if a == b:
        print("%-14s ok" % typ)
    else:
        bad += 1
        print("%-14s WEICHT AB (- Spezifikation, + Bundle)" % typ)
        for l in difflib.unified_diff(a, b, lineterm="", n=0):
            if l[:2] not in ("--", "++"):
                print("    ", l)

extra = sorted(set(n[:-3] for n in os.listdir(os.path.join(BUNDLE, "typedefs"))
                   if n.endswith(".md")) - set(t for t, _ in blocks))
if extra:
    bad += len(extra)
    print("nicht in §3 beschrieben:", ", ".join(extra))

print("\n%d von %d Typdefinitionen weichen ab" % (bad, TYPEN))
sys.exit(1 if bad else 0)
