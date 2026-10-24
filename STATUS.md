# STATUS

## What was built

A self-contained freebie pack of fill-in job documents for Asdale Dynamics,
LLC: résumé, cover letter, and reference-sheet templates in three styles
(classic, modern, pivot-story) — nine templates total — that build into
polished, unbranded, single-page PDFs with one local script. No accounts, no
network calls, no secrets, no personal data (all sample text is fictitious,
built around the placeholder "Avery Sample").

Layout of the pack:

- `build.py` — the one build script. Fills every `{{token}}` from
  `data/my-details.json` (strings; lists feed the `*_bullets` keys; keys
  starting with `_` are treated as comments; `{{today}}` auto-fills), then
  renders HTML to PDF with the locally installed WeasyPrint. Flags:
  `--variants`, `--docs`, `--data`, `--out`, `--keep-html`, `--list`. Build
  errors come out as plain-English messages, not stack traces.
- `data/my-details.json` — one shared details file samples all nine
  documents; users fill it once and rebuild everything.
- `templates/{classic,modern,pivot-story}/{resume,cover-letter,references}.html`
  plus one CSS file per style. All layouts are deliberately ATS-safe:
  single column, standard headings, real selectable text, no images, no
  data in headers/footers.
- `Printables/` — the nine unbranded sample PDFs (rebuilt by the script).
- `docs/` — plain-English fill guide per template (resume, cover letter,
  references) plus ATS-safe layout notes.
- `tests/test_build.py` — 19 tests, described below.
- `README.md`, `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"),
  `requirements.txt`, `.gitignore`, `pytest.ini`.

## How to run it

```bash
python3 -m venv .venv && source .venv/bin/activate   # once
pip install -r requirements.txt                      # once
python3 build.py                                     # build all 9 PDFs
pytest -q                                            # run the test suite
```

Optional: `python3 build.py --keep-html` also writes filled-in HTML files
under `Printables/html/` for the browser "Print to PDF" route.

## Verification results

- All 9 templates build; each fits on exactly **one page**, verified by
  page counts from pypdf and by visually inspecting rendered page images
  (pdftoppm). Three distinct, polished designs confirmed.
- `pytest -q`: **19 passed**. Coverage includes: every template file and
  stylesheet exists; every PDF starts with a `%PDF` header, has ≥ 1 page,
  and has a selectable text layer containing the sample name (the
  ATS-readable property); `build_all` produces exactly the nine expected
  files; a missing detail raises a plain-English error naming the field; a
  JSON typo produces a friendly error with the line number; `_comment` keys
  are ignored; list values become list items; the sample data contains no
  real-looking personal domains or secret-shaped strings; and the CLI builds
  all nine end-to-end via `subprocess`.
- `--keep-html`, `--list`, and `--variants/--docs` filtering exercised by
  hand during development and working.

## Known gaps

- Inline skill "chips" and any color dependence are intentionally omitted in
  favor of strict ATS safety; users wanting a designed column layout would
  need to add it themselves (the guides advise against multi-column).
- Two-page overflow is not auto-warned: if a user's real history runs long,
  the résumé will simply spill to page two with clean break behavior (entries
  never split mid-job), rather than failing. A length check could be added.
- Fonts follow named stacks (Georgia/Helvetica families with Noto/DejaVu
  fallbacks); exact look will vary slightly on machines without those fonts.
- `--keep-html` assumes the folder is kept together (the stylesheet link is
  relative); it is documented as such.
- Windows is untested here (development machine is Linux); the venv setup
  commands differ slightly on Windows and the guides only cover Unix-style
  shells.
- The pivot-story variant only re-frames the résumé's structure; its cover
  letter and reference sheet share the other variants' layout (by design, but
  worth knowing when choosing).
