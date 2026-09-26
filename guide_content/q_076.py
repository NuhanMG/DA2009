"""
30 questions for 24ada076 - ethics and robots.txt, BeautifulSoup, PDFs.

Each entry is (level, question, answer) or (level, question, answer, code).
"""

Q_076 = [

#=========================================================================#
#  ETHICS AND ROBOTS.TXT                                                  #
#=========================================================================#

("Easy", "Which files did you write?",
 "`src/ethics.py`, which handles every request the project makes; "
 "`src/static_scraper.py`, the `requests` and BeautifulSoup part; and "
 "`src/pdf_extractor.py`, which reads the text out of the PDF documents."),

("Easy", "In one sentence, what does `src/ethics.py` do?",
 "It sends every web request the project makes, and applies the ethical "
 "rules to each one - checking robots.txt, waiting between requests, saying "
 "who we are, and writing everything to a log."),

("Easy", "Where does the project read robots.txt from?",
 "`https://www.cse.lk/robots.txt`. Every website keeps it at the top level "
 "of the site, at that exact name."),

("Easy", "How often do you read robots.txt?",
 "Once at the start of every run, in `read_robots()`. We do not keep a "
 "permanent copy, because a site can change its rules and an old copy would "
 "mean we were following permissions that had expired."),

("Easy", "What is a User-Agent?",
 "A short piece of text sent with every request that says what program is "
 "asking. Browsers send one that names the browser. Ours names the "
 "university, the course, the group and a contact email."),

("Medium", "Walk me through what happens when `fetch()` is called.",
 "Four steps, in this order.\n\n"
 "First it asks `can_fetch()` whether robots.txt allows that address. If "
 "not, it stops there and records the attempt as skipped. Second it calls "
 "`wait()`, which sleeps until 1.5 seconds have passed since the last "
 "request. Third it sends the request through the session, which carries "
 "our User-Agent. Fourth it writes a row to `logs/request_log.csv` and "
 "checks the status code before returning the data.",
 "def fetch(self, url, method=\"GET\", data=None, save_as=None, want=\"json\"):\n"
 "    allowed, reason = self.can_fetch(url)      # 1. permission\n"
 "    if not allowed:\n"
 "        return {\"ok\": False, ...}\n"
 "    self.wait()                                # 2. politeness\n"
 "    response = self.session.post(url, ...)     # 3. the request\n"
 "    self.log.log_request(method, url, ...)     # 4. the record"),

("Medium", "How does `can_fetch()` actually decide?",
 "It uses `RobotFileParser`, which is part of Python's standard library. We "
 "give it the text of robots.txt with `parse()`, then call "
 "`can_fetch(user_agent, url)` and it returns True or False. We did not "
 "write the rule matching ourselves - the standard library already knows "
 "the format."),

("Medium", "Why does `wait()` measure the time instead of always sleeping "
           "1.5 seconds?",
 "Because part of the delay may have passed already. If parsing the last "
 "reply took a second, we only need to wait another half second - the "
 "server still got its 1.5 seconds of breathing room either way. Sleeping "
 "the full amount every time would just make the program slower for no "
 "extra politeness.",
 "def wait(self):\n"
 "    since_last = time.time() - self.last_request_time\n"
 "    if since_last < self.delay:\n"
 "        time.sleep(self.delay - since_last)\n"
 "    self.last_request_time = time.time()"),

("Medium", "Why does `fetch()` return a dictionary instead of raising an "
           "error?",
 "Because it runs behind a web page. If an error were raised and not "
 "caught, it would stop the whole app and the screen would go blank. "
 "Returning `{\"ok\": False, \"error\": ...}` means the tab can show a "
 "readable message and everything else keeps working."),

("Medium", "What is a `requests.Session` and why use one?",
 "A Session keeps the connection to the server open between requests, "
 "instead of opening a new one each time. It saves the server a little work "
 "on every request, and it lets us set the User-Agent once instead of "
 "repeating it on every call."),

("Medium", "What is in `logs/request_log.csv`?",
 "One row for every request the project has ever sent: the time, whether it "
 "was GET or POST, the address, the status code that came back, whether "
 "robots.txt allowed it, and the delay we waited. It is the evidence for "
 "how the data was collected."),

("Medium", "What happens if robots.txt cannot be read at all?",
 "We treat every address as blocked. `can_fetch()` returns False with the "
 "reason that robots.txt could not be read. If we cannot see the rules we "
 "do not guess in our own favour - we stop."),

("Hard", "Somebody says the delay makes the project slow. Defend it.",
 "The slowness is the ethics working, not a fault.\n\n"
 "Collecting 15 company profiles takes about 25 seconds, and it could take "
 "under a second if we fired them all at once. Choosing not to is the whole "
 "point - it is the difference between behaving like a considerate visitor "
 "and behaving like a denial of service.\n\n"
 "It also costs us almost nothing in practice, because the main dataset "
 "arrives in a single request. The delay only shows when we deliberately "
 "loop over many companies."),

("Hard", "What did you deliberately choose not to do, and why?",
 "We did not use any technique for getting around a security control. No "
 "logins, no paywalls, and no CAPTCHA solving.\n\n"
 "We also did not rotate User-Agents or hide who we are. Plenty of scraping "
 "tutorials tell you to copy a browser's User-Agent so the site cannot tell "
 "you apart from a person. We do the opposite and name ourselves, because "
 "the point of the header is to identify the traffic, not to disguise it."),

("Hard", "How would you prove to the lecturer that you did not overload "
         "their server?",
 "By opening `logs/request_log.csv`. It has one row per request with a "
 "timestamp, so you can see the requests are spaced at least 1.5 seconds "
 "apart, and count them - roughly 30 to 40 for a full run.\n\n"
 "The Ethics tab in the app shows the same file on screen."),

#=========================================================================#
#  BEAUTIFULSOUP AND STATIC VS DYNAMIC                                    #
#=========================================================================#

("Easy", "What is BeautifulSoup?",
 "A Python library for pulling data out of HTML. You give it the HTML text, "
 "it works out the structure, and then you can ask it for tags, text or "
 "attributes by name."),

("Easy", "Which parser did you use with BeautifulSoup?",
 "`html.parser`, which comes with Python so nothing extra has to be "
 "installed. For the sitemap we use `xml` mode, which needs lxml, and the "
 "code falls back to `html.parser` if lxml is missing."),

("Easy", "What does `find()` do, and how is `find_all()` different?",
 "`find()` returns the first tag that matches. `find_all()` returns a list "
 "of every tag that matches."),

("Medium", "Go through the BeautifulSoup methods you used.",
 "`find()` for the first matching tag and `find_all()` for all of them. "
 "`select()` and `select_one()` do the same thing but with CSS selectors, "
 "which is handy for something like `div.price > span`. `get_text()` gives "
 "the words inside a tag, and `strip=True` removes the surrounding "
 "whitespace. `get()` reads one attribute, such as the `href` on a link.",
 "soup.find(\"title\")                 # first matching tag\n"
 "soup.find_all(\"a\")                 # every matching tag\n"
 "soup.select_one(\"div.price\")       # CSS selector\n"
 "tag.get_text(strip=True)           # the words inside\n"
 "tag.get(\"href\")                    # one attribute"),

("Medium", "What exactly did `requests` return for the CSE page?",
 "About 25,000 bytes of HTML, with a status code of 200 - so the request "
 "itself worked perfectly. But asking BeautifulSoup for the text gave about "
 "24 characters, and asking for tables gave none."),

("Medium", "How do you know the problem was the page and not your code?",
 "We pointed the same library, with the same methods, at CSE's sitemap - "
 "which is an ordinary file with no JavaScript - and it read all 15 pages "
 "listed without any trouble. Same tool, working result. That isolates the "
 "problem to the page."),

("Medium", "How would you tell whether a page is static or dynamic before "
           "writing any code?",
 "Right-click and choose View Page Source, which shows what the server "
 "actually sent. Then right-click and choose Inspect, which shows the page "
 "as it is now, after JavaScript has run.\n\n"
 "If the numbers appear in Inspect but not in View Source, the page is "
 "built by JavaScript and `requests` will not see them."),

("Hard", "Why did you keep code in the project that does not get the data?",
 "Because it explains the design. Without it, somebody reading the project "
 "would reasonably ask why we are not just using BeautifulSoup like "
 "everybody else.\n\n"
 "`src/static_scraper.py` answers that in one run: it shows the ordinary "
 "approach returning almost nothing on this particular site, and then shows "
 "the same library working fine on a normal file. It is the reasoning "
 "behind the whole project, written as code you can execute."),

("Hard", "If CSE were a normal static site, what would change?",
 "We would use `src/static_scraper.py` as the main collector instead of the "
 "API client. We would find the table in the HTML, loop over the `<tr>` "
 "rows, take the `<td>` cells with `get_text(strip=True)`, and build the "
 "DataFrame from those.\n\n"
 "The ethics layer, the cleaning, the PDF work and the charts would all "
 "stay exactly the same, because they do not care where the rows came "
 "from."),

#=========================================================================#
#  PDFs                                                                   #
#=========================================================================#

("Easy", "Which two libraries do you use to read PDFs?",
 "PyPDF2 and pdfplumber. We use both, because they are good at different "
 "things."),

("Easy", "What are the three types of PDF?",
 "Text based, made by a computer, where the letters are real text. Image "
 "based, which is a scan - a picture of the words with no text inside. And "
 "hybrid, which has some of each, such as a report with digital tables and "
 "a scanned diagram."),

("Medium", "What is the difference between PyPDF2 and pdfplumber?",
 "PyPDF2 is the simpler one. It extracts text and gives us the file details "
 "- the page count, the author, and what the file was created with. It does "
 "not keep the layout well and it cannot find tables.\n\n"
 "pdfplumber keeps the layout much better and can pull tables out using the "
 "position of the text on the page. That is why it is our main method, and "
 "we use PyPDF2 alongside it for the file details.",
 "# PyPDF2 - simple text and the file details\n"
 "reader = PdfReader(path)\n"
 "text = reader.pages[0].extract_text()\n"
 "details = reader.metadata\n\n"
 "# pdfplumber - layout and tables\n"
 "with pdfplumber.open(path) as pdf:\n"
 "    text = pdf.pages[0].extract_text()\n"
 "    tables = pdf.pages[0].extract_tables()"),

("Medium", "How does your code decide a PDF needs OCR?",
 "It counts the characters on each page. If a page gives fewer than 50, we "
 "treat it as a scan and mark it for OCR.\n\n"
 "We use 50 rather than zero because a scan sometimes carries a few stray "
 "characters that are not the real document text - a header added "
 "afterwards, for instance. Requiring a real amount of text means a handful "
 "of stray letters cannot fool us into skipping OCR."),

("Medium", "Why do you write `page.extract_text() or \"\"` instead of just "
           "`page.extract_text()`?",
 "Because `extract_text()` returns `None`, not an empty string, when there "
 "is nothing on the page. Calling `.strip()` or `len()` on `None` would "
 "crash. The `or \"\"` turns it into an empty string so the rest of the "
 "code can treat every page the same way."),

("Hard", "What makes extracting text from PDFs difficult in general?",
 "A PDF is a set of drawing instructions, not a document with a structure. "
 "It says where to put each character, not which paragraph it belongs to. "
 "So the library has to guess at things a human reads instantly.\n\n"
 "Tables are the worst case - they can span pages, have merged cells, and "
 "there is nothing in the file saying 'this is a table'. Line breaks are "
 "ambiguous, because a break at the edge of the page might be a new "
 "paragraph or just the line running out. Headers and footers repeat on "
 "every page and you may or may not want them. And formatting like bold, "
 "italics and ligatures often comes out wrong."),

]
