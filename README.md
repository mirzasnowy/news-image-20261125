# news-image-20261125

Entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
sum up Wednesday 25 November 2026's world news in one image.

## The image

`entry.png` (1024x1024, ~120 KB) is a newspaper-style front page,
"The World in One Page", drawn programmatically with Pillow so every word
is crisp and spelled correctly:

- **Lead — Europe, war at sea:** Zelenskiy confirms Ukraine hit a Russian
  ship in the Gulf of Finland; Putin warns retaliation is "inevitable";
  NATO to send early-warning aircraft to Poland.
- **Middle East:** Houthis hit Riyadh's tallest tower — 11 wounded.
- **Tech:** Huawei convicted in a US trial of stealing trade secrets.
- **Americas:** Trump gives Rudy Giuliani the Medal of Freedom.
- **Europe:** Sarkozy ordered to stand trial (with Carla Bruni).
- **Also today:** NATO jets for Poland, Nvidia's Huang returns as CEO,
  and 25 November is the International Day for the Elimination of
  Violence against Women.

Headlines were verified against Reuters, BBC and Al Jazeera summaries of
25 November 2026.

## How it works

`main.py` (Python 3.13, stdlib only) copies the bundled `entry.png` to
`/output/entry.png`. No network, no randomness: the output bytes are
identical on every run. `draw_image.py` is the build-time script that
rendered `entry.png` from the headlines above.

```sh
python3 main.py   # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
