"""
Chapters shared by the four member documents.

Each function returns finished PDF blocks. The member files
(member_nuhan.py and so on) call these and add their own chapters.
"""

import config
from guide_content import pdf_engine as E

IMG = config.ROOT_DIR / "guide_content" / "images"


def label(member):
    return config.member_label(member)


#=========================================================================#
#  COVER                                                                  #
#=========================================================================#

def cover(member, part_title):
    return E.cover(
        "CSE Web Data Collection",
        f"Document for {label(member)}",
        [
            f"**Your part: {part_title}**",
            "",
            "Everything behind your part of the project - the ideas, the "
            "reasons, and the code - explained step by step, from the "
            "beginning.",
            "",
            "**DA 2009 - Data Collection Methods II**",
            "Assignment 2 (Group Project)",
            "University of Colombo",
            "",
            "25ada072 - Pasindu  |  25ada073 - Sasini  |  "
            "25ada141 - Salaama  |  24ada076 - Nuhan",
        ])


#=========================================================================#
#  HOW TO USE THIS DOCUMENT                                               #
#=========================================================================#

def how_to_use(member, files):
    b = []
    b += E.h1("How to use this document")

    b += E.p(
        "This document explains your part of the project from the very "
        "beginning. It does not assume you have seen any of it before. Each "
        "chapter builds on the one before it, so read it in order the first "
        "time.")

    b += E.p("Your files are:")
    b += E.bullets([f"`{f}`" for f in files])

    b += E.p("You will see four kinds of coloured box:")
    b += E.idea(
        "a comparison with something from everyday life, to make a new "
        "idea easier to picture.")
    b += E.remember(
        "the one thing to take away from a section. If you only read the "
        "green boxes, you will still know the main points.")
    b += E.careful(
        "a trap, or something an examiner might test you on.")
    b += E.tryit("something to type on the computer, and what should happen.")

    b += E.p(
        "Grey boxes in a typewriter font are **code** - real lines copied "
        "from our project files, not made-up examples.")

    b += E.h2("A plan for the week before the viva")
    b += E.table([
        ["Day", "What to do"],
        ["1", "Read chapters 1 to 3. They explain the project and the ideas "
              "behind your part."],
        ["2", "Read the chapter on reading Python, with your own files open "
              "beside it."],
        ["3 and 4", "Read the chapters on your files, one at a time. Run "
                    "each file as the 'Try it yourself' boxes show."],
        ["5", "Read how your part fits into the whole project, and the "
              "ethics chapter."],
        ["6", "Practise the viva chapter out loud - say your 30-second "
              "explanation until it feels natural."],
        ["7", "Go through the practice questions at the end. Cover the "
              "answer and try to say it first."],
    ], widths=[1.3, 7.2])
    return b


#=========================================================================#
#  THE PROJECT IN SIMPLE WORDS                                            #
#=========================================================================#

