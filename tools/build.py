#!/usr/bin/env python3
"""Build per-prospect site variants. Bespoke sections marked with
data-for="CODE" are stripped from the base build and each appears only
in its own CODE.html. Usage: python3 tools/build.py PASSWORD"""
import re, sys, subprocess, tempfile, os
pw = sys.argv[1]
src = open('index.src.html').read()
pat = re.compile(r'<section class="bespoke[^"]*"[^>]*data-for="(\w+)"[^>]*>.*?</section>\n?', re.S)
sections = {m.group(1): m.group(0) for m in pat.finditer(src)}
def encrypt(text, out):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, dir='.') as f:
        f.write(text); tmp = f.name
    subprocess.run(['python3', 'tools/encrypt.py', pw, tmp, out], check=True)
    os.unlink(tmp)
base = pat.sub('', src)
encrypt(base, 'index.html')
for code, block in sections.items():
    variant = src
    for other, oblock in sections.items():
        if other != code:
            variant = variant.replace(oblock, '')
    encrypt(variant, code + '.html')
    print('built', code + '.html')
print('built index.html (no bespoke content), prospects:', ', '.join(sections) or 'none')
