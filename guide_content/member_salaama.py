"""
Document for 25ada141 - Salaama.

OCR (src/ocr_extractor.py), saving the files (src/storage.py), and the
charts (src/analysis.py).
"""

from guide_content import member_common as M
from guide_content import pdf_engine as E

MEMBER = "25ada141"
FILES = ["src/ocr_extractor.py", "src/storage.py", "src/analysis.py"]


#=========================================================================#
#  THE IDEAS BEHIND YOUR PART                                             #
#=========================================================================#

def ideas():
    b = []
    b += E.h1("The ideas behind your part")
    b += E.p(
        "Your part has three pieces. **OCR** reads documents that are really "
        "pictures. **Saving** writes the data into files other people can "
        "open. **Charts** turn a long table into something a person can "
        "understand at a glance. OCR has the most ideas behind it, so most "
        "of this chapter is about OCR.")

    #--- Why OCR --------------------------------------------------------#
    b += E.h2("Why the project needed OCR")
    b += E.p(
        "Sasini's crawler downloads the PDF documents CSE publishes, and "
        "Nuhan's code reads the text out of them. For most documents that "
        "works: a normal PDF has the letters stored inside it, and the "
        "computer can copy them straight out. Nuhan's code counts the "
        "characters it finds on each page:")
    b += E.table([
        ["Document", "Pages", "Characters found", "Kind"],
        ["Employee share option schemes", "1", "896", "Text-based"],
        ["DFCC Bank debentures", "1", "792", "Text-based"],
        ["De-listing - Associated Motor Finance", "1", "**0**",
         "**Scanned**"],
        ["Revised format for disclosure ...", "4",
         "0, 127, 1,129, 274", "**Hybrid** - page 1 is a scan"],
    ], widths=[3.9, 0.9, 2.1, 2.0])
    b += E.p(
        "The de-listing notice gives **nothing** - not one character. It "
        "looks like an ordinary letter on screen, but it is a **scan**: "
        "somebody printed it, signed it, and put it through a scanner. The "
        "PDF holds a photograph of the page, not the letters themselves.")
    b += E.image(
        M.IMG / "scan_full_page.png", 7.5,
        "The de-listing notice. Every word you can see here is part of a "
        "photograph.")
    b += E.p(
        "A page with fewer than **50** characters is treated as a scan. Of "
        "the 12 documents saved when this was written, two need OCR: the de-listing "
        "notice, and page 1 of the revised-format document.")
    b += E.idea(
        "a text-based PDF is a typed letter - you can copy any word out of "
        "it. A scanned PDF is a photo of that letter - you can see the "
        "words, but to the computer it is just dots of colour. OCR is "
        "somebody reading the photo out loud and typing what they read.")

    #--- What OCR is ----------------------------------------------------#
    b += E.h2("What OCR is")
    b += E.p(
        "**OCR** stands for **Optical Character Recognition**. The Week 8 "
        "lecture defines it as converting images of text into "
        "machine-readable text. 'Optical' means it works from a picture; "
        "'character recognition' means it works out which letter each shape "
        "is.")
    b += E.p("The lecture gave real uses of OCR:")
    b += E.bullets([
        "Turning paper invoices, receipts and bank statements into digital "
        "records.",
        "Reading car number plates from road and car-park cameras.",
        "Reading passports at airport immigration counters.",
        "Pulling policy numbers, names and amounts out of insurance forms.",
        "Reading printed text aloud for people who cannot see it.",
    ])

    #--- Images are numbers ---------------------------------------------#
    b += E.h2("What a picture is, to a computer")
    b += E.p(
        "A digital picture is a grid of tiny squares called **pixels**. "
        "Each pixel is stored as a **number** for how bright it is: **0** is "
        "black, **255** is white, and everything in between is a shade of "
        "grey. Zoom right into a grey picture of the letter 'n' and this is "
        "all the computer sees:")
    b += E.code(
        "255 255 255 255 255 255\n"
        "255  38  41 190  52 255\n"
        "255  35 255 255  40 255\n"
        "255  36 255 255  44 255\n"
        "255 255 255 255 255 255")
    b += E.p(
        "The small numbers are dark ink; the 255s are white paper. The "
        "computer has no idea this is a letter. OCR has to work that out "
        "from the pattern of numbers.")
    b += E.p(
        "A **colour** picture stores **three** numbers for every pixel - how "
        "much red, green and blue light is in it. Mixing those three makes "
        "every colour. OpenCV stores them in the order blue, green, red, "
        "which is why its setting is called `COLOR_BGR2GRAY`.")
    b += E.idea(
        "a picture is like a huge mosaic made of tiny tiles. Each tile has a "
        "number painted on the back saying how dark it is. The computer "
        "never sees the picture - only the numbers.")

    b += E.h3("Resolution and dpi")
    b += E.p(
        "A PDF page has no pixels until we make an image from it. **dpi** "
        "(dots per inch) decides how many pixels to use for each inch of "
        "paper. More pixels means more detail - and more work. Our "
        "de-listing notice is an A4 page, about 8.3 by 11.7 inches:")
    b += E.table([
        ["dpi", "Image size", "What it is like"],
        ["72", "about 595 x 841 pixels", "Screen size. Small print turns to "
                                        "mush."],
        ["**200**", "**1,653 x 2,337 pixels** (about 3.9 million)",
         "**Our setting.** Clear for printed documents."],
        ["300", "about 2,480 x 3,504 pixels", "More detail for very small "
                                              "print, but slower."],
    ], widths=[1.1, 3.6, 3.8])
    b += E.p("The 200 dpi size is the real size of the image our code made "
             "from the de-listing notice.")

    #--- The pipeline ---------------------------------------------------#
    b += E.h2("The OCR pipeline - four steps")
    b += E.p(
        "The Week 8 lecture split OCR into four steps, each with its own "
        "tool. Your file follows exactly these steps:")
    b += E.table([
        ["Step", "What happens", "Tool"],
        ["1. Image acquisition", "Get the picture - here, turn the PDF page "
                                 "into an image", "pdfplumber, giving "
                                                  "a PIL image"],
        ["2. Preprocessing", "Clean the picture up so the letters are easy "
                             "to read", "OpenCV"],
        ["3. Text recognition", "Read the letters", "pytesseract and "
                                                    "Tesseract"],
        ["4. Post-processing", "Tidy the text into a table and save it",
         "pandas"],
    ], widths=[2.6, 3.9, 2.0])
    b += E.idea(
        "photocopying a faded old letter before trying to read it. First "
        "you get the letter onto the copier (step 1). You turn the contrast "
        "up so the writing is dark and the paper is white (step 2). Then "
        "you read it (step 3), and type it up neatly (step 4).")

    #--- Preprocessing --------------------------------------------------#
    b += E.h2("Preprocessing - why clean the picture?")
    b += E.p(
        "The lecture's list of OCR challenges starts with **poor image "
        "quality**, and its answer is to improve the image before reading "
        "it. Tesseract, the reading program, works best on plain black "
        "letters on a clean white background. A real scan is not like "
        "that: the paper is slightly grey, the ink is uneven, and one side "
        "of the page can be darker than the other.")

    b += E.h3("Greyscale")
    b += E.p(
        "Colour tells us nothing about which letter a shape is - an 'a' is "
        "an 'a' in blue or in black. Turning the picture grey leaves **one** "
        "number per pixel instead of three, so every later step has a third "
        "of the numbers to deal with.")

    b += E.h3("Thresholding - black or white, nothing in between")
    b += E.p(
        "**Thresholding** makes every pixel either pure black (0) or pure "
        "white (255). You pick a cut-off: anything brighter becomes white, "
        "anything darker becomes black. The letters get hard, clean edges.")
    b += E.code(
        "grey pixels:        250  243  128   36   40  201  248\n"
        "cut-off 150:        255  255    0    0    0  255  255")
    b += E.p(
        "The problem is choosing **one** cut-off for the whole page. If the "
        "left side of a scan is darker, a cut-off that suits the right side "
        "turns the left side's paper black.")
    b += E.p(
        "**Adaptive thresholding** fixes this. Instead of one cut-off for "
        "the whole page, it works out a separate cut-off for every small "
        "area, from the pixels around it. A pixel only turns black if it is "
        "darker than its own neighbourhood.")
    b += E.idea(
        "judging whether someone is tall. One rule for everybody - 'over "
        "six feet is tall' - fails in a class of children. Adaptive "
        "thresholding compares each person with the people standing around "
        "them.")

    b += E.h3("Noise, kernels and morphology")
    b += E.p(
        "**Noise** means small marks that are not part of the text - specks "
        "of dust on the scanner glass, for example. The lecture's OCR "
        "example includes an optional **noise removal** step using a "
        "method called **morphology**, which changes the shapes in a "
        "black-and-white image.")
    b += E.p(
        "Morphology slides a tiny grid, called a **kernel**, over every "
        "pixel of the image. The kernel's size decides how big a mark it "
        "can affect. There are two basic moves:")
    b += E.table([
        ["Move", "What it does to the white areas"],
        ["Erosion", "Shrinks them - white shapes get thinner"],
        ["Dilation", "Grows them - white shapes get fatter"],
        ["**Opening**", "Erosion, then dilation. Removes small **white** "
                        "spots"],
        ["**Closing**", "Dilation, then erosion. Fills in small **black** "
                        "spots"],
    ], widths=[2.2, 6.3])
    b += E.p(
        "A scan of a printed page has **black** specks on **white** paper, "
        "so closing is the move that would remove them - the white paper "
        "grows over the speck, then shrinks back, and the speck stays "
        "filled in.")
    b += E.careful(
        "the lecture's example uses **opening** with a **1 x 1** kernel. A "
        "1 x 1 kernel looks at only one pixel at a time, so it cannot change "
        "anything. We measured it on the de-listing notice: **0 pixels "
        "different** before and after. Your code keeps the step so the "
        "pipeline matches the lecture, and your file says honestly that it "
        "changes nothing. If you are asked, say exactly that - never claim "
        "it removes specks.")
    b += E.p(
        "Why not just switch to closing with a bigger kernel? Because a "
        "full stop is also a small black dot. A kernel big enough to remove "
        "a speck of dust can also remove full stops, the dot on an 'i', or "
        "thin parts of letters. That change would need testing on real "
        "pages before it could be trusted.")

    #--- Tesseract ------------------------------------------------------#
    b += E.h2("How the reading step works")
    b += E.p(
        "**Tesseract** is the program that actually reads the letters. The "
        "lecture notes that it was first created by HP and later developed "
        "by Google, and it is free to use. It finds the lines of text on the "
        "page, splits them into words, and recognises the letters using "
        "patterns it learned from a large amount of example text. For every word it also gives a "
        "**confidence** score from 0 to 100 - how sure it is.")
    b += E.p(
        "**pytesseract** is not Tesseract. It is a small Python **wrapper**: "
        "it sends our image to the Tesseract program, waits for the answer, "
        "and hands it back to Python. That is why there are two things to "
        "install:")
    b += E.table([
        ["What", "How it is installed", "Done?"],
        ["pytesseract (the Python wrapper)", "`pip install pytesseract` - in "
                                             "requirements.txt", "Yes"],
        ["Tesseract (the actual program)", "Downloaded and installed "
                                           "separately on Windows, then "
                                           "added to the PATH", "Must be done "
                                                                "on the "
                                                                "laptop used"],
    ], widths=[3.0, 3.8, 1.7])
    b += E.idea(
        "pytesseract is a telephone, and Tesseract is the expert on the "
        "other end of the line. You can own a perfectly good telephone, but "
        "if nobody is on the other end, you get no answer.")
    b += E.careful(
        "until Tesseract is installed, the OCR tab shows installation "
        "instructions instead of the pictures and the text. Install it on "
        "the laptop you will use for the viva, and check it by typing "
        "`tesseract --version` in a terminal.")

    #--- Limits ---------------------------------------------------------#
    b += E.h2("OCR is not perfect")
    b += E.p(
        "OCR makes mistakes, and the lecture's last best practice is to "
        "**verify** the output - check it against the real page by eye. "
        "Some mistakes are common because the shapes really are alike:")
    b += E.table([
        ["Easily confused", "Why"],
        ["0 (zero) and O (letter)", "Both are round"],
        ["1, l (small L) and I (capital i)", "All are one straight line"],
        ["rn and m", "Two letters close together look like one"],
        ["5 and S, 8 and B", "Similar curves"],
    ], widths=[3.5, 5.0])
    b += E.p(
        "Logos are especially hard. The CSE logo at the top of every notice "
        "separates its letters with thin lines, and an OCR program may read "
        "those lines as extra letters, such as an I or a 1:")
    b += E.image(M.IMG / "scan_logo.png", 7,
                 "The CSE logo from the scanned notice. To OCR, the lines "
                 "between C, S and E look a lot like letters.")
    b += E.p(
        "That is what the confidence score is for. Your code lists the "
        "words Tesseract was **least** sure about, so a person knows exactly "
        "which words to check by hand instead of re-reading everything.")

    #--- Saving ---------------------------------------------------------#
    b += E.h2("Saving data - three kinds of file")
    b += E.table([
        ["Format", "What it is", "Good for"],
        ["**CSV**", "Plain text. One row per line, commas between the "
                    "columns", "Opens in anything - Excel, pandas, even "
                               "Notepad"],
        ["**Excel** (.xlsx)", "A spreadsheet file, which can hold several "
                              "sheets", "People who want to sort and filter "
                                        "by hand"],
        ["**JSON**", "Names and values, like the data CSE sends us",
         "Other programs, and keeping extra details beside the data"],
    ], widths=[1.8, 3.4, 3.3])
    b += E.p(
        "A CSV file of our share prices starts like this - it really is "
        "just text:")
    b += E.code(
        "symbol,price,change\n"
        "SAMP.N0000,136.75,-0.25\n"
        "AEL.N0000,24.5,0.3")

    b += E.h3("Crediting the source - inside the file")
    b += E.p(
        "The Week 6 lecture lists crediting the data source as part of "
        "ethical scraping. A spreadsheet gets copied and emailed on, and a "
        "note in a separate document gets lost along the way. So every file "
        "we save carries the credit **inside itself**: where the data came "
        "from, when it was collected, and that it was for academic use.")
    b += E.idea(
        "the label sewn into a piece of clothing. However many times it is "
        "passed on, the label still says where it was made.")

    b += E.h3("Text encoding")
    b += E.p(
        "Every letter in a text file is stored as a number, and an "
        "**encoding** is the table that says which number means which "
        "letter. **UTF-8** covers every language and symbol. CSE's titles "
        "use curly quotation marks and long dashes - for example "
        "DFCC BANK PLC (\u201cBANK\u201d) \u2013 ... - so the encoding "
        "matters. Opened with the wrong one, those characters turn into "
        "rubbish symbols.")

    #--- Charts ---------------------------------------------------------#
    b += E.h2("Why charts?")
    b += E.p(
        "The share price table has about 284 rows. Reading 284 rows tells "
        "you very little. A sorted bar chart shows in one second which "
        "companies moved the most. Choosing the right chart matters:")
    b += E.bullets([
        "**Horizontal bars** - company codes are long, and they fit along "
        "the side of a chart better than squeezed under each bar.",
        "**Sorted** - the biggest at one end, so the order means something.",
        "**Green for up, red for down** - the usual colours for share "
        "prices.",
        "**Never colour alone** - red and green are the hardest pair to tell "
        "apart for people with colour blindness, so every bar also says "
        "'up' or 'down' and has a plus or minus sign.",
        "**Sensible units** - turnover in millions of rupees, not raw "
        "numbers with nine digits.",
    ])
    b += E.remember(
        "OCR turns a picture of text back into text, in four steps: get the "
        "image, clean it, read it, tidy it. Saving puts the data into CSV, "
        "Excel and JSON with the source written inside. Charts make the "
        "numbers readable at a glance.")
    return b


