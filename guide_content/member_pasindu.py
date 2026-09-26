"""
Document for 25ada072 - Pasindu.

Getting the data from the site (src/api_client.py), Selenium
(src/selenium_scraper.py), and the settings (config.py, warm_cache.py).
"""

from guide_content import member_common as M
from guide_content import pdf_engine as E

MEMBER = "25ada072"
FILES = ["src/api_client.py", "src/selenium_scraper.py", "config.py",
         "warm_cache.py"]


#=========================================================================#
#  THE IDEAS BEHIND YOUR PART                                             #
#=========================================================================#

def ideas():
    b = []
    b += E.h1("The ideas behind your part")
    b += E.p(
        "Your part is where the project actually gets its numbers. It rests "
        "on two ideas: **APIs** - addresses that hand out data instead of "
        "pages - and **browsers**, which run JavaScript to build a page. "
        "This chapter explains both before we look at any code.")

    #--- APIs -----------------------------------------------------------#
    b += E.h2("What an API is")
    b += E.p(
        "**API** stands for Application Programming Interface. That sounds "
        "complicated, but the idea is simple: it is a way for one program "
        "to ask another program for data. You send a request, and you get "
        "a reply - usually in JSON.")
    b += E.idea(
        "the Week 5 lecture compared an API to a waiter. You tell the waiter "
        "what you want. The waiter takes the order to the kitchen. The "
        "kitchen cooks it, and the waiter brings it back to your table. You "
        "never go into the kitchen yourself. An API is the waiter between "
        "your program and the website's data.")

    b += E.h3("How a website talks to its data")
    b += E.p("Behind every website there is a **database** - a store of all "
             "its information. The lecture described how a page gets data "
             "out of it:")
    b += E.code(
        "  The page (in your browser)\n"
        "        |   1. asks for something\n"
        "        v\n"
        "  The API  (/api/tradeSummary)\n"
        "        |   2. asks the database for you\n"
        "        v\n"
        "  The database\n"
        "        |   3. finds the data\n"
        "        v\n"
        "  The API\n"
        "        |   4. sends it back as JSON\n"
        "        v\n"
        "  The page shows it")

    b += E.h3("Why websites have APIs")
    b += E.p("The Week 5 lecture gave these reasons:")
    b += E.bullets([
        "**So the site's own pages can load data** without reloading the "
        "whole page. This is CSE's reason - their trade summary page calls "
        "`/api/tradeSummary` itself.",
        "To share data with developers safely.",
        "To let others build apps with their data.",
        "To reduce the load on the website, because data can be fetched "
        "without opening full pages.",
    ])

    #--- JSON -----------------------------------------------------------#
    b += E.h2("JSON, the shape of the replies")
    b += E.p(
        "Every reply from a CSE data address is JSON. You met the basics in "
        "the chapter on how the web works. Here is a real record for one "
        "company, exactly as CSE sent it:")
    b += E.code(
        '{\n'
        '  "id": 266,\n'
        '  "name": "SAMPATH BANK PLC",\n'
        '  "symbol": "SAMP.N0000",\n'
        '  "price": 141.0,\n'
        '  "previousClose": 140.25,\n'
        '  "change": 0.75,\n'
        '  "percentageChange": 0.5347593582887701,\n'
        '  "high": 141.25,\n'
        '  "low": 140.0,\n'
        '  "turnover": 13244976.75,\n'
        '  "lastTradedTime": 1790326797431,\n'
        '  "marketCap": 165350807160.0\n'
        '  ...  (23 fields in all)\n'
        '}')
    b += E.table([
        ["Field", "Meaning"],
        ["`price`", "What one share sold for today, in rupees"],
        ["`previousClose`", "The price at the end of the last trading day"],
        ["`change`", "The difference: 141.00 - 140.25 = 0.75"],
        ["`percentageChange`", "That change as a percentage of the old price"],
        ["`turnover`", "Total money that changed hands for this company "
                       "today"],
        ["`lastTradedTime`", "When the last trade happened - as a number "
                             "(explained below)"],
        ["`marketCap`", "The whole company's value: share price times the "
                        "number of shares"],
    ], widths=[2.7, 5.8])
    b += E.p(
        "The whole reply is one big wrapper holding a list of these records "
        "- one for every company that traded:")
    b += E.code(
        '{\n'
        '  "reqTradeSummery": [\n'
        '     { ...ABANS ELECTRICALS PLC... },\n'
        '     { ...ABANS FINANCE PLC... },\n'
        '     ...\n'
        '     { ...SAMPATH BANK PLC... },\n'
        '     ...   (284 records on the day we checked)\n'
        '  ]\n'
        '}')
    b += E.p(
        "Notice `reqTradeSummery` is misspelled - 'Summery' instead of "
        "'Summary'. That is CSE's spelling, so our code has to use it "
        "exactly. The same goes for `topLooses` and `companyInfoSummery`. "
        "When you read somebody else's API, you use their names, spelling "
        "mistakes and all.")

    b += E.h3("Dates as big numbers")
    b += E.p(
        "`lastTradedTime` is `1790326797431`. That is not a mistake. It is "
        "the number of **milliseconds since 1 January 1970** - a common way "
        "for computers to store a moment in time, called **epoch time**. "
        "Divide by 1000 to get seconds, and Python can turn it into a normal "
        "date. Your function `to_datetime()` does exactly that.")

    #--- Finding it -----------------------------------------------------#
    b += E.h2("How we found CSE's data addresses")
    b += E.p(
        "CSE does not publish a list of its data addresses. We found them "
        "the way the Week 1 lecture taught: by watching the page work.")
    b += E.numbered([
        "Open `https://www.cse.lk/equity/trade-summary` in Chrome or Edge.",
        "Press **F12**. The developer tools open at the side or bottom.",
        "Click the **Network** tab. It lists every request the page makes.",
        "Click the **Fetch/XHR** filter, so only data requests are shown - "
        "not pictures and fonts.",
        "Press **F5** to reload the page, and watch the list fill up.",
        "Click the request called `tradeSummary`. The **Headers** section "
        "shows its address and that it was sent as **POST**. The "
        "**Response** or **Preview** section shows the JSON it got back.",
    ])
    b += E.idea(
        "the Network tab is like standing next to the waiter's hatch in a "
        "restaurant, writing down every order that goes into the kitchen. "
        "You learn exactly what to ask for - and then you can ask for it "
        "yourself.")
    b += E.tryit(
        "do these six steps yourself before the viva. Being able to say 'I "
        "pressed F12 and watched the Network tab' - and to show it - is the "
        "most convincing thing you can say about your part.")

    #--- API vs scraping ------------------------------------------------#
    b += E.h2("Why an API is better than scraping the page")
    b += E.p(
        "The Week 6 lecture said it plainly: 'Use APIs where available - an "
        "official API is generally more reliable and structured than "
        "scraping.' For CSE the difference is large:")
    b += E.table([
        ["", "Reading the data address", "Scraping the page in a browser"],
        ["Companies from one go", "All of them - 284", "About 25 - the table "
                                                       "is split into pages"],
        ["Time", "About 1 second", "About 5 seconds"],
        ["Size of reply", "One JSON file", "142 KB of HTML, plus scripts, "
                                          "fonts and images"],
        ["Work for CSE's server", "Send one piece of data",
         "Send the whole page - and then the browser asks for the same data "
         "anyway"],
    ], widths=[2.4, 2.9, 3.2])
    b += E.p(
        "That last row is the ethical point. Loading the page does not "
        "avoid the data address - the page calls it too. Reading it "
        "directly just skips all the extra work.")

    b += E.h3("The limits of an API")
    b += E.p("The Week 5 lecture listed the weaknesses of APIs too. Here is "
             "how each one applies to us:")
    b += E.table([
        ["Limitation", "Does it affect us?"],
        ["Limits on how many requests you may send", "CSE sets none that we "
                                                     "know of - we wait 1.5 "
                                                     "seconds anyway"],
        ["May need a key or an account", "No - CSE's addresses are open"],
        ["May give less data than the website shows", "No - it is the "
                                                      "same data the page "
                                                      "shows"],
        ["Can change without warning", "**Yes** - these addresses are not "
                                       "officially published, so CSE could "
                                       "change them any day"],
    ], widths=[4.2, 4.3])
    b += E.remember(
        "we found CSE's data addresses by watching the Network tab, and we "
        "use them because they are faster, give every company at once, and "
        "are less work for CSE's server than loading the page.")

    #--- Browsers and Selenium ------------------------------------------#
    b += E.h2("Browsers, JavaScript and Selenium")
    b += E.p(
        "When a browser opens the CSE page, it does much more than download "
        "a file:")
    b += E.numbered([
        "It downloads the HTML - the nearly empty shell.",
        "It downloads the JavaScript files the HTML points to.",
        "It **runs** the JavaScript.",
        "The JavaScript calls `/api/tradeSummary` - the same address your "
        "code uses.",
        "The JavaScript builds the table and puts it on the page.",
    ])
    b += E.p(
        "The page, as it is after all that, is called the **DOM**. `requests` "
        "only ever does step 1, which is why it sees nothing. A real browser "
        "does all five.")
    b += E.p(
        "**Selenium** is a tool that lets a program control a real web "
        "browser - open pages, click, type, scroll - exactly as a person "
        "would. The Week 6 lecture showed how it works:")
    b += E.code(
        "  Your Python script\n"
        "        |   'open this page'\n"
        "        v\n"
        "  The driver  (msedgedriver / chromedriver)\n"
        "        |   passes the order on\n"
        "        v\n"
        "  The real browser  (Edge / Chrome)\n"
        "        |   opens the page, runs the JavaScript\n"
        "        v\n"
        "  The finished page comes back to your script")
    b += E.p(
        "The **driver** is a small program that sits between Python and the "
        "browser, turning Python's orders into actions. Each browser needs "
        "its own driver, and it must match the browser's version. The "
        "lecture described downloading it by hand - but since Selenium 4.6, "
        "a part called **Selenium Manager** finds and downloads the right "
        "driver by itself.")
    b += E.idea(
        "requests is like asking for a photocopy of a newspaper before it "
        "has been printed. Selenium sends a robot to sit at a real computer, "
        "open the paper, wait for the ink to dry, and then take a photo.")
    b += E.table([
        ["Selenium word", "Meaning"],
        ["`driver.get(url)`", "Open this page in the browser"],
        ["Headless", "Run the browser invisibly, with no window - faster, "
                     "and it does not pop up during a demonstration"],
        ["`WebDriverWait`", "Wait until something appears on the page - "
                            "the lecture's 'explicit wait'"],
        ["`driver.page_source`", "The page's HTML as it is now, after the "
                                 "JavaScript has run"],
        ["`driver.save_screenshot()`", "Save a picture of what the browser "
                                       "shows"],
        ["`driver.quit()`", "Close the browser completely"],
    ], widths=[3.0, 5.5])
    return b


