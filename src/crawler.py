#=========================================================================#
#  FILE   : src/crawler.py                                                 #
#  PURPOSE: Finds the announcement PDFs on the CSE website and downloads   #
#           them.                                                          #
#  OWNER  : 25ada073                                                       #
#                                                                          #
#  Scraping means taking data from a page we already know about. Crawling  #
#  means finding pages by following links.                                 #
#                                                                          #
#  This file crawls. We do not know which documents exist, so we read the  #
#  list of circulars, work out the address of each PDF, and then follow    #
#  those addresses to download the files.                                  #
#                                                                          #
#  The list only gives part of the address, like                           #
#      upload_report_file/abc123.pdf                                       #
#  and the PDFs are kept on a different server to the website, so we add   #
#  https://cdn.cse.lk/cmt/ in front of it to make a full link.             #
#=========================================================================#

import pandas as pd

import config
from src.api_client import CSEApi
from src.ethics import Scraper
from src.storage import save_pdf


#-------------------------------------------------------------------------#
#  STEP 1 - FIND THE DOCUMENTS                                             #
#-------------------------------------------------------------------------#

def find_documents(api=None):
    """
    Build a list of the PDFs available, without downloading anything yet.
    """
    api = api or CSEApi()
    found = []

    circulars = api.circulars()
    for _, row in circulars.iterrows():
        found.append({
            "Title": str(row.get("fileText", "Untitled")).strip(),
            "Date": row.get("uploadedDate", ""),
            "url": row.get("pdf_url"),
            "id": row.get("id"),
        })

    df = pd.DataFrame(found)

    # The same document can appear twice in the list. Downloading it twice
    # would waste the website's bandwidth for no benefit.
    if not df.empty:
        df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)

    api.scraper.log.add(f"Found {len(df)} documents to download")
    return df


#-------------------------------------------------------------------------#
#  STEP 2 - DOWNLOAD THEM                                                  #
#-------------------------------------------------------------------------#

def download_documents(documents, limit=5, scraper=None, progress=None):
    """
    Download the PDFs, one at a time, with a pause between each.

    We use a limit because there are far more documents on the site than
    we need. Downloading everything just because we can would put load on
    their server for no reason.
    """
    scraper = scraper or Scraper()

    if documents is None or documents.empty:
        return pd.DataFrame()

    wanted = documents.head(limit)
    results = []

    for number, (_, row) in enumerate(wanted.iterrows(), start=1):
        if progress:
            progress(number / len(wanted),
                     f"Downloading {number} of {len(wanted)}")

        title = row["Title"]
        filename = f"{row.get('id', number)}_{title[:60]}"

        # Skip anything we already have.
        existing = list(config.PDF_DIR.glob(f"{row.get('id', '')}_*.pdf"))
        if existing and str(row.get("id", "")):
            results.append({"Title": title[:65], "Result": "Already saved",
                            "File": existing[0].name})
            continue

        reply = scraper.fetch(row["url"], want="bytes")

        if not reply["ok"]:
            results.append({"Title": title[:65],
                            "Result": f"Failed: {reply['error']}",
                            "File": "-"})
            continue

        content = reply["data"]

        # Every PDF file starts with the characters %PDF. If ours does
        # not, we received something else and should not save it.
        if not content[:4] == b"%PDF":
            results.append({"Title": title[:65],
                            "Result": "Not a PDF file", "File": "-"})
            continue

        path = save_pdf(content, filename)
        results.append({"Title": title[:65], "Result": "Downloaded",
                        "File": path.name})

    return pd.DataFrame(results)


#-------------------------------------------------------------------------#
#  BOTH STEPS TOGETHER                                                     #
#-------------------------------------------------------------------------#

def crawl(limit=5, api=None, progress=None):
    api = api or CSEApi()
    documents = find_documents(api)
    downloaded = download_documents(documents, limit=limit,
                                    scraper=api.scraper, progress=progress)
    return documents, downloaded


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.crawler                        #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    api = CSEApi()

    print("Step 1 - finding documents")
    print("-" * 60)
    documents, downloaded = crawl(limit=5, api=api)
    if not documents.empty:
        print(documents[["Title", "Date"]].to_string(index=False))

    print()
    print("Step 2 - downloading them")
    print("-" * 60)
    if not downloaded.empty:
        print(downloaded.to_string(index=False))

    print()
    print(api.scraper.log.text())
