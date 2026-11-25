# news-image-20261125 — Wednesday 25 November 2026 in one image

Entry for the make.fun bounty "Sum up 25 November's world news in one image".

`main.py` (Python 3.13, **standard library only**) draws the whole picture itself —
anti-aliased vector rasteriser, built-in stroke font, hand-built pictograms —
and writes a 1024x1024 PNG (~255 KB) to `/output/entry.png`.
No network, no fonts, no assets, no randomness: two runs give byte-identical files.

```
python main.py              # writes /output/entry.png
python main.py test.png     # optional: write somewhere else (local testing)
```

## What the image shows (8 stories + ticker)

| Card | Story |
|------|-------|
| Ukraine war | US-brokered Abu Dhabi talks ended with no major breakthrough |
| Climate | COP31 (Antalya) ended 22 Nov with no deal, longest UN climate summit ever |
| Trade | US readying new tariffs on 16 partners incl. China and the EU (AP sources) |
| US Congress | Shutdown looms (deadline 11 Dec) over Iran war funding |
| Tech/markets | Nvidia reinstates CEO Jensen Huang after Trump pressure; shares jump ~30% |
| Gaza | Board of Peace warns the ceasefire may collapse; 74,000+ killed since 2023 |
| Health | DR Congo Ebola outbreak "still not under control": 11,000+ cases, 5,500+ deaths |
| Sudan | Drone war in Kordofan: 2,230+ civilians killed Jan-Oct 2026 |
| Ticker | Markets (24 Nov session), Seoul subway strike averted, UN Day to end violence against women (25 Nov) |

To refresh the content, edit `STORIES`, `FOOT_1`, `FOOT_2` near the bottom of `main.py`.
Copy is auto-uppercased and word-wrapped; only A-Z, 0-9 and `. , - : ; % $ ~ ' + | / ( ) ? !` are drawn.

## Sources (researched 25 Nov 2026)

- COP31: UN News https://news.un.org/en/story/2026/11/1168855 · CBS News https://www.cbsnews.com/news/un-cop31-climate-conference-ends-no-agreement-fossil-fuel-debate-standstill/
- Tariffs: AP via Korea Times https://www.koreatimes.co.kr/world/20261125/us-ready-to-slap-tariffs-on-china-eu-and-others-over-subsidized-production-ap-sources-say
- Shutdown / Iran war funding: https://www.yahoo.com/news/politics/articles/gop-leaders-signal-openness-cutting-140100010.html
- Nvidia: NBC News https://www.nbcnews.com/tech/tech-news/nvidia-reinstates-jensen-huang-rcna610864 · Washington Post https://www.washingtonpost.com/politics/2026/11/23/trump-personally-orchestrated-jensen-huang-return-nvidia-ceo/ · CNN https://www.cnn.com/2026/11/23/business/live-news/jensen-huang-reinstated-as-ceo-of-nvidia
- Ukraine talks: ITV https://www.itv.com/news/2026-11-10/talks-between-russia-and-ukraine-begin-in-abu-dhabi-with-us-mediation · Forbes https://www.forbes.com/sites/marktemnycky/2026/11/12/why-us-led-talks-with-russia-and-ukraine-had-no-major-breakthrough/
- Gaza: Al Jazeera https://www.aljazeera.com/news/2026/11/18/board-of-peace-warns-gaza-ceasefire-faces-imminent-collapse-without-action
- Ebola: Al Jazeera https://aljazeera.com/news/2026/11/15/africa-cdc-says-ebola-outbreak-in-dr-congo-still-not-under-control · Rio Times Africa brief https://www.riotimesonline.com/africa-intelligence-brief-tuesday-november-24-2026/
- Sudan: Rio Times Africa brief (above)
- Markets: https://eurasiabusinessnews.com/2026/11/24/stock-market-today-november-24-2026-nasdaq-falls-as-nvidia-and-anthropic-slide-oil-price-at-89-gold-drops-to-3620/
- Seoul subway: SBS https://news.sbs.co.kr/english/article.do?news_id=N1008861969

## AI transcripts

The bounty requires the AI coding-agent transcripts of the session(s) that built this entry.
Add them to this repository (e.g. `transcripts/`) before submitting.