#=========================================================================#
#  READING PYTHON                                                         #
#=========================================================================#

def python_chapter():
    examples = {
        "comment": (
            "# The reply has several parts. The company details are under\n"
            "# reqSymbolInfo.",
            "From `company_info()`. It explains the line below it to a "
            "reader. Python skips both lines."),
        "variable": (
            'url = f"{config.API_BASE}/{endpoint}"',
            "From `call()`. The finished address is put in a box called "
            "`url`, ready to be sent."),
        "text": (
            'url = f"{config.API_BASE}/{endpoint}"',
            "The same line, as an f-string. `config.API_BASE` holds "
            "`https://www.cse.lk/api`. If `endpoint` holds `tradeSummary`, "
            "the result is `https://www.cse.lk/api/tradeSummary`."),
        "numbers": (
            "DELAY = 1.5\n"
            "TIMEOUT = 30",
            "From `config.py`. The polite pause between requests, and how "
            "many seconds to wait for a reply before giving up. Names in "
            "capital letters are a Python habit meaning 'a setting - do not "
            "change this while the program runs'."),
        "list": (
            "rows = []\n"
            "for number, symbol in enumerate(symbols, start=1):\n"
            "    ...\n"
            "    info = self.company_info(symbol)\n"
            "    if info:\n"
            "        rows.append(info)",
            "From `several_companies()`. Start with an empty list, then add "
            "each company's details to it, one at a time."),
        "dict": (
            "ENDPOINTS = {\n"
            '    "tradeSummary":    {"method": "POST", "desc": "Trade data for every company"},\n'
            '    "allSecurityCode": {"method": "GET",  "desc": "List of all listed companies"},\n'
            "    ...\n"
            "}",
            "From `config.py`. A dictionary of dictionaries: under each "
            "address name is a smaller dictionary saying whether it needs "
            "GET or POST. Your `call()` reads it with "
            "`config.ENDPOINTS.get(endpoint, {}).get(\"method\", \"POST\")` "
            "- 'find this address; if it is not listed, use an empty "
            "dictionary; then find its method, or use POST if none is "
            "given'."),
        "function": (
            "def company_info(self, symbol):\n"
            '    reply = self.call("companyInfoSummery",\n'
            '                      data={"symbol": symbol})\n'
            '    if not reply["ok"]:\n'
            "        return {}\n"
            '    return dict(reply["data"].get("reqSymbolInfo", {}))',
            "The ingredient is a company symbol such as `SAMP.N0000`. The "
            "function sends it with the request and returns that company's "
            "details - or an empty dictionary `{}` if something went wrong."),
        "if": (
            'if not reply["ok"]:\n'
            "    return pd.DataFrame()",
            "From `sectors()` and several others. If the request failed, "
            "hand back an empty table straight away, so the app shows "
            "nothing instead of crashing."),
        "for": (
            "for number, symbol in enumerate(symbols, start=1):",
            "From `several_companies()`. Go through the list of symbols one "
            "by one, counting 1, 2, 3 so the progress bar can say 'Getting "
            "SAMP.N0000 (3 of 15)'."),
        "import": (
            "from datetime import datetime\n"
            "import pandas as pd\n"
            "from selenium import webdriver\n"
            "from bs4 import BeautifulSoup",
            "Your files use datetime to read epoch times, pandas to make "
            "tables, Selenium to drive a browser, and BeautifulSoup to read "
            "the browser's finished page."),
        "try": (
            "try:\n"
            "    return datetime.fromtimestamp(float(value) / 1000)\n"
            "except (ValueError, OSError, TypeError):\n"
            "    return None",
            "From `to_datetime()`. If the value cannot be turned into a date "
            "- it is text, or far too big - give back `None` instead of "
            "stopping the whole table from loading. Naming the exact errors "
            "in brackets means only those are caught."),
        "class": (
            "class CSEApi:\n\n"
            "    def __init__(self, scraper=None):\n"
            "        self.scraper = scraper or Scraper()",
            "From `api_client.py`. When the app makes a `CSEApi()`, it is "
            "given a Scraper - Nuhan's class that sends requests politely. "
            "`scraper or Scraper()` means 'use the one I was given, or make "
            "a new one'. Every method then sends its requests through "
            "`self.scraper`."),
        "pandas": (
            "df = pd.DataFrame(records)\n"
            "...\n"
            "df[column] = df[column].apply(to_datetime)",
            "From `make_dataframe()`. The first line turns the list of "
            "company records into a table - one row per company, one column "
            "per field. The second runs `to_datetime()` on every value in a "
            "date column. `.apply()` means 'do this to each value'."),
    }

    extras = [
        ("isinstance - what kind of thing is this?",
         "`isinstance(x, list)` answers True if `x` is a list. Your "
         "`get_records()` uses it because different CSE addresses send "
         "different shapes:",
         "if isinstance(reply, list):\n"
         "    ...\n"
         "if isinstance(reply, dict):\n"
         "    ...",
         None),
        ("try and finally - always tidy up",
         "`finally` runs at the end whatever happened - success or error. "
         "Your Selenium code uses it to make sure the browser always closes:",
         "try:\n"
         "    driver.get(url)\n"
         "    ...\n"
         "finally:\n"
         "    driver.quit()",
         "Without it, one error would leave an invisible browser running in "
         "the background, using memory, and after a few failed runs there "
         "would be several."),
        ("Functions without brackets",
         "Writing a function's name **with** brackets runs it: "
         "`api.aspi()`. Writing it **without** brackets just refers to it, "
         "so it can be stored and run later. Your `warm_cache.py` makes a "
         "list of jobs this way:",
         "jobs = [\n"
         '    ("Market status", api.market_status),\n'
         '    ("Index", api.aspi),\n'
         "    ...\n"
         "]\n"
         "for name, job in jobs:\n"
         "    result = job()",
         "Nothing runs while the list is being made. Each job runs later, at "
         "`job()`."),
    ]
    return M.python_chapter(MEMBER, examples, "src/api_client.py", extras)