def the_project(member):
    b = []
    b += E.h1("The project in simple words")

    b += E.h2("What a stock exchange is")
    b += E.p(
        "A company can split its ownership into many small pieces called "
        "**shares**. If you buy one share of a bank, you own a tiny piece of "
        "that bank.")
    b += E.p(
        "A **stock exchange** is the marketplace where people buy and sell "
        "those shares. The price of a share goes up when many people want "
        "to buy it, and down when many people want to sell it. The "
        "**Colombo Stock Exchange** - CSE for short - is Sri Lanka's stock "
        "exchange, and its website is `www.cse.lk`.")
    b += E.idea(
        "a stock exchange is like a big weekly fair where, instead of "
        "vegetables, people trade small pieces of companies. The website is "
        "the notice board at the entrance that shows today's prices.")

    b += E.h2("What we were asked to do")
    b += E.p(
        "Our group was given the CSE website and asked to collect data from "
        "it with a computer program, using the methods taught in the course, "
        "and to do it **ethically** - politely, legally, and without causing "
        "the website any trouble.")

    b += E.h2("What we collect")
    b += E.table([
        ["What", "What it means", "Example"],
        ["Share prices", "What every company traded at today",
         "Sampath Bank: Rs 141.00"],
        ["Company details", "Facts about one company",
         "Its total value, its highest and lowest price this year"],
        ["Announcements", "Notices companies publish, often as PDF files",
         "'A dividend will be paid', 'A meeting will be held'"],
    ], widths=[1.8, 3.2, 3.5])

    b += E.p(
        "After collecting, we tidy the data, check it makes sense, draw "
        "charts, and save it as files that other people can open.")

    b += E.h2("Who did what")
    rows = [["Member", "Part of the project"]]
    for m in ["24ada076", "25ada072", "25ada073", "25ada141"]:
        mark = "  (this is you)" if m == member else ""
        rows.append([f"**{label(m)}**{mark}", config.OWNERSHIP[m]["role"]])
    b += E.table(rows, widths=[3.0, 5.5])
    b += E.p(
        "The app itself (`app.py`) was put together by all four of us. Each "
        "tab in the app is labelled with the member whose part it shows.")

    b += E.h2("The one surprise that shaped the whole project")
    b += E.p(
        "The first thing we tried was the ordinary method from the course: "
        "download the web page and pick the prices out of it. It found "
        "almost nothing - about 24 letters of text, and no tables at all.")
    b += E.p(
        "The reason is that the CSE website is built with **JavaScript**. "
        "The page arrives nearly empty, and a small program inside your "
        "browser then fetches the prices and fills them in. A plain "
        "download never runs that program, so it never sees the prices.")
    b += E.p(
        "So we opened the site in a browser, pressed **F12**, and watched "
        "the **Network** tab, which lists everything the page asks for. It "
        "showed the page fetching its prices from addresses such as "
        "`https://www.cse.lk/api/tradeSummary`. We read those addresses "
        "directly instead, and one request gives us every company at once.")
    b += E.remember(
        "the CSE page is built by JavaScript, so we read the data from the "
        "same addresses the page itself uses. That one decision explains "
        "why the project is built the way it is.")
    return b


#=========================================================================#
#  HOW THE WEB WORKS - the basics everybody needs                         #
#=========================================================================#

