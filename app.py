#=========================================================================#
#  DA 2009 - Data Collection Methods II | Assignment 2 (Group Project)     #
#  Colombo Stock Exchange (CSE) - Web Data Collection                      #
#                                                                          #
#  FILE   : app.py                                                         #
#  PURPOSE: The screen. Each tab does one job.                             #
#  OWNER  : all four - each tab is labelled with the member whose part    #
#           it shows                                                      #
#                                                                          #
#  Run it with:   python app.py                                            #
#  Then open  :   http://127.0.0.1:7860                                    #
#=========================================================================#

import sys

import gradio as gr
import pandas as pd

import config
from src.analysis import (chart_movers, chart_sectors, chart_turnover,
                          empty_chart, market_figures, summary)
from src.api_client import CSEApi
from src.cleaner import check, clean, compare, describe
from src.crawler import crawl
from src.ethics import ETHICAL_RULES, Scraper
from src.ocr_extractor import ocr_pdf_page, tesseract_ready
from src.pdf_extractor import check_all_pdfs, list_pdfs, pages_table, read_pdf
from src.storage import export, list_exports


#=========================================================================#
#  WHAT THE APP REMEMBERS WHILE IT IS RUNNING                              #
#=========================================================================#

class State:
    def __init__(self):
        self._scraper = None
        self._api = None
        self.trades = pd.DataFrame()      # the data as collected
        self.tidy = pd.DataFrame()        # after cleaning
        self.sectors = pd.DataFrame()
        self.companies = pd.DataFrame()
        self.announcements = pd.DataFrame()
        self.index = {}

    @property
    def scraper(self):
        # Made when first needed, so the app window opens straight away.
        if self._scraper is None:
            self._scraper = Scraper()
        return self._scraper

    @property
    def api(self):
        if self._api is None:
            self._api = CSEApi(scraper=self.scraper)
        return self._api


state = State()


#=========================================================================#
#  HOW IT LOOKS                                                            #
#                                                                          #
#  Dark by default with a light option, because dark backgrounds can look  #
#  washed out on a projector.                                              #
#=========================================================================#

