# CV — Timur Kryvasheyev

Source of the CV site published at <https://timurkry.github.io/cv/> and of the PDF
versions linked from it.

## How it works

All content lives in **one** file — [`src/cv.data.json`](src/cv.data.json). Everything
else is generated from it:

| Output | What it is |
| --- | --- |
| `index.html` | the site (single file, styles inlined, no dependencies) |
| `cv-fullstack-developer.pdf` | CV, full-stack focus (EN) |
| `cv-frontend-developer.pdf` | CV, frontend focus (EN) |
| `cv-fullstack-developer-de.pdf` | Lebenslauf, full-stack (DE) |
| `og.png` | 1200×630 link-preview card |

Facts that appear in more than one document (contact details, periods, the number of
freelance client sites) are defined once in the `facts` block and referenced as
`{{token}}`. An unknown token fails the build instead of rendering empty — so the
site and the PDFs cannot drift apart the way they previously did.

## Rebuild

```sh
node src/build.mjs
```

Requires Node ≥ 18 and Chromium (used headless to print the PDFs and shoot the OG
card). The build looks for Chromium in the usual locations; override with
`CHROME_PATH=/path/to/chrome node src/build.mjs`.

Generated files are committed on purpose: GitHub Pages serves them directly, and the
PDF URLs are already in circulation, so their filenames must stay stable.

## Layout

```
src/cv.data.json        all content and facts
src/build.mjs           build script (no dependencies)
src/site.template.mjs   site markup + meta tags, JSON-LD, favicon
src/print.template.mjs  print markup for the PDF variants
src/og.template.mjs     link-preview card
src/site.css            site styles, inlined into index.html
src/print.css           A4 print styles
build/                  intermediate HTML, not committed
```

Fields named `about`, `intro`, `bullets`, `note` and `focus` may contain inline
`<strong>`; everything else is HTML-escaped at render time.

## Notes

- The PDFs are role-targeted application documents and carry a "Mid-Level" title; the
  site headline deliberately omits it to stay open to a wider range of roles.
- The "last updated" date in the footer is stamped at build time — nothing to bump by
  hand.