#=========================================================================#
#  READING PYTHON                                                         #
#=========================================================================#

def python_chapter():
    examples = {
        "comment": (
            "# Turnover runs into the billions, which is hard to read on an axis,\n"
            "# so we show it in millions.",
            "From `chart_turnover()`. It explains why the next line divides "
            "by a million. Python skips both lines."),
        "variable": (
            "millions = data[\"turnover\"] / 1_000_000",
            "Take the turnover column, divide every value by a million, and "
            "keep the result in a box called `millions`. The underscores in "
            "`1_000_000` are only there to make it easier to read - Python "
            "ignores them."),
        "text": (
            "image_path = config.IMAGE_DIR / f\"{name}_page{page_number}.png\"",
            "From `pdf_page_to_image()`. The f-string builds a file name like "
            "`14364_DE-LISTING OF THE ..._page1.png`. The `/` here is not "
            "division - it joins a folder and a file name into one path, "
            "like `data/images/14364_..._page1.png`."),
        "numbers": (
            "OCR_TEXT_THRESHOLD = 50\n"
            "OCR_DPI = 200",
            "From `config.py`, and used by your code: a page with fewer than "
            "50 characters is treated as a scan, and pages are turned into "
            "images at 200 dpi. Your `tesseract_ready()` also returns `True` "
            "or `False` to say whether Tesseract is installed."),
        "list": (
            "rows = []\n"
            "...\n"
            "rows.append({\"Word\": word, \"Confidence\": confidence})",
            "From `read_words_with_confidence()`. Start with an empty list, "
            "then add one small dictionary for every word Tesseract read."),
        "dict": (
            "steps = {\"grey\": grey_path, \"threshold\": threshold_path,\n"
            "         \"cleaned\": cleaned_path}",
            "From `preprocess_image()`. The three image files are kept under "
            "labels, so the app can ask for `steps[\"grey\"]` and show the "
            "right picture in the right place."),
        "function": (
            "def pdf_page_to_image(pdf_path, page_number=1, dpi=None):",
            "The ingredients are the PDF, which page, and how detailed the "
            "image should be. `page_number=1` is a **default** - if nobody "
            "says which page, it uses page 1. `dpi=None` means 'not given - "
            "use the normal setting'."),
        "if": (
            "if page_number < 1 or page_number > len(pdf.pages):\n"
            "    return None, f\"This PDF has {len(pdf.pages)} page(s).\"",
            "If someone asks for page 0, or page 5 of a 4-page document, "
            "stop and explain instead of crashing. `or` means either one "
            "being true is enough. `len(pdf.pages)` is how many pages there "
            "are."),
        "for": (
            "for i in range(len(data[\"text\"])):\n"
            "    word = data[\"text\"][i].strip()\n"
            "    confidence = int(data[\"conf\"][i])",
            "Tesseract returns separate lists - one of words, one of "
            "confidence scores - in the same order. `range(len(...))` counts "
            "0, 1, 2, ... up to the number of words, and `i` picks the "
            "matching item from each list."),
        "import": (
            "import cv2\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import pdfplumber\n"
            "import pytesseract\n"
            "from PIL import Image",
            "`cv2` is OpenCV's name in Python. `numpy` handles grids of "
            "numbers - which is what images are. `PIL` is Pillow, the image "
            "library from the lecture. These are the tools from the lecture's "
            "OCR pipeline."),
        "try": (
            "try:\n"
            "    version = pytesseract.get_tesseract_version()\n"
            "    return True, f\"Tesseract {version} is installed and ready.\"\n"
            "except Exception:\n"
            "    return False, INSTALL_HELP",
            "From `tesseract_ready()`. Ask Tesseract for its version number. "
            "If it answers, it is installed. If anything goes wrong, it is "
            "not - so return the installation instructions instead of "
            "crashing."),
        "with": (
            "with open(path, \"w\", encoding=\"utf-8-sig\", newline=\"\") as f:\n"
            "    f.write(f\"# {config.ATTRIBUTION}\\n\")",
            "From `export()`. Open a file for writing (`\"w\"`), write into "
            "it, and close it automatically at the end. `\\n` means 'start "
            "a new line'."),
        "pandas": (
            "risers = data.nlargest(top, \"percentageChange\")\n"
            "fallers = data.nsmallest(top, \"percentageChange\")\n"
            "movers = pd.concat([fallers, risers]).sort_values(\"percentageChange\")",
            "From `chart_movers()`. Take the 10 biggest rises and the 10 "
            "biggest falls, stack the two tables into one with `pd.concat`, "
            "and sort it so the chart runs from the biggest fall to the "
            "biggest rise."),
    }

    extras = [
        ("Giving back two answers at once",
         "A function can return two values separated by a comma, and the "
         "caller can catch them in two boxes:",
         "return str(image_path), None          # inside the function\n\n"
         "image_path, error = pdf_page_to_image(pdf_path, page_number, dpi)",
         "Your functions return 'the result, and an error message'. When it "
         "works, the error is `None`. When it fails, the result is `None` "
         "and the error says why."),
        ("List comprehensions - building a list in one line",
         "A **list comprehension** makes a new list from an old one in a "
         "single line. From `text_to_lines()`:",
         "lines = [line.strip() for line in text.strip().split(\"\\n\")]\n"
         "lines = [line for line in lines if line]",
         "The first line reads: 'split the text at every new line, and trim "
         "the spaces off each line'. The second: 'keep only the lines that "
         "are not empty' - an empty text counts as false."),
        ("Formatting numbers",
         "Inside an f-string, a colon after the value sets how a number is "
         "shown. Your charts use these:",
         "f\"{v:+.2f}%\"          ->  +3.21%   or  -0.50%\n"
         "f\"{v:,.1f}M\"          ->  1,234.5M\n"
         "f\"Rs {total / 1_000_000_000:,.2f} bn\"  ->  Rs 0.49 bn",
         "`+` always shows the sign, `,` puts commas in thousands, and "
         "`.2f` means two numbers after the decimal point."),
        ("if and else in one line",
         "A short choice can be written on one line:",
         "direction = (\"rose\" if change > 0\n"
         "             else \"fell\" if change < 0 else \"did not move\")",
         "From `summary()`. Read it as: 'rose if it went up, otherwise fell "
         "if it went down, otherwise did not move'."),
        ("or - use this, or else that",
         "`dpi = dpi or config.OCR_DPI` means: use the dpi we were given, "
         "but if none was given, use the normal setting of 200.",
         None, None),
        ("numpy arrays",
         "An image loaded by OpenCV is a **numpy array** - a grid of "
         "numbers. Your kernel is a tiny one:",
         "kernel = np.ones((1, 1), np.uint8)",
         "A grid 1 row by 1 column, filled with ones. `np.uint8` means whole "
         "numbers from 0 to 255 - the same kind of number a pixel is."),
        ("Named arguments",
         "When a function has many settings, you can name each one as you "
         "pass it in, so the order does not matter and the code explains "
         "itself:",
         "go.Bar(x=movers[\"percentageChange\"], y=movers[\"symbol\"],\n"
         "       orientation=\"h\", cliponaxis=False)",
         "`orientation=\"h\"` means horizontal bars."),
    ]
    return M.python_chapter(MEMBER, examples, "src/ocr_extractor.py", extras)