#=========================================================================#
#  FILE 1 - src/api_client.py                                             #
#=========================================================================#

def file_api():
    b = []
    b += E.h1("Your file: src/api_client.py")
    b += E.big(
        "This is where the project gets its numbers. It asks CSE's data "
        "addresses for information and turns each JSON reply into a table.")
    b += E.p(
        "The file has three small helper functions at the top, and then one "
        "class, `CSEApi`, with one method for each kind of data we want.")

    #--- helpers --------------------------------------------------------#
    b += E.h2("Part 1 - The three helpers")
    b += E.h3("to_datetime(): big numbers into dates")
    b += E.code(
        "def to_datetime(value):\n"
        "    if value is None:\n"
        "        return None\n"
        "    try:\n"
        "        return datetime.fromtimestamp(float(value) / 1000)\n"
        "    except (ValueError, OSError, TypeError):\n"
        "        return None")
    b += E.p(
        "`1790326797431` divided by 1000 is the number of seconds since "
        "1970. `datetime.fromtimestamp()` turns seconds into a normal date "
        "and time. `float(...)` makes sure the value is a number first.")
    b += E.p(
        "`fromtimestamp()` gives the time in the computer's own time zone. "
        "On our laptops in Sri Lanka that is Sri Lanka time, which is what "
        "we want. Sasini's cleaner converts the share price times to Colombo "
        "time on purpose, so those are right on any computer.")

    b += E.h3("get_records(): digging out the list")
    b += E.p(
        "The CSE addresses do not all reply in the same shape. Some send a "
        "plain list. Some wrap the list in a dictionary under a name like "
        "`reqTradeSummery`. A few send a list inside another list. This "
        "function copes with all of them, so the rest of the code does not "
        "have to:")
    b += E.code(
        "def get_records(reply, key=None):\n"
        "    if reply is None:\n"
        "        return []\n\n"
        "    if isinstance(reply, list):\n"
        "        # A few replies are a list inside another list.\n"
        "        if len(reply) == 1 and isinstance(reply[0], list):\n"
        "            return reply[0]\n"
        "        return reply\n\n"
        "    if isinstance(reply, dict):\n"
        "        if key and key in reply:\n"
        "            return reply[key]\n"
        "        for value in reply.values():\n"
        "            if isinstance(value, list):\n"
        "                return value\n"
        "        return [reply]\n\n"
        "    return []")
    b += E.table([
        ["If the reply looks like", "It gives back"],
        ["`[ {...}, {...} ]` - a plain list", "The list as it is"],
        ["`[ [ {...}, {...} ] ]` - a list inside a list",
         "The inner list"],
        ["`{\"reqTradeSummery\": [ ... ]}` - a wrapper",
         "The list under the name we asked for"],
        ["`{\"status\": \"Market Closed\"}` - one record",
         "That record, inside a list of one"],
        ["`None` - nothing", "An empty list"],
    ], widths=[4.6, 3.9])
    b += E.idea(
        "parcels arrive in different packaging - a bag, a box, a box inside "
        "a box. get_records() unwraps each one, so what lands on the table "
        "is always the same: a list of records.")

    b += E.h3("make_dataframe(): the list becomes a table")
    b += E.code(
        "def make_dataframe(records, date_columns=()):\n"
        "    if not records:\n"
        "        return pd.DataFrame()\n\n"
        "    df = pd.DataFrame(records)\n\n"
        "    for column in date_columns:\n"
        "        if column in df.columns:\n"
        "            df[column] = df[column].apply(to_datetime)\n\n"
        "    return df")
    b += E.p(
        "`pd.DataFrame(records)` does most of the work in one line: a list "
        "of dictionaries becomes a table, one row per dictionary, one column "
        "per name. Then any columns we name as dates are converted with "
        "`to_datetime()`.")
    b += E.p("284 dictionaries like the Sampath Bank one become a table like "
             "this:")
    b += E.code(
        "       symbol                    name    price  change  percentageChange\n"
        "0  ABAN.N0000   ABANS ELECTRICALS PLC  1058.25    16.0          1.535140\n"
        "1  AFSL.N0000       ABANS FINANCE PLC    84.50     1.0          1.197605\n"
        "2   AEL.N0000  ACCESS ENGINEERING PLC    80.10     0.0          0.000000\n"
        "3   ACL.N0000          ACL CABLES PLC    92.50    -0.8         -0.857449\n"
        "4  APLA.N0000        ACL PLASTICS PLC   159.50     0.5          0.314465")

    #--- call -----------------------------------------------------------#
    b += E.h2("Part 2 - call(), sending one request")
    b += E.code(
        "class CSEApi:\n\n"
        "    def __init__(self, scraper=None):\n"
        "        self.scraper = scraper or Scraper()\n\n"
        "    def call(self, endpoint, data=None):\n"
        "        method = config.ENDPOINTS.get(endpoint, {}).get(\"method\",\n"
        "                                                        \"POST\")\n"
        "        url = f\"{config.API_BASE}/{endpoint}\"\n"
        "        return self.scraper.fetch(url, method=method, data=data,\n"
        "                                  save_as=endpoint)")
    b += E.p("Every method in the class sends its request through `call()`. "
             "It does three things:")
    b += E.numbered([
        "Looks up whether this address needs GET or POST, in the `ENDPOINTS` "
        "table in `config.py`.",
        "Builds the full address, such as "
        "`https://www.cse.lk/api/tradeSummary`.",
        "Hands it to `self.scraper.fetch()` - Nuhan's function, which checks "
        "robots.txt, waits 1.5 seconds, sends the request with our "
        "User-Agent, and records it. `save_as=endpoint` means the reply is "
        "also saved as `data/cache/tradeSummary.json`.",
    ])
    b += E.remember(
        "your code never talks to the internet directly. It asks Nuhan's "
        "`fetch()` to do it, so every one of your requests follows the "
        "ethical rules automatically.")

    #--- methods --------------------------------------------------------#
    b += E.h2("Part 3 - One method for each kind of data")
    b += E.p("Most methods follow the same three-line pattern. Here is the "
             "main one:")
    b += E.code(
        "def trade_summary(self):\n"
        "    reply = self.call(\"tradeSummary\")\n"
        "    if not reply[\"ok\"]:\n"
        "        self.scraper.log.add(f\"Could not get trade summary: \"\n"
        "                             f\"{reply['error']}\")\n"
        "        return pd.DataFrame()\n\n"
        "    df = make_dataframe(get_records(reply[\"data\"],\n"
        "                                    \"reqTradeSummery\"))\n"
        "    self.scraper.log.add(f\"Got trade data for {len(df)} companies\")\n"
        "    return df")
    b += E.numbered([
        "**Ask** - `self.call(\"tradeSummary\")`.",
        "**Check** - if it failed, write a message in the log and return an "
        "empty table.",
        "**Unwrap and tabulate** - `get_records()` digs out the list, "
        "`make_dataframe()` makes the table.",
    ])
    b += E.p("The whole set:")
    b += E.table([
        ["Method", "Address", "What it gives back"],
        ["`market_status()`", "`marketStatus`", "'Market Open' or 'Market "
                                                "Closed'"],
        ["`aspi()`", "`aspiData`", "The All Share Price Index - one number "
                                   "for the whole market"],
        ["`market_summary()`", "`marketSummery`", "Today's total turnover "
                                                  "and volume"],
        ["`sectors()`", "`allSectors`", "A table of sector indices - Banks, "
                                        "Energy and so on"],
        ["`trade_summary()`", "`tradeSummary`", "**The main table** - every "
                                                "company that traded"],
        ["`top_gainers()`", "`topGainers`", "The biggest risers"],
        ["`top_losers()`", "`topLooses`", "The biggest fallers (CSE's "
                                          "spelling)"],
        ["`all_companies()`", "`allSecurityCode`", "Every listed company and "
                                                   "its symbol"],
        ["`company_info(symbol)`", "`companyInfoSummery`",
         "Details for one company"],
        ["`announcements()`", "`approvedAnnouncement`",
         "Company announcements"],
        ["`circulars()`", "`circularAnnouncement`",
         "CSE circulars, with PDF links"],
    ], widths=[2.6, 2.7, 3.2])

    b += E.h3("company_info() - sending a value with the request")
    b += E.code(
        "def company_info(self, symbol):\n"
        "    reply = self.call(\"companyInfoSummery\",\n"
        "                      data={\"symbol\": symbol})\n"
        "    if not reply[\"ok\"]:\n"
        "        return {}\n"
        "    return dict(reply[\"data\"].get(\"reqSymbolInfo\", {}))")
    b += E.p(
        "This address has to know which company you mean, so the symbol is "
        "sent **with** the POST request, as form data: "
        "`data={\"symbol\": \"SAMP.N0000\"}` - like filling in one box on a "
        "form before handing it in.")
    b += E.p(
        "The reply has four parts: `reqSymbolBetaInfo`, `reqTagsLogo`, "
        "`reqLogo` and `reqSymbolInfo`. We found which one held the prices "
        "by printing the reply and looking. The details are in "
        "`reqSymbolInfo`, so that is the part we keep.")

    b += E.h3("several_companies() - slow on purpose")
    b += E.code(
        "def several_companies(self, symbols, progress=None):\n"
        "    rows = []\n"
        "    for number, symbol in enumerate(symbols, start=1):\n"
        "        if progress:\n"
        "            progress(number / len(symbols),\n"
        "                     f\"Getting {symbol} ({number} of {len(symbols)})\")\n"
        "        info = self.company_info(symbol)\n"
        "        if info:\n"
        "            rows.append(info)\n"
        "    return make_dataframe(rows)")
    b += E.p(
        "Each company is a separate request, and each one waits its 1.5 "
        "seconds - so 15 companies take a little over 20 seconds. That is "
        "deliberate. This is the only loop in the project that sends many "
        "requests in a row, so it is where politeness matters most. "
        "`progress(...)` moves the progress bar in the app.")

    b += E.h3("circulars() - building full PDF addresses")
    b += E.code(
        "df = make_dataframe(get_records(reply[\"data\"],\n"
        "                                \"reqCircularAnnouncement\"))\n\n"
        "if not df.empty and \"path\" in df.columns:\n"
        "    df[\"pdf_url\"] = config.CDN_BASE + df[\"path\"].astype(str)")
    b += E.p(
        "Each circular comes with only part of its PDF's address, such as "
        "`upload_report_file/abc.pdf`. The PDFs live on a different server, "
        "so we add `https://cdn.cse.lk/cmt/` in front. Adding two text "
        "columns with `+` in pandas joins them row by row, making a new "
        "column `pdf_url`. Sasini's crawler then uses those links.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.api_client")
    b += E.code(
        "Market status: Market Closed\n"
        "ASPI index   : 21,037.35 (-29.54)\n\n"
        "Trade summary - first 5 companies\n"
        "       symbol                    name    price  change\n"
        "0  ABAN.N0000   ABANS ELECTRICALS PLC  1058.25    16.0\n"
        "...\n\n"
        "One company\n"
        "SAMPATH BANK PLC - 141.0\n\n"
        "17:48:03  POST https://www.cse.lk/api/marketStatus - status 200\n"
        "17:48:04  POST https://www.cse.lk/api/aspiData - status 200\n"
        "17:48:05  POST https://www.cse.lk/api/tradeSummary - status 200\n"
        "17:48:05  Got trade data for 284 companies")
    b += E.p(
        "Look at the times at the bottom: each request is at least a second "
        "and a half after the one before. That is Nuhan's `wait()` working "
        "on your requests.")
    return b


