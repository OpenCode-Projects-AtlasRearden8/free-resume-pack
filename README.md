# Free Resume Pack

Clean, fill-in résumé, cover letter, and reference-sheet templates that build
into polished, print-ready PDFs — right on your own computer. No accounts, no
uploads, no "free" website that quietly asks for your personal data.

Three styles × three documents = nine templates:

|  | Classic | Modern | Pivot-story |
|---|---|---|---|
| Résumé | ✓ | ✓ | ✓ |
| Cover letter | ✓ | ✓ | ✓ |
| Reference sheet | ✓ | ✓ | ✓ |

**Classic** — quiet serif design for traditional fields: healthcare,
government, banking, schools.

**Modern** — clean sans-serif with one deep-teal accent. Great default for
most office, coordinator, retail, and small-business roles.

**Pivot-story** — made for career changers. It leads with a short "who I am"
story and shows concretely how your old skills travel ("what I bring with
me → where it shows up"), while keeping the standard headings hiring tools
search for.

Built by **Asdale Dynamics, LLC** (Dylan Asdale) as part of our plain-English
toolkit: AI and job-hunting explained like a friend would — step by step,
never condescending. More at dylanasdale.github.io.

## Quick start (plain English, one time)

You need Python 3.10 or newer, installed once, on your computer.
Get it from python.org — or on some Macs you already have it (run
`python3 --version` to check).

Then, from inside this folder, in a terminal:

```bash
# 1. Make a private workspace for the tools (called a "virtual environment"):
python3 -m venv .venv

# 2. Turn it on:
source .venv/bin/activate

# 3. Install the two small tools this pack needs:
pip install -r requirements.txt
```

That's setup. It stays done.

## Using it (every time you change your info)

1. **Fill in your details.** Open `data/my-details.json` in any text editor.
   It currently holds clearly-fake sample text (a person named "Avery
   Sample") so you can see how the pages look. Replace each value with your
   own — the guides in `docs/` walk through every field, template by
   template, in plain English.
2. **Build the PDFs.** `python3 build.py`
3. **Find them.** Nine PDFs appear in `Printables/` — unbranded and ready to
   print or attach. Print at 100% on US Letter paper (that's what they're
   drawn for).

Useful variants:

```bash
python3 build.py --variants classic            # only one style
python3 build.py --docs resume                 # only résumés
python3 build.py --variants modern --docs resume,cover-letter   # a mix
python3 build.py --keep-html                   # also saves filled-in HTML
```

With `--keep-html`, each PDF gets a matching file in `Printables/html/` that
you can open in a browser and choose "Print to PDF" yourself — an extra path
for computers where the first route won't cooperate. Keep the folders
together so the HTML can find its stylesheet.

## The tests (so you can trust the pack)

```bash
pytest -q
```

Nineteen checks run automatically: every template must build to a real,
openable PDF with selectable text (the property that keeps it ATS-readable),
the sample data must stay obviously fictitious, the command line must work
end-to-end, and the build must fail *nicely* — plain-English error, no crash —
whenever a fill-in field is missing or a JSON typo sneaks in.
The tests keep the pack honest whenever anyone changes it.

## The guides

- `docs/fill-guide-resume.md` — every résumé field, plus bullet-writing help.
- `docs/fill-guide-cover-letter.md` — the four-paragraph formula and tone.
- `docs/fill-guide-references.md` — choosing references and simple etiquette.
- `docs/ats-notes.md` — what "ATS" is, why these layouts read well by
  machines *and* humans, and what to avoid if you edit the HTML yourself.

## A note about your info

The sample data shipped in `data/my-details.json` is entirely fictitious.
When you fill it with your real name, phone, and history, that file becomes
*your* personal information — so keep it (and the PDFs you build) out of any
place you share publicly. The `.gitignore` already protects the usual
accidents, but it can't protect a copy you move by hand.

## License

MIT — free to use, change, and share, including for anything you run or
publish. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
