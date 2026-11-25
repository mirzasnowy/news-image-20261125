# news-image-20261125

A program that sums up the world's news of Wednesday 25 November 2026
in a single image, for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125).

## Run it

```sh
python3 main.py                 # writes /output/entry.png
python3 main.py out.png         # writes out.png (for local testing)
```

Python 3.13 (works on 3.12 too). No third-party packages, no network:
the program uses only the standard library.

## What it draws

A 1024x1024 newspaper front page:

- Masthead "THE WORLD IN ONE PAGE" and the date, Wednesday, 25 November 2026.
- Eight story cards: Ukraine (Abu Dhabi talks stall), COP31 (summit ends
  with no deal), US tariffs (planned on 16 partners), the shutdown fight
  (Congress split over Iran war funding), Nvidia (Huang reinstated, shares
  up about 30%), Gaza (ceasefire may collapse), Ebola in DR Congo (still
  not under control), Sudan (drone war in Kordofan).
- A markets ticker (24 Nov session): Nasdaq about -1.4%, Brent about $89,
  gold about $3,600; the Seoul subway strike averted; 25 Nov is the UN Day
  to End Violence Against Women.
- A source footer.

## How it works

`main.py` is a single file with no dependencies. It contains:

- A hand-built 5x7 bitmap font (A-Z, a-z, 0-9 and the punctuation the
  page needs), drawn at several scales for the masthead, card titles,
  body text and ticker.
- A small canvas (an RGB byte array) with rectangle and text drawing,
  plus greedy word wrap so no text overflows its card.
- A hand-written PNG encoder (zlib level 9, no filtering). The output
  is deterministic: two runs write byte-identical files.

The image is 1024x1024 and about 19 KB, well inside the 1 MiB limit.

## Sources

AP, UN News, Al Jazeera. Figures marked `~` in the image rest on a
single source (the markets figures and the Seoul subway item).
