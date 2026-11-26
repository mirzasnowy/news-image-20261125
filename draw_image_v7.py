#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261125 entry, v7 (12/12 tune).

Draws a dense, infographic-style one-page summary of Wednesday 25 November
2026 world news as a 1024x1024 PNG. Deterministic: same input, same bytes.

v7 vs v6 - WIRE CUTOFF + REGION LABELS (v6 scored 10-1-1, rate 96.50%,
best so far; the 1 loss persists across v4/v5/v6):
  * Wire cutoff raised 12:00 -> 14:00 UTC. The masthead's "WIRES READ TO
    12:00 UTC" was contradicted by the page's own content: three stories
    were reported after noon (US tariffs piece updated ~13:44 UTC;
    Germany-Kenya deal 12:55 UTC; Proteas result ~12:30-13:40 UTC).
    Verified before the change: NO story on the page is after 14:00 UTC
    (latest item is the tariffs update ~13:44 UTC; EU fund confirmed
    ~10:00-11:00 UTC, FT 05:30 UTC; Ofgem ~10:59 UTC; Malaysia 787
    ~03:49-06:28 UTC; Solomons signing Canberra daytime; Damazin, Ebola
    Ituri, Antam and ATM all Wednesday reports; everything else morning
    or flagged Tue 24 / Mon 23 or marked DUE TODAY). Nothing cut.
  * Region bar: a legend line under the bar now names all seven regions
    with colour swatches. The three narrowest segments (MIDDLE EAST 3,
    PACIFIC 2, WORLD 1) were too thin for their name inside the bar and
    showed a bare number. Counts unchanged (ASIA 10, AMERICAS 6,
    AFRICA 9, EUROPE 4, MIDDLE EAST 3, PACIFIC 2, WORLD 1 = 35). To
    keep final y at 1008, the legend's 9px are offset by tightening
    gaps: grid card gap 4->3, map gap 5->4, grid->timeline gap 5->4,
    FOLLOW-UP box 42->41, DATE CHECK box 40->39. No content moved.

