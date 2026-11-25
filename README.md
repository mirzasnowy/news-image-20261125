# news-image-20261125

Entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
sum up Wednesday 25 November 2026's world news in one image.

## The image

`entry-v2.png` (1024x1024, ~203 KB) is a newspaper-style front page,
"The World in One Page", drawn programmatically with Pillow so every word
is crisp and spelled correctly. It carries **40 stories**:

- **Lead — Asia, space:** Pakistan's first astronaut docks at China's
  Tiangong station (Shenzhou-24).
- **Markets:** Asia's chip rout — Kospi plunges 6.2% as AI doubts return.
- **Middle East:** two tankers hit mines and burn in the Strait of Hormuz.
- **Pacific:** Solomons sign a security pact with Australia.
- **Disaster + labour:** 26 miners trapped in a flooded Java gold mine;
  Bangladesh raises garment wages 36% after weeks of protests.
- **Also on — 28 more stories in one line each**, a world map with 12
  numbered pins, a UTC timeline of the day, region bars, a big-number
  strip, and a DATE CHECK box listing 7 stories deliberately left out
  because their dates were wrong (Huawei verdict, Giuliani Medal of
  Freedom, Sarkozy trial — all 24 November).

Every story carries a confidence label (CONFIRMED / REPORTED / CLAIM)
and its source (Reuters, AP, AFP, Al Jazeera, WSJ, CMSA/Xinhua, UN).

Headlines were verified against Reuters, AP, AFP, Al Jazeera, WSJ,
CMSA/Xinhua and UN summaries of 25 November 2026.

## How it works

`main.py` (Python 3.13, stdlib only) copies the bundled `entry-v2.png`
to `/output/entry.png`. No network, no randomness: the output bytes are
identical on every run. `draw_image_v2.py` is the build-time script that
rendered `entry-v2.png` from the headlines above.

```sh
python3 main.py   # writes /output/entry.png
```

`draw_image.py` and `entry.png` are the superseded v1 (8 stories),
kept for history.

## License

MIT — see `LICENSE`.
