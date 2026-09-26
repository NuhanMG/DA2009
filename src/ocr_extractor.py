#=========================================================================#
#  FILE   : src/ocr_extractor.py                                           #
#  PURPOSE: Reads scanned PDF pages, where there is no text to extract.    #
#  OWNER  : 25ada141                                                       #
#                                                                          #
#  OCR means Optical Character Recognition - turning a picture of text     #
#  into text the computer can actually use.                                #
#                                                                          #
#  We follow the four step OCR pipeline from the lecture:                  #
#                                                                          #
#    1. IMAGE ACQUISITION   turn the PDF page into an image        (PIL)   #
#    2. PREPROCESSING       make the text easier to read        (OpenCV)   #
#    3. TEXT RECOGNITION    read the letters               (pytesseract)   #
#    4. POST-PROCESSING     tidy the text and save it          (pandas)    #
#                                                                          #
#  Preprocessing matters more than people expect. Tesseract works best on  #
#  plain black text on a white background, so we convert the page to grey  #
#  and then to pure black and white before reading it.                     #
#=========================================================================#

import shutil
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image

import config

# The Tesseract installer puts the program in C:\Program Files\Tesseract-OCR
# but does not always add it to the PATH, so pytesseract cannot find it.
# If it is in that usual place, we tell pytesseract where to look.
_USUAL_PLACE = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if shutil.which("tesseract") is None and _USUAL_PLACE.exists():
    pytesseract.pytesseract.tesseract_cmd = str(_USUAL_PLACE)


#-------------------------------------------------------------------------#
#  IS TESSERACT INSTALLED?                                                 #
#                                                                          #
#  pytesseract is only a small Python wrapper. The actual OCR is done by   #
#  the Tesseract program, which has to be installed separately on Windows. #
#  Importing pytesseract works even when Tesseract is missing, so we ask   #
#  it for its version number to find out for certain.                      #
#-------------------------------------------------------------------------#

INSTALL_HELP = (
    "Tesseract is not installed on this computer.\n\n"
    "The easy way: close this app, double-click "
    "1_SETUP_First_Time_Only.bat and press Y when it asks about "
    "Tesseract.\n\n"
    "Or install it by hand:\n"
    "  1. Download it from "
    "https://github.com/UB-Mannheim/tesseract/wiki\n"
    "  2. Install it to C:\\Program Files\\Tesseract-OCR\\\n"
    "  3. Restart this app\n\n"
    "The Python part (pip install pytesseract) is already done."
)


def tesseract_ready():
    """Returns (True or False, a message to show the user)."""
    try:
        version = pytesseract.get_tesseract_version()
        return True, f"Tesseract {version} is installed and ready."
    except Exception:
        return False, INSTALL_HELP


#-------------------------------------------------------------------------#
#  STEP 1 - IMAGE ACQUISITION                                              #
#-------------------------------------------------------------------------#

