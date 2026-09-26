"""
Document for 25ada073 - Sasini.

Crawling for documents (src/crawler.py and the Scrapy spider) and cleaning
the data (src/cleaner.py).
"""

from guide_content import member_common as M
from guide_content import pdf_engine as E

MEMBER = "25ada073"
FILES = ["src/crawler.py", "src/cleaner.py",
         "scrapy_project/cse_crawler/spiders/cse_announcements.py",
         "scrapy_project/cse_crawler/settings.py"]


#=========================================================================#
#  THE IDEAS BEHIND YOUR PART                                             #
#=========================================================================#

def ideas():
    b = []
    b += E.h1("The ideas behind your part")
    b += E.p(
        "Your part has two halves. The first is **crawling** - finding "
        "documents by following links, and downloading them politely. The "
        "second is **cleaning** - tidying the data once it has arrived, "
        "because data taken from a website is never ready to use straight "
        "away.")

    #--- Crawling -------------------------------------------------------#
    b += E.h2("Scraping and crawling are different jobs")
    b += E.p(
        "**Scraping** means taking data out of a page you already know "
        "about. **Crawling** means finding pages by following links from one "
        "to the next. The Week 6 lecture compared them:")
    b += E.table([
        ["", "Web scraping", "Web crawling"],
        ["Purpose", "Take specific data out of pages", "Browse and discover "
                                                       "pages"],
        ["Scope", "Particular pages you choose", "Many pages, found by "
                                                 "following links"],
        ["Output", "Tidy data - CSV, JSON", "A list of the pages or files "
                                            "found"],
        ["Focus", "Getting the data out and cleaning it",
         "Finding links and moving between pages"],
    ], widths=[1.7, 3.3, 3.5])
    b += E.p(
        "Both use a program to visit pages, both read what comes back, and "
        "both gather web data. Most of our project is scraping: Pasindu's "
        "code knows the exact address of the share prices and goes straight "
        "there. **Your part is the crawling.** We do not know in advance "
        "which documents CSE has published, so your code reads the list, "
        "works out where each document lives, and follows each link.")
    b += E.idea(
        "scraping is going to a shop you know and buying one thing. "
        "Crawling is walking through a market, reading every signpost, and "
        "following each one to see what is there.")

    b += E.h3("Why crawlers are called spiders")
    b += E.p(
        "The lecture explained the nickname: a crawler starts from a few "
        "known addresses and follows links outwards, building a network of "
        "pages it has found - like a spider moving across its web. Scrapy, "
        "the framework you used, calls its crawlers **spiders** for the same "
        "reason.")

    #--- Addresses and files --------------------------------------------#
    b += E.h2("Finding where each document lives")
    b += E.p(
        "Pasindu's code asks CSE for the list of circulars - official "
        "notices, each with a PDF attached. Each record in the list looks "
        "like this (shortened):")
    b += E.code(
        '{\n'
        '  "id": 14364,\n'
        '  "fileText": "DE-LISTING OF THE ORDINARY VOTING SHARES OF ...",\n'
        '  "uploadedDate": "06 Aug 2026 09:21:30 AM",\n'
        '  "path": "upload_report_file/hHXxBdUT5ylLsSvz_6Aug2026...pdf"\n'
        '}')
    b += E.p(
        "The `path` is only **part** of an address. On its own it goes "
        "nowhere. It is like being told 'flat 4' without the street name. "
        "We needed the rest.")
    b += E.p(
        "The PDFs are not kept on the website itself. Big files are often "
        "stored on a separate server built just for delivering files, called "
        "a **CDN** (Content Delivery Network). We tried the likely "
        "addresses until one gave back a real PDF:")
    b += E.table([
        ["Address we tried", "What came back"],
        ["`https://www.cse.lk/cmt/` + path", "404 - no such page"],
        ["`https://cdn.cse.lk/` + path", "403 - not allowed"],
        ["`https://cdn.cse.lk/cmt/` + path", "**200 - a real PDF**"],
    ], widths=[4.8, 3.7])
    b += E.p("So every document's full address is "
             "`https://cdn.cse.lk/cmt/` followed by its path.")

    b += E.h3("How do you know a file is really a PDF?")
    b += E.p(
        "Every file is really just a long row of **bytes** - small numbers "
        "from 0 to 255. Many file types start with a few fixed bytes that "
        "announce what they are, a bit like a label on the front of a box. "
        "Every PDF begins with the four characters `%PDF`.")
    b += E.p(
        "So before saving anything, your crawler looks at the first four "
        "bytes. If a server sent back an error page instead of a document, "
        "it would start with something like `<htm` - and we would not save "
        "it as a PDF.")
    b += E.idea(
        "checking the stamp on an envelope before opening it. If it does "
        "not say 'PDF', whatever is inside is not what you asked for.")

    b += E.h3("Crawling politely")
    b += E.p("A crawler can do a lot of damage quickly, because following "
             "links can go on forever. Yours has five limits:")
    b += E.numbered([
        "**A download limit** - only the first few documents, not every one "
        "on the site. The lecture: 'only scrape the data you need'.",
        "**No duplicates** - the same document can appear twice in the "
        "list; it is only downloaded once.",
        "**Skip what we already have** - if a PDF is already saved, it is "
        "not downloaded again.",
        "**One at a time, with a pause** - every download goes through "
        "Nuhan's `fetch()`, so it waits 1.5 seconds and follows robots.txt.",
        "**Stay on CSE** - the Scrapy spider is told it may only visit "
        "cse.lk addresses.",
    ])

    #--- Scrapy ---------------------------------------------------------#
    b += E.h2("Scrapy, the crawling framework")
    b += E.p(
        "**Scrapy** is a Python framework built specially for crawling. A "
        "**framework** is bigger than a library: instead of you calling its "
        "tools, it runs the show and calls **your** code at the right "
        "moments. The lecture described it as fast, open source, and widely "
        "used in industry.")
    b += E.p("How Scrapy works, from the Week 6 lecture:")
    b += E.numbered([
        "**Start a project** - `scrapy startproject name` creates the "
        "folders.",
        "**Write a spider** - a class that says where to start and what to "
        "do with each page.",
        "**The engine sends the requests** - Scrapy queues them up and sends "
        "them, following its settings.",
        "**parse() takes the data out** - Scrapy hands each reply to your "
        "code.",
        "**Store the results** - to a JSON or CSV file.",
        "**Run it** - `scrapy crawl spider_name`.",
    ])
    b += E.idea(
        "Scrapy is like a delivery company. You tell it where to start and "
        "what to do with each parcel. It handles the vans, the timetable, "
        "the queue and the paperwork - you only write the part that opens "
        "the parcels.")
    b += E.table([
        ["Scrapy word", "Meaning"],
        ["Spider", "Your class - where to start, and what to do with each "
                   "reply"],
        ["Request", "One page or file to fetch"],
        ["Callback", "The function Scrapy calls when that reply arrives"],
        ["yield", "Hand something back to Scrapy - a new request to follow, "
                  "or a finished item"],
        ["Item", "One finished record, with named fields"],
        ["Settings", "The rules - delays, robots.txt, how many at once"],
    ], widths=[2.2, 6.3])

    #--- Cleaning -------------------------------------------------------#
    b += E.h2("Why data needs cleaning")
    b += E.p(
        "The Week 1 lecture listed a common mistake: 'data collected "
        "through scraping is ready for analysis'. It is not. Data arrives in "
        "whatever shape the website sent it. Before anyone can sort it, "
        "total it or chart it, it has to be tidied.")
    b += E.p("A computer stores each value as a particular **type**, and the "
             "type decides what you can do with it:")
    b += E.table([
        ["Type", "Example", "What you can do"],
        ["Number", "`141.0`", "Add, average, sort by size"],
        ["Text", "`\"141.0\"`", "Search it, join it - but not add it up"],
        ["Date", "`2026-09-25 14:39`", "Sort by time, find the day or month"],
        ["Missing", "`None` / `NaN`", "Nothing - it marks a gap"],
    ], widths=[1.6, 2.9, 4.0])
    b += E.p("We found four problems in the CSE data:")
    b += E.table([
        ["Problem", "Example", "Why it matters"],
        ["Dates as huge numbers", "`1790326797431`",
         "pandas thinks it is an ordinary number - you could even average "
         "it"],
        ["Numbers stored as text", "`\"141.0\"`",
         "Text sorts by its first character, so '9' comes after '100'"],
        ["Completely empty columns", "a column of nothing but gaps",
         "Clutters every table and every saved file"],
        ["Extra spaces", "`\"  SAMPATH BANK \"`",
         "Looks the same as 'SAMPATH BANK' to a person, but not to a "
         "computer"],
    ], widths=[2.4, 2.6, 3.5])
    b += E.idea(
        "cleaning data is like tidying a kitchen before cooking: putting "
        "things in the right cupboards, labelling the jars, throwing out "
        "empty boxes. Nothing new is added - it just becomes usable.")

    b += E.h2("Cleaning and checking are different jobs")
    b += E.p(
        "**Cleaning** fixes the shape of the data - the types, the empty "
        "columns, the repeated rows. **Checking** asks whether the values "
        "make sense.")
    b += E.p(
        "A share price of minus five rupees would be perfectly tidy - a "
        "number, in the right column - and completely wrong. Cleaning would "
        "never notice. Only a check that says 'prices cannot be negative' "
        "would.")
    b += E.remember(
        "crawling finds and downloads the documents politely; cleaning makes "
        "the data usable; checking makes sure it is believable. Your part "
        "does all three.")
    return b


