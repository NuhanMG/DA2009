"""
Document for 24ada076 - Nuhan.

Ethical scraping and robots.txt (src/ethics.py), requests and BeautifulSoup
(src/static_scraper.py), and reading PDFs (src/pdf_extractor.py).
"""

from guide_content import member_common as M
from guide_content import pdf_engine as E

MEMBER = "24ada076"
FILES = ["src/ethics.py", "src/static_scraper.py", "src/pdf_extractor.py"]


#=========================================================================#
#  THE IDEAS BEHIND YOUR PART                                             #
#=========================================================================#

def ideas():
    b = []
    b += E.h1("The ideas behind your part")
    b += E.p(
        "Your part rests on three ideas: behaving well on somebody else's "
        "website, reading a web page with BeautifulSoup, and getting text "
        "out of PDF documents. This chapter explains each idea before we "
        "look at any code.")

    #--- robots.txt -----------------------------------------------------#
    b += E.h2("Behaving well on somebody else's website")
    b += E.p(
        "A website belongs to somebody. Their server costs money to run, and "
        "it has to answer everybody who visits. A person clicking around "
        "sends a request every few seconds. A program can send hundreds a "
        "second if nobody stops it - and a server flooded like that can slow "
        "down or stop for everyone else.")
    b += E.p(
        "So web scraping comes with manners. The Week 6 lecture put them in "
        "a table:")
    b += E.table([
        ["Ethical scraping", "Unethical scraping"],
        ["Scrapes only publicly visible data, without getting past logins, "
         "CAPTCHAs or paywalls", "Gets past logins, paywalls or CAPTCHAs to "
                                  "reach restricted data"],
        ["Respects the terms of service and follows robots.txt",
         "Ignores the terms and disobeys robots.txt"],
        ["Uses rate limiting so the server is not overloaded",
         "Sends requests too fast, slowing the site or taking it down"],
        ["Follows privacy law and avoids personal data",
         "Collects personal data without permission"],
        ["Credits the source and uses the data fairly",
         "Uses the data with no credit, or to cause harm"],
    ], widths=[4.25, 4.25])
    b += E.p("Your file, `src/ethics.py`, is where our project does the "
             "left-hand column.")

    b += E.h3("robots.txt, line by line")
    b += E.p(
        "**robots.txt** is a plain text file that a website keeps at a fixed "
        "place - the very top of the site - so that programs always know "
        "where to find it. It was agreed as a convention in 1994. It is "
        "**voluntary**: nothing stops a program ignoring it. Following it is "
        "a choice, and it is the choice ethical scrapers make.")
    b += E.p("This is CSE's, exactly as they publish it:")
    b += E.code(
        "User-agent: *\n"
        "Disallow:\n"
        "Disallow: /cgi-bin/\n"
        "Sitemap: https://www.cse.lk/sitemap.xml")
    b += E.table([
        ["Line", "What it means"],
        ["`User-agent: *`", "The rules below are for every program. The "
                            "star means 'everyone'. A site can also write "
                            "separate rules for one named program."],
        ["`Disallow:` (empty)", "An empty Disallow blocks nothing. On its "
                                "own it means 'you may visit everything'."],
        ["`Disallow: /cgi-bin/`", "Keep out of any address that starts "
                                  "with /cgi-bin/."],
        ["`Sitemap: ...`", "Where the site lists its own pages for "
                           "programs to read."],
    ], widths=[2.8, 5.7])
    b += E.p(
        "Just as important is what is **not** there. There is no "
        "`Crawl-delay:` line, which is how a site asks programs to wait a "
        "number of seconds between requests. So CSE does not ask us to wait "
        "at all. We wait 1.5 seconds anyway, because being allowed to go "
        "fast is not a reason to.")
    b += E.idea(
        "robots.txt is a notice on a shop door: 'Staff only beyond this "
        "point'. There is no lock. You stay out because you respect the "
        "people who own the shop.")

    b += E.h3("The /cgi-bin/ puzzle - know this one")
    b += E.p(
        "When you run `python -m src.ethics`, one line of its output looks "
        "wrong:")
    b += E.code("  yes  https://www.cse.lk/cgi-bin/test   (allowed)")
    b += E.p(
        "The site says keep out of /cgi-bin/, so why does our check say "
        "yes? The answer is how Python's robots.txt reader works. It reads "
        "the rules from top to bottom and uses **the first rule that "
        "matches**. CSE's empty `Disallow:` line comes first, and an empty "
        "rule matches every address and allows it - so the reader stops "
        "there and never reaches the /cgi-bin/ line.")
    b += E.p(
        "Some other readers, such as Google's, use the most specific rule "
        "instead, and they would say no. The site owner almost certainly "
        "means 'keep out of /cgi-bin/'. In practice it makes no difference "
        "to us, because **none of the addresses our project uses are in "
        "/cgi-bin/** - we never go near it.")
    b += E.careful(
        "if an examiner spots this line, do not be thrown by it. Explain the "
        "first-match rule and the empty Disallow line, and say that we never "
        "request anything in /cgi-bin/. Knowing why the output looks odd "
        "shows you understand robots.txt better than if the output were "
        "simply 'no'.")

    b += E.h3("How websites defend themselves")
    b += E.p("The Week 6 lecture listed the ways sites protect themselves "
             "from badly behaved programs:")
    b += E.table([
        ["Defence", "What it does", "How our project relates"],
        ["User-Agent checks", "Blocks requests with no name, or a default "
                              "program name", "We send an honest name, so "
                                              "we are easy to recognise"],
        ["Rate limiting", "Limits how many requests one visitor can send",
         "We wait 1.5 s, far slower than any limit"],
        ["CAPTCHAs", "Asks 'are you a person?'", "We never met one, and would "
                                                 "not try to get past one"],
        ["IP blocking", "Bans a computer's address", "We never gave them a "
                                                     "reason to"],
    ], widths=[2.1, 3.1, 3.3])
    b += E.remember(
        "we are not trying to sneak past any of these. We behave well enough "
        "that none of them ever needed to act.")

    #--- HTML and BeautifulSoup -----------------------------------------#
    b += E.h2("Reading a web page with BeautifulSoup")
    b += E.p(
        "**requests** is the library that sends a request and brings back "
        "the reply. If the reply is a web page, what you get is one very long "
        "piece of HTML text. To find the parts you want in it, you need "
        "something that understands HTML. That is **BeautifulSoup**.")
    b += E.p(
        "BeautifulSoup reads the HTML and builds a **tree** - a map of which "
        "tags sit inside which. Then you can ask it questions like 'find the "
        "title' or 'find every table'. Reading the text and building the "
        "tree is called **parsing**, and the part of BeautifulSoup that does "
        "it is the **parser**.")
    b += E.code(
        "html\n"
        " +-- head\n"
        " |    +-- title        'Trade Summary - CSE 2025'\n"
        " +-- body\n"
        "      +-- h1           'Today's prices'\n"
        "      +-- table\n"
        "           +-- tr\n"
        "           |    +-- th 'Company'   +-- th 'Price'\n"
        "           +-- tr\n"
        "                +-- td 'Sampath'   +-- td '141.00'")
    b += E.idea(
        "the HTML is a long letter with no paragraphs. BeautifulSoup turns "
        "it into a family tree, so you can say 'find me the table, and every "
        "row inside it' instead of reading the whole letter yourself.")
    b += E.p("The methods from the Week 4 lecture:")
    b += E.table([
        ["Method", "What it does", "Example"],
        ["`find()`", "The first tag that matches", "`soup.find('title')`"],
        ["`find_all()`", "Every tag that matches, as a list",
         "`soup.find_all('a')`"],
        ["`get_text()`", "The words inside a tag", "`tag.get_text()`"],
        ["`get()`", "The value of one attribute", "`tag.get('href')`"],
        ["`select()`", "Every match for a CSS selector",
         "`soup.select('div > p')`"],
        ["`select_one()`", "The first CSS selector match",
         "`soup.select_one('.title')`"],
    ], widths=[1.9, 3.4, 3.2])
    b += E.p(
        "An **attribute** is extra information inside a tag. In "
        "`<a href=\"https://www.cse.lk\">`, the attribute is `href` and its "
        "value is the address the link goes to.")

    #--- PDFs -----------------------------------------------------------#
    b += E.h2("Getting text out of PDFs")
    b += E.p(
        "A **PDF** is a document format designed to look exactly the same on "
        "every computer and printer. It keeps the fonts, the layout and the "
        "pictures precisely where they were put.")
    b += E.p(
        "The surprising thing is that a PDF is not really a text document at "
        "all. Inside, it is a list of drawing instructions: 'put the letter "
        "D at this spot, the letter E just to its right, draw a line here'. "
        "There is no instruction that says 'this is a paragraph' or 'this is "
        "a table'. A PDF library has to work those out by looking at where "
        "the letters sit.")
    b += E.h3("The three kinds of PDF")
    b += E.table([
        ["Kind", "What is inside", "Can we pull the text out?"],
        ["Text-based", "Real letters, made by a computer (for example saved "
                       "from Word)", "Yes"],
        ["Image-based (scanned)", "A photograph of a printed page",
         "No - there are no letters inside, only a picture. It needs OCR."],
        ["Hybrid", "Some pages of each kind", "Only from the typed pages"],
    ], widths=[2.2, 3.6, 2.7])
    b += E.p("We have real examples of all three among the CSE documents we "
             "downloaded:")
    b += E.table([
        ["Document", "Pages", "Characters found", "Kind"],
        ["Extension of the final suspension date", "1", "3,267",
         "Text-based"],
        ["Employee share option schemes", "1", "896", "Text-based"],
        ["De-listing - Associated Motor Finance", "1", "**0**",
         "**Scanned**"],
        ["Revised format for disclosure ...", "4",
         "0, 127, 1,129, 274", "**Hybrid** - page 1 is a scan"],
    ], widths=[3.9, 0.9, 2.1, 2.0])
    b += E.image(
        M.IMG / "scan_full_page.png", 7.5,
        "The de-listing notice. It looks like an ordinary document, but it "
        "is a photograph of paper - there is not a single letter of text "
        "inside the file.")
    b += E.idea(
        "a text-based PDF is a typed letter - you can copy any word out of "
        "it. A scanned PDF is a photo of that letter - you can see the "
        "words, but to the computer it is just coloured dots.")

    b += E.h3("Why getting text out is harder than it sounds")
    b += E.p("The Week 7 lecture listed the problems:")
    b += E.bullets([
        "**Tables** can run over several pages and have merged cells.",
        "**Paragraphs** - a line break might mean a new paragraph, or just "
        "the edge of the page.",
        "**Headers and footers** repeat on every page, and you may not want "
        "them.",
        "**Formatting** such as bold, italics and joined letters can come "
        "out wrong.",
        "**Scanned pages** have no text at all.",
    ])

    b += E.h3("PyPDF2 and pdfplumber")
    b += E.table([
        ["", "PyPDF2", "pdfplumber"],
        ["Good at", "Simple text, and the file's details (pages, author)",
         "Text that keeps its layout, and tables"],
        ["Layout", "Often merges lines and loses structure",
         "Uses the position of each letter to keep structure"],
        ["Tables", "Cannot find them", "Can find and extract them"],
        ["We use it for", "The file details", "The main text, and tables"],
    ], widths=[1.8, 3.3, 3.4])
    b += E.remember(
        "we use both because they are good at different things: pdfplumber "
        "for the text and tables, PyPDF2 for the file details. And no "
        "library at all can read a scanned page - that is OCR's job.")
    return b