#=========================================================================#
#  FILE 2 - src/selenium_scraper.py                                       #
#=========================================================================#

def file_selenium():
    b = []
    b += E.h1("Your file: src/selenium_scraper.py")
    b += E.big(
        "Opens the CSE page in a real browser, so the JavaScript runs and "
        "the prices actually appear - then reads the finished page.")
    b += E.p(
        "This file is not how the project collects its data - the API is. "
        "It is here to show the browser method works, to prove the API "
        "gives the same numbers a visitor sees, and as a backup if the data "
        "addresses ever change.")

    b += E.h2("Part 1 - start_browser()")
    b += E.code(
        "def start_browser(headless=True):\n"
        "    from selenium import webdriver\n\n"
        "    browsers = [\n"
        "        (\"Edge\", webdriver.Edge, webdriver.EdgeOptions),\n"
        "        (\"Chrome\", webdriver.Chrome, webdriver.ChromeOptions),\n"
        "        (\"Firefox\", webdriver.Firefox, webdriver.FirefoxOptions),\n"
        "    ]\n\n"
        "    for name, browser, options_class in browsers:\n"
        "        try:\n"
        "            options = options_class()\n"
        "            if headless:\n"
        "                options.add_argument(\"--headless=new\")\n"
        "            options.add_argument(\"--window-size=1920,1080\")\n"
        "            options.add_argument(f\"--user-agent={config.USER_AGENT}\")\n\n"
        "            return browser(options=options), name\n"
        "        except Exception:\n"
        "            continue\n\n"
        "    return None, \"No browser could be started. ...\"")
    b += E.bullets([
        "The lecture used Chrome. The laptop we built this on has only "
        "Microsoft Edge, so the code tries Edge first, then Chrome, then "
        "Firefox. It works on anybody's computer.",
        "The list holds three **tuples** - groups of three things each: a "
        "name, the browser, and its settings type.",
        "`--headless=new` - run without a window.",
        "`--window-size=1920,1080` - pretend the screen is a normal laptop "
        "size, so the page lays itself out properly.",
        "`--user-agent=...` - the same honest name as the rest of the "
        "project, so CSE sees one consistent visitor.",
        "If a browser will not start, `continue` moves on and tries the "
        "next one.",
    ])

    b += E.h2("Part 2 - load_page()")
    b += E.code(
        "driver, browser_name = start_browser(headless)\n"
        "...\n"
        "try:\n"
        "    driver.get(url)\n\n"
        "    try:\n"
        "        WebDriverWait(driver, wait_seconds).until(\n"
        "            expected_conditions.presence_of_element_located(\n"
        "                (By.TAG_NAME, \"table\"))\n"
        "        )\n"
        "    except Exception:\n"
        "        pass  # No table appeared, but we can still look at the page.\n\n"
        "    time.sleep(2)  # Let the last few rows settle.\n\n"
        "    html = driver.page_source\n"
        "    driver.save_screenshot(screenshot)\n\n"
        "    soup = BeautifulSoup(html, \"html.parser\")\n"
        "    words = soup.get_text(strip=True)\n"
        "    tables = soup.find_all(\"table\")\n"
        "    ...\n"
        "finally:\n"
        "    try:\n"
        "        driver.quit()\n"
        "    except Exception:\n"
        "        pass")
    b += E.p("Step by step:")
    b += E.numbered([
        "`driver.get(url)` - the browser opens the page. At this moment the "
        "table does not exist yet - JavaScript is still fetching the data.",
        "`WebDriverWait(driver, 15).until(...)` - wait, up to 15 seconds, "
        "until a `<table>` tag appears on the page. This is the lecture's "
        "**explicit wait**. `By.TAG_NAME` means 'find it by its tag name'.",
        "`time.sleep(2)` - a short extra pause so the last rows finish "
        "appearing.",
        "`driver.page_source` - the page's HTML **as it is now**, after "
        "JavaScript. This is the key line. It is the difference from "
        "`response.text` in the requests version, which is the page before "
        "JavaScript.",
        "`save_screenshot()` - a picture of what the browser saw.",
        "From there it is ordinary BeautifulSoup, the same methods as in "
        "Nuhan's file.",
        "`finally: driver.quit()` - always close the browser, even if "
        "something went wrong.",
    ])
    b += E.image(M.IMG / "selenium_page.png", 15,
                 "The CSE trade summary page as our Selenium browser saw it "
                 "- the table is there, because the JavaScript ran.")

    b += E.h3("Why wait for the table instead of just sleeping?")
    b += E.p(
        "You could write `time.sleep(10)` and hope the table has appeared by "
        "then. But on a fast connection that wastes most of the 10 seconds, "
        "and on a slow one 10 seconds might not be enough. "
        "`WebDriverWait` carries on the moment the table appears - never "
        "sooner, never later than it needs to.")
    b += E.idea(
        "waiting for a bus by watching the road, instead of setting a "
        "timer for 10 minutes. You get on as soon as it arrives, and you "
        "never leave before it comes.")

    b += E.h2("Part 3 - read_table()")
    b += E.code(
        "def read_table(table):\n"
        "    headings = [cell.get_text(strip=True)\n"
        "                for cell in table.find_all(\"th\")]\n\n"
        "    rows = []\n"
        "    for row in table.find_all(\"tr\"):\n"
        "        cells = row.find_all(\"td\")\n"
        "        if not cells:\n"
        "            continue  # this is the heading row\n"
        "        rows.append([cell.get_text(strip=True) for cell in cells])\n\n"
        "    if not rows:\n"
        "        return pd.DataFrame()\n\n"
        "    if len(headings) != len(rows[0]):\n"
        "        headings = [f\"Column {i + 1}\" for i in range(len(rows[0]))]\n\n"
        "    return pd.DataFrame(rows, columns=headings)")
    b += E.p(
        "This turns an HTML table into a pandas table, using the Week 3 "
        "idea of how tables are built: `<th>` cells are headings, `<tr>` is "
        "a row, and `<td>` cells are the data.")
    b += E.bullets([
        "The headings are collected from every `<th>` cell.",
        "Each row's `<td>` cells become one list. The heading row has no "
        "`<td>` cells, so `continue` skips it.",
        "If the number of headings does not match the number of cells, the "
        "columns are simply numbered, so no rows are lost.",
    ])

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own (it takes about 5 seconds):",
                 "python -m src.selenium_scraper")
    b += E.code(
        "  Browser    : Edge\n"
        "  HTML size  : 142,407 bytes\n"
        "  Words found: 4,121 characters\n"
        "  Tables     : 1\n"
        "  Time taken : 5.3 seconds")
    b += E.table([
        ["", "requests (Nuhan's file)", "Selenium (your file)"],
        ["HTML", "17,898 bytes", "142,407 bytes"],
        ["Words found", "24 characters", "4,121 characters"],
        ["Tables", "0", "1"],
    ], widths=[2.4, 3.0, 3.1])
    b += E.p("Same address, same BeautifulSoup code afterwards. The only "
             "difference is that the browser ran the JavaScript first.")
    b += E.careful(
        "Selenium's browser makes its own requests, so they do **not** go "
        "through Nuhan's `fetch()` - robots.txt is not checked by our code "
        "for them, and they are not in the request log. We give the browser "
        "our honest User-Agent, load only this one page, and the page is "
        "allowed by robots.txt. If asked, say this plainly: it is the one "
        "exception to 'every request goes through fetch()'.")
    b += E.remember(
        "Selenium works because it runs a real browser, which runs the "
        "JavaScript. It is not our main method because it is slower, much "
        "heavier for CSE's server, and only gets the first page of about 25 "
        "companies - the API gives all of them in one request.")
    return b