CSS = """
.gradio-container {
    --bg: #0d1117; --panel: #161b22; --line: #30363d;
    --ink: #e6edf3; --faint: #8b949e; --accent: #22d3ee;
    --up: #34d399; --down: #f87171;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif !important;
}

/* The light theme. Gradio keeps its own colours in these variables, so
   they have to be set here as well or the tabs and tables stay dark. */
.gradio-container.light-theme {
    --bg: #ffffff; --panel: #f6f8fa; --line: #d0d7de;
    --ink: #10161d; --faint: #57606a; --accent: #0e7490;
    --up: #047857; --down: #b91c1c;

    --body-text-color: #10161d;
    --body-text-color-subdued: #57606a;
    --body-background-fill: #ffffff;
    --background-fill-primary: #ffffff;
    --background-fill-secondary: #f6f8fa;
    --border-color-primary: #d0d7de;
    --block-background-fill: #ffffff;
    --block-label-text-color: #10161d;
    --block-title-text-color: #10161d;
    --block-border-color: #d0d7de;
    --table-text-color: #10161d;
    --table-border-color: #d0d7de;
    --table-odd-background-fill: #f6f8fa;
    --table-even-background-fill: #ffffff;
    --code-background-fill: #eef1f5;
    --input-background-fill: #ffffff;
    --input-border-color: #d0d7de;
    --link-text-color: #0e7490;
    --color-accent: #0e7490;
    --panel-background-fill: #ffffff;
    --button-secondary-background-fill: #f6f8fa;
    --button-secondary-text-color: #10161d;
    --neutral-950: #ffffff;
    --neutral-900: #f6f8fa;
}
.gradio-container.light-theme .tab-container button { color: #57606a !important; }
.gradio-container.light-theme .tab-container button.selected { color: #0e7490 !important; }
.gradio-container.light-theme code { background: #eef1f5 !important; color: #0b3d4d !important; }

.gradio-container { background: var(--bg) !important; }

.title-bar {
    background: var(--panel);
    border: 1px solid var(--line);
    border-left: 3px solid var(--accent);
    border-radius: 10px; padding: 16px 20px;
}
.title-bar h1 { margin: 0; font-size: 20px; color: var(--ink); }
.title-bar .under { color: var(--faint); font-size: 12.5px; margin-top: 4px; }

.figures { display: flex; flex-wrap: wrap; gap: 10px; margin: 8px 0; }
.figure {
    flex: 1 1 150px; min-width: 140px; background: var(--panel);
    border: 1px solid var(--line); border-radius: 9px; padding: 12px 14px;
}
.figure .name {
    color: var(--faint); font-size: 10.5px;
    text-transform: uppercase; letter-spacing: 0.6px;
}
.figure .amount {
    color: var(--ink); font-size: 21px; font-weight: 600; margin-top: 4px;
    font-family: ui-monospace, Consolas, monospace;
}
.figure .amount.up { color: var(--up); }
.figure .amount.down { color: var(--down); }
.figure .extra { color: var(--faint); font-size: 10.5px; margin-top: 3px; }

.explain {
    background: var(--panel); border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 8px 0;
    color: var(--ink); font-size: 13px; line-height: 1.6;
}
.explain b { color: var(--accent); }
.explain code {
    background: var(--bg); padding: 1px 5px; border-radius: 4px;
    font-family: ui-monospace, Consolas, monospace; font-size: 12px;
}

.owner {
    display: inline-block; margin-bottom: 6px;
    font-family: ui-monospace, Consolas, monospace;
    font-size: 11px; color: var(--faint);
    border: 1px solid var(--line); border-radius: 20px;
    padding: 3px 11px;
}
.owner b { color: var(--accent); font-weight: 600; }

.log textarea {
    background: #05080c !important; color: #7ee787 !important;
    font-family: ui-monospace, Consolas, monospace !important;
    font-size: 11.5px !important; border: 1px solid var(--line) !important;
}
"""

# The button adds or removes one class name, and every colour above is
# written against that class, so the whole screen changes at once.
SWITCH_THEME = """
() => {
    const box = document.querySelector('.gradio-container');
    box.classList.toggle('light-theme');
    return box.classList.contains('light-theme') ? 'Dark theme' : 'Light theme';
}
"""


def figures_html(items):
    """Build the row of headline numbers."""
    blocks = []
    for name, amount, direction, extra in items:
        css = f" {direction}" if direction in ("up", "down") else ""
        note = f"<div class='extra'>{extra}</div>" if extra else ""
        blocks.append(f"<div class='figure'><div class='name'>{name}</div>"
                      f"<div class='amount{css}'>{amount}</div>{note}</div>")
    return f"<div class='figures'>{''.join(blocks)}</div>"


def explain(text):
    return f"<div class='explain'>{text}</div>"


def owner(*members):
    """
    A small label showing whose part of the project this tab is.

    The assignment asks us to keep a note of what each member did, so the
    index number appears on the tab as well as in the table on the Home
    tab and in docs/contributions.md.
    """
    names = " &middot; ".join(f"<b>{config.member_label(m)}</b>"
                              for m in members)
    return f"<div class='owner'>Written by {names}</div>"


#=========================================================================#
#  TAB 2 - ETHICS                                                          #
#=========================================================================#

def show_ethics():
    scraper = state.scraper
    blocked = scraper.blocked_paths()

    rules = pd.DataFrame([{"Rule": name, "What we do": detail}
                          for name, detail in ETHICAL_RULES])

    # With no internet the file cannot be read, and then we send nothing.
    if scraper.robots is None:
        blocked_text = ("could not read robots.txt (no internet?) - so we "
                        "send nothing and show saved copies")
    else:
        blocked_text = ", ".join(blocked) if blocked else "none"

    facts = (
        f"Website          : {config.BASE_URL}\n"
        f"Blocked sections : {blocked_text}\n"
        f"Delay we use     : {config.DELAY} seconds between requests\n"
        f"Our User-Agent   : {config.USER_AGENT}"
    )

    return scraper.robots_text, facts, rules, scraper.log.text()


