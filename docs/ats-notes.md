# ATS-safe layout notes

What an ATS is, why these templates are safe with it, and what to keep doing
(and what to avoid) if you edit the templates yourself.

## What "ATS" means

Most medium and large employers use an "applicant tracking system" (ATS): a
program that reads your PDF before any human does, pulls out your name, job
titles, dates, and skills, and shows them to a recruiter. An ATS is basically
good at reading *simple, tidy* documents and basically bad at reading *fancy*,
scattered ones. Small businesses and referrals often skip ATS altogether and
read the PDF directly — and simple, tidy impresses humans too.

## Why these templates read well

- **One column, top to bottom.** No side bars or floating text boxes. The ATS
  gets the page's story in the order you'd read it aloud: name → contact →
  summary → skills → jobs → education.
- **Real, selectable text.** These PDFs are typeset, not pictures of text:
  select-all in any PDF reader and you'll get actual words. (Images of text — a
  photo of your résumé, or a scanned page — are the #1 ATS trap.)
- **Standard section headings.** "Summary", "Work Experience", "Education" —
  the words parsers look for. Even the pivot-story variant keeps these
  headings; its storytelling lives *inside* the standard sections, which is
  exactly why it works.
- **No headers/footers, no page numbers carrying data.** Vital details
  (name, phone, email) stay in the body where every parser looks.
- **Fonts do what fonts do.** Georgia/Helvetica-family fonts, normal sizes,
  normal spacing. No letters stretched into logos.
- **Standard bullets, simple tables only where parsers are fine with them.**
  The one table in the pack is the reference sheet — which is for human eyes
  after an interview, not for the parsing stage.
- **Line and paragraph structure with real markup.** Jobs are list items and
  headings, not "clever" arrangements of empty spaces or drawn shapes.
- **PDF metadata comes from the HTML title**, so the file's document title is
  "Résumé — Your Name", not a temp-file name.

## Field-by-field do's

- **Dates as words**: "2022 – Present", "Jan 2019 – May 2022" — month names
  with years parse cleanly. Avoid odd shapes like "left after Q3";
  use whole, standard formats.
- **Phone in any sane format** — (555) 010-4567 parses everywhere.
- **Email as plain text**, never behind a "click to email" link picture.
- **One job title per block, one employer per block.**
- **File name with your name in it.** The recruiter and the ATS both see
  `avery-sample-resume.pdf` before opening anything: name it like you sign it.

## Don'ts if you edit the HTML

- No text inside images or photos (headshots included — many systems discard
  resumes with photos outright).
- No multi-column layouts via floated boxes: the pack is deliberately
  single-column; keep it that way.
- No white text used to cram unseen keywords onto the page — systems and
  humans both increasingly check for that trick.
- No absolute-positioned "cleverness": if a design idea needs words to float
  off in a box, save it for your portfolio, not your résumé.
- No special characters that only render in one font: arrows you can't type on
  a normal keyboard are a gamble. Words play safer than symbols everywhere.

## Checking after you edit

The most reliable self-test, open the built PDF and **select all text**:

1. Ctrl/Cmd-A, then copy into any plain text editor.
2. Everything you care about — name, phone, every job title, every date, the
   whole skills section — must be readable in the paste output.
3. If a piece is missing, that piece is probably sitting inside something
   non-text, and an ATS will miss it too.

The pack's automated tests do a cousin of this check for every template,
every build (they run the PDF extraction function). The test suite checks
sample text appears in the extracted layer — the same property you want for
every rebuild.

## The one-page thing, again

Most ATS don't care about page count; humans time-allocate. One tidy page
from this pack beats a two-page résumé arriving at the same inbox unless the
second page carries real extra proof not found on page one. When in doubt:
trim, don't shrink — and never shrink the text font size below about 9.5pt.