#=========================================================================#
#  FILE 3 - config.py and warm_cache.py                                   #
#=========================================================================#

def file_config():
    b = []
    b += E.h1("Your files: config.py and warm_cache.py")

    b += E.h2("config.py - every setting in one place")
    b += E.p(
        "`config.py` holds every setting the project uses. Nothing in it "
        "does anything by itself - it just stores values that the other files read. "
        "If CSE ever changes an address, or we want a longer delay, we "
        "change one line here instead of hunting through ten files.")
    b += E.table([
        ["Setting", "Value", "Used by"],
        ["`BASE_URL`", "`https://www.cse.lk`", "Everything"],
        ["`API_BASE`", "`https://www.cse.lk/api`", "`api_client.py`"],
        ["`CDN_BASE`", "`https://cdn.cse.lk/cmt/`", "`circulars()` - the PDF "
                                                   "server"],
        ["`ENDPOINTS`", "The 11 data addresses, and GET or POST",
         "`call()`"],
        ["`USER_AGENT`", "Our honest name", "`ethics.py`, Selenium"],
        ["`DELAY`", "`1.5`", "`ethics.py` - the pause"],
        ["`TIMEOUT`", "`30`", "Give up waiting for a reply after 30 s"],
        ["`OCR_TEXT_THRESHOLD`", "`50`", "`pdf_extractor.py`"],
        ["`OCR_DPI`", "`200`", "`ocr_extractor.py`"],
        ["`NAMES`", "Index numbers and names", "The app and the documents"],
    ], widths=[2.8, 3.2, 2.5])

    b += E.h3("The folders")
    b += E.code(
        "ROOT_DIR   = Path(__file__).parent\n"
        "DATA_DIR   = ROOT_DIR / \"data\"\n"
        "PDF_DIR    = DATA_DIR / \"pdfs\"\n"
        "CACHE_DIR  = DATA_DIR / \"cache\"\n"
        "...\n\n"
        "for _folder in (RAW_DIR, PDF_DIR, IMAGE_DIR, EXPORT_DIR, CACHE_DIR,\n"
        "                LOG_DIR, DOCS_DIR):\n"
        "    _folder.mkdir(parents=True, exist_ok=True)")
    b += E.bullets([
        "`Path(__file__).parent` - 'the folder this file is in'. So the "
        "project works wherever it is copied to, not only on one computer.",
        "`/` joins folder names into a path: `DATA_DIR / \"pdfs\"` is "
        "`data\\pdfs`.",
        "The loop creates every folder when the project starts. "
        "`exist_ok=True` means 'if it is already there, that is fine'. So no "
        "file ever crashes because a folder is missing.",
    ])

    b += E.h3("Names beside index numbers")
    b += E.code(
        "NAMES = {\n"
        "    \"24ada076\": \"Nuhan\",\n"
        "    \"25ada072\": \"Pasindu\",\n"
        "    \"25ada073\": \"Sasini\",\n"
        "    \"25ada141\": \"Salaama\",\n"
        "}\n\n"
        "def member_label(index):\n"
        "    name = NAMES.get(index)\n"
        "    return f\"{index} - {name}\" if name else index")
    b += E.p(
        "`member_label(\"25ada072\")` gives `25ada072 - Pasindu`. The app "
        "uses it for the title bar, the Home table, and the label on each "
        "tab. `x if condition else y` is a one-line if: 'the name label if "
        "we have a name, otherwise just the index'.")

    b += E.h2("warm_cache.py - collecting a copy before the viva")
    b += E.p(
        "Every reply `fetch()` receives is saved as a copy. `warm_cache.py` "
        "asks for everything once, so every copy exists before a "
        "demonstration. Then if the internet fails in the viva room, the "
        "app shows the saved copies instead of errors.")
    b += E.code(
        "jobs = [\n"
        "    (\"Market status\", api.market_status),\n"
        "    (\"Index\", api.aspi),\n"
        "    (\"Share prices\", api.trade_summary),\n"
        "    ...\n"
        "]\n\n"
        "for name, job in jobs:\n"
        "    try:\n"
        "        result = job()\n"
        "        size = len(result) if hasattr(result, \"__len__\") else 1\n"
        "        print(f\"  saved   {name:18} ({size} record(s))\")\n"
        "    except Exception as e:\n"
        "        print(f\"  failed  {name:18} {e}\")")
    b += E.bullets([
        "Each job is a pair: a name to print, and a method to run later.",
        "`hasattr(result, \"__len__\")` - 'can this be counted?' A table or "
        "list can; a single word like 'Market Closed' cannot, so it counts "
        "as 1.",
        "`{name:18}` pads the name to 18 characters, so the printed list "
        "lines up neatly.",
        "If one job fails, `except` prints it and the loop carries on with "
        "the rest.",
    ])
    b += E.tryit("run it before the viva - it takes about a minute:",
                 "python warm_cache.py")
    b += E.remember(
        "config.py stores every setting in one place, and warm_cache.py "
        "collects a copy of everything so the demonstration works without "
        "internet - and the demonstration itself then sends almost no "
        "requests to CSE.")
    return b


