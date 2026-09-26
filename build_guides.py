"""
Builds the study guides and the member documents:

    docs/CSE_Team_Guide.pdf          shared with all four members
    docs/CSE_24ada076_Deep_Guide.pdf the detailed one
    docs/member_documents/           one document for each member
    docs/Speaker_Notes_Slides.pdf    what to say with docs/slides.pptx
    docs/Speaker_Notes_Live_Demo.pdf Plan B - presenting the app live

Helper script, not part of the scraping project itself.
Run:  python build_guides.py            (everything)
      python build_guides.py sasini     (just one member's document)
      python build_guides.py notes      (just the two speaker notes)
"""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from guide_content import common, deep, speaker_notes
from guide_content import pdf_engine as E
from guide_content.q_072 import Q_072
from guide_content.q_073 import Q_073
from guide_content.q_076 import Q_076
from guide_content.q_141 import Q_141
from guide_content.q_general import GENERAL

OUT = config.DOCS_DIR

MEMBER_QUESTIONS = {
    "24ada076": Q_076,
    "25ada072": Q_072,
    "25ada073": Q_073,
    "25ada141": Q_141,
}

LEVELS = ["Easy", "Medium", "Hard"]

FOOTER = "DA 2009 - Assignment 2 - Colombo Stock Exchange"


#=========================================================================#
#  QUESTIONS                                                              #
#=========================================================================#

def question_blocks(member):
    """
    The 50 questions for one member: their own 30, plus the 20 general
    ones everybody should know. Sorted easy first.
    """
    own = [(lvl, q, a, (item[3] if len(item) > 3 else None))
           for item in MEMBER_QUESTIONS[member]
           for lvl, q, a in [item[:3]]]

    shared = [(lvl, q, a, None) for lvl, q, a in GENERAL]

    blocks = []
    number = 0

    for lvl in LEVELS:
        at_this_level = ([x for x in own if x[0] == lvl]
                         + [x for x in shared if x[0] == lvl])
        if not at_this_level:
            continue

        label = {"Easy": "Easy - the basics",
                 "Medium": "Medium - how it works",
                 "Hard": "Harder - explain and defend it"}[lvl]
        blocks += E.level(label)

        for _, q, a, code in at_this_level:
            number += 1
            blocks += E.qa(number, q, a, code)

    return blocks, number


#=========================================================================#
#  THE TEAM GUIDE                                                         #
#=========================================================================#

def team_guide():
    b = []

    b += E.cover(
        "CSE Web Data Collection",
        "Study and viva guide for the whole team",
        [
            "**DA 2009 - Data Collection Methods II**",
            "Assignment 2 (Group Project)",
            "University of Colombo",
            "",
            "**25ada072 - Pasindu  |  25ada073 - Sasini  |  25ada141 - Salaama  |  24ada076 - Nuhan**",
            "",
            "Website: www.cse.lk",
            "",
            "Read the section with your own index number. Then read the "
            "shared sections at the front, because any of it can be asked "
            "of anybody.",
        ])

    b += E.contents()

    #--- About ----------------------------------------------------------#
    b += E.h1("About this guide")
    b += E.p(
        "This is for all four of us. It explains what each person built, in "
        "plain words, and lists the files you should read before the viva.")
    b += E.p("Each member has **50 questions with answers** at the end of "
             "their section: about 30 on your own part, and 20 on the "
             "project as a whole that anybody could be asked.")

    b += E.h2("How the viva works")
    b += E.table([
        ["Part", "Time", "What happens"],
        ["Presentation", "3 minutes",
         "Any number of us can present the project."],
        ["Questions", "5 minutes",
         "Questions on what each member contributed."],
    ], widths=[1.6, 1.2, 5.5])

    b += E.note(
        "The assignment says marks are given for **following ethical "
        "scraping practices** and for **being able to explain your work**. "
        "So knowing why we did something matters as much as knowing what we "
        "did.")

    #--- The project ----------------------------------------------------#
    b += E.h1("What the project does")
    for para in common.WHAT_WE_DO:
        b += E.p(para)
    b += E.bullets(common.WHAT_WE_COLLECT)
    for para in common.WHAT_WE_DO_AFTER:
        b += E.p(para)

    b += E.h2("The problem we had to solve")
    for para in common.THE_PROBLEM:
        b += E.p(para)

    b += E.h2("How we solved it")
    for para in common.THE_SOLUTION:
        b += E.p(para)

    b += E.h2("How a request travels through the project")
    for para in common.THE_FLOW_INTRO:
        b += E.p(para)
    b += E.numbered(common.THE_FLOW)

    #--- Ethics ---------------------------------------------------------#
    b += E.h1("Ethical scraping - everybody should know this")
    for para in common.ETHICS_INTRO:
        b += E.p(para)
    b += E.bullets(common.ETHICS_POINTS)

    #--- Who did what ---------------------------------------------------#
    b += E.h1("Who did what")
    rows = [["Member", "Their part", "Files"]]
    for member in common.MEMBER_ORDER:
        info = config.OWNERSHIP[member]
        rows.append([f"**{config.member_label(member)}**",
                     common.MEMBERS[member]["title"],
                     ", ".join(f"`{m}`" for m in info["modules"])])
    b += E.table(rows, widths=[1.3, 3.2, 4.0])

    b += E.p(
        "`app.py` was put together by all four of us. Each tab in the app "
        "is labelled with the member whose part it shows.")

    #--- Per member -----------------------------------------------------#
    for member in common.MEMBER_ORDER:
        info = common.MEMBERS[member]

        b += E.page_break()
        b += E.h1(f"{config.member_label(member)}: {info['title']}")
        b += E.note(info["one_line"])

        b += E.h2("Your part, explained simply")
        for para in info["simple"]:
            b += E.p(para)

        b += E.h2("Files to read before the viva")
        rows = [["File", "What to look at"]]
        for filename, what in info["files"]:
            rows.append([f"`{filename}`", what])
        b += E.table(rows, widths=[3.0, 5.5])

        b += E.h2("Things you must be able to explain")
        b += E.bullets(info["must_know"])

        qb, count = question_blocks(member)
        b += E.h2(f"{count} questions and answers for "
                   f"{config.member_label(member)}")
        b += E.p(
            "The first group are on your own part. The later ones are about "
            "the project as a whole, and everybody should know them.")
        b += qb

    #--- Reference ------------------------------------------------------#
    b += E.page_break()
    b += E.h1("Quick reference")

    b += E.table([
        ["Thing", "Value"],
        ["Website", "`https://www.cse.lk`"],
        ["Text `requests` finds on the page",
         "about 24 characters, no tables"],
        ["Companies in one request", "around 290"],
        ["Delay between requests", f"{config.DELAY} seconds"],
        ["Section blocked by robots.txt", "`/cgi-bin/` only"],
        ["Crawl-delay CSE asks for", "none"],
        ["Main data address", "`/api/tradeSummary`"],
        ["Where the PDFs live", "`https://cdn.cse.lk/cmt/`"],
        ["PDF libraries", "PyPDF2 and pdfplumber"],
        ["OCR libraries", "PIL, OpenCV, pytesseract"],
        ["OCR resolution", f"{config.OCR_DPI} dpi"],
        ["A page is a scan if it has under",
         f"{config.OCR_TEXT_THRESHOLD} characters"],
        ["Export formats", "CSV, Excel, JSON"],
        ["Request log", "`logs/request_log.csv`"],
    ], widths=[3.4, 5.1])

    b += E.h2("Running each part on its own")
    b += E.code(
        "python -m src.ethics             # 24ada076 - Nuhan\n"
        "python -m src.static_scraper     # 24ada076 - Nuhan\n"
        "python -m src.pdf_extractor      # 24ada076 - Nuhan\n"
        "python -m src.api_client         # 25ada072 - Pasindu\n"
        "python -m src.selenium_scraper   # 25ada072 - Pasindu\n"
        "python -m src.crawler            # 25ada073 - Sasini\n"
        "python -m src.cleaner            # 25ada073 - Sasini\n"
        "python -m src.ocr_extractor      # 25ada141 - Salaama\n"
        "python -m src.storage            # 25ada141 - Salaama\n"
        "python -m src.analysis           # 25ada141 - Salaama")

    b += E.note(
        "Data source: Colombo Stock Exchange (www.cse.lk). Collected for "
        "academic purposes only. This is one trading day. It is not "
        "investment advice.")

    return b


