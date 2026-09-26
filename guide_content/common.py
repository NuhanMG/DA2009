"""
The shared explanations used in both guides.

Plain data only - build_guides.py turns this into PDF blocks.
"""

#=========================================================================#
#  WHAT THE PROJECT IS                                                    #
#=========================================================================#

WHAT_WE_DO = [
    "Our group was given the Colombo Stock Exchange, `www.cse.lk`, and asked "
    "to collect data from it. We collect three things:",
]

WHAT_WE_COLLECT = [
    "**Share prices** - what every listed company traded at today. There are "
    "around 290 companies.",
    "**Company details** - the price, the market value, and the highest and "
    "lowest price over the past year, for any company we choose.",
    "**Announcements** - the notices companies publish, such as dividends "
    "and shareholder meetings, and the PDF documents attached to them.",
]

WHAT_WE_DO_AFTER = [
    "Once we have the data we clean it, check it makes sense, draw a few "
    "charts from it, and save it as CSV, Excel and JSON files.",
]

#=========================================================================#
#  THE PROBLEM WE HAD TO SOLVE                                            #
#=========================================================================#

THE_PROBLEM = [
    "We started the way the course taught us: download the page with "
    "`requests`, then read it with BeautifulSoup. On the CSE website that "
    "does not work, and it is important that everybody understands why, "
    "because it is the reason the whole project is built the way it is.",

    "When we download the page we get about 25,000 bytes of HTML back. But "
    "if we ask BeautifulSoup for the words on the page, we get about 24 "
    "characters, and if we ask for the tables we get none at all.",

    "The reason is that the CSE website is built with **JavaScript**. The "
    "server sends an almost empty page, and then a small program running "
    "inside the browser fetches the prices and puts them onto the page "
    "afterwards. `requests` only downloads the file. It does not run "
    "JavaScript, so it never sees the prices.",

    "This is the difference between **static** and **dynamic** content. A "
    "static page has its content sitting in the HTML file. A dynamic page "
    "builds its content after loading. CSE is dynamic.",
]

THE_SOLUTION = [
    "The fix came from the same lecture that described the problem: open the "
    "site in a browser, press **F12**, and look at the **Network** tab. That "
    "tab lists every request the page makes.",

    "Doing that showed the page fetching its own data from addresses like "
    "`https://www.cse.lk/api/tradeSummary`. Those addresses return **JSON**, "
    "which is a tidy, structured format that pandas can read directly. One "
    "request returns every listed company at once.",

    "So our project reads those addresses instead of trying to read the "
    "page. No login is needed, and `robots.txt` does not ask us to stay away "
    "from them - it is exactly the same request the page itself makes for "
    "any ordinary visitor.",
]

#=========================================================================#
#  HOW A REQUEST TRAVELS THROUGH THE PROJECT                              #
#=========================================================================#

THE_FLOW_INTRO = [
    "Everything in the project follows the same path. If you can describe "
    "these six steps, you can explain how any part of it works.",
]

THE_FLOW = [
    "**You click a button** on the screen. `app.py` calls the right function.",

    "**The function asks for some data**, for example "
    "`api.trade_summary()` in `src/api_client.py`.",

    "**That goes to `Scraper.fetch()`** in `src/ethics.py`. Every single "
    "request in the project goes through this one function.",

    "**`fetch()` applies the rules**: it checks `robots.txt`, waits 1.5 "
    "seconds, sends the request saying who we are, and writes a line to "
    "`logs/request_log.csv`.",

    "**The reply comes back as JSON**, and pandas turns it into a table "
    "(a DataFrame).",

    "**The table goes back to the screen**, and from there it can be "
    "cleaned, charted, or saved to a file.",
]

#=========================================================================#
#  ETHICS - EVERYBODY NEEDS THIS                                          #
#=========================================================================#

ETHICS_INTRO = [
    "The assignment says marks are given for following ethical scraping "
    "practices. This section belongs to 24ada076 - Nuhan, but **every member should "
    "be able to answer questions on it**, because it is the part the "
    "assignment singles out.",
]

ETHICS_POINTS = [
    "**robots.txt** is a file websites publish telling automated programs "
    "which pages they may visit. Following it is voluntary. We follow it "
    "because that is what ethical scraping means.",

    "**CSE's robots.txt blocks one section**, `/cgi-bin/`, and allows "
    "everything else. It does **not** ask us to wait between requests.",

    "**We wait 1.5 seconds anyway.** Being allowed to go fast is not a "
    "reason to. Sending requests as fast as the computer can manage would "
    "put load on their server for no benefit to us.",

    "**We say who we are.** Our User-Agent gives the university, the course "
    "and an email address, instead of pretending to be an ordinary browser.",

    "**We save a copy of every reply**, so we never ask for the same thing "
    "twice.",

    "**We only collect public data.** No logins, no paywalls, no CAPTCHAs, "
    "and no personal information about any individual - only company "
    "figures that CSE publishes for everyone.",

    "**We credit the source.** Every file we export names the Colombo Stock "
    "Exchange and records when the data was collected.",
]

