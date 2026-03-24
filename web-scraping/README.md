# Web Scraping Assignment — Marvel's Spider-Man Fandom Wiki
## Soham Solanki (ssolan24)

## Wiki Choice & Personal Motivation

I chose the **Marvel's Spider-Man Fandom Wiki** (`marvels-spider-man.fandom.com`) because Spider-Man has been my favorite Marvel hero since I was a kid. There's something about Peter Parker that always resonated with me. He's not a billionaire or a god; he's just a regular guy from Queens doing the right thing just because. The *Marvel's Spider-Man* game series by Insomniac Games captures that essence beautifully and expands on it with an original story and rich cast of characters that feel both faithful to the comics and genuinely new. That was one of the first video games I owned on my PlayStation 4, and with the trailer for the new Spider-Man movie coming out just a few days ago, this felt fitting.

Scraping the wiki for this game universe felt like a natural fit: it's a self-contained continuity (Earth-1048) with well-documented characters, consistent infobox formatting, and a level of detail that makes structured data extraction both meaningful and achievable.

---

## What I Scraped

### Target: Character pages in Marvel's Spider-Man (2018) and its sequels

For each character the scraper collects:

| Field | Description |
|---|---|
| `name` | Character's real name |
| `url` | Source wiki page |
| `alias` | Superhero / villain alias |
| `status` | Alive, Deceased, or Incarcerated |
| `gender` | Character gender |
| `affiliation` | Organisations the character belongs to |
| `first_appearance` | Which game in the series they debut in |
| `voice_actor` | Voice / motion-capture performer |
| `bio_excerpt` | First substantive paragraph of the wiki article |

### Research Value

1. **Character network analysis** — The `affiliation` field maps characters to organisations (Sinister Six, F.E.A.S.T., NYPD, Oscorp, etc.), enabling graph-based studies of how narrative organizations are structured in AAA video game storytelling.

2. **Adaptation studies** — Comparing this dataset against similar datasets from the comics wiki or the MCU wiki reveals how character attributes (status, alliances, morality) are reinterpreted across media. This is relevant to transmedia studies and fan-studies research.

3. **Voice performance research** — The `voice_actor` field links characters to performers, useful for researchers studying labour in the video game industry or the growing field of voice-acting studies.

4. **Narrative mortality / stakes analysis** — The `status` field (Alive / Deceased / Incarcerated) across a full cast lets researchers quantify how a story uses consequence and permanence, a metric increasingly used in game narrative analysis.

5. **NLP training data** — The `bio_excerpt` field provides short, clean character descriptions that could serve as seed data for named-entity recognition, relation extraction, or character-centric summarisation models grounded in the video game domain.

6. **Gender & representation research** — Structured demographic fields allow quick quantitative snapshots of gender representation in a blockbuster game's cast, suitable for diversity-in-games studies.

---

## robots.txt Compliance

The `robots.txt` file for the Fandom network (which governs all subdomains including `marvels-spider-man.fandom.com`) was reviewed before scraping.

**robots.txt URL:** https://marvels-spider-man.fandom.com/robots.txt

Key rules relevant to this project:

- **`User-agent: *`** — General crawlers are **allowed** on `/wiki/` article pages (no blanket `Disallow: /` for the wildcard agent).
- **Blocked bots:** Commercial crawlers such as `GPTBot`, `SemrushBot`, `serpstatbot`, and `ImagesiftBot` are individually disallowed with `Disallow: /`.
- **Disallowed namespaces for general crawlers:** `Special:`, `User:`, `User_talk:`, `Template:`, `Template_talk:`, `Help:` — none of which this scraper accesses.
- **Allowed for general crawlers:** `/wiki/` article pages and `/api.php?` endpoints.

This scraper:
- Uses only `/wiki/<CharacterName>` URLs (explicitly permitted).
- Identifies itself with a descriptive `User-Agent` string.
- Respects a **2-second crawl delay** between requests.
- Does **not** access any disallowed namespace or bot-blocked path.

---

## Technical Stack

| Tool | Purpose |
|---|---|
| `cloudscraper` | Fetches pages while handling Cloudflare anti-bot challenges |
| `BeautifulSoup4` | Parses HTML; extracts infobox fields and article text |
| `csv` / `json` | Writes output in two interoperable formats |

---

## Output Files

Both files are located in `../web_scraping/`:

| File | Format | Description |
|---|---|---|
| `spider_man_characters.csv` | CSV | Tabular data, suitable for spreadsheet tools or pandas |
| `spider_man_characters.json` | JSON | Nested records, suitable for APIs or document databases |

---

## How to Run

```bash
# Install dependencies
pip install cloudscraper beautifulsoup4

# Run the scraper
python web-scraping/fandom_wiki_scraping.py
```

Output files will be written to `web_scraping/`.

---

## Ethical Notes

- Data is scraped from publicly accessible wiki article pages only.
- Content on Fandom wikis is community-contributed and licensed under [CC-BY-SA](https://www.fandom.com/licensing).
- The scraper does not log in, does not scrape user pages, and does not attempt to bypass any authentication.
- A polite crawl delay prevents unnecessary server load.