#=========================================================================#
#  VIVA                                                                   #
#=========================================================================#

def viva():
    return M.viva_chapter(
        MEMBER,
        tab_steps=[
            "Open the **Market Data** tab. Your name is on the label at the "
            "top.",
            "Press **Get the market data**. Point to the numbers across the "
            "top - the index, the number of companies, how many rose and "
            "fell - then scroll through the **Share prices** table.",
            "Open **The addresses we read the data from** below it. This is "
            "the list of CSE data addresses you use.",
            "Open the **Companies** tab. Press **Load the company list**, "
            "choose a company and press **Get details**.",
            "If there is time, show the Network tab in a real browser: open "
            "the CSE trade summary page, press F12, and point to the "
            "`tradeSummary` request.",
        ],
        commands=(
            "python -m src.api_client         # the data addresses\n"
            "python -m src.selenium_scraper   # a real browser (about 5 s)\n"
            "python warm_cache.py             # save a copy of everything"),
        script=(
            "My part is getting the data. The CSE page is built by "
            "JavaScript, so I opened it with F12 and watched the Network "
            "tab, and saw the page fetching its prices from addresses like "
            "api slash tradeSummary. Those return JSON, so my code asks "
            "those addresses directly - through Nuhan's fetch function, so "
            "the rules still apply - and turns each reply into a pandas "
            "table. One request gives us all 284 companies. I also wrote the "
            "Selenium version, which opens a real browser so the JavaScript "
            "runs. It works, but it is slower and only gets the first page "
            "of about 25 companies, so the API is our main method."),
        pointers=[
            ["`self.scraper.fetch(...)` in `call()`",
             "My requests go through Nuhan's fetch, so robots.txt, the delay "
             "and the log apply to them too."],
            ["`config.ENDPOINTS`", "The list of CSE data addresses, and "
                                   "whether each needs GET or POST. Most "
                                   "need POST - a GET gives an error."],
            ["`get_records()`", "Different addresses wrap their data "
                                "differently; this always hands back a plain "
                                "list."],
            ["`\"reqTradeSummery\"`", "CSE's own spelling. We must use their "
                                      "names exactly."],
            ["`data={\"symbol\": symbol}`", "This address needs to know the "
                                            "company, so we send the symbol "
                                            "as form data with the POST."],
            ["`/ 1000` in `to_datetime()`", "CSE sends milliseconds since "
                                            "1970; dividing by 1000 gives "
                                            "seconds, which Python turns "
                                            "into a date."],
            ["`WebDriverWait(...)`", "Waits until the table appears instead "
                                     "of guessing a sleep time."],
            ["`driver.page_source`", "The page after JavaScript ran - the "
                                     "reason Selenium finds the prices."],
        ])