#=========================================================================#
#  READING PYTHON                                                         #
#=========================================================================#

def python_chapter():
    examples = {
        "comment": (
            "# If we cannot read the rules we do not guess - we stop.",
            "From `can_fetch()`. Python skips this line - it explains to a "
            "reader why the next line returns False."),
        "variable": (
            "since_last = time.time() - self.last_request_time",
            "From `wait()`. `time.time()` is the current time in seconds. "
            "Take away the time of the last request, and the answer - how "
            "many seconds have passed - goes into a box called "
            "`since_last`."),
        "text": (
            'self.log.add(f"SKIPPED {url} - {reason}")',
            "From `fetch()`. If `url` holds `https://www.cse.lk/cgi-bin/x` "
            "and `reason` holds `not allowed by robots.txt`, the message "
            "becomes `SKIPPED https://www.cse.lk/cgi-bin/x - not allowed by "
            "robots.txt`."),
        "numbers": (
            'return True, "allowed"',
            "From `can_fetch()`. The function hands back two things at once: "
            "`True` (yes, we may) and a short reason. The code that asked "
            "catches both: `allowed, reason = self.can_fetch(url)`."),
        "list": (
            "paths = []\n"
            "for line in self.robots_text.splitlines():\n"
            "    ...\n"
            "    paths.append(value)",
            "From `blocked_paths()`. Start with an empty list, then add each "
            "blocked folder found in robots.txt. For CSE the finished list "
            "is `['/cgi-bin/']`."),
        "dict": (
            'return {"ok": True, "data": result, "from_file": False,\n'
            '        "error": None}',
            "From `fetch()`. Every request hands back a dictionary with the "
            "same four labels, so the code that asked can check "
            "`reply[\"ok\"]` first and then read `reply[\"data\"]`."),
        "function": (
            "def page_type(text):\n"
            "    length = len(text.strip())\n"
            "    if length < config.OCR_TEXT_THRESHOLD:\n"
            "        return \"Scanned image\", f\"Only {length} characters - needs OCR\"\n"
            "    return \"Text based\", f\"{length:,} characters read from the page\"",
            "From `pdf_extractor.py`. The ingredient is the text from one "
            "page. `len()` counts its characters, and the function returns "
            "what kind of page it is."),
        "if": (
            "if since_last < self.delay:\n"
            "    time.sleep(self.delay - since_last)",
            "From `wait()`. Only if less than 1.5 seconds have passed do we "
            "sleep - and only for the time that is left."),
        "for": (
            "for number, page in enumerate(reader.pages, start=1):\n"
            "    text = page.extract_text() or \"\"",
            "From `read_with_pypdf2()`. Go through the pages one at a time. "
            "`enumerate` numbers them 1, 2, 3 so we can report 'page 2'."),
        "import": (
            "import requests\n"
            "from urllib.robotparser import RobotFileParser\n"
            "from bs4 import BeautifulSoup\n"
            "import pdfplumber\n"
            "from PyPDF2 import PdfReader",
            "Your three files use these toolboxes: requests to send "
            "requests, RobotFileParser to understand robots.txt, "
            "BeautifulSoup to read HTML, and pdfplumber and PyPDF2 to read "
            "PDFs."),
        "try": (
            "try:\n"
            "    response = requests.get(config.ROBOTS_URL, ...)\n"
            "    ...\n"
            "except Exception as e:\n"
            "    self.robots = None",
            "From `read_robots()`. If the internet is down and robots.txt "
            "cannot be read, the program does not crash - it notes that it "
            "has no rules, and from then on refuses every request."),
        "with": (
            "with pdfplumber.open(str(pdf_path)) as pdf:\n"
            "    for number, page in enumerate(pdf.pages, start=1):\n"
            "        text = page.extract_text() or \"\"",
            "From `read_with_pdfplumber()`. The PDF is opened for the "
            "indented lines only, and closed automatically at the end - so "
            "no file is left open on the computer."),
        "class": (
            "class Scraper:\n\n"
            "    def __init__(self, delay=config.DELAY):\n"
            "        self.delay = delay\n"
            "        self.log = ScraperLog()\n"
            "        self.last_request_time = 0",
            "From `ethics.py`. `Scraper` is the design. When the app writes "
            "`Scraper()`, one scraper object is made, and `__init__` gives it "
            "its own delay, its own log, and a note of when it last sent a "
            "request. Your file has two classes: `ScraperLog` and "
            "`Scraper`."),
        "pandas": (
            "return pd.DataFrame(rows)",
            "From `scrape_sitemap()` and `check_all_pdfs()`. `rows` is a "
            "list of dictionaries, one per sitemap page or per PDF, and "
            "this line turns it into a table the app can display."),
    }

    extras = [
        ("Two tricks worth knowing",
         "**`or` as a fallback.** `x or y` gives `x`, unless `x` is empty or "
         "`None`, in which case it gives `y`. We use it where a library "
         "might hand back `None`:",
         'text = page.extract_text() or ""',
         "If `extract_text()` returns `None` - which it does for an empty "
         "page - `text` becomes an empty string instead, so later lines "
         "such as `len(text)` do not crash."),
        ("@staticmethod",
         "A line starting with `@` just above a function changes how it "
         "behaves. `@staticmethod` means the method does not need `self` - "
         "it does not use anything belonging to one particular scraper:",
         "@staticmethod\n"
         "def save_copy(name, data):\n"
         "    path = config.CACHE_DIR / f\"{name}.json\"",
         "Saving a copy of a reply works the same for every scraper, so it "
         "does not need to know which one called it."),
    ]
    return M.python_chapter(MEMBER, examples, "src/ethics.py", extras)


