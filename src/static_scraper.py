#=========================================================================#
#  FILE   : src/static_scraper.py                                          #
#  PURPOSE: Scraping a page with requests and BeautifulSoup.               #
#  OWNER  : 24ada076                                                       #
#                                                                          #
#  This was the first thing we tried on the CSE website, and it is worth   #
#  keeping because of what it shows.                                       #
#                                                                          #
#  requests downloads the HTML file and stops there. It does not run the   #
#  JavaScript on the page. The CSE website builds its tables with          #
#  JavaScript after the page loads, so the HTML we download is almost      #
#  empty - about 25,000 bytes of code holding hardly any words.            #
#                                                                          #
#  That is why the rest of the project reads the data from the address     #
#  the page itself uses (see src/api_client.py) instead of the HTML.       #
#                                                                          #
#  BeautifulSoup is not the problem here. The second part of this file     #
#  uses the same library on the sitemap, which is an ordinary file, and    #
#  it reads it without any trouble.                                        #
#                                                                          #
#  Run it with:  python -m src.static_scraper                              #
#=========================================================================#

import pandas as pd
from bs4 import BeautifulSoup

import config
from src.ethics import Scraper


#-------------------------------------------------------------------------#
#  SCRAPING A PAGE                                                         #
#-------------------------------------------------------------------------#

def scrape_page(url=None, scraper=None):
    """
    Download a page and count what BeautifulSoup can find in it.
    """
    scraper = scraper or Scraper()
    url = url or config.PAGES["trade_summary"]

    # The request goes through the same fetch() as everything else, so
    # robots.txt is checked, the delay is applied and it is logged.
    # want="text" gives us the HTML as a string instead of JSON.
    reply = scraper.fetch(url, want="text")

    if not reply["ok"]:
        return {"url": url, "status": None, "error": reply["error"],
                "html_size": 0, "words": 0, "tables": 0, "links": 0,
                "title": "", "sample": "", "html": ""}

    html = reply["data"]
    status = 200          # fetch() only says ok when the reply was 200

    # html.parser comes with Python, so nothing extra needs installing.
    soup = BeautifulSoup(html, "html.parser")

    # These are the BeautifulSoup methods from the lecture.
    title = soup.title.get_text(strip=True) if soup.title else "no title"
    words = soup.get_text(strip=True)
    tables = soup.find_all("table")
    links = soup.find_all("a")

    return {
        "url": url,
        "status": status,
        "html_size": len(html),
        "words": len(words),
        "tables": len(tables),
        "links": len(links),
        "title": title,
        "sample": words[:200],
        "html": html,
    }


#-------------------------------------------------------------------------#
#  SCRAPING THE SITEMAP                                                    #
#                                                                          #
#  A sitemap is a file where a website lists its own pages for programs    #
#  like ours to read. It is an ordinary file with no JavaScript, so        #
#  BeautifulSoup handles it easily.                                        #
#-------------------------------------------------------------------------#

def scrape_sitemap(scraper=None):
    """Read the list of pages from the sitemap."""
    scraper = scraper or Scraper()

    reply = scraper.fetch(f"{config.BASE_URL}/sitemap.xml", want="text")
    if not reply["ok"]:
        return pd.DataFrame()

    # "xml" mode needs lxml, so we fall back to the built in parser if
    # lxml is not installed.
    try:
        soup = BeautifulSoup(reply["data"], "xml")
    except Exception:
        soup = BeautifulSoup(reply["data"], "html.parser")

    rows = []
    for entry in soup.find_all("url"):
        location = entry.find("loc")
        updated = entry.find("changefreq")
        rows.append({
            "Page": location.get_text(strip=True) if location else None,
            "Updated": updated.get_text(strip=True) if updated else None,
        })

    return pd.DataFrame(rows)


#-------------------------------------------------------------------------#
#  BEAUTIFULSOUP METHODS                                                   #
#-------------------------------------------------------------------------#

def beautifulsoup_methods(html):
    """
    Each BeautifulSoup method from the lecture, run on real HTML, so we
    can see what it returns.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    def show(method, code, value):
        text = str(value)
        rows.append({"Method": method, "Code": code,
                     "Returned": text[:70] + ("..." if len(text) > 70 else "")})

    show("find()", "soup.find('title')", soup.find("title"))
    show("find_all()", "len(soup.find_all('a'))", len(soup.find_all("a")))
    show("get_text()", "soup.get_text(strip=True)[:40]",
         soup.get_text(strip=True)[:40] or "nothing")
    first_link = soup.find("a")
    show("get()", "soup.find('a').get('href')",
         first_link.get("href") if first_link else "no links")
    show("select()", "len(soup.select('meta'))", len(soup.select("meta")))
    show("select_one()", "soup.select_one('meta[name=viewport]')",
         soup.select_one("meta[name=viewport]"))

    return pd.DataFrame(rows)


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.static_scraper                 #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    scraper = Scraper()

    print("Downloading the CSE trade summary page with requests")
    print("-" * 65)
    result = scrape_page(scraper=scraper)

    print(f"  Address    : {result['url']}")
    print(f"  Status     : {result['status']}")
    print(f"  HTML size  : {result['html_size']:,} bytes")
    print(f"  Words found: {result['words']} characters")
    print(f"  Tables     : {result['tables']}")
    print()
    print("  The page has almost no words in it because the prices are")
    print("  added by JavaScript after the page loads, and requests does")
    print("  not run JavaScript. This is why we read the data from the")
    print("  address the page itself uses instead (src/api_client.py).")

    print()
    print("The same library on the sitemap, which is an ordinary file")
    print("-" * 65)
    sitemap = scrape_sitemap(scraper)
    print(sitemap.head(8).to_string(index=False))
    print(f"  ({len(sitemap)} pages listed, read without any trouble)")

    print()
    print("BeautifulSoup methods")
    print("-" * 65)
    print(beautifulsoup_methods(result["html"]).to_string(index=False))
