# Neurocritical Care Board Review

250 single-best-answer practice questions with explanations, written to the content of
*The Practice of Neurocritical Care*, 2nd Edition (Neurocritical Care Society, 2021), plus an
80-minute high-yield audio review in a choice of two narrators.

**Site:** https://gmitt98.github.io/ncc-board-review/

## What's here

- `index.html` — all questions on one page. Click an option to check it, or expand
  *Answer & explanation*, which ends with the textbook chapter and page reference. Filter by
  difficulty, search, jump by chapter. Your answers are stored in your browser only.
- `audio.html` — the audio review with a choice of two Kokoro neural voices (Bella, Michael), chapter
  jump points, and per-voice download; `audio/transcript.md` is the script.
- `downloads/` — printable PDFs (with explanations, and test mode with answer key) and a Word
  version; all linked from the site's **Downloads** menu.
- `data/questions.json` — the question bank (chapter, topic, difficulty, stem, options,
  answer, explanation, book pages). Load it into Anki or anything else.

Each explanation cites the chapter and printed page(s) of the textbook it is drawn from, so you
can check the source in your own copy. The book itself is not included.

## Rebuilding the site

```bash
python3 scripts/build_site.py
```

## Re-rendering the audio

```bash
/opt/homebrew/bin/python3.12 -m venv .venv && .venv/bin/pip install kokoro soundfile
brew install espeak-ng   # fallback pronunciation for unusual words
.venv/bin/python scripts/render_audio_kokoro.py --voice af_bella  --out audio/ncc_audio_summary_bella.m4a   --chapters audio/chapters_bella.json
.venv/bin/python scripts/render_audio_kokoro.py --voice am_michael --out audio/ncc_audio_summary_michael.m4a --chapters audio/chapters_michael.json
```

## How it was made

Each chapter's text was OCR'd from the epub, then a writer produced questions and high-yield
facts from that text only, and an independent reviewer re-checked every question against the
chapter, editing 26 of them. The textbook remains the authority; report anything that looks
wrong by opening an issue.

Not affiliated with or endorsed by the Neurocritical Care Society.
