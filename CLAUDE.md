# CLAUDE.md

Personal academic website (https://larsoner.com) built with Pelican.

## Branches

- `source`: everything you edit lives here.
- `master`: generated HTML served by GitHub Pages. Never edit or commit to it by
  hand; `ghp-import` replaces its whole tree on each deploy.

Pushing to `source` triggers `.github/workflows/deploy.yml`, which runs
`make github` (build with `publishconf.py`, `ghp-import` to `master`, push). So a
push to `source` publishes the live site; don't push without being asked.

## Build and preview

```bash
pip install -r requirements.txt
make html    # build into output/ (gitignored)
make serve   # http://localhost:8000
```

A clean `make html` is the test: `pelicanconf.py` asserts that the BibTeX parses
and every entry has a date.

## Where content lives

- `pelicanconf.py`: most of the landing page is data here, not Markdown.
  `SOFTWARE`, `SOFTWARE_MORE`, `TIMELINE` (logos come from `content/images/`),
  `SOCIAL`, plus the BibTeX-to-HTML formatting (`make_nice_author`, `make_venue`,
  etc.).
- `data/larsoner.bib`: publication list, exported from Zotero. Authors must be
  full "Surname, Given and ..." records; `annote`, `owner`, `group`, and `topic`
  fields are stripped. Entries are sorted by `date`/`year` ("in press" sorts
  first).
- `content/pages/shortbio.md`: the bio text.
- `themes/pure-eric/`: Jinja templates and CSS. `index.html` is the landing page
  and `publications.html` is rendered via `TEMPLATE_PAGES`.
- `tools/coi_from_bibtex.py`: generates NSF COA co-author rows from the bib file.
- `logo.py`: regenerates `content/extra/favicon.ico` (needs ImageMagick).

## Conventions

- Commit messages are short with a prefix: `ENH:` or `FIX:`.
- Figures stated on the site (e.g. the "200+" projects count in `SOFTWARE_MORE`)
  have a comment saying how and when they were measured; update both together.
