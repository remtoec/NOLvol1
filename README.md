# 愛的本質 · 第一卷　第一章 — 行動裝置閱讀器

A single-file, mobile-optimized **Traditional-Chinese reader** for Chapter 1 of
Irving Singer's *The Nature of Love, Volume 1*. Built for reading on a phone and
for reading **together** in a book club — share a link and everyone lands on the
same paragraph.

## 📖 Read it now

**→ https://remtoec.github.io/NOLvol1/**

Deep-link to any paragraph by adding `#pN`, e.g.
[`…/NOLvol1/#p12`](https://remtoec.github.io/NOLvol1/#p12) opens at paragraph 12.

## Features

- **直排 / 橫排 toggle** — authentic vertical (top-to-bottom, right-to-left)
  typesetting by default, or switch to horizontal with a sliding toggle.
- **Jump to paragraph (book-club sync)** — type a paragraph number to jump, and
  the URL updates to `#pN`. Share that link and everyone opens to the same place.
- **Copy a paragraph link** — tap the small red paragraph number to copy its
  shareable `#pN` link to the clipboard.
- **Copy passage text** — select any text and tap **複製所選文字** to copy it
  (the per-paragraph link copy and text copy coexist without conflict).
- **Reading comfort** — light / sepia (米黃) / dark (夜間) themes, A−/A+ font
  size, a reading-progress bar, and the original paragraph numbers in the margin.
- **Self-contained & offline** — one `index.html` with the text embedded; no
  server or internet required. Uses Noto Serif TC online, falling back to the
  device's built-in 明體/宋體 offline.
- All preferences (theme, size, layout) persist across visits via `localStorage`.

## How it's built

The text lives in [`NOL.txt`](NOL.txt) (37 numbered paragraphs). A small
generator, [`build_reader.py`](build_reader.py), reads that file, strips the
leading line-number prefixes, and bakes the paragraphs into a styled, fully
self-contained `index.html`.

To regenerate after editing the text:

```bash
python build_reader.py   # reads NOL.txt → writes index.html
```

Then commit/upload the updated `index.html`.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The reader — this is what gets published (GitHub Pages serves it). |
| `NOL.txt` | Source text, 37 numbered paragraphs. |
| `build_reader.py` | Generator that turns `NOL.txt` into `index.html`. |

## Publishing (GitHub Pages)

Pages is set to **Deploy from a branch** → `main` / root, so any push that
updates `index.html` republishes automatically at the link above.

---

*Text reproduced from a Traditional-Chinese translation of Irving Singer,*
*The Nature of Love, Vol. 1, Ch. 1. Reader built for a book-club reading group.*
