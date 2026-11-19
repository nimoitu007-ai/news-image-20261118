"""Render v3 of the news-image-20261118 front page: 46 stories, 1024x1024.

Deterministic, offline. Run: python3 render_v3.py
Writes news-2026-11-18.png in this directory (v2 is kept as
news-2026-11-18-v2.png). All stories are from Wednesday 18 Nov 2026;
see BUILD-NOTES.md for the source list.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 26
GUTTER = 14
COLS = 3
COL_W = (W - 2 * MARGIN - (COLS - 1) * GUTTER) // COLS  # 313

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLDSANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

PAPER = (251, 250, 245)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
ACCENT = (150, 20, 20)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_deck(draw, text, fnt, width):
    """Single-line deck, truncated with ellipsis to fit."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "..."


# (headline, deck) — headlines short caps, decks one line.
LEADS = [
    ("XI AND PUTIN MEET IN SHENZHEN",
     "One day before a first trilateral summit with Trump."),
    ("US STRIKES QESHM; IRAN HITS GULF",
     "Iran fires at Bahrain and Kuwait after the US hits Qeshm."),
    ("UKRAINE HITS CRIMEA BRIDGE",
     "Second day running; part of the Kerch road span collapses."),
]

# (section, [(headline, deck), ...])
SECTIONS = [
    ("ASIA", [
        ("TRUMP MEETS MARCOS JR. IN MANILA",
         "State lunch ahead of the flight to China."),
        ("TRUMP CLAIMS PHILIPPINES DEAL",
         "\"Very big\" trade deal, Manila calls it an understanding."),
        ("MYANMAR REVIEWS ASEAN TIES",
         "Junta chief cites unfair treatment by the bloc."),
        ("XI VOWS TO FIGHT PROTECTIONISM",
         "Putin criticises Western sanctions in Shenzhen."),
        ("SEOUL BUILDS TIES WITH BEIJING",
         "Lee uses the APEC gathering to court China."),
        ("WORLD COURT TO RULE ON MYANMAR",
         "Genocide case judgment due from The Hague."),
        ("XI, TAKAICHI SHAKE HANDS",
         "First meeting since Japan ties deteriorated."),
        ("6.6 QUAKE OFF TUAL, INDONESIA",
         "Strong tremor recorded near the Maluku islands."),
    ]),
    ("MIDDLE EAST", [
        ("COLD KILLS IN GAZA TENTS",
         "Displaced families face freezing nights."),
        ("KAHANA ELECTED KNESSET SPEAKER",
         "Win for PM-elect Eisenkot's Yashar party."),
        ("HOUTHIS TARGET SAUDI PIPELINE",
         "Five drones fired at East-West pumping stations."),
        ("IRAN DOWNS US MQ-9 DRONE",
         "Shot down near the Strait of Hormuz."),
        ("BOARD OF PEACE: BOTH SIDES FAILING",
         "Israel and Hamas miss commitments, report says."),
        ("ISRAEL KILLS TWO HAMAS COMMANDERS",
         "Gaza strikes target senior commanders."),
        ("SYRIA HOSTS EU, FRENCH, US ENVOYS",
         "Diplomatic and military engagement steps up."),
    ]),
    ("EUROPE", [
        ("RUSSIAN PLANE CRASHES, 19 DEAD",
         "Military aircraft down in Siberia's Kemerovo region."),
        ("ROMANIA QUAKE 5.3",
         "Tremor felt across the region; no major damage yet."),
        ("UK SANCTIONS WEST BANK FIRMS",
         "Eight settlement companies hit by London."),
        ("NATO UNVEILS COMMS STRATEGY",
         "Next-generation alliance networks announced."),
        ("8,000 BOMB THREATS SWEEP EUROPE",
         "Wave of threats in a single month."),
        ("PUTIN \"NOT READY\" FOR PEACE TALKS",
         "Sources tell the NYT he will not negotiate seriously."),
        ("UKRAINE HITS WARSHIP OFF FINLAND",
         "Drone damages Russian vessel in the Gulf of Finland."),
        ("KYIV SEEKS MORE JETS, DEFENCES",
         "Ukraine asks allies for fighters and air defence."),
        ("RUSSIA PLANS 20M DRONES FOR 2027",
         "Moscow scales up drone production for Ukraine war."),
        ("ECB: DECEMBER HIKE HIGHLY LIKELY",
         "Vice-president Vujcic signals a rate rise."),
    ]),
    ("AMERICAS", [
        ("DEMOCRATS WIN ALASKA, SENATE 56-44",
         "Peltola beats Sullivan in the last Senate race."),
        ("US LOSES MEASLES-FREE STATUS",
         "5,400+ cases, 10 deaths after 26 years."),
        ("US OUTAGES REACH THE NSA",
         "Repeated computer failures hit federal systems."),
        ("TRUMP ON IRAN \"DIRTY BOMB\" REPORT",
         "President says the US takes the report seriously."),
        ("US OFFICER HELD IN SPY CASE",
         "Lt. Col. accused of spying for Russia in custody."),
        ("DHS CHIEF MULLIN FACES HOUSE",
         "Homeland Security secretary called to a hearing."),
        ("NWSL AWARDS: MVP CROWNED",
         "Winner announced in Washington, D.C.; Hamm presents."),
        ("MARINERS-ROYALS TRADE",
         "Garcia to Seattle; Miller, Evans, Ferrer to Kansas City."),
        ("ARGENTINA 3-0 VENEZUELA",
         "Messi scores twice in a World Cup qualifier."),
    ]),
    ("AFRICA", [
        ("EBOLA SURGES IN CONGO",
         "11,000+ cases and 5,400 deaths reported."),
    ]),
    ("OCEANIA", [
        ("CYCLONE XAVIER HITS COOK ISLANDS",
         "Category 5 storm strikes the northern islands."),
        ("PNG QUAKE 6.0",
         "Strong earthquake shakes Papua New Guinea."),
    ]),
    ("BUSINESS & TECH", [
        ("NVIDIA Q3: $115.8B, UP 103%",
         "Record revenue in the first report since Huang's exit."),
        ("WAYMO PULLS DRIVERLESS FREEWAYS",
         "Driverless rides withdrawn from US freeways."),
        ("AI FINDS CRITICAL JAVA FLAW",
         "Start-up Calif spots the bug using AI."),
        ("WORD OF THE YEAR: \"HUMAN\"",
         "Cambridge Dictionary picks its 2026 word."),
        ("KKR STAKE SALE TO ARES: $400M",
         "22.5% stake values the IPL club at $1.78B."),
        ("ONDAS-ASTON MARTIN F1 DEAL",
         "Branding debuts on the car at the Las Vegas GP."),
    ]),
]

