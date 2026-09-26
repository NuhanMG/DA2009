#=========================================================================#
#  FILE   : src/selenium_scraper.py                                        #
#  PURPOSE: Opens the CSE website in a real browser so the JavaScript      #
#           runs, then reads the finished page with BeautifulSoup.         #
#  OWNER  : 25ada072                                                       #
#                                                                          #
#  requests cannot see the prices on the CSE website, because it does not  #
#  run JavaScript (see src/static_scraper.py).                             #
#                                                                          #
#  Selenium solves that by controlling an actual browser. The browser      #
#  loads the page, runs the JavaScript and builds the table, and then we   #
#  ask it for the finished HTML with driver.page_source.                   #
#                                                                          #
#      requests           the HTML file only, no prices                    #
#      Selenium           the page after JavaScript has run                #
#                                                                          #
#  We use the API for the main data collection because it is quicker and   #
#  gives us every company at once, while the page only shows the first     #
#  25 or so before you have to click to the next page. This file shows     #
#  the browser method working, and is our backup if the API changes.       #
#                                                                          #
#  Run it with:  python -m src.selenium_scraper                            #
#=========================================================================#

import time

import pandas as pd
from bs4 import BeautifulSoup

import config


#-------------------------------------------------------------------------#
#  STARTING A BROWSER                                                      #
#-------------------------------------------------------------------------#

def start_browser(headless=True):
    """
    Open a browser and return it.

    The lecture uses Chrome. This computer has Microsoft Edge, which
    Selenium supports in the same way, so we try Edge first and then the
    others. Selenium downloads the matching driver by itself the first
    time it runs.

    headless=True means the browser runs in the background without a
    window, which is faster and does not interrupt a demonstration.
    """
    from selenium import webdriver

    browsers = [
        ("Edge", webdriver.Edge, webdriver.EdgeOptions),
        ("Chrome", webdriver.Chrome, webdriver.ChromeOptions),
        ("Firefox", webdriver.Firefox, webdriver.FirefoxOptions),
    ]

    for name, browser, options_class in browsers:
        try:
            options = options_class()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            # Use the same User-Agent as the rest of the project.
            options.add_argument(f"--user-agent={config.USER_AGENT}")

            return browser(options=options), name
        except Exception:
            continue

    return None, "No browser could be started. Install Edge, Chrome or Firefox."


#-------------------------------------------------------------------------#
#  LOADING A PAGE                                                          #
#-------------------------------------------------------------------------#

def load_page(url=None, headless=True, wait_seconds=15):
    """
    Open a page in a browser, wait for the table to appear, and read it.

    The waiting is the important part. When the browser first opens the
    page the table does not exist yet, because JavaScript is still
    fetching the data. If we read the HTML straight away we would get the
    same empty page that requests gets.

    WebDriverWait pauses until the table actually appears, instead of
    guessing how long to sleep for.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.ui import WebDriverWait

    url = url or config.PAGES["trade_summary"]
    driver, browser_name = start_browser(headless)

    if driver is None:
        return {"ok": False, "error": browser_name, "table": pd.DataFrame()}

    started = time.time()

    try:
        driver.get(url)

        try:
            WebDriverWait(driver, wait_seconds).until(
                expected_conditions.presence_of_element_located(
                    (By.TAG_NAME, "table"))
            )
        except Exception:
            pass  # No table appeared, but we can still look at the page.

        time.sleep(2)  # Let the last few rows settle.

        # page_source is the page AFTER JavaScript has run. This is the
        # difference from response.text in the requests version.
        html = driver.page_source

        screenshot = str(config.DATA_DIR / "selenium_page.png")
        driver.save_screenshot(screenshot)

        # From here it is ordinary BeautifulSoup, exactly as before.
        soup = BeautifulSoup(html, "html.parser")
        words = soup.get_text(strip=True)
        tables = soup.find_all("table")

        return {
            "ok": True,
            "error": None,
            "browser": browser_name,
            "html_size": len(html),
            "words": len(words),
            "tables": len(tables),
            "seconds": round(time.time() - started, 1),
            "screenshot": screenshot,
            "table": read_table(tables[0]) if tables else pd.DataFrame(),
        }

    except Exception as e:
        return {"ok": False, "error": str(e), "table": pd.DataFrame()}

    finally:
        # Always close the browser, even if something went wrong,
        # otherwise it keeps running in the background.
        try:
            driver.quit()
        except Exception:
            pass


#-------------------------------------------------------------------------#
#  TURNING AN HTML TABLE INTO A DATAFRAME                                  #
#-------------------------------------------------------------------------#

def read_table(table):
    """
    Read one HTML table into a DataFrame.

        <table>
          <tr> <th>Symbol</th> <th>Price</th> </tr>   the heading row
          <tr> <td>SAMP</td>   <td>136.75</td> </tr>  a data row
        </table>
    """
    headings = [cell.get_text(strip=True) for cell in table.find_all("th")]

    rows = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue  # this is the heading row
        rows.append([cell.get_text(strip=True) for cell in cells])

    if not rows:
        return pd.DataFrame()

    # If the headings do not match the data, number the columns instead
    # so we do not lose the rows.
    if len(headings) != len(rows[0]):
        headings = [f"Column {i + 1}" for i in range(len(rows[0]))]

    return pd.DataFrame(rows, columns=headings)


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.selenium_scraper               #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    print("Opening the CSE trade summary page in a browser")
    print("-" * 65)

    result = load_page()

    if not result["ok"]:
        print("Could not run Selenium:", result["error"])
    else:
        print(f"  Browser    : {result['browser']}")
        print(f"  HTML size  : {result['html_size']:,} bytes")
        print(f"  Words found: {result['words']:,} characters")
        print(f"  Tables     : {result['tables']}")
        print(f"  Time taken : {result['seconds']} seconds")
        print(f"  Screenshot : {result['screenshot']}")

        if not result["table"].empty:
            print()
            print("First few rows of the table:")
            print(result["table"].head(5).to_string(index=False))

        print()
        print("  requests found 24 characters and no tables on this same")
        print("  page. The difference is that the browser ran the")
        print("  JavaScript first.")
