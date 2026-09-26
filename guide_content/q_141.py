"""
30 questions for 25ada141 - OCR, saving the files, and the charts.
"""

Q_141 = [

#=========================================================================#
#  OCR                                                                    #
#=========================================================================#

("Easy", "Which files did you write?",
 "`src/ocr_extractor.py`, which reads scanned documents; `src/storage.py`, "
 "which saves the data as CSV, Excel and JSON; and `src/analysis.py`, which "
 "builds the charts and the summary figures."),

("Easy", "What does OCR stand for, and what does it do?",
 "Optical Character Recognition. It means getting a computer to look at a "
 "picture of writing and work out which letters it is seeing, so the words "
 "become text you can search and copy."),

("Easy", "Why did this project need OCR at all?",
 "Because one of the CSE circulars is a scan. Somebody printed the page, "
 "signed it and put it through a scanner, so the file contains a photograph "
 "of the words. Ordinary PDF extraction returns nothing from it, no matter "
 "which library you use."),

("Easy", "Name some real uses of OCR outside this project.",
 "Digitising invoices, receipts and bank statements. Reading number plates "
 "for traffic cameras and car parks. Scanning passports at airports. "
 "Reading insurance claim forms. And reading text aloud for people who "
 "cannot see well."),

("Easy", "Which three libraries make up your OCR pipeline?",
 "PIL (Pillow) for opening and handling the image, OpenCV for cleaning the "
 "image up, and pytesseract for actually reading the letters. pandas then "
 "tidies the result."),

("Medium", "What are the four steps of the OCR pipeline?",
 "**Image acquisition** - turn the PDF page into an image.\n\n"
 "**Preprocessing** - improve the image so the text is easier to read: "
 "remove the colour, then turn it pure black and white.\n\n"
 "**Text recognition** - pytesseract reads the letters.\n\n"
 "**Post-processing** - tidy the text into lines with pandas, and save it."),

("Medium", "How do you turn a PDF page into an image?",
 "With pdfplumber's `to_image()`, at 200 dpi, and then save it as a PNG. "
 "OCR works on pictures, not on PDFs, so the page has to become an image "
 "before anything else can happen.",
 "with pdfplumber.open(pdf_path) as pdf:\n"
 "    page_image = pdf.pages[page_number - 1].to_image(resolution=dpi)\n"
 "    page_image.save(str(image_path))"),

("Medium", "Why convert the image to grey?",
 "Because colour tells us nothing about which letter something is. A grey "
 "image has one brightness value per pixel instead of three colour values, "
 "so there is less for the OCR engine to work through and nothing useful "
 "has been lost."),

("Medium", "What is thresholding, and why do you use the adaptive kind?",
 "Thresholding turns every pixel either pure black or pure white, so the "
 "letters have hard edges instead of soft grey ones. That is what Tesseract "
 "reads best.\n\n"
 "We use adaptive thresholding, which works out the cut-off separately for "
 "each small part of the page instead of using one value for the whole "
 "thing. That matters on a scan, where one side of the page is often darker "
 "than the other - a single cut-off would lose the text on the dark side.",
 "thresh = cv2.adaptiveThreshold(\n"
 "    grey, 255,\n"
 "    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\n"
 "    cv2.THRESH_BINARY,\n"
 "    31, 2)"),

("Medium", "What does the noise removal step do?",
 "In our project, nothing - and it is worth knowing why. It is the optional "
 "step from the lecture's OCR example, which uses a 1x1 kernel. A 1x1 kernel "
 "leaves every pixel as it was; we checked, and 0 pixels changed.\n\n"
 "The idea behind the step is to remove specks left by the scanner, which "
 "OCR would otherwise read as stray full stops. But those specks are black "
 "dots on a white page, and `MORPH_OPEN` removes small white spots, so doing "
 "it properly would need `MORPH_CLOSE` with a 2x2 or 3x3 kernel. A bigger "
 "kernel can also rub out thin parts of letters, so it would need testing "
 "before we changed it. We kept the lecture's setting.",
 "kernel = np.ones((1, 1), np.uint8)       # 1x1: changes nothing\n"
 "cleaned = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)"),

("Medium", "What does the dpi setting change?",
 "How large the image is. dpi means dots per inch, so a higher number means "
 "more detail for the OCR engine to work with, but a bigger image and a "
 "slower job.\n\n"
 "At 72 dpi small print turns to mush and accuracy collapses. We use 200, "
 "which is enough for a printed document. 300 helps with very small print "
 "but takes noticeably longer."),

("Medium", "Why do you convert between OpenCV and PIL?",
 "Because the libraries hold images differently. OpenCV works with numpy "
 "arrays - grids of numbers - while PIL has its own image type, and the "
 "lecture passed PIL images to pytesseract. `Image.fromarray()` converts "
 "the OpenCV result into a PIL image, so we can use OpenCV for the cleaning "
 "and pytesseract for the reading.\n\n"
 "To be accurate: pytesseract will also take a numpy array directly. We "
 "convert anyway so the code follows the lecture's pipeline, where each "
 "library gets the kind of image it is normally used with."),

("Medium", "How do you know whether Tesseract is actually installed?",
 "Importing `pytesseract` is not enough. It is only a small Python wrapper "
 "- the real work is done by the Tesseract program, which on Windows has to "
 "be installed separately. The import succeeds even when the program is "
 "missing.\n\n"
 "So we call `pytesseract.get_tesseract_version()`, which forces it to go "
 "and find the program. If that raises an error, we know it is not there "
 "and we show the install instructions instead of a crash.",
 "def tesseract_ready():\n"
 "    try:\n"
 "        version = pytesseract.get_tesseract_version()\n"
 "        return True, f\"Tesseract {version} is installed and ready.\"\n"
 "    except Exception:\n"
 "        return False, INSTALL_HELP"),

("Medium", "What is the difference between `image_to_string` and "
           "`image_to_data`?",
 "`image_to_string` gives you the text as one block. `image_to_data` gives "
 "you far more - every word separately, where it sits on the page, and a "
 "confidence score from 0 to 100 saying how sure Tesseract is.\n\n"
 "We use both: the string for reading, and the data so we can show which "
 "words are least certain."),

("Medium", "Why only OCR some pages instead of the whole document?",
 "Because OCR is slow and it guesses, while reading a text layer is instant "
 "and exact. The PDF module tells us which pages returned nothing, and we "
 "run OCR only on those. Running it over pages we already read perfectly "
 "would waste time and introduce mistakes into text that was already "
 "correct."),

("Hard", "Is OCR accurate? Show that you understand its limits.",
 "Not completely, and the output shows it. It runs words together where the "
 "spacing is tight, and it misreads logos and stamps as letters because it "
 "is looking for letter shapes everywhere.\n\n"
 "That is why it is the last resort rather than the first choice. If a "
 "document has a real text layer we always read that instead, because it is "
 "exact. We also record the confidence score for every word, so anything "
 "the engine was unsure about can be checked by hand rather than trusted "
 "silently."),

("Hard", "What are the main challenges in OCR, and how do you deal with "
         "them?",
 "Poor image quality - dealt with by scanning at a higher resolution and "
 "improving the contrast, which is what our preprocessing does.\n\n"
 "Complicated layouts with columns and tables, where the engine has to work "
 "out the reading order.\n\n"
 "Handwriting, which needs a different kind of model altogether.\n\n"
 "Unusual fonts and symbols. And pages that are slightly rotated, which "
 "need straightening before anything else, because Tesseract expects "
 "roughly horizontal lines."),

("Hard", "If OCR gave poor results on a document, what would you try?",
 "Raise the dpi first, since small print is the most common cause. Then "
 "look at the preprocessed image - if the thresholding has eaten thin "
 "strokes or left the background patchy, adjust the block size in the "
 "adaptive threshold.\n\n"
 "After that, crop to just the part of the page that matters, so the engine "
 "is not trying to read a logo or a signature. And if the page is tilted, "
 "straighten it, because a few degrees of rotation hurts accuracy more than "
 "people expect."),

#=========================================================================#
#  SAVING THE FILES                                                       #
#=========================================================================#

("Easy", "Which formats do you save the data in?",
 "CSV, Excel and JSON. CSV opens anywhere, Excel is what most people "
 "actually use, and JSON keeps the structure for another program to read."),

("Medium", "How does the source get into each type of file?",
 "Each format needs a different trick.\n\n"
 "A CSV gets comment lines at the top, each starting with `#`. Excel shows "
 "them, and pandas can skip them when reading the file back with "
 "`pd.read_csv(path, comment=\"#\")`.\n\n"
 "An Excel file gets a second worksheet called Source, because a "
 "spreadsheet has no way to hold a comment.\n\n"
 "A JSON file gets a details section above the records.",
 "with open(path, \"w\", encoding=\"utf-8-sig\", newline=\"\") as f:\n"
 "    f.write(f\"# {config.ATTRIBUTION}\\n\")\n"
 "    f.write(f\"# Collected on: {collected}\\n\")\n"
 "    df.to_csv(f, index=False)"),

("Medium", "Why does crediting the source matter?",
 "Because a spreadsheet passed on to somebody else with no source attached "
 "is how data gets misused. Somebody finds the file six months later and "
 "has no idea where the numbers came from or when they were true.\n\n"
 "Putting it inside the file means it travels with the data, instead of "
 "living in an email that gets lost."),

("Medium", "What does `utf-8-sig` mean when writing the CSV?",
 "It writes a small marker at the start of the file that tells Excel the "
 "file is UTF-8. Without it, Excel on Windows sometimes guesses the wrong "
 "encoding and company names with special characters come out as nonsense."),

("Medium", "Why do you strip odd characters out of the PDF filenames?",
 "Because the announcement titles contain characters Windows will not "
 "accept in a filename, such as slashes and quotation marks. We keep only "
 "letters, numbers, spaces, dots, underscores and dashes, and cut the name "
 "to a sensible length so the full path does not get too long."),

#=========================================================================#
#  CHARTS                                                                 #
#=========================================================================#

("Easy", "What do your charts show?",
 "Three things: the companies whose price moved the most today, the "
 "companies with the highest turnover, and how each sector of the market "
 "moved."),

("Medium", "Why is the movers chart a different shape from the turnover "
           "chart?",
 "Because they answer different questions. The movers chart shows direction "
 "as well as size, so it spreads out both ways from a zero line, with "
 "risers on one side and fallers on the other.\n\n"
 "Turnover has no direction - it is only ever an amount - so it is a "
 "straightforward bar chart in one colour. Adding a second colour there "
 "would suggest a difference that does not exist."),

("Medium", "Why green and red, and why the extra labels?",
 "Green up and red down is the usual convention for share prices, so it is "
 "what anyone reading a market chart expects.\n\n"
 "But red and green are the hardest pair to tell apart for people with "
 "colour blindness, so every bar also carries the direction in words and a "
 "plus or minus sign. The colour is never the only thing telling you which "
 "way the price went."),

("Medium", "Why show turnover in millions rather than the raw number?",
 "Because the raw figures run into the billions of rupees, and an axis "
 "labelled 1500000000 is unreadable. Dividing by a million gives numbers a "
 "person can compare at a glance, and the axis title says the unit."),

("Medium", "What is `cliponaxis=False` for?",
 "Without it, Plotly cuts off any label that reaches past the edge of the "
 "plot. We put the value at the end of each bar, so the longest bar's label "
 "was being clipped. Turning clipping off lets the label draw over the "
 "margin, and we also widen the axis range to leave room."),

("Hard", "What do the summary figures actually tell you about the market?",
 "They give the breadth of the day rather than just the headline. The index "
 "can rise while more companies fall than rise, which happens when a few "
 "large companies pull the average up.\n\n"
 "So we count how many rose, how many fell and how many did not move, "
 "alongside the index. If more fell than rose, the day was broadly negative "
 "even if the index went up - and the written summary says that in plain "
 "words rather than leaving it to the reader."),

("Easy", "Why do you save the image after each cleaning step?",
 "So they can be shown side by side in the OCR tab - the grey version, the "
 "black and white version, and the version after the noise step. It makes "
 "the "
 "preprocessing visible instead of something that just happens invisibly "
 "before the text appears."),

]