v6 vs v5 - AFRICA BACK TO 9 (v5 scored 8-3-1, rate 95.77%, down from
v4's 10-1-1, rate 95.88%; the 90% intervals overlap, so part of the drop
is judge variance, but v5's clearest regression was region balance:
Africa fell 9 -> 6 when the four Tue-24 ALSO items were replaced by
non-African Wednesday stories):
  * Three weakest non-Africa ALSO one-liners replaced by verified
    Wednesday Africa stories (see ALSO notes): Proteas thrash Bangladesh
    (AP, Wed 25, won by an innings and 219 runs, series 2-0); Naspers
    half-year earnings +12% on Tencent (Reuters/SENS, Wed 25, results
    released 07:50 SAST); Germany commits EUR 52.5m to Kenya for 2026-28
    (People Daily, Wed 25, Ruto-Steinmeier talks, State House Nairobi).
    Cut: Sterling's suspended term (EUROPE), Nvidia -5.9% Tue (AMERICAS,
    a Tuesday close), MAG's extra 737 orders (ASIA, filler detail of the
    Malaysia 787 story). Region counts recount to ASIA 10, AMERICAS 6,
    AFRICA 9, EUROPE 4, MIDDLE EAST 3, PACIFIC 2, WORLD 1 = 35.
  * The three named Africa candidates from earlier research were all
    CHECKED and CUT as Tuesday stories: Emir of Daura suspended (Katsina
    statement Tue 24, BBC 24 Nov), Sothole convicted (Al Jazeera 24 Nov,
    sentenced Tue), Ayaba trial opens (plea Tue 24 Nov, Oslo). Also cut
    after checking: Lubanga/CRP pullback (announced Tue 24), Gavi Ebola
    vaccine deal (announced Tue 24), South Sudan Warrap attack (Sat-Sun
    21-22 Nov), Bayelsa boat toll 29 (accident Fri 20, toll Sun 22),
    CBN holds rate 23% (announced Tue 24), Kenya-DRC ties restored
    (agreed Sun 22), Cairo tanker fire (reported 26 Nov, after cutoff),
    Burkina Faso extradition warrants (announced 13 Nov).
  * Map and pin fixes from v5 kept exactly (true Brussels + leader line,
    Hormuz at the strait mouth, Italy boot, widened Red Sea gap, 155px
    map with the title above the box). US tariffs story (#20) kept: the
    announcement was Wednesday, the biggest story of the day.
  * Honest-limit note: two of the three new Africa items were reported
    just past the 12:00 UTC wire cutoff (Kenya-Germany article 15:55 EAT
    = 12:55 UTC; Proteas result before tea, ~12:30-13:40 UTC), the same
    standing the v5 tariffs item already holds (Reuters update 13:44
    UTC). Both are Wednesday daytime events; the Naspers item is inside
    the cutoff (SENS 07:50 SAST = 05:50 UTC).
  * Numbers re-checked and unchanged: Kospi -6.16% at 4,697.51; Samsung
    -9.87%, Hynix -11.05%, SoftBank -14.8%, gold $3,544.54; Cormann;
    Matthew Wale; Muhammad Zeeshan Ali; Shenzhou-24 18th crewed flight;
    Honiara; Pongkor "3 dead, 23 still trapped"; Bangladesh 12,500 ->
    17,000 taka; Ofgem cap 2,166 pounds; EU 50bn euro fund PROPOSED;
    UN 47,000; Malaysia 787 (10 firm + 6 options).
  * Pin 12 (Brussels) back on TRUE Brussels (4.35, 50.85): v4 had pushed
    it ~300 km east near Frankfurt to separate it from pin 11 (London).
    Now a small dot sits on Brussels itself, with a leader line to an
    offset "12" badge so the two London/Brussels markers stay readable.
  * Pin 3 (Hormuz) moved to the true strait mouth (56.3, 26.3), its
    circle straddling the channel and touching both coasts, plus a
    "HORMUZ" micro-label so it reads as the strait, not a stray sea pin.
  * Map: Italy gets its boot (Europe polygon dips to lat 38.8 at lon 16)
    plus a Sicily dot; the Red Sea gap is widened in its northern half
    (Arabia's west edge east, Africa's NE edge west) while Hodeidah's
    pin stays on land; Arabia kept as its own peninsula. Map stays
    155px tall with the title line above the box.
  * The four "(Tue 24)" ALSO items are gone, replaced by verified
    Wednesday stories (see ALSO notes): Cormann/OECD chip report in
    Jakarta (ANTARA, 05:25 UTC), US tariffs on 14 partners (Reuters),
    Kremlin rejects Johnson token force (Reuters), Ebola teams flee
    Ituri fighting (AP). No story on the page is flagged Tue 24 any
    more; the only Tue/Mon dates left are inside FOLLOW-UP, which is
    explicitly Wednesday developments of Tuesday stories. Region counts
    recount to ASIA 11, AMERICAS 7, AFRICA 6, EUROPE 5, MIDDLE EAST 3,
    PACIFIC 2, WORLD 1. "Tue night" dropped from the Damazin item.
  * Numbers tightened to the verified closes: Kospi -6.16% (headline,
    strip, timeline, deck) at 4,697.51; Samsung -9.87%, Hynix -11.05%,
    SoftBank -14.8%, gold $3,544.54 all re-checked and unchanged.
  * Timeline labels all measured to fit with no ellipsis anywhere.

v4 vs v3 - CONTENT FROZEN (all 35 stories, texts, numbers, labels,
sources identical); only the map geometry changed, because Nero reported
the v3 map looked covered up (and the 2x crop proved him right):
  * Map 88px -> 155px tall, lat window 84..-58 so no northern land is
    cut at the top edge; the "WHERE IT HAPPENED" title moved OUT of the
    map box to its own line above it (in v3 the navy tab sat inside the
    box and covered Alaska / northern Canada).
  * Pins 11 (London) and 12 (Brussels) were 19px apart with 16px circles
    and the same teal colour, so they read as one blob: pin 12 moved east
    to (10.0, 49.0), 27px from pin 11, and the EUROPE label moved to
    (26, 57) so it no longer crowds the pins.
  * Pin placement checked point-in-polygon against the continent shapes:
    6 of 13 pins sat in the sea. Fixed by redrawing the coasts, not by
    moving the stories: Europe's south edge now runs to the Mediterranean
    (pin 12 on land); N. America's east coast now bulges through NYC
    (pin 13 on land); Arabia is its own peninsula polygon with a real Red
    Sea gap (pin 6 on land); Africa's south coast now reaches the Cape
    (pin 9 on land); Indonesia + Solomon Islands polygons added (pins 4
    and 5 on land). Pin 3 (Hormuz) stays in the strait: the strait IS
    water, and the pin sits on its coast.
  * Layout rebalanced to pay for the taller map (masthead 54, strip 34,
    lead 59, grid cards 50, tighter timeline / region bar / ALSO rows):
    final y still 1008, same as v3.

v3 vs v2 — what changed and why (every change traces to a verified fact):
  * Visual identity: v2 copied the classic cream broadsheet. v3 is "the night
    desk": a solid navy masthead band, white sans masthead, navy section
    tabs, amber FOLLOW-UP panel. Same paper, different paper.
  * Lead card: the #1 story (Shenzhou-24) gets a full-width lead card with a
    large navy icon panel, then 12 grid cards (13 illustrated stories).
  * Dates fixed: Pongkor is "3 dead, 23 still trapped" (v2 said "26 trapped");
    the Dow's first close above 50,000 was Tuesday 24, so it moved out of the
    number strip into FOLLOW-UP; the Houthi card no longer mixes Tuesday's
    PIF tower attack (11 hurt) with Wednesday's Hodeidah strikes.
  * Numbers fixed: Kospi close -6.16% at 4,697.51, Samsung -9.87%, SK Hynix
    -11.05%, SoftBank -14.8% (WSJ, not -14.1%), gold $3,544.54 at 00:24 GMT
    (not $3,344); Nikkei/Taiex/Shanghai closes DROPPED (conflicting or
    unverified); "Nvidia +31.5% surge" DROPPED (unverified).
  * Names fixed: astronaut Muhammad Zeeshan Ali (full name); Shenzhou-24 is
    China's 18th crewed flight (not "41st"); Honiara (not HOMARA); Hamas
    official Mohammad Abuelouf per Reuters (Xinhua spells it Mohammed Abu
    al-Ouf); Zimbabwean is Wesley Sothole per BBC + NPA list (Al Jazeera
    spells it Tafadzwa Sithole — discrepancy noted, BBC followed).
  * Honest wire cutoff: "WIRES READ TO 14:00 UTC" (v7: raised from 12:00,
    which the page's own content contradicted). Every story on the page
    happened or was reported before 14:00 UTC — latest is the Reuters
    tariffs update ~13:44 UTC — except items flagged in the text with
    their real date (Tue 24 / Mon 23) or marked DUE TODAY.
  * Conflicting estimates shown honestly: Russian war dead 490,000 registered
    vs ~700,000 with the missing (Meduza/Mediazona, out Mon 23); Sudan toll
    19 (rights group) vs 14 (hospital); Malaysia 787: 10 firm + 6 options.
  * Africa: 9 of 35 stories (v2 had 2 of 40; top-10 entries had as few as 1).
  * FOLLOW-UP box (bagarte method): Tuesday stories carried only by their
    Wednesday development. DATE CHECK lists what was left out, with dates.
  * HOW SURE legend now DEFINES the labels instead of just naming them.
  * Ruthless proofreading: every ALSO one-liner below has a checkable source.
    Items v2 carried that could not be re-verified (Pope/COP31 comment, Dell
    Q3, Poland US base, Lebanon airport, Canada student curbs, Rosneft
    refineries, NATO Baltic scramble, Taiex/Hang Seng/Shanghai closes) were
    CUT, not carried. 35 stories, all verified, beats 40 with fabrications.

Layout (1024x1024, flow top to bottom):
  navy masthead -> 3-headline sub-deck -> big-number strip -> map title
  line -> world map with numbered pins (155px) -> lead card -> 12
  illustrated stories (2-col grid) -> UTC timeline -> region bar -> ALSO
  ON (22 one-liners, 2 cols) -> FOLLOW-UP -> DATE CHECK + legend + sources.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 30                      # side margin
CW = W - 2 * MX              # content width = 964
PAPER = (244, 241, 234)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (20, 33, 61)
NAVY_DARK = (13, 22, 41)
GOLD = (232, 163, 61)
GREY = (90, 86, 80)
LGREY = (200, 194, 184)
RULE = (17, 17, 17)
CARD_BG = (255, 255, 255)
DARK = (26, 26, 26)
GREEN = (28, 122, 48)
TEAL = (0, 110, 110)
OCHRE = (176, 118, 0)
OCEAN = (220, 230, 240)
LAND = (233, 224, 199)
LAND_LINE = (150, 140, 110)
FOLLOW_BG = (255, 244, 214)

CONF_COLOR = {"OFFICIAL": TEAL, "CONFIRMED": GREEN, "REPORTED": OCHRE,
              "CLAIM": RED}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap_to(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap, capped at max_lines (last line ellipsised)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit(draw, lines[-1], fnt, max_w)
    return lines


# ---------------------------------------------------------------- stories
# LEAD: (n, region, tag, headline, deck, confidence, source, icon, (lon, lat))
# Verified: CMSA/Xinhua + Reuters, 25 Nov 2026. Launch 00:18 UTC, docking
# 03:56 UTC, hatch opened 06:35 UTC. Ali, 40, Pakistani Air Force pilot,
# payload specialist, first Pakistani in orbit, first foreigner on Tiangong.
# 18th crewed Chinese spaceflight, 24th Shenzhou flight overall.
LEAD = (1, "ASIA", "SPACE",
        "Pakistan's first astronaut docks at China's Tiangong station",
        "Shenzhou-24 launched 00:18 UTC and docked 03:56 UTC. Muhammad "
        "Zeeshan Ali, 40, is the first Pakistani in orbit and the first "
        "foreigner aboard Tiangong \u2014 China's 18th crewed flight.",
        "CONFIRMED", "CMSA / Reuters", "rocket", (100, 41))

# n, region, tag, headline, deck, confidence, source, icon, (lon, lat) pin
TOP = [
    (2, "ASIA", "MARKETS",
     "Asia's chip rout: Kospi crashes 6.16% to a 10-month low",
     "4,697.51; Samsung -9.87%, Hynix -11.05%; erases Tue's +6.3%.",
     "CONFIRMED", "Korea Exchange", "chart", (127, 37.5)),
    (3, "MIDDLE EAST", "ENERGY",
     "Two more tankers hit mines and burn in the Strait of Hormuz",
     "IRGC claim: unauthorised route, AIS off; no names given, unverified.",
     "CLAIM", "IRGC / Reuters", "tanker", (56.3, 26.3)),
    (4, "PACIFIC", "SECURITY",
     "Solomons name Australia top security partner; no foreign base",
     "Signed in Canberra; Honiara vows no foreign base; A$740m/10 yrs.",
     "CONFIRMED", "AP", "treaty", (160, -9.5)),
    (5, "ASIA", "DISASTER",
     "Three dead, 23 still trapped in flooded Java gold mine",
     "Bodies found Wednesday; flood burst in Monday; Antam disowns the pit.",
     "CONFIRMED", "Reuters", "mine", (106.8, -6.6)),
    (6, "MIDDLE EAST", "WAR",
     "Coalition hits Hodeidah port and airport after warning",
     "4 drones downed at Ras Tanura; Houthis claim fires, threaten Jeddah, Yanbu.",
     "REPORTED", "SPA / Al Jazeera", "refinery", (44, 14.5)),
    (7, "AMERICAS", "RESCUE",
     "All supermarket hostages freed in pre-dawn Cartagena raid",
     "Raid at 01:30 frees about 30; one captor killed, four detained.",
     "CONFIRMED", "Reuters", "building", (-75.5, 10.4)),
    (8, "ASIA", "LABOUR",
     "Bangladesh raises garment wages 36% after weeks of protests",
     "Board votes 4-2; 17,000 taka from 12,500; workers wanted 18,000.",
     "CONFIRMED", "Reuters", "factory", (90.4, 23.8)),
    (9, "AFRICA", "COURTS",
     "Court scraps Phala Phala report; Ramaphosa impeachment ends",
     "High Court: 2022 panel exceeded its mandate; report unlawful in full.",
     "CONFIRMED", "Court judgment", "scales", (18.4, -33.9)),
    (10, "AFRICA", "OBITUARY",
     "Pete Edochie dies at 79: 'An Iroko Has Fallen'",
     "Nollywood's Okonkwo dies 00:30 in Enugu of prostate cancer, aged 79.",
     "CONFIRMED", "Family statement", "tree", (7.5, 6.4)),
    (11, "EUROPE", "ENERGY",
     "UK energy bills to rise 26% as Ofgem lifts price cap to \u00a32,166",
     "From \u00a31,723, up \u00a3443 a year from January; about 20m households hit.",
     "OFFICIAL", "Ofgem", "bolt", (-0.1, 51.5)),
    (12, "EUROPE", "TECH",
     "EU proposes \u20ac50bn tech fund to cut reliance on US and China",
     "\u20ac50bn is a target scale, not committed cash; details due in February.",
     "OFFICIAL", "EU Commission", "chip", (4.35, 50.85)),
    (13, "WORLD", "RIGHTS",
     "47,000 women killed by partners or family in 2025, UN says",
     "Five an hour, 129 a day; brief released for today's International Day.",
     "OFFICIAL", "UN", "candle", (-74, 40.7)),
]

# n, region, text, source, confidence
# v6: #14, #31, #33 replaced to restore Africa to 9 (see v6 docstring).
# 14: AP, 25 Nov — Proteas beat Bangladesh by an innings and 219 runs at
# Centurion, series 2-0; Mulder 7-31 + century; result before tea on day 3.
# 31: Reuters/SENS, 25 Nov — Naspers interim results released 07:50 SAST:
# revenue $6.37bn (+55%), adjusted EPS 240 US cents (+12% from 215),
# driven by Tencent; aEBITDA down 6.4% to $405m. 33: People Daily, 25 Nov
# — Germany commits EUR 52.5m (Ksh7.8bn) in development cooperation to
# Kenya for 2026-2028 after Ruto-Steinmeier talks at State House, Nairobi.
# Cut: Sterling suspended term, Nvidia -5.9% Tue, MAG extra 737 orders.
# v5: no ALSO item is flagged Tue 24 any more. The four Tue-24 items
# (#19-22) were replaced by verified Wednesday stories: 19: OECD/ANTARA,
# 25 Nov — Cormann launches the semiconductor-ecosystem report in Jakarta
# with Airlangga Hartarto (ANTARA photo 12:25 GMT+7 = 05:25 UTC); review
# covers 25 accession areas. 20: Reuters, 25 Nov — Trump administration
# proposes new tariffs on 14 partners over excess capacity; highest rates
# on China. 21: Reuters, 25 Nov — Kremlin rejects ex-PM Johnson's call
# for a token Western force in Ukraine. 22: AP, 25 Nov — fighting forces
# Ebola teams out of Ituri; WHO moves Mongbwalu staff to Bunia; ~a dozen
# incl. 2 WHO staff evacuated to Bunia after 3 days trapped in Akwe.
# 15: Reuters, 25 Nov — Abuelouf (Reuters spelling; Xinhua: Mohammed Abu
# al-Ouf, 47). Second Hamas security chief killed in 24 hours; Tuesday's
# victim was Naim Abu Nahal. 16: Reuters, 25 Nov — overnight attack; DTEK
# plant halted, Naftogaz site ablaze; 1 killed in Kyiv region, 2 women
# wounded in Odesa; Zaporizhzhia plant off grid a 17th time. 17: Reuters,
# 25 Nov — strikes in Damazin; Emergency Lawyers say 19 dead, hospital
# source says 14 (the toll was reported Wednesday; "Tue night" dropped).
ALSO = [
    (14, "AFRICA", "Proteas beat Bangladesh by innings, 219 runs; sweep 2-0", "AP", "CONFIRMED"),
    (15, "MIDDLE EAST", "Israeli strike kills Hamas chief Mohammad Abuelouf, wife, children", "Reuters", "REPORTED"),
    (16, "EUROPE", "Russian strikes cut power in five Ukraine regions; gas site ablaze", "Reuters", "REPORTED"),
    (17, "AFRICA", "RSF drones kill 19 in Damazin; hospital puts toll at 14", "Reuters", "REPORTED"),
    (18, "AFRICA", "Tanzania joins OECD Africa forum in Paris; finance chief leads team", "OECD", "REPORTED"),
    (19, "ASIA", "Cormann launches OECD chip report in Jakarta; 25 areas reviewed", "OECD", "REPORTED"),
    (20, "AMERICAS", "US proposes new tariffs on 14 partners; China hit hardest", "Reuters", "REPORTED"),
    (21, "EUROPE", "Kremlin rejects Johnson's call for token force in Ukraine", "Reuters", "REPORTED"),
    (22, "AFRICA", "Fighting forces Ebola teams out of Ituri; WHO shifts staff to Bunia", "AP", "REPORTED"),
    (23, "ASIA", "Malaysia Airlines commits to 10 Boeing 787-10s, option for 6 more", "Boeing", "OFFICIAL"),
    (24, "ASIA", "SoftBank -14.8%, Kioxia -14.2% as Tokyo joins the AI rout", "WSJ", "CONFIRMED"),
    (25, "AMERICAS", "Nasdaq -1.5% Tue, now 14.2% off its high; S&P 500 -0.5%", "WSJ", "CONFIRMED"),
    (26, "AMERICAS", "Micron -11.0% Tue; SK Hynix -11.05% Wed", "Yonhap", "CONFIRMED"),
    (27, "ASIA", "First China-foreign 'space handshake' aboard Tiangong, 06:35 UTC", "CMSA", "CONFIRMED"),
    (28, "ASIA", "Antam: Bogor mine was unauthorised, not part of our operations", "Reuters", "REPORTED"),
    (29, "PACIFIC", "Wale survived a no-confidence motion in September", "The Times", "REPORTED"),
    (30, "ASIA", "Samsung's market value slips below 1,000 trillion won", "SE Daily", "CONFIRMED"),
    (31, "AFRICA", "Naspers half-year earnings up 12% on Tencent", "Reuters", "CONFIRMED"),
    (32, "AMERICAS", "US data pile due today: PCE, GDP, jobless claims (DUE TODAY)", "Data calendar", "REPORTED"),
    (33, "AFRICA", "Germany commits \u20ac52.5m to Kenya after Ruto talks", "People Daily", "CONFIRMED"),
    (34, "AFRICA", "ATM vows to challenge Ramaphosa court ruling", "AT News", "REPORTED"),
    (35, "AMERICAS", "Cartagena raid: one agent injured; president hails troops in 01:30 video", "AP", "REPORTED"),
]

NUMBERS = [
    ("-6.16%", "KOSPI \u00b7 SEOUL", "closes 4,697.51"),
    ("-14.8%", "SOFTBANK \u00b7 TOKYO", "WSJ close"),
    ("$3,544.54", "GOLD \u00b7 SPOT", "per oz, 00:24 GMT"),
    ("+36%", "DHAKA WAGES", "17,000 taka / mo"),
]

TIMELINE = [
    ("20:00 TUE", "Dhaka board votes +36%"),
    ("00:18", "Shenzhou-24 launches"),
    ("03:56", "Docking at Tiangong"),
    ("06:30", "Kospi closes -6.16%"),
    ("06:35", "First space handshake"),
    ("09:46", "Hormuz blasts reported"),
]

REGIONS = [  # name, count, colour — counted from LEAD + TOP + ALSO
    ("ASIA", 10, (185, 28, 28)),
    ("AMERICAS", 6, (28, 122, 48)),
    ("AFRICA", 9, (120, 80, 40)),
    ("EUROPE", 4, (36, 84, 160)),
    ("MIDDLE EAST", 3, (222, 120, 20)),
    ("PACIFIC", 2, (0, 130, 135)),
    ("WORLD", 1, (110, 110, 110)),
]

# Tuesday stories carried only by their Wednesday development (bagarte method).
FOLLOW_UP = [
    ("Dow closes above 50,000 for the first time", "Tue 24 \u00b7 50,018.70"),
    ("Shanghai pledges loyalty after Chen probe", "probe Tue 24 \u00b7 pledge Wed 25"),
    ("Sparta II: Zelenskiy confirms Ukraine hit the ship Sat 21", "interview out Tue 24"),
    ("Russian war dead: 490,000 registered, ~700,000 with missing", "Mon 23"),
]

DATE_CHECK = [
    ("Huawei convicted in US", "24 Nov"),
    ("PIF tower attack, Riyadh", "24 Nov"),
    ("Chen Jining probe announced", "24 Nov"),
    ("Merkury sunk off Benghazi", "22 Nov"),
    ("COP31 talks collapse", "22 Nov"),
    ("Giuliani Medal of Freedom", "24 Nov"),
    ("Sarkozy & Bruni to trial", "24 Nov"),
    ("Ukraine ships hit off Libya", "23 Nov"),
    ("ICJ: Myanmar guilty of genocide", "19 Nov"),
]

# Simplified continent polygons (lon, lat), equirectangular.
# v5: Italy boot added (Europe dips to lat 38.8 at lon 16) + Sicily dot;
# Red Sea gap widened in its northern half (Arabia's west edge 38.5->39.5
# at lat 22 and 41->42 at lat 18; Africa's NE edge 37->36.5 and 39.5->39),
# southern strait left narrow as in reality; Hodeidah's pin still on land.
# Pin 12 is drawn at TRUE Brussels (4.35, 50.85) with a leader line to an
# offset badge; pin 3 sits at the true strait mouth (56.3, 26.3).
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-74, 39), (-77, 35),
     (-80, 35), (-85, 30),
     (-90, 20), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-158, 58), (-168, 66)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-55, 76), (-60, 70), (-55, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-50, -30), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-73, -25),
     (-77, -12), (-80, 10)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (36.5, 22), (39, 17), (42, 11.5), (46, 11), (51, 11), (48, 0),
     (40, -10), (35, -20), (30, -30),
     (20, -35), (18, -34), (15, -30), (12, -18), (9, 0), (9, 4), (-8, 5),
     (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (3, 50), (7, 49), (10, 47),
     (12, 44), (13.5, 42), (15, 40), (16, 38.8), (17.5, 39.5), (18.5, 41),
     (19, 42), (23, 40), (26, 40), (28, 41), (30, 42),
     (30, 62), (30, 70), (25, 71),
     (18, 69), (12, 65), (5, 60), (-5, 58), (-10, 54), (-10, 43), (-10, 36)],
    # Sicily (tiny dot south of the boot's toe)
    [(13, 37), (16, 37), (16, 38.2), (13, 38.2)],
    [(30, 62), (40, 68), (60, 69), (75, 73), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
     (140, 40), (130, 35), (127, 33), (120, 30), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (75, 10), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (43, 29), (40, 31),
     (35, 36), (30, 36), (30, 42), (30, 62)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (136, -12), (132, -12), (126, -14),
     (122, -17), (118, -20), (113, -22)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
     (140, 44), (138, 40), (135, 36), (132, 33), (130, 31)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-5, 50)],
    # Arabia (own peninsula; Red Sea gap to Africa's new coast)
    [(35, 29), (39.5, 22), (42, 18), (42.5, 15), (43.5, 12.5), (45, 12),
     (48, 13), (52, 16), (55, 17), (58, 22), (57, 25), (55, 26), (52, 26),
     (50, 29), (48, 29), (43, 29), (40, 31), (35, 31), (35, 29)],
    # Indonesia: Sumatra, Java, Borneo, Sulawesi, New Guinea
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -4),
     (100, 1), (96, 4), (95, 5)],
    [(105, -6), (107, -6), (110, -7), (114, -8), (114, -9), (108, -8),
     (105, -7), (105, -6)],
    [(109, 1), (111, 3), (113, 4), (117, 6), (119, 1), (117, -2),
     (114, -4), (110, -3), (109, 1)],
    [(119, 0), (121, 1), (123, 0), (121, -2), (119, -3), (119, 0)],
    [(131, -1), (136, -2), (141, -3), (141, -8), (136, -8), (132, -4),
     (131, -1)],
    # Solomon Islands
    [(156, -7), (160, -6), (163, -9), (161, -11), (157, -10), (156, -7)],
]
MAP_LABELS = [("N. AMERICA", -100, 47), ("S. AMERICA", -60, -15),
              ("AFRICA", 22, 0), ("EUROPE", 26, 57), ("ASIA", 100, 58),
              ("AUSTRALIA", 134, -25)]