#=========================================================================#
#  FILE 1 - src/ethics.py                                                 #
#=========================================================================#

def file_ethics():
    b = []
    b += E.h1("Your file: src/ethics.py")
    b += E.big(
        "Every request our project sends to the internet goes through this "
        "file. It is where the ethical rules live.")
    b += E.p(
        "Putting the rules in one place is the most important design "
        "decision in the project. If each file sent its own requests, each "
        "one would have to remember to check robots.txt, to wait, and to "
        "log. Forget it once, in one file, and the project breaks its own "
        "rules. With one door, there is nothing to forget.")
    b += E.idea(
        "a building where every visitor must go through the one front desk. "
        "The desk checks the visitor list, makes you wait your turn, signs "
        "you in, and writes you in the book. There is no side door to "
        "forget to lock.")

    b += E.h2("The toolboxes at the top")
    b += E.code(
        "import csv\n"
        "import json\n"
        "import time\n"
        "from datetime import datetime\n"
        "from urllib.robotparser import RobotFileParser\n\n"
        "import requests\n\n"
        "import config")
    b += E.table([
        ["Import", "Used for"],
        ["`csv`", "Writing the request log as a CSV file"],
        ["`json`", "Saving and loading copies of the replies"],
        ["`time`", "Measuring time, and sleeping for the delay"],
        ["`datetime`", "Writing the date and time on each log line"],
        ["`RobotFileParser`", "Understanding robots.txt - it comes with "
                              "Python"],
        ["`requests`", "Actually sending the requests"],
        ["`config`", "Our own settings file: the delay, the User-Agent, "
                     "the addresses"],
    ], widths=[2.6, 5.9])

    #--- ScraperLog -----------------------------------------------------#
    b += E.h2("Part 1 - ScraperLog, the record book")
    b += E.p("This class keeps two records: the messages shown in the app, "
             "and a permanent CSV file with one line per request.")
    b += E.code(
        "class ScraperLog:\n\n"
        "    def __init__(self):\n"
        "        self.messages = []\n"
        "        self.request_count = 0\n\n"
        "    def add(self, message):\n"
        "        stamp = datetime.now().strftime(\"%H:%M:%S\")\n"
        "        self.messages.append(f\"{stamp}  {message}\")\n"
        "        return self.text()")
    b += E.p(
        "`add()` puts the time in front of every message, so the app shows "
        "lines like `17:47:55  Read robots.txt from the website`. "
        "`strftime(\"%H:%M:%S\")` turns the time into hours:minutes:seconds.")
    b += E.code(
        "    def log_request(self, method, url, status, allowed):\n"
        "        self.request_count += 1\n"
        "        new_file = not config.REQUEST_LOG.exists()\n\n"
        "        with open(config.REQUEST_LOG, \"a\", newline=\"\",\n"
        "                  encoding=\"utf-8\") as f:\n"
        "            writer = csv.writer(f)\n"
        "            if new_file:\n"
        "                writer.writerow([\"time\", \"method\", \"url\",\n"
        "                                 \"status\", \"robots_allowed\",\n"
        "                                 \"delay_seconds\"])\n"
        "            writer.writerow([ ...the values... ])")
    b += E.p("Line by line:")
    b += E.bullets([
        "`self.request_count += 1` - add one to the count. `+=` means 'add "
        "to what is already there'.",
        "`new_file = not config.REQUEST_LOG.exists()` - is this the first "
        "time? If the file does not exist yet, we will need a heading row.",
        "`open(..., \"a\")` - the `\"a\"` means **append**: add to the end "
        "of the file instead of wiping it. That is why the log keeps growing "
        "across every run of the project.",
        "The heading row is written only once, then one row per request.",
    ])
    b += E.p("This is what the log looks like - these are real rows:")
    b += E.code(
        "time,method,url,status,robots_allowed,delay_seconds\n"
        "2026-09-26 17:47:17,GET,https://www.cse.lk/sitemap.xml,200,True,1.5\n"
        "2026-09-26 17:47:31,GET,https://www.cse.lk/equity/trade-summary,200,True,1.5")
    b += E.remember(
        "the request log is our evidence. If anybody asks whether we "
        "overloaded CSE's server, we open this file and show them every "
        "request, when it was sent, and that we waited 1.5 seconds before "
        "each one.")

    #--- Scraper.__init__ -----------------------------------------------#
    b += E.h2("Part 2 - Setting up a Scraper")
    b += E.code(
        "class Scraper:\n\n"
        "    def __init__(self, delay=config.DELAY):\n"
        "        self.delay = delay\n"
        "        self.log = ScraperLog()\n"
        "        self.last_request_time = 0\n\n"
        "        self.session = requests.Session()\n"
        "        self.session.headers.update(\n"
        "            {\"User-Agent\": config.USER_AGENT})\n\n"
        "        self.robots_text = \"\"\n"
        "        self.robots = None\n"
        "        self.read_robots()")
    b += E.bullets([
        "`delay=config.DELAY` - the delay is 1.5 seconds unless somebody "
        "asks for a different one.",
        "`self.last_request_time = 0` - no request has been sent yet.",
        "`requests.Session()` - a **session** keeps the connection to the "
        "server open between requests, instead of opening a fresh one every "
        "time. That is a little less work for CSE's server.",
        "`headers.update({\"User-Agent\": ...})` - write our name on every "
        "request this session sends, once, here.",
        "`self.read_robots()` - read robots.txt straight away, before any "
        "other request can be made.",
    ])
    b += E.p("The User-Agent it sends, from `config.py`:")
    b += E.code(
        "CSE-Academic-Scraper/1.0 (University of Colombo; DA 2009 group\n"
        "project; contact: nuhanmalee@gmail.com)")
    b += E.p(
        "Many scraping tutorials tell you to copy a browser's User-Agent so "
        "the website cannot tell you apart from a person. We do the "
        "opposite. The point of the header is to say who is asking, not to "
        "hide it.")

    #--- read_robots ----------------------------------------------------#
    b += E.h2("Part 3 - Reading robots.txt")
    b += E.code(
        "def read_robots(self):\n"
        "    try:\n"
        "        response = requests.get(\n"
        "            config.ROBOTS_URL,\n"
        "            headers={\"User-Agent\": config.USER_AGENT},\n"
        "            timeout=config.TIMEOUT,\n"
        "        )\n"
        "        self.robots_text = response.text\n\n"
        "        self.robots = RobotFileParser()\n"
        "        self.robots.parse(self.robots_text.splitlines())\n\n"
        "        self.log.add(\"Read robots.txt from the website\")\n\n"
        "    except Exception as e:\n"
        "        self.robots = None\n"
        "        self.log.add(f\"Could not read robots.txt: {e}\")")
    b += E.bullets([
        "`requests.get(config.ROBOTS_URL, ...)` - download "
        "`https://www.cse.lk/robots.txt`. `timeout=30` means give up after "
        "30 seconds rather than waiting forever.",
        "`response.text` - the reply as text: the four lines we saw earlier.",
        "`RobotFileParser()` then `.parse(...)` - hand those lines to "
        "Python's own robots.txt reader. We did not write the rule-matching "
        "ourselves; the standard library already knows the format.",
        "`.splitlines()` - split the text into a list of separate lines, "
        "which is what the parser wants.",
    ])
    b += E.p(
        "This is the one request in the project that does **not** go "
        "through `fetch()` - and it cannot, because `fetch()` checks "
        "robots.txt first, and we cannot check robots.txt before we have "
        "read it.")
    b += E.p(
        "The `except` part is the careful bit. If robots.txt cannot be read, "
        "we set `self.robots = None`. From then on every permission check "
        "answers no. When we cannot see the rules, we do not guess in our "
        "own favour.")

    #--- can_fetch ------------------------------------------------------#
    b += E.h2("Part 4 - Asking permission")
    b += E.code(
        "def can_fetch(self, url):\n"
        "    if self.robots is None:\n"
        "        # If we cannot read the rules we do not guess - we stop.\n"
        "        return False, \"robots.txt could not be read\"\n\n"
        "    if self.robots.can_fetch(config.USER_AGENT, url):\n"
        "        return True, \"allowed\"\n"
        "    return False, \"not allowed by robots.txt\"")
    b += E.p(
        "Give it an address, and it answers yes or no, with a reason. "
        "`self.robots.can_fetch(...)` is the standard library doing the "
        "real work: it compares our User-Agent and the address with the "
        "rules it read.")
    b += E.p(
        "`blocked_paths()` just below it reads the Disallow lines so the app "
        "can show them:")
    b += E.code(
        "def blocked_paths(self):\n"
        "    paths = []\n"
        "    for line in self.robots_text.splitlines():\n"
        "        line = line.strip()\n"
        "        if line.lower().startswith(\"disallow:\"):\n"
        "            value = line.split(\":\", 1)[1].strip()\n"
        "            if value:\n"
        "                paths.append(value)\n"
        "    return paths")
    b += E.bullets([
        "`.strip()` removes spaces at both ends of the line.",
        "`.lower().startswith(\"disallow:\")` - does this line start with "
        "'disallow:', ignoring capital letters?",
        "`.split(\":\", 1)[1]` - cut the line at the first colon and take "
        "the part after it. `Disallow: /cgi-bin/` becomes `/cgi-bin/`.",
        "`if value:` - skip the empty `Disallow:` line, which blocks "
        "nothing.",
    ])

    #--- wait -----------------------------------------------------------#
    b += E.h2("Part 5 - Waiting politely")
    b += E.code(
        "def wait(self):\n"
        "    since_last = time.time() - self.last_request_time\n"
        "    if since_last < self.delay:\n"
        "        time.sleep(self.delay - since_last)\n"
        "    self.last_request_time = time.time()")
    b += E.p(
        "It does not blindly sleep 1.5 seconds every time. It measures how "
        "long it has been since the last request, and sleeps only for what "
        "is left. A worked example:")
    b += E.table([
        ["Time since last request", "Is it less than 1.5?", "Sleeps for"],
        ["0.2 seconds", "Yes", "1.3 seconds"],
        ["1.0 seconds", "Yes", "0.5 seconds"],
        ["4.0 seconds", "No", "0 seconds - go straight away"],
    ], widths=[3.2, 2.5, 2.8])
    b += E.p(
        "Either way the server gets at least 1.5 seconds between our "
        "requests, and we never waste time waiting longer than we promised.")
    b += E.idea(
        "not ringing a doorbell again and again. You ring, you wait a "
        "moment, and if you have already been waiting on the step for a "
        "while, you do not need to wait any longer.")
    b += E.p("`set_delay()` lets the delay be changed, but only within safe "
             "limits:")
    b += E.code(
        "def set_delay(self, seconds):\n"
        "    self.delay = max(config.MIN_DELAY,\n"
        "                     min(float(seconds), config.MAX_DELAY))")
    b += E.p(
        "`min(x, 10)` means 'no more than 10', and `max(0.5, ...)` means "
        "'no less than 0.5'. Ask for 0.1 and you get 0.5. Ask for 50 and you "
        "get 10. Nobody can switch the politeness off.")

    #--- save / load copy -----------------------------------------------#
    b += E.h2("Part 6 - Keeping a copy of every reply")
    b += E.code(
        "@staticmethod\n"
        "def save_copy(name, data):\n"
        "    path = config.CACHE_DIR / f\"{name}.json\"\n"
        "    with open(path, \"w\", encoding=\"utf-8\") as f:\n"
        "        json.dump(data, f)")
    b += E.p(
        "Each reply is saved as a file in `data/cache/`, named after the "
        "address it came from - for example `data/cache/tradeSummary.json`. "
        "`load_copy()` reads it back. The `/` between the folder and the "
        "file name joins them into one path.")
    b += E.p(
        "Why keep copies? The Week 6 lecture says 'avoid over-requesting - "
        "don't repeatedly fetch unchanged content'. And if the internet "
        "fails during a demonstration, the app can show the saved copy "
        "instead of an error.")

    #--- fetch ----------------------------------------------------------#
    b += E.h2("Part 7 - fetch(), the one door")
    b += E.p("Everything above leads to this function. Read it in four "
             "steps:")
    b += E.code(
        "def fetch(self, url, method=\"GET\", data=None, save_as=None,\n"
        "          want=\"json\"):\n\n"
        "    #--- Step 1: are we allowed? ---\n"
        "    allowed, reason = self.can_fetch(url)\n"
        "    if not allowed:\n"
        "        self.log.add(f\"SKIPPED {url} - {reason}\")\n"
        "        self.log.log_request(method, url, \"skipped\", allowed)\n"
        "        return {\"ok\": False, \"data\": None, \"from_file\": False,\n"
        "                \"error\": \"robots.txt says we should not ...\"}\n\n"
        "    #--- Step 2: wait ---\n"
        "    self.wait()\n\n"
        "    #--- Step 3: send it ---\n"
        "    try:\n"
        "        if method == \"POST\":\n"
        "            response = self.session.post(url, data=data,\n"
        "                                         timeout=config.TIMEOUT)\n"
        "        else:\n"
        "            response = self.session.get(url, timeout=config.TIMEOUT)\n\n"
        "        #--- Step 4: record it ---\n"
        "        self.log.log_request(method, url, response.status_code,\n"
        "                             allowed)")
    b += E.table([
        ["Step", "What happens", "Why"],
        ["1. Permission", "Ask robots.txt. If the answer is no, stop and "
                          "record that we skipped it.",
         "It is the first line - no request can get past it"],
        ["2. Wait", "Sleep until 1.5 seconds have passed", "Politeness"],
        ["3. Send", "GET or POST, through the session with our User-Agent",
         "Some CSE addresses only answer POST"],
        ["4. Record", "Write a row in the request log", "Evidence"],
    ], widths=[1.8, 3.8, 2.9])
    b += E.p("Then it looks at the reply:")
    b += E.code(
        "        if response.status_code != 200:\n"
        "            return {\"ok\": False, ...,\n"
        "                    \"error\": f\"The server replied with \"\n"
        "                             f\"{response.status_code}.\"}\n\n"
        "        if want == \"bytes\":\n"
        "            return {\"ok\": True, \"data\": response.content, ...}\n\n"
        "        if want == \"text\":\n"
        "            return {\"ok\": True, \"data\": response.text, ...}\n\n"
        "        result = response.json()\n"
        "        if save_as:\n"
        "            self.save_copy(save_as, result)\n"
        "        return {\"ok\": True, \"data\": result, ...}")
    b += E.p(
        "`!=` means 'is not equal to'. Anything other than 200 is treated as "
        "a failure and reported, not retried again and again. Then `want` "
        "decides what shape the reply is handed back in:")
    b += E.table([
        ["want", "Gives back", "Used by"],
        ["`\"json\"` (the default)", "Python lists and dictionaries, made "
                                     "from the JSON reply",
         "`api_client.py` - the market data"],
        ["`\"text\"`", "The reply as a string", "`static_scraper.py` - web "
                                                "pages and the sitemap"],
        ["`\"bytes\"`", "The raw contents of a file", "`crawler.py` - PDF "
                                                     "downloads"],
    ], widths=[2.2, 3.4, 2.9])
    b += E.p("And if anything goes wrong at all:")
    b += E.code(
        "    except Exception as e:\n"
        "        self.log.add(f\"Request failed: {e}\")\n"
        "        if save_as:\n"
        "            saved = self.load_copy(save_as)\n"
        "            if saved is not None:\n"
        "                return {\"ok\": True, \"data\": saved,\n"
        "                        \"from_file\": True, \"error\": None}\n"
        "        return {\"ok\": False, \"data\": None, \"from_file\": False,\n"
        "                \"error\": str(e)}")
    b += E.p(
        "If the internet is down, use the saved copy if there is one, and "
        "say so with `from_file: True`. Otherwise report the error. The "
        "program never crashes - which matters because it runs behind a web "
        "page, and a crash would close the whole app.")
    b += E.remember(
        "fetch() does four things in a fixed order - check robots.txt, "
        "wait, send, record - and the check comes first. Because it is the "
        "only function that sends requests, no request can skip the rules.")
    b += E.careful(
        "there is one honest exception. `src/selenium_scraper.py` drives a "
        "real web browser, and the browser makes its own requests that "
        "never pass through `fetch()`. We give it the same User-Agent and "
        "use it on one page only, but if asked 'does every request go "
        "through fetch()?', the true answer is 'every request except "
        "Selenium's browser'. Saying so shows you understand the design.")

    #--- ETHICAL_RULES --------------------------------------------------#
    b += E.h2("Part 8 - The rules shown in the app")
    b += E.p(
        "At the bottom of the file is `ETHICAL_RULES`, a list of pairs: a "
        "rule and what we do about it. The Ethics tab shows it as a table. "
        "Each pair is written `(\"name\", \"explanation\")` - round brackets "
        "hold a fixed pair of values, called a **tuple**.")
    b += E.code(
        "ETHICAL_RULES = [\n"
        "    (\"Check robots.txt\",\n"
        "     \"We read the robots.txt file and check every address ...\"),\n"
        "    (\"Wait between requests\", ...),\n"
        "    (\"Say who we are\", ...),\n"
        "    ...\n"
        "]")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.ethics")
    b += E.code(
        "robots.txt from CSE\n"
        "-------------------------------------------------------\n"
        "User-agent: *\n"
        "Disallow:\n"
        "Disallow: /cgi-bin/\n"
        "Sitemap: https://www.cse.lk/sitemap.xml\n\n"
        "Paths the website asks us not to visit: ['/cgi-bin/']\n\n"
        "Permission checks\n"
        "-------------------------------------------------------\n"
        "  yes  https://www.cse.lk/api/aspiData   (allowed)\n"
        "  yes  https://www.cse.lk/equity/trade-summary   (allowed)\n"
        "  yes  https://www.cse.lk/cgi-bin/test   (allowed)\n\n"
        "A real request\n"
        "-------------------------------------------------------\n"
        "ok  : True\n"
        "data: {'id': 37116752, 'value': 21037.35, ...}")
    b += E.p(
        "The third permission line is the /cgi-bin/ puzzle from the ideas "
        "chapter. The last part is a real request for the market index "
        "(ASPI), sent through `fetch()`.")
    return b


