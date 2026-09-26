"""
30 questions for 25ada073 - crawling for documents, and cleaning the data.
"""

Q_073 = [

#=========================================================================#
#  CRAWLING                                                               #
#=========================================================================#

("Easy", "Which files did you write?",
 "`src/crawler.py`, which finds and downloads the PDF documents; "
 "`src/cleaner.py`, which tidies the data and checks it; and the Scrapy "
 "project in `scrapy_project/`."),

("Easy", "What is the difference between scraping and crawling?",
 "Scraping is taking data from a page you already know about. Crawling is "
 "finding pages by following links from one to the next.\n\n"
 "Most of our project is scraping, because we know the address. My part is "
 "the crawling - we do not know which documents exist until we look."),

("Easy", "Why are crawlers sometimes called spiders?",
 "Because they crawl across the web the way a spider moves across its web. "
 "They start from a few known addresses and follow links outward, building "
 "up a network of pages they have found."),

("Easy", "What is Scrapy?",
 "A Python framework built specifically for crawling and scraping. It "
 "handles the queue of requests, the delays, robots.txt and saving the "
 "output, so you only write the part that says what to extract and which "
 "links to follow."),

("Medium", "Walk me through your crawler.",
 "Two stages.\n\n"
 "`find_documents()` asks for the list of circulars, and for each one "
 "builds the full address of the PDF. It also removes duplicates, because "
 "the same document can appear twice and downloading it twice would waste "
 "CSE's bandwidth for nothing.\n\n"
 "`download_documents()` then fetches them one at a time through the "
 "ethical session, so each download waits its 1.5 seconds. It skips "
 "anything we already have on disk."),

("Medium", "How did you work out where the PDFs are stored?",
 "The list only gives part of the address, something like "
 "`upload_report_file/abc123.pdf`, which is not a working link on its own. "
 "And the PDFs are not on the website itself - they are on a separate "
 "server.\n\n"
 "So we tried the likely addresses until one returned a real PDF. "
 "`www.cse.lk/cmt/...` gave 404, `cdn.cse.lk/...` gave 403, and "
 "`cdn.cse.lk/cmt/...` returned 200 with content type `application/pdf`."),

("Medium", "How do you check a downloaded file really is a PDF?",
 "Every PDF file starts with the four characters `%PDF`. We check the first "
 "four bytes before saving. If they do not match, something else came back "
 "- an error page, for instance - and we do not save it as a PDF.",
 "if not content[:4] == b\"%PDF\":\n"
 "    results.append({\"Title\": title, \"Result\": \"Not a PDF file\"})\n"
 "    continue"),

("Medium", "Why limit how many documents you download?",
 "There are far more documents on the site than we need to show the "
 "technique works. Downloading all of them just because we could would put "
 "load on their server for no benefit. The lecture put it as: only scrape "
 "the data you need."),

("Medium", "Explain the Scrapy spider.",
 "`start()` sends POST requests to the two announcement addresses, because "
 "CSE does not answer GET. `parse()` reads the JSON reply, builds the full "
 "address of each PDF, and yields a new request for it - that yielding of a "
 "new request is the crawling step. `parse_document()` then records what "
 "came back at the other end.",
 "def parse(self, response, record_name, label):\n"
 "    reply = json.loads(response.text)\n"
 "    for record in reply.get(record_name, []):\n"
 "        pdf_url = self.CDN_BASE + record[\"path\"]\n"
 "        yield scrapy.Request(pdf_url,           # follow the link\n"
 "                             callback=self.parse_document,\n"
 "                             method=\"HEAD\")"),

("Medium", "Why does the spider use HEAD instead of GET?",
 "A HEAD request asks only for the details of the file - its type and its "
 "size - without downloading the file itself. We want to confirm each "
 "document exists and see how big it is, and downloading several megabytes "
 "of PDF just to find that out would be wasteful."),

("Medium", "Which Scrapy settings keep the spider polite?",
 "`ROBOTSTXT_OBEY = True`, which makes Scrapy check robots.txt itself. "
 "`DOWNLOAD_DELAY = 1.5`, matching the rest of our project. "
 "`CONCURRENT_REQUESTS = 1`, where the default is 8 - that would mean eight "
 "connections at once. AutoThrottle, which slows down further if the server "
 "starts responding slowly. And `CLOSESPIDER_ITEMCOUNT = 40` so it stops "
 "after enough items."),

("Medium", "Why does the spider record `None` rather than `0` when the file "
           "size is missing?",
 "Because 0 is a measurement, and a wrong one - it says the file is empty "
 "when it is not. `None` honestly says we did not find out.\n\n"
 "The CSE server does not always send the `Content-Length` header back on a "
 "HEAD request. Writing 0 in that case would put false figures into our "
 "dataset, which is exactly the kind of quiet data quality problem the "
 "course warned about."),

("Hard", "Your first version of the spider collected nothing. What "
         "happened?",
 "It reported 0 items and finished in about a hundredth of a second, "
 "without sending a single request.\n\n"
 "The method for sending the first requests used to be called "
 "`start_requests()`, which is what the course notes use. Scrapy 2.13 "
 "replaced it with an asynchronous `start()` method, and by version 2.17, "
 "which is what we have installed, `start_requests()` was removed "
 "completely. So Scrapy never called our method and nothing warned us.\n\n"
 "It is a real example of a scraper breaking because something underneath "
 "it changed - usually that is the website, but here it was the library."),

("Hard", "Why does the project have two crawlers doing the same job?",
 "`src/crawler.py` is ours, written directly with `requests`, and it is "
 "what the app actually uses. It is simple and it goes through the same "
 "ethical layer as everything else in the project.\n\n"
 "The Scrapy version shows the framework approach that the course taught "
 "and that industry uses. It runs as a separate process, because Scrapy's "
 "engine cannot be started twice inside one program."),

("Hard", "How would you extend the crawler to follow links deeper?",
 "At the moment we go two levels: the listing, then each document. To go "
 "deeper you would have `parse_document()` yield further requests for any "
 "links it found, and Scrapy would queue those the same way.\n\n"
 "You would also need to keep a set of addresses already visited so it "
 "cannot loop forever, and set `DEPTH_LIMIT` so it does not wander across "
 "the whole site. `allowed_domains` already stops it leaving cse.lk."),

#=========================================================================#
#  CLEANING                                                               #
#=========================================================================#

("Easy", "Why does scraped data need cleaning at all?",
 "Because it comes out in whatever shape the website happened to send it, "
 "not in a shape that is ready to analyse. The course listed 'data "
 "collected through scraping is ready for analysis' as a misconception."),

("Easy", "What are the four things you had to clean in the CSE data?",
 "Dates arriving as very large numbers. Numbers arriving as text. Columns "
 "that are empty for every single company. And text with extra spaces "
 "around it."),

("Medium", "Explain the date problem.",
 "CSE sends dates as the number of milliseconds since 1 January 1970 - a "
 "number like `1786440420412`. Left alone, pandas treats that as an "
 "ordinary number, which means you could sort by it, or worse, calculate an "
 "average of it, and nothing would warn you.\n\n"
 "We convert those columns with `pd.to_datetime(column, unit=\"ms\", "
 "utc=True)`, and then into Colombo time. The numbers are counted in UTC, "
 "and Sri Lanka is 5 hours 30 minutes ahead - without that step every "
 "trade would look as if it happened before the market opened."),

("Medium", "How do you avoid converting a column by mistake?",
 "Three checks, and all of them have to pass. The column name has to "
 "contain a word like 'date', 'time' or 'created'. The column has to hold "
 "numbers. And the values themselves have to be larger than a trillion, "
 "which any real date in milliseconds will be but a price or a quantity "
 "never is.",
 "if not any(word in column.lower()\n"
 "           for word in (\"date\", \"time\", \"created\")):\n"
 "    continue\n"
 "if not pd.api.types.is_numeric_dtype(tidy[column]):\n"
 "    continue\n"
 "...\n"
 "if not values.empty and values.median() > 1_000_000_000_000:\n"
 "    tidy[column] = (pd.to_datetime(tidy[column], unit=\"ms\", utc=True,\n"
 "                                   errors=\"coerce\")\n"
 "                    .dt.tz_convert(\"Asia/Colombo\")\n"
 "                    .dt.tz_localize(None))"),

("Medium", "Why does a number stored as text matter?",
 "Because you cannot add up text, and sorting it sorts alphabetically. That "
 "puts \"9\" after \"100\", because it compares the first character. Any "
 "chart or total built on it would be wrong."),

("Medium", "How do you decide a text column is really numbers?",
 "We take a sample of the column, try converting it to numbers, and see how "
 "much of it succeeds. If more than 90 per cent converts, it was a number "
 "column stored as text and we convert the whole thing.\n\n"
 "We do not require 100 per cent, because a genuine number column can still "
 "have a few blanks or dashes in it."),

("Medium", "What is the difference between cleaning and checking?",
 "Cleaning fixes the shape of the data - the types, the empty columns, the "
 "duplicates. Checking asks whether the values are believable.\n\n"
 "A share price of minus five rupees would be perfectly tidy and completely "
 "wrong. Cleaning would never catch it; a check does."),

("Medium", "What checks do you run?",
 "That there are rows at all. That no price is negative. That nothing moved "
 "by more than 100 per cent in a day, which would be suspicious. That every "
 "row has a trading symbol. That no company appears twice. And an overall "
 "completeness figure - what percentage of cells actually have a value."),

("Medium", "Why do you copy the DataFrame before cleaning it?",
 "So the original stays untouched. If the cleaning turns out to have a bug, "
 "we can look at the raw version and compare, without having to go back to "
 "CSE and download everything again."),

("Medium", "How do you show that the cleaning did something?",
 "We count the problems before and after and show them side by side - the "
 "number of rows, empty cells, empty columns, duplicate rows, number "
 "columns and date columns. Saying 'we cleaned the data' means very little; "
 "showing date columns going from 0 to 1 is evidence."),

("Hard", "Your before and after table shows the number columns going down "
         "by one. Why is that a good thing?",
 "Because that column became a date column instead. It was being counted as "
 "a number, which is exactly the problem - it was a timestamp being treated "
 "as an ordinary figure.\n\n"
 "So one column moved out of the number count and into the date count. The "
 "two changes together are the fix showing up in the numbers."),

("Hard", "Is dropping empty columns always the right thing to do?",
 "Not always, and it is worth being honest about. A column that is empty "
 "today might be filled in tomorrow, or might be empty only for the "
 "particular set of companies we happened to fetch.\n\n"
 "We do it because those columns are noise on screen and in every exported "
 "file, and because we keep the raw version, so nothing is actually lost. "
 "If we were building something that ran every day, dropping columns based "
 "on one day's data would be the wrong call."),

("Hard", "How would you handle a company that legitimately moved more than "
         "100 per cent?",
 "The check does not delete anything - it flags it. That is the important "
 "part of the design.\n\n"
 "A big move can be real, after a share split or a return from suspension. "
 "So the check says 'look at this', not 'this is wrong'. Automatically "
 "deleting rows that look odd is how you quietly lose real data."),

("Hard", "If you had more time, what would you add to the cleaning?",
 "Two things. Cross-checking against another source, so we could tell "
 "whether a strange number is a collection error or a real market event. "
 "And keeping the data from several days, which would let us spot a value "
 "that is impossible given yesterday's - a price that has jumped a hundred "
 "times overnight, for example."),

("Easy", "Why does the crawler skip documents you already have?",
 "Because downloading the same file twice costs CSE bandwidth and gains us "
 "nothing. Before each download we look in `data/pdfs/` for a file already "
 "saved under that document id, and if it is there we move on."),

]