def web_basics():
    b = []
    b += E.h1("How the web works")

    b += E.p(
        "Before looking at any code, it helps to understand what actually "
        "happens when a computer 'visits' a website. There are only a few "
        "ideas, and every part of our project uses them.")

    b += E.h2("Requests and responses")
    b += E.p(
        "When you open a web page, your computer sends a message to another "
        "computer, called a **server**, asking for that page. This message "
        "is a **request**. The server sends something back - the page, a "
        "file, or some data. That is the **response**.")
    b += E.idea(
        "writing a letter and getting a reply. You write to an address and "
        "ask for something. A little later, a reply arrives in your "
        "letterbox. Every single thing a website shows you - each picture, "
        "each price - arrives this way, one letter and one reply at a time.")

    b += E.h2("Addresses - URLs")
    b += E.p(
        "Every page and file on the web has an address, called a **URL**. "
        "For example:")
    b += E.code("https://www.cse.lk/api/tradeSummary")
    b += E.table([
        ["Part", "What it means"],
        ["`https://`", "How to talk to the server. The 's' means the "
                       "conversation is locked so nobody can read it on the "
                       "way."],
        ["`www.cse.lk`", "Which server - the CSE website."],
        ["`/api/tradeSummary`", "Which thing on that server we want. This "
                                "part is called the **path**."],
    ], widths=[2.6, 5.9])

    b += E.h2("GET and POST - two ways of asking")
    b += E.p(
        "There are two common kinds of request. A **GET** request simply "
        "asks for something: 'please give me this page'. A **POST** request "
        "sends some information along with the question, like filling in a "
        "form before handing it over.")
    b += E.p(
        "Most of the CSE data addresses only answer **POST** requests - if "
        "you send a GET, they reply with an error. That is their rule, not "
        "ours, and we found it by trying both.")

    b += E.h2("Status codes - the result stamped on every reply")
    b += E.p(
        "Every response comes with a three-digit number that says how it "
        "went. These were taught in Week 2:")
    b += E.table([
        ["Code", "Meaning", "In everyday words"],
        ["200", "OK", "Here is what you asked for."],
        ["301", "Moved Permanently", "That has moved - look over there."],
        ["403", "Forbidden", "You are not allowed to have this."],
        ["404", "Not Found", "There is no such page."],
        ["500", "Internal Server Error", "Something broke on our side."],
    ], widths=[1.0, 2.8, 4.7])

    b += E.h2("Headers - the envelope")
    b += E.p(
        "Along with every request travel a few lines of extra information "
        "called **headers**. One of them, the **User-Agent**, says what "
        "program is asking. A browser sends something like 'Chrome on "
        "Windows'. Our project sends its own name, the university, the "
        "course, and an email address.")
    b += E.idea(
        "the User-Agent is like writing your name and address on the back "
        "of the envelope. The receiver knows who wrote, and can write back "
        "if there is a problem.")

    b += E.h2("HTML - what a web page is made of")
    b += E.p(
        "A web page is a text file written in **HTML**. It uses **tags** - "
        "words inside angle brackets - to label each part of the page:")
    b += E.code(
        "<html>\n"
        "  <head>\n"
        "    <title>Trade Summary</title>\n"
        "  </head>\n"
        "  <body>\n"
        "    <h1>Today's prices</h1>\n"
        "    <table>\n"
        "      <tr> <th>Company</th> <th>Price</th> </tr>\n"
        "      <tr> <td>Sampath Bank</td> <td>141.00</td> </tr>\n"
        "    </table>\n"
        "  </body>\n"
        "</html>")
    b += E.p(
        "Tags usually come in pairs: `<title>` opens and `</title>` closes. "
        "Whatever sits between them is the content. Tags sit inside other "
        "tags, like boxes inside boxes: the table is inside the body, each "
        "row `<tr>` is inside the table, and each cell `<td>` is inside a "
        "row.")

    b += E.h2("JSON - data in a tidy shape")
    b += E.p(
        "Websites do not only send pages. They also send plain **data**, and "
        "the most common format for that is **JSON**. JSON is made of "
        "**names and values**, grouped with curly brackets `{ }`, and lists "
        "grouped with square brackets `[ ]`. This is a real piece of what "
        "CSE sends us:")
    b += E.code(
        '{\n'
        '  "symbol": "SAMP.N0000",\n'
        '  "name": "SAMPATH BANK PLC",\n'
        '  "price": 141.0,\n'
        '  "change": 1.0\n'
        '}')
    b += E.idea(
        "JSON is like a neatly filled-in form. Every box has a label "
        "('name', 'price') and an answer. A program can read it straight "
        "away, with no need to search through the decorations of a web "
        "page.")

    b += E.h2("Static and dynamic pages")
    b += E.table([
        ["", "Static page", "Dynamic page"],
        ["Where the content is", "Already written inside the HTML file",
         "Added by JavaScript after the page arrives"],
        ["Can a plain download see it?", "Yes", "No"],
        ["Example", "A list of university departments", "CSE's live prices"],
    ], widths=[2.6, 2.9, 3.0])
    b += E.idea(
        "a static page is a printed menu - everything is already on it. A "
        "dynamic page is an empty chalkboard; a waiter writes today's "
        "specials on it after you sit down. If you take a photo the moment "
        "you walk in, you photograph an empty board.")
    b += E.tryit(
        "open `https://www.cse.lk/equity/trade-summary` in Chrome or Edge. "
        "Right-click and choose **View Page Source** - this shows what the "
        "server sent, and you will not find the prices in it. Now "
        "right-click a price and choose **Inspect** - this shows the page "
        "after JavaScript ran, and the prices are there.")
    return b


