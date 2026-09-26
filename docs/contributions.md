# Team Contributions

**Project:** Colombo Stock Exchange — Web Data Collection
**Course:** DA 2009 — Data Collection Methods II · Assignment 2 (Group)
**Group:** 25ada072 - Pasindu · 25ada073 - Sasini · 25ada141 - Salaama · 24ada076 - Nuhan

Each file has a banner at the top naming who wrote it, so the split is visible
in the code as well as in this table. Each tab in the app is labelled the same
way.

```
#=========================================================================#
#  FILE   : src/ethics.py                                                  #
#  PURPOSE: Sends all our web requests, politely and legally.              #
#  OWNER  : 24ada076                                                       #
#=========================================================================#
```

---

## Who wrote what

### 24ada076 - Nuhan — ethical scraping, BeautifulSoup, and PDFs

| File | What it does |
|---|---|
| `src/ethics.py` | robots.txt, the delay between requests, `requests` and status codes, the request log |
| `src/static_scraper.py` | `requests` + BeautifulSoup, static vs dynamic content, the sitemap |
| `src/pdf_extractor.py` | Reading PDFs with PyPDF2 and pdfplumber |

**Should be able to explain:** what robots.txt is and how we check every
address against it; why we wait between requests when the site does not ask
us to; HTTP status codes; why `requests` finds almost no text on the CSE page;
the BeautifulSoup methods (`find`, `find_all`, `select`, `select_one`,
`get_text`, `get`); the difference between PyPDF2 and pdfplumber; and why a
scanned PDF returns no text at all.

---

### 25ada072 - Pasindu — getting the data, and Selenium

| File | What it does |
|---|---|
| `src/api_client.py` | Reads the JSON addresses the site uses, and makes DataFrames |
| `src/selenium_scraper.py` | Opens the site in a real browser so the JavaScript runs |
| `config.py` | All the settings in one place |
| `warm_cache.py` | Saves a copy of the data for offline use |

**Should be able to explain:** what an API is and why a site has one; how we
found the addresses using the Network tab; why those addresses need POST and
not GET; how the JSON replies become DataFrames; how Selenium runs the
JavaScript first; and why we wait for the table to appear before reading it.

---

### 25ada073 - Sasini — crawling, and cleaning the data

| File | What it does |
|---|---|
| `src/crawler.py` | Finds the PDF documents and downloads them |
| `src/cleaner.py` | Cleans the data and checks it makes sense |
| `scrapy_project/` | The Scrapy spider |

**Should be able to explain:** the difference between scraping and crawling;
how the full PDF address is built from the part the website gives us; how the
Scrapy spider follows links and which settings keep it polite; what had to be
cleaned in the CSE data; and the difference between cleaning the shape of the
data and checking the values make sense.

---

### 25ada141 - Salaama — OCR, saving the files, and the charts

| File | What it does |
|---|---|
| `src/ocr_extractor.py` | The OCR pipeline: PIL, OpenCV, pytesseract |
| `src/storage.py` | Saves CSV, Excel and JSON with the source credited |
| `src/analysis.py` | The charts and the summary figures |

**Should be able to explain:** the four OCR steps; why the image is converted
to grey and then to black and white before reading it; what the dpi setting
changes; how we know whether Tesseract is actually installed; how the source
is recorded inside each exported file; and what the charts show.

---

## The app

`app.py` was put together by all four of us. Each tab is labelled with the
member whose part of the project it shows:

| Tab | Labelled |
|---|---|
| Ethics | 24ada076 - Nuhan |
| Market Data | 25ada072 - Pasindu |
| Companies | 25ada072 - Pasindu |
| Announcements | 25ada073 - Sasini · 24ada076 - Nuhan |
| OCR | 25ada141 - Salaama |
| Data & Export | 25ada073 - Sasini · 25ada141 - Salaama |

---

## Shared

All four members worked on choosing the website, deciding the ethical rules,
testing, the presentation, and this documentation.

---

## Running each part on its own

```bash
python -m src.ethics             # 24ada076 - Nuhan
python -m src.static_scraper     # 24ada076 - Nuhan
python -m src.pdf_extractor      # 24ada076 - Nuhan
python -m src.api_client         # 25ada072 - Pasindu
python -m src.selenium_scraper   # 25ada072 - Pasindu
python -m src.crawler            # 25ada073 - Sasini
python -m src.cleaner            # 25ada073 - Sasini
python -m src.ocr_extractor      # 25ada141 - Salaama
python -m src.storage            # 25ada141 - Salaama
python -m src.analysis           # 25ada141 - Salaama
```

And the Scrapy spider:

```bash
cd scrapy_project
scrapy crawl cse_announcements -O ../data/scrapy_output.json
```
