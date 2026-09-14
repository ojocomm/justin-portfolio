#!/usr/bin/env python3
"""Assemble case pages from homepage-v1-template.html (header/footer) + <case>-case-main.html."""
import re, hashlib, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
CASES = {
    'about-2-1-1.html': dict(
        main='ambiance-case-main.html',
        title='Ambiance Zonwering — Justin Norman',
        canonical='https://www.justinnorman.nl/about-2-1-1',
        body='page-case page-case-ambiance'),
    'winning-proposal.html': dict(
        main='winning-proposal-case-main.html',
        title='Winning Proposal — Justin Norman',
        canonical='https://www.justinnorman.nl/winning-proposal',
        body='page-case page-case-wp'),
    'hoppenbrouwers.html': dict(
        main='hoppenbrouwers-case-main.html',
        title='Hoppenbrouwers Energy Manager — Justin Norman',
        canonical='https://www.justinnorman.nl/hoppenbrouwers',
        body='page-case page-case-hoppenbrouwers'),
    'etz.html': dict(
        main='etz-case-main.html',
        title='ETZ Voeding- en Medicatie-app — Justin Norman',
        canonical='https://www.justinnorman.nl/etz',
        body='page-case page-case-etz'),
    'portfolio.html': dict(
        main='portfolio-main.html',
        title='Portfolio — Justin Norman',
        canonical='https://www.justinnorman.nl/portfolio',
        body='page-portfolio'),
}
idx = open(f'{ROOT}/homepage-v1-template.html').read()
header = idx[idx.index('<header'):idx.index('<main')]
footer = open(f'{ROOT}/footer-v2.html').read()
_sym = re.search(r'<svg[^>]*data-usage="social-icons-svg".*?</svg>', idx, re.S)
footer += _sym.group(0) if _sym else ''
v = lambda p: hashlib.sha1(open(f'{SITE}/{p}', 'rb').read()).hexdigest()[:8]
for out_name, cfg in CASES.items():
    main = open(f"{ROOT}/{cfg['main']}").read().replace('<!--CARDS-->', open(f'{ROOT}/cards.html').read())
    head = idx[:idx.index('</head>')]
    head = head.replace('<title>Justin Norman</title>', f"<title>{cfg['title']}</title>")
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{cfg["canonical"]}">', head)
    head = re.sub(r'<link rel="stylesheet" href="assets/css/pages.css[^"]*">',
                  lambda m: m.group(0) + '\n  <link rel="stylesheet" href="assets/css/home-v2.css?v=%s">\n  <link rel="stylesheet" href="assets/css/case.css?v=%s">' % (v('assets/css/home-v2.css'), v('assets/css/case.css')), head)
    out = head + f'</head>\n<body class="{cfg["body"]}">\n' + header + main + '\n' + footer + \
          '<script src="assets/js/main.js?v=%s" defer></script>\n</body>\n</html>\n' % v('assets/js/main.js')
    out = out.replace('header-nav-item header-nav-item--active', 'header-nav-item').replace(' aria-current="page"', '')
    open(f'{SITE}/{out_name}', 'w').write(out)
    print(out_name, len(out))
