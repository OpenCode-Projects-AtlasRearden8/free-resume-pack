# Fill guide — Reference sheet

A reference sheet is simple on purpose: one page, three people, clean
contact info. It goes along once someone is seriously considering you.
This guide walks through filling it and using it well.

## What you'll touch

Same as always: `data/my-details.json`, the `ref_...` fields near the bottom.

## Fill it in minutes

| Field | What it holds |
|---|---|
| `ref_note` | One friendly sentence shown at the top of the sheet. The sample ("These references have agreed to speak about my work...") already does the job — rewrite only if you want a different tone. |
| `ref1_name` ... `ref3_name` | Full names, one person per group. |
| `ref1_role` | How they know your work, e.g. "Program Manager (my direct supervisor)". The parenthetical helps the caller place them fast. |
| `ref1_org` | Where they worked with you. Same organization as you? Say so. |
| `ref1_phone`, `ref1_email` | Their preferred contact. Ask them which they'd rather be reached on. |

## Choosing three good references

- **One direct supervisor** from your most recent job, if possible. This is the
  one most employers expect.
- **One coworker** who saw your daily work close up and can vouch with
  specifics.
- **One wild-card character reference** who adds something new: a professor,
  a volunteer coordinator, a client, a mentor.
- Bonus: work at least one reference who has watched you in a situation like
  the job you're after.
- People you live with or your family don't count (unless a family business
  employed you, and then name the relationship openly).

## The two-minute etiquette that pays

1. **Ask first.** Texting "hey can I use you as a reference?" works, but do it
   before you hand the sheet to anyone — never after a call has already
   surprised them.
2. **Give them context.** Tell them the role and the company so they can frame
   their answers. A short email works: "I'm applying for X at Y; they may call.
   Things I'd love you to mention: ___. Thank you!"
3. **Say thank you** when an application lands, and again if you get the job.
   References get re-used for years if you treat them well.

## Printing and sharing

- Build the sheet: `python3 build.py` (or just the sheets:
  `python3 build.py --docs references`).
- Bring a printed copy to interviews in a folder that also holds extra copies of
  your résumé. Hand it over when asked — usually at or after the interview,
  not in the initial application.
- Online: only upload it when a form asks for it. File-name copy for sending:
  `Jordan-Rivera-References.pdf`.

## What's in the layout you couldn't mess up

The sheet is one page, three rows, and lines for every phone and email —
a clean little thing a busy interviewer can find someone on in 10 seconds.
That's the whole job of the document. Resist adding paragraphs about yourself;
that's what the résumé is for.

## If you have fewer than three references

It's fine to hand over two rather than a wobbly third. Delete one whole
`<tr>...</tr>` block from `templates/<style>/references.html` and rebuild
(a `<tr>` block is one row of the table — it starts with `<tr>` and ends with
`</tr>`).