def pdf_page_to_image(pdf_path, page_number=1, dpi=None):
    """
    Turn one page of a PDF into an image file.

    OCR reads pictures, not PDFs, so the page has to become an image
    first. pdfplumber can do this with to_image().

    The dpi setting controls how large the image is. Higher numbers give
    Tesseract more detail to work with but take longer:
        72 dpi   screen size, small print becomes unreadable
        200 dpi  our setting, good for printed documents
        300 dpi  better for very small print, slower
    """
    dpi = dpi or config.OCR_DPI
    pdf_path = str(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:
        if page_number < 1 or page_number > len(pdf.pages):
            return None, f"This PDF has {len(pdf.pages)} page(s)."

        page_image = pdf.pages[page_number - 1].to_image(resolution=dpi)

        name = pdf_path.replace("\\", "/").split("/")[-1].replace(".pdf", "")
        image_path = config.IMAGE_DIR / f"{name}_page{page_number}.png"
        page_image.save(str(image_path))

    return str(image_path), None


#-------------------------------------------------------------------------#
#  STEP 2 - PREPROCESSING WITH OPENCV                                      #
#-------------------------------------------------------------------------#

def preprocess_image(image_path):
    """
    Clean up the image so Tesseract can read it more accurately.

    Three steps, each saved so we can show them in the app:

      grayscale   colour tells us nothing about which letter this is, and
                  removing it leaves one brightness value per pixel
                  instead of three colour values.

      threshold   turns every pixel either pure black or pure white, so
                  the letters have hard edges. We use adaptive
                  thresholding, which works out the cut-off separately
                  for each part of the page - useful for a scan where
                  one side is darker than the other.

      noise step  the optional noise removal step from the lecture's
                  OCR example, which uses a 1x1 kernel. A 1x1 kernel
                  changes nothing - we measured it: 0 pixels different.
                  We keep it so our pipeline matches the lecture, and
                  because this is the place to tune it. Scanner specks
                  are BLACK dots on a WHITE page, so removing them would
                  need MORPH_CLOSE with a 2x2 or 3x3 kernel - but a
                  bigger kernel can also rub out thin parts of letters,
                  so it has to be tested before it is changed.
    """
    base = str(image_path).replace(".png", "")

    # cv2.imread loads the image as a grid of numbers.
    image = cv2.imread(str(image_path))
    if image is None:
        return None, "Could not open the image."

    # Colour to grey.
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grey_path = f"{base}_1_grey.png"
    cv2.imwrite(grey_path, grey)

    # Grey to pure black and white.
    threshold = cv2.adaptiveThreshold(
        grey, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2,
    )
    threshold_path = f"{base}_2_threshold.png"
    cv2.imwrite(threshold_path, threshold)

    # The lecture's optional noise removal step. With a 1x1 kernel it
    # leaves the image exactly as it was (see the note above).
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    cleaned_path = f"{base}_3_cleaned.png"
    cv2.imwrite(cleaned_path, cleaned)

    steps = {"grey": grey_path, "threshold": threshold_path,
             "cleaned": cleaned_path}

    return cleaned, steps


#-------------------------------------------------------------------------#
#  STEP 3 - TEXT RECOGNITION WITH PYTESSERACT                              #
#-------------------------------------------------------------------------#

def read_text(image_array):
    """
    Read the text out of a prepared image.

    OpenCV gives us a numpy array. We turn it into a PIL image with
    Image.fromarray(), which is how the lecture passed images to
    pytesseract, so each library gets the kind of image it is used to.
    """
    pil_image = Image.fromarray(image_array)
    return pytesseract.image_to_string(pil_image)


def read_words_with_confidence(image_array):
    """
    Get each word separately along with how confident Tesseract is.

    image_to_data gives us far more than image_to_string: the position of
    every word and a confidence score from 0 to 100. Low scores are a
    useful warning that a word was probably misread.
    """
    pil_image = Image.fromarray(image_array)
    data = pytesseract.image_to_data(
        pil_image, output_type=pytesseract.Output.DICT)

    rows = []
    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        confidence = int(data["conf"][i])
        if word and confidence > 0:
            rows.append({"Word": word, "Confidence": confidence})

    return pd.DataFrame(rows)


#-------------------------------------------------------------------------#
#  STEP 4 - POST-PROCESSING                                                #
#-------------------------------------------------------------------------#

def text_to_lines(text):
    """
    Tidy the OCR output and put it into a DataFrame.

    OCR output arrives as one long string with blank lines in it. Turning
    it into a table makes it easier to check and to save as CSV or Excel.
    """
    lines = [line.strip() for line in text.strip().split("\n")]
    lines = [line for line in lines if line]

    return pd.DataFrame({
        "Line": range(1, len(lines) + 1),
        "Text": lines,
    })


#-------------------------------------------------------------------------#
#  THE WHOLE PIPELINE                                                      #
#-------------------------------------------------------------------------#

def ocr_pdf_page(pdf_path, page_number=1, dpi=None):
    """
    Run all four steps on one page of a PDF.

    Returns a dictionary with the text, the tidied lines, the word
    confidences, and the file paths of each preprocessing step so the app
    can show them.
    """
    ready, message = tesseract_ready()
    if not ready:
        return {"ok": False, "error": message}

    #--- Step 1 -------------------------------------------------------#
    image_path, error = pdf_page_to_image(pdf_path, page_number, dpi)
    if image_path is None:
        return {"ok": False, "error": error}

    #--- Step 2 -------------------------------------------------------#
    prepared, steps = preprocess_image(image_path)
    if prepared is None:
        return {"ok": False, "error": steps}

    #--- Step 3 -------------------------------------------------------#
    try:
        text = read_text(prepared)
        words = read_words_with_confidence(prepared)
    except Exception as e:
        return {"ok": False, "error": f"Tesseract failed: {e}"}

    #--- Step 4 -------------------------------------------------------#
    lines = text_to_lines(text)

    average_confidence = (round(words["Confidence"].mean(), 1)
                          if not words.empty else 0)

    return {
        "ok": True,
        "error": None,
        "page": page_number,
        "dpi": dpi or config.OCR_DPI,
        "original_image": image_path,
        "steps": steps,
        "text": text,
        "lines": lines,
        "words": words,
        "characters": len(text.strip()),
        "average_confidence": average_confidence,
    }


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.ocr_extractor                  #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    from src.pdf_extractor import list_pdfs, read_pdf

    ready, message = tesseract_ready()
    print(message)
    print()

    if not ready:
        raise SystemExit(0)

    # Find a PDF that actually needs OCR.
    target = None
    page = 1
    for pdf in list_pdfs():
        result = read_pdf(pdf)
        if result["ok"] and result["scanned_pages"]:
            target = pdf
            page = result["scanned_pages"][0]
            break

    if target is None:
        print("None of the PDFs we have need OCR.")
        raise SystemExit(0)

    print(f"This PDF is a scan and gave us no text: {target.name}")
    print(f"Running OCR on page {page}")
    print("-" * 60)

    result = ocr_pdf_page(target, page)

    if not result["ok"]:
        print("OCR failed:", result["error"])
    else:
        print(f"Characters read   : {result['characters']:,}")
        print(f"Average confidence: {result['average_confidence']}%")
        print(f"Resolution        : {result['dpi']} dpi")
        print()
        print("Text found")
        print("-" * 60)
        print(result["text"][:900])
        print()
        print("Least confident words - these are the ones to check by hand")
        print("-" * 60)
        print(result["words"].nsmallest(8, "Confidence").to_string(index=False))