#=========================================================================#
#  THE WHOLE DOCUMENT                                                     #
#=========================================================================#

WORDS = [
    ("API", "Application Programming Interface - an address a program can "
            "ask for data."),
    ("Database", "Where a website keeps all its information."),
    ("DOM", "The page as it is after JavaScript has run."),
    ("Driver", "A small program that passes Selenium's orders to a browser."),
    ("Endpoint", "One particular API address, such as tradeSummary."),
    ("Epoch time", "A moment stored as the number of milliseconds since 1 "
                   "January 1970."),
    ("Explicit wait", "Waiting until something appears on a page, instead "
                      "of for a fixed time."),
    ("Form data", "Values sent along with a POST request."),
    ("GET", "A request that just asks for something."),
    ("Headless", "Running a browser with no window."),
    ("Market cap", "A company's total value - share price times number of "
                   "shares."),
    ("Network tab", "The part of the browser's developer tools that lists "
                    "every request a page makes."),
    ("POST", "A request that sends some information along with it."),
    ("Selenium", "A tool that lets a program control a real web browser."),
    ("Symbol", "A company's short trading code, such as SAMP.N0000."),
    ("Turnover", "The total money that changed hands in a day."),
]


def build():
    b = []
    b += M.cover(MEMBER, "Getting the data from the site, and Selenium")
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
    b += file_api()
    b += E.page_break()
    b += file_selenium()
    b += E.page_break()
    b += file_config()
    b += E.page_break()
    b += M.big_picture(
        MEMBER, ["src/api_client.py"],
        ["Your part is step 2 and step 4. When the app wants data, it calls "
         "your `CSEApi`. Your `call()` passes the request to Nuhan's "
         "`fetch()` at step 3, and when the JSON comes back, your "
         "`make_dataframe()` turns it into the table at step 4. Every other "
         "part of the project - Sasini's crawler, the cleaning, the charts, "
         "the saved files - starts from the tables your code produces."])
    b += E.page_break()
    b += M.ethics_for_everyone()
    b += E.page_break()
    b += viva()
    b += E.page_break()
    b += M.practice_questions(MEMBER)
    b += E.page_break()
    b += M.word_list(WORDS)
    return b