#=========================================================================#
#  READING PYTHON                                                         #
#=========================================================================#

def python_chapter():
    examples = {
        "comment": (
            "# Every PDF file starts with the characters %PDF. If ours does\n"
            "# not, we received something else and should not save it.",
            "From `download_documents()`. It explains why the next line "
            "checks the first four bytes. Python skips both lines."),
        "variable": (
            "wanted = documents.head(limit)",
            "From `download_documents()`. `documents.head(5)` is the first "
            "five rows of the table of documents. They go into a box called "
            "`wanted` - the ones we will actually download."),
        "text": (
            "filename = f\"{row.get('id', number)}_{title[:60]}\"",
            "From `download_documents()`. It builds a file name from the "
            "document's id number and the first 60 characters of its title, "
            "such as `14364_DE-LISTING OF THE ORDINARY VOTING SHARES OF "
            "ASSOCIATED MOTOR`. `title[:60]` means 'the first 60 "
            "characters' - explained properly below."),
        "numbers": (
            "DOWNLOAD_DELAY = 1.5\n"
            "CONCURRENT_REQUESTS = 1\n"
            "CLOSESPIDER_ITEMCOUNT = 40",
            "From the spider's `settings.py`: wait 1.5 seconds, send only one "
            "request at a time, and stop after 40 items."),
        "list": (
            "found = []\n"
            "for _, row in circulars.iterrows():\n"
            "    found.append({ ... })",
            "From `find_documents()`. Start with an empty list and add one "
            "entry for each circular. `iterrows()` goes through a table one "
            "row at a time."),
        "dict": (
            "found.append({\n"
            "    \"Title\": str(row.get(\"fileText\", \"Untitled\")).strip(),\n"
            "    \"Date\": row.get(\"uploadedDate\", \"\"),\n"
            "    \"url\": row.get(\"pdf_url\"),\n"
            "    \"id\": row.get(\"id\"),\n"
            "})",
            "Each document becomes a small dictionary with four labels. "
            "`row.get(\"fileText\", \"Untitled\")` means 'the title, or the "
            "word Untitled if there is none'."),
        "function": (
            "def download_documents(documents, limit=5, scraper=None,\n"
            "                       progress=None):",
            "The ingredients are the table of documents, how many to "
            "download, a scraper and a progress bar. `limit=5` is a "
            "**default**: if nobody says how many, it downloads 5. "
            "`scraper=None` means 'none given - make one yourself'."),
        "if": (
            "if not content[:4] == b\"%PDF\":\n"
            "    results.append({\"Title\": title[:65],\n"
            "                    \"Result\": \"Not a PDF file\", \"File\": \"-\"})\n"
            "    continue",
            "If the first four bytes are not `%PDF`, note it in the results "
            "and move on to the next document without saving anything."),
        "for": (
            "for column in tidy.columns:",
            "From `clean()`. Go through the table's columns one by one - "
            "`symbol`, `name`, `price`, and so on - checking each to see if "
            "it holds dates stored as numbers."),
        "import": (
            "import scrapy\n"
            "import pandas as pd\n"
            "from src.api_client import CSEApi\n"
            "from src.ethics import Scraper",
            "Your files use Scrapy for the spider, pandas for the tables, "
            "Pasindu's `CSEApi` to get the list of circulars, and Nuhan's "
            "`Scraper` to download politely. The last two are our own files "
            "- you can import code from inside the project the same way."),
        "try": (
            "try:\n"
            "    reply = json.loads(response.text)\n"
            "except json.JSONDecodeError:\n"
            "    self.logger.warning(f\"{response.url} did not return JSON\")\n"
            "    return",
            "From the spider's `parse()`. `json.loads` turns JSON text into "
            "Python lists and dictionaries. If the reply is not valid JSON, "
            "the spider notes a warning and stops handling that reply, "
            "instead of crashing the whole crawl."),
        "class": (
            "class CseAnnouncementsSpider(scrapy.Spider):\n\n"
            "    name = \"cse_announcements\"\n"
            "    allowed_domains = [\"cse.lk\", \"cdn.cse.lk\", \"www.cse.lk\"]",
            "The name in brackets, `scrapy.Spider`, means your class is "
            "**built on top of** Scrapy's own spider. It gets everything "
            "Scrapy's spider can already do, and you only add what is "
            "special about yours. This is called **inheritance**. `name` is "
            "what you type after `scrapy crawl`."),
        "pandas": (
            "df = df.drop_duplicates(subset=[\"url\"]).reset_index(drop=True)",
            "From `find_documents()`. Remove rows with the same address, so "
            "no document is downloaded twice. `reset_index(drop=True)` "
            "renumbers the rows 0, 1, 2 afterwards, so there are no gaps "
            "where the repeats were."),
    }

    extras = [
        ("Slicing - taking part of a list or text",
         "Square brackets with a colon take a piece of something. The "
         "number before the colon is where to start (blank means the "
         "beginning), and the number after is where to stop:",
         "title[:60]      # the first 60 characters\n"
         "content[:4]     # the first 4 bytes\n"
         "table[1:]       # everything except the first item",
         "Counting starts from 0, and the stop position itself is not "
         "included, so `[:4]` gives positions 0, 1, 2 and 3 - four things."),
        ("Bytes",
         "Text written with a `b` in front, like `b\"%PDF\"`, is **bytes** "
         "- raw file contents - rather than ordinary text. A downloaded PDF "
         "arrives as bytes, so we compare it with bytes.",
         None, None),
        ("continue - skip to the next one",
         "Inside a loop, `continue` means 'stop here for this item and go "
         "straight on to the next'. Your crawler uses it to skip a document "
         "that is already saved, failed, or is not a PDF.",
         None, None),
        ("any() - is at least one true?",
         "`any(...)` answers True if at least one thing is true. In "
         "`clean()` it asks: does this column's name contain 'date', 'time' "
         "or 'created'?",
         "if not any(word in column.lower()\n"
         "           for word in (\"date\", \"time\", \"created\")):\n"
         "    continue",
         "`column.lower()` makes the name small letters first, so "
         "`lastTradedTime` still matches 'time'."),
        ("lambda - a tiny one-line function",
         "`lambda` makes a small function without a name, written in one "
         "line. It is handy when you need a function only once:",
         "tidy[column].apply(\n"
         "    lambda value: value.strip() if isinstance(value, str) else value)",
         "Read it as: 'for each value: if it is text, trim the spaces off; "
         "otherwise leave it exactly as it is'."),
        ("yield - handing things back one at a time",
         "`return` gives back one answer and the function ends. `yield` "
         "gives back one thing and **keeps going**, ready to give back "
         "another. Scrapy spiders use `yield` to hand Scrapy each new "
         "request or finished item as soon as it is ready.",
         None, None),
        ("async def",
         "`async def` marks a function that can pause and let other work "
         "happen while it waits, such as waiting for a reply from a server. "
         "Newer versions of Scrapy need the first function to be written "
         "this way. You do not need to understand it deeply - just know that "
         "Scrapy requires it.",
         None, None),
    ]
    return M.python_chapter(MEMBER, examples, "src/crawler.py", extras)


