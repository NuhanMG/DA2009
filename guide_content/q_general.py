"""
The 20 general questions. Every member gets these, because any of them
could be asked of anybody.

Each entry is (level, question, answer).
"""

GENERAL = [

#--- Easy ----------------------------------------------------------------#

("Easy", "What is web scraping?",
 "Collecting data from websites automatically with a program, instead of "
 "copying it by hand. You send a request for a page, get the content back, "
 "find the parts you want, and save them in a structured form such as a CSV "
 "file."),

("Easy", "What website did your group work on, and what did you collect?",
 "The Colombo Stock Exchange, `www.cse.lk`. We collect share prices for "
 "around 290 listed companies, details for individual companies such as "
 "market value and yearly high and low, and company announcements together "
 "with the PDF documents attached to them."),

("Easy", "Is the data you collected public?",
 "Yes. Everything we collect can be seen by anybody visiting the site "
 "without logging in. CSE publishes it so the investing public can read it. "
 "We collect no personal information about any individual - only company "
 "figures."),

("Easy", "What is robots.txt?",
 "A text file websites publish at the top level of the site telling "
 "automated programs which pages they may and may not visit. It is a "
 "voluntary guideline, not a lock - a program can ignore it. Ethical "
 "scrapers choose to follow it."),

("Easy", "What does CSE's robots.txt say?",
 "It blocks one section, `/cgi-bin/`, and allows everything else. It does "
 "not set a `Crawl-delay`, so it does not ask us to wait between requests "
 "at all."),

("Easy", "If the site does not ask you to wait, why do you wait?",
 "Because being allowed to go fast is not a reason to. Sending requests as "
 "fast as the computer can manage would put load on their server and gain "
 "us nothing. We wait 1.5 seconds between requests."),

("Easy", "What does the HTTP status code 200 mean?",
 "The request worked. 403 means we are not allowed, 404 means the page does "
 "not exist, and 500 means the server had a problem."),

("Easy", "What is a DataFrame?",
 "A table in pandas, with rows and named columns, a bit like a sheet in "
 "Excel. Almost everything we collect ends up in one, because it makes the "
 "data easy to sort, filter and save."),

#--- Medium --------------------------------------------------------------#

("Medium", "Why did `requests` and BeautifulSoup not work on the CSE site?",
 "Because the page is dynamic. `requests` downloads the HTML file and stops "
 "- it does not run JavaScript. The CSE server sends an almost empty page, "
 "and a program inside the browser fetches the prices and puts them on the "
 "page afterwards. So the file we download has about 24 characters of text "
 "in it and no tables."),

("Medium", "What is the difference between static and dynamic content?",
 "On a static page the content is already inside the HTML file the server "
 "sends, so downloading the file is enough. On a dynamic page the file "
 "arrives nearly empty and JavaScript fills it in afterwards, so you need "
 "either a real browser or the address the page gets its data from."),

("Medium", "How did you find the addresses the site uses for its data?",
 "We opened the CSE site in a browser, pressed F12 to open the developer "
 "tools, went to the Network tab, and reloaded the page. That tab lists "
 "every request the page makes, and it showed the page fetching its own "
 "data from addresses like `/api/tradeSummary`."),

("Medium", "What is JSON, and why is it convenient here?",
 "JSON is a structured text format for data, made of names and values. It "
 "is convenient because it is already organised - pandas can turn it "
 "straight into a table, with no need to hunt through HTML tags for the "
 "numbers."),

("Medium", "How does your project make sure the ethical rules are followed?",
 "Every request in the whole project goes through one function, "
 "`Scraper.fetch()` in `src/ethics.py`. That function checks robots.txt, "
 "waits the delay, sends the request with our User-Agent, and writes a line "
 "to the log. Because there is only one way out to the internet, the rules "
 "cannot be skipped by accident in some other file."),

("Medium", "What does your User-Agent say, and why does that matter?",
 "It gives the university, the course, the group and an email address, "
 "instead of pretending to be an ordinary browser. If our requests ever "
 "caused a problem, the site administrator could see who was responsible "
 "and get in touch."),

("Medium", "How much load did you put on CSE's servers?",
 "Around 30 to 40 requests for a full run of the app, spaced at least 1.5 "
 "seconds apart. Every one is recorded in `logs/request_log.csv`. Somebody "
 "browsing the same pages by hand would actually generate more traffic, "
 "because each page load also pulls scripts, fonts and images that we never "
 "request."),

("Medium", "Why are there two kinds of PDF in the project?",
 "A text based PDF was made by a computer, so the letters inside it are "
 "real text and we can read them straight out. A scanned PDF is a "
 "photograph of a printed page - the words are part of a picture, so there "
 "is no text inside to extract and it has to go through OCR instead."),

#--- Hard ----------------------------------------------------------------#

("Hard", "Is web scraping legal?",
 "It is not automatically legal or illegal - it depends on the data, the "
 "website's terms, and what you do with the result.\n\n"
 "We stayed well on the safe side: only public company information, no "
 "personal data, robots.txt followed, no security measure bypassed, the "
 "source credited in every file, and academic use only. We also did not ask "
 "CSE for written permission, which would be the right next step if we "
 "wanted to publish or sell anything based on this."),

("Hard", "Is it acceptable to use an address that is not officially "
         "documented?",
 "We think so, for three reasons.\n\n"
 "It needs no login and no key, so it is exactly the same request the page "
 "makes for any visitor. `robots.txt` does not ask us to stay away from it. "
 "And it is actually less work for their server than loading the whole "
 "page, because loading the page makes them send the HTML, the JavaScript, "
 "the fonts and the images, and the browser then requests that same data "
 "address at the end of it anyway.\n\n"
 "The honest limitation is that an undocumented address can change without "
 "warning, and that is CSE's right."),

("Hard", "Did you get past any CAPTCHAs or logins?",
 "No, and we would not. Everything we collect is visible without logging "
 "in, and we never met a CAPTCHA because we never behaved in a way that "
 "would set one off.\n\n"
 "A CAPTCHA is a website asking whether you are a person. Getting around "
 "one means answering yes when the honest answer is no. Being able to "
 "defeat a control is not the same as being allowed to."),

("Hard", "What would break this project, and how bad would it be?",
 "CSE changing the addresses their site uses to load data. They are not "
 "officially documented, so they could change at any time without notice.\n\n"
 "It would not be a disaster. Every address is listed in one place, in "
 "`config.py`, so fixing it means editing that table rather than hunting "
 "through the whole project. We also save a copy of every reply, so a "
 "demonstration still works from the saved data even if the live site has "
 "changed."),

]