#=========================================================================#
#  FILE 1 - src/ocr_extractor.py                                          #
#=========================================================================#

def file_ocr():
    b = []
    b += E.h1("Your file: src/ocr_extractor.py")
    b += E.big(
        "Reads scanned PDF pages, where there is no text to extract, using "
        "the four-step OCR pipeline from the lecture.")
    b += E.p("The file has one function for each step, plus one that runs "
             "all four in order:")
    b += E.code(
        "tesseract_ready()               is Tesseract installed?\n"
        "pdf_page_to_image()             step 1  image acquisition\n"
        "preprocess_image()              step 2  preprocessing\n"
        "read_text()                     step 3  text recognition\n"
        "read_words_with_confidence()    step 3  (word by word)\n"
        "text_to_lines()                 step 4  post-processing\n"
        "ocr_pdf_page()                  all four steps together")

    b += E.h2("Before anything - is Tesseract installed?")
    b += E.code(
        "def tesseract_ready():\n"
        "    try:\n"
        "        version = pytesseract.get_tesseract_version()\n"
        "        return True, f\"Tesseract {version} is installed and ready.\"\n"
        "    except Exception:\n"
        "        return False, INSTALL_HELP")
    b += E.p(
        "`import pytesseract` works even when Tesseract is missing - "
        "remember, pytesseract is only the telephone. The only sure way to "
        "know is to ask Tesseract something. If it cannot give its version "
        "number, it is not there, and we show `INSTALL_HELP` - the "
        "installation steps from the lecture, in short - instead of an "
        "error.")

    b += E.h2("Step 1 - turning the page into an image")
    b += E.code(
        "def pdf_page_to_image(pdf_path, page_number=1, dpi=None):\n"
        "    dpi = dpi or config.OCR_DPI\n"
        "    pdf_path = str(pdf_path)\n\n"
        "    with pdfplumber.open(pdf_path) as pdf:\n"
        "        if page_number < 1 or page_number > len(pdf.pages):\n"
        "            return None, f\"This PDF has {len(pdf.pages)} page(s).\"\n\n"
        "        page_image = pdf.pages[page_number - 1].to_image(resolution=dpi)\n\n"
        "        name = pdf_path.replace(\"\\\\\", \"/\").split(\"/\")[-1].replace(\".pdf\", \"\")\n"
        "        image_path = config.IMAGE_DIR / f\"{name}_page{page_number}.png\"\n"
        "        page_image.save(str(image_path))\n\n"
        "    return str(image_path), None")
    b += E.bullets([
        "OCR reads pictures, not PDFs, so the page must become a picture "
        "first. pdfplumber's `to_image()` does that, and gives back a PIL "
        "image.",
        "`pdf.pages[page_number - 1]` - people count pages from 1, but "
        "Python counts from 0. Page 1 is `pages[0]`.",
        "`resolution=dpi` - 200 dots per inch, which made a 1,653 x 2,337 "
        "pixel image of the de-listing notice.",
        "The `name` line takes the file name without its folder or `.pdf`, "
        "so the image is saved as `14364_DE-LISTING ..._page1.png` in "
        "`data/images`.",
    ])

    b += E.h2("Step 2 - cleaning the image")
    b += E.code(
        "image = cv2.imread(str(image_path))\n"
        "if image is None:\n"
        "    return None, \"Could not open the image.\"\n\n"
        "# Colour to grey.\n"
        "grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
        "cv2.imwrite(grey_path, grey)\n\n"
        "# Grey to pure black and white.\n"
        "threshold = cv2.adaptiveThreshold(\n"
        "    grey, 255,\n"
        "    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\n"
        "    cv2.THRESH_BINARY,\n"
        "    31, 2,\n"
        ")\n"
        "cv2.imwrite(threshold_path, threshold)\n\n"
        "# The lecture's optional noise removal step. With a 1x1 kernel it\n"
        "# leaves the image exactly as it was (see the note above).\n"
        "kernel = np.ones((1, 1), np.uint8)\n"
        "cleaned = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)\n"
        "cv2.imwrite(cleaned_path, cleaned)")
    b += E.bullets([
        "`cv2.imread` loads the image as a grid of numbers. If the file "
        "cannot be opened, it gives back `None`, so we check for that.",
        "`cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)` - colour to grey. BGR "
        "is OpenCV's blue-green-red order.",
        "`cv2.imwrite` saves each stage as its own picture, so the app can "
        "show all of them side by side.",
    ])
    b += E.p("The adaptive threshold has five settings:")
    b += E.table([
        ["Setting", "What it means"],
        ["`grey`", "The picture to work on"],
        ["`255`", "The value for pixels that pass - white"],
        ["`ADAPTIVE_THRESH_GAUSSIAN_C`", "Work out each cut-off from the "
                                         "pixels around it, counting nearer "
                                         "pixels more"],
        ["`THRESH_BINARY`", "Brighter than the cut-off becomes white; darker "
                            "becomes black"],
        ["`31`", "The size of the neighbourhood: 31 x 31 pixels. It has to "
                 "be an odd number, so there is a centre pixel"],
        ["`2`", "Taken off the local average. A pixel must be a little darker "
                "than its surroundings to become black, so slightly grey "
                "paper stays white"],
    ], widths=[3.4, 5.1])

    b += E.p("This is what each stage did to part of the de-listing notice:")
    b += E.image(M.IMG / "ocr_step_original.png", 14,
                 "The page as it came out of the PDF.")
    b += E.image(M.IMG / "ocr_step_grey.png", 14,
                 "1. Colour removed. Almost the same to the eye - but now "
                 "one number per pixel instead of three.")
    b += E.image(M.IMG / "ocr_step_threshold.png", 14,
                 "2. Black and white. The letters have hard edges and the "
                 "paper is pure white. Look closely and you can see a few "
                 "dark specks between words.")
    b += E.image(M.IMG / "ocr_step_cleaned.png", 14,
                 "3. After the noise step. Identical to picture 2 - 0 "
                 "pixels changed, because the kernel is 1 x 1.")
    b += E.p(
        "The specks in picture 2 are exactly the kind of noise that closing "
        "with a bigger kernel could remove. They stay, and your code says "
        "why: the same change could also rub out full stops and thin parts "
        "of letters.")

    b += E.h2("Step 3 - reading the text")
    b += E.code(
        "def read_text(image_array):\n"
        "    pil_image = Image.fromarray(image_array)\n"
        "    return pytesseract.image_to_string(pil_image)")
    b += E.p(
        "OpenCV gives us a numpy array. `Image.fromarray()` turns it into a "
        "PIL image, the way the lecture passed images to pytesseract. "
        "`image_to_string` returns everything Tesseract read as one long "
        "piece of text.")
    b += E.code(
        "def read_words_with_confidence(image_array):\n"
        "    pil_image = Image.fromarray(image_array)\n"
        "    data = pytesseract.image_to_data(\n"
        "        pil_image, output_type=pytesseract.Output.DICT)\n\n"
        "    rows = []\n"
        "    for i in range(len(data[\"text\"])):\n"
        "        word = data[\"text\"][i].strip()\n"
        "        confidence = int(data[\"conf\"][i])\n"
        "        if word and confidence > 0:\n"
        "            rows.append({\"Word\": word, \"Confidence\": confidence})\n\n"
        "    return pd.DataFrame(rows)")
    b += E.p(
        "`image_to_data` gives far more: every word separately, where it is "
        "on the page, and a confidence score. Tesseract also lists empty "
        "boxes for whole blocks and lines, with a confidence of -1. "
        "`if word and confidence > 0` keeps only real words.")

    b += E.h2("Step 4 - tidying the result")
    b += E.code(
        "def text_to_lines(text):\n"
        "    lines = [line.strip() for line in text.strip().split(\"\\n\")]\n"
        "    lines = [line for line in lines if line]\n\n"
        "    return pd.DataFrame({\n"
        "        \"Line\": range(1, len(lines) + 1),\n"
        "        \"Text\": lines,\n"
        "    })")
    b += E.p(
        "OCR output arrives as one long string full of blank lines. This "
        "splits it into lines, trims them, drops the empty ones, and numbers "
        "them 1, 2, 3 in a table - which is easy to check, and can be saved "
        "as CSV or Excel.")

    b += E.h2("All four steps together - ocr_pdf_page()")
    b += E.code(
        "ready, message = tesseract_ready()\n"
        "if not ready:\n"
        "    return {\"ok\": False, \"error\": message}\n\n"
        "image_path, error = pdf_page_to_image(pdf_path, page_number, dpi)  # 1\n"
        "prepared, steps = preprocess_image(image_path)                    # 2\n"
        "text = read_text(prepared)                                        # 3\n"
        "words = read_words_with_confidence(prepared)                      # 3\n"
        "lines = text_to_lines(text)                                       # 4\n\n"
        "average_confidence = (round(words[\"Confidence\"].mean(), 1)\n"
        "                      if not words.empty else 0)")
    b += E.p(
        "(Shortened - the real function checks for an error after every "
        "step.) It returns a dictionary with the text, the lines, the word "
        "scores, the average confidence and the paths of the three "
        "pictures, which is everything the OCR tab shows.")
    b += E.p(
        "Which page does it read? The app asks Nuhan's PDF reader which "
        "pages are scans and reads the **first scanned page**. For the "
        "de-listing notice that is page 1, and for the revised-format "
        "document it is also page 1 - its pages 2 to 4 have ordinary text.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.ocr_extractor")
    b += E.p("On a computer without Tesseract, this is the real output:")
    b += E.code(
        "Tesseract is not installed on this computer.\n\n"
        "To install it:\n"
        "  1. Download it from https://github.com/UB-Mannheim/tesseract/wiki\n"
        "  2. Install it to C:\\Program Files\\Tesseract-OCR\\\n"
        "  3. Tick the option to add it to the system PATH\n"
        "  4. Restart this app\n\n"
        "The Python part (pip install pytesseract) is already done.")
    b += E.p(
        "Once Tesseract is installed, the same command finds a scanned PDF "
        "by itself and prints how many characters it read, the average "
        "confidence, the resolution, the first part of the text, and the "
        "eight words Tesseract was least sure about. Run it yourself before "
        "the viva, so you know what it says for our documents.")
    return b


