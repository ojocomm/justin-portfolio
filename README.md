# justinnorman.nl — statische portfolio-site

Statische kopie (HTML, CSS, JavaScript en afbeeldingen) van de portfolio-website van Justin Norman,
nagebouwd vanaf de Squarespace-versie op www.justinnorman.nl. Geen build-stap of framework nodig:
de map kan direct op elke webserver of op GitHub Pages worden geplaatst.

## Pagina's

| Bestand            | Pagina                                | Oude Squarespace-URL |
|--------------------|---------------------------------------|----------------------|
| `index.html`       | Home                                  | `/`                  |
| `about.html`       | About                                 | `/about`             |
| `home-1-2.html`    | Portfolio (overzicht cases)           | `/home-1-2`          |
| `contact.html`     | Contact (met formulier)               | `/contact`           |
| `about-2.html`     | Case: Hoppenbrouwers Energy Manager   | `/about-2`           |
| `about-2-1-1.html` | Case: Ambiance Zonwering              | `/about-2-1-1`       |
| `etz.html`         | Case: ETZ Voeding- & Medicatie        | `/etz`               |
| `404.html`         | Niet-gevonden-pagina                  |                      |

## Structuur

```
assets/css/main.css   ontwerp: kleuren, typografie (Epilogue), header, menu, knoppen, formulier
assets/css/pages.css  per pagina de rasterindeling (24-koloms fluid grid) en blokinstellingen
assets/js/main.js     vaste header, mobiel menu, scroll-animaties, contactformulier
assets/img/           alle afbeeldingen (2500px breed geëxporteerd)
assets/fonts/         Epilogue en Poppins (woff2, SIL Open Font License)
```

## Contactformulier

Een statische site heeft geen server om formulieren te verwerken. Het formulier opent daarom het
e-mailprogramma van de bezoeker met het ingevulde bericht aan `info@justinnorman.nl`. Wil je echte
verzending zonder e-mailprogramma, koppel dan een formulierdienst (bijv. Formspree of Netlify Forms)
in `assets/js/main.js`.

## Publiceren

- **GitHub Pages**: Settings → Pages → branch `main`, map `/ (root)`.
- **Eigen hosting (bijv. SiteGround)**: upload de volledige inhoud van deze map naar `public_html`.

Op een gewone webserver werken ook de "schone" URL's (`/about` → `about.html`) als de server
`MultiViews` of een vergelijkbare rewrite-regel heeft; een `.htaccess` hiervoor staat meegeleverd.
