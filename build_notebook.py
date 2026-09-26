"""
Builds notebooks/CSE_Data_Collection.ipynb.

A helper script, not part of the project itself. It writes the notebook cell
by cell so the file is easy to regenerate.

Run:  python build_notebook.py
"""

import json
from pathlib import Path

CELLS = []


def md(text):
    # nbformat accepts "source" as one string. Do not split it into a list
    # of lines without keeping the newline characters, or Jupyter joins
    # every line onto line 1.
    CELLS.append({"cell_type": "markdown", "metadata": {},
                  "source": text.strip()})


def code(text):
    CELLS.append({"cell_type": "code", "execution_count": None,
                  "metadata": {}, "outputs": [], "source": text.strip()})


#=========================================================================#
md("""
# Colombo Stock Exchange — Web Data Collection

**DA 2009 — Data Collection Methods II · Assignment 2 (Group Project)**
University of Colombo

**Group:** 25ada072 - Pasindu · 25ada073 - Sasini · 25ada141 - Salaama · 24ada076 - Nuhan

---

This notebook shows how the project collects its data, using the same code as
the app. Run it from top to bottom.

We collect three things from https://www.cse.lk :

- share prices for every listed company
- details for individual companies
- announcements, and the PDF documents attached to them
""")

code("""
# Run from the project folder so the src files can be imported.
import os, sys
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
sys.path.insert(0, os.getcwd())

import pandas as pd
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 12)

import config
print("Website:", config.BASE_URL)
""")

#=========================================================================#
md("""
---
## 1. Checking we are allowed — robots.txt

`robots.txt` is a file websites publish to tell automated programs which pages
they may visit. We read it before collecting anything.

*Written by 24ada076 - Nuhan*
""")

code("""
from src.ethics import Scraper

scraper = Scraper()
print(scraper.robots_text)
""")

md("""
Reading that:

- `User-agent: *` — the rules apply to us
- `Disallow:` on its own blocks nothing
- `Disallow: /cgi-bin/` blocks one section
- there is no `Crawl-delay`, so the site does not ask us to wait at all

We wait 1.5 seconds between requests anyway.
""")

code("""
# Check a few addresses against the rules.
for address in [config.API_BASE + "/tradeSummary",
                config.PAGES["trade_summary"]]:
    allowed, reason = scraper.can_fetch(address)
    print(f"{'allowed' if allowed else 'blocked':8} {address}")

print()
print("Sections the site asks bots to avoid:", scraper.blocked_paths())
print("Our delay:", config.DELAY, "seconds")
""")

#=========================================================================#
md("""
---
## 2. Trying requests and BeautifulSoup

This is the first thing we tried.

*Written by 24ada076 - Nuhan*
""")

code("""
import requests
from bs4 import BeautifulSoup

url = "https://www.cse.lk/"
response = requests.get(url, headers={"User-Agent": config.USER_AGENT},
                        timeout=30)

print("Status code:", response.status_code)
print("HTML size  :", f"{len(response.text):,} bytes")

soup = BeautifulSoup(response.text, "html.parser")

print("Words found:", len(soup.get_text(strip=True)), "characters")
print("Tables      :", len(soup.find_all("table")))
""")

md("""
About 25,000 bytes of HTML, and almost no words in it.

The CSE website builds its pages with JavaScript. The server sends a nearly
empty page and the browser fills in the prices afterwards. `requests`
downloads the HTML file but does not run JavaScript, so there is nothing in
it for BeautifulSoup to find.

BeautifulSoup itself is fine. Here it is on the sitemap, which is an ordinary
file:
""")

code("""
from src.static_scraper import scrape_sitemap

sitemap = scrape_sitemap(scraper)
print(f"{len(sitemap)} pages read from the sitemap without any trouble")
sitemap.head()
""")

#=========================================================================#
md("""
---
## 3. Getting the data the way the website does

We opened the CSE site in a browser, pressed F12 and looked at the **Network**
tab. The page loads its data from addresses like
`https://www.cse.lk/api/tradeSummary`, which return JSON.

*Written by 25ada072 - Pasindu*
""")

code("""
from src.api_client import CSEApi

api = CSEApi(scraper=scraper)

print("Market:", api.market_status())

index = api.aspi()
print(f"ASPI index: {index['value']:,.2f} ({index['change']:+.2f})")
""")

code("""
# One request gives us every listed company.
prices = api.trade_summary()

print("Shape:", prices.shape)
prices[["symbol", "name", "price", "change", "percentageChange",
        "turnover"]].head(10)
""")

code("""
# Some addresses need a value sent with them.
info = api.company_info("SAMP.N0000")

for field in ["name", "symbol", "lastTradedPrice", "previousClose",
              "marketCap", "p12HiPrice", "p12LowPrice"]:
    print(f"  {field:18} {info.get(field)}")
""")

#=========================================================================#
md("""
---
## 4. Cleaning the data

Data taken from a website is not ready to use straight away.

*Written by 25ada073 - Sasini*
""")

code("""
from src.cleaner import check, clean, compare, describe

before = describe(prices)
tidy, changes = clean(prices)
after = describe(tidy)

print("What we changed:")
for change in changes:
    print("  -", change)
""")

md("""
The biggest problem is the dates. CSE sends them as the number of
milliseconds since 1970, which pandas would otherwise treat as an ordinary
number.
""")

code("""
from src.api_client import to_datetime

print("As CSE sends it:", 1786440420412)
print("What it means  :", to_datetime(1786440420412))
""")

code("""
compare(before, after)
""")

