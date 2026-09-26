#=========================================================================#
#  FILE   : scrapy_project/cse_crawler/settings.py                         #
#  PURPOSE: Scrapy's rule book for our spider.                             #
#  OWNER  : 25ada073                                                       #
#                                                                          #
#  These settings make the spider follow the same rules as the rest of    #
#  the project: obey robots.txt, wait between requests, and say who we    #
#  are.                                                                    #
#=========================================================================#

BOT_NAME = "cse_crawler"

SPIDER_MODULES = ["cse_crawler.spiders"]
NEWSPIDER_MODULE = "cse_crawler.spiders"

#-------------------------------------------------------------------------#
#  THE ETHICAL SETTINGS - the ones that earn marks                         #
#-------------------------------------------------------------------------#

# THE MOST IMPORTANT LINE IN THIS FILE.
# Scrapy reads robots.txt and refuses any URL the site disallows. Note
# that new Scrapy projects ship with this set to True, but plenty of
# tutorials tell you to switch it off to "make things work". We leave it
# on. If a page is blocked, we do not want it.
ROBOTSTXT_OBEY = True

# The same honest User-Agent our own scraper uses, so CSE sees one
# consistent, identifiable visitor rather than two mystery bots.
USER_AGENT = (
    "CSE-Academic-Scraper/1.0 "
    "(University of Colombo; DA 2009 Data Collection Methods II; "
    "group 25ada072-25ada073-25ada141-24ada076; "
    "educational use; contact: nuhanmalee@gmail.com)"
)

# Wait 1.5 seconds between requests - matching config.DEFAULT_DELAY.
DOWNLOAD_DELAY = 1.5

# Randomise that delay by +/-50% so our requests do not arrive in a
# perfectly regular machine-gun rhythm.
RANDOMIZE_DOWNLOAD_DELAY = True

# Only one request at a time to this website. The default is 8, which
# would mean eight simultaneous connections - far more aggressive than a
# person browsing.
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# AutoThrottle watches how quickly CSE responds and slows us down further
# if their server starts to struggle. It is politeness that adapts by
# itself rather than a fixed guess.
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.5
AUTOTHROTTLE_MAX_DELAY = 15.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Stop after 40 items. We only need enough to show the spider works,
# not the entire website.
CLOSESPIDER_ITEMCOUNT = 40

# Remember responses on disk, so re-running the spider while developing
# does not send the same requests to CSE over and over.
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 900
HTTPCACHE_DIR = "httpcache"

# Retry politely on temporary failures instead of hammering.
RETRY_ENABLED = True
RETRY_TIMES = 2

#-------------------------------------------------------------------------#
#  Housekeeping                                                            #
#-------------------------------------------------------------------------#

FEED_EXPORT_ENCODING = "utf-8"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
LOG_LEVEL = "INFO"