MARKETS = "MARKETS 18 NOV:  S&P 500 7,340.53 -1.03%  |  Nasdaq 24,328.38 -0.74%  |  Gold $3,775 -2.31%  |  Brent $91.55 -1.71%"
FOOTER = "46 stories from six continents - all from Wednesday 18 November 2026 - Sources: Open Chronicle, Just Security, Horizon, Level Headlines, Daily Baku, Spearnet, USA Today, Morningstar"


def measure_body(draw, hl_size, dk_size):
    """Total body height for given font sizes; returns (height, layout)."""
    f_hl = font(BOLDSANS, hl_size)
    f_dk = font(REG, dk_size)
    f_sec = font(BOLDSANS, 12)
    lh_hl = hl_size + 3
    lh_dk = dk_size + 3
    items = []  # (kind, section, lines, y_offset within column flow)
    total = 0
    for sec, stories in SECTIONS:
        total += 12 + 8 + 4  # section header + rules + gap
        for hl, dk in stories:
            lines = wrap(draw, hl, f_hl, COL_W)
            n = min(len(lines), 2)
            total += n * lh_hl + lh_dk + 7
    return total


def render(hl_size=14, dk_size=11):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_name = font(BOLD, 62)
    f_date = font(BOLDSANS, 21)
    f_sub = font(REG, 15)
    f_lead_hl = font(BOLDSANS, 16)
    f_lead_dk = font(REG, 12)
    f_hl = font(BOLDSANS, hl_size)
    f_dk = font(REG, dk_size)
    f_sec = font(BOLDSANS, 12)
    f_mkt = font(BOLDSANS, 12)
    f_ft = font(REG, 10)

    y = 22
    # Masthead
    d.text((W // 2, y), "THE WORLD", font=f_name, fill=INK, anchor="ma")
    y += 72
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    y += 8
    d.text((W // 2, y), "WEDNESDAY  18  NOVEMBER  2026", font=f_date,
           fill=ACCENT, anchor="ma")
    y += 30
    d.text((W // 2, y), "Gulf drone strikes  ·  Trump–Xi–Putin eve  ·  46 stories from six continents",
           font=f_sub, fill=GREY, anchor="ma")
    y += 26
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)

    # Leads: three boxes across
    y += 10
    lead_top = y
    lead_h = 0
    boxes = []
    for hl, dk in LEADS:
        lines = wrap(d, hl, f_lead_hl, COL_W)
        dk_lines = wrap(d, dk, f_lead_dk, COL_W)
        h = len(lines) * 20 + len(dk_lines) * 16 + 6
        boxes.append((lines, dk_lines, h))
        lead_h = max(lead_h, h)
    for i, (lines, dk_lines, h) in enumerate(boxes):
        x = MARGIN + i * (COL_W + GUTTER)
        yy = lead_top
        for ln in lines:
            d.text((x, yy), ln, font=f_lead_hl, fill=INK)
            yy += 20
        for ln in dk_lines:
            d.text((x, yy), ln, font=f_lead_dk, fill=GREY)
            yy += 16
        if i < 2:
            d.line([(x + COL_W + GUTTER // 2, lead_top),
                    (x + COL_W + GUTTER // 2, lead_top + lead_h)],
                   fill=(200, 200, 190), width=1)
    y = lead_top + lead_h + 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    body_top = y + 10

    # Body: flow sections across 3 columns, balanced by measured height.
    lh_hl = hl_size + 3
    lh_dk = dk_size + 3
    # Build flat list of blocks: ("sec", name) or ("item", hl_lines, deck)
    blocks = []
    for sec, stories in SECTIONS:
        blocks.append(("sec", sec))
        for hl, dk in stories:
            lines = wrap(d, hl, f_hl, COL_W)[:2]
            deck = fit_deck(d, dk, f_dk, COL_W)
            blocks.append(("item", lines, deck))
    heights = []
    for b in blocks:
        if b[0] == "sec":
            heights.append(12 + 8 + 4)
        else:
            heights.append(len(b[1]) * lh_hl + lh_dk + 7)
    # Greedy column balance: assign consecutive blocks to the
    # currently shortest column, but never split a section header
    # from its first item (keep header+next item together).
    cols = [[], [], []]
    col_h = [0, 0, 0]
    i = 0
    while i < len(blocks):
        take = 1
        if blocks[i][0] == "sec" and i + 1 < len(blocks):
            take = 2  # header + first item together
        h = sum(heights[i:i + take])
        c = col_h.index(min(col_h))
        cols[c].extend(blocks[i:i + take])
        col_h[c] += h
        i += take
    body_h = max(col_h)
    footer_top = H - MARGIN - 44
    avail = footer_top - body_top - 6
    if body_h > avail:
        return None, body_h, avail

    for ci, col in enumerate(cols):
        x = MARGIN + ci * (COL_W + GUTTER)
        yy = body_top
        for b in col:
            if b[0] == "sec":
                d.text((x, yy), b[1], font=f_sec, fill=ACCENT)
                yy += 12
                d.line([(x, yy + 2), (x + COL_W, yy + 2)], fill=RULE, width=1)
                yy += 8 + 4
            else:
                for ln in b[1]:
                    d.text((x, yy), ln, font=f_hl, fill=INK)
                    yy += lh_hl
                d.text((x, yy), b[2], font=f_dk, fill=GREY)
                yy += lh_dk + 7
    # Footer
    d.line([(MARGIN, footer_top), (W - MARGIN, footer_top)], fill=RULE, width=2)
    d.text((W // 2, footer_top + 8), MARKETS, font=f_mkt, fill=INK, anchor="ma")
    d.text((W // 2, footer_top + 28), FOOTER, font=f_ft, fill=GREY, anchor="ma")
    return img, body_h, avail


if __name__ == "__main__":
    for hl, dk in [(14, 11), (13, 11), (13, 10)]:
        img, bh, av = render(hl, dk)
        if img is not None:
            print(f"fits at headline {hl} / deck {dk}: body {bh}px, avail {av}px")
            break
        print(f"overflow at headline {hl} / deck {dk}: body {bh}px > avail {av}px")
    else:
        raise SystemExit("v3 does not fit at any tried size")
    out = "news-2026-11-18.png"
    img.save(out, optimize=True)
    import hashlib
    from pathlib import Path
    data = Path(out).read_bytes()
    print(f"wrote {out}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}")
    n = sum(len(s) for _, s in SECTIONS) + len(LEADS)
    print(f"stories: {n} (leads {len(LEADS)} + sections {sum(len(s) for _, s in SECTIONS)})")