#=========================================================================#
#  READING PYTHON - shared explanations, filled with each member's code   #
#=========================================================================#

# Each concept: (heading, general explanation, everyday comparison or None)
PY_CONCEPTS = {
    "comment": (
        "Comments - notes for people",
        "A line that starts with `#` is a **comment**. Python ignores it "
        "completely. It is there for people reading the code. Our files are "
        "full of comments explaining why each part exists.",
        None),
    "variable": (
        "Variables - labelled boxes",
        "A **variable** is a name that holds a value. The `=` sign means "
        "'put the thing on the right into the box on the left'. It does not "
        "mean 'equals' the way it does in maths.",
        "a variable is a labelled box. `price = 141.0` means: take a box, "
        "write 'price' on the label, and put 141.0 inside."),
    "text": (
        "Text, and filling in blanks with f-strings",
        "Text in Python is written inside quote marks, like `\"hello\"`. It "
        "is called a **string**. A string that starts with `f` is an "
        "**f-string**: anything inside curly brackets `{ }` is replaced "
        "with the value of that variable.",
        "an f-string is a form letter with blanks. `f\"Dear {name}\"` fills "
        "in the blank with whatever `name` holds."),
    "numbers": (
        "Numbers, and True and False",
        "Python has whole numbers like `30`, numbers with a decimal point "
        "like `1.5`, and two special values: `True` and `False`. `None` "
        "means 'nothing here yet'.",
        None),
    "list": (
        "Lists - things in order",
        "A **list** holds several values in order, inside square brackets. "
        "`.append()` adds one more to the end. `[]` on its own is an empty "
        "list, ready to be filled.",
        "a list is a numbered shopping list. You can add items to the end, "
        "and read them back in order."),
    "dict": (
        "Dictionaries - values with labels",
        "A **dictionary** holds values under names, inside curly brackets: "
        "`{\"name\": value}`. You get a value back by its name: "
        "`reply[\"ok\"]`. The method `.get(name, default)` does the same, "
        "but gives back the default instead of crashing if the name is "
        "missing.",
        "a dictionary is a set of labelled drawers. You open a drawer by "
        "reading its label, not by counting from the top."),
    "function": (
        "Functions - recipes",
        "A **function** is a named set of steps. `def` starts one. The names "
        "in brackets are its **parameters** - the ingredients it needs. "
        "`return` hands back the result. The function does nothing until "
        "somebody **calls** it by writing its name followed by brackets.",
        "a function is a recipe. The parameters are the ingredients, the "
        "indented lines are the steps, and `return` is the finished dish."),
    "if": (
        "if and else - making decisions",
        "`if` runs the indented lines only when a condition is true. `else` "
        "runs when it is not. `not` turns true into false and the other way "
        "round.",
        None),
    "for": (
        "for loops - doing the same thing for each item",
        "A **for loop** repeats its indented lines once for every item in a "
        "list or table. `enumerate(..., start=1)` also counts them for you: "
        "1, 2, 3.",
        "a for loop is a teacher going down the register, doing the same "
        "thing for each name."),
    "import": (
        "import - taking a toolbox off the shelf",
        "Python comes with some tools built in. For everything else we "
        "**import** a library - a toolbox somebody else wrote. "
        "`import pandas as pd` means 'load pandas, and let me call it pd for "
        "short'. `from X import Y` takes just one tool out of the box.",
        None),
    "try": (
        "try and except - a safety net",
        "Code inside `try` is attempted. If anything goes wrong, Python "
        "jumps to `except` instead of crashing. We use this wherever the "
        "internet or a file might fail.",
        "try and except is a trapeze artist with a safety net. They attempt "
        "the jump; if they fall, the net catches them and the show goes on."),
    "with": (
        "with - borrow, use, and give back automatically",
        "`with` opens something - usually a file - for the indented lines "
        "that follow, and closes it again afterwards, even if something "
        "goes wrong in the middle.",
        "borrowing a library book with a promise that it is returned "
        "automatically, even if you forget."),
    "class": (
        "Classes, objects and self",
        "A **class** is a design for making things that hold both "
        "information and actions. The thing you make from the design is an "
        "**object**. Functions written inside a class are called "
        "**methods**. `__init__` is the special method that runs once, when "
        "the object is first made - it sets it up. Inside a class, **self** "
        "means 'this particular object'.",
        "a class is a cake tin, and each object is a cake made from it. "
        "`self` means 'this cake' - so `self.delay` is this cake's own "
        "delay, not somebody else's."),
    "pandas": (
        "pandas DataFrames - tables in Python",
        "A **DataFrame** is a table with rows and named columns, like a "
        "sheet in Excel. pandas is the library that provides it. "
        "`pd.DataFrame(rows)` builds one from a list of dictionaries, "
        "`df.head(5)` shows the first five rows, and `df[\"price\"]` picks "
        "out one column.",
        None),
}


