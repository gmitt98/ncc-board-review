#!/usr/bin/env python3
"""Render audio/transcript.md to an M4A audiobook with chapter markers using Kokoro TTS.

Usage:
  .venv/bin/python scripts/render_audio_kokoro.py [--voice af_heart] [--speed 1.0]
                                                 [--out audio/ncc_audio_summary.m4a]
                                                 [--sample N]   # only the first N chapters
Setup:
  python3 -m venv .venv && .venv/bin/pip install kokoro soundfile
  brew install espeak-ng   # optional fallback phonemizer for unusual words
"""
import argparse, os, pathlib, re, subprocess, sys
import numpy as np
import soundfile as sf

ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--voice", default="af_heart")
ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--src", default=str(ROOT / "audio/transcript.md"))
ap.add_argument("--out", default=str(ROOT / "audio/ncc_audio_summary.m4a"))
ap.add_argument("--work", default=str(ROOT / "tts_work"))
ap.add_argument("--sample", type=int, default=0)
args = ap.parse_args()

from kokoro import KPipeline  # noqa: E402  (slow import; after arg parsing)

SR = 24000
work = pathlib.Path(args.work) / args.voice
work.mkdir(parents=True, exist_ok=True)


def chapters(md):
    parts = re.split(r"^## ", md, flags=re.M)
    out = []
    for i, p in enumerate(parts):
        if not p.strip():
            continue
        if i == 0:
            title, body = "Introduction", p
        else:
            title, _, body = p.partition("\n")
        body = re.sub(r"^\s*[-*]\s+", "", body, flags=re.M).replace("*", "")
        out.append((title.strip(), body.strip()))
    return out


def spoken_fixes(t):
    # Small pronunciation helps for the neural model.
    t = re.sub(r"\bI C H\b", "I-C-H", t)
    t = re.sub(r"\bT T M\b", "T-T-M", t)
    t = t.replace("gabba", "GABA").replace("ICP", "I-C-P").replace("mmHg", "millimeters of mercury")
    return t


pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
chs = chapters(open(args.src).read())
if args.sample:
    chs = chs[: args.sample]

chapter_index = []
files, meta, t0 = [], [";FFMETADATA1", "title=Neurocritical Care Board Review Audio Summary", "artist=Kokoro TTS"], 0.0
for i, (title, body) in enumerate(chs):
    wav = work / f"{i:02d}.wav"
    if not wav.exists():
        text = spoken_fixes(f"{title}.\n\n{body}")
        chunks = []
        for _, _, audio in pipe(text, voice=args.voice, speed=args.speed, split_pattern=r"\n+"):
            chunks.append(np.asarray(audio, dtype=np.float32))
            chunks.append(np.zeros(int(SR * 0.35), dtype=np.float32))  # short pause between paragraphs
        sf.write(wav, np.concatenate(chunks), SR)
    dur = sf.info(wav).duration
    meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(t0*1000)}", f"END={int((t0+dur)*1000)}", f"title={title}"]
    chapter_index.append({"title": title, "start": round(t0, 1)})
    t0 += dur
    files.append(wav)
    print(f"{i:02d} {dur/60:5.1f} min  {title}", flush=True)

(work / "list.txt").write_text("".join(f"file '{f.resolve()}'\n" for f in files))
(work / "meta.txt").write_text("\n".join(meta) + "\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"),
                "-i", str(work / "meta.txt"), "-map_metadata", "1", "-c:a", "aac", "-b:a", "96k", args.out], check=True)
if not args.sample:
    import json
    json.dump(chapter_index, open(ROOT / "audio/chapters.json", "w"), indent=1)
print(f"TOTAL {t0/60:.1f} min -> {args.out}")