#=========================================================================#
#  FILE 1 - src/crawler.py                                                #
#=========================================================================#

def file_crawler():
    b = []
    b += E.h1("Your file: src/crawler.py")
    b += E.big(
        "Finds the PDF documents CSE has published, and downloads them one "
        "at a time. This is the crawler the app uses.")
    b += E.p("It works in two steps: first find the documents, then fetch "
             "them. Keeping the steps apart means we can see the whole list "
             "before downloading anything.")

    b += E.h2("Step 1 - find_documents()")
    b += E.code(
        "def find_documents(api=None):\n"
        "    api = api or CSEApi()\n"
        "    found = []\n\n"
        "    circulars = api.circulars()\n"
        "    for _, row in circulars.iterrows():\n"
        "        found.append({\n"
        "            \"Title\": str(row.get(\"fileText\", \"Untitled\")).strip(),\n"
        "            \"Date\": row.get(\"uploadedDate\", \"\"),\n"
        "            \"url\": row.get(\"pdf_url\"),\n"
        "            \"id\": row.get(\"id\"),\n"
        "        })\n\n"
        "    df = pd.DataFrame(found)\n\n"
        "    if not df.empty:\n"
        "        df = df.drop_duplicates(subset=[\"url\"]).reset_index(drop=True)\n\n"
        "    api.scraper.log.add(f\"Found {len(df)} documents to download\")\n"
        "    return df")
    b += E.numbered([
        "`api.circulars()` - Pasindu's method asks CSE for the list of "
        "circulars. It has already joined each `path` onto "
        "`https://cdn.cse.lk/cmt/`, so each row has a full `pdf_url`.",
        "The loop takes the four things we need from each row: the title, "
        "the date, the address and the id number.",
        "`pd.DataFrame(found)` - turn the list into a table.",
        "`drop_duplicates(subset=[\"url\"])` - if the same address appears "
        "twice, keep only one. Downloading a document twice would waste "
        "CSE's bandwidth for no benefit.",
    ])
    b += E.p(
        "`for _, row in ...` - `iterrows()` gives back two things for each "
        "row: its row number and the row itself. We do not need the number, "
        "so we name it `_`, which is the usual Python way of saying 'I am "
        "ignoring this'.")
    b += E.remember(
        "nothing is downloaded in step 1. It only builds the list of what "
        "exists and where it lives - the link discovery that makes this "
        "crawling.")

    b += E.h2("Step 2 - download_documents()")
    b += E.code(
        "wanted = documents.head(limit)\n"
        "results = []\n\n"
        "for number, (_, row) in enumerate(wanted.iterrows(), start=1):\n"
        "    ...\n"
        "    title = row[\"Title\"]\n"
        "    filename = f\"{row.get('id', number)}_{title[:60]}\"\n\n"
        "    # Skip anything we already have.\n"
        "    existing = list(config.PDF_DIR.glob(f\"{row.get('id', '')}_*.pdf\"))\n"
        "    if existing and str(row.get(\"id\", \"\")):\n"
        "        results.append({... \"Result\": \"Already saved\" ...})\n"
        "        continue\n\n"
        "    reply = scraper.fetch(row[\"url\"], want=\"bytes\")\n"
        "    if not reply[\"ok\"]:\n"
        "        results.append({... \"Result\": f\"Failed: {reply['error']}\" ...})\n"
        "        continue\n\n"
        "    content = reply[\"data\"]\n"
        "    if not content[:4] == b\"%PDF\":\n"
        "        results.append({... \"Result\": \"Not a PDF file\" ...})\n"
        "        continue\n\n"
        "    path = save_pdf(content, filename)\n"
        "    results.append({... \"Result\": \"Downloaded\" ...})")
    b += E.p("For each wanted document, four checks happen in order:")
    b += E.table([
        ["Check", "The code", "If it fails"],
        ["Do we already have it?", "`config.PDF_DIR.glob(\"14364_*.pdf\")` "
                                   "looks for a saved file starting with "
                                   "this id", "Skip it - 'Already saved'"],
        ["Did the download work?", "`scraper.fetch(url, want=\"bytes\")` - "
                                   "through Nuhan's fetch, so it waits and "
                                   "is logged", "Record the error and move "
                                                "on"],
        ["Is it really a PDF?", "`content[:4] == b\"%PDF\"`", "Do not save "
                                                              "it"],
        ["All good", "`save_pdf(content, filename)` - Salaama's function "
                     "writes the file", "-"],
    ], widths=[2.3, 4.0, 2.2])
    b += E.bullets([
        "`glob(\"14364_*.pdf\")` - the `*` means 'anything here'. It finds "
        "any file whose name starts with `14364_` and ends with `.pdf`.",
        "`want=\"bytes\"` - ask `fetch()` for the raw file contents, not "
        "text or JSON.",
        "Each check ends with `continue`, so a problem with one document "
        "never stops the others.",
    ])
    b += E.p(
        "`crawl()` at the bottom of the file simply runs step 1 and then "
        "step 2.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.crawler")
    b += E.p("This is a real run (titles shortened to fit the page):")
    b += E.code(
        "Step 2 - downloading them\n"
        "Title                                   Result         File\n"
        "DFCC BANK PLC (\"BANK\") - BASEL III ...  Already saved  14475_DFCC BANK PLC ...pdf\n"
        "PAN ASIA BANKING CORPORATION PLC ...    Already saved  14471_PAN ASIA BANKING ...pdf\n"
        "PEOPLE'S LEASING & FINANCE PLC ...      Already saved  14465_PEOPLES LEASING ...pdf\n"
        "AITKEN SPENCE HOTEL HOLDINGS PLC ...    Already saved  14457_AITKEN SPENCE ...pdf\n"
        "DFCC BANK PLC (\"BANK\") - ISSUANCE ...   Already saved  14436_DFCC BANK PLC ...pdf\n\n"
        "18:23:46  Read robots.txt from the website\n"
        "18:23:47  POST https://www.cse.lk/api/circularAnnouncement - status 200\n"
        "18:23:47  Got 5 circulars with PDFs\n"
        "18:23:47  Found 5 documents to download")
    b += E.p(
        "Every row says 'Already saved' because these five had been "
        "downloaded on an earlier run. The whole run sent CSE just **one** "
        "request - the list itself - and downloaded nothing twice. The "
        "first time a new circular appears, its row says 'Downloaded' "
        "instead, and the log shows a `GET` line for it at least a second "
        "and a half after the one before.")
    return b


