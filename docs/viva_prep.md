# Viva Notes

**Format:** 8 minutes per team — about 3 minutes presenting, then 5 minutes of
questions on what each member did.

Read your own section until you can say it without looking. Then read the last
section, because anybody can be asked anything.

---

## The 3 minute presentation

One person can do this, or split it between two.

> "We were given the Colombo Stock Exchange, and we collect three things from
> it: share prices, company details, and announcements.
>
> We started with `requests` and BeautifulSoup, the way we were taught. That
> gave us about 25,000 bytes of HTML with almost no words in it and no tables.
> The reason is that CSE builds its pages with JavaScript, and `requests` only
> downloads the HTML file — it does not run the JavaScript.
>
> So we opened the site in a browser and looked at the Network tab, and we
> could see the page loading its data from addresses like
> `/api/tradeSummary`. Those return JSON, which pandas reads directly, and one
> request gives us every company at once. That is what the project uses.
>
> Announcements have PDF documents attached. Most of them we read with
> pdfplumber. One of them gave us nothing at all, because it is a scan — a
> photograph of a printed page. For that one we used OCR: we turn the page
> into an image, clean it up with OpenCV, and read it with pytesseract.
>
> On the ethics side, every request in the project goes through one function.
> It checks robots.txt, waits one and a half seconds, and writes a line to a
> log file. We can show you every request we have sent."

---

## 24ada076 - Nuhan — ethical scraping, BeautifulSoup, and PDFs

*Files: `src/ethics.py`, `src/static_scraper.py`, `src/pdf_extractor.py`*

### Ethical scraping and robots.txt

**What does your ethics file do?**
Every request in the project goes through one function, `Scraper.fetch()`. It
checks robots.txt for that address, waits 1.5 seconds, sends the request with
our User-Agent, and writes a row to `logs/request_log.csv`. Doing it in one
place means the rules are applied every time instead of being repeated in
every file.

**What is robots.txt?**
A file websites publish at the top level telling automated programs which
pages they may visit. It is a voluntary guideline, not a lock — anyone *can*
ignore it. We follow it because that is what ethical scraping means.

**What does CSE's robots.txt say?**
It blocks one section, `/cgi-bin/`, and allows everything else. There is no
`Crawl-delay`, so it does not ask us to wait at all. We wait 1.5 seconds
anyway, because being allowed to go fast is not a reason to.

**How do you check an address against it?**
`RobotFileParser` comes with Python. We give it the text of robots.txt, then
call `can_fetch()` with our User-Agent and the address. It returns True or
False.

**Why does your User-Agent say who you are?**
Most scrapers copy a browser's User-Agent so they look like an ordinary
visitor. Ours gives the university, the course and an email address, so if our
requests ever caused a problem the site administrator could get in touch.

**What do the HTTP status codes mean?**
200 is success. 403 means we are not allowed. 404 means the page does not
exist. 500 means the server had a problem. We check for 200 and report
anything else instead of retrying.

**How much load did you put on their server?**
Around 30 to 40 requests for a full run, at least 1.5 seconds apart. Every one
is in `logs/request_log.csv`.

### BeautifulSoup and static vs dynamic content

**Why does `requests` find nothing on the CSE page?**
Because the page is dynamic, not static. `requests` downloads the HTML file
and stops; it does not run any JavaScript. CSE sends a nearly empty page and
the browser fills in the prices afterwards, so there is nothing in the file
for BeautifulSoup to find — about 24 characters of text and no tables.

**How do you know BeautifulSoup was not the problem?**
We used the same library on CSE's sitemap, which is an ordinary file with no
JavaScript, and it read all 15 pages listed with no trouble. So the library
works; the page just had nothing in it.

**How can you tell a page is like this before writing any code?**
Right-click and View Page Source shows what the server sent. Right-click and
Inspect shows what the page looks like now, after JavaScript has run. If the
numbers appear in Inspect but not in View Source, the page is built by
JavaScript.

**Which BeautifulSoup methods did you use?**
`find()` for the first match, `find_all()` for all of them, `select()` and
`select_one()` for CSS selectors, `get_text(strip=True)` for the words inside
a tag, and `get()` for an attribute such as `href`. `src/static_scraper.py`
runs each of them and prints what it returned.

**What parser did you use and why?**
`html.parser`, which comes with Python, so nothing extra has to be installed.
For the sitemap we use `xml` mode, which needs lxml, and we fall back to
`html.parser` if lxml is missing.

### Reading PDFs

**What is the difference between PyPDF2 and pdfplumber?**
PyPDF2 is the simpler one. It extracts text and gives us the file details —
page count, author, what the file was made with. It does not keep the layout
well and cannot find tables. pdfplumber keeps the layout better and can
extract tables, so it is our main method. We use both.

