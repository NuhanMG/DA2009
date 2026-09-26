#=========================================================================#
#  FILE   : src/ethics.py                                                  #
#  PURPOSE: Sends all our web requests, politely and legally.              #
#  OWNER  : 24ada076                                                       #
#                                                                          #
#  Every request in this project goes through this file. That way the      #
#  ethical rules are applied once, in one place, instead of being repeated #
#  (and possibly forgotten) in every other module.                         #
#                                                                          #
#  What happens before each request:                                       #
#     1. Check robots.txt to see if we are allowed                         #
#     2. Wait 1.5 seconds so we do not overload the server                 #
#     3. Send the request with a User-Agent that says who we are           #
#     4. Write the result to logs/request_log.csv                          #
#=========================================================================#

import csv
import json
import time
from datetime import datetime
from urllib.robotparser import RobotFileParser

import requests

import config


#-------------------------------------------------------------------------#
#  THE LOG                                                                 #
#                                                                          #
#  Keeps the messages we show in the app, and writes every request to a    #
#  CSV file so we can show exactly how the data was collected.             #
#-------------------------------------------------------------------------#

class ScraperLog:

    def __init__(self):
        self.messages = []
        self.request_count = 0

    def add(self, message):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.messages.append(f"{stamp}  {message}")
        return self.text()

    def text(self):
        return "\n".join(self.messages)

    def clear(self):
        self.messages = []
        self.request_count = 0

    def log_request(self, method, url, status, allowed):
        """Write one row to logs/request_log.csv."""
        self.request_count += 1
        new_file = not config.REQUEST_LOG.exists()

        with open(config.REQUEST_LOG, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if new_file:
                writer.writerow(["time", "method", "url", "status",
                                 "robots_allowed", "delay_seconds"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                method, url, status, allowed, config.DELAY,
            ])


#-------------------------------------------------------------------------#
#  THE SCRAPER                                                             #
#-------------------------------------------------------------------------#

class Scraper:

    def __init__(self, delay=config.DELAY):
        self.delay = delay
        self.log = ScraperLog()
        self.last_request_time = 0

        # A Session keeps the connection open between requests, which is
        # a little kinder to the server than opening a new one each time.
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": config.USER_AGENT})

        self.robots_text = ""
        self.robots = None
        self.read_robots()

    #---------------------------------------------------------------------#
    #  ROBOTS.TXT                                                          #
    #                                                                      #
    #  robots.txt is a file websites publish to tell automated programs    #
    #  which pages they may visit. Following it is voluntary - we follow   #
    #  it because that is what ethical scraping means.                     #
    #---------------------------------------------------------------------#

    def read_robots(self):
        """Download robots.txt and read the rules."""
        try:
            response = requests.get(
                config.ROBOTS_URL,
                headers={"User-Agent": config.USER_AGENT},
                timeout=config.TIMEOUT,
            )
            self.robots_text = response.text

            # RobotFileParser comes with Python and understands the rules
            # for us, so we do not have to read the file by hand.
            self.robots = RobotFileParser()
            self.robots.parse(self.robots_text.splitlines())

            self.log.add("Read robots.txt from the website")

        except Exception as e:
            self.robots = None
            self.log.add(f"Could not read robots.txt: {e}")

    def can_fetch(self, url):
        """
        Ask robots.txt whether we may request this address.
        Returns (True or False, reason).
        """
        if self.robots is None:
            # If we cannot read the rules we do not guess - we stop.
            return False, "robots.txt could not be read"

        if self.robots.can_fetch(config.USER_AGENT, url):
            return True, "allowed"
        return False, "not allowed by robots.txt"

    def blocked_paths(self):
        """The Disallow lines from robots.txt, for showing in the app."""
        paths = []
        for line in self.robots_text.splitlines():
            line = line.strip()
            if line.lower().startswith("disallow:"):
                value = line.split(":", 1)[1].strip()
                if value:
                    paths.append(value)
        return paths

    #---------------------------------------------------------------------#
    #  WAITING BETWEEN REQUESTS                                            #
    #---------------------------------------------------------------------#

    def wait(self):
        """
        Sleep so that our requests are at least self.delay apart.

        The website does not ask us to wait. We do it anyway, because
        sending requests as fast as the computer can manage would put
        load on their server for no good reason.
        """
        since_last = time.time() - self.last_request_time
        if since_last < self.delay:
            time.sleep(self.delay - since_last)
        self.last_request_time = time.time()

    def set_delay(self, seconds):
        self.delay = max(config.MIN_DELAY,
                         min(float(seconds), config.MAX_DELAY))
        return self.delay

    #---------------------------------------------------------------------#
    #  SAVING A COPY OF EACH REPLY                                         #
    #                                                                      #
    #  We save each reply to a file. If a later request fails because the  #
    #  internet is down, we can show the saved copy instead of an error.   #
    #---------------------------------------------------------------------#

    @staticmethod
    def save_copy(name, data):
        path = config.CACHE_DIR / f"{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @staticmethod
    def load_copy(name):
        path = config.CACHE_DIR / f"{name}.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    #---------------------------------------------------------------------#
    #  SENDING A REQUEST                                                   #
    #---------------------------------------------------------------------#

    def fetch(self, url, method="GET", data=None, save_as=None, want="json"):
        """
        Send one request and return a dictionary:
            {"ok": True or False, "data": ..., "error": ..., "from_file": ...}

        We return a dictionary instead of letting errors crash the program,
        because this runs behind a web page - a crash would close the whole
        app, but an error message can simply be shown on screen.
        """
        #--- Step 1: are we allowed? -------------------------------------#
        allowed, reason = self.can_fetch(url)
        if not allowed:
            self.log.add(f"SKIPPED {url} - {reason}")
            self.log.log_request(method, url, "skipped", allowed)

            # With no internet, robots.txt cannot be read, so nothing is
            # sent. Showing a copy we saved earlier sends nothing to the
            # website either, so it is still within the rules.
            saved = self.load_copy(save_as) if save_as else None
            if saved is not None:
                self.log.add(f"Using the saved copy of {save_as} instead")
                return {"ok": True, "data": saved, "from_file": True,
                        "error": None}

            return {"ok": False, "data": None, "from_file": False,
                    "error": f"robots.txt says we should not request this "
                             f"address ({reason})"}

        #--- Step 2: wait ------------------------------------------------#
        self.wait()

        #--- Step 3: send it ---------------------------------------------#
        try:
            if method == "POST":
                response = self.session.post(url, data=data,
                                             timeout=config.TIMEOUT)
            else:
                response = self.session.get(url, timeout=config.TIMEOUT)

            #--- Step 4: record it ---------------------------------------#
            self.log.log_request(method, url, response.status_code, allowed)
            self.log.add(f"{method} {url} - status {response.status_code}")

            # 200 means success. 403 means we are not allowed, 404 means the
            # page does not exist, 500 means the server had a problem.
            if response.status_code != 200:
                return {"ok": False, "data": None, "from_file": False,
                        "error": f"The server replied with "
                                 f"{response.status_code}."}

            # What kind of reply do we want back?
            #   "bytes" - raw file contents, for PDFs
            #   "text"  - a web page or XML file as a string, for
            #             BeautifulSoup
            #   "json"  - the data addresses, turned into Python lists and
            #             dictionaries (the default)
            if want == "bytes":
                return {"ok": True, "data": response.content,
                        "from_file": False, "error": None}

            if want == "text":
                return {"ok": True, "data": response.text,
                        "from_file": False, "error": None}

            result = response.json()

            if save_as:
                self.save_copy(save_as, result)

            return {"ok": True, "data": result, "from_file": False,
                    "error": None}

        except Exception as e:
            self.log.add(f"Request failed: {e}")

            # If we saved a copy earlier, show that rather than nothing.
            if save_as:
                saved = self.load_copy(save_as)
                if saved is not None:
                    self.log.add(f"Using the saved copy of {save_as} instead")
                    return {"ok": True, "data": saved, "from_file": True,
                            "error": None}

            return {"ok": False, "data": None, "from_file": False,
                    "error": str(e)}


#-------------------------------------------------------------------------#
#  THE RULES WE FOLLOW - shown in the app                                  #
#-------------------------------------------------------------------------#

ETHICAL_RULES = [
    ("Check robots.txt",
     "We read the robots.txt file and check every address against it "
     "before requesting that address."),

    ("Wait between requests",
     f"We pause {config.DELAY} seconds between requests. The website does "
     f"not ask us to, but sending requests as fast as possible would put "
     f"load on their server for no reason."),

    ("Say who we are",
     "Our User-Agent gives the university, the course and an email address "
     "instead of pretending to be an ordinary browser."),

    ("Only take what we need",
     "We collect the pages and documents we actually use, and save a copy "
     "so we do not ask for the same thing twice."),

    ("Only public data",
     "Everything we collect can be seen by anyone without logging in. We "
     "do not use logins, paywalls or CAPTCHAs, and we collect no personal "
     "information about any individual."),

    ("Handle errors properly",
     "If the server returns an error we stop and report it, instead of "
     "requesting the same address over and over."),

    ("Credit the source",
     "Every file we export names the Colombo Stock Exchange as the source "
     "and records when the data was collected."),
]


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.ethics                         #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    scraper = Scraper()

    print("robots.txt from CSE")
    print("-" * 55)
    print(scraper.robots_text)

    print("Paths the website asks us not to visit:", scraper.blocked_paths())
    print()

    print("Permission checks")
    print("-" * 55)
    for test_url in [config.API_BASE + "/aspiData",
                     config.PAGES["trade_summary"],
                     config.BASE_URL + "/cgi-bin/test"]:
        allowed, reason = scraper.can_fetch(test_url)
        mark = "yes" if allowed else "no"
        print(f"  {mark:4} {test_url}   ({reason})")

    print()
    print("A real request")
    print("-" * 55)
    result = scraper.fetch(config.API_BASE + "/aspiData", method="POST",
                           save_as="aspiData")
    print("ok  :", result["ok"])
    print("data:", result["data"])

    print()
    print(scraper.log.text())
