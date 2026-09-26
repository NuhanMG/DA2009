#=========================================================================#
#  FILE   : warm_cache.py                                                  #
#  PURPOSE: Collects the data once and saves a copy of every reply, so     #
#           the app still works if the internet is unavailable.            #
#  OWNER  : 25ada072                                                       #
#                                                                          #
#  Run this before a demonstration. It also means the demonstration        #
#  itself sends almost no requests to the CSE website.                     #
#                                                                          #
#  Run it with:  python warm_cache.py                                      #
#=========================================================================#

import config
from src.api_client import CSEApi
from src.crawler import crawl


def main():
    api = CSEApi()

    print("=" * 55)
    print("  Collecting a copy of the data")
    print(f"  {config.DELAY} seconds between requests - this is meant to be slow")
    print("=" * 55)

    jobs = [
        ("Market status", api.market_status),
        ("Index", api.aspi),
        ("Market summary", api.market_summary),
        ("Share prices", api.trade_summary),
        ("Top risers", api.top_gainers),
        ("Top fallers", api.top_losers),
        ("Sectors", api.sectors),
        ("Company list", api.all_companies),
        ("Announcements", api.announcements),
        ("Circulars", api.circulars),
    ]

    for name, job in jobs:
        try:
            result = job()
            size = len(result) if hasattr(result, "__len__") else 1
            print(f"  saved   {name:18} ({size} record(s))")
        except Exception as e:
            print(f"  failed  {name:18} {e}")

    #--- A few company profiles -----------------------------------------#
    companies = api.all_companies()
    if not companies.empty:
        symbols = companies["symbol"].head(15).tolist()
        print(f"\n  Saving {len(symbols)} company profiles...")
        for number, symbol in enumerate(symbols, start=1):
            api.company_info(symbol)
            print(f"    {number:2}/{len(symbols)}  {symbol}")

    #--- The PDFs -------------------------------------------------------#
    print("\n  Downloading documents...")
    crawl(limit=5, api=api)

    print()
    print("=" * 55)
    print("  Done")
    print("=" * 55)
    print(f"  Saved replies : {len(list(config.CACHE_DIR.glob('*.json')))}")
    print(f"  PDFs on disk  : {len(list(config.PDF_DIR.glob('*.pdf')))}")
    print(f"  Requests sent : {api.scraper.log.request_count}")


if __name__ == "__main__":
    main()
