#=========================================================================#
#  DA 2009 - Data Collection Methods II | Assignment 2 (Group Project)     #
#  Colombo Stock Exchange (CSE) - Web Data Collection                      #
#                                                                          #
#  FILE   : config.py                                                      #
#  PURPOSE: All the settings the project uses, kept in one place so we     #
#           only have to change them once.                                 #
#  OWNER  : 25ada072                                                       #
#=========================================================================#

from pathlib import Path

#-------------------------------------------------------------------------#
#  PROJECT DETAILS                                                         #
#-------------------------------------------------------------------------#

PROJECT_NAME = "CSE Data Collection"
COURSE       = "DA 2009 - Data Collection Methods II"
UNIVERSITY   = "University of Colombo"

TEAM = ["25ada072", "25ada073", "25ada141", "24ada076"]

# Names, shown beside the index numbers on screen and in the documents.
# The OWNER line at the top of each code file keeps the index number only,
# because that is how the university identifies each of us.
NAMES = {
    "24ada076": "Nuhan",
    "25ada072": "Pasindu",
    "25ada073": "Sasini",
    "25ada141": "Salaama",
}


def member_label(index):
    """Turn "24ada076" into "24ada076 - Nuhan"."""
    name = NAMES.get(index)
    return f"{index} - {name}" if name else index

# Who wrote which file. Also used in docs/contributions.md.
OWNERSHIP = {
    "24ada076": {
        "role": "Ethical scraping and robots.txt, BeautifulSoup, "
                "and reading PDFs",
        "modules": ["src/ethics.py", "src/static_scraper.py",
                    "src/pdf_extractor.py"],
    },
    "25ada072": {
        "role": "Getting the data from the site, and Selenium",
        "modules": ["src/api_client.py", "src/selenium_scraper.py",
                    "config.py", "warm_cache.py"],
    },
    "25ada073": {
        "role": "Crawling for documents, and cleaning the data",
        "modules": ["src/crawler.py", "src/cleaner.py", "scrapy_project/"],
    },
    "25ada141": {
        "role": "OCR, saving the files, and the charts",
        "modules": ["src/ocr_extractor.py", "src/storage.py",
                    "src/analysis.py"],
    },
}

#-------------------------------------------------------------------------#
#  THE WEBSITE                                                             #
#-------------------------------------------------------------------------#

BASE_URL   = "https://www.cse.lk"
ROBOTS_URL = f"{BASE_URL}/robots.txt"

# The CSE website loads its data from these addresses. We found them by
# opening the site, pressing F12 and looking at the Network tab.
API_BASE = f"{BASE_URL}/api"

# The announcement PDFs are stored on a different server to the website.
CDN_BASE = "https://cdn.cse.lk/cmt/"

# Ordinary pages, used by the Selenium script.
PAGES = {
    "home":          f"{BASE_URL}/",
    "trade_summary": f"{BASE_URL}/equity/trade-summary",
    "announcements": f"{BASE_URL}/announcements",
}

#-------------------------------------------------------------------------#
#  THE API ADDRESSES WE USE                                                #
#                                                                          #
#  Most of these need a POST request. A GET returns an error.              #
#-------------------------------------------------------------------------#

ENDPOINTS = {
    "marketStatus":         {"method": "POST", "desc": "Is the market open or closed"},
    "aspiData":             {"method": "POST", "desc": "All Share Price Index"},
    "marketSummery":        {"method": "POST", "desc": "Today's turnover and volume"},
    "tradeSummary":         {"method": "POST", "desc": "Trade data for every company"},
    "topGainers":           {"method": "POST", "desc": "Companies that rose the most"},
    "topLooses":            {"method": "POST", "desc": "Companies that fell the most"},
    "allSectors":           {"method": "POST", "desc": "Sector indices"},
    "allSecurityCode":      {"method": "GET",  "desc": "List of all listed companies"},
    "companyInfoSummery":   {"method": "POST", "desc": "One company's details"},
    "approvedAnnouncement": {"method": "POST", "desc": "Company announcements"},
    "circularAnnouncement": {"method": "POST", "desc": "CSE circulars (with PDFs)"},
}

#-------------------------------------------------------------------------#
#  ETHICAL SCRAPING SETTINGS                                               #
#-------------------------------------------------------------------------#

# A User-Agent that says who we are, instead of hiding behind a fake
# browser name.
USER_AGENT = (
    "CSE-Academic-Scraper/1.0 "
    "(University of Colombo; DA 2009 group project; "
    "contact: nuhanmalee@gmail.com)"
)

# Seconds to wait between requests so we do not overload the server.
DELAY = 1.5
MIN_DELAY = 0.5
MAX_DELAY = 10.0

TIMEOUT = 30

# Line added to every file we export, so the source is always credited.
ATTRIBUTION = (
    "Data source: Colombo Stock Exchange (https://www.cse.lk). "
    "Collected for academic purposes only - DA 2009, University of Colombo."
)

#-------------------------------------------------------------------------#
#  FOLDERS                                                                 #
#-------------------------------------------------------------------------#

ROOT_DIR   = Path(__file__).parent
DATA_DIR   = ROOT_DIR / "data"
RAW_DIR    = DATA_DIR / "raw"
PDF_DIR    = DATA_DIR / "pdfs"
IMAGE_DIR  = DATA_DIR / "images"      # page images made for OCR
EXPORT_DIR = DATA_DIR / "exports"
CACHE_DIR  = DATA_DIR / "cache"
LOG_DIR    = ROOT_DIR / "logs"
DOCS_DIR   = ROOT_DIR / "docs"

for _folder in (RAW_DIR, PDF_DIR, IMAGE_DIR, EXPORT_DIR, CACHE_DIR,
                LOG_DIR, DOCS_DIR):
    _folder.mkdir(parents=True, exist_ok=True)

REQUEST_LOG = LOG_DIR / "request_log.csv"

#-------------------------------------------------------------------------#
#  PDF AND OCR SETTINGS                                                    #
#-------------------------------------------------------------------------#

# If a PDF page gives us fewer characters than this, we treat it as a
# scanned image and send it to OCR instead.
OCR_TEXT_THRESHOLD = 50

# Resolution used when turning a PDF page into an image for OCR.
OCR_DPI = 200

APP_PORT = 7860
