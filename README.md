[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/mirzasnowy/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/mirzasnowy/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# news-image-20261125

Entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
sum up Wednesday 25 November 2026's world news in one image.

## The image

`entry-v6.png` (1024x1024, ~211 KB) is "The World Wire", a newspaper-style
front page drawn programmatically with Pillow so every word is crisp and
spelled correctly. It carries **35 stories**: 1 lead, 12 main cards, and
22 more in the ALSO ON list.

- **Lead — Asia, space:** Pakistan's first astronaut docks at China's
  Tiangong station (Shenzhou-24, the 18th crewed Shenzhou flight).
- **Markets:** Asia's chip rout — Kospi closes 6.16% down at 4,697.51.
- **Middle East:** two more tankers hit mines and burn in the Strait of
  Hormuz; coalition strike on Hodeidah at dawn.
- **Pacific:** Solomons sign a security pact with Australia.
- **Disaster + labour:** 3 bodies found, 23 still trapped in the flooded
  Pongkor gold mine in Java; Bangladesh raises garment wages 36% after
  weeks of protests.
- **Africa — 9 of 35 stories**, the widest regional spread of the
  front page.
- **Also on — 22 more stories in one line each**, a world map with 12
  numbered pins, a UTC timeline of the day, region bars, a big-number
  strip, a FOLLOW-UP box for Wednesday developments of Tuesday stories,
  and a DATE CHECK box listing 9 stories deliberately left out because
  their dates were wrong (Huawei verdict, Giuliani Medal of Freedom,
  Sarkozy trial — all 24 November).

Every story carries a confidence label (CONFIRMED / REPORTED / CLAIM)
with its source (Reuters, AP, AFP, Al Jazeera, WSJ, CMSA/Xinhua, UN)
and a HOW SURE legend that defines the labels. Wires read to 12:00 UTC.

Headlines were verified against Reuters, AP, AFP, Al Jazeera, WSJ,
CMSA/Xinhua and UN summaries of 25 November 2026.

## How it works

`main.py` (Python 3.13, stdlib only) copies the bundled `entry-v6.png`
to `/output/entry.png`. No network, no randomness: the output bytes are
identical on every run. `draw_image_v6.py` is the build-time script that
rendered `entry-v6.png` from the headlines above.

```sh
python3 main.py   # writes /output/entry.png
```

`draw_image_v5.py` / `entry-v5.png`, `draw_image_v4.py` /
`entry-v4.png`, `draw_image_v3.py` / `entry-v3.png`,
`draw_image_v2.py` / `entry-v2.png`, and `draw_image.py` /
`entry.png` are superseded versions, kept for history.

## License

MIT — see `LICENSE`.
