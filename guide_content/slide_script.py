"""
The spoken script for docs/slides.pptx - one entry per slide.

This one file feeds both the speaker notes inside the slides and the
speaker notes PDF, so the two always say the same thing.

    who     who says it
    say     the words, one string per paragraph
    point   what to point at on the slide
    asked   likely questions about this slide, with short answers
"""

OPENING = "24ada076 - Nuhan (opening)"
ANYONE = "Any member"

SLIDES = [
    {
        "title": "Collecting data from the Colombo Stock Exchange",
        "who": OPENING,
        "say": [
            "Good morning. I'm Nuhan, and this is our DA 2009 group project: "
            "collecting data from the Colombo Stock Exchange website. Our "
            "group is Pasindu, Sasini, Salaama and me.",
            "I'll open, and my teammates will explain how it works.",
        ],
        "point": ["The four names on the slide as you say them."],
        "asked": [],
    },
    {
        "title": "What we collect",
        "who": OPENING,
        "say": [
            "We collect three kinds of public data: share prices for every "
            "listed company, details for each company, and company "
            "announcements, many of them as PDF files. No logins, and nothing "
            "personal.",
            "It all runs in this app, with one tab for each step. But our "
            "first attempt found almost nothing - here's why.",
        ],
        "point": ["The three numbered items.",
                  "The app screenshot when you say 'this app'."],
        "asked": [
            ("Why the Colombo Stock Exchange?",
             "It was the website our group was given. It is a good test "
             "because it has live data, company records and PDF documents - "
             "so it needed several different collection methods."),
        ],
        "handover": "Hand over to the next speaker.",
    },
    {
        "title": "The surprise: the page is built by JavaScript",
        "who": ANYONE,
        "say": [
            "We started as the course taught us, with requests and "
            "BeautifulSoup. The trade summary page gave just 24 characters "
            "of text and no tables.",
            "CSE builds its pages with JavaScript, and requests never runs it. "
            "Selenium, a real browser, did see the table - but took over five "
            "seconds a page.",
        ],
        "point": ["The red 24 on the left.",
                  "The table in the browser picture on the right."],
        "asked": [
            ("Why not just use Selenium for everything?",
             "It works, but it is slow - over five seconds a page - and it "
             "loads the whole page with its pictures and scripts, which puts "
             "more load on CSE. Reading the data addresses directly is faster "
             "and lighter."),
            ("What is a dynamic page?",
             "A page whose content is added by JavaScript after it arrives. "
             "A plain download only gets the empty page."),
        ],
    },
    {
        "title": "The answer: read the data the page itself uses",
        "who": ANYONE,
        "say": [
            "We pressed F12 and watched the Network tab. The page gets its "
            "prices from addresses like api/tradeSummary, which answer in "
            "JSON.",
            "We ask those addresses directly - most only answer POST - and "
            "pandas turns the JSON into a table. One request gives all 284 "
            "companies; company details come one at a time, by symbol.",
        ],
        "point": ["The four steps, left to right.",
                  "The JSON record, then the big 284."],
        "asked": [
            ("Is it allowed to use those addresses?",
             "They are public - the page itself uses them for every visitor, "
             "with no login - and robots.txt does not block them. We still "
             "wait 1.5 seconds between requests and say who we are."),
            ("What is the difference between GET and POST?",
             "GET just asks for something. POST sends information along with "
             "the request, like a filled-in form. Most CSE addresses only "
             "answer POST."),
        ],
    },
    {
        "title": "Ethics: every request goes through one function",
        "who": ANYONE,
        "say": [
            "Ethics is a main part of the marks, so every request goes "
            "through one function.",
            "It checks robots.txt - CSE only blocks cgi-bin, which we never "
            "use. It waits 1.5 seconds, though CSE doesn't ask us to, says who "
            "we are, logs every request, and keeps a copy so we never ask "
            "twice.",
        ],
        "point": ["The five numbered steps.",
                  "The Disallow: /cgi-bin/ line in the robots.txt box."],
        "asked": [
            ("Why wait 1.5 seconds if robots.txt doesn't ask for a delay?",
             "Being allowed to go fast is not a reason to. Sending requests "
             "as fast as possible would put load on their server for no "
             "benefit to us."),
            ("Can you show the requests you sent?",
             "Yes - every one is in logs/request_log.csv, and the Ethics tab "
             "of the app shows it."),
        ],
    },
    {
        "title": "Announcements: finding and reading the PDFs",
        "who": ANYONE,
        "say": [
            "Our crawler reads the list of circulars, finds each PDF on CSE's "
            "file server, and downloads a few at a time, skipping copies. A "
            "Scrapy spider does the same crawl, also obeying robots.txt.",
            "pdfplumber reads the text, PyPDF2 the file details - but one PDF "
            "was a scan, with no text inside.",
        ],
        "point": ["The three steps of the crawler.",
                  "The red 0 on the Scanned card."],
        "asked": [
            ("What is the difference between scraping and crawling?",
             "Scraping takes data from a page you already know about. "
             "Crawling finds pages or files by following links. We did not "
             "know which documents existed, so we crawled for them."),
            ("How do you know a download is really a PDF?",
             "Every PDF file starts with the characters %PDF. The crawler "
             "checks the first four bytes before saving anything."),
        ],
    },
    {
        "title": "OCR: reading a scanned page",
        "who": ANYONE,
        "say": [
            "For scans we use OCR, in the lecture's four steps. pdfplumber "
            "makes an image, OpenCV turns it grey and then pure black and "
            "white - you can see the difference here - pytesseract reads the "
            "letters, and pandas tidies the result.",
            "Every word gets a confidence score, so we know which to check "
            "by hand.",
        ],
        "point": ["The four steps.",
                  "The two pictures - before, and after cleaning."],
        "asked": [
            ("Why make the image black and white first?",
             "Tesseract reads best with plain black letters on a white "
             "background. We use adaptive thresholding, which picks a "
             "separate cut-off for each small area, so uneven lighting does "
             "not spoil it."),
            ("Is OCR always right?",
             "No. Letters like O and 0, or l and 1, get mixed up, and logos "
             "confuse it. That is why we show the least confident words, so "
             "a person can check them."),
        ],
    },
    {
        "title": "Clean, check, chart and save",
        "who": ANYONE,
        "say": [
            "Website data is never ready to use. We turn dates from huge "
            "numbers into Sri Lanka time, and check the values make sense - "
            "all six checks passed.",
            "The app draws three charts - movers, turnover and sectors. On "
            "this day 96 companies rose, 113 fell and 75 didn't "
            "move. We save CSV, Excel and JSON, crediting CSE in every file.",
        ],
        "point": ["The chart as you say the three numbers.",
                  "The four steps on the right."],
        "asked": [
            ("What is the difference between cleaning and checking?",
             "Cleaning fixes the shape - dates, number types, spaces, empty "
             "columns. Checking asks whether the values are believable - a "
             "negative price would be tidy but wrong."),
            ("How is the source credited in the files?",
             "Comment lines at the top of the CSV, a second sheet called "
             "Source in the Excel file, and a details section in the JSON."),
        ],
    },
    {
        "title": "Who did what",
        "who": ANYONE,
        "say": [
            "That's who built each part - every tab in the app is labelled "
            "with its member, and we built the app together.",
            "Thank you. We're happy to take questions, and we can show any "
            "part of it running in the app.",
        ],
        "point": ["Each card as you name the member."],
        "asked": [],
    },
]

# Spoken words per minute used for the timings. A calm, clear pace.
WORDS_PER_MINUTE = 145


def spoken_words(slide):
    return sum(len(p.split()) for p in slide["say"])


def notes_text(slide, number):
    """The text that goes into the slide's speaker notes."""
    parts = []
    if slide["who"] == OPENING:
        parts.append(f"PRESENTED BY: {OPENING}")
    elif number == 3:
        parts.append("(From here, any member can present.)")
    parts += slide["say"]
    if slide.get("handover"):
        parts.append(f"({slide['handover']})")
    return "\n\n".join(parts)


if __name__ == "__main__":
    # Writes the notes for the slide builder, and prints the timing.
    import json
    import sys

    notes = {str(i): notes_text(s, i) for i, s in enumerate(SLIDES, 1)}
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=2)
    total = sum(spoken_words(s) for s in SLIDES)
    print(f"{total} words - about {total / WORDS_PER_MINUTE:.1f} minutes")