#=========================================================================#
#  THE DEEP GUIDE                                                         #
#=========================================================================#

def deep_guide():
    b = []

    b += E.cover(
        "CSE Web Data Collection",
        "How the project works, in detail",
        [
            "**Written for 24ada076 - Nuhan**",
            "",
            "**DA 2009 - Data Collection Methods II**",
            "Assignment 2 (Group Project)",
            "University of Colombo",
            "",
            "Covers the whole project - the architecture, the pipeline, and "
            "every file - as well as the three files you wrote.",
            "",
            "Your 50 questions are in the shared team guide.",
        ])

    b += E.contents()
    b += deep.build()

    return b


#=========================================================================#
#  THE MEMBER DOCUMENTS                                                   #
#=========================================================================#

# Each member's document is written in its own file in guide_content.
MEMBER_DOCUMENTS = {
    "24ada076": "member_nuhan",
    "25ada072": "member_pasindu",
    "25ada073": "member_sasini",
    "25ada141": "member_salaama",
}


def member_document(member):
    module = importlib.import_module(
        f"guide_content.{MEMBER_DOCUMENTS[member]}")
    folder = OUT / "member_documents"
    folder.mkdir(exist_ok=True)
    path = folder / f"Document_{member}_{config.NAMES[member]}.pdf"
    E.build(path, f"{FOOTER} - {config.member_label(member)}",
            module.build(), toc_depth=1)
    return path


#=========================================================================#
#  THE SPEAKER NOTES                                                      #
#=========================================================================#

def speaker_note_files():
    slides = OUT / "Speaker_Notes_Slides.pdf"
    E.build(slides, FOOTER + " - speaker notes, slides",
            speaker_notes.slides_notes(), toc_depth=1)

    demo = OUT / "Speaker_Notes_Live_Demo.pdf"
    E.build(demo, FOOTER + " - speaker notes, live demo",
            speaker_notes.demo_notes(), toc_depth=1)
    return slides, demo


#=========================================================================#

def show(path):
    print(f"  {path.name:34} {path.stat().st_size / 1024:,.0f} KB")


def main(only=None):
    if only and only.lower() == "notes":
        for path in speaker_note_files():
            show(path)
        return

    # Just one member's document, chosen by name or index number.
    if only:
        for member, name in config.NAMES.items():
            if only.lower() in (member, name.lower()):
                show(member_document(member))
                return
        print(f"No member called {only}")
        return

    team = OUT / "CSE_Team_Guide.pdf"
    E.build(team, FOOTER, team_guide())
    show(team)

    solo = OUT / "CSE_24ada076_Deep_Guide.pdf"
    E.build(solo, FOOTER + " - 24ada076 - Nuhan", deep_guide())
    show(solo)

    for member in MEMBER_DOCUMENTS:
        show(member_document(member))

    for path in speaker_note_files():
        show(path)


if __name__ == "__main__":
    print("Building the study guides")
    print("-" * 55)
    main(sys.argv[1] if len(sys.argv) > 1 else None)