#=========================================================================#
#  FILE 2 - src/storage.py                                                #
#=========================================================================#

def file_storage():
    b = []
    b += E.h1("Your file: src/storage.py")
    b += E.big(
        "Saves the data as CSV, Excel and JSON files - and every file "
        "carries the credit to the Colombo Stock Exchange inside it.")

    b += E.h2("export() - the time stamps")
    b += E.code(
        "stamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")\n"
        "collected = datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")")
    b += E.p(
        "`datetime.now()` is the current date and time. `strftime` writes it "
        "out in a chosen pattern:")
    b += E.table([
        ["Code", "Means", "Example"],
        ["`%Y`", "Year", "2026"],
        ["`%m`", "Month", "09"],
        ["`%d`", "Day", "26"],
        ["`%H %M %S`", "Hours, minutes, seconds", "18 27 47"],
    ], widths=[2.0, 3.5, 3.0])
    b += E.p(
        "`stamp` goes in the file name - `cse_share_prices_20260926_182747"
        ".csv` - so a new save never overwrites an older one. `collected` "
        "is the easy-to-read version written inside the file.")

    b += E.h2("The CSV file")
    b += E.code(
        "with open(path, \"w\", encoding=\"utf-8-sig\", newline=\"\") as f:\n"
        "    f.write(f\"# {config.ATTRIBUTION}\\n\")\n"
        "    f.write(f\"# Collected on: {collected}\\n\")\n"
        "    f.write(f\"# Rows: {len(df)}   Columns: {len(df.columns)}\\n\")\n"
        "    df.to_csv(f, index=False)")
    b += E.p(
        "Three lines starting with `#` are written first, then pandas "
        "writes the table underneath. This is the top of a real file:")
    b += E.code(
        "# Data source: Colombo Stock Exchange (https://www.cse.lk). "
        "Collected\n"
        "#   for academic purposes only - DA 2009, University of Colombo.\n"
        "# Collected on: 2026-09-26 18:27:47\n"
        "# Rows: 3   Columns: 3\n"
        "symbol,price,change\n"
        "SAMP.N0000,136.75,-0.25")
    b += E.p("(The first line is one long line in the real file.)")
    b += E.bullets([
        "`utf-8-sig` - UTF-8 with a tiny marker at the very start of the "
        "file. The marker tells Excel the file is UTF-8, so the curly quotes "
        "and dashes in CSE's titles show properly. Without it, Excel can "
        "guess wrong and show rubbish characters.",
        "`newline=\"\"` - lets the CSV writer control the line endings. "
        "Without it, Windows can add an extra blank line between every row.",
        "`index=False` - do not write pandas's row numbers 0, 1, 2 as an "
        "extra column.",
    ])
    b += E.p("pandas can read the file back and skip the comment lines:")
    b += E.code("pd.read_csv(path, comment=\"#\")")

    b += E.h2("The Excel file - a second sheet")
    b += E.code(
        "source = pd.DataFrame({\n"
        "    \"Item\": [\"Source\", \"Website\", \"Collected on\", \"Rows\",\n"
        "             \"Collected by\", \"Course\"],\n"
        "    \"Value\": [\"Colombo Stock Exchange\", config.BASE_URL, collected,\n"
        "              len(df), ..., config.COURSE],\n"
        "})\n\n"
        "with pd.ExcelWriter(path, engine=\"openpyxl\") as writer:\n"
        "    df.to_excel(writer, sheet_name=\"Data\", index=False)\n"
        "    source.to_excel(writer, sheet_name=\"Source\", index=False)")
    b += E.p(
        "Comment lines would break an Excel sheet, so Excel carries the "
        "credit differently: the data goes on a sheet called **Data** and "
        "the details on a second sheet called **Source**. `openpyxl` is the "
        "library pandas uses to write .xlsx files. 'Collected by' lists all "
        "four of us, with our names.")
    b += E.careful(
        "the Excel part is inside `try` with `except Exception: pass`, "
        "which means 'if it fails, carry on quietly'. The usual reason it "
        "fails is that a file of the same name is open in Excel. The CSV and "
        "JSON files are still saved, and the app's list of saved files shows "
        "exactly which files were made - so a missing Excel file is visible "
        "there, even though no error appears.")

    b += E.h2("The JSON file - details above the records")
    b += E.code(
        "contents = {\n"
        "    \"details\": {\n"
        "        \"source\": config.ATTRIBUTION,\n"
        "        \"collected_on\": collected,\n"
        "        \"rows\": len(df),\n"
        "        \"collected_by\": [config.member_label(m) for m in config.TEAM],\n"
        "    },\n"
        "    \"records\": json.loads(df.to_json(orient=\"records\",\n"
        "                                     date_format=\"iso\")),\n"
        "}\n\n"
        "with open(path, \"w\", encoding=\"utf-8\") as f:\n"
        "    json.dump(contents, f, indent=2)")
    b += E.bullets([
        "`orient=\"records\"` - one `{ }` per row, the same shape CSE sent "
        "us.",
        "`date_format=\"iso\"` - dates written like `2026-09-25T14:39:57.431`, "
        "a standard every program understands, instead of big numbers.",
        "`json.loads(...)` turns pandas's JSON text back into Python lists "
        "and dictionaries, so it can sit inside `contents`.",
        "`indent=2` - spread over many lines with indents, so a person can "
        "read it.",
    ])
    b += E.p("The top of a real JSON file:")
    b += E.code(
        "{\n"
        "  \"details\": {\n"
        "    \"source\": \"Data source: Colombo Stock Exchange ...\",\n"
        "    \"collected_on\": \"2026-09-26 18:27:47\",\n"
        "    \"rows\": 3,\n"
        "    \"collected_by\": [\n"
        "      \"25ada072 - Pasindu\",\n"
        "      \"25ada073 - Sasini\",\n"
        "      \"25ada141 - Salaama\",\n"
        "      \"24ada076 - Nuhan\"\n"
        "    ]\n"
        "  },\n"
        "  \"records\": [ ...")
    b += E.remember(
        "three formats, three ways of carrying the credit: comment lines at "
        "the top of the CSV, a Source sheet in Excel, and a details section "
        "in the JSON. The credit travels inside the file, wherever the file "
        "goes.")

    b += E.h2("save_pdf() - safe file names")
    b += E.code(
        "safe = \"\".join(c for c in filename if c.isalnum() or c in \" ._-\").strip()\n"
        "safe = safe[:110] or \"document\"\n"
        "if not safe.lower().endswith(\".pdf\"):\n"
        "    safe += \".pdf\"")
    b += E.p(
        "Sasini's crawler names each PDF after its title, but Windows does "
        "not allow some characters in file names - such as `\\ / : * ? \" "
        "< > |`. This keeps only letters, numbers, spaces, dots, underscores "
        "and hyphens. `isalnum()` means 'is a letter or a number'.")
    b += E.p(
        "You can see it in our real files. The title "
        "DFCC BANK PLC (\u201cBANK\u201d) \u2013 BASEL III ... was saved as "
        "`14475_DFCC BANK PLC BANK  BASEL III ...pdf` - the brackets, curly "
        "quotes and long dash were removed, which is why there are two "
        "spaces in a row. `safe[:110]` keeps names to a sensible length, "
        "and `or \"document\"` gives a name even if nothing was left.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.storage")
    b += E.code(
        "Saving a small example in all three formats\n"
        "-------------------------------------------------------\n"
        "  saved: example_20260926_182747.csv\n"
        "  saved: example_20260926_182747.xlsx\n"
        "  saved: example_20260926_182747.json\n\n"
        "Reading the CSV back, skipping the comment lines:\n"
        "    symbol   price  change\n"
        "SAMP.N0000  136.75   -0.25\n"
        " AEL.N0000   24.50    0.30\n"
        "ABAN.N0000 1094.25    0.00")
    b += E.p(
        "It saves a small made-up table of three companies, then reads the "
        "CSV back - proving the comment lines do not get in the way. Open "
        "the files in `data/exports` to see the credit for yourself.")
    return b