#=========================================================================#
#  FILE 2 - the Scrapy spider                                             #
#=========================================================================#

def file_scrapy():
    b = []
    b += E.h1("Your files: the Scrapy spider")
    b += E.big(
        "The same crawling job done a second way, with the Scrapy framework "
        "the lecture taught.")
    b += E.p(
        "`src/crawler.py` is what the app uses. The spider shows the "
        "framework approach used in industry. It runs as a separate program, "
        "because Scrapy's engine cannot be started twice inside one running "
        "program such as our app.")

    b += E.h2("The folders")
    b += E.code(
        "scrapy_project/\n"
        "    scrapy.cfg                      tells Scrapy where the settings are\n"
        "    cse_crawler/\n"
        "        settings.py                 the rules\n"
        "        items.py                    the shape of one record\n"
        "        spiders/\n"
        "            cse_announcements.py    the spider itself")
    b += E.p(
        "This is the same layout that `scrapy startproject` creates, and the "
        "same as the `quotes_crawler` example in the course repository.")

    b += E.h2("The spider, step by step")
    b += E.p("The spider has three functions. Scrapy calls them in this "
             "order:")
    b += E.code(
        "   start()            ask CSE for the list of circulars\n"
        "      |\n"
        "   parse()            read the list, work out each PDF address,\n"
        "      |               and FOLLOW it   <-- the crawling step\n"
        "      |\n"
        "   parse_document()   record what was found at the other end")

    b += E.h3("start() - the first requests")
    b += E.code(
        "SOURCES = [\n"
        "    (\"https://www.cse.lk/api/circularAnnouncement\",\n"
        "     \"reqCircularAnnouncement\", \"Circular\"),\n"
        "    (\"https://www.cse.lk/api/approvedAnnouncement\",\n"
        "     \"approvedAnnouncements\", \"Announcement\"),\n"
        "]\n\n"
        "async def start(self):\n"
        "    for url, record_name, label in self.SOURCES:\n"
        "        yield scrapy.Request(\n"
        "            url=url,\n"
        "            method=\"POST\",\n"
        "            callback=self.parse,\n"
        "            cb_kwargs={\"record_name\": record_name, \"label\": label},\n"
        "            dont_filter=True,\n"
        "        )")
    b += E.bullets([
        "Most spiders just list their start addresses in `start_urls`, and "
        "Scrapy sends ordinary GET requests. We build the requests ourselves "
        "because these CSE addresses only answer **POST**.",
        "`callback=self.parse` - 'when this reply arrives, give it to "
        "`parse()`'.",
        "`cb_kwargs` - extra information passed along to `parse()`, so it "
        "knows which list the reply came from.",
        "`yield` - hand each request to Scrapy, which queues it.",
    ])
    b += E.careful(
        "the course notes call this method `start_requests()`. That was "
        "Scrapy's name for years, but newer versions replaced it with "
        "`async def start()`, and in version 2.17 - the one we have - "
        "`start_requests()` has been removed. Our first version used the "
        "old name. The spider ran, collected 0 items and finished almost at "
        "once, because Scrapy never called our code - and nothing warned "
        "us. It is a real example of a scraper breaking because something "
        "underneath it changed.")

    b += E.h3("parse() - reading the list and following each link")
    b += E.code(
        "def parse(self, response, record_name, label):\n"
        "    try:\n"
        "        reply = json.loads(response.text)\n"
        "    except json.JSONDecodeError:\n"
        "        self.logger.warning(f\"{response.url} did not return JSON\")\n"
        "        return\n\n"
        "    records = reply.get(record_name, []) \\\n"
        "              if isinstance(reply, dict) else []\n"
        "    self.logger.info(f\"{label}: found {len(records)} records\")\n\n"
        "    seen = set()\n\n"
        "    for record in records:\n"
        "        path = record.get(\"path\")\n"
        "        if not path or not str(path).lower().endswith(\".pdf\"):\n"
        "            continue\n\n"
        "        pdf_url = self.CDN_BASE + str(path)\n"
        "        if pdf_url in seen:\n"
        "            continue\n"
        "        seen.add(pdf_url)\n"
        "        ...\n\n"
        "        yield scrapy.Request(\n"
        "            url=pdf_url,\n"
        "            callback=self.parse_document,\n"
        "            cb_kwargs={...},\n"
        "            method=\"HEAD\",\n"
        "        )")
    b += E.bullets([
        "`json.loads(response.text)` - the reply is JSON, not HTML, so we "
        "read it with `json` instead of the CSS selectors the quotes spider "
        "used. The idea is the same: take the useful parts out of the reply.",
        "`endswith(\".pdf\")` - not every announcement has a document; skip "
        "those that do not.",
        "`seen = set()` - a **set** is like a list that never holds the same "
        "thing twice. It remembers which addresses we have already followed.",
        "`yield scrapy.Request(pdf_url, ...)` - **this is the crawling "
        "step**: we found a new address and we follow it.",
    ])
    b += E.p(
        "`method=\"HEAD\"` asks only for the **details** of the file - its "
        "type and size - without downloading the file itself. The spider "
        "only needs to confirm each document exists; downloading megabytes "
        "of PDF to find that out would be wasteful.")

    b += E.h3("parse_document() - recording the result")
    b += E.code(
        "def parse_document(self, response, title, label, uploaded):\n"
        "    raw_size = response.headers.get(\"Content-Length\", b\"\").decode()\n"
        "    if raw_size == \"0\":\n"
        "        raw_size = \"\"\n\n"
        "    item = DocumentItem()\n"
        "    item[\"title\"] = title\n"
        "    item[\"url\"] = response.url\n"
        "    item[\"source\"] = label\n"
        "    item[\"uploaded\"] = uploaded\n"
        "    item[\"content_type\"] = response.headers.get(\n"
        "        \"Content-Type\", b\"unknown\").decode()\n"
        "    item[\"size_kb\"] = (round(int(raw_size) / 1024, 1)\n"
        "                       if raw_size.isdigit() else None)\n"
        "    item[\"status\"] = response.status\n"
        "    yield item")
    b += E.p(
        "Each finished `item` is one record in the output file. Note the "
        "size. `Content-Length` is the header where a server says how big a "
        "file is, and CSE's server does not always fill it in properly - on "
        "our run, two of the five PDFs came back saying 0. A real PDF is "
        "never empty, so we record `None` instead. Zero would be a **wrong** "
        "measurement - it would say the file is empty. `None` honestly "
        "says 'we did not find out'.")
    b += E.careful(
        "our first version only handled a missing size, not a size of 0. "
        "The output file said two real documents were 0.0 KB, and it was "
        "only noticed by reading the output. Always look at what your "
        "scraper actually produced - not just whether it ran without "
        "errors.")

    b += E.h2("items.py - the shape of one record")
    b += E.code(
        "class DocumentItem(scrapy.Item):\n"
        "    title = scrapy.Field()\n"
        "    url = scrapy.Field()\n"
        "    source = scrapy.Field()\n"
        "    uploaded = scrapy.Field()\n"
        "    content_type = scrapy.Field()\n"
        "    size_kb = scrapy.Field()\n"
        "    status = scrapy.Field()")
    b += E.p(
        "Declaring the fields up front is a safety check. If somebody types "
        "`item[\"ttile\"]` by mistake, Scrapy raises an error at once instead "
        "of quietly creating a misspelled column in the output.")

    b += E.h2("settings.py - the polite rules")
    b += E.table([
        ["Setting", "Value", "What it means"],
        ["`ROBOTSTXT_OBEY`", "`True`", "Scrapy reads robots.txt itself and "
                                       "refuses blocked addresses. Many "
                                       "tutorials tell you to switch this "
                                       "off - we left it on."],
        ["`USER_AGENT`", "our honest name", "The same as the rest of the "
                                            "project"],
        ["`DOWNLOAD_DELAY`", "`1.5`", "Wait 1.5 seconds between requests"],
        ["`RANDOMIZE_DOWNLOAD_DELAY`", "`True`", "Vary the wait a little, so "
                                                 "requests do not arrive in "
                                                 "a machine-gun rhythm"],
        ["`CONCURRENT_REQUESTS`", "`1`", "One request at a time. Normally "
                                         "Scrapy sends up to 8 at once to "
                                         "the same website."],
        ["`AUTOTHROTTLE_ENABLED`", "`True`", "Slow down automatically if "
                                             "CSE's server starts replying "
                                             "slowly"],
        ["`CLOSESPIDER_ITEMCOUNT`", "`40`", "Stop after 40 items - enough to "
                                            "show it works"],
        ["`HTTPCACHE_ENABLED`", "`True`", "Remember replies for 15 minutes, "
                                          "so running it again soon after "
                                          "does not ask CSE again"],
    ], widths=[3.4, 1.7, 3.4])
    b += E.remember(
        "your own crawler gets its politeness from Nuhan's fetch(). The "
        "Scrapy spider gets the same politeness from its settings file - "
        "robots.txt obeyed, 1.5 seconds between requests, one at a time.")

    b += E.h2("Running the spider")
    b += E.tryit("from the project folder:",
                 "cd scrapy_project\n"
                 "scrapy crawl cse_announcements -O ../data/scrapy_output.json")
    b += E.p(
        "`crawl cse_announcements` runs the spider by its `name`. `-O` "
        "(a capital O) saves the items to a JSON file, replacing the old "
        "one. A small `-o` would **add** to the end of the old file instead, "
        "and two JSON lists stuck end to end is no longer valid JSON.")
    b += E.p("When it finishes, Scrapy prints a summary. These lines are "
             "from a real run:")
    b += E.code(
        "[cse_announcements] INFO: Circular: found 5 records\n"
        "[cse_announcements] INFO: Announcement: found 125 records\n"
        " 'downloader/request_count': 9,\n"
        " 'elapsed_time_seconds': 14.64,\n"
        " 'item_scraped_count': 5,\n"
        " 'robotstxt/request_count': 2,")
    b += E.bullets([
        "The circulars list had 5 records, each with a PDF. The announcements "
        "list had 125 records, but none had a PDF attached, so the spider "
        "skipped them all.",
        "9 requests in total: robots.txt from both servers (2), the two "
        "lists (2), and one HEAD request for each of the 5 PDFs (5).",
        "`robotstxt/request_count: 2` - Scrapy read robots.txt from "
        "`www.cse.lk` and `cdn.cse.lk` **before** crawling either of them.",
        "About 15 seconds for 9 requests - that is the delay and the "
        "one-at-a-time rule working.",
    ])
    b += E.p(
        "Run it again within 15 minutes and the summary says "
        "`'httpcache/hit': 9` - every reply came from the cache, and CSE "
        "received no requests at all.")
    return b


