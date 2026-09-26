#=========================================================================#
#  FILE   : src/api_client.py                                              #
#  PURPOSE: Gets the stock market data from the CSE website and turns it   #
#           into pandas DataFrames.                                        #
#  OWNER  : 25ada072                                                       #
#                                                                          #
#  The CSE website is built with JavaScript, so the prices are not in the  #
#  HTML that requests downloads. We opened the site, pressed F12 and       #
#  looked at the Network tab, which showed the page loading its data from  #
#  addresses like https://www.cse.lk/api/tradeSummary. Those addresses     #
#  return JSON, so we read them with requests and pandas.                  #
#                                                                          #
#  Every request goes through Scraper, so robots.txt is checked and the    #
#  1.5 second delay is applied automatically.                              #
#=========================================================================#

from datetime import datetime

import pandas as pd

import config
from src.ethics import Scraper


#-------------------------------------------------------------------------#
#  HELPERS                                                                 #
#-------------------------------------------------------------------------#

def to_datetime(value):
    """
    CSE sends dates as the number of milliseconds since 1970, like
    1786440420412. This turns that into a normal date and time.
    """
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(float(value) / 1000)
    except (ValueError, OSError, TypeError):
        return None


def get_records(reply, key=None):
    """
    Pull the list of records out of a reply.

    Some addresses return a plain list, and others wrap the list inside a
    dictionary under a name such as "reqTradeSummery". This handles both.
    """
    if reply is None:
        return []

    if isinstance(reply, list):
        # A few replies are a list inside another list.
        if len(reply) == 1 and isinstance(reply[0], list):
            return reply[0]
        return reply

    if isinstance(reply, dict):
        if key and key in reply:
            return reply[key]
        for value in reply.values():
            if isinstance(value, list):
                return value
        return [reply]

    return []


def make_dataframe(records, date_columns=()):
    """Turn a list of dictionaries into a DataFrame."""
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    for column in date_columns:
        if column in df.columns:
            df[column] = df[column].apply(to_datetime)

    return df


#-------------------------------------------------------------------------#
#  THE API CLIENT                                                          #
#-------------------------------------------------------------------------#