#=========================================================================#
#  THE MEMBERS                                                            #
#=========================================================================#

MEMBERS = {
    "24ada076": {
        "title": "Ethical scraping, BeautifulSoup, and reading PDFs",
        "one_line": "The rules every request follows, the first attempt at "
                    "scraping the page, and getting the text out of PDF "
                    "documents.",
        "simple": [
            "Your part has three pieces.",

            "**First, the rules.** `src/ethics.py` is the only file in the "
            "project that is allowed to talk to the internet. Every request "
            "made by anybody's code goes through your `fetch()` function. "
            "That function reads `robots.txt`, checks whether we are allowed "
            "to request the address, waits 1.5 seconds, sends the request "
            "with our honest User-Agent, and writes the result to a log "
            "file. Putting it in one place means the rules cannot be "
            "forgotten somewhere else.",

            "**Second, BeautifulSoup.** `src/static_scraper.py` is the "
            "ordinary way of scraping - download the page with `requests`, "
            "then pick things out of it with BeautifulSoup. On the CSE page "
            "it finds almost nothing, and that result is the reason the rest "
            "of the project reads the JSON addresses instead. The same file "
            "then points BeautifulSoup at the sitemap, which is an ordinary "
            "file, and reads it perfectly - proving the library was never "
            "the problem.",

            "**Third, PDFs.** `src/pdf_extractor.py` opens the documents we "
            "download and pulls the text out. It uses two libraries: PyPDF2, "
            "which is simple and also gives the file details, and "
            "pdfplumber, which keeps the layout better and can find tables. "
            "It also works out whether a PDF is a real document or a scan, "
            "because a scan has no text inside it and has to go to OCR "
            "instead.",
        ],
        "files": [
            ("src/ethics.py",
             "The whole file. Especially `read_robots()`, `can_fetch()`, "
             "`wait()` and `fetch()`."),
            ("src/static_scraper.py",
             "`scrape_page()` and `beautifulsoup_methods()`."),
            ("src/pdf_extractor.py",
             "`page_type()`, `read_with_pypdf2()` and "
             "`read_with_pdfplumber()`."),
            ("config.py",
             "Just the settings section - the User-Agent, the delay, and "
             "the OCR threshold."),
        ],
        "must_know": [
            "What robots.txt is, and what CSE's actually says.",
            "Why we wait 1.5 seconds when nothing forces us to.",
            "The common HTTP status codes: 200, 403, 404, 500.",
            "Why `requests` finds almost no text on the CSE page.",
            "The BeautifulSoup methods and what each one returns.",
            "The difference between PyPDF2 and pdfplumber.",
            "Why a scanned PDF gives no text at all.",
        ],
    },

    "25ada072": {
        "title": "Getting the data from the site, and Selenium",
        "one_line": "Reading the JSON addresses that hold the real data, "
                    "and driving a real browser when JavaScript has to run.",
        "simple": [
            "Your part has two pieces.",

            "**First, the data.** `src/api_client.py` is where the project "
            "actually gets its numbers. The CSE website loads its own data "
            "from addresses like `/api/tradeSummary`. Those addresses return "
            "JSON - a structured text format - and your file sends the "
            "request, takes the reply apart, and turns it into a pandas "
            "table. There is one method per thing we want: the market index, "
            "the share prices, the sector list, one company's details, and "
            "the announcements.",

            "An **API** is just a way for one program to ask another for "
            "data. You send a request, you get a reply. A website has one so "
            "its own pages can load data without reloading, and it is often "
            "left open so other people can use it too.",

            "**Second, Selenium.** `src/selenium_scraper.py` opens the CSE "
            "page in a real browser. Because it is a real browser, the "
            "JavaScript runs, the table gets built, and the prices are "
            "actually on the page. We then take the finished HTML with "
            "`driver.page_source` and read it with BeautifulSoup as normal.",

            "Selenium proves the browser approach works, but it is not our "
            "main method. It takes several seconds instead of one, it makes "
            "CSE serve the whole page with all its images and scripts, and "
            "the table on screen is split into pages so one load only gives "
            "about 25 companies. The API gives all of them in one request.",
        ],
        "files": [
            ("src/api_client.py",
             "`call()`, `trade_summary()`, `company_info()` and the two "
             "helpers `get_records()` and `make_dataframe()`."),
            ("src/selenium_scraper.py",
             "`start_browser()`, `load_page()` and `read_table()`."),
            ("config.py",
             "The `ENDPOINTS` table - the list of addresses and whether "
             "each needs GET or POST."),
        ],
        "must_know": [
            "What an API is, in plain words.",
            "How we found the addresses using the Network tab.",
            "Why those addresses need POST and not GET.",
            "How a JSON reply becomes a pandas DataFrame.",
            "How Selenium makes the JavaScript run.",
            "What `WebDriverWait` is for and why a fixed sleep is worse.",
            "Why the API is our main method and Selenium is the backup.",
        ],
    },

    "25ada073": {
        "title": "Crawling for documents, and cleaning the data",
        "one_line": "Finding and downloading the PDF documents, the Scrapy "
                    "spider, and tidying the data once it arrives.",
        "simple": [
            "Your part has two pieces.",

            "**First, crawling.** There is a difference between scraping and "
            "crawling. Scraping is taking data from a page you already know "
            "about. Crawling is finding pages by following links. Most of "
            "our project is scraping, because we know the address. Your part "
            "is the crawling.",

            "`src/crawler.py` reads the list of circulars, and for each one "
            "works out where the PDF actually lives. The list only gives "
            "part of the address, something like "
            "`upload_report_file/abc123.pdf`, and the PDFs are stored on a "
            "different server from the website. We tried the likely "
            "addresses until one returned a real PDF, which turned out to be "
            "`https://cdn.cse.lk/cmt/` followed by that path. Then it "
            "downloads them one at a time, with a pause between each.",

            "`scrapy_project/` does the same job again using Scrapy, which "
            "is the framework the lecture described as widely used in "
            "industry. The spider starts at the announcement addresses, "
            "reads the list, and then follows the link to each PDF - that "
            "following step is what makes it a crawler.",

            "**Second, cleaning.** `src/cleaner.py` fixes the data after it "
            "arrives, because data taken from a website is never ready to "
            "use straight away. Dates come as huge numbers, some numbers "
            "come as text, some columns are empty for every company, and "
            "text has extra spaces around it. The file also runs checks "
            "afterwards, which is a different job: cleaning fixes the shape "
            "of the data, checking asks whether the values are believable.",
        ],
        "files": [
            ("src/crawler.py",
             "`find_documents()` and `download_documents()`."),
            ("src/cleaner.py",
             "`clean()` and `check()`, and the `describe()` counts."),
            ("scrapy_project/cse_crawler/spiders/cse_announcements.py",
             "`start()`, `parse()` and `parse_document()`."),
            ("scrapy_project/cse_crawler/settings.py",
             "The polite settings near the top."),
        ],
        "must_know": [
            "The difference between scraping and crawling.",
            "How the full PDF address is built from the fragment.",
            "How we check a downloaded file really is a PDF.",
            "How the Scrapy spider follows links.",
            "Which Scrapy settings keep it polite.",
            "The four things that had to be cleaned in the CSE data.",
            "The difference between cleaning and checking.",
        ],
    },

    "25ada141": {
        "title": "OCR, saving the files, and the charts",
        "one_line": "Reading scanned documents that contain no text, saving "
                    "everything with the source credited, and the charts.",
        "simple": [
            "Your part has three pieces, and the first is the hardest thing "
            "in the project.",

            "**First, OCR.** Some of the CSE documents are scans - somebody "
            "printed a page, signed it, and put it through a scanner. What "
            "is inside the file is a photograph of the words. There is no "
            "text in it, so no PDF library can pull anything out, no matter "
            "which one you try.",

            "OCR stands for Optical Character Recognition, and it means "
            "getting a computer to look at a picture of writing and work out "
            "the letters. `src/ocr_extractor.py` does it in four steps: turn "
            "the PDF page into an image, clean the image up with OpenCV, "
            "read the letters with pytesseract, and then tidy the result "
            "into a table with pandas.",

            "The cleaning up matters more than people expect. Tesseract "
            "reads plain black text on a white background best, so we remove "
            "the colour and then turn every pixel either black or white. "
            "There is also the lecture's optional noise removal step, "
            "which at the lecture's setting leaves the image unchanged.",

            "**Second, saving.** `src/storage.py` writes the data out as "
            "CSV, Excel and JSON. Every file carries the source and the time "
            "it was collected, inside the file itself. Each format needs a "
            "different trick: comment lines at the top of a CSV, a second "
            "sheet in an Excel file, and a details section in a JSON file.",

            "**Third, the charts.** `src/analysis.py` builds the bar charts "
            "and works out the summary figures - how many companies rose, "
            "how many fell, and the total turnover.",
        ],
        "files": [
            ("src/ocr_extractor.py",
             "The whole file. Especially `preprocess_image()` and "
             "`ocr_pdf_page()`."),
            ("src/storage.py",
             "`export()` - look at how each format carries the source."),
            ("src/analysis.py",
             "`chart_movers()` and `market_figures()`."),
        ],
        "must_know": [
            "What OCR is and why we needed it here.",
            "The four steps of the OCR pipeline.",
            "Why the image is turned grey and then black and white.",
            "What the dpi setting changes.",
            "How we check whether Tesseract is really installed.",
            "Why OCR makes mistakes, and how we spot them.",
            "How the source gets into each type of exported file.",
        ],
    },
}

MEMBER_ORDER = ["24ada076", "25ada072", "25ada073", "25ada141"]
