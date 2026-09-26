# How It Works — Colombo Stock Exchange Web Data Collection

> **New here?** Start with the step-by-step guide in [README.md](README.md).
> This page is the technical explanation of the project.

**DA 2009 — Data Collection Methods II · Assignment 2 (Group Project)**
University of Colombo · Faculty of Science / Department of Statistics

**Group:** 25ada072 - Pasindu · 25ada073 - Sasini · 25ada141 - Salaama · 24ada076 - Nuhan
**Website:** https://www.cse.lk
**Data collected:** share prices, company details, announcements

---

## What the project does

We collect three kinds of data from the Colombo Stock Exchange:

- **Share prices** — today's trading for every listed company (around 290)
- **Company details** — price, market value, yearly high and low
- **Announcements** — company notices, and the PDF documents attached to them

Everything is then cleaned, checked, charted, and saved as CSV, Excel and JSON.

---

## How we get the data

The CSE website builds its pages with JavaScript. When `requests` downloads
the page it gets about 25,000 bytes of HTML containing only a couple of dozen
characters of actual words and no tables, because the prices are added by
JavaScript after the page loads and `requests` does not run JavaScript.

So we opened the site in a browser, pressed F12 and looked at the **Network**
tab. The page loads its data from addresses like:

```
https://www.cse.lk/api/tradeSummary
```

Those addresses return JSON, which pandas reads directly, and one request
gives us every company at once. They need no login and are not blocked by
`robots.txt`.

`src/static_scraper.py` and `src/selenium_scraper.py` show the `requests` and
Selenium approaches on the same page, and can be run on their own.

---

## Ethical scraping

The details are in [`docs/ethics_statement.md`](docs/ethics_statement.md).
In short:

- We read `robots.txt` and check every address against it before requesting it
- We wait **1.5 seconds** between requests, even though the site does not ask
  us to
- Our User-Agent gives the university, the course and an email address
- We save a copy of every reply so we never ask for the same thing twice
- We only collect data that is public — no logins, no CAPTCHAs, no personal
  information about anybody
- Every file we export names CSE as the source and records the collection time

Every request is written to `logs/request_log.csv`.

---

## Reading the PDFs

Announcements come with PDF documents. There are two kinds:

- **Text based** — made by a computer. `pdfplumber` reads the text straight
  out, and `PyPDF2` gives us the file details.
- **Scanned** — a photograph of a printed page. There is no text inside to
  extract, so these need **OCR**.

The OCR follows the four steps from the lecture:

1. **Image acquisition** — turn the PDF page into an image
2. **Preprocessing** — OpenCV converts it to grey, then to black and white
   (the lecture's optional noise step follows, which at its 1x1 setting
   leaves the image unchanged)
3. **Text recognition** — pytesseract reads the letters
4. **Post-processing** — pandas tidies the text and saves it

---

## Setting it up

### The quick way — the numbered .bat files

| File | What it does | The command it runs |
|---|---|---|
| `1_SETUP_First_Time_Only.bat` | Finds or installs Python, builds `.venv`, installs the packages, offers to install Tesseract | `python -m venv .venv` then `pip install -r requirements.txt` |
| `2_START_The_App.bat` | Starts the app and opens the browser | `python app.py --open` |
| `3_Collect_Fresh_Data.bat` | Collects everything once and saves a copy | `python warm_cache.py` |
| `4_Run_Each_Members_Part.bat` | A menu that runs each `src/` file on its own | `python -m src.<name>` |
| `5_Open_The_Notebook.bat` | Opens the notebook walkthrough (installs Jupyter the first time) | `python -m notebook notebooks\CSE_Data_Collection.ipynb` |
| `6_Run_The_Scrapy_Spider.bat` | Runs the Scrapy spider | `scrapy crawl cse_announcements -O ../data/scrapy_output.json` |
| `Run_CSE_App.bat` | Same as file 2 (kept because the guides mention it) | |

Keep the black window open while you use the app — closing it stops the app.

The steps below do the same thing by hand.

### 1. Install Python packages

Open a Command Prompt in the project folder, then:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> A virtual environment is used because the system Python on this machine had
> pandas and numpy from two different installations, which made even
> `pd.DataFrame([{"a": 1}])` fail.

### 2. Install Tesseract (needed for the OCR tab)

`pip install pytesseract` only installs the Python part. The Tesseract program
itself is a separate download:

1. Get it from https://github.com/UB-Mannheim/tesseract/wiki
   (or run `winget install UB-Mannheim.TesseractOCR`)
