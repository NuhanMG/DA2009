"""
Content for the deep guide written for 24ada076.

Returns finished PDF blocks, so it can lay things out exactly.
"""

from guide_content import pdf_engine as E


def build():
    b = []

    #=====================================================================#
    b += E.h1("How to use this guide")

    b += E.p(
        "This guide covers the whole project, not only your own files. You "
        "are presenting it and you own the ethics section, so you are the "
        "most likely person to be asked about how the parts fit together.")

    b += E.p("It is arranged so you can read it in three passes:")

    b += E.numbered([
        "**Sections 2 to 4** - what the project does, why it is built this "
        "way, and how a request travels from the button to the screen. Read "
        "this first. It is what you would say if somebody asked you to "
        "explain the project in two minutes.",

        "**Sections 5 to 7** - your three files, walked through in order, "
        "with the real code. This is the detail you need for questions "
        "about your own part.",

        "**Sections 8 to 10** - what everybody else's files do, how the "
        "screen is wired up, and how to run each piece. Read this so no "
        "question about the project can catch you out.",
    ])

    b += E.note(
        "**Your 50 questions are in the shared team guide**, in the section "
        "headed 24ada076 - Nuhan. This document is the explanation behind those "
        "answers.")

    #=====================================================================#
    b += E.page_break()
    b += E.h1("The project in one page")

    b += E.p(
        "We collect share prices, company details and announcements from the "
        "Colombo Stock Exchange, clean the result, and save it as CSV, Excel "
        "and JSON files.")

    b += E.h2("The four numbers to remember")

    b += E.table([
        ["Figure", "Value", "Where it comes from"],
        ["Text `requests` finds on the CSE page",
         "about 24 characters, no tables",
         "`python -m src.static_scraper`"],
        ["Companies in one request", "around 290",
         "`/api/tradeSummary`"],
        ["Delay between our requests", "1.5 seconds",
         "`config.DELAY`"],
        ["Section blocked by robots.txt", "`/cgi-bin/` only",
         "`https://www.cse.lk/robots.txt`"],
    ], widths=[3.4, 2.4, 3.0])

    b += E.h2("The story in five sentences")

    b += E.numbered([
        "We tried `requests` and BeautifulSoup, and got almost nothing, "
        "because the CSE page is built by JavaScript.",
        "We opened the site with F12 and watched the Network tab, which "
        "showed the page fetching its own data from `/api/` addresses.",
        "Those addresses return JSON, so we read them directly - one request "
        "gives every company.",
        "Announcements link to PDF documents, which we download and read "
        "with pdfplumber and PyPDF2.",
        "One of those documents is a scan with no text inside, so that one "
        "goes through OCR.",
    ])

    #=====================================================================#
    b += E.page_break()
    b += E.h1("Why the project is built this way")

    b += E.h2("What went wrong with the ordinary approach")

    b += E.p(
        "The course teaches: download the page with `requests`, parse it "
        "with BeautifulSoup. On CSE that produces this:")

    b += E.code(
        "Status     : 200          <- the request worked perfectly\n"
        "HTML size  : 25,071 bytes <- there is plenty of HTML\n"
        "Words found: 24 characters\n"
        "Tables     : 0")

    b += E.p(
        "Nothing failed. The request succeeded, BeautifulSoup parsed the "
        "HTML without complaint. There is simply nothing in the file to "
        "find.")

    b += E.h2("Static and dynamic content")

    b += E.table([
        ["", "Static page", "Dynamic page"],
        ["Where the content is",
         "Already inside the HTML the server sends",
         "Added by JavaScript after the page loads"],
        ["Does `requests` see it?", "Yes", "No - it never runs JavaScript"],
        ["How to check",
         "View Page Source shows the content",
         "View Page Source is empty, but Inspect shows the content"],
        ["CSE", "-", "This one"],
    ], widths=[2.2, 3.2, 3.4])

    b += E.p(
        "The practical test takes ten seconds. **View Page Source** shows "
        "what the server sent; **Inspect** shows the page as it is now. If "
        "the numbers are in Inspect but not in View Source, it is dynamic.")

    b += E.h2("Proving the library was not the problem")

    b += E.p(
        "The obvious follow-up question is whether we just used BeautifulSoup "
        "badly. So `src/static_scraper.py` also points the same library at "
        "CSE's sitemap, an ordinary file with no JavaScript:")

    b += E.code(
        "15 pages read from the sitemap without any trouble\n"
        "\n"
        "  Page                                  Updated\n"
        "  https://www.cse.lk/                   daily\n"
        "  https://www.cse.lk/about-us/          monthly\n"
        "  https://www.cse.lk/market-summary/    daily")

    b += E.p(
        "Same library, same methods, perfect result. That isolates the "
        "problem to the page.")

    b += E.h2("The way in")

    b += E.p(
        "Week 1 gave the fix as well as the problem: use the Network tab. "
        "Opening the site with F12 showed the page requesting its own data:")

    b += E.code(
        "POST https://www.cse.lk/api/tradeSummary       -> 200, JSON\n"
        "GET  https://www.cse.lk/api/allSecurityCode    -> 200, JSON")

    b += E.p(
        "Those replies are JSON, so pandas turns them into a table in one "
        "line. No login is needed, and `robots.txt` does not ask us to stay "
        "away from them.")

    b += E.note(
        "**The ethical argument, which is the one that matters.** Loading "
        "the page makes CSE send the HTML, the JavaScript, the fonts and "
        "the images, and then the browser calls that same data address at "
        "the end of it anyway. Reading the address directly skips all of "
        "that work. It is less load on their server, not more.")

    #=====================================================================#
    # No page break here on purpose: the section above ends on a full page,
    # so forcing one would leave an almost empty sheet.
    b += E.h1("How the whole thing fits together")

    b += E.h2("The files and what depends on what")

    b += E.code(
        "app.py                     the screen, 7 tabs\n"
        "  |\n"
        "  +-- src/ethics.py        Scraper.fetch()  <-- ALL requests\n"
        "  |     |                                       pass through here\n"
        "  |     +--> robots.txt check\n"
        "  |     +--> 1.5 second wait\n"
        "  |     +--> requests.Session\n"
        "  |     +--> logs/request_log.csv\n"
        "  |     +--> data/cache/*.json\n"
        "  |\n"
        "  +-- src/api_client.py    uses Scraper -> the market data\n"
        "  +-- src/crawler.py       uses Scraper -> downloads PDFs\n"
        "  +-- src/static_scraper.py uses Scraper -> requests + BS4\n"
        "  |\n"
        "  +-- src/selenium_scraper.py   drives its own browser\n"
        "  +-- src/pdf_extractor.py      reads files already on disk\n"
        "  +-- src/ocr_extractor.py      reads files already on disk\n"
        "  +-- src/cleaner.py            pure pandas, no internet\n"
        "  +-- src/analysis.py           pure plotly, no internet\n"
        "  +-- src/storage.py            writes files out")

    b += E.p(
        "The important shape here: the four files at the top touch the "
        "internet, and every one of them goes through `Scraper`. Everything "
        "below works on data that is already on the computer.")

    b += E.h2("An honest gap, in case you are asked")

    b += E.p(
        "`src/selenium_scraper.py` does **not** go through `Scraper`. It "
        "drives a browser, and the browser makes its own requests, so our "
        "`fetch()` function never sees them.")

    b += E.p(
        "If somebody points that out, the honest answer is: that is true. "
        "What we do instead is give the browser the same User-Agent, load "
        "one page rather than crawling, and check by hand that the page is "
        "allowed. It is a demonstration script that runs a handful of times, "
        "not part of the collection pipeline. But it is a real exception to "
        "the rule, and it is better to say so than to claim otherwise.")

    #=====================================================================#
    b += E.page_break()
    b += E.h1("The pipeline, from button to file")

    b += E.p(
        "This is the sequence to have ready if you are asked to explain how "
        "the project works. Every tab follows it.")

    b += E.code(
        "1. You click a button in app.py\n"
        "        |\n"
        "2. app.py calls something like  api.trade_summary()\n"
        "        |                       (src/api_client.py)\n"
        "        |\n"
        "3. that calls  self.call(\"tradeSummary\")\n"
        "        |      which looks up GET or POST in config.ENDPOINTS\n"
        "        |\n"
        "4. that calls  Scraper.fetch(url, method=\"POST\", ...)\n"
        "        |      (src/ethics.py)  <-- THE ONE DOOR\n"
        "        |\n"
        "        |      a. can_fetch(url)   is robots.txt happy?\n"
        "        |      b. wait()           sleep until 1.5s has passed\n"
        "        |      c. session.post()   send it, with our User-Agent\n"
        "        |      d. log_request()    write a row to the CSV log\n"
        "        |      e. save_copy()      keep a copy of the reply\n"
        "        |\n"
        "5. the JSON reply comes back as a Python list of dictionaries\n"
        "        |\n"
        "6. get_records() finds the list, make_dataframe() builds the table\n"
        "        |\n"
        "7. the table goes back to app.py and onto the screen\n"
        "        |\n"
        "8. optionally: clean() -> check() -> chart -> export()")

    b += E.h2("Where things end up on disk")

    b += E.table([
        ["Folder", "What goes there", "Written by"],
        ["`data/cache/`", "A copy of every reply, named after the address",
         "`src/ethics.py`"],
        ["`data/pdfs/`", "The announcement documents we downloaded",
         "`src/crawler.py`"],
        ["`data/images/`", "Page images made for OCR, plus each cleaning step",
         "`src/ocr_extractor.py`"],
        ["`data/exports/`", "The CSV, Excel and JSON files",
         "`src/storage.py`"],
        ["`logs/request_log.csv`", "One row per request, ever",
         "`src/ethics.py`"],
    ], widths=[2.3, 4.0, 2.2])

    #=====================================================================#
    b += E.page_break()
    b += E.h1("Your file 1 - src/ethics.py")

    b += E.p(
        "This is the most important file in the project, and it is the one "
        "the assignment weights most heavily. It has two classes.")

    b += E.h2("ScraperLog - the record")

    b += E.p(
        "Two jobs. It keeps the messages shown on screen, and it writes "
        "every request to `logs/request_log.csv`. That CSV is the evidence "
        "for how the data was collected - if anyone asks whether we "
        "hammered their server, that file is the answer.")

    b += E.code(
        "def log_request(self, method, url, status, allowed):\n"
        "    self.request_count += 1\n"
        "    new_file = not config.REQUEST_LOG.exists()\n"
        "\n"
        "    with open(config.REQUEST_LOG, \"a\", newline=\"\",\n"
        "              encoding=\"utf-8\") as f:\n"
        "        writer = csv.writer(f)\n"
        "        if new_file:\n"
        "            writer.writerow([\"time\", \"method\", \"url\", \"status\",\n"
        "                             \"robots_allowed\", \"delay_seconds\"])\n"
        "        writer.writerow([...])")

    b += E.p(
        "Note the `\"a\"` mode - it appends, so the log builds up across "
        "runs rather than being overwritten each time.")

    b += E.h2("Scraper - reading the rules")

    b += E.p(
        "`read_robots()` downloads the file and hands it to "
        "`RobotFileParser`, which is part of Python's standard library and "
        "already understands the format. We feed it the text we downloaded "
        "rather than letting it fetch the address itself, so the rules come "
        "from exactly the bytes we can show on screen.")

    b += E.code(
        "def read_robots(self):\n"
        "    try:\n"
        "        response = requests.get(config.ROBOTS_URL, ...)\n"
        "        self.robots_text = response.text\n"
        "\n"
        "        self.robots = RobotFileParser()\n"
        "        self.robots.parse(self.robots_text.splitlines())\n"
        "    except Exception as e:\n"
        "        self.robots = None          # fail closed, not open")

    b += E.p(
        "If it cannot be read we set `self.robots = None`, and `can_fetch()` "
        "then returns False for everything. If we cannot see the rules we do "
        "not guess in our own favour.")

    b += E.h2("Scraper - the waiting")

    b += E.p(
        "`wait()` measures rather than blindly sleeping. If parsing the last "
        "reply already took a second, we only need another half second - the "
        "server got its 1.5 seconds either way.")

    b += E.code(
        "def wait(self):\n"
        "    since_last = time.time() - self.last_request_time\n"
        "    if since_last < self.delay:\n"
        "        time.sleep(self.delay - since_last)\n"
        "    self.last_request_time = time.time()")

    b += E.h2("Scraper - fetch(), the one door")

    b += E.p(
        "Everything comes through here. The order of the four steps is the "
        "thing to remember, because the permission check being first is what "
        "makes the ethics claim true rather than aspirational.")

    b += E.code(
        "def fetch(self, url, method=\"GET\", data=None,\n"
        "          save_as=None, want=\"json\"):\n"
        "\n"
        "    # 1. are we allowed?\n"
        "    allowed, reason = self.can_fetch(url)\n"
        "    if not allowed:\n"
        "        self.log.log_request(method, url, \"skipped\", allowed)\n"
        "        return {\"ok\": False, \"error\": ...}\n"
        "\n"
        "    # 2. wait\n"
        "    self.wait()\n"
        "\n"
        "    try:\n"
        "        # 3. send it\n"
        "        if method == \"POST\":\n"
        "            response = self.session.post(url, data=data, ...)\n"
        "        else:\n"
        "            response = self.session.get(url, ...)\n"
        "\n"
        "        # 4. record it\n"
        "        self.log.log_request(method, url,\n"
        "                             response.status_code, allowed)\n"
        "\n"
        "        if response.status_code != 200:\n"
        "            return {\"ok\": False, \"error\": ...}\n"
        "\n"
        "        result = response.json()\n"
        "        if save_as:\n"
        "            self.save_copy(save_as, result)\n"
        "        return {\"ok\": True, \"data\": result, ...}\n"
        "\n"
        "    except Exception as e:\n"
        "        # fall back to the saved copy if we have one\n"
        "        if save_as:\n"
        "            saved = self.load_copy(save_as)\n"
        "            if saved is not None:\n"
        "                return {\"ok\": True, \"data\": saved,\n"
        "                        \"from_file\": True}\n"
        "        return {\"ok\": False, \"error\": str(e)}")

    b += E.h3("Three design decisions worth being able to defend")

    b += E.bullets([
        "**It returns a dictionary instead of raising.** This runs behind a "
        "web page. An uncaught error would take the whole app down; an "
        "`ok: False` can be shown neatly on screen.",

        "**The permission check is the first statement.** Not somewhere in "
        "the middle, and not optional. It is not possible to send a request "
        "that skips it, because this is the only function that sends "
        "requests.",

        "**The saved copy is a fallback, not a shortcut.** We always try "
        "live first. The copy is only used when the request fails - which is "
        "what keeps a demonstration working if the venue internet drops.",
    ])

    #=====================================================================#
    b += E.page_break()
    b += E.h1("Your file 2 - src/static_scraper.py")

    b += E.p(
        "This is the `requests` and BeautifulSoup part. It does not collect "
        "the project's data, and it is in the project deliberately - it is "
        "the reasoning behind the design, written as code you can run.")

    b += E.h2("What it measures")

    b += E.p(
        "`scrape_page()` downloads a page and counts what BeautifulSoup can "
        "find in it - the size of the HTML, the number of readable "
        "characters, the number of tables and links.")

    b += E.code(
        "soup = BeautifulSoup(html, \"html.parser\")\n"
        "\n"
        "title  = soup.title.get_text(strip=True)\n"
        "words  = soup.get_text(strip=True)\n"
        "tables = soup.find_all(\"table\")\n"
        "links  = soup.find_all(\"a\")")

    b += E.h2("The methods, and what each returns")

    b += E.table([
        ["Method", "What it does", "Example"],
        ["`find()`", "The first matching tag", "`soup.find('title')`"],
        ["`find_all()`", "Every matching tag, as a list",
         "`soup.find_all('a')`"],
        ["`select()`", "Every match, using a CSS selector",
         "`soup.select('div.price')`"],
        ["`select_one()`", "The first CSS match",
         "`soup.select_one('#total')`"],
        ["`get_text()`", "The words inside a tag",
         "`tag.get_text(strip=True)`"],
        ["`get()`", "One attribute of a tag", "`tag.get('href')`"],
    ], widths=[1.8, 3.6, 3.1])

    b += E.p(
        "`strip=True` on `get_text()` removes the whitespace around the "
        "text. Without it you get newlines and indentation from the HTML "
        "source mixed in with the words.")

    b += E.h2("The sitemap, and why it is in the file")

    b += E.p(
        "`scrape_sitemap()` reads CSE's `sitemap.xml` - a file where the "
        "site lists its own pages for programs like ours. It is ordinary "
        "static content, and BeautifulSoup reads it perfectly.")

    b += E.p(
        "It is there to answer the obvious challenge to the failure above. "
        "Same library, same methods, working result - so the problem was the "
        "page, not the tool.")

    b += E.code(
        "try:\n"
        "    soup = BeautifulSoup(response.text, \"xml\")\n"
        "except Exception:\n"
        "    soup = BeautifulSoup(response.text, \"html.parser\")")

    b += E.p(
        "The `xml` mode needs lxml installed, so there is a fallback to the "
        "built-in parser. Nothing in the project should break because of an "
        "optional library.")

    #=====================================================================#
    b += E.page_break()
    b += E.h1("Your file 3 - src/pdf_extractor.py")

    b += E.h2("Why two libraries")

    b += E.table([
        ["", "PyPDF2", "pdfplumber"],
        ["What it is for", "General PDF work - text, metadata, merging",
         "Text extraction that respects the layout"],
        ["Layout", "Often merges lines and loses structure",
         "Keeps the layout using the position of the text"],
        ["Tables", "No table support", "Can detect and extract tables"],
        ["We use it for", "The file details - pages, author, producer",
         "The main text extraction, and tables"],
    ], widths=[1.9, 3.3, 3.3])

    b += E.h2("Deciding whether a page is a scan")

    b += E.code(
        "def page_type(text):\n"
        "    length = len(text.strip())\n"
        "\n"
        "    if length < config.OCR_TEXT_THRESHOLD:     # 50\n"
        "        return \"Scanned image\", f\"Only {length} characters\"\n"
        "    return \"Text based\", f\"{length:,} characters read\"")

    b += E.p(
        "The threshold is 50 rather than 0. A real page of a CSE circular "
        "returns over a thousand characters and a scan returns nothing, so "
        "almost anything would work - but a scan sometimes carries a few "
        "stray characters that are not the document text, such as a header "
        "added afterwards. Requiring a real amount of text means a handful "
        "of stray letters cannot fool us into skipping OCR.")

    b += E.h2("The None trap")

    b += E.code("text = page.extract_text() or \"\"")

    b += E.p(
        "`extract_text()` returns `None`, not an empty string, when a page "
        "has nothing on it. Calling `.strip()` or `len()` on `None` raises "
        "an error - and the pages most likely to return `None` are exactly "
        "the scanned ones we care about. The `or \"\"` makes every page "
        "safe to handle the same way.")

    b += E.h2("What the file details give you")

    b += E.p(
        "PyPDF2 can read the information stored inside the PDF, which is "
        "often more revealing than people expect:")

    b += E.code(
        "Pages          1\n"
        "Title          not set\n"
        "Author         Nirmalee Ganegoda\n"
        "Created with   Microsoft Word for Microsoft 365")

    b += E.p(
        "That tells you the document was typed in Word rather than scanned, "
        "which is a second clue on top of the character count.")

    #=====================================================================#
    b += E.page_break()
    b += E.h1("What everybody else's files do")

    b += E.p(
        "Enough to answer a question about any part of the project without "
        "having to hand over to somebody else.")

    b += E.h2("25ada072 - Pasindu: api_client.py and selenium_scraper.py")

    b += E.bullets([
        "`call()` looks up whether an address needs GET or POST in "
        "`config.ENDPOINTS`, then hands it to your `Scraper.fetch()`.",

        "`get_records()` exists because the replies are not all shaped the "
        "same - some are a plain list, some wrap the list under a name like "
        "`reqTradeSummery`, some are a list inside a list.",

        "`make_dataframe()` turns the list of dictionaries into a table, and "
        "converts any millisecond timestamps into real dates.",

        "`selenium_scraper.py` opens the page in Edge, waits for the table "
        "to appear with `WebDriverWait`, takes `driver.page_source`, and "
        "parses that with BeautifulSoup. It only gets about 25 companies, "
        "because the table on screen is paginated.",
    ])

    b += E.h2("25ada073 - Sasini: crawler.py, cleaner.py and the Scrapy spider")

    b += E.bullets([
        "`find_documents()` builds the full PDF address from the fragment "
        "the listing gives, by putting `https://cdn.cse.lk/cmt/` in front "
        "of it, and removes duplicates.",

        "`download_documents()` fetches them one at a time through your "
        "`Scraper`, and checks the first four bytes are `%PDF` before "
        "saving.",

        "`cleaner.py` converts millisecond dates into real dates, turns "
        "numbers-stored-as-text into numbers, drops columns that are empty "
        "for every company, and strips extra spaces. Then `check()` asks "
        "whether the values are believable.",

        "The Scrapy spider does the crawl a second time using the framework "
        "- `start()` sends the first POSTs, `parse()` follows each PDF link, "
        "`parse_document()` records the result.",
    ])

    b += E.h2("25ada141 - Salaama: ocr_extractor.py, storage.py and analysis.py")

    b += E.bullets([
        "OCR runs in four steps: pdfplumber turns the page into an image, "
        "OpenCV converts it to grey then to black and white (plus the "
        "lecture's optional noise step, which at 1x1 changes nothing), "
        "pytesseract reads the letters, pandas tidies the result.",

        "`tesseract_ready()` calls `get_tesseract_version()`, because "
        "importing pytesseract succeeds even when the Tesseract program "
        "itself is missing.",

        "`storage.py` writes CSV, Excel and JSON, and puts the source inside "
        "each one - comment lines in the CSV, a second sheet in the Excel "
        "file, a details block in the JSON.",

        "`analysis.py` builds three charts and works out the summary "
        "figures - how many companies rose, how many fell, total turnover.",
    ])

    #=====================================================================#
    b += E.page_break()
    b += E.h1("How the screen is wired up")

    b += E.p(
        "`app.py` holds no collection logic. It calls the modules and puts "
        "the results on screen. Understanding two things is enough.")

    b += E.h2("Shared state")

    b += E.p(
        "One `State` object holds the `Scraper`, the `CSEApi`, and whatever "
        "data has been collected so far, so a table fetched on one tab can "
        "be cleaned on another. Both are created the first time they are "
        "needed, so the window opens instantly instead of waiting for "
        "robots.txt.")

    b += E.code(
        "@property\n"
        "def scraper(self):\n"
        "    if self._scraper is None:\n"
        "        self._scraper = Scraper()\n"
        "    return self._scraper")

    b += E.h2("Buttons")

    b += E.p(
        "Every button follows the same pattern: a function does the work and "
        "returns values, and `.click()` says which boxes on screen those "
        "values go into, in order.")

    b += E.code(
        "market_button.click(get_market_data,\n"
        "                    outputs=[market_figures_html, trades_table,\n"
        "                             sectors_table, addresses_table,\n"
        "                             market_log])")

    b += E.p(
        "So `get_market_data()` returns five things, and they fill those "
        "five boxes. If you ever add an output you must add it in both "
        "places, or Gradio raises an error about the count not matching.")

    #=====================================================================#
    b += E.page_break()
    b += E.h1("Running it, and the demonstration")

    b += E.h2("Starting the app")

    b += E.code(
        "cd D:\\DA2009\\CSE-Scraping-Project\n"
        ".venv\\Scripts\\activate\n"
        "python app.py\n"
        "\n"
        "then open  http://127.0.0.1:7860")

    b += E.h2("Running each part on its own")

    b += E.p(
        "Each member can show their own work without launching the app:")

    b += E.code(
        "python -m src.ethics             # 24ada076 - Nuhan\n"
        "python -m src.static_scraper     # 24ada076 - Nuhan\n"
        "python -m src.pdf_extractor      # 24ada076 - Nuhan\n"
        "python -m src.api_client         # 25ada072 - Pasindu\n"
        "python -m src.selenium_scraper   # 25ada072 - Pasindu\n"
        "python -m src.crawler            # 25ada073 - Sasini\n"
        "python -m src.cleaner            # 25ada073 - Sasini\n"
        "python -m src.ocr_extractor      # 25ada141 - Salaama\n"
        "python -m src.storage            # 25ada141 - Salaama\n"
        "python -m src.analysis           # 25ada141 - Salaama")

    b += E.h2("Before the viva")

    b += E.numbered([
        "Run `python warm_cache.py`. It collects everything once and saves a "
        "copy, so the demonstration works even if the internet does not.",
        "Check the OCR tab actually runs. It needs the Tesseract program "
        "installed, not just the Python package.",
        "Open the Ethics tab and press the button, so `robots.txt` is "
        "already on screen when you start talking.",
        "Have `logs/request_log.csv` ready to show if anybody asks about "
        "load.",
    ])

    b += E.h2("A three minute run through the app")

    b += E.table([
        ["Time", "Tab", "What to say"],
        ["0:00", "Home",
         "What we collect, and that the site is JavaScript so the ordinary "
         "approach found nothing."],
        ["0:30", "Ethics",
         "Press the button. Show the real robots.txt, the one blocked "
         "section, and that we wait anyway."],
        ["1:15", "Market Data",
         "Press the button. Around 290 companies from one request."],
        ["1:50", "Announcements",
         "Download a few PDFs, then read the text out of one."],
        ["2:20", "OCR",
         "The scanned one. Show the three cleaning images and the recovered "
         "text."],
        ["2:45", "Data & Export",
         "Clean, chart, and save. Mention the source is inside every file."],
    ], widths=[0.9, 1.9, 5.7])

    return b
