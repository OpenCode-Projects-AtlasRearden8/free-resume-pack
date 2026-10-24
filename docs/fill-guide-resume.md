# Fill guide — Résumé

How to turn the sample résumé into your résumé. Take it one section at a time;
there is no rush and nothing here needs an account.

## What you'll touch

- `data/my-details.json` — the same file feeds every template, so you only fill
  facts in once and all nine documents pick them up.
- Nothing else, unless you want to delete a whole section (see the end).

## Choosing a style first

All three styles read from the same data, so fill first, choose later. If you
want a peek at each: open any PDF in `Printables/`.

- **Classic** — for traditional fields (healthcare, government, banking, schools)
  and anywhere you expect an older or stricter reader.
- **Modern** — clean lines and one calm color everyday. For most office,
  coordinator, retail, and small-business roles.
- **Pivot-story** — for career changers. It leads with *your story* and shows
  how old skills travel to the new field.

## Filling the résumé fields

Everything lives in `data/my-details.json`. The tool that edits it is any plain
text editor (Windows Notepad, Mac TextEdit, or a code editor). Leave the
punctuation alone: every value sits in `"quotes"`, lines end with a comma, and
your words go between the quotes.

Name and contact:

| Field | What it holds |
|---|---|
| `full_name` | Your name, the one people should call you. The sample is "Avery Sample" — that's a placeholder, not a person. |
| `target_title` | The job title you're aiming at, written the way employers write it. Not your current title. |
| `location` | "City, ST" works. You do not need a full street address. |
| `phone` | The phone you actually answer. |
| `email` | A normal, calm address. `name@gmail.com` outshines `partytime99@...`. |
| `website`, `linkedin` | Need one or both. Don't have one? Delete that line (see "Deleting things" below). |

Summary (2 sentences maximum): who you are, what you're good at, one concrete
honor or habit that carries proof. If you're stuck, write like you'd tell a
friendly neighbor, then trim.

Skills (three groups): name the group (e.g. "Everyday tools"), then list real
things people would recognize. Use words the job posting uses. Free and honest:
no invented skills.

Work experience (three jobs, newest first):

- `job1_title`, `job1_org`, `job1_dates` — your newest job. `job2_...` is the
  one before that, `job3_...` before that.
- `job1_bullets` etc. are lists (square brackets, several lines). One line of
  one accomplishment each, starting with a plain action word: ran, kept, wrote,
  trained, cut, fixed. Numbers are magic: "40 volunteers", "zero shortfalls"
  say more than "responsible for".

Education: newest first. Degree first, school second, years third. If you have
no degree, edit the HTML and swap this section in (see "Deleting things").

Extra credit: two lines of proof that you're trustworthy: certifications,
volunteer work, anything a coordinator/manager would nod at.

## Rebuild, then look

From the same folder the project lives in:

```bash
python3 build.py --docs resume
```

Open `Printables/resume-classic.pdf` (or modern / pivot-story, same command
without `--docs`). Print preview every time — one clean page beats two
half-filled ones. For most jobs, one page is the best résumé length.

## Deleting things (if you don't have one)

Open the matching file in `templates/classic` (or the style you rely on) — the
résumé file is `resume.html` — and delete the whole block you don't need. A
block is one `article` line group or one whole `<section>...</section>`.
Example: no LinkedIn? Delete the whole `<span>{{linkedin}}</span>` chunk.
Save, rebuild, done. Sections are labeled by heading, so scroll until you see
the one you want.

## Writing bullets that land

If a sentence is long or stiff, split it into two bullets, cut extra words, or
add a number. Short, concrete lines are easier to read at a glance — and that's
the moment you're competing for.

## One last habit

Before you apply anywhere, reread it once as a stranger — "would I call this
person?" — and fix anything a stranger would stumble on. When you send it out,
save a renamed copy with your name in the file name, like
`Jordan-Rivera-Resume.pdf` (the build only ever writes to `Printables/`, so
renaming a copy of the PDF never breaks anything).

## Before you apply

- Save or rename a copy of the finished PDF (moving it elsewhere is fine; the
  build only ever writes to `Printables/`).
- Read the "ATS-safe layout notes" once before
  you send it anywhere: `docs/ats-notes.md`.
- Every name, date, and number in the sample data is fictitious. When you
  replace them with real ones, that file becomes *your* personal data — keep it
  out of any public repo or shared drive.