class CSEApi:

    def __init__(self, scraper=None):
        self.scraper = scraper or Scraper()

    def call(self, endpoint, data=None):
        """Send one request to one CSE address."""
        method = config.ENDPOINTS.get(endpoint, {}).get("method", "POST")
        url = f"{config.API_BASE}/{endpoint}"

        # save_as gives the saved copy a readable filename, e.g.
        # data/cache/tradeSummary.json
        return self.scraper.fetch(url, method=method, data=data,
                                  save_as=endpoint)

    #---------------------------------------------------------------------#
    #  MARKET LEVEL                                                        #
    #---------------------------------------------------------------------#

    def market_status(self):
        """Is the market open or closed right now?"""
        reply = self.call("marketStatus")
        if not reply["ok"]:
            return "Unknown"
        return reply["data"].get("status", "Unknown")

    def aspi(self):
        """
        The All Share Price Index - one number that summarises how the
        whole Colombo market moved today.
        """
        reply = self.call("aspiData")
        if not reply["ok"]:
            return {}
        return dict(reply["data"])

    def market_summary(self):
        """Today's total turnover, share volume and number of trades."""
        reply = self.call("marketSummery")
        if not reply["ok"]:
            return {}
        return dict(reply["data"])

    def sectors(self):
        """Sector indices, such as Banks, Energy and Materials."""
        reply = self.call("allSectors")
        if not reply["ok"]:
            return pd.DataFrame()
        return make_dataframe(get_records(reply["data"]))

    #---------------------------------------------------------------------#
    #  SHARE PRICES                                                        #
    #---------------------------------------------------------------------#

    def trade_summary(self):
        """
        Our main dataset: today's trading for every listed company.
        One request returns around 285 companies.
        """
        reply = self.call("tradeSummary")
        if not reply["ok"]:
            self.scraper.log.add(f"Could not get trade summary: {reply['error']}")
            return pd.DataFrame()

        df = make_dataframe(get_records(reply["data"], "reqTradeSummery"))
        self.scraper.log.add(f"Got trade data for {len(df)} companies")
        return df

    def top_gainers(self):
        """Companies whose share price rose the most today."""
        reply = self.call("topGainers")
        if not reply["ok"]:
            return pd.DataFrame()
        return make_dataframe(get_records(reply["data"]),
                              date_columns=["tradeDate"])

    def top_losers(self):
        """
        Companies whose share price fell the most today.
        (CSE spells the address topLooses, so we keep their spelling.)
        """
        reply = self.call("topLooses")
        if not reply["ok"]:
            return pd.DataFrame()
        return make_dataframe(get_records(reply["data"]),
                              date_columns=["tradeDate"])

    #---------------------------------------------------------------------#
    #  COMPANY LEVEL                                                       #
    #---------------------------------------------------------------------#

    def all_companies(self):
        """
        The list of every listed company and its symbol.

        A symbol such as SAMP.N0000 means:
            SAMP  the company (Sampath Bank)
            N     voting shares
            0000  the share class number
        """
        reply = self.call("allSecurityCode")
        if not reply["ok"]:
            return pd.DataFrame()
        df = make_dataframe(get_records(reply["data"]))
        self.scraper.log.add(f"Got the list of {len(df)} companies")
        return df

    def company_info(self, symbol):
        """
        Details for one company.

        This address needs a value sent with it, so we pass
        data={"symbol": "SAMP.N0000"} in the POST request.
        """
        reply = self.call("companyInfoSummery", data={"symbol": symbol})
        if not reply["ok"]:
            return {}

        # The reply has several parts. The company details are under
        # reqSymbolInfo.
        return dict(reply["data"].get("reqSymbolInfo", {}))

    def several_companies(self, symbols, progress=None):
        """
        Get details for a list of companies, one at a time.

        This is slow on purpose. Each company is a separate request, and
        every request waits its 1.5 seconds first.
        """
        rows = []
        for number, symbol in enumerate(symbols, start=1):
            if progress:
                progress(number / len(symbols),
                         f"Getting {symbol} ({number} of {len(symbols)})")
            info = self.company_info(symbol)
            if info:
                rows.append(info)

        self.scraper.log.add(f"Got details for {len(rows)} companies")
        return make_dataframe(rows)

    #---------------------------------------------------------------------#
    #  ANNOUNCEMENTS                                                       #
    #---------------------------------------------------------------------#

    def announcements(self):
        """Company announcements - dividends, meetings, board changes."""
        reply = self.call("approvedAnnouncement")
        if not reply["ok"]:
            return pd.DataFrame()

        df = make_dataframe(get_records(reply["data"], "approvedAnnouncements"),
                            date_columns=["createdDate"])
        self.scraper.log.add(f"Got {len(df)} announcements")
        return df

    def circulars(self):
        """
        CSE circulars. Each one has a PDF attached.

        The reply gives only part of the address, such as
        "upload_report_file/abc.pdf", so we add the server name in front
        of it to make a full link.
        """
        reply = self.call("circularAnnouncement")
        if not reply["ok"]:
            return pd.DataFrame()

        df = make_dataframe(get_records(reply["data"],
                                        "reqCircularAnnouncement"))

        if not df.empty and "path" in df.columns:
            df["pdf_url"] = config.CDN_BASE + df["path"].astype(str)

        self.scraper.log.add(f"Got {len(df)} circulars with PDFs")
        return df


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.api_client                     #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    api = CSEApi()

    print("Market status:", api.market_status())

    index = api.aspi()
    print(f"ASPI index   : {index.get('value'):,.2f} "
          f"({index.get('change'):+.2f})")

    print()
    print("Trade summary - first 5 companies")
    print("-" * 55)
    trades = api.trade_summary()
    if not trades.empty:
        print(trades[["symbol", "name", "price", "change",
                      "percentageChange"]].head())

    print()
    print("One company")
    print("-" * 55)
    info = api.company_info("SAMP.N0000")
    print(info.get("name"), "-", info.get("lastTradedPrice"))

    print()
    print("Circulars with PDF links")
    print("-" * 55)
    circulars = api.circulars()
    if not circulars.empty:
        for _, row in circulars.head(3).iterrows():
            print(" ", str(row["fileText"])[:55])

    print()
    print(api.scraper.log.text())
