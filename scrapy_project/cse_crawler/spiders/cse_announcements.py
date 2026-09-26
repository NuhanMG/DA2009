#=========================================================================#
#  FILE   : scrapy_project/cse_crawler/spiders/cse_announcements.py        #
#  PURPOSE: A Scrapy spider that finds the CSE circulars and follows the   #
#           link to each PDF document.                                     #
#  OWNER  : 25ada073                                                       #
#                                                                          #
#  This does the same job as src/crawler.py, written as a Scrapy spider.   #
#                                                                          #
#  How it works:                                                           #
#                                                                          #
#      start()            ask CSE for the list of circulars                #
#         |                                                                #
#      parse()            read the list, work out each PDF address,        #
#         |               and follow it                                    #
#         |                                                                #
#      parse_document()   record what we found at the other end            #
#                                                                          #
#  The spider does not know which documents exist when it starts. It       #
#  finds them and then follows them, which is what crawling means.         #
#                                                                          #
#  Run it with:                                                            #
#      cd scrapy_project                                                   #
#      scrapy crawl cse_announcements -O ../data/scrapy_output.json        #
#=========================================================================#

import json

import scrapy

from cse_crawler.items import DocumentItem


class CseAnnouncementsSpider(scrapy.Spider):

    # The name we type after "scrapy crawl".
    name = "cse_announcements"

    # Never follow a link to another website by accident.
    allowed_domains = ["cse.lk", "cdn.cse.lk", "www.cse.lk"]

    # The PDFs are stored on a different server from the website.
    CDN_BASE = "https://cdn.cse.lk/cmt/"

    # The lists we start from. Each one wraps its records under a
    # different name, so we keep the name next to the address.
    SOURCES = [
        ("https://www.cse.lk/api/circularAnnouncement",
         "reqCircularAnnouncement", "Circular"),
        ("https://www.cse.lk/api/approvedAnnouncement",
         "approvedAnnouncements", "Announcement"),
    ]

    #---------------------------------------------------------------------#
    #  THE FIRST REQUESTS                                                  #
    #---------------------------------------------------------------------#

    async def start(self):
        """
        Send the first requests.

        Most spiders just set start_urls and let Scrapy send GET requests.
        We build the requests ourselves because the CSE addresses only
        answer POST - a GET returns an error.

        Note: older versions of Scrapy used a method called
        start_requests() for this. It was replaced by start(), and in the
        version we are using start_requests() has been removed, so a
        spider written the old way runs and collects nothing.
        """
        for url, record_name, label in self.SOURCES:
            yield scrapy.Request(
                url=url,
                method="POST",
                callback=self.parse,
                # cb_kwargs passes extra information to the callback, so
                # parse() knows which list replied.
                cb_kwargs={"record_name": record_name, "label": label},
                dont_filter=True,
            )

    #---------------------------------------------------------------------#
    #  READ THE LIST AND FOLLOW EACH DOCUMENT                              #
    #---------------------------------------------------------------------#

    def parse(self, response, record_name, label):
        """
        Read a list of documents and follow the link to each one.

        The quotes spider from the lecture used CSS selectors here because
        it received HTML. We receive JSON, so we use json.loads instead.
        The idea is the same: take the useful fields out of the reply,
        then follow the links we found.
        """
        try:
            reply = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.warning(f"{response.url} did not return JSON")
            return

        records = reply.get(record_name, []) if isinstance(reply, dict) else []
        self.logger.info(f"{label}: found {len(records)} records")

        seen = set()

        for record in records:
            path = record.get("path")

            # Not every announcement has a document attached.
            if not path or not str(path).lower().endswith(".pdf"):
                continue

            pdf_url = self.CDN_BASE + str(path)

            # The same document can appear twice in the list.
            if pdf_url in seen:
                continue
            seen.add(pdf_url)

            title = (record.get("fileText")
                     or record.get("announcementCategory")
                     or "Untitled")

            # This is the crawling step: we found a new address and now we
            # follow it. Scrapy queues it, applies the download delay and
            # checks robots.txt before sending it.
            yield scrapy.Request(
                url=pdf_url,
                callback=self.parse_document,
                cb_kwargs={
                    "title": str(title).strip(),
                    "label": label,
                    "uploaded": record.get("uploadedDate")
                                or record.get("dateOfAnnouncement", ""),
                },
                # HEAD asks only for the details of the file, not the file
                # itself. We want to check it exists and see how big it
                # is, and downloading several megabytes to find that out
                # would be wasteful.
                method="HEAD",
            )

    #---------------------------------------------------------------------#
    #  RECORD WHAT WE FOUND                                                #
    #---------------------------------------------------------------------#

    def parse_document(self, response, title, label, uploaded):
        """
        Build one record for the output file.

        We ask for Content-Length to record how big each PDF is. The CSE
        content server does not always tell us on a HEAD request - some
        replies leave the header out, and some say 0. A real PDF is never
        empty, so in both cases we record None rather than 0, because 0
        would be a wrong measurement - it would say the file is empty.
        """
        raw_size = response.headers.get("Content-Length", b"").decode()
        if raw_size == "0":
            raw_size = ""

        item = DocumentItem()
        item["title"] = title
        item["url"] = response.url
        item["source"] = label
        item["uploaded"] = uploaded
        item["content_type"] = response.headers.get(
            "Content-Type", b"unknown").decode()
        item["size_kb"] = (round(int(raw_size) / 1024, 1)
                           if raw_size.isdigit() else None)
        item["status"] = response.status

        yield item