def python_chapter(member, examples, intro_file, extras=None):
    """
    The 'reading Python' chapter.

    examples: {concept: (code copied from the member's file, explanation)}
    extras:   extra (heading, text, code, explanation) sections that only
              this member's files need.
    """
    b = []
    b += E.h1("Reading Python")
    b += E.p(
        "To explain your code, you first need to be able to read it. This "
        "chapter explains every piece of Python that appears in your files. "
        "Every example is a real line from your own code, so by the end of "
        "the chapter you will recognise all of it.")
    b += E.tryit(
        f"open `{intro_file}` in VS Code or Notepad and keep it beside this "
        f"document while you read. Find each example in the file as you go.")

    for concept, (heading, text, comparison) in PY_CONCEPTS.items():
        if concept not in examples:
            continue
        example, explanation = examples[concept]
        b += E.h2(heading)
        b += E.p(text)
        if comparison:
            b += E.idea(comparison)
        b += E.p("From your code:")
        b += E.code(example)
        b += E.p(explanation)

    for heading, text, example, explanation in (extras or []):
        b += E.h2(heading)
        b += E.p(text)
        if example:
            b += E.code(example)
        if explanation:
            b += E.p(explanation)

    b += E.h2("Running a file")
    b += E.p(
        "Every file in our project can be run on its own to show what it "
        "does. You open a terminal in the project folder, switch on the "
        "project's Python, and ask Python to run the file:")
    b += E.code(
        "cd D:\\DA2009\\CSE-Scraping-Project\n"
        ".venv\\Scripts\\activate\n"
        "python -m src.ethics")
    b += E.p(
        "`.venv` is the project's own copy of Python with all the libraries "
        "installed. `-m src.ethics` means 'run the file `ethics.py` inside "
        "the `src` folder'. The part at the bottom of each file that starts "
        "`if __name__ == \"__main__\":` is what runs when you do this.")
    return b


#=========================================================================#
#  THE WHOLE PIPELINE, WITH THIS MEMBER'S PART MARKED                     #
#=========================================================================#

