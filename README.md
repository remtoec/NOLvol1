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

- **Warm, easy-on-the-eyes type** — body set in **LXGW WenKai TC (霞鶩文楷)**, a
  warm hand-brushed 楷書 whose even, open strokes are gentler for long mobile
  reading than thin Ming hairlines; the masthead title stays in Noto Serif TC for
  a more authoritative frame.
- **橫排 / 直排 toggle** — comfortable horizontal reading by default; switch to
  authentic vertical (top-to-bottom, right-to-left) typesetting with a sliding toggle.
- **Jump to paragraph (book-club sync)** — type a paragraph number to jump, and
  the URL updates to `#pN`. Share that link and everyone opens to the same place.
- **Copy a paragraph link** — tap the small red paragraph number to copy its
  shareable `#pN` link to the clipboard.
- **Copy passage text** — select any text and tap **複製所選文字** to copy it
  (the per-paragraph link copy and text copy coexist without conflict).
- **Resume where you left off** — your reading position is remembered and restored
  on your next visit (a deep `#pN` link always takes precedence).
- **目錄 (table of contents)** — tap **☰** to open a drawer listing all 37
  paragraphs with snippets; tap any to jump straight there. It also shows an
  estimated reading time and lets you switch the body typeface between
  **楷 (霞鶩文楷)** and **明 (思源宋體 / Noto Serif)**.
- **Distraction-free scrolling** — in horizontal mode the toolbar tucks away as you
  read downward and slides back the moment you scroll up; a subtle indicator shows
  **第 N 段 / 共 37 段** while you scroll.
- **Reading comfort** — light / 米黃 / 夜間 themes (auto-matching your phone's
  light/dark setting on first visit), A−/A+ font size, a reading-progress bar, and
  the original paragraph numbers in the margin. The dark theme uses a soft warm
  charcoal to reduce night-time glare.
- **Self-contained & offline** — one `index.html` with the text embedded; no
  server required. Web fonts load from a CDN with `font-display:swap` and degrade
  gracefully to the device's built-in 明體/宋體 when offline.
- All preferences (theme, size, layout, position) persist across visits via `localStorage`.

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
