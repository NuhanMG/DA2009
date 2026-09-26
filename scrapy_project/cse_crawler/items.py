#=========================================================================#
#  FILE   : scrapy_project/cse_crawler/items.py                            #
#  PURPOSE: Defines the shape of one record the spider produces.           #
#  OWNER  : 25ada073                                                       #
#                                                                          #
#  An Item is Scrapy's version of a form with named boxes. Declaring the   #
#  fields up front means a typo like 'ttile' raises an error straight      #
#  away, instead of quietly creating a wrong column in the output file.    #
#=========================================================================#

import scrapy


class DocumentItem(scrapy.Item):
    """One CSE document discovered by the spider."""

    title = scrapy.Field()          # what the document is called
    url = scrapy.Field()            # where the PDF actually lives
    source = scrapy.Field()         # which listing we found it in
    uploaded = scrapy.Field()       # when CSE published it
    content_type = scrapy.Field()   # confirms it really is a PDF
    size_kb = scrapy.Field()        # how big the file is
    status = scrapy.Field()         # the HTTP status we got back