#=========================================================================#
#  FILE 3 - src/analysis.py                                               #
#=========================================================================#

def file_analysis():
    b = []
    b += E.h1("Your file: src/analysis.py")
    b += E.big(
        "Draws the three charts and works out the summary figures, using "
        "the cleaned share price table.")
    b += E.p(
        "The charts are made with **Plotly**, a charting library that makes "
        "interactive charts - you can hover over a bar to see its exact "
        "value. `import plotly.graph_objects as go` brings it in, and "
        "`go.Figure(go.Bar(...))` makes a bar chart.")

    b += E.h2("Colours and style")
    b += E.code(
        "COLOURS = {\n"
        "    \"dark\": {\n"
        "        \"up\": \"#34d399\", \"down\": \"#c02626\", \"bar\": \"#22d3ee\", ...\n"
        "    },\n"
        "    \"light\": {\n"
        "        \"up\": \"#047857\", \"down\": \"#dc2626\", \"bar\": \"#0891b2\", ...\n"
        "    },\n"
        "}")
    b += E.p(
        "The app has a dark and a light theme, so there are two sets of "
        "colours. `#047857` is a colour written as a **hex code** - three "
        "pairs of characters for the amount of red, green and blue. "
        "`style()` gives every chart the same plain look: a see-through "
        "background so it matches the theme, and faint grid lines so the "
        "bars stand out.")
    b += E.p(
        "`empty_chart()` shows a short message such as 'Collect the market "
        "data first' instead of a broken, empty chart.")

    b += E.h2("Chart 1 - the biggest movers")
    b += E.code(
        "data = df[[\"symbol\", \"percentageChange\"]].dropna()\n"
        "data = data[data[\"percentageChange\"] != 0]\n\n"
        "risers = data.nlargest(top, \"percentageChange\")\n"
        "fallers = data.nsmallest(top, \"percentageChange\")\n"
        "movers = pd.concat([fallers, risers]).sort_values(\"percentageChange\")\n\n"
        "bar_colours = [c[\"up\"] if v > 0 else c[\"down\"]\n"
        "               for v in movers[\"percentageChange\"]]\n"
        "labels = [f\"{'up' if v > 0 else 'down'} {v:+.2f}%\"\n"
        "          for v in movers[\"percentageChange\"]]")
    b += E.numbered([
        "Keep just the company code and its percentage change, and drop any "
        "rows with a gap.",
        "Remove companies that did not move - `!= 0` means 'is not zero'.",
        "Take the 10 biggest rises and 10 biggest falls, stack them, and "
        "sort from the biggest fall to the biggest rise.",
        "Colour each bar green or red, and label it with the word and the "
        "sign, such as `up +3.21%` or `down -2.10%`.",
    ])
    b += E.code(
        "figure = go.Figure(go.Bar(\n"
        "    x=movers[\"percentageChange\"],\n"
        "    y=movers[\"symbol\"],\n"
        "    orientation=\"h\",\n"
        "    ...\n"
        "    textposition=\"outside\",\n"
        "    cliponaxis=False,\n"
        "))\n\n"
        "limit = movers[\"percentageChange\"].abs().max() * 1.6\n"
        "figure.update_xaxes(title_text=\"Price change (%)\",\n"
        "                    range=[-limit, limit], zeroline=True)")
    b += E.bullets([
        "`orientation=\"h\"` - horizontal bars, with the company codes down "
        "the side.",
        "`textposition=\"outside\"` puts each label just past the end of its "
        "bar. `cliponaxis=False` stops the longest bar's label being cut off "
        "at the edge.",
        "The axis runs the same distance left and right of zero, and 1.6 "
        "times the biggest move, which leaves room for the labels. "
        "`zeroline=True` draws the line at zero that separates the falls "
        "from the rises.",
    ])

    b += E.h2("Chart 2 - where the money went")
    b += E.code(
        "data = df[[\"symbol\", \"turnover\"]].dropna()\n"
        "data = data[data[\"turnover\"] > 0].nlargest(top, \"turnover\")\n"
        "data = data.sort_values(\"turnover\")\n\n"
        "millions = data[\"turnover\"] / 1_000_000")
    b += E.p(
        "**Turnover** is the total value of shares traded - how much money "
        "changed hands for each company. It has no up or down, only size, so "
        "this chart uses **one** colour. A second colour would suggest a "
        "difference that does not exist. It shows the top 15, in millions of "
        "rupees, labelled like `12.3M`.")

    b += E.h2("Chart 3 - the sectors")
    b += E.code(
        "bar_colours = [c[\"up\"] if v > 0 else c[\"down\"] if v < 0\n"
        "               else c[\"faint\"]\n"
        "               for v in data[\"changePercentage\"]]")
    b += E.p(
        "A **sector** is a group of companies in the same kind of business - "
        "banks, hotels, telecoms. This chart shows how each sector's index "
        "moved today. It uses three colours, because a sector can also stay "
        "exactly the same: green up, red down, and grey for no change. "
        "The chart's height grows with the number of sectors - "
        "`max(400, 26 * len(data) + 110)` - so the bars never get squashed.")

    b += E.h2("The summary figures")
    b += E.code(
        "figures = {\"Companies\": len(df)}\n\n"
        "changes = df[\"percentageChange\"].dropna()\n"
        "figures[\"Rose\"] = int((changes > 0).sum())\n"
        "figures[\"Fell\"] = int((changes < 0).sum())\n"
        "figures[\"No change\"] = int((changes == 0).sum())\n\n"
        "total = df[\"turnover\"].dropna().sum()\n"
        "figures[\"Turnover\"] = f\"Rs {total / 1_000_000_000:,.2f} bn\"")
    b += E.p(
        "`changes > 0` marks every company that rose as True, and `.sum()` "
        "counts the Trues. `summary()` then turns the figures into "
        "sentences, and always ends by saying that one day of data is not "
        "investment advice.")

    b += E.h2("What you see when you run it")
    b += E.tryit("run your file on its own:", "python -m src.analysis")
    b += E.p("A real run:")
    b += E.code(
        "Summary figures\n"
        "-------------------------------------------------------\n"
        "  Companies    284\n"
        "  Rose         96\n"
        "  Fell         113\n"
        "  No change    75\n"
        "  Turnover     Rs 0.49 bn\n\n"
        "The All Share Price Index fell to 21,037.35 (-29.54 points). Out of\n"
        "284 companies traded, 96 rose, 113 fell and 75 finished unchanged,\n"
        "so more companies fell than rose. Total turnover was Rs 0.49 bn.\n"
        "This is one trading day, collected for a university assignment. It\n"
        "is not investment advice.\n\n"
        "Building the charts\n"
        "-------------------------------------------------------\n"
        "  movers     built\n"
        "  turnover   built\n"
        "  sectors    built")
    b += E.p(
        "96 + 113 + 75 = 284, so every company is counted exactly once. The "
        "**All Share Price Index** (ASPI) is one number that sums up the "
        "prices of every company on the exchange - when it falls, the "
        "market as a whole went down that day. Your numbers will be "
        "different on the day you run it, because the market changes.")
    b += E.remember(
        "the charts are built from the cleaned table, green and red always "
        "come with words and signs, turnover is shown in millions, and the "
        "summary checks itself - rose, fell and unchanged add up to the "
        "number of companies.")
    return b