#=========================================================================#
#  FILE 2 - src/static_scraper.py                                         #
#=========================================================================#

def file_static():
    b = []
    b += E.h1("Your file: src/static_scraper.py")
    b += E.big(
        "The ordinary way of scraping - download the page, read it with "
        "BeautifulSoup - and why it finds almost nothing on the CSE site.")
    b += E.p(
        "This file does not collect the project's data. It is here because "
        "of what it shows. Without it, a reader would reasonably ask why we "
        "did not just use BeautifulSoup like everybody else. This file "
        "answers that in one run.")

    b += E.h2("Part 1 - scrape_page()")
    b += E.code(
        "def scrape_page(url=None, scraper=None):\n"
        "    scraper = scraper or Scraper()\n"
        "    url = url or config.PAGES[\"trade_summary\"]\n\n"
        "    reply = scraper.fetch(url, want=\"text\")\n\n"
        "    if not reply[\"ok\"]:\n"
        "        return {\"url\": url, \"status\": None,\n"
        "                \"error\": reply[\"error\"], ...}\n\n"
        "    html = reply[\"data\"]\n"
        "    status = 200")
    b += E.bullets([
        "`scraper or Scraper()` - use the scraper we were given, or make a "
        "new one if none was given.",
        "`url or config.PAGES[\"trade_summary\"]` - if no address was given, "
        "use the CSE trade summary page.",
        "`scraper.fetch(url, want=\"text\")` - the request goes through your "
        "own `fetch()`, so robots.txt is checked, the delay applied and the "
        "request logged. `want=\"text\"` gives us the HTML as one string.",
        "`status = 200` - `fetch()` only says ok when the server replied "
        "200, so we know the status.",
    ])
    b += E.p("Then BeautifulSoup reads it:")
    b += E.code(
        "    soup = BeautifulSoup(html, \"html.parser\")\n\n"
        "    title = soup.title.get_text(strip=True) if soup.title \\\n"
        "            else \"no title\"\n"
        "    words = soup.get_text(strip=True)\n"
        "    tables = soup.find_all(\"table\")\n"
        "    links = soup.find_all(\"a\")")
    b += E.bullets([
        "`BeautifulSoup(html, \"html.parser\")` - build the tree. "
        "`html.parser` is the parser that comes with Python, so nothing "
        "extra is needed.",
        "`soup.title.get_text(strip=True)` - the words inside the "
        "`<title>` tag, with spaces trimmed.",
        "`soup.get_text(strip=True)` - every word on the whole page.",
        "`soup.find_all(\"table\")` - every table. `len()` of that list is "
        "how many there are.",
    ])
    b += E.p("The result on the CSE trade summary page:")
    b += E.code(
        "  Address    : https://www.cse.lk/equity/trade-summary\n"
        "  Status     : 200\n"
        "  HTML size  : 17,898 bytes\n"
        "  Words found: 24 characters\n"
        "  Tables     : 0")
    b += E.p(
        "The request worked perfectly - status 200 - and nearly 18,000 "
        "bytes of HTML came back. (The CSE home page gives about 25,000.) "
        "Yet BeautifulSoup finds only 24 characters of words and not one "
        "table. The prices are simply not in the file.")
    b += E.idea(
        "you asked for a newspaper and got the paper with all the pages "
        "blank - the printing happens later, inside the reader's browser. "
        "requests brings you the blank paper. BeautifulSoup reads it "
        "perfectly well; there is just nothing printed on it yet.")

    b += E.h2("Part 2 - scrape_sitemap(), the proof")
    b += E.p(
        "The obvious question is: are you sure BeautifulSoup was not the "
        "problem? This function answers it. It uses the same library on "
        "CSE's sitemap, which is an ordinary file with no JavaScript.")
    b += E.code(
        "def scrape_sitemap(scraper=None):\n"
        "    scraper = scraper or Scraper()\n\n"
        "    reply = scraper.fetch(f\"{config.BASE_URL}/sitemap.xml\",\n"
        "                          want=\"text\")\n"
        "    if not reply[\"ok\"]:\n"
        "        return pd.DataFrame()\n\n"
        "    try:\n"
        "        soup = BeautifulSoup(reply[\"data\"], \"xml\")\n"
        "    except Exception:\n"
        "        soup = BeautifulSoup(reply[\"data\"], \"html.parser\")\n\n"
        "    rows = []\n"
        "    for entry in soup.find_all(\"url\"):\n"
        "        location = entry.find(\"loc\")\n"
        "        updated = entry.find(\"changefreq\")\n"
        "        rows.append({\n"
        "            \"Page\": location.get_text(strip=True) if location else None,\n"
        "            \"Updated\": updated.get_text(strip=True) if updated else None,\n"
        "        })\n"
        "    return pd.DataFrame(rows)")
    b += E.p(
        "A sitemap is written in **XML**, which looks like HTML but with "
        "tags the website makes up itself. Each page in the list looks like "
        "this:")
    b += E.code(
        "<url>\n"
        "  <loc>https://www.cse.lk/market-summary/</loc>\n"
        "  <changefreq>daily</changefreq>\n"
        "</url>")
    b += E.bullets([
        "`BeautifulSoup(..., \"xml\")` - read it as XML. That needs the lxml "
        "library, so if lxml is missing, `except` falls back to the normal "
        "parser instead of crashing.",
        "`soup.find_all(\"url\")` - every `<url>` block.",
        "`entry.find(\"loc\")` - inside each one, the `<loc>` tag holding "
        "the address.",
        "`... if location else None` - if a block has no `<loc>`, write "
        "`None` instead of crashing.",
    ])
    b += E.p("Result: **15 pages read without any trouble.** Same library, "
             "same methods, a perfect result - so the earlier problem was "
             "the page, not the tool.")

    b += E.h2("Part 3 - beautifulsoup_methods()")
    b += E.p(
        "This last function runs each Week 4 method on the real CSE page and "
        "shows what it gave back. It is useful for revising, and for "
        "answering 'show me you know BeautifulSoup':")
    b += E.table([
        ["Method", "Code we ran", "What it gave back"],
        ["`find()`", "`soup.find('title')`",
         "`<title>Trade Summary - CSE 2025</title>`"],
        ["`find_all()`", "`len(soup.find_all('a'))`", "0 - no links at all"],
        ["`get_text()`", "`soup.get_text(strip=True)[:40]`",
         "`Trade Summary - CSE 2025`"],
        ["`get()`", "`soup.find('a').get('href')`", "no links to read"],
        ["`select()`", "`len(soup.select('meta'))`", "3"],
        ["`select_one()`", "`soup.select_one('meta[name=viewport]')`",
         "the viewport meta tag"],
    ], widths=[1.8, 3.6, 3.1])
    b += E.p(
        "Notice that nearly all the 24 characters of text are just the page "
        "title. That is everything a plain download can see.")
    b += E.tryit("run it yourself:", "python -m src.static_scraper")
    b += E.remember(
        "requests downloaded the page correctly and BeautifulSoup read it "
        "correctly. The page itself had almost nothing in it, because CSE "
        "builds its content with JavaScript afterwards. That finding is why "
        "the rest of the project reads the data addresses instead.")
    return b


