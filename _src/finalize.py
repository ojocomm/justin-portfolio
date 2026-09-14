#!/usr/bin/env python3
"""Cache-busting via bestandsnaam: kopieer assets naar naam.<hash>.ext en herschrijf alle HTML-verwijzingen."""
import hashlib, re, glob, os, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
ASSETS = ['assets/css/main.css', 'assets/css/home-v2.css', 'assets/css/case.css',
          'assets/css/pages.css', 'assets/js/main.js']
mapping = {}
for rel in ASSETS:
    full = f'{SITE}/{rel}'
    h = hashlib.sha1(open(full, 'rb').read()).hexdigest()[:8]
    d, base = os.path.split(rel)
    stem, ext = base.rsplit('.', 1)
    for old in glob.glob(f'{SITE}/{d}/{stem}.????????.{ext}'):
        os.remove(old)
    hashed = f'{d}/{stem}.{h}.{ext}'
    shutil.copy(full, f'{SITE}/{hashed}')
    mapping[rel] = (re.compile(rf'{re.escape(d)}/{stem}(?:\.[0-9a-f]{{8}})?\.{ext}(?:\?v=[0-9a-f]+)?'), hashed)
n = 0
for f in glob.glob(f'{SITE}/*.html'):
    s = open(f).read(); t = s
    for pat, hashed in mapping.values():
        t = pat.sub(hashed, t)
    if t != s:
        open(f, 'w').write(t); n += 1
print('herschreven:', n, '|', ' '.join(v[1].split('/')[-1] for v in mapping.values()))