def big_picture(member, marked_lines, words):
    b = []
    b += E.h1("How your part fits into the whole project")
    b += E.p(
        "Every button in the app follows the same path. The lines marked "
        "`<-- YOU` are yours.")

    steps = [
        ("1. You click a button in the app", "app.py"),
        ("2. The app asks for some data", "src/api_client.py"),
        ("3. Every request goes through fetch()", "src/ethics.py"),
        ("     a. check robots.txt", "src/ethics.py"),
        ("     b. wait 1.5 seconds", "src/ethics.py"),
        ("     c. send it, saying who we are", "src/ethics.py"),
        ("     d. write it in the request log", "src/ethics.py"),
        ("4. The reply (JSON) becomes a table", "src/api_client.py"),
        ("5. Documents are found and downloaded", "src/crawler.py"),
        ("6. Their text is read", "src/pdf_extractor.py"),
        ("7. Scanned pages are read by OCR", "src/ocr_extractor.py"),
        ("8. The table is tidied and checked", "src/cleaner.py"),
        ("9. Charts are drawn", "src/analysis.py"),
        ("10. Files are saved (CSV, Excel, JSON)", "src/storage.py"),
    ]
    lines = []
    for text, file in steps:
        mark = "   <-- YOU" if file in marked_lines else ""
        lines.append(f"{text:44} {file:22}{mark}")
    b += E.code("\n".join(lines))

    b += E.p(
        "Two more pieces sit beside this path rather than on it: "
        "`src/static_scraper.py` shows the ordinary requests-and-"
        "BeautifulSoup method, and `src/selenium_scraper.py` shows the "
        "real-browser method. The Scrapy spider in `scrapy_project/` does "
        "the document search a second way, with the Scrapy framework.")
    for para in words:
        b += E.p(para)
    return b


#=========================================================================#
#  ETHICS - EVERY MEMBER NEEDS TO KNOW THIS                               #
#=========================================================================#

def ethics_for_everyone():
    b = []
    b += E.h1("Ethics - what every member must know")
    b += E.p(
        "The assignment says marks are given for **following ethical "
        "scraping practices** and for **being able to explain your work**. "
        "Ethics was Nuhan's file, but any of us can be asked about it, so "
        "here is the short version.")

    b += E.h2("Ethical and unethical scraping")
    b += E.table([
        ["Ethical (what we do)", "Unethical (what we avoid)"],
        ["Only collect what anyone can see without logging in",
         "Getting past logins, paywalls or CAPTCHAs"],
        ["Follow the website's robots.txt", "Ignoring robots.txt"],
        ["Wait between requests", "Firing requests as fast as possible"],
        ["Collect no personal information", "Collecting data about people"],
        ["Credit the source", "Using the data without saying where it came "
                              "from"],
    ], widths=[4.25, 4.25])

    b += E.h2("robots.txt")
    b += E.p(
        "**robots.txt** is a small file a website publishes to tell programs "
        "like ours which parts they may visit. CSE's says:")
    b += E.code(
        "User-agent: *\n"
        "Disallow:\n"
        "Disallow: /cgi-bin/\n"
        "Sitemap: https://www.cse.lk/sitemap.xml")
    b += E.p(
        "`User-agent: *` means the rules are for every program. The next two "
        "lines ask programs to keep out of one folder, `/cgi-bin/`. None of "
        "the addresses we use are in that folder. There is no line asking "
        "us to wait between requests.")
    b += E.idea(
        "robots.txt is a sign on a shop door that says 'Staff only beyond "
        "this point'. Nothing physically stops you walking past it - you "
        "stay out because you respect it.")

    b += E.h2("What our code does about it")
    b += E.numbered([
        "Every request goes through one function, `fetch()` in "
        "`src/ethics.py`. It checks robots.txt first.",
        "It waits **1.5 seconds** between requests, even though CSE does not "
        "ask us to.",
        "It sends a **User-Agent** with our university, course and email.",
        "It writes every request to `logs/request_log.csv`.",
        "It saves a copy of each reply so we never ask twice.",
        "Every exported file names the **Colombo Stock Exchange** as the "
        "source.",
    ])
    b += E.remember(
        "'We only collect public data, we follow robots.txt, we wait 1.5 "
        "seconds between requests, we say who we are, and we credit CSE in "
        "every file we save.' If you are asked about ethics, start with "
        "that sentence.")
    return b


#=========================================================================#
#  THE VIVA                                                               #
#=========================================================================#