#=========================================================================#
#  FILE 3 - src/pdf_extractor.py                                          #
#=========================================================================#

def file_pdf():
    b = []
    b += E.h1("Your file: src/pdf_extractor.py")
    b += E.big(
        "Opens the announcement PDFs, pulls the text out, and works out "
        "which ones are scans that need OCR instead.")

    b += E.h2("Part 1 - Is this page real text, or a scan?")
    b += E.code(
        "def page_type(text):\n"
        "    length = len(text.strip())\n\n"
        "    if length < config.OCR_TEXT_THRESHOLD:\n"
        "        return \"Scanned image\", f\"Only {length} characters - needs OCR\"\n"
        "    return \"Text based\", f\"{length:,} characters read from the page\"")
    b += E.p(
        "Count the characters on a page. Fewer than 50, and we call it a "
        "scan. `{length:,}` writes the number with a comma, so 3267 appears "
        "as 3,267.")
    b += E.p(
        "Why 50 and not 0? A real page of a CSE circular gives hundreds or "
        "thousands of characters, and a scan gives none - so almost any "
        "number would work. But a scan sometimes carries a few stray "
        "characters that are not the real text - a label stamped on "
        "afterwards, for instance. Demanding at least 50 means a few stray "
        "letters cannot fool us into skipping OCR.")

    b += E.h2("Part 2 - Reading with PyPDF2")
    b += E.code(
        "def read_with_pypdf2(pdf_path):\n"
        "    reader = PdfReader(str(pdf_path))\n\n"
        "    pages = []\n"
        "    for number, page in enumerate(reader.pages, start=1):\n"
        "        text = page.extract_text() or \"\"\n"
        "        kind, note = page_type(text)\n"
        "        pages.append({\"Page\": number,\n"
        "                      \"Characters\": len(text.strip()),\n"
        "                      \"Type\": kind, \"Note\": note, \"text\": text})\n\n"
        "    details = reader.metadata or {}\n"
        "    info = {\n"
        "        \"Pages\": len(reader.pages),\n"
        "        \"Title\": details.get(\"/Title\", \"not set\"),\n"
        "        \"Author\": details.get(\"/Author\", \"not set\"),\n"
        "        \"Created with\": details.get(\"/Producer\", \"not set\"),\n"
        "    }\n"
        "    return pages, info")
    b += E.bullets([
        "`PdfReader(...)` - open the PDF. `reader.pages` is the list of its "
        "pages.",
        "`page.extract_text() or \"\"` - the text on this page. For an "
        "empty page PyPDF2 gives back `None`, and the `or \"\"` turns that "
        "into an empty string so nothing below crashes.",
        "`reader.metadata` - the **metadata**: facts stored inside the file "
        "about the file, such as who wrote it and what program made it.",
        "`details.get(\"/Author\", \"not set\")` - the author, or 'not set' "
        "if the file does not say.",
    ])
    b += E.p("Real metadata from one CSE circular:")
    b += E.code(
        "  Pages          1\n"
        "  Title          not set\n"
        "  Author         Nirmalee Ganegoda\n"
        "  Created with   Microsoft Word for Microsoft 365")
    b += E.p(
        "'Created with Microsoft Word' is a second clue that this is a "
        "typed, text-based PDF and not a scan.")

    b += E.h2("Part 3 - Reading with pdfplumber")
    b += E.code(
        "def read_with_pdfplumber(pdf_path):\n"
        "    pages = []\n"
        "    tables = []\n\n"
        "    with pdfplumber.open(str(pdf_path)) as pdf:\n"
        "        for number, page in enumerate(pdf.pages, start=1):\n"
        "            text = page.extract_text() or \"\"\n"
        "            kind, note = page_type(text)\n"
        "            pages.append({...})\n\n"
        "            for table in (page.extract_tables() or []):\n"
        "                if len(table) > 1:\n"
        "                    heading = [(cell if cell else f\"Column {i + 1}\")\n"
        "                               for i, cell in enumerate(table[0])]\n"
        "                    tables.append(pd.DataFrame(table[1:],\n"
        "                                               columns=heading))\n\n"
        "    return pages, tables")
    b += E.bullets([
        "`with pdfplumber.open(...) as pdf:` - open the PDF, and close it "
        "automatically afterwards.",
        "`page.extract_tables()` - pdfplumber looks at where the text sits "
        "and finds tables. Each table comes back as a list of rows, and "
        "each row as a list of cells.",
        "`if len(table) > 1:` - a table needs a heading row and at least one "
        "row of data.",
        "`table[0]` is the heading row, and `table[1:]` is every row after "
        "it. `[1:]` means 'from position 1 to the end'.",
        "An empty heading cell becomes 'Column 1', 'Column 2' and so on, so "
        "every column has a name.",
    ])
    b += E.p(
        "The line that builds `heading` is a **list comprehension** - a "
        "short way to build a list in one line. It reads: 'for each cell in "
        "the first row, use the cell, or Column n if it is empty'.")

    b += E.h2("Part 4 - read_pdf() puts it together")
    b += E.code(
        "def read_pdf(pdf_path):\n"
        "    ...\n"
        "    try:\n"
        "        pages, tables = read_with_pdfplumber(pdf_path)\n"
        "        _, info = read_with_pypdf2(pdf_path)\n"
        "    except Exception as e:\n"
        "        return {\"ok\": False, \"file\": name, \"error\": str(e), ...}\n\n"
        "    scanned = [p[\"Page\"] for p in pages\n"
        "               if p[\"Type\"] == \"Scanned image\"]")
    b += E.bullets([
        "pdfplumber gives the pages and tables. PyPDF2 gives the file "
        "details. `_, info = ...` means 'I only want the second thing it "
        "returns' - the `_` is a name for something we ignore.",
        "`scanned` is the list of page numbers that need OCR. For the "
        "de-listing notice it is `[1]`. For the hybrid document it is also "
        "`[1]` - its first page is a scan, and the other three are typed.",
    ])
    b += E.p(
        "The OCR tab uses exactly that list, so for a hybrid PDF it reads "
        "the page that is actually scanned, not just page 1.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.pdf_extractor")
    b += E.code(
        "File                                     Pages Characters  Type          Needs OCR\n"
        "14336_EXTENSION OF THE FINAL SUSPENSION     1     3267     Text based    No\n"
        "14358_EMPLOYEE SHARE OPTION SCHEMES         1      896     Text based    No\n"
        "14364_DE-LISTING OF THE ORDINARY VOTING     1        0     Scanned image Yes\n"
        "14396_THE REVISED FORMAT FOR DISCLOSURE     4     1530     Scanned image Yes")
    b += E.p(
        "Look at the row with 0 characters: that file is about 190 KB and "
        "full of writing when you open it, but there is no text inside it. "
        "The 14396 row shows 1,530 characters and still needs OCR - that is "
        "the hybrid one, with a scanned first page.")
    b += E.remember(
        "PyPDF2 and pdfplumber can only read letters that are really in the "
        "file. A scanned page is a picture, so they get nothing - and that "
        "is when OCR takes over.")
    return b