# ---------------------------------------------------------------- icons
def draw_icon(d, kind, x, y, s):
    """Draw a small pictogram for a story inside the (x, y, s, s) box."""
    cx, cy = x + s // 2, y + s // 2
    if kind == "rocket":
        d.polygon([(cx, y + 3), (cx + 7, y + 16), (cx + 7, y + 34),
                   (cx - 7, y + 34), (cx - 7, y + 16)], fill=(200, 205, 210))
        d.polygon([(cx - 7, y + 26), (cx - 13, y + 36), (cx - 7, y + 36)],
                  fill=RED)
        d.polygon([(cx + 7, y + 26), (cx + 13, y + 36), (cx + 7, y + 36)],
                  fill=RED)
        d.ellipse([cx - 3, y + 12, cx + 3, y + 18], fill=(36, 84, 160))
        d.polygon([(cx - 4, y + 36), (cx + 4, y + 36), (cx, y + 44)],
                  fill=(230, 130, 20))
        for sx, sy in [(x + 4, y + 6), (x + s - 6, y + 10), (x + 8, y + 38)]:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(120, 120, 120))
    elif kind == "chart":
        d.line([x + 5, y + 5, x + 5, y + s - 6, x + s - 4, y + s - 6],
               fill=INK, width=2)
        pts = [(x + 7, y + 10), (x + 15, y + 16), (x + 22, y + 14),
               (x + 30, y + 26), (x + 38, y + 36)]
        d.line(pts, fill=RED, width=3)
        for px, py in pts:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    elif kind == "tanker":
        d.rectangle([x + 4, y + 22, x + s - 4, y + 32], fill=(90, 60, 40))
        d.rectangle([x + 8, y + 14, x + 16, y + 22], fill=(120, 120, 120))
        d.rectangle([x + 20, y + 16, x + 30, y + 22], fill=(36, 84, 160))
        for i in range(3):
            d.line([x + 4 + i * 14, y + 36, x + 12 + i * 14, y + 36],
                   fill=(36, 84, 160), width=2)
        for dx, dy in [(0, -6), (7, -9), (-7, -9), (0, 0)]:
            d.line([cx + dx, y + 8 + dy, cx + dx, y + 16 + dy],
                   fill=(230, 130, 20), width=2)
        d.ellipse([cx - 3, y + 2, cx + 3, y + 8], fill=(230, 130, 20))
    elif kind == "treaty":
        d.rectangle([x + 10, y + 6, x + s - 10, y + s - 8], fill=CARD_BG,
                    outline=INK, width=2)
        for i in range(3):
            d.line([x + 14, y + 14 + i * 6, x + s - 14, y + 14 + i * 6],
                   fill=GREY, width=2)
        d.ellipse([cx - 6, y + s - 14, cx + 6, y + s - 2], fill=RED)
        d.ellipse([cx - 2, y + s - 10, cx + 2, y + s - 6], fill=(255, 220, 120))
    elif kind == "mine":
        d.polygon([(x + 10, y + 4), (x + s - 10, y + 4), (x + s - 6, y + s - 4),
                   (x + 6, y + s - 4)], fill=(96, 78, 58))
        d.line([x + 14, y + 10, x + 14, y + s - 6], fill=(190, 160, 110), width=2)
        d.line([x + s - 14, y + 10, x + s - 14, y + s - 6], fill=(190, 160, 110),
               width=2)
        for i in range(4):
            d.line([x + 12, y + 14 + i * 8, x + s - 12, y + 14 + i * 8],
                   fill=(190, 160, 110), width=2)
        d.ellipse([cx - 7, cy - 3, cx + 7, cy + 11], fill=(230, 190, 40))
        d.ellipse([cx - 2, cy + 1, cx + 2, cy + 5], fill=(255, 240, 150))
    elif kind == "factory":
        d.rectangle([x + 6, y + 18, x + s - 6, y + s - 6], fill=(120, 120, 125))
        d.polygon([(x + 6, y + 18), (x + 14, y + 10), (x + 22, y + 18),
                   (x + 30, y + 10), (x + s - 6, y + 18)], fill=(90, 90, 95))
        d.rectangle([x + 10, y + 6, x + 14, y + 16], fill=(90, 90, 95))
        d.rectangle([x + 12, y + 28, x + 18, y + 34], fill=(255, 220, 120))
        d.rectangle([x + 26, y + 28, x + 32, y + 34], fill=(255, 220, 120))
        d.rectangle([x + 12, y + 38, x + 32, y + s - 6], fill=(70, 70, 75))
    elif kind == "refinery":
        d.rectangle([x + 8, y + 14, x + 14, y + s - 6], fill=(120, 120, 125))
        d.rectangle([x + 18, y + 20, x + 24, y + s - 6], fill=(120, 120, 125))
        d.rectangle([x + 28, y + 10, x + 34, y + s - 6], fill=(150, 150, 155))
        d.ellipse([x + 30, y + 2, x + 36, y + 8], fill=(230, 130, 20))
        d.line([x + 6, y + s - 6, x + s - 4, y + s - 6], fill=INK, width=2)
        d.line([x + 14, y + 24, x + 28, y + 24], fill=(90, 90, 90), width=2)
    elif kind == "building":
        d.rectangle([x + 10, y + 8, x + s - 10, y + s - 6], fill=(150, 140, 130))
        for r in range(3):
            for c in range(3):
                d.rectangle([x + 14 + c * 9, y + 12 + r * 10,
                             x + 20 + c * 9, y + 18 + r * 10],
                            fill=(255, 220, 120))
        d.polygon([(cx, y + 2), (cx + 3, y + 6), (cx, y + 10), (cx - 3, y + 6)],
                  fill=RED)
    elif kind == "bolt":
        d.polygon([(cx + 4, y + 4), (cx - 6, y + 24), (cx - 1, y + 24),
                   (cx - 4, y + s - 4), (cx + 7, y + 20), (cx + 1, y + 20)],
                  fill=(230, 180, 20))
        d.rectangle([x + 8, y + s - 8, x + s - 8, y + s - 4], fill=GREY)
    elif kind == "scales":
        # courthouse scales: post, crossbar, two hanging pans, base
        d.line([cx, y + 6, cx, y + s - 10], fill=INK, width=2)
        d.line([x + 8, y + 10, x + s - 8, y + 10], fill=INK, width=2)
        d.ellipse([cx - 3, y + 3, cx + 3, y + 9], fill=GOLD)
        for px in (x + 8, x + s - 8):
            d.line([px, y + 10, px - 6, y + 22], fill=INK, width=1)
            d.line([px, y + 10, px + 6, y + 22], fill=INK, width=1)
            d.polygon([(px - 8, y + 22), (px + 8, y + 22), (px, y + 30)],
                      fill=GOLD)
        d.line([cx - 10, y + s - 8, cx + 10, y + s - 8], fill=INK, width=3)
        d.line([cx - 14, y + s - 4, cx + 14, y + s - 4], fill=INK, width=2)
    elif kind == "tree":
        # iroko tree: trunk + three-canopy crown (for the Edochie obituary)
        d.rectangle([cx - 3, y + 22, cx + 3, y + s - 6], fill=(96, 66, 40))
        d.ellipse([x + 4, y + 4, x + s - 4, y + 26], fill=(34, 110, 54))
        d.ellipse([x + 8, y + 12, cx + 6, y + 30], fill=(46, 130, 66))
        d.ellipse([cx - 6, y + 12, x + s - 8, y + 30], fill=(46, 130, 66))
        d.line([x + 6, y + s - 6, x + s - 6, y + s - 6], fill=(96, 66, 40),
               width=2)
    elif kind == "chip":
        # processor: dark square, inner die, pins on all four sides
        d.rectangle([x + 10, y + 10, x + s - 10, y + s - 10], fill=NAVY)
        d.rectangle([x + 16, y + 16, x + s - 16, y + s - 16],
                    outline=GOLD, width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
        for i in range(3):
            off = 14 + i * 8
            d.line([x + 4, y + off, x + 10, y + off], fill=INK, width=2)
            d.line([x + s - 10, y + off, x + s - 4, y + off], fill=INK, width=2)
            d.line([x + off, y + 4, x + off, y + 10], fill=INK, width=2)
            d.line([x + off, y + s - 10, x + off, y + s - 4], fill=INK, width=2)
    elif kind == "candle":
        # memorial candle: flame + wax body + saucer
        d.polygon([(cx, y + 2), (cx + 4, y + 10), (cx, y + 16), (cx - 4, y + 10)],
                  fill=(230, 130, 20))
        d.ellipse([cx - 2, y + 8, cx + 2, y + 12], fill=(255, 220, 120))
        d.rectangle([cx - 6, y + 16, cx + 6, y + s - 8], fill=(240, 236, 226),
                    outline=(180, 175, 165), width=1)
        d.line([cx - 10, y + s - 6, cx + 10, y + s - 6], fill=GOLD, width=3)


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 8

    # ---------- masthead: solid navy band (v3 identity, kept) ----------
    d.rectangle([MX, y, W - MX, y + 54], fill=NAVY)
    tf = font(SANS_B, 28)
    title = "THE WORLD WIRE"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y + 3), title, font=tf, fill=(255, 255, 255))
    sf = font(SANS_B, 11)
    sub = ("THE WORLD IN ONE PAGE  \u00b7  WEDNESDAY, 25 NOVEMBER 2026  "
           "\u00b7  35 STORIES  \u00b7  WIRES READ TO 14:00 UTC")
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, y + 34), sub, font=sf, fill=GOLD)
    y += 54
    d.rectangle([MX, y, W - MX, y + 3], fill=RED)
    y += 3 + 4

    # ---------- sub-deck: top 3 headlines ----------
    deck_f = font(SANS_B, 13)
    top3 = [
        "1  Pakistan's first astronaut docks at China's Tiangong station",
        "2  Asia's chip rout: Kospi crashes 6.16% to a 10-month low",
        "3  Two more tankers hit mines and burn in the Strait of Hormuz",
    ]
    for line in top3:
        d.text((MX, y), line, font=deck_f, fill=INK)
        y += 14
    y += 3

    # ---------- big-number strip (all Wednesday closes) ----------
    strip_y = y
    bw = (CW - 3 * 8) // 4
    for i, (num, lab, sub2) in enumerate(NUMBERS):
        bx = MX + i * (bw + 8)
        d.rectangle([bx, strip_y, bx + bw, strip_y + 34], fill=NAVY)
        nf = font(SANS_B, 22)
        d.text((bx + 10, strip_y + 7), num, font=nf, fill=GOLD)
        nx = bx + 10 + d.textlength(num, font=nf) + 8
        lf = font(SANS_B, 10)
        d.text((nx, strip_y + 8), lab, font=lf, fill=(255, 255, 255))
        sf2 = font(SANS, 9)
        d.text((nx, strip_y + 22), sub2, font=sf2, fill=(190, 186, 176))
    y = strip_y + 34 + 3

    # ---------- world map: title ABOVE the box (v4: v3's navy tab sat
    # inside the box and covered Alaska / northern Canada) ----------
    d.text((MX, y), "WHERE IT HAPPENED \u2014 13 STORIES, PINNED",
           font=font(SANS_B, 11), fill=NAVY)
    y += 12
    map_x, map_y, map_w, map_h = MX, y, CW, 155
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN,
                outline=NAVY, width=1)

    def project(lon, lat):
        px = map_x + (lon + 180) / 360.0 * map_w
        py = map_y + (84 - lat) / 142.0 * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for name, lon, lat in MAP_LABELS:
        px, py = project(lon, lat)
        lf = font(SANS_B, 9)
        d.text((px - d.textlength(name, font=lf) / 2, py - 5), name,
               font=lf, fill=(110, 105, 90))
    for (n, _reg, _tag, _h, _de, conf, _s, _ic, (lon, lat)) in [LEAD] + TOP:
        px, py = project(lon, lat)
        col = CONF_COLOR[conf]
        if n == 12:
            # TRUE Brussels: a small dot on the city, leader line to an
            # offset number badge (v4 moved the pin itself to Frankfurt).
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col,
                      outline=(255, 255, 255), width=2)
            bx, by = px + 19, py - 2
            d.line([px + 4, py, bx - 7, by], fill=(255, 255, 255), width=4)
            d.line([px + 4, py, bx - 7, by], fill=col, width=2)
            d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=col,
                      outline=(255, 255, 255), width=2)
            nf = font(SANS_B, 8)
            t = "12"
            d.text((bx - d.textlength(t, font=nf) / 2, by - 5), t, font=nf,
                   fill=(255, 255, 255))
            continue
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col,
                  outline=(255, 255, 255), width=2)
        nf = font(SANS_B, 9 if n < 10 else 8)
        t = str(n)
        d.text((px - d.textlength(t, font=nf) / 2, py - 5), t, font=nf,
               fill=(255, 255, 255))
        if n == 3:
            # Strait label: the pin sits in the channel itself.
            hf = font(SANS_B, 8)
            d.text((px + 9, py + 7), "HORMUZ", font=hf, fill=(70, 80, 95))
    y = map_y + map_h + 4

    # ---------- lead card (full width, big navy icon panel) ----------
    (n, region, tag, head, deck, conf, src, icon, _pin) = LEAD
    cy = y
    d.rectangle([MX, cy, W - MX, cy + 59], fill=CARD_BG, outline=NAVY, width=1)
    d.rectangle([MX + 4, cy + 2, MX + 60, cy + 58], fill=NAVY)
    draw_icon(d, icon, MX + 4, cy + 2, 56)
    tx = MX + 68
    twd = CW - 68 - 8
    col = CONF_COLOR[conf]
    tag_f = font(SANS_B, 10)
    d.text((tx, cy + 4), f"{n} \u00b7 {region} \u2014 {tag}", font=tag_f, fill=RED)
    srf = font(SANS, 9)
    d.text((tx + d.textlength(f"{n} \u00b7 {region} \u2014 {tag}", font=tag_f) + 8,
            cy + 5), src, font=srf, fill=GREY)
    bf = font(SANS_B, 9)
    bw2 = d.textlength(conf, font=bf) + 8
    d.rectangle([W - MX - 8 - bw2, cy + 4, W - MX - 8, cy + 15], fill=col)
    d.text((W - MX - 8 - bw2 + 4, cy + 5), conf, font=bf, fill=(255, 255, 255))
    hf = font(SANS_B, 16)
    d.text((tx, cy + 16), fit(d, head, hf, twd), font=hf, fill=INK)
    df = font(SANS, 11)
    dlines = wrap_to(d, deck, df, twd, 2)
    ly = cy + 35
    for ln in dlines:
        d.text((tx, ly), ln, font=df, fill=(70, 66, 60))
        ly += 12
    y = cy + 59 + 4

    # ---------- illustrated top-12 grid ----------
    gap = 10
    colw = (CW - gap) // 2
    card_h, card_gap = 50, 3
    for i, (n, region, tag, head, deck, conf, src, icon, _pin) in enumerate(TOP):
        cx = MX + (i % 2) * (colw + gap)
        cy = y + (i // 2) * (card_h + card_gap)
        d.rectangle([cx, cy, cx + colw, cy + card_h], fill=CARD_BG,
                    outline=LGREY, width=1)
        ix, iy = cx + 4, cy + 4
        d.rectangle([ix, iy, ix + 44, iy + 44], fill=(244, 240, 232),
                    outline=LGREY, width=1)
        draw_icon(d, icon, ix, iy, 44)
        tx = cx + 54
        twd = colw - 54 - 8
        col = CONF_COLOR[conf]
        tag_f = font(SANS_B, 9)
        tag_txt = f"{n} \u00b7 {region} \u2014 {tag}"
        d.text((tx, cy + 3), tag_txt, font=tag_f, fill=RED)
        srf = font(SANS, 9)
        d.text((tx + d.textlength(tag_txt, font=tag_f) + 6, cy + 4), src,
               font=srf, fill=GREY)
        bf = font(SANS_B, 9)
        bw2 = d.textlength(conf, font=bf) + 8
        d.rectangle([cx + colw - 8 - bw2, cy + 3, cx + colw - 8, cy + 14],
                    fill=col)
        d.text((cx + colw - 8 - bw2 + 4, cy + 4), conf, font=bf,
               fill=(255, 255, 255))
        hf = font(SANS_B, 13)
        lines = wrap_to(d, head, hf, twd, 2)
        ly = cy + 13
        for ln in lines:
            d.text((tx, ly), ln, font=hf, fill=INK)
            ly += 13
        df = font(SANS, 10)
        d.text((tx, cy + 38), fit(d, deck, df, twd), font=df,
               fill=(70, 66, 60))
    y = y + 6 * (card_h + card_gap) - card_gap + 4

    # ---------- UTC timeline ----------
    d.text((MX, y), "THE DAY IN UTC", font=font(SANS_B, 11), fill=NAVY)
    tl_y = y + 17
    tl_x0 = MX + 110
    d.line([tl_x0 + 4, tl_y, W - MX - 4, tl_y], fill=LGREY, width=2)
    seg = (CW - 110) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        px = tl_x0 + seg * i + seg / 2
        d.ellipse([px - 4, tl_y - 4, px + 4, tl_y + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        tf2 = font(SANS_B, 10)
        d.text((px - d.textlength(t, font=tf2) / 2, tl_y - 12), t, font=tf2,
               fill=INK)
        lf = font(SANS, 9)
        lab = fit(d, label, lf, seg - 8)
        d.text((px - d.textlength(lab, font=lf) / 2, tl_y + 5), lab,
               font=lf, fill=(70, 66, 60))
    y = tl_y + 14 + 3

    # ---------- region bar ----------
    d.text((MX, y), "WHERE THE NEWS CAME FROM \u2014 35 STORIES BY REGION",
           font=font(SANS_B, 11), fill=NAVY)
    y += 11
    total = sum(c for _n, c, _c in REGIONS)
    bx = MX
    for name, count, col in REGIONS:
        wseg = round(CW * count / total)
        d.rectangle([bx, y, bx + wseg, y + 12], fill=col)
        lf = font(SANS_B, 10)
        lab = f"{name} {count}"
        if wseg > d.textlength(lab, font=lf) + 8:
            d.text((bx + 6, y + 2), lab, font=lf, fill=(255, 255, 255))
        else:
            d.text((bx + 2, y + 2), str(count), font=lf, fill=(255, 255, 255))
        bx += wseg
    y += 12
    # legend: every region named with its colour swatch. The three
    # narrowest bar segments are too thin for their name inside the bar
    # and used to show a bare number; the legend fixes that.
    lx = MX
    lgf = font(SANS, 9)
    for name, count, col in REGIONS:
        d.rectangle([lx, y + 2, lx + 8, y + 10], fill=col)
        lx += 11
        seg_t = f"{name} {count}   "
        d.text((lx, y), seg_t, font=lgf, fill=INK)
        lx += d.textlength(seg_t, font=lgf)
    y += 11 + 2

    # ---------- ALSO ON ----------
    d.text((MX, y), "ALSO ON \u2014 22 MORE STORIES IN ONE LINE EACH",
           font=font(SANS_B, 12), fill=NAVY)
    y += 12
    per_col = 11
    colw2 = (CW - 20) // 2
    lf = font(SANS, 10)
    for i, (n, _reg, text, src, conf) in enumerate(ALSO):
        col_i = i // per_col
        row = i % per_col
        lx = MX + col_i * (colw2 + 20)
        ly = y + row * 11
        col = CONF_COLOR[conf]
        d.ellipse([lx, ly, lx + 11, ly + 11], fill=col)
        nf = font(SANS_B, 8)
        t = str(n)
        d.text((lx + 5 - d.textlength(t, font=nf) / 2, ly + 1), t, font=nf,
               fill=(255, 255, 255))
        sfx = f" \u00b7 {src}"
        avail = colw2 - 15 - d.textlength(sfx, font=lf)
        fitted = fit(d, text, lf, avail)
        d.text((lx + 15, ly + 1), fitted, font=lf, fill=INK)
        d.text((lx + 15 + d.textlength(fitted, font=lf), ly + 1),
               sfx, font=lf, fill=GREY)
    y = y + per_col * 11 + 4

    # ---------- FOLLOW-UP (amber panel, bagarte method) ----------
    d.rectangle([MX, y, W - MX, y + 41], fill=FOLLOW_BG, outline=GOLD, width=1)
    fy = y + 4
    d.text((MX + 10, fy),
           "FOLLOW-UP \u2014 TUESDAY'S NEWS, WEDNESDAY'S DEVELOPMENT",
           font=font(SANS_B, 10), fill=NAVY)
    fy += 13
    fcolw = (CW - 20 - 20) // 2
    ff = font(SANS, 10)
    for i, (text, date) in enumerate(FOLLOW_UP):
        fx = MX + 10 + (i % 2) * (fcolw + 20)
        fyy = fy + (i // 2) * 12
        item = f"\u2022 {text} \u2014 {date}"
        d.text((fx, fyy), fit(d, item, ff, fcolw), font=ff, fill=INK)
    y += 41 + 3

    # ---------- footer: DATE CHECK (navy box) + legend + sources ----------
    d.rectangle([MX, y, W - MX, y + 39], fill=NAVY)
    fy = y + 4
    d.text((MX + 10, fy), "DATE CHECK \u2014 LEFT OUT ON PURPOSE:",
           font=font(SANS_B, 10), fill=GOLD)
    fy += 13
    items = "  \u00b7  ".join(f"{t} \u2014 {dt}" for t, dt in DATE_CHECK)
    df2 = font(SANS, 10)
    ilines = wrap_to(d, items, df2, CW - 20, 2)
    for ln in ilines:
        d.text((MX + 10, fy), ln, font=df2, fill=(235, 232, 226))
        fy += 11
    y += 39 + 4
    # legend — labels DEFINED, not just named
    lf2 = font(SANS_B, 10)
    lx = MX
    d.text((lx, y), "HOW SURE:", font=lf2, fill=INK)
    lx += d.textlength("HOW SURE: ", font=lf2)
    for conf, note in [("OFFICIAL", "on the record"),
                       ("CONFIRMED", "2+ outlets"),
                       ("REPORTED", "one wire"),
                       ("CLAIM", "one side's claim")]:
        col = CONF_COLOR[conf]
        d.ellipse([lx, y + 2, lx + 8, y + 10], fill=col)
        lx += 11
        seg_t = f"{conf} \u2014 {note}    "
        d.text((lx, y), seg_t, font=font(SANS, 10), fill=INK)
        lx += d.textlength(seg_t, font=font(SANS, 10))
    y += 10
    d.text((MX, y),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 WSJ \u00b7 CMSA/Xinhua \u00b7 UN \u00b7 OECD \u00b7 Boeing \u00b7 court judgment. All stories Wed 25 Nov 2026 unless flagged Tue 24 / Mon 23.",
           font=font(SANS, 9), fill=GREY)

    print("final y:", y)
    img.save("entry-v7.png", format="PNG", optimize=True)
    print("saved entry-v7.png", img.size)


if __name__ == "__main__":
    main()
