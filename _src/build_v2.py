#!/usr/bin/env python3
"""Assemble site/index.html + site/home-v2.html from homepage-v1-template.html + home-v2-main.html + cards.html + footer-v2.html."""
import re, hashlib, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
idx = open(f'{ROOT}/homepage-v1-template.html').read()
header = idx[idx.index('<header'):idx.index('<main')]
footer = open(f'{ROOT}/footer-v2.html').read()
_sym = re.search(r'<svg[^>]*data-usage="social-icons-svg".*?</svg>', idx, re.S)
footer += _sym.group(0) if _sym else ''
v = lambda p: hashlib.sha1(open(f'{SITE}/{p}', 'rb').read()).hexdigest()[:8]
main = open(f'{ROOT}/home-v2-main.html').read().replace('<!--CARDS-->', open(f'{ROOT}/cards.html').read())
head = idx[:idx.index('</head>')]
head = head.replace('<title>Justin Norman</title>', '<title>Justin Norman — Senior Product Designer</title>')
head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://www.justinnorman.nl">', head)
head = re.sub(r'<link rel="stylesheet" href="assets/css/pages.css[^"]*">',
              lambda m: m.group(0) + '\n  <link rel="stylesheet" href="assets/css/home-v2.css?v=%s">' % v('assets/css/home-v2.css'), head)
out = head + '</head>\n<body class="page-home-v2">\n' + header + main + '\n' + footer + \
      '<script src="assets/js/main.js?v=%s" defer></script>\n</body>\n</html>\n' % v('assets/js/main.js')
for name in ('index.html', 'home-v2.html'):
    open(f'{SITE}/{name}', 'w').write(out)
    print(name, len(out))
