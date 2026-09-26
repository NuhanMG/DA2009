#=========================================================================#
#  FILE   : src/pdf_extractor.py                                           #
#  PURPOSE: Reads the text out of the announcement PDFs we downloaded.     #
#  OWNER  : 24ada076                                                       #
#                                                                          #
#  There are three kinds of PDF:                                           #
#                                                                          #
#    1. Text-based  - made by a computer. The letters are real text, so    #
#                     we can read them straight out.                       #
#    2. Image-based - a scan or photograph of a page. The letters are      #
#                     part of a picture, so nothing can be extracted and   #
#                     we need OCR instead (see src/ocr_extractor.py).      #
#    3. Hybrid      - a mix of both.                                       #
#                                                                          #
#  We use the two libraries from the lecture:                              #
#                                                                          #
#    PyPDF2      simple text extraction, and the file details              #
#                (page count, title, author).                              #
#    pdfplumber  keeps the layout better and can also find tables.         #
#=========================================================================#

import pandas as pd
import pdfplumber
from PyPDF2 import PdfReader

import config


#-------------------------------------------------------------------------#
#  WORKING OUT WHICH KIND OF PDF WE HAVE                                   #
#-------------------------------------------------------------------------#

def page_type(text):
    """
    Decide whether a page gave us real text or needs OCR.

    A normal page of a CSE circular returns over a thousand characters.
    A scanned page returns nothing at all. We use 50 characters as the
    dividing line rather than zero, because a scan sometimes carries a
    few stray characters that are not the actual document text.
    """
    length = len(text.strip())

    if length < config.OCR_TEXT_THRESHOLD:
        return "Scanned image", f"Only {length} characters - needs OCR"
    return "Text based", f"{length:,} characters read from the page"


#-------------------------------------------------------------------------#
#  METHOD 1 - PyPDF2                                                       #
#-------------------------------------------------------------------------#

def read_with_pypdf2(pdf_path):
    """
    Read a PDF with PyPDF2.

    PyPDF2 is the simpler of the two libraries. It gives us the text and
    the file details, but it does not keep the layout very well and it
    cannot find tables.
    """
    reader = PdfReader(str(pdf_path))

    pages = []
    for number, page in enumerate(reader.pages, start=1):
        # extract_text() returns None on an empty page, so we use "" as
        # a fallback to avoid an error further down.
        text = page.extract_text() or ""
        kind, note = page_type(text)
        pages.append({"Page": number, "Characters": len(text.strip()),
                      "Type": kind, "Note": note, "text": text})

    # PyPDF2 can also read the file details stored inside the PDF.
    details = reader.metadata or {}
    info = {
        "Pages": len(reader.pages),
        "Title": details.get("/Title", "not set"),
        "Author": details.get("/Author", "not set"),
        "Created with": details.get("/Producer", "not set"),
    }

    return pages, info


#-------------------------------------------------------------------------#
#  METHOD 2 - pdfplumber                                                   #
#-------------------------------------------------------------------------#

def read_with_pdfplumber(pdf_path):
    """
    Read a PDF with pdfplumber.

    pdfplumber keeps the layout better than PyPDF2, and it can also pull
    out tables, which is why we use it as our main method.
    """
    pages = []
    tables = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            kind, note = page_type(text)
            pages.append({"Page": number, "Characters": len(text.strip()),
                          "Type": kind, "Note": note, "text": text})

            # Tables come back as a list of rows. The first row is
            # normally the heading.
            for table in (page.extract_tables() or []):
                if len(table) > 1:
                    heading = [
                        (cell if cell else f"Column {i + 1}")
                        for i, cell in enumerate(table[0])
                    ]
                    try:
                        tables.append(pd.DataFrame(table[1:], columns=heading))
                    except Exception:
                        tables.append(pd.DataFrame(table))

    return pages, tables


#-------------------------------------------------------------------------#
#  READING ONE PDF                                                         #
#-------------------------------------------------------------------------#

def read_pdf(pdf_path):
    """
    Read a PDF and report what we found.

    Returns a dictionary with the pages, any tables, the file details,
    and which pages still need OCR.
    """
    pdf_path = str(pdf_path)
    name = pdf_path.replace("\\", "/").split("/")[-1]

    try:
        pages, tables = read_with_pdfplumber(pdf_path)
        _, info = read_with_pypdf2(pdf_path)
    except Exception as e:
        return {"ok": False, "file": name, "error": str(e),
                "pages": [], "tables": [], "info": {},
                "text": "", "scanned_pages": [], "summary": ""}

    all_text = "\n\n".join(
        f"----- Page {p['Page']} -----\n{p['text']}" for p in pages
    )

    scanned = [p["Page"] for p in pages if p["Type"] == "Scanned image"]
    total = sum(p["Characters"] for p in pages)

    if scanned:
        summary = (
            f"{len(pages)} page(s) read. Page(s) "
            f"{', '.join(map(str, scanned))} gave almost no text, so this "
            f"is a scanned document. Use the OCR tab to read it."
        )
    else:
        summary = (
            f"{len(pages)} page(s) read, {total:,} characters extracted. "
            f"Tables found: {len(tables)}."
        )

    return {"ok": True, "file": name, "error": None, "pages": pages,
            "tables": tables, "info": info, "text": all_text,
            "scanned_pages": scanned, "summary": summary}


def pages_table(result):
    """The page by page results, without the long text column."""
    if not result.get("pages"):
        return pd.DataFrame()
    return pd.DataFrame([
        {k: v for k, v in page.items() if k != "text"}
        for page in result["pages"]
    ])


def list_pdfs():
    return sorted(config.PDF_DIR.glob("*.pdf"))


def check_all_pdfs():
    """Look at every PDF we have and say which ones need OCR."""
    rows = []
    for path in list_pdfs():
        result = read_pdf(path)
        if not result["ok"]:
            rows.append({"File": path.name, "Pages": 0, "Characters": 0,
                         "Type": "Could not read", "Needs OCR": "-"})
            continue

        rows.append({
            "File": path.name,
            "Pages": len(result["pages"]),
            "Characters": sum(p["Characters"] for p in result["pages"]),
            "Type": "Scanned image" if result["scanned_pages"] else "Text based",
            "Needs OCR": "Yes" if result["scanned_pages"] else "No",
        })
    return pd.DataFrame(rows)


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.pdf_extractor                  #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    files = list_pdfs()

    if not files:
        print("No PDFs yet. Run:  python -m src.crawler")
    else:
        print("All the PDFs we have downloaded")
        print("-" * 70)
        print(check_all_pdfs().to_string(index=False))

        print()
        print(f"Details for: {files[0].name}")
        print("-" * 70)
        result = read_pdf(files[0])
        print(result["summary"])
        print()
        for key, value in result["info"].items():
            print(f"  {key:14} {value}")
        print()
        print(pages_table(result).to_string(index=False))
        print()
        print("First 400 characters:")
        print(result["text"][:400])