2. Install to `C:\Program Files\Tesseract-OCR\`

`src/ocr_extractor.py` looks in that folder by itself if Tesseract is not on
the PATH. Everything except the OCR tab works without it.

### 3. Run it

```bash
python app.py
```

Then open **http://127.0.0.1:7860**.

### 4. Optional — collect a copy first

```bash
python warm_cache.py
```

Saves a copy of every reply so the app still works without internet.

The repository does not include any collected data — the `data/` folder is
created empty the first time the code runs, and fills up as you collect.

---

## The tabs

| Tab | What it does |
|---|---|
| Home | What the project collects, and who did what |
| Ethics | robots.txt, our settings, and the request log |
| Market Data | Share prices for every company, plus the index and sectors |
| Companies | Details for one company, or several at once |
| Announcements | Company announcements, downloading PDFs, reading their text |
| OCR | Reading a scanned document that has no text in it |
| Data & Export | Cleaning, checking, charts, and saving to CSV/Excel/JSON |

Dark by default, with a light option for projectors.

---

## Files

```
CSE-Scraping-Project/
├── app.py                    the screen                    [all four]
├── config.py                 settings                      [25ada072 - Pasindu]
├── warm_cache.py             saves a copy of the data      [25ada072 - Pasindu]
│
├── src/
│   ├── ethics.py             robots.txt, delay, log        [24ada076 - Nuhan]
│   ├── static_scraper.py     requests + BeautifulSoup      [24ada076 - Nuhan]
│   ├── pdf_extractor.py      PyPDF2 and pdfplumber         [24ada076 - Nuhan]
│   ├── api_client.py         gets the data                 [25ada072 - Pasindu]
│   ├── selenium_scraper.py   browser automation            [25ada072 - Pasindu]
│   ├── crawler.py            finds and downloads PDFs      [25ada073 - Sasini]
│   ├── cleaner.py            cleaning and checks           [25ada073 - Sasini]
│   ├── ocr_extractor.py      PIL, OpenCV, pytesseract      [25ada141 - Salaama]
│   ├── storage.py            saves CSV / Excel / JSON      [25ada141 - Salaama]
│   └── analysis.py           charts and figures            [25ada141 - Salaama]
│
├── scrapy_project/           the Scrapy spider             [25ada073 - Sasini]
├── notebooks/                a walkthrough of the code
├── docs/                     ethics, contributions, viva notes, slides
├── data/                     saved data, PDFs, images, exports
└── logs/request_log.csv      every request we sent
```

---

## Running each part on its own

Each file can be run by itself, so each member can show their own work:

```bash
python -m src.ethics             # robots.txt and a test request  [24ada076 - Nuhan]
python -m src.static_scraper     # requests + BeautifulSoup       [24ada076 - Nuhan]
python -m src.pdf_extractor      # reading PDFs                   [24ada076 - Nuhan]
python -m src.api_client         # getting the data               [25ada072 - Pasindu]
python -m src.selenium_scraper   # browser automation             [25ada072 - Pasindu]
python -m src.crawler            # downloading PDFs               [25ada073 - Sasini]
python -m src.cleaner            # cleaning and checks            [25ada073 - Sasini]
python -m src.ocr_extractor      # OCR on a scanned page          [25ada141 - Salaama]
python -m src.storage            # saving files                   [25ada141 - Salaama]
python -m src.analysis           # figures and charts             [25ada141 - Salaama]
```

The Scrapy spider:

```bash
cd scrapy_project
scrapy crawl cse_announcements -O ../data/scrapy_output.json
```

---

## Study guides and slides

PDFs in `docs/`, for learning the project and preparing for the viva:

| File | Who it is for |
|---|---|
| `docs/CSE_Team_Guide.pdf` | **Everyone.** Explains each member's part in plain words, lists the files each person should read, and has 50 questions with answers for each member. |
| `docs/CSE_24ada076_Deep_Guide.pdf` | The architecture, the full pipeline, and a walkthrough of the code. |
| `docs/member_documents/Document_<index>_<name>.pdf` | **One for each member.** Everything behind that member's part - the ideas, the reasons and the code - explained step by step from the beginning, with a chapter on reading Python, a viva chapter and the 50 practice questions. |

Rebuild them all with `python build_guides.py`, or one member's document with
`python build_guides.py sasini` (a name or an index number).

`docs/slides.pptx` is the short presentation. Each slide has a speaker script
in its notes - about 3 minutes in total.

---

## Source

Data source: **Colombo Stock Exchange** (https://www.cse.lk). Collected for
academic purposes only under DA 2009, University of Colombo. This is one
trading day. It is not investment advice.