def show_request_log():
    if not config.REQUEST_LOG.exists():
        return pd.DataFrame(), "No requests sent yet."

    log = pd.read_csv(config.REQUEST_LOG)
    note = (f"{len(log)} requests recorded.\n"
            f"Every row shows the address, the reply, and the delay we "
            f"waited before sending it.")
    return log.tail(200).iloc[::-1], note


#=========================================================================#
#  TAB 3 - MARKET DATA                                                     #
#=========================================================================#

def get_market_data(progress=gr.Progress()):
    state.scraper.log.clear()
    api = state.api

    progress(0.15, "Checking if the market is open")
    status = api.market_status()

    progress(0.35, "Getting the index")
    index = api.aspi()
    state.index = index

    progress(0.6, "Getting the trade summary")
    trades = api.trade_summary()
    state.trades = trades

    progress(0.85, "Getting the sectors")
    sectors = api.sectors()
    state.sectors = sectors

    change = index.get("change", 0) or 0
    counts = market_figures(trades)

    header = figures_html([
        ("Market", status, "", ""),
        ("ASPI index", f"{index.get('value', 0):,.2f}",
         "up" if change > 0 else "down", f"{change:+.2f} today"),
        ("Companies", f"{counts.get('Companies', 0)}", "", "traded today"),
        ("Rose", f"{counts.get('Rose', 0)}", "up", ""),
        ("Fell", f"{counts.get('Fell', 0)}", "down", ""),
        ("Turnover", counts.get("Turnover", "-"), "", "total traded"),
    ])

    addresses = pd.DataFrame([
        {"Address": f"/api/{name}", "Type": spec["method"],
         "What it gives us": spec["desc"]}
        for name, spec in config.ENDPOINTS.items()
    ])

    return header, trades, sectors, addresses, state.scraper.log.text()


#=========================================================================#
#  TAB 4 - COMPANIES                                                       #
#=========================================================================#

def get_company_list():
    companies = state.api.all_companies()
    state.companies = companies

    if companies.empty:
        return gr.update(choices=[]), pd.DataFrame(), state.scraper.log.text()

    choices = [f"{row['symbol']} - {row['name']}"
               for _, row in companies.iterrows()]

    return (gr.update(choices=choices, value=choices[0]),
            companies, state.scraper.log.text())


def get_one_company(choice):
    if not choice:
        return "", pd.DataFrame(), state.scraper.log.text()

    symbol = choice.split(" - ")[0].strip()
    info = state.api.company_info(symbol)

    if not info:
        return (explain("Nothing came back for that company."),
                pd.DataFrame(), state.scraper.log.text())

    change = info.get("change", 0) or 0

    header = figures_html([
        ("Company", str(info.get("name", "-"))[:24], "", symbol),
        ("Price now", f"{info.get('lastTradedPrice', 0):,.2f}",
         "up" if change > 0 else "down", f"{change:+.2f} today"),
        ("Previous close", f"{info.get('previousClose', 0):,.2f}", "", ""),
        ("Market value",
         f"{(info.get('marketCap') or 0) / 1e9:,.1f} bn", "", "rupees"),
        ("Year high", f"{info.get('p12HiPrice', 0):,.2f}", "up", ""),
        ("Year low", f"{info.get('p12LowPrice', 0):,.2f}", "down", ""),
    ])

    details = pd.DataFrame([{"Item": key, "Value": value}
                            for key, value in info.items()])

    return header, details, state.scraper.log.text()