#=========================================================================#
#  FILE 3 - src/cleaner.py                                                #
#=========================================================================#

def file_cleaner():
    b = []
    b += E.h1("Your file: src/cleaner.py")
    b += E.big(
        "Tidies the table of share prices so it can be sorted, totalled and "
        "charted - and then checks that the values make sense.")

    b += E.h2("Part 1 - describe(): counting the problems")
    b += E.code(
        "def describe(df):\n"
        "    ...\n"
        "    return {\n"
        "        \"Rows\": len(df),\n"
        "        \"Columns\": len(df.columns),\n"
        "        \"Empty cells\": int(df.isna().sum().sum()),\n"
        "        \"Empty columns\": int(df.isna().all().sum()),\n"
        "        \"Duplicate rows\": int(df.duplicated().sum()),\n"
        "        \"Number columns\": int(df.select_dtypes(include=\"number\").shape[1]),\n"
        "        \"Date columns\": int(df.select_dtypes(include=\"datetime\").shape[1]),\n"
        "    }")
    b += E.p(
        "This counts problems in the table. It runs **before** and **after** "
        "cleaning, so the two can be shown side by side. Saying 'we cleaned "
        "the data' proves nothing; showing the counts change does.")
    b += E.bullets([
        "`df.isna()` marks every missing cell as True. `.sum().sum()` counts "
        "them - once down each column, then across.",
        "`df.isna().all()` - is a column missing in **every** row?",
        "`df.duplicated()` - is this row an exact copy of an earlier one?",
        "`select_dtypes(include=\"number\")` - just the number columns. "
        "`.shape[1]` is how many columns that is.",
    ])

    b += E.h2("Part 2 - clean(): six steps")
    b += E.code(
        "def clean(df):\n"
        "    ...\n"
        "    tidy = df.copy()\n"
        "    changes = []")
    b += E.p(
        "`df.copy()` first, always. The original table stays untouched, so "
        "if the cleaning ever turns out to be wrong, we can compare with "
        "the original - without downloading everything from CSE again. "
        "`changes` collects a sentence about each thing we did.")

    b += E.h3("Step 1 - turning big numbers back into dates")
    b += E.code(
        "for column in tidy.columns:\n"
        "    if not any(word in column.lower()\n"
        "               for word in (\"date\", \"time\", \"created\")):\n"
        "        continue\n"
        "    if not pd.api.types.is_numeric_dtype(tidy[column]):\n"
        "        continue\n\n"
        "    values = tidy[column].dropna()\n"
        "    if not values.empty and values.median() > 1_000_000_000_000:\n"
        "        tidy[column] = (pd.to_datetime(tidy[column], unit=\"ms\",\n"
        "                                       utc=True, errors=\"coerce\")\n"
        "                        .dt.tz_convert(\"Asia/Colombo\")\n"
        "                        .dt.tz_localize(None))\n"
        "        date_columns.append(column)")
    b += E.p("A column is converted only if it passes **three** tests:")
    b += E.numbered([
        "Its name contains 'date', 'time' or 'created'.",
        "It holds numbers.",
        "Its middle value (the **median**) is over one trillion "
        "(`1_000_000_000_000` - the underscores are only there to make it "
        "readable). Any recent date in milliseconds is about 1.8 trillion, "
        "but no price or quantity ever is.",
    ])
    b += E.p(
        "The three tests together mean we never turn a price into a date by "
        "accident, just because its column happens to have 'date' in the "
        "name. `unit=\"ms\"` tells pandas the numbers are milliseconds. "
        "`errors=\"coerce\"` means any value that cannot be converted "
        "becomes missing instead of stopping everything.")
    b += E.p("The last three lines deal with **time zones**:")
    b += E.bullets([
        "The milliseconds are counted in **UTC**, the world's standard "
        "time. `utc=True` tells pandas so.",
        "Sri Lanka is 5 hours 30 minutes ahead of UTC. "
        "`tz_convert(\"Asia/Colombo\")` moves every time into Colombo time.",
        "`tz_localize(None)` removes the time zone label afterwards, "
        "because Excel cannot save a date that carries one.",
    ])
    b += E.careful(
        "our first version left out the time zone. The table looked fine - "
        "real dates, real times - but every trade showed between 04:00 and "
        "09:00. The CSE only trades from 9.30 in the morning to 2.30 in the "
        "afternoon, so every time was 5 hours 30 minutes early. After the "
        "fix they run from 09:30 to 14:30. Nothing crashed and nothing "
        "warned us: it was found by asking whether the values made sense, "
        "which is exactly what cleaning and checking are for.")

    b += E.h3("Step 2 - turning text that is really numbers into numbers")
    b += E.code(
        "for column in tidy.select_dtypes(include=[\"object\", \"str\"]).columns:\n"
        "    sample = tidy[column].dropna().astype(str).head(50)\n"
        "    ...\n"
        "    converted = pd.to_numeric(sample.str.replace(\",\", \"\",\n"
        "                                                 regex=False),\n"
        "                              errors=\"coerce\")\n"
        "    if converted.notna().mean() > 0.9:\n"
        "        tidy[column] = pd.to_numeric(...)\n"
        "        number_columns.append(column)")
    b += E.bullets([
        "`select_dtypes(include=[\"object\", \"str\"])` - just the text "
        "columns. Newer pandas keeps text in its own `str` type and older "
        "pandas used `object`, so we ask for both.",
        "Take a sample of 50 values and try turning them into numbers. "
        "`.str.replace(\",\", \"\")` removes commas first, so '1,094.25' "
        "becomes '1094.25'.",
        "`converted.notna().mean()` is the share that converted - "
        "`.mean()` of True and False values gives the fraction that are "
        "True.",
        "If more than 90% convert, it was a number column dressed as text, "
        "and the whole column is converted. Not 100%, because a real number "
        "column can still have a few blanks or dashes.",
    ])

    b += E.h3("Step 3 - trimming extra spaces")
    b += E.code(
        "for column in tidy.select_dtypes(include=[\"object\", \"str\"]).columns:\n"
        "    tidy[column] = tidy[column].apply(\n"
        "        lambda value: value.strip() if isinstance(value, str) else value)")
    b += E.p(
        "`\"  SAMPATH BANK \"` and `\"SAMPATH BANK\"` look the same to a "
        "person but are different to a computer - grouping by name would "
        "give two groups. `.strip()` removes spaces from both ends.")
    b += E.p(
        "Only real text is trimmed. A missing value is left missing. That "
        "matters: an older way of writing this turned missing values into "
        "the text 'nan', which hides gaps and makes the table look more "
        "complete than it really is.")

    b += E.h3("Steps 4, 5 and 6")
    b += E.code(
        "# 4. Drop columns that are empty for every row\n"
        "empty = [c for c in tidy.columns if tidy[c].isna().all()]\n"
        "if empty:\n"
        "    tidy = tidy.drop(columns=empty)\n\n"
        "# 5. Remove repeated rows\n"
        "tidy = tidy.drop_duplicates().reset_index(drop=True)\n\n"
        "# 6. Put the useful columns first\n"
        "useful = [\"symbol\", \"name\", \"price\", \"change\",\n"
        "          \"percentageChange\", \"quantity\", \"turnover\"]\n"
        "front = [c for c in useful if c in tidy.columns]\n"
        "tidy = tidy[front + [c for c in tidy.columns if c not in front]]")
    b += E.bullets([
        "**Step 4** - a column that is empty for every company is only "
        "clutter.",
        "**Step 5** - repeated rows would count the same company twice.",
        "**Step 6** - purely for people: the table opens with the symbol, "
        "name and price, instead of internal id numbers.",
    ])

    b += E.h2("Part 3 - check(): do the values make sense?")
    b += E.code(
        "if \"price\" in df.columns:\n"
        "    negative = int((df[\"price\"] < 0).sum())\n"
        "    add(\"No negative prices\", negative == 0, ...)\n\n"
        "if \"percentageChange\" in df.columns:\n"
        "    extreme = int((df[\"percentageChange\"].abs() > 100).sum())\n"
        "    add(\"Price changes look sensible\", extreme == 0, ...)")
    b += E.p(
        "`df[\"price\"] < 0` marks every negative price as True, and "
        "`.sum()` counts them. `.abs()` means 'ignore the minus sign', so "
        "it catches moves of more than 100% up **or** down.")
    b += E.table([
        ["Check", "Why"],
        ["Rows collected", "Is there any data at all?"],
        ["No negative prices", "A share cannot cost less than nothing"],
        ["Price changes look sensible", "More than 100% in a day is "
                                        "suspicious"],
        ["Every row has a symbol", "Every company needs its code"],
        ["No company appears twice", "Each symbol should be there once"],
        ["How complete is the data", "What share of cells have a value"],
    ], widths=[3.5, 5.0])
    b += E.p(
        "A check that fails says **'Check this'** - it does not delete "
        "anything. A big price move can be real, after a share split for "
        "example. Automatically deleting rows that look odd is how real data "
        "gets quietly lost.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.cleaner")
    b += E.p("This is a real run:")
    b += E.code(
        "What we changed\n"
        "  - Turned 1 column(s) of large numbers back into dates: lastTradedTime\n"
        "  - Removed extra spaces from the text columns\n"
        "  - Moved the most useful columns to the front\n\n"
        "Before and after\n"
        "         Check  Before  After\n"
        "          Rows     284    284\n"
        "       Columns      23     23\n"
        "   Empty cells      14     14\n"
        " Empty columns       0      0\n"
        "Duplicate rows       0      0\n"
        "Number columns      19     18\n"
        "  Date columns       0      1\n\n"
        "Checks\n"
        "                      Check Result                       Detail\n"
        "             Rows collected     OK                     284 rows\n"
        "         No negative prices     OK All prices are zero or above\n"
        "Price changes look sensible     OK Nothing moved more than 100%\n"
        "     Every row has a symbol     OK            All rows have one\n"
        "   No company appears twice     OK    Each company appears once\n"
        "   How complete is the data     OK  99.8% of cells have a value")
    b += E.p(
        "Look at 'Number columns 19 -> 18' and 'Date columns 0 -> 1'. That "
        "is one column - `lastTradedTime` - moving from being counted as a "
        "number to being counted as a date. The two changes together are "
        "the fix showing up in the counts.")
    b += E.p(
        "Some steps changed nothing on this run - there were no empty "
        "columns and no repeated rows, and no text columns needed turning "
        "into numbers. That is fine. The steps are there for the days the "
        "data does arrive with those problems, and `describe()` proves "
        "whether they were needed. The number of companies changes from day "
        "to day - usually somewhere around 284 to 291.")
    b += E.remember(
        "cleaning fixes the shape - dates, number types, spaces, empty "
        "columns, repeats. Checking asks whether the values are believable. "
        "And the original is always kept, untouched.")
    return b


