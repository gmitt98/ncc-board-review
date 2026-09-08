#!/usr/bin/env python3
"""Build index.html (all 250 questions on one page) from data/questions.json."""
import json, html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
qs = json.load(open(ROOT / "data/questions.json"))
chapters = json.load(open(ROOT / "data/chapters.json"))
tpl = open(ROOT / "scripts/template.html").read()

SECTION = {"I": "Part I · General Critical Care", "II": "Part II · Neurocritical Care", "III": "Part III · Administration"}


def esc(s):
    return html.escape(str(s or ""))


def first_page(pages):
    m = re.search(r"\d+", str(pages))
    return int(m.group()) if m else None


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# chapter order and per-chapter question ranges
by_chapter = {}
for i, q in enumerate(qs, 1):
    by_chapter.setdefault(q["chapter"], []).append(i)

nav = []
cur_section = None
for c in chapters:
    sec = re.match(r"[IVX]+", c["key"]).group()
    if sec != cur_section:
        cur_section = sec
        nav.append(f'<li class="nav-sec">{esc(SECTION[sec])}</li>')
    nums = by_chapter.get(c["title"], [])
    if nums:
        nav.append(f'<li><a href="#{slug(c["title"])}">{esc(c["title"])}</a><span class="nav-n">{nums[0]}–{nums[-1]}</span></li>')

cards = []
cur = None
for i, q in enumerate(qs, 1):
    if q["chapter"] != cur:
        cur = q["chapter"]
        meta = next(c for c in chapters if c["title"] == cur)
        cards.append(f'<h2 class="chapter" id="{slug(cur)}">{esc(cur)}<span class="chapter-pages">book pp. {meta["start"]}–{meta["end"]}</span></h2>')
    p = first_page(q.get("pages"))
    page_link = (f'<a class="book-link" href="book.html?p={p}" title="Open book page {p}">'
                 f'Book: {esc(q["chapter"])}, p. {esc(q.get("pages"))}</a>') if p else esc(q.get("pages"))
    opts = "".join(
        f'<li><button class="opt" data-l="{L}"><span class="letter">{L}</span><span>{esc(q["options"][L])}</span></button></li>'
        for L in "ABCDE")
    expl = esc(q["explanation"])
    expl = re.sub(r"(Key point:)\s*", r'</p><p class="keypoint"><strong>\1</strong> ', expl, count=1)
    cards.append(f'''
<article class="q" id="q{i}" data-n="{i}" data-ans="{q["answer"]}" data-ch="{esc(q["chapter"])}" data-diff="{esc(q.get("difficulty",""))}">
  <header><span class="qnum">Question {i}</span><span class="tags">{esc(q.get("topic",""))} <em class="diff diff-{esc(q.get("difficulty",""))}">{esc(q.get("difficulty",""))}</em></span></header>
  <p class="stem">{esc(q["stem"])}</p>
  <ol class="opts">{opts}</ol>
  <details class="answer">
    <summary>Answer &amp; explanation</summary>
    <p class="ans-line"><strong>Answer: {q["answer"]}.</strong> {esc(q["options"][q["answer"]])}</p>
    <p class="expl">{expl}</p>
    <p class="src">{page_link}</p>
  </details>
</article>''')

out = (tpl.replace("{{NAV}}", "\n".join(nav))
          .replace("{{CARDS}}", "\n".join(cards))
          .replace("{{COUNT}}", str(len(qs))))
open(ROOT / "index.html", "w").write(out)
print(f"wrote index.html with {len(qs)} questions, {len(by_chapter)} chapters")