def get_several_companies(how_many, progress=gr.Progress()):
    if state.companies.empty:
        get_company_list()

    if state.companies.empty:
        return pd.DataFrame(), "", state.scraper.log.text()

    symbols = state.companies["symbol"].head(int(how_many)).tolist()

    df = state.api.several_companies(
        symbols, progress=lambda done, text: progress(done, text))

    note = explain(
        f"Collected details for <b>{len(df)}</b> companies.<br><br>"
        f"Each company is a separate request and each one waited "
        f"{config.DELAY} seconds first, which is why this takes a while.")

    return df, note, state.scraper.log.text()


#=========================================================================#
#  TAB 5 - ANNOUNCEMENTS AND PDFs                                          #
#=========================================================================#

def get_announcements():
    state.scraper.log.clear()
    df = state.api.announcements()
    state.announcements = df

    if df.empty:
        return pd.DataFrame(), state.scraper.log.text()

    columns = [c for c in ["dateOfAnnouncement", "company",
                           "announcementCategory"] if c in df.columns]
    return (df[columns] if columns else df), state.scraper.log.text()


def download_pdfs(how_many, progress=gr.Progress()):
    found, downloaded = crawl(
        limit=int(how_many), api=state.api,
        progress=lambda done, text: progress(done, text))

    return (found[["Title", "Date"]] if not found.empty else pd.DataFrame(),
            downloaded, refresh_pdfs()[0], check_all_pdfs(),
            state.scraper.log.text())


def refresh_pdfs():
    names = [p.name for p in list_pdfs()]
    return (gr.update(choices=names, value=names[0] if names else None),
            check_all_pdfs())


def read_one_pdf(filename):
    if not filename:
        return "", pd.DataFrame(), "", pd.DataFrame()

    result = read_pdf(config.PDF_DIR / filename)

    if not result["ok"]:
        return explain(f"Could not read it: {result['error']}"), \
            pd.DataFrame(), "", pd.DataFrame()

    details = pd.DataFrame([{"Item": k, "Value": v}
                            for k, v in result["info"].items()])

    if result["scanned_pages"]:
        note = explain(
            f"{result['summary']}<br><br>"
            f"This document is a scan, so there is no text inside it to "
            f"pull out. Use the <b>OCR</b> tab to read it.")
    else:
        note = explain(result["summary"])

    return note, pages_table(result), result["text"][:6000], details


#=========================================================================#
#  TAB 6 - OCR                                                             #
#=========================================================================#

def ocr_status():
    ready, message = tesseract_ready()
    return explain(message.replace("\n", "<br>"))


def scanned_pdf_choices():
    """Only offer the PDFs that actually need OCR."""
    names = []
    for path in list_pdfs():
        result = read_pdf(path)
        if result["ok"] and result["scanned_pages"]:
            names.append(path.name)

    # If none of them are scans, offer them all so the tab still works.
    if not names:
        names = [p.name for p in list_pdfs()]

    return gr.update(choices=names, value=names[0] if names else None)


def run_ocr(filename, dpi, progress=gr.Progress()):
    blank = (None, None, None)

    if not filename:
        return explain("Choose a document first."), *blank, "", pd.DataFrame()

    # Read the first page that has no text. In a hybrid PDF - some pages
    # typed, some scanned - that is not necessarily page 1.
    checked = read_pdf(config.PDF_DIR / filename)
    page = (checked["scanned_pages"] or [1])[0] if checked["ok"] else 1

    progress(0.2, f"Turning page {page} into an image")
    result = ocr_pdf_page(config.PDF_DIR / filename, page_number=page,
                          dpi=int(dpi))

    if not result["ok"]:
        return (explain(result["error"].replace("\n", "<br>")),
                *blank, "", pd.DataFrame())

    progress(0.9, "Reading the text")

    note = explain(
        f"Read <b>{result['characters']:,} characters</b> from page "
        f"{result['page']}, "
        f"at {result['dpi']} dpi.<br>"
        f"Tesseract was on average <b>{result['average_confidence']}%</b> "
        f"confident about each word.<br><br>"
        f"OCR is not perfect. Words with a low confidence score are the "
        f"ones worth checking by hand.")

    steps = result["steps"]
    return (note, steps["grey"], steps["threshold"], steps["cleaned"],
            result["text"], result["words"].nsmallest(12, "Confidence"))