#=========================================================================#
#  VIVA                                                                   #
#=========================================================================#

def viva():
    return M.viva_chapter(
        MEMBER,
        tab_steps=[
            "Open the **Announcements** tab. Your name is on the label at "
            "the top.",
            "Press **Get the announcements** - the list of company notices.",
            "Under **Download the documents**, leave the number at 5 and "
            "press **Download**. Point to the two tables: the documents "
            "found, and what happened to each - 'Downloaded' or 'Already "
            "saved'.",
            "Open the **Data & Export** tab (after the market data has been "
            "collected on the Market Data tab). Press **Clean and check**. "
            "Point to the before-and-after table and the checks.",
        ],
        commands=(
            "python -m src.crawler            # find and download PDFs\n"
            "python -m src.cleaner            # before/after and checks\n"
            "cd scrapy_project\n"
            "scrapy crawl cse_announcements -O ../data/scrapy_output.json"),
        script=(
            "My part is crawling and cleaning. Scraping takes data from a "
            "page you know; crawling finds pages by following links. We did "
            "not know which documents CSE had published, so my crawler reads "
            "the list of circulars, builds each PDF's full address - they "
            "live on a separate server, cdn.cse.lk - and downloads them one "
            "at a time, skipping duplicates and checking each file really "
            "starts with percent-PDF. I did the same job again as a Scrapy "
            "spider, with robots.txt obeyed and a 1.5 second delay in its "
            "settings. Then I clean the share price table: dates that arrive "
            "as huge numbers become real dates, text that is really numbers "
            "becomes numbers, and I check the values make sense - for "
            "example, no negative prices."),
        pointers=[
            ["`drop_duplicates(subset=[\"url\"])`",
             "The same document can be listed twice; downloading it twice "
             "would waste CSE's bandwidth."],
            ["`content[:4] == b\"%PDF\"`", "Every PDF starts with %PDF. If "
                                           "not, we got something else, like "
                                           "an error page."],
            ["`scraper.fetch(row[\"url\"], want=\"bytes\")`",
             "Downloads go through Nuhan's fetch, so robots.txt, the delay "
             "and the log apply."],
            ["`yield scrapy.Request(pdf_url, ...)` in `parse()`",
             "The crawling step - we found a new address and follow it."],
            ["`async def start(self)`", "Scrapy 2.17 removed start_requests; "
                                        "start() is its replacement."],
            ["`ROBOTSTXT_OBEY = True`", "Scrapy checks robots.txt itself. "
                                        "We left it on."],
            ["`values.median() > 1_000_000_000_000`",
             "Only numbers that big can be dates in milliseconds - so we "
             "never convert a price by mistake."],
            ["`tidy = df.copy()`", "The original is never changed, so we can "
                                   "always compare against it."],
        ])


