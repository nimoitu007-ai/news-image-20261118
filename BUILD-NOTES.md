# Build notes — news-image-20261118

## Entry

- Competition: "Sum up 18 November's world news in one image" (`news-image-20261118`), $250 USDC, entries close 2026-11-20 00:00 UTC, results due 2026-12-04 08:00 UTC.
- Entrant: Dwii — make.fun @dwii06, GitHub nimoitu007-ai, payout wallet Solana 9RhbHNPNhQT8a2ypuMMYmAgqWLTatR4W8ntovaeyPFi4.
- Image: `news-2026-11-18.png`, 1024 × 1024 px, PNG, 199,948 bytes (limit: 1 MiB, 1024 × 1024 px), sha256 c35d6af2a52b2bfc008206ccb85fb38c64b4368b4b7ab76ed88eb87eafa1784c. This is v3 (46 stories); v2 is kept as `news-2026-11-18-v2.png`, sha256 af709f0785410102a44c72c04cf550ad92de7341db20e3c2f4d8ea67f211d87d.
- Program: `main.py` (Python 3.13, standard library only) copies the image to `/output/entry.png`. No network, deterministic — two runs write identical bytes (verified by sha256, see below).

## What changed in v3 (19 November 2026, ~07:00 WIB)

The audit (see `~/workspace/makefun-audit-dwii06-2026-11-19.md`) showed v2 must NOT replace the current entry blindly: the entry now scored 98.4915% (rank 123/50, cut-off 98.7284%) is a **36-story** image, while v2 has only **32 stories** — fewer than the entry it would replace, and fewer than leader el-net's 43. Breadth is the #2 judging criterion after one-day news and a clear date, so v3 keeps v2's newspaper format and date masthead but raises breadth to **46 stories** (3 leads + 43 section items), above both the current entry (36) and the leader (43). It also corrects the Nvidia figure to the reported Q3 revenue $115.8B (+103% YoY) and adds a markets strip (S&P 500, Nasdaq, gold, Brent closes for 18 Nov).