#=========================================================================#
#  TAB 7 - DATA AND EXPORT                                                 #
#=========================================================================#

def clean_data():
    if state.trades.empty:
        return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
                explain("Get the market data first, on the Market Data tab."))

    before = describe(state.trades)
    tidy, changes = clean(state.trades)
    state.tidy = tidy
    after = describe(tidy)

    note = explain(
        "<b>What we changed:</b><ul>"
        + "".join(f"<li>{c}</li>" for c in changes)
        + "</ul>")

    return compare(before, after), tidy.head(25), check(tidy), note


def draw_charts(dark):
    df = state.tidy if not state.tidy.empty else state.trades

    if df.empty:
        blank = empty_chart("Get the market data first", dark)
        return blank, blank, blank, "No data yet."

    return (chart_movers(df, dark=dark),
            chart_turnover(df, dark=dark),
            chart_sectors(state.sectors, dark=dark),
            summary(df, state.index))


def save_files(datasets, formats):
    choices = {
        "Share prices": ("cse_share_prices",
                         state.tidy if not state.tidy.empty else state.trades),
        "Sectors": ("cse_sectors", state.sectors),
        "Companies": ("cse_companies", state.companies),
        "Announcements": ("cse_announcements", state.announcements),
    }

    saved = []
    for label in datasets:
        name, df = choices.get(label, (None, pd.DataFrame()))
        if name and df is not None and not df.empty:
            saved += export(df, name, formats=[f.lower() for f in formats])

    if not saved:
        return (list_exports(),
                explain("Nothing was saved - those tables are still empty. "
                        "Collect some data first."), None)

    return (list_exports(),
            explain(f"Saved <b>{len(saved)}</b> file(s). Each one names the "
                    f"Colombo Stock Exchange as the source and records when "
                    f"the data was collected."),
            [str(p) for p in saved])


#=========================================================================#
#  BUILDING THE SCREEN                                                     #
#=========================================================================#