#=========================================================================#
#  VIVA                                                                   #
#=========================================================================#

def viva():
    return M.viva_chapter(
        MEMBER,
        tab_steps=[
            "Open the **Ethics** tab. Your name is on the label at the top.",
            "Press **Read robots.txt**. Point to the file on the left and the "
            "settings on the right - the one blocked section, the 1.5 second "
            "delay, and our User-Agent.",
            "Press **Show the request log**. Show that every request is "
            "recorded with the time and the delay.",
            "Open the **Announcements** tab and scroll to **Read the text out "
            "of a document**. Choose a typed document and press **Read the "
            "text** - show the page table and the file details.",
            "Choose the de-listing document and read it again - show that it "
            "gives no text and says to use OCR.",
        ],
        commands=(
            "python -m src.ethics             # robots.txt, a real request\n"
            "python -m src.static_scraper     # 24 characters, then the sitemap\n"
            "python -m src.pdf_extractor      # which PDFs need OCR"),
        script=(
            "My part is the rules, and reading the documents. Every request "
            "our project makes goes through one function I wrote, fetch(). "
            "Before anything is sent, it checks CSE's robots.txt, waits one "
            "and a half seconds, and says who we are in the User-Agent, and "
            "afterwards it writes the request to a log. I also wrote our "
            "first scraping attempt with requests and BeautifulSoup - it "
            "found only 24 characters, because the CSE page is built by "
            "JavaScript, and that is why we read the data addresses instead. "
            "Finally, I read the text out of the announcement PDFs with "
            "pdfplumber and PyPDF2, and spot the scanned ones that need OCR."),
        pointers=[
            ["`allowed, reason = self.can_fetch(url)` at the top of "
             "`fetch()`", "This is the permission check. It is the first "
                          "line, so no request can skip it."],
            ["`wait()`", "It measures the time since the last request and "
                         "sleeps only for what is left of the 1.5 seconds."],
            ["`self.robots = None` in `read_robots()`",
             "If robots.txt cannot be read, every request is refused. We do "
             "not guess in our own favour."],
            ["The `/cgi-bin/ ... (allowed)` output line",
             "Python's parser uses the first matching rule, and CSE's empty "
             "Disallow line comes first. We never request /cgi-bin/ anyway."],
            ["`want=\"text\"` in `scrape_page()`",
             "The page request goes through fetch() like every other, and "
             "comes back as text for BeautifulSoup."],
            ["`soup.get_text(strip=True)`", "Every word on the page, with "
                                            "spaces trimmed - only 24 "
                                            "characters on CSE."],
            ["`page.extract_text() or \"\"`", "extract_text gives None on an "
                                              "empty page; this turns it "
                                              "into an empty string."],
            ["`config.OCR_TEXT_THRESHOLD` (50)",
             "Under 50 characters means a scan. Not 0, because scans can "
             "carry a few stray characters."],
        ])


