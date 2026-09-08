#!/usr/bin/env python3
"""Extract page images from your own epub of The Practice of Neurocritical Care (2nd ed.)
into book/pages/<printed page>.png so book.html can display them locally.

Usage: python3 scripts/extract_book_pages.py /path/to/book.epub

The output folder is gitignored: the textbook is copyrighted and must not be published.
"""
import sys, zipfile, re, pathlib, io, tempfile

OFFSET = 8  # spine item N corresponds to printed page N - 8 in this edition's epub

if len(sys.argv) != 2:
    sys.exit(__doc__)
epub = pathlib.Path(sys.argv[1]).expanduser()
root = pathlib.Path(__file__).resolve().parent.parent
out = root / "book/pages"
out.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(epub) as z:
    container = z.read("META-INF/container.xml").decode()
    opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
    opf_dir = str(pathlib.PurePosixPath(opf_path).parent)
    opf = z.read(opf_path).decode()
    hrefs = dict(re.findall(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf))
    hrefs.update({i: h for h, i in re.findall(r'<item[^>]*href="([^"]+)"[^>]*id="([^"]+)"', opf)})
    spine = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf)
    n_written = 0
    for idx, idref in enumerate(spine, 1):
        printed = idx - OFFSET
        if printed < 1:
            continue
        page_html = z.read(f"{opf_dir}/{hrefs[idref]}").decode()
        m = re.search(r'src="([^"]+)"', page_html)
        if not m:
            continue
        img_path = str(pathlib.PurePosixPath(f"{opf_dir}/{hrefs[idref]}").parent / m.group(1))
        (out / f"{printed}.png").write_bytes(z.read(img_path))
        n_written += 1
print(f"wrote {n_written} page images to {out}")