def build_app():
    with gr.Blocks(title="CSE Data Collection") as app:

        with gr.Row():
            with gr.Column(scale=6):
                gr.HTML(
                    "<div class='title-bar'>"
                    "<h1>Colombo Stock Exchange &mdash; Web Data Collection</h1>"
                    "<div class='under'>DA 2009 &middot; Assignment 2 "
                    "&middot; "
                    + " &nbsp;|&nbsp; ".join(config.member_label(m)
                                             for m in config.TEAM)
                    + "</div></div>")
            with gr.Column(scale=1, min_width=130):
                theme_button = gr.Button("Light theme", size="sm")

        dark = gr.State(True)

        with gr.Tabs():

            #=============================================================#
            #  HOME                                                       #
            #=============================================================#
            with gr.Tab("Home"):
                gr.HTML(explain(
                    "We collect share prices, company details and "
                    "announcements from the Colombo Stock Exchange "
                    "(<code>www.cse.lk</code>).<br><br>"
                    "The website builds its pages with JavaScript, so the "
                    "prices are not in the HTML that <code>requests</code> "
                    "downloads. We found the addresses the site itself uses "
                    "to load its data by opening it in a browser and looking "
                    "at the Network tab, and we read those addresses "
                    "instead. They return JSON, which pandas can read "
                    "directly.<br><br>"
                    "Announcements come with PDF documents attached. Most of "
                    "them we can read straight away. Some are scans, and "
                    "those need OCR."))

                gr.Markdown("### Who did what")
                gr.Dataframe(
                    value=pd.DataFrame([
                        {"Member": config.member_label(member),
                         "Part of the project": info["role"],
                         "Files": ", ".join(info["modules"])}
                        for member, info in config.OWNERSHIP.items()
                    ]),
                    wrap=True, interactive=False)

                gr.Markdown(
                    "The app itself was put together by all four of us. "
                    "Each tab is labelled with the member whose part it "
                    "shows.\n\n"
                    "Start on the **Ethics** tab, then **Market Data**."
                )

            #=============================================================#
            #  ETHICS                                                     #
            #=============================================================#
            with gr.Tab("Ethics"):
                gr.HTML(owner("24ada076"))
                gr.HTML(explain(
                    "Before collecting anything we read the website's "
                    "<code>robots.txt</code> file, which tells automated "
                    "programs which pages they may visit. Every address we "
                    "request is checked against it first."))

                ethics_button = gr.Button("Read robots.txt", variant="primary")

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### The file as CSE publishes it")
                        robots_box = gr.Code(label="robots.txt", lines=6)
                    with gr.Column():
                        gr.Markdown("#### Our settings")
                        settings_box = gr.Textbox(show_label=False, lines=6)

                gr.Markdown("#### The rules we follow")
                rules_table = gr.Dataframe(wrap=True, interactive=False)

                gr.Markdown("#### Every request we have sent")
                log_button = gr.Button("Show the request log")
                log_note = gr.Textbox(show_label=False, lines=3)
                log_table = gr.Dataframe(max_height=320, interactive=False)

                ethics_log = gr.Textbox(label="Messages", lines=5,
                                        elem_classes="log")

            #=============================================================#
            #  MARKET DATA                                                #
            #=============================================================#
            with gr.Tab("Market Data"):
                gr.HTML(owner("25ada072"))
                gr.HTML(explain(
                    "Today's trading for every company listed on the "
                    "exchange, plus the market index and the sector "
                    "indices."))

                market_button = gr.Button("Get the market data",
                                          variant="primary")
                market_figures_html = gr.HTML()

                with gr.Tabs():
                    with gr.Tab("Share prices"):
                        trades_table = gr.Dataframe(max_height=420,
                                                    interactive=False)
                    with gr.Tab("Sectors"):
                        sectors_table = gr.Dataframe(max_height=420,
                                                     interactive=False)

                with gr.Accordion("The addresses we read the data from",
                                  open=False):
                    addresses_table = gr.Dataframe(wrap=True,
                                                   interactive=False)

                market_log = gr.Textbox(label="Messages", lines=6,
                                        elem_classes="log")

            #=============================================================#
            #  COMPANIES                                                  #
            #=============================================================#
            with gr.Tab("Companies"):
                gr.HTML(owner("25ada072"))
                gr.HTML(explain(
                    "Details for one company at a time. This address needs "
                    "the company symbol sent with the request, for example "
                    "<code>symbol=SAMP.N0000</code>."))

                list_button = gr.Button("Load the company list")

                with gr.Row():
                    company_choice = gr.Dropdown(label="Company", choices=[],
                                                 scale=4)
                    company_button = gr.Button("Get details", scale=1)

                company_figures = gr.HTML()

                with gr.Row():
                    company_details = gr.Dataframe(label="All the details",
                                                   max_height=360,
                                                   interactive=False)
                    company_list = gr.Dataframe(label="Every listed company",
                                                max_height=360,
                                                interactive=False)

                gr.Markdown("#### Several companies at once")
                with gr.Row():
                    how_many = gr.Slider(5, 50, value=15, step=5, scale=3,
                                         label="How many companies")
                    many_button = gr.Button("Collect them", scale=1)
                many_note = gr.HTML()
                many_table = gr.Dataframe(max_height=300, interactive=False)

                company_log = gr.Textbox(label="Messages", lines=5,
                                         elem_classes="log")

            #=============================================================#
            #  ANNOUNCEMENTS                                              #
            #=============================================================#
            with gr.Tab("Announcements"):
                gr.HTML(owner("25ada073", "24ada076"))
                gr.HTML(explain(
                    "Company announcements, and the PDF documents attached "
                    "to them. We do not know in advance which documents "
                    "exist, so we read the list, work out the address of "
                    "each PDF, and then download them one at a time."))

                announce_button = gr.Button("Get the announcements",
                                            variant="primary")
                announce_table = gr.Dataframe(max_height=280,
                                              interactive=False)

                gr.Markdown("#### Download the documents")
                with gr.Row():
                    pdf_count = gr.Slider(1, 10, value=5, step=1, scale=3,
                                          label="How many to download")
                    download_button = gr.Button("Download", scale=1)

                with gr.Row():
                    found_table = gr.Dataframe(label="Documents found",
                                               max_height=240,
                                               interactive=False)
                    downloaded_table = gr.Dataframe(label="Downloaded",
                                                    max_height=240,
                                                    interactive=False)

                gr.Markdown("#### Read the text out of a document")
                gr.HTML(explain(
                    "We use <b>pdfplumber</b> to read the text, because it "
                    "keeps the layout better than PyPDF2 and can also find "
                    "tables. <b>PyPDF2</b> gives us the file details."))

                pdf_overview = gr.Dataframe(label="The documents we have",
                                            interactive=False)

                with gr.Row():
                    pdf_choice = gr.Dropdown(label="Document", choices=[],
                                             scale=4)
                    read_button = gr.Button("Read the text", scale=1)

                pdf_note = gr.HTML()
                with gr.Row():
                    pdf_pages = gr.Dataframe(label="Page by page", scale=2,
                                             interactive=False)
                    pdf_details = gr.Dataframe(label="File details", scale=1,
                                               interactive=False)
                pdf_text = gr.Textbox(label="The text we extracted", lines=14)

                announce_log = gr.Textbox(label="Messages", lines=5,
                                          elem_classes="log")

            #=============================================================#
            #  OCR                                                        #
            #=============================================================#
            with gr.Tab("OCR"):
                gr.HTML(owner("25ada141"))
                gr.HTML(explain(
                    "Some of the announcement PDFs are scans - photographs "
                    "of a printed page. There is no text inside them to pull "
                    "out, so nothing is returned no matter which library we "
                    "use.<br><br>"
                    "OCR reads the picture instead. There are four steps: "
                    "turn the page into an image, clean the image up, read "
                    "the letters, then tidy the result."))

                ocr_engine_note = gr.HTML()

                with gr.Row():
                    ocr_choice = gr.Dropdown(label="Scanned document",
                                             choices=[], scale=3)
                    ocr_dpi = gr.Slider(100, 300, value=config.OCR_DPI,
                                        step=50, scale=2,
                                        label="Image detail (dpi)")
                    ocr_button = gr.Button("Read it", variant="primary",
                                           scale=1)

                ocr_note = gr.HTML()

                gr.Markdown("#### Step 2 - cleaning the image up for OCR")
                with gr.Row():
                    image_grey = gr.Image(label="1. Colour removed",
                                          height=260)
                    image_threshold = gr.Image(label="2. Black and white",
                                               height=260)
                    image_clean = gr.Image(label="3. After the noise step",
                                           height=260)

                gr.Markdown("#### Steps 3 and 4 - the text we recovered")
                with gr.Row():
                    ocr_text = gr.Textbox(label="Text read from the image",
                                          lines=16, scale=2)
                    ocr_words = gr.Dataframe(
                        label="Least confident words", scale=1,
                        interactive=False)

            #=============================================================#
            #  DATA AND EXPORT                                            #
            #=============================================================#
            with gr.Tab("Data & Export"):
                gr.HTML(owner("25ada073", "25ada141"))
                gr.HTML(explain(
                    "Data taken from a website is not ready to use straight "
                    "away. Dates arrive as very large numbers, some numbers "
                    "arrive as text, and some columns are empty for every "
                    "company. This tab fixes those, checks the result, and "
                    "saves it."))

                clean_button = gr.Button("Clean and check", variant="primary")
                clean_note = gr.HTML()

                with gr.Row():
                    clean_compare = gr.Dataframe(label="Before and after",
                                                 interactive=False)
                    clean_checks = gr.Dataframe(label="Checks",
                                                interactive=False)
                clean_table = gr.Dataframe(label="The cleaned data",
                                           max_height=300, interactive=False)

                gr.Markdown("#### Charts")
                chart_button = gr.Button("Draw the charts")
                chart_words = gr.Textbox(label="What the numbers show",
                                         lines=4)
                with gr.Row():
                    chart_one = gr.Plot()
                    chart_two = gr.Plot()
                chart_three = gr.Plot()

                gr.Markdown("#### Save the data")
                with gr.Row():
                    which_data = gr.CheckboxGroup(
                        ["Share prices", "Sectors", "Companies",
                         "Announcements"],
                        value=["Share prices"], label="What to save")
                    which_format = gr.CheckboxGroup(
                        ["CSV", "Excel", "JSON"],
                        value=["CSV", "Excel", "JSON"], label="File type")

                save_button = gr.Button("Save", variant="primary")
                save_note = gr.HTML()
                save_files_box = gr.File(label="Download",
                                         file_count="multiple")
                saved_table = gr.Dataframe(label="Files saved so far",
                                           interactive=False)

        #=================================================================#
        #  CONNECTING THE BUTTONS                                         #
        #=================================================================#

        theme_button.click(fn=None, outputs=theme_button, js=SWITCH_THEME)
        theme_button.click(lambda now: not now, inputs=dark, outputs=dark)

        ethics_button.click(show_ethics,
                            outputs=[robots_box, settings_box, rules_table,
                                     ethics_log])
        log_button.click(show_request_log, outputs=[log_table, log_note])

        market_button.click(get_market_data,
                            outputs=[market_figures_html, trades_table,
                                     sectors_table, addresses_table,
                                     market_log])

        list_button.click(get_company_list,
                          outputs=[company_choice, company_list, company_log])
        company_button.click(get_one_company, inputs=company_choice,
                             outputs=[company_figures, company_details,
                                      company_log])
        many_button.click(get_several_companies, inputs=how_many,
                          outputs=[many_table, many_note, company_log])

        announce_button.click(get_announcements,
                              outputs=[announce_table, announce_log])
        download_button.click(download_pdfs, inputs=pdf_count,
                              outputs=[found_table, downloaded_table,
                                       pdf_choice, pdf_overview,
                                       announce_log])
        read_button.click(read_one_pdf, inputs=pdf_choice,
                          outputs=[pdf_note, pdf_pages, pdf_text,
                                   pdf_details])

        ocr_button.click(run_ocr, inputs=[ocr_choice, ocr_dpi],
                         outputs=[ocr_note, image_grey, image_threshold,
                                  image_clean, ocr_text, ocr_words])

        clean_button.click(clean_data,
                           outputs=[clean_compare, clean_table, clean_checks,
                                    clean_note])
        chart_button.click(draw_charts, inputs=dark,
                           outputs=[chart_one, chart_two, chart_three,
                                    chart_words])
        save_button.click(save_files, inputs=[which_data, which_format],
                          outputs=[saved_table, save_note, save_files_box])

        #--- Things we can show without sending any requests --------------#
        app.load(refresh_pdfs, outputs=[pdf_choice, pdf_overview])
        app.load(scanned_pdf_choices, outputs=ocr_choice)
        app.load(ocr_status, outputs=ocr_engine_note)
        app.load(show_request_log, outputs=[log_table, log_note])

    return app


if __name__ == "__main__":
    print("=" * 55)
    print("  CSE Data Collection - DA 2009 Assignment 2")
    print(f"  Open http://127.0.0.1:{config.APP_PORT}")
    print("=" * 55)

    build_app().launch(
        server_name="127.0.0.1", server_port=config.APP_PORT,
        # "python app.py --open" opens the browser as soon as the app is
        # ready. 2_START_The_App.bat starts it this way.
        inbrowser="--open" in sys.argv, show_error=True,
        # Gradio 6 takes the theme and stylesheet here rather than in
        # gr.Blocks().
        theme=gr.themes.Base(), css=CSS)