#=========================================================================#
#  THE WHOLE DOCUMENT                                                     #
#=========================================================================#

WORDS = [
    ("Attribute", "Extra information inside an HTML tag, like href in a link."),
    ("BeautifulSoup", "A Python library that reads HTML and lets you find "
                      "parts of it."),
    ("CAPTCHA", "A test a website uses to check a visitor is a person."),
    ("Crawl-delay", "A robots.txt line asking programs to wait between "
                    "requests. CSE does not have one."),
    ("Disallow", "A robots.txt line naming a part of the site programs "
                 "should not visit."),
    ("Hybrid PDF", "A PDF with some typed pages and some scanned pages."),
    ("Metadata", "Facts stored inside a file about the file itself, such as "
                 "its author."),
    ("OCR", "Optical Character Recognition - reading letters from a picture."),
    ("Parser", "The part of a library that reads text and works out its "
               "structure."),
    ("pdfplumber", "A PDF library that keeps the layout and can find tables."),
    ("PyPDF2", "A simpler PDF library that also reads the file details."),
    ("Rate limiting", "Limiting how many requests are sent in a given time."),
    ("RobotFileParser", "The part of Python that reads robots.txt and answers "
                        "'may I fetch this?'"),
    ("Scanned PDF", "A PDF that holds a photograph of a page, with no real "
                    "text inside."),
    ("Session", "A connection to a server kept open for several requests."),
    ("Sitemap", "A file where a website lists its own pages for programs."),
    ("Text-based PDF", "A PDF made by a computer, with real letters inside."),
    ("Tuple", "A fixed group of values in round brackets, like (name, "
              "explanation)."),
    ("XML", "A text format like HTML, where the website chooses its own tag "
            "names."),
]


def build():
    b = []
    b += M.cover(MEMBER, "Ethical scraping and robots.txt, BeautifulSoup, "
                         "and reading PDFs")
    b += E.contents()
    b += M.how_to_use(MEMBER, FILES)
    b += E.page_break()
    b += M.the_project(MEMBER)
    b += E.page_break()
    b += M.web_basics()
    b += E.page_break()
    b += ideas()
    b += E.page_break()
    b += python_chapter()
    b += E.page_break()
    b += file_ethics()
    b += E.page_break()
    b += file_static()
    b += E.page_break()
    b += file_pdf()
    b += E.page_break()
    b += M.big_picture(
        MEMBER, FILES,
        ["Your part sits at the front and the middle of the project. At the "
         "front, `ethics.py` is step 3 - every request made by anybody's "
         "code goes through it. In the middle, `pdf_extractor.py` is step 6 "
         "- it reads the documents Sasini's crawler downloads, and tells "
         "Salaama's OCR which pages need reading as pictures."])
    b += E.page_break()
    b += viva()
    b += E.page_break()
    b += M.practice_questions(MEMBER)
    b += E.page_break()
    b += M.word_list(WORDS)
    return b