**What are the types of PDF?**
Text based, made by a computer, where the letters are real text. Image based,
which is a scan — a picture of the words, with no text inside. And hybrid,
which has both.

**Why does a scanned PDF give no text?**
A PDF is a set of drawing instructions, not a text file. If somebody printed a
page, signed it and scanned it, what is inside the file is a photograph. There
is no text in it to extract, so any library returns nothing.

**How does the code decide a PDF needs OCR?**
If a page gives fewer than 50 characters we treat it as a scan. We use 50
rather than zero because a scan sometimes carries a few stray characters that
are not the real document text.

**What makes PDF extraction difficult in general?**
Tables that span pages or have merged cells, deciding whether a line break is
a real paragraph break, headers and footers you may or may not want, and
formatting like bold or ligatures that often comes out wrong.

---

## 25ada072 - Pasindu — getting the data, and Selenium

*Files: `src/api_client.py`, `src/selenium_scraper.py`, `config.py`,
`warm_cache.py`*

**What is an API?**
A way for one program to ask another for data. You send a request and get a
reply back, usually as JSON. A website has one so its own pages can load data,
and often so other developers can use it too.

**How did you find the addresses CSE uses?**
We opened the CSE site in a browser, pressed F12, opened the Network tab and
reloaded the page. The list showed the page requesting its own data from
`/api/tradeSummary` and similar addresses.

**Why is using them acceptable?**
They need no login or key — it is the same request the page makes for any
visitor. robots.txt does not block them. And it is less work for CSE's server
than loading the whole page, because loading the page makes them send the
HTML, the JavaScript, the fonts and the images, and the browser then requests
that same data address anyway.

**Why POST and not GET?**
Most of the CSE addresses only answer POST requests. A GET returns an error.
We found that by trying it.

**How does the JSON become a DataFrame?**
Some addresses return a plain list of records, and others wrap the list inside
a dictionary under a name like `reqTradeSummery`. `get_records()` handles both
shapes, then `pd.DataFrame()` turns the list of dictionaries into a table.

**What are the limitations of using an API?**
Rate limits, needing a key for some of them, only giving you part of the data
the site holds, and the fact that it can change without warning. Ours are not
officially documented, so CSE could change them at any time.

**How does Selenium fix the JavaScript problem?**
Selenium controls a real browser, so the JavaScript runs and the table is
actually there. We then take `driver.page_source`, which is the page after
JavaScript, and give that to BeautifulSoup as normal.

**Why is Selenium not the main method?**
It takes several seconds instead of one, it makes CSE serve the whole page,
and the table on screen is split across pages so one load only gives about 25
companies. The data address gives all of them in one request.

**What is `WebDriverWait` for?**
When the browser first opens the page the table does not exist yet, because
JavaScript is still fetching the data. `WebDriverWait` pauses until the table
appears, instead of guessing a `sleep` time.

**Why the `try` / `finally`?**
So `driver.quit()` always runs. If it does not, the browser keeps running in
the background using memory.

---

## 25ada073 - Sasini — crawling, and cleaning the data

*Files: `src/crawler.py`, `src/cleaner.py`, `scrapy_project/`*

**What is the difference between scraping and crawling?**
Scraping is taking data from a page you already know about. Crawling is
finding pages by following links. Most of our project is scraping, because we
know the address. My part is crawling: we do not know which documents exist,
so we read the list of circulars, work out each PDF address, and follow them.

**How did you work out the PDF addresses?**
The list only gives part of the address, like
`upload_report_file/abc123.pdf`. The PDFs are kept on a different server from
the website, so we tried the likely addresses until one returned a real PDF —
`https://cdn.cse.lk/cmt/` followed by that path.

**Why limit the number of downloads?**
There are far more documents on the site than we need. Downloading all of them
just because we could would put load on their server for no reason.

**How do you check a downloaded file is really a PDF?**
Every PDF file begins with the characters `%PDF`. We check the first four
bytes before saving it, so an error page does not get saved as a PDF.

**Explain the Scrapy spider.**
`start()` sends POST requests to the two announcement addresses, because CSE
does not answer GET. `parse()` reads the JSON, builds each PDF address, and
yields a new request for it — that is the crawling step. `parse_document()`
records what came back. It uses HEAD rather than GET, so we confirm the file
exists without downloading it.

**Which Scrapy settings keep it polite?**
`ROBOTSTXT_OBEY = True`, `DOWNLOAD_DELAY = 1.5`,
`CONCURRENT_REQUESTS = 1` instead of the default 8, AutoThrottle to slow down
further if the server struggles, and `CLOSESPIDER_ITEMCOUNT = 40`.