code("""
# Cleaning fixes the shape of the data. These checks ask whether the
# values make sense - a share price of -5 rupees would be tidy and still
# completely wrong.
check(tidy)
""")

#=========================================================================#
md("""
---
## 5. Announcements and their documents

We do not know which documents exist, so we read the list of circulars, work
out the address of each PDF, and follow those addresses.

*Written by 25ada073 - Sasini*
""")

code("""
from src.crawler import find_documents

documents = find_documents(api)
documents[["Title", "Date"]]
""")

code("""
from src.crawler import download_documents

downloaded = download_documents(documents, limit=5, scraper=scraper)
downloaded
""")

#=========================================================================#
md("""
---
## 6. Reading the PDFs

There are two kinds of PDF. A text based one was made by a computer and the
letters are real text. A scanned one is a photograph of a printed page, and
there is no text inside it to extract.

We use **pdfplumber** for the text and layout, and **PyPDF2** for the file
details.

*Written by 24ada076 - Nuhan*
""")

code("""
from src.pdf_extractor import check_all_pdfs

check_all_pdfs()
""")

md("""
Look at the row with almost no characters. That file is about 190 KB and is
clearly full of writing when you open it — but there is no text inside it,
because it is a scan.
""")

code("""
from src.pdf_extractor import list_pdfs, pages_table, read_pdf

# A document that worked normally.
for path in list_pdfs():
    result = read_pdf(path)
    if result["ok"] and not result["scanned_pages"]:
        break

print(result["summary"])
print()
for key, value in result["info"].items():
    print(f"  {key:14} {value}")
print()
print(result["text"][:500])
""")

#=========================================================================#
md("""
---
## 7. OCR — reading the scanned document

OCR turns a picture of text into text the computer can use. There are four
steps: turn the page into an image, clean the image up, read the letters,
then tidy the result.

*Written by 25ada141 - Salaama*

This needs the Tesseract program installed, not just the Python package.
""")

code("""
from src.ocr_extractor import tesseract_ready

ready, message = tesseract_ready()
print(message)
""")

code("""
from src.ocr_extractor import ocr_pdf_page

# Find the document that gave us no text.
scanned = None
for path in list_pdfs():
    result = read_pdf(path)
    if result["ok"] and result["scanned_pages"]:
        scanned = path
        break

if scanned is None:
    print("None of the PDFs we have are scans.")
elif not ready:
    print("Install Tesseract to run this step.")
else:
    print("Reading:", scanned.name)
    ocr = ocr_pdf_page(scanned, page_number=1)

    if ocr["ok"]:
        print(f"Characters read   : {ocr['characters']:,}")
        print(f"Average confidence: {ocr['average_confidence']}%")
        print()
        print(ocr["text"][:700])
    else:
        print(ocr["error"])
""")

md("""
OCR is not perfect. It runs words together and misreads logos as letters,
which is why we also record how confident it was about each word.
""")

#=========================================================================#
md("""
---
## 8. Charts and saving the data

*Written by 25ada141 - Salaama*
""")

code("""
from src.analysis import market_figures, summary

for name, value in market_figures(tidy).items():
    print(f"  {name:12} {value}")

print()
print(summary(tidy, index))
""")

code("""
from src.analysis import chart_movers

chart_movers(tidy, dark=False)
""")

code("""
from src.storage import export

files = export(tidy, "notebook_prices", formats=["csv", "json"])
for path in files:
    print("saved:", path.name)

print()
print("Reading the CSV back, skipping the comment lines at the top:")
pd.read_csv(files[0], comment="#").head(3)
""")

#=========================================================================#
md("""
---
## 9. What it cost the website

Every request is written to `logs/request_log.csv`.
""")

code("""
log = pd.read_csv(config.REQUEST_LOG)

print("Requests recorded:", len(log))
log.tail(8)[["time", "method", "url", "status", "delay_seconds"]]
""")

#=========================================================================#
md("""
---
## Summary

| Step | Tool |
|---|---|
| Checking we are allowed | `robots.txt`, `RobotFileParser` |
| Getting the HTML | `requests`, BeautifulSoup |
| Getting the data | the addresses the site itself uses, read with `requests` and pandas |
| Running JavaScript when needed | Selenium |
| Finding and downloading documents | our crawler, and a Scrapy spider |
| Reading PDFs | PyPDF2, pdfplumber |
| Reading scanned pages | PIL, OpenCV, pytesseract |
| Cleaning and checking | pandas |
| Saving | CSV, Excel, JSON |

**Who wrote what**

| Member | Part |
|---|---|
| 24ada076 - Nuhan | robots.txt and requests, BeautifulSoup, reading PDFs |
| 25ada072 - Pasindu | getting the data from the site, Selenium |
| 25ada073 - Sasini | crawling for documents, the Scrapy spider, cleaning |
| 25ada141 - Salaama | OCR, saving the files, charts |

---

*Data source: Colombo Stock Exchange (https://www.cse.lk). Collected for
academic purposes only. Not investment advice.*
""")


#=========================================================================#
notebook = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.13"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path("notebooks/CSE_Data_Collection.ipynb")
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(notebook, indent=1), encoding="utf-8")

# Remove the old notebook name if it is still there.
old = Path("notebooks/CSE_Learning_Journey.ipynb")
if old.exists():
    old.unlink()

print(f"Wrote {out}")
print(f"  {len(CELLS)} cells "
      f"({sum(1 for c in CELLS if c['cell_type'] == 'code')} code, "
      f"{sum(1 for c in CELLS if c['cell_type'] == 'markdown')} markdown)")