def viva_chapter(member, tab_steps, commands, script, pointers):
    b = []
    b += E.h1("Showing your part in the viva")
    b += E.p(
        "The viva is 8 minutes for the whole team: about 3 minutes of "
        "presentation, then 5 minutes of questions about what each member "
        "did. This chapter gets you ready for your share of it.")

    b += E.h2("Before the viva")
    b += E.numbered([
        "Double-click `Run_CSE_App.bat` in the project folder. The app opens "
        "in your browser. Keep the black window open - closing it stops the "
        "app.",
        "Check your tab works, as below.",
        "Run your files once from the terminal, so you have seen the output "
        "yourself.",
    ])

    b += E.h2("Showing it in the app")
    b += E.numbered(tab_steps)

    b += E.h2("Showing it from the terminal")
    b += E.code(commands)

    b += E.h2("Your 30-second explanation")
    b += E.p("Practise saying this out loud until it feels natural. Change "
             "the words so they sound like you.")
    b += E.big('"' + script + '"')

    b += E.h2("If the examiner points at your code")
    b += E.p("These are the parts of your files most likely to be pointed "
             "at, and what to say about each:")
    b += E.table([["If they point at...", "Say..."]] + pointers,
                 widths=[3.2, 5.3])
    return b


#=========================================================================#
#  WORD LIST                                                              #
#=========================================================================#

COMMON_WORDS = [
    ("URL", "The address of a page or file on the web."),
    ("Request", "A message asking a server for something."),
    ("Response", "The server's reply to a request."),
    ("Server", "A computer that stores a website and answers requests."),
    ("Status code", "A number on each reply saying how it went - 200 means OK."),
    ("HTML", "The language web pages are written in, using tags."),
    ("Tag", "A label in HTML, such as <title> or <table>."),
    ("JSON", "A tidy text format for data: names and values."),
    ("JavaScript", "A language that runs inside the browser and can change "
                   "the page after it loads."),
    ("Static page", "A page whose content is already in the HTML file."),
    ("Dynamic page", "A page whose content is added by JavaScript later."),
    ("robots.txt", "A file where a website says which parts programs may "
                   "visit."),
    ("User-Agent", "The part of a request that says which program sent it."),
    ("Library", "Code somebody else wrote that we can import and use."),
    ("DataFrame", "A table in pandas, with rows and named columns."),
    ("Function", "A named set of steps that can be called to do a job."),
    ("Variable", "A name that holds a value."),
    ("CSV", "A simple table file: one row per line, commas between columns."),
    ("PDF", "A document file that looks the same on every computer."),
    ("Share", "A small piece of a company that people can buy and sell."),
]


def word_list(extra_words):
    b = []
    b += E.h1("Word list")
    b += E.p("Every special word used in this document, from A to Z.")
    b += E.glossary(COMMON_WORDS + list(extra_words))
    return b


#=========================================================================#
#  PRACTICE QUESTIONS - the same 50 as in the team guide                  #
#=========================================================================#

def practice_questions(member):
    from guide_content.q_072 import Q_072
    from guide_content.q_073 import Q_073
    from guide_content.q_076 import Q_076
    from guide_content.q_141 import Q_141
    from guide_content.q_general import GENERAL

    own = {"24ada076": Q_076, "25ada072": Q_072,
           "25ada073": Q_073, "25ada141": Q_141}[member]

    b = []
    b += E.h1("Practice questions")
    b += E.p(
        "These are the same 50 questions as your section of the team guide: "
        "about 30 on your own part, then 20 on the project as a whole. "
        "Cover each answer with your hand and try to say it first. By now, "
        "every answer should make sense - if one does not, go back to the "
        "chapter it comes from.")

    number = 0
    headings = {"Easy": "Easy - the basics",
                "Medium": "Medium - how it works",
                "Hard": "Harder - explain and defend it"}
    for level in ("Easy", "Medium", "Hard"):
        items = ([q for q in own if q[0] == level]
                 + [q for q in GENERAL if q[0] == level])
        if not items:
            continue
        b += E.level(headings[level])
        for item in items:
            number += 1
            b += E.qa(number, item[1], item[2],
                      item[3] if len(item) > 3 else None)
    return b