#=========================================================================#
#  VIVA                                                                   #
#=========================================================================#

def viva():
    return M.viva_chapter(
        MEMBER,
        tab_steps=[
            "Open the **OCR** tab. Your name is on the label at the top. "
            "The line under it says whether Tesseract is installed.",
            "The **Scanned document** list only offers documents that need "
            "OCR. Choose the de-listing notice (it starts with 14364). Leave "
            "**Image detail** at 200 and press **Read it**.",
            "Point to the three pictures: colour removed, black and white, "
            "and after the noise step - and say honestly that the third "
            "one is the same as the second.",
            "Point to the text Tesseract read, and the table of least "
            "confident words - the ones a person should check.",
            "Open the **Data & Export** tab (after collecting the market "
            "data on the Market Data tab). Press **Draw the charts**.",
            "Under **Save the data**, leave CSV, Excel and JSON ticked and "
            "press **Save**. Open the CSV to show the source lines at the "
            "top.",
        ],
        commands=(
            "tesseract --version              # is Tesseract installed?\n"
            "python -m src.ocr_extractor      # OCR on a scanned page\n"
            "python -m src.storage            # save in three formats\n"
            "python -m src.analysis           # summary figures and charts"),
        script=(
            "My part is OCR, saving the files, and the charts. Some CSE "
            "announcements are scans - photographs of paper - so there is no "
            "text inside them to extract. OCR reads the picture instead, in "
            "the four steps from the lecture: I turn the page into an image "
            "at 200 dpi, clean it with OpenCV - grey, then adaptive "
            "thresholding to pure black and white - read it with pytesseract, "
            "and tidy the result into a table with pandas. Tesseract also "
            "gives a confidence score, so we show which words to check by "
            "hand. Then I save the data as CSV, Excel and JSON, and every "
            "file credits the Colombo Stock Exchange inside itself. Finally "
            "the charts show the biggest movers, the turnover and the "
            "sectors, with words and signs as well as colours."),
        pointers=[
            ["`pytesseract.get_tesseract_version()`",
             "Importing pytesseract works even without Tesseract; asking for "
             "its version proves it is really installed."],
            ["`to_image(resolution=dpi)`", "Step 1 - the PDF page becomes a "
                                           "200 dpi image, 1,653 x 2,337 "
                                           "pixels."],
            ["`cv2.adaptiveThreshold(... 31, 2)`",
             "Black or white, with a separate cut-off for each 31 x 31 "
             "area, so uneven lighting does not spoil it."],
            ["`np.ones((1, 1), np.uint8)` and `MORPH_OPEN`",
             "The lecture's optional noise step. A 1 x 1 kernel changes "
             "nothing - we measured 0 pixels. A bigger kernel could erase "
             "full stops."],
            ["`image_to_data` and `confidence > 0`",
             "Every word with a confidence score; -1 marks empty boxes, so "
             "we skip those."],
            ["`encoding=\"utf-8-sig\"`", "So Excel shows CSE's curly quotes "
                                         "and dashes correctly."],
            ["`sheet_name=\"Source\"`", "Excel carries the credit on a second "
                                        "sheet, because comment lines would "
                                        "break it."],
            ["`cliponaxis=False`", "Stops the longest bar's label being cut "
                                   "off at the edge."],
        ])