**What had to be cleaned in the CSE data?**
Four things. Dates arrive as very large numbers like `1786440420412`, which is
milliseconds since 1970 — left alone pandas treats them as ordinary numbers.
Some numbers arrive as text, which sorts alphabetically so "9" comes after
"100". Some columns are empty for every company. And text has extra spaces
around it, so grouping creates two groups that look the same.

**How do you avoid converting a column by mistake?**
Two checks. The column name has to contain something like "date" or "time",
and the values have to be larger than a trillion, which any real date in
milliseconds will be. Both have to be true before we convert it.

**What is the difference between cleaning and checking?**
Cleaning fixes the shape of the data — the types, the empty columns, the
duplicates. Checking asks whether the values make sense. A share price of -5
rupees would be perfectly tidy and still completely wrong, so we check for
negative prices, movements over 100%, missing symbols and duplicates.

---

## 25ada141 - Salaama — OCR, saving the files, and the charts

*Files: `src/ocr_extractor.py`, `src/storage.py`, `src/analysis.py`*

**What is OCR?**
Optical Character Recognition — turning a picture of text into text the
computer can use. We needed it because one of the CSE circulars is a scan and
gave us no text at all.

**What are the four steps?**
1. **Image acquisition** — turn the PDF page into an image
2. **Preprocessing** — OpenCV converts it to grey, then to pure black and
   white. The lecture's optional noise step follows; at its 1x1 setting it
   changes nothing, which is worth knowing if asked
3. **Text recognition** — pytesseract reads the letters
4. **Post-processing** — pandas tidies the text into lines and saves it

**Why convert to grey and then to black and white?**
Colour tells us nothing about which letter something is, and removing it
leaves one brightness value per pixel instead of three. Thresholding then
makes every pixel either black or white, so the letters have hard edges, which
is what Tesseract reads best. We use adaptive thresholding, which works out
the cut-off separately for each part of the page — useful on a scan where one
side is darker than the other.

**What does the dpi setting change?**
How large the image is. At 72 dpi small print becomes unreadable. We use 200,
which is enough for a printed document. 300 is better for very small print but
takes longer.

**How do you know whether Tesseract is actually installed?**
Importing `pytesseract` is not enough — the Python package imports fine even
when the Tesseract program is missing. So we call
`pytesseract.get_tesseract_version()`, which makes it look for the program. If
that fails, we know it is not installed.

**Is OCR accurate?**
Not completely. It runs words together and misreads logos as letters. We use
`image_to_data` to get a confidence score for every word, so we can see which
ones are worth checking by hand.

**What else can go wrong with OCR?**
Poor quality scans, complicated layouts with columns and tables, handwriting,
unusual fonts, and pages that are slightly rotated. Most of those are helped
by better preprocessing.

**How does the source get into the exported files?**
Each file type needs a different method. CSV gets comment lines at the top
starting with `#`, which pandas can skip with `pd.read_csv(path, comment="#")`.
Excel gets a second sheet called Source. JSON gets a details section above the
records.

**Why does that matter?**
A spreadsheet passed on to somebody else with no source attached is how data
gets misused. Putting the credit inside the file means it travels with the
data.

**Why green and red on the charts?**
It is the usual convention for share prices. Because red and green are hard to
tell apart for some people, every bar also shows the direction in words and a
plus or minus sign, so the colour is never the only clue.

---

## Questions anybody might get

**Is web scraping legal?**
It depends on the data, the website's terms, and what you do with it. We kept
to the safe side: only public company information, no personal data, robots.txt
followed, no security measure bypassed, the source credited, and academic use
only.

**Did you have to get past any CAPTCHAs or logins?**
No. Everything we collect is visible without logging in, and we never met a
CAPTCHA because we never behaved in a way that would set one off.

**What would break this project?**
CSE changing the addresses their site uses. They are not officially
documented, so they could change at any time. All the addresses are in
`config.py`, so it would be a small fix, and we save a copy of the data so a
demonstration still works.

**What would you do differently?**
Collect on several days instead of one, so we could show how prices change
over time rather than a single snapshot.

---

## Numbers worth remembering

| | |
|---|---|
| Words `requests` found on the CSE page | about 24 characters, no tables |
| Companies from one request | around 290 |
| Delay between our requests | 1.5 seconds |
| Section blocked by robots.txt | `/cgi-bin/` only |
| PDF libraries used | PyPDF2 and pdfplumber |
| OCR steps | image, preprocess, recognise, tidy |
| OCR resolution | 200 dpi |
| Threshold for deciding a page is a scan | under 50 characters |
