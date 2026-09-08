# Neurocritical Care Board Review

250 single-best-answer practice questions with explanations, written to the content of
*The Practice of Neurocritical Care*, 2nd Edition (Neurocritical Care Society, 2021), plus a
63-minute high-yield audio review.

**Site:** https://gmitt98.github.io/ncc-board-review/

## What's here

- `index.html` — all questions on one page. Click an option to check it, or expand
  *Answer & explanation*. Filter by difficulty, search, jump by chapter. Your answers are
  stored in your browser only.
- `audio.html` — the audio review with chapter jump points; `audio/transcript.md` is the script.
- `book.html?p=N` — page viewer. Each explanation links to the textbook page it draws from.
- `data/questions.json` — the question bank (chapter, topic, difficulty, stem, options,
  answer, explanation, book pages). Load it into Anki or anything else.

## Book pages

The textbook is copyrighted, so its page images are **not** in this repository and the public
site shows only chapter and page references. If you own the epub, extract pages locally:

```bash
python3 scripts/extract_book_pages.py /path/to/Practice_of_Neurocritical_Care.epub
python3 -m http.server   # then open http://localhost:8000
```

`book/pages/` is gitignored.

## Rebuilding the site

```bash
python3 scripts/build_site.py
```

## How it was made

Each chapter's text was OCR'd from the epub, then a writer produced questions and high-yield
facts from that text only, and an independent reviewer re-checked every question against the
chapter, editing 26 of them. The textbook remains the authority; report anything that looks
wrong by opening an issue.

Not affiliated with or endorsed by the Neurocritical Care Society.