#=========================================================================#
#  THE WHOLE DOCUMENT                                                     #
#=========================================================================#

WORDS = [
    ("Bytes", "The raw contents of a file, as small numbers from 0 to 255."),
    ("Callback", "The function Scrapy calls when a reply arrives."),
    ("CDN", "Content Delivery Network - a server built just for delivering "
            "files."),
    ("Cleaning", "Fixing the shape of data - types, gaps, repeats, spaces."),
    ("Crawling", "Finding pages or files by following links."),
    ("Duplicate", "A row or item that is an exact copy of another."),
    ("Framework", "A tool that runs the show and calls your code at the "
                  "right moments."),
    ("HEAD request", "A request for a file's details without the file "
                     "itself."),
    ("Inheritance", "Building a class on top of another, so it gets "
                    "everything the other can do."),
    ("Item", "One finished record produced by a Scrapy spider."),
    ("Median", "The middle value when all the values are put in order."),
    ("Missing value", "A gap in the data - shown as None or NaN."),
    ("Scrapy", "A Python framework built for crawling."),
    ("Set", "A collection that never holds the same thing twice."),
    ("Spider", "A crawler - in Scrapy, the class that does the crawling."),
    ("Type", "What kind of value something is: number, text, date."),
    ("yield", "Hand something back and carry on, ready to hand back more."),
]


def build():
    b = []
    b += M.cover(MEMBER, "Crawling for documents, and cleaning the data")
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
    b += file_crawler()
    b += E.page_break()
    b += file_scrapy()
    b += E.page_break()
    b += file_cleaner()
    b += E.page_break()
    b += M.big_picture(
        MEMBER, ["src/crawler.py", "src/cleaner.py"],
        ["Your part is step 5 and step 8. At step 5, your crawler takes the "
         "list of circulars from Pasindu's code and downloads the documents "
         "- which Nuhan's PDF reader and Salaama's OCR then read. At step 8, "
         "your cleaner tidies the share price table from Pasindu's code "
         "before Salaama's charts are drawn from it and her code saves it "
         "to files. Both of your steps sit in the middle of the project, "
         "joining the collecting to the using."])
    b += E.page_break()
    b += M.ethics_for_everyone()
    b += E.page_break()
    b += viva()
    b += E.page_break()
    b += M.practice_questions(MEMBER)
    b += E.page_break()
    b += M.word_list(WORDS)
    return b
