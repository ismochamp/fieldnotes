# Verification results — 28 September 2026

## Standalone runtime

`python3 test_app.py`: **5 tests passed** using an isolated HTTP server.

- All eight article pages contain their own title, three original sections and a practical checklist.
- Full-text query `idempotency` finds the retry policy article by body content.
- WordPress topic returns two resources; incompatible query/topic combination returns none.
- Empty result guidance appears and search input containing markup is HTML-escaped.
- Saved view is configured, bookmark script is served, missing article returns 404.

## Actual WordPress runtime

Official WordPress image, PHP 8.3 image family, WordPress **7.1.2**, MariaDB image. Images pinned by digest in `compose.yaml`.

`python3 test_wordpress.py`: **7 integration checks passed**.

- Active original theme lists eight imported resources.
- WordPress full-text search finds a term inside the article body.
- Metadata topic filter returns two WordPress resources.
- No-match state gives a useful recovery path.
- Real article permalink renders full content.
- Registered content type exposes eight published resources through WordPress REST API.
- Saved-list route uses the bookmark view.

## Limits

Automated HTTP checks do not execute browser JavaScript, so localStorage persistence and visual/mobile behavior need browser interaction. Root port assembly performs that browser check and screenshots separately. No audience, SEO, formal accessibility, load or public-deployment results are claimed.

## Additional browser verification

Browser capture verified actual WordPress pages. The library bookmark action produced a saved list containing the selected article; the service form stored a labeled verification inquiry and showed a success confirmation. Each relevant action was checked on its own site. Both WordPress sites were inspected at a 390-pixel viewport with document width also 390 pixels. Screenshots are in `screenshots/`.