#=========================================================================#
#  THE WHOLE DOCUMENT                                                     #
#=========================================================================#

WORDS = [
    ("Adaptive thresholding", "Thresholding with a separate cut-off for "
                              "each small area of the image."),
    ("ASPI", "All Share Price Index - one number summing up the prices of "
             "every company on the exchange."),
    ("Closing", "Dilation then erosion - fills in small black spots."),
    ("Confidence", "How sure Tesseract is about a word, from 0 to 100."),
    ("dpi", "Dots per inch - how many pixels are made for each inch of "
            "paper."),
    ("Encoding", "The table that says which number stands for which "
                 "letter, such as UTF-8."),
    ("Greyscale", "An image with one brightness number per pixel, no "
                  "colour."),
    ("Kernel", "A tiny grid slid over an image to change its shapes."),
    ("Morphology", "Changing the shapes in a black-and-white image, using a "
                   "kernel."),
    ("Noise", "Small marks in an image that are not part of the text."),
    ("numpy array", "A grid of numbers - how OpenCV holds an image."),
    ("OCR", "Optical Character Recognition - turning a picture of text into "
            "text."),
    ("OpenCV", "A library for working with images, used as cv2 in Python."),
    ("Opening", "Erosion then dilation - removes small white spots."),
    ("Pixel", "One tiny square of a digital picture."),
    ("PIL / Pillow", "A Python library for opening and changing images."),
    ("Plotly", "The library that draws our interactive charts."),
    ("pytesseract", "The Python wrapper that sends images to Tesseract."),
    ("Scanned PDF", "A PDF that holds a photograph of a page, with no "
                    "text inside."),
    ("Sector", "A group of companies in the same kind of business."),
    ("Tesseract", "The free OCR program that actually reads the letters."),
    ("Thresholding", "Turning every pixel pure black or pure white."),
    ("Turnover", "The total value of shares traded in a day."),
    ("Wrapper", "Code that lets one program use another, passing messages "
                "between them."),
]


def build():
    b = []
    b += M.cover(MEMBER, "OCR, saving the files, and the charts")
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
    b += file_ocr()
    b += E.page_break()
    b += file_storage()
    b += E.page_break()
    b += file_analysis()
    b += E.page_break()
    b += M.big_picture(
        MEMBER, ["src/ocr_extractor.py", "src/storage.py", "src/analysis.py"],
        ["Your part is steps 7, 9 and 10 - the end of the path. At step 7, "
         "your OCR reads the scanned pages that Nuhan's PDF reader could get "
         "no text from, in the documents Sasini's crawler downloaded. At "
         "step 9, your charts are drawn from the table Pasindu's code "
         "collected and Sasini's code cleaned. At step 10, your code saves "
         "that table as files, with the credit to CSE inside each one. "
         "Your part turns what the others collected into something a person "
         "can read and keep."])
    b += E.page_break()
    b += M.ethics_for_everyone()
    b += E.page_break()
    b += viva()
    b += E.page_break()
    b += M.practice_questions(MEMBER)
    b += E.page_break()
    b += M.word_list(WORDS)
    return b