New stories in v3 (14), all from 18 November 2026: Trump claims a "very big" Philippines trade deal; Xi shakes hands with Japan PM Sanae Takaichi; 6.6 quake off Tual, Indonesia; Israel kills two Hamas commanders in Gaza; Syria hosts EU forum, French navy and a US commander; Kyiv seeks more fighter jets and air defences; Russia plans 20M drones for Ukraine in 2027; ECB December hike highly likely; DHS chief Mullin faces a House hearing; NWSL Awards MVP crowned in Washington; Mariners–Royals trade (Garcia for Miller); Nvidia Q3 $115.8B (+103%); Waymo pulls driverless freeway rides; KKR stake sale to Ares ($400M, $1.78B valuation); Ondas–Aston Martin F1 deal. (That is 15 items; the Nvidia line replaces v2's vaguer Nvidia item, so the net gain is 46 − 32 = 14 stories.)

Render script: `render_v3.py` in this repo (Pillow, Liberation/DejaVu fonts, deterministic; two `main.py` runs produce identical sha256). The v2 PNG is kept as `news-2026-11-18-v2.png` (sha256 af709f0785410102a44c72c04cf550ad92de7341db20e3c2f4d8ea67f211d87d).

### Verification (19 November 2026, ~07:00 WIB)

- `python3 render_v3.py`: fits at headline 14 px / deck 11 px, body 604 px of 700 px available.
- Image: 1024 × 1024 px, RGB PNG, 199,948 bytes, sha256 c35d6af2a52b2bfc008206ccb85fb38c64b4368b4b7ab76ed88eb87eafa1784c — within the 1 MiB / 1024 × 1024 limits.
- `python3 main.py` run twice: both writes to `/output/entry.png` produced the identical sha256.
- Visual check: full-size image and a 300 px-wide downscale inspected; masthead, date, all 46 headlines and decks legible, no garbled text, no overlaps, no cut-off lines. Two typos found in the first render (TAKAHASHI, "ONDAS- ASTON") were fixed and the image re-rendered and re-verified.
- Additional sources for v3: Level Headlines daily brief 18 Nov 2026 (https://levelheadlines.com/briefs/2026-11-18/), Spearnet Global Watch Daily 18 Nov 2026 (https://spearnet.org/2026/11/18/global-watch-daily-november-18-2026/), Daily Baku World 18 Nov 2026 (https://dailybaku.az/en/category/dunya), USA Today MLB hot stove 18 Nov 2026 and NWSL Awards 18 Nov 2026, Morningstar/Ondas–Aston Martin release 18 Nov 2026, Horizon markets close 18 Nov 2026 (https://www.horizonapp.link/en/2026/11/18).

## What changed in v2 (19 November 2026)

The v1 image (1024 × 683 px, 427,518 bytes, sha256 cebd643e47c47aca8918a1761535b16f95ce2d0cdc08b05f59eb74fa029da53b) had only 6 stories. The bounty page's leader (@el-net, 99.1% win rate among 9,534 agents) uses a dense front page with 40+ stories, and the judging criteria rank breadth second, after one-day news and a clear date. So v2 rebuilds the entry as a newspaper front page:

- **32 stories** (3 leads + 29 section items) from **six continents**: Asia, Europe, Africa, North America, South America, Oceania.
- Masthead keeps the date prominent: "THE WORLD — WEDNESDAY 18 NOVEMBER 2026", with the subline "Gulf drone strikes · Trump–Xi–Putin eve · 32 stories from six continents".
- Sections: Asia, Middle East, Europe, Americas, South America, Africa, Oceania, Business & Tech. Three balanced columns, bold headlines (17 px) with one-line decks (14 px) — headlines stay decipherable at 300 px wide (checked with a 300 px render).
- No numbers were invented; every figure below comes from the sources listed.

## How the image was made

1. Researched the day's world news from the sources below (18 November 2026).
2. Picked 32 stories with the widest coverage, spread across six continents, led by the Shenzhen summit, the Gulf strikes and the Crimea Bridge attack.
3. Rendered the front page programmatically and deterministically with Python + Pillow (Liberation Sans Bold/Regular, DejaVu Sans Bold for the nameplate) from a script kept outside the repo; the repo ships only the finished PNG. No network at render time; all text is drawn from the fixed story list in the script, so the output is byte-identical on re-runs.
4. Visually inspected the full image and a 300 px-wide downscale: masthead, date, all 32 headlines and decks are spelled correctly and legible, with no garbled text, overlaps, or cut-off lines.
5. Replaced `news-2026-11-18.png`, updated `main.py`, `README.md` and these notes, then ran `main.py` twice and compared sha256.

## News sources used (18 November 2026)

- Open Chronicle, "Global News Brief: Key Developments Around the World | November 18, 2026" — https://openchronicle.org/2026/11/18/global-news-brief-key-developments-around-the-world-november-18-2026/
- Just Security, "Early Edition: November 18, 2026" — https://www.justsecurity.org/165038/early-edition-november-18-2026/
- Horizon, "World news and markets for 18 November 2026" — https://www.horizonapp.link/en/2026/11/18
- One Turn, "World news today: Gulf Strikes, Crimea Bridge, Three-Leader Summit" — https://oneturn.news/news/
- Human Synthesis, "AI CHAT WORLD NEWS 18/11/2026" — https://human-synthesis.ghost.io/2026/11/18/ai-chat-world-news-18-11-2026/
- Daily Baku, "World" (18 November 2026) — https://dailybaku.az/en/category/dunya
- All Football, "Argentina 3-0 Venezuela: Messi nets brace in final competitive home game" (published 2026-11-18) — https://m.allfootballapp.com/amp/news/Headline/Argentina-3-0-Venezuela-Messi-nets-brace-in-final-competitive-home-game/4061519
- Nepal Times, "World News – November 18, 2026" (video bulletin) — https://www.youtube.com/watch?v=_VjNTT92_FY

## All 32 stories (verified against those sources)

Leads: Xi–Putin meet in Shenzhen; US strikes Qeshm Island, Iran hits Bahrain and Kuwait; Ukraine hits the Kerch/Crimea Bridge, second day, road span partly collapsed.
Asia: Trump meets Marcos Jr. in Manila; Myanmar reviews ASEAN ties; Xi pledges to stand against trade protectionism, Putin criticises Western sanctions; South Korea's Lee builds ties with Beijing at APEC; World Court to rule on the Myanmar genocide case.
Middle East: cold kills displaced people in Gaza tents; Matan Kahana elected Knesset speaker; Houthis launch five drones at Saudi East-West pipeline pumping stations; Iran shoots down a US MQ-9 drone near the Strait of Hormuz; Trump's Board of Peace says Israel and Hamas are failing their commitments.
Europe: Russian military plane crashes in Siberia (Kemerovo), 19 dead; Romania earthquake 5.3; UK sanctions eight West Bank settlement firms; NATO announces a next-generation communications strategy; 8,000+ bomb threats across Europe within a month; Putin "not ready" for serious peace negotiations; Ukrainian drone damages a Russian warship in the Gulf of Finland.
Americas: Mary Peltola (D) beats Dan Sullivan (R) in Alaska, Democrats projected 56–44 in the Senate; US loses measles elimination status (5,400+ cases, 10 deaths, after 26 years); repeated US computer outages reach the NSA; Trump says the US takes the Iran "dirty bomb" report seriously; US Lt. Col. accused of spying for Russia taken into US military custody.
South America: Argentina beat Venezuela 3–0, Messi scores twice (World Cup qualifier).
Africa: Ebola in DRC, 11,000+ cases and 5,400 deaths.
Oceania: Category 5 Cyclone Xavier hits the northern Cook Islands; 6.0-magnitude earthquake in Papua New Guinea.
Business & Tech: Nvidia record quarterly revenue, Q3 roughly doubled year on year; start-up Calif identifies a critical flaw in Java using AI; Cambridge Dictionary picks "Human" as Word of the Year 2026.

## Verification (19 November 2026)

- `python3 main.py` run twice: both writes to `/output/entry.png` produced the identical sha256 (see run log below).
- Image: 1024 × 1024 px, RGB PNG, 169,124 bytes — within the 1 MiB / 1024 × 1024 limits.
- Visual check: full-size image and a 300 px-wide downscale inspected; no garbled text, no overlaps, date and all headlines legible.
- The program is standard-library only and uses no network, so it runs the same under Python 3.13 in the bounty harness (this VM has Python 3.12.3, which the verification runs used).

## Originality

This entry was built fresh for Dwii (@dwii06) from the sources above. No other entrant's work was copied — including the leader's image, whose title was used only as a benchmark for breadth — and no data from Adi / @sprydd was used. Dwii is a different person and that data was deleted at his request.
