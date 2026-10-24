# Fill guide — Cover letter

A cover letter is four short paragraphs and one subject line. It answers two
questions the hiring person is quietly asking: "Why are you here?" and "What's
in it for us?" Here's how to fill this one.

## What you'll touch

Still just `data/my-details.json` — the letter at the bottom of the file, under
`letter_...`. The date line fills itself from today's date at build time.

## The fields, one at a time

| Field | What it holds |
|---|---|
| `letter_role` | The exact job title from the posting — copy it word for word. |
| `letter_company` | The exact organization name from the posting. |
| `letter_manager` | Greeting name: "Ms. Alvarez". Find a real name if you can (posting, website, or the phone). "Hiring Team" is fine when there's no name. |
| `letter_opening` | Paragraph 1: which job, where, and the one honest hook. |
| `letter_body` | Paragraph 2: your best proof, in two or three sentences, aimed at that posting. |
| `letter_bullets` | The 3 short lines the reader can scan in 5 seconds. |
| `letter_closing` | Paragraph 3: the friendly ask — call, meet, thank you. |

## The formula, in plain English

1. **Opener (1–2 sentences).** "I am applying for the [role] at [company]"
   plus one line about why *this* posting or *this* place, mentioned by name.
   Short and factual — that shows respect.
2. **Proof (2–3 sentences).** Your most relevant experience stated plainly.
   Think "here's what I've been doing that looks like this job".
3. **Three scannable bullets.** Any numbers you have go here. A hiring person
   will genuinely read these bullets before the paragraphs — often *instead of*
   the paragraphs, so make them count.
4. **The ask + appreciation.** "If this looks like a fit, I'd be glad to talk"
   or something similar. One sentence of thanks at the end. Done — no extra
   formalities.

## Notes on tone

- Write like a composed version of how you actually talk. Plain and
  friendly beats fancy every time.
- "Please" and honest enthusiasm are fine. Begging is not. You're not asking
  for a favor — the company posted because it needs someone.
- The subject line already handles the "which job" part for you — it says
  `Re: the [role] opening at [company]`, auto-filled from the fields. So don't
  restate it again in paragraph one; open with your hook instead.
- One page beats one-and-a-half every time. If it runs long, cut a sentence.

## Attachments, file names, and sending

- Rebuild the letters after you've edited: `python3 build.py --docs cover-letter`
  (or the whole pack: `python3 build.py`).
- When you send it, attach two files: the letter and your résumé, plus the
  reference sheet occasionally (when someone asks or when it's an in-person
  application). Name files like this on your side:
  - `Jordan-Rivera-Cover-Letter-HousingCouncil.pdf`
  - `Jordan-Rivera-Resume.pdf`
- The PDFs are already the right size to email or upload. If a site wants
  pasted text instead of a file, open the PDF, select-all, and paste — the
  letter keeps its paragraph breaks.

## If you really can't think of an opener

Try one of these exact shapes and fill the holes:

- "Your posting for the [role] at [company] caught my eye because
  __________________."
- "I've kept an eye on [company] since __________________, so I was glad to
  see the [role] opening."
- "I'm applying for the [role]. I've worked
  __________________ for the last ______ years, and your list of duties
  reads like my current week."

## One more check before you hit send

Say the company name out loud — what's in the letter should match exactly.
Lots of rejections aren't about quality; the two quickest fix-ups are (1) the
job title copied exactly from the posting and (2) the right company name in
every mention.

## Where everything is

- Build all the letters: `python3 build.py`
- Data: `data/my-details.json` (the `letter_...` fields)
- Template files (if you edit directly): `templates/<style>/cover-letter.html`
