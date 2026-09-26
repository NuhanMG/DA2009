"""
The two speaker-note documents:

    docs/Speaker_Notes_Slides.pdf      presenting with docs/slides.pptx
    docs/Speaker_Notes_Live_Demo.pdf   Plan B - presenting the app live
"""

from reportlab.platypus import KeepTogether

import config
from guide_content import pdf_engine as E
from guide_content.slide_script import (OPENING, SLIDES, WORDS_PER_MINUTE,
                                        spoken_words)

SLIDE_IMAGES = config.ROOT_DIR / "guide_content" / "images" / "slides"
IMAGES = config.ROOT_DIR / "guide_content" / "images"

TEAM_LINE = ("25ada072 - Pasindu  |  25ada073 - Sasini  |  "
             "25ada141 - Salaama  |  24ada076 - Nuhan")


def clock(seconds):
    seconds = int(round(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


#=========================================================================#
#  1. THE SLIDES                                                          #
#=========================================================================#

def slide_timings():
    """Start time and length of each slide, from its number of words."""
    rows, start = [], 0.0
    for slide in SLIDES:
        length = spoken_words(slide) / WORDS_PER_MINUTE * 60
        rows.append((start, length))
        start += length
    return rows, start


def slides_notes():
    timings, total = slide_timings()
    b = []
    b += E.cover(
        "Speaker notes",
        "The presentation - docs/slides.pptx",
        [
            f"**9 slides, about {round(total / 60)} minutes**",
            "",
            "What to say on each slide, what to point at, and short answers "
            "to the questions each slide may bring up.",
            "",
            "**DA 2009 - Data Collection Methods II**",
            "Assignment 2 (Group Project)",
            "University of Colombo",
            "",
            TEAM_LINE,
        ])
    b += E.contents()

    #--- How it works ---------------------------------------------------#
    b += E.h1("How the presentation works")
    b += E.p(
        "The viva is 8 minutes for the whole team: about 3 minutes of "
        "presentation, then 5 minutes of questions on what each member did. "
        "Any number of us can present.")
    b += E.bullets([
        "**Slides 1 and 2** - Nuhan opens.",
        "**Slides 3 to 9** - any member who wants to present. The script is "
        "written so that anyone can read it.",
    ])

    rows = [["Slide", "Starts at", "Who", "Words"]]
    for i, (slide, (start, _)) in enumerate(zip(SLIDES, timings), 1):
        who = "Nuhan" if slide["who"] == OPENING else "Any member"
        rows.append([f"{i}. {slide['title']}", clock(start), who,
                     str(spoken_words(slide))])
    rows.append(["**End**", f"**{clock(total)}**", "", ""])
    b += E.table(rows, widths=[5.0, 1.3, 1.4, 0.8])
    b += E.p(
        f"The times assume a calm pace of about {WORDS_PER_MINUTE} words a "
        "minute. Speaking a little faster than that is fine; rushing is not.")

    b += E.h2("Sharing the slides between volunteers")
    b += E.table([
        ["Volunteers", "Suggested split after Nuhan's opening"],
        ["1", "Slides 3 to 9"],
        ["2", "Slides 3 to 5, then 6 to 9"],
        ["3", "Slides 3 and 4, then 5 and 6, then 7 to 9"],
    ], widths=[2.0, 6.5])
    b += E.p("When you hand over, keep it short - for example:")
    b += E.code(
        "\"Now Sasini will show how we found the documents.\"\n"
        "\"Over to Salaama for the scanned page.\"")
    b += E.remember(
        "the words on each slide are only reminders. Look at the audience, "
        "not the screen, and point at the part of the slide you are "
        "talking about.")

    #--- Before you start ----------------------------------------------#
    b += E.h1("Before you start")
    b += E.numbered([
        "Open `docs/slides.pptx` in PowerPoint on the laptop you will "
        "present from.",
        "On the **Slide Show** tab, tick **Use Presenter View**, then press "
        "**F5**. The audience sees the slide; your screen also shows these "
        "notes and a timer.",
        "Move with the arrow keys or a clicker. **Esc** ends the show.",
        "Practise out loud at least twice with a timer - once alone, and "
        "once with the whole team handing over to each other.",
        "Keep the app ready in the background (double-click "
        "`2_START_The_App.bat`), in case the examiner asks to see something "
        "running. The live demo notes list what to show for each member.",
    ])
    b += E.careful(
        "the numbers on the slides - 284 companies, 96 rose, 113 fell - are "
        "from one trading day, 25 September 2026. If you are asked, say "
        "that they change every day, and the app always shows the latest.")

    #--- The script -----------------------------------------------------#
    b += E.h1("The script, slide by slide")
    for i, (slide, (start, length)) in enumerate(zip(SLIDES, timings), 1):
        b += E.page_break() if i > 1 else []
        b += E.h2(f"Slide {i} - {slide['title']}")
        picture = SLIDE_IMAGES / f"Slide{i}.PNG"
        if picture.exists():
            b += E.image(picture, 9.5, None)
        who = "24ada076 - Nuhan" if slide["who"] == OPENING else "Any member"
        b += E.table([
            ["Time", f"{clock(start)} to {clock(start + length)} "
                     f"(about {round(length)} seconds)"],
            ["Who", who],
        ], widths=[1.6, 6.9], head=False)
        b += E.h3("Say")
        for para in slide["say"]:
            b += E.big(para)
        if slide.get("handover"):
            b += E.note(f"**{slide['handover']}**")
        b += E.h3("Point to")
        b += E.bullets(slide["point"])
        if slide["asked"]:
            b += E.h3("If you are asked")
            for question, answer in slide["asked"]:
                b += E.p(f"**{question}**")
                b += E.p(answer)

    #--- Questions ------------------------------------------------------#
    b += E.page_break()
    b += E.h1("After the slides - the questions")
    b += E.p(
        "The last 5 minutes are questions on what each member did. Each "
        "member's own document in `docs/member_documents` ends with 50 "
        "practice questions with answers - about 30 on their own part and 20 "
        "on the whole project.")
    b += E.bullets([
        "If a question is about someone else's part, it is fine to say "
        "'Pasindu wrote that part - Pasindu, would you like to answer?'",
        "If you do not know, say so, and say what you would check. That is "
        "better than guessing.",
        "Offer to show it: 'We can show you that running in the app.' The "
        "live demo notes list what to show for each member.",
    ])
    return b


#=========================================================================#
#  2. PLAN B - THE LIVE DEMO                                              #
#=========================================================================#

# One entry per stop on the route through the app.
STOPS = [
    {
        "title": "Home",
        "short": "Nothing",
        "time": "0:00",
        "who": "24ada076 - Nuhan",
        "press": "Nothing - the app is already open on the Home tab.",
        "wait": "-",
        "say": [
            "Good morning. I'm Nuhan, and this is our DA 2009 project: "
            "collecting data from the Colombo Stock Exchange. Instead of "
            "slides, we'll show you the system running live.",
            "Here's who built each part - Pasindu, Sasini, Salaama and me - "
            "and every tab is labelled with its member.",
        ],
        "point": ["The names in the title bar.",
                  "The **Who did what** table."],
        "change": True,
    },
    {
        "title": "Ethics",
        "short": "Read robots.txt",
        "time": "0:20",
        "who": "Any member",
        "press": "The **Ethics** tab, then **Read robots.txt**.",
        "wait": "1 to 2 seconds",
        "say": [
            "This is Nuhan's part, and it comes first. Before any request, "
            "the app reads CSE's robots.txt - it blocks just one folder, "
            "cgi-bin, which we never use.",
            "We wait 1.5 seconds between requests, though CSE doesn't ask us "
            "to, and our User-Agent says who we are. Every request we've "
            "ever sent is logged here.",
        ],
        "point": ["The `Disallow: /cgi-bin/` line in the robots.txt box.",
                  "**Our settings**: the delay and the User-Agent.",
                  "Scroll down to **Every request we have sent** - the "
                  "number of requests recorded."],
        "wrong": "If the robots.txt box is empty and Our settings says "
                 "'could not read robots.txt (no internet?)', there is no "
                 "internet. Say: \"There's no internet here, so the app "
                 "sends nothing at all and shows the copies we saved this "
                 "morning.\" Then carry on - every other stop still works.",
    },
    {
        "title": "Market Data",
        "short": "Get the market data",
        "time": "0:45",
        "who": "Any member",
        "press": "The **Market Data** tab, then **Get the market data**.",
        "wait": "about 8 seconds",
        "while": "\"It's waiting 1.5 seconds between each request - that's "
                 "the politeness rule working.\"",
        "say": [
            "This is Pasindu's part. The CSE page is built by JavaScript, so "
            "a plain download found only 24 characters of text.",
            "In the browser's Network tab we found the addresses the page "
            "itself uses, like tradeSummary. They send JSON, and pandas "
            "makes this table - every company from one request, plus the "
            "index, and how many rose and fell.",
        ],
        "point": ["The row of figures: ASPI index, companies, rose, fell.",
                  "The **Share prices** table.",
                  "Open **The addresses we read the data from** - each "
                  "address, and whether it is GET or POST.",
                  "The **Messages** box - one line per request, status 200."],
        "image": "app_market.png",
        "change": True,
    },
    {
        "title": "Announcements",
        "short": "Get the announcements, Download, Read the text",
        "time": "1:20",
        "who": "Any member",
        "press": "The **Announcements** tab, then **Get the announcements**. "
                 "Set **How many to download** to 3 and press **Download**. "
                 "Then scroll down and press **Read the text** (the first "
                 "document is already chosen).",
        "wait": "about 2 seconds for each button",
        "say": [
            "This is Sasini's crawler. It reads the list of circulars, finds "
            "each PDF on CSE's file server, and downloads a few at a time - "
            "ones we already have just say Already saved.",
            "Then Nuhan's reader opens a document: pdfplumber reads the text "
            "page by page, and PyPDF2 gives the file details. But one "
            "document is a scan, with no text at all.",
        ],
        "point": ["The **Downloaded** table - 'Already saved'.",
                  "**The documents we have** - the Type column says "
                  "'Scanned image' for the de-listing notice.",
                  "**Page by page** and **File details** after Read the "
                  "text."],
    },
    {
        "title": "OCR",
        "short": "Read it",
        "time": "1:55",
        "who": "Any member",
        "press": "The **OCR** tab. The de-listing notice (it starts with "
                 "14364) is chosen already. Leave **Image detail** at 200 "
                 "and press **Read it**.",
        "wait": "about 5 to 10 seconds",
        "while": "\"It's turning the page into an image at 200 dots per "
                 "inch.\"",
        "say": [
            "This is Salaama's OCR, in the four steps from the lecture. The "
            "page becomes an image, and OpenCV turns it grey, then pure "
            "black and white, so the letters have sharp edges.",
            "Tesseract reads the letters - here's the text - and gives each "
            "word a confidence score, so we know which words to check by "
            "hand.",
        ],
        "point": ["The three pictures, left to right.",
                  "**Text read from the image**.",
                  "**Least confident words** - the ones to check."],
        "wrong": "If the tab shows installation steps instead of pictures, "
                 "Tesseract is not installed on this laptop. Say so, and "
                 "show slide 7 of `docs/slides.pptx` instead.",
        "change": True,
    },
    {
        "title": "Data & Export",
        "short": "Clean and check, Draw the charts, Save",
        "time": "2:30",
        "who": "Any member",
        "press": "The **Data & Export** tab, then **Clean and check**, then "
                 "**Draw the charts**, then **Save**.",
        "wait": "about 1 second for each button",
        "say": [
            "Website data is never ready to use. Sasini's cleaning turns "
            "dates from huge numbers into Sri Lanka time, and the checks "
            "confirm there are no negative prices and no company twice.",
            "Salaama's charts show the biggest movers, turnover and sectors. "
            "Save writes CSV, Excel and JSON, with CSE credited inside every "
            "file.",
        ],
        "point": ["**Before and after** - Date columns go from 0 to 1.",
                  "**Checks** - every row says OK.",
                  "The three charts.",
                  "**Files saved so far**."],
        "wrong": "If it says 'Get the market data first', the Market Data "
                 "button was not pressed - go back one stop and press it.",
    },
    {
        "title": "Closing",
        "short": "Nothing",
        "time": "2:55",
        "who": "Any member, or Nuhan",
        "press": "Nothing. (You can click back to **Home**.)",
        "wait": "-",
        "say": [
            "That's the whole system, running live. Thank you - we're happy "
            "to take questions, and we can show any part in more detail.",
        ],
        "point": [],
    },
]

# What to show for each member if the examiner asks.
EXTRAS = [
    ("24ada076 - Nuhan", "Ethical scraping, BeautifulSoup and PDFs", [
        ("The request log",
         "**Ethics** tab, **Show the request log**.",
         "Every request we have sent: the time, the address, the status and "
         "the delay we waited."),
        ("The ethics code",
         "VS Code: `src/ethics.py`, the `fetch()` function.",
         "One function for every request: check robots.txt, wait, send, "
         "record - and use a saved copy if the internet fails."),
        ("The plain download",
         "`4_Run_Each_Members_Part.bat`, option **2**.",
         "requests and BeautifulSoup get 17,898 bytes of HTML but only 24 "
         "characters of text and no tables - the page is built by "
         "JavaScript."),
        ("The PDF reader",
         "`4_Run_Each_Members_Part.bat`, option **3**.",
         "Every saved PDF, page by page: text-based, scanned or hybrid."),
    ]),
    ("25ada072 - Pasindu", "Getting the data, and Selenium", [
        ("One company",
         "**Companies** tab, **Load the company list**, choose "
         "`SAMP.N0000 - SAMPATH BANK PLC`, **Get details**.",
         "This address needs the company symbol sent with a POST request. "
         "It shows the price, market value, and the year's high and low."),
        ("Several companies",
         "Same tab: set **How many companies** to 5, **Collect them**.",
         "It takes several seconds because every company is a separate "
         "request, and each one waits 1.5 seconds first."),
        ("The addresses",
         "**Market Data** tab, **The addresses we read the data from**.",
         "Every CSE address we use, and whether it is GET or POST."),
        ("Selenium",
         "`4_Run_Each_Members_Part.bat`, option **5**.",
         "Opens a hidden Edge browser, waits for the JavaScript, and finds "
         "the table - but it takes about 5 seconds for one page."),
    ]),
    ("25ada073 - Sasini", "Crawling for documents, and cleaning", [
        ("The Scrapy spider",
         "Double-click `6_Run_The_Scrapy_Spider.bat`.",
         "The same crawl done with Scrapy. At the end, "
         "`robotstxt/request_count` shows it read robots.txt first, and "
         "`item_scraped_count` how many documents it found."),
        ("The crawler code",
         "VS Code: `src/crawler.py`, `download_documents()`.",
         "It skips files we already have, and checks the first four bytes "
         "say %PDF before saving."),
        ("The cleaning",
         "**Data & Export** tab, **Before and after**, then "
         "`src/cleaner.py`, step 1.",
         "Dates arrive as milliseconds in UTC; we turn them into Sri Lanka "
         "time, so trades show between 09:30 and 14:30."),
    ]),
    ("25ada141 - Salaama", "OCR, saving the files, and the charts", [
        ("OCR detail",
         "**OCR** tab: move **Image detail** to 100, then 300, pressing "
         "**Read it** each time.",
         "Fewer dots per inch is faster but blurrier; more is sharper but "
         "slower. 200 is the balance we chose."),
        ("The source inside a file",
         "File Explorer: `data\\exports`, open the newest "
         "`cse_share_prices_...csv` in Notepad.",
         "The first lines start with # and credit the Colombo Stock "
         "Exchange. In the Excel file, it is the second sheet, Source."),
        ("The charts",
         "**Data & Export** tab: hover over any bar.",
         "Each bar shows its exact value. Green up, red down - and every "
         "bar also says up or down, so colour is never the only clue."),
    ]),
]


def demo_notes():
    b = []
    b += E.cover(
        "Speaker notes",
        "Plan B - presenting the system live",
        [
            "**About 3 minutes, straight through the app**",
            "",
            "Nuhan runs the app on his laptop and shares the screen. The "
            "team talks through each tab while it works live.",
            "",
            "**DA 2009 - Data Collection Methods II**",
            "Assignment 2 (Group Project)",
            "University of Colombo",
            "",
            TEAM_LINE,
        ])
    b += E.contents()

    #--- The plan on one page ------------------------------------------#
    b += E.h1("Plan B on one page")
    b += E.p(
        "Instead of slides, we show the system itself. Nuhan opens and "
        "clicks every button from start to finish. Whoever volunteers does "
        "the talking - the script marks where a new speaker can take over. "
        "If only one person volunteers, they read it all.")
    rows = [["Time", "Tab", "What to press", "Who"]]
    for stop in STOPS:
        rows.append([stop["time"], f"**{stop['title']}**", stop["short"],
                     stop["who"]])
    b += E.table(rows, widths=[1.0, 2.0, 4.0, 1.5])
    b += E.remember(
        "keep talking while a page loads. A few seconds of silence feels "
        "long; saying 'it's waiting 1.5 seconds between requests - that's our "
        "politeness rule' turns the wait into a point in our favour.")
    b += E.p(
        "**Plan A or Plan B?** The live demo proves the system works and is "
        "the best way to show how it is built, but it needs the laptop, the "
        "projector and ideally the internet. The slides are the safe "
        "choice. Keep `docs/slides.pptx` open in the background either way, "
        "so you can switch if something fails.")

    #--- Getting ready --------------------------------------------------#
    b += E.h1("Getting ready")
    b += E.h2("The day before")
    b += E.numbered([
        "If the project has never been set up on this laptop, double-click "
        "`1_SETUP_First_Time_Only.bat` and press **Y** when it asks about "
        "Tesseract.",
        "Start the app and open the **OCR** tab. The line at the top must "
        "say that Tesseract is installed and ready - otherwise the OCR stop "
        "will not work.",
        "Walk through the whole route below twice, with a timer, with the "
        "people who will speak.",
    ])
    b += E.h2("On the morning of the viva")
    b += E.numbered([
        "With internet, double-click `3_Collect_Fresh_Data.bat`. It takes "
        "about 1 to 2 minutes. It saves a fresh copy of every reply and "
        "downloads any new documents. If the internet fails during the "
        "viva, the app shows these copies instead.",
    ])
    b += E.h2("Ten minutes before")
    b += E.numbered([
        "Double-click `2_START_The_App.bat`. The browser opens the app by "
        "itself at `http://127.0.0.1:7860`. Keep the black window open - "
        "make it small, but do not close it.",
        "Press **Light theme** at the top right - it is easier to read on a "
        "projector.",
        "Zoom the browser to about 110% (**Ctrl** and **+**) so the back of "
        "the room can read it.",
        "Close other browser tabs and turn on **Do not disturb**, so no "
        "messages pop up while you share.",
        "Have these open in the background for the questions: VS Code with "
        "the project, File Explorer at `data\\exports`, and "
        "`docs/slides.pptx`.",
        "Leave the app on the **Home** tab. Do not press any buttons yet - "
        "the demo shows them working for the first time.",
    ])
    b += E.careful(
        "the numbers on screen - the number of companies, the index, how "
        "many rose and fell - change every trading day. On a weekend or a "
        "holiday the market is closed and the app shows the last trading "
        "day. Say what you see, not what these notes say.")

    #--- The route ------------------------------------------------------#
    b += E.h1("The live script")
    b += E.p(
        "Seven stops, about 3 minutes. For each stop: what Nuhan presses, "
        "how long it takes, what the speaker says, and what to point at.")
    for n, stop in enumerate(STOPS, 1):
        # Each stop is kept on one page, so nobody turns a page mid-stop.
        part = []
        part += E.h2(f"Stop {n} - {stop['title']}  ({stop['time']})")
        part += E.table([
            ["Who speaks", stop["who"]],
            ["Nuhan presses", stop["press"]],
            ["Wait", stop["wait"]],
        ], widths=[2.3, 6.2], head=False)
        if stop.get("while"):
            part += E.p(f"**While it loads, say:** {stop['while']}")
        part += E.h3("Say")
        for para in stop["say"]:
            part += E.big(para)
        if stop["point"]:
            part += E.h3("Point to")
            part += E.bullets(stop["point"])
        if stop.get("image"):
            part += E.image(IMAGES / stop["image"], 14,
                            "What the Market Data tab looks like after the "
                            "button is pressed (light theme).")
        if stop.get("wrong"):
            part += E.careful(stop["wrong"])
        if stop.get("change"):
            part += E.note("**A new speaker can take over here.**")
        b.append(KeepTogether(part))

    #--- Extras ---------------------------------------------------------#
    b += E.page_break()
    b += E.h1("Extras for the questions")
    b += E.p(
        "The 5 minutes of questions are on what each member did. These are "
        "ready-made things to show when a question comes up. Nothing here "
        "is part of the 3 minutes.")
    b += E.p(
        "`4_Run_Each_Members_Part.bat` opens a menu that runs any member's "
        "file on its own and prints what it does:")
    b += E.table([
        ["Member", "Menu options"],
        ["24ada076 - Nuhan", "1 Ethics   2 Static scraper   3 PDF reader"],
        ["25ada072 - Pasindu", "4 API client   5 Selenium"],
        ["25ada073 - Sasini", "6 Crawler   7 Cleaner   8 Scrapy spider"],
        ["25ada141 - Salaama", "9 OCR   10 Storage   11 Analysis"],
    ], widths=[3.0, 5.5])
    b += E.p("Options 3 and 9 need some PDFs, so run option 6 first on a "
             "new computer.")
    for member, part, items in EXTRAS:
        b += E.h2(f"{member} - {part}")
        for name, how, say in items:
            b += E.p(f"**{name}.** {how}")
            b += E.p(f"Say: {say}")

    #--- Problems -------------------------------------------------------#
    b += E.page_break()
    b += E.h1("If something goes wrong")
    b += E.table([
        ["What happens", "What to do"],
        ["**No internet.** The robots.txt box is empty, and the Messages "
         "box says 'Using the saved copy of ... instead'.",
         "Keep going - every tab works from the copies saved that morning. "
         "Say: \"There's no internet here, so the app sends nothing and "
         "shows the copies we saved earlier.\" New documents cannot be "
         "downloaded; the ones we have say 'Already saved'."],
        ["**Slow internet.** A button seems stuck.",
         "Keep talking. Each request gives up after 30 seconds, and the "
         "Messages box shows what is happening."],
        ["**OCR shows installation steps.**",
         "Tesseract is not installed. Say so, and show slide 7 of "
         "`docs/slides.pptx` instead."],
        ["**A table stays empty, or a red error appears.**",
         "Press the button once more. If it still fails, move on: \"This "
         "part talks to the live website, which does not always answer.\""],
        ["**'Get the market data first'** on the Data & Export tab.",
         "The Market Data button was skipped. Go back, press it, return."],
        ["**The page will not load, or the black window was closed.**",
         "Double-click `2_START_The_App.bat` again. If the app is still "
         "running, it just opens the browser."],
        ["**Everything fails.**",
         "Switch to Plan A: open `docs/slides.pptx` and press F5."],
    ], widths=[3.4, 5.1])
    return b
