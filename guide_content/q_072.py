"""
30 questions for 25ada072 - getting the data from the site, and Selenium.
"""

Q_072 = [

#=========================================================================#
#  GETTING THE DATA                                                       #
#=========================================================================#

("Easy", "Which files did you write?",
 "`src/api_client.py`, which gets the data from CSE; "
 "`src/selenium_scraper.py`, which opens the site in a real browser; "
 "`config.py`, the settings; and `warm_cache.py`, which saves a copy of the "
 "data so the app works offline."),

("Easy", "What is an API, in plain words?",
 "A way for one program to ask another program for data. You send a "
 "request, and you get a reply back, usually as JSON. The lecture compared "
 "it to a waiter: you tell the waiter what you want, the waiter goes to the "
 "kitchen, and the food comes back."),

("Easy", "Why do websites have an API?",
 "So their own pages can load data without reloading the whole page, so "
 "other developers can build things with their data, and so that automated "
 "access does not have to go through the website itself, which is heavier."),

("Easy", "What is JSON?",
 "A text format for structured data, made of names and values, and lists of "
 "those. It is easy for programs to read, which is why almost every API "
 "replies in it."),

("Easy", "Which address gives you the main dataset?",
 "`https://www.cse.lk/api/tradeSummary`. One request to it returns today's "
 "trading for every listed company - around 290 of them."),

("Medium", "How did you find these addresses?",
 "We opened the CSE site in a browser, pressed F12 to open the developer "
 "tools, opened the Network tab, and reloaded the page. That tab lists "
 "every request the page makes while it loads, and among them were the "
 "calls the page was making to its own backend."),

("Medium", "Why do those addresses need POST and not GET?",
 "Because that is what the server accepts. Sending a GET returns an error. "
 "It is a little unusual, because the requests only read data and GET would "
 "be the normal choice, but it is the server's decision and we found it by "
 "trying both.\n\n"
 "`config.ENDPOINTS` records which method each address needs, so `call()` "
 "picks the right one automatically.",
 "ENDPOINTS = {\n"
 "    \"tradeSummary\":    {\"method\": \"POST\", ...},\n"
 "    \"allSecurityCode\": {\"method\": \"GET\",  ...},\n"
 "}"),

("Medium", "Walk me through `call()`.",
 "It takes the short name of an address, looks up whether it needs GET or "
 "POST in `config.ENDPOINTS`, builds the full address, and hands it to "
 "`Scraper.fetch()`.\n\n"
 "It also passes `save_as=endpoint`, which is what gives the saved copy a "
 "readable filename such as `data/cache/tradeSummary.json`.",
 "def call(self, endpoint, data=None):\n"
 "    method = config.ENDPOINTS.get(endpoint, {}).get(\"method\", \"POST\")\n"
 "    url = f\"{config.API_BASE}/{endpoint}\"\n"
 "    return self.scraper.fetch(url, method=method, data=data,\n"
 "                              save_as=endpoint)"),

("Medium", "Why do you need `get_records()`?",
 "Because the replies do not all have the same shape. Some addresses return "
 "a plain list of records. Others wrap the list inside a dictionary under a "
 "name such as `reqTradeSummery`. A couple return a list inside another "
 "list.\n\n"
 "`get_records()` handles all of those and always hands back a plain list, "
 "so the rest of the code does not have to care which address it came "
 "from."),

("Medium", "How does a JSON reply become a table?",
 "The reply is a list of dictionaries, where each dictionary is one "
 "company. `pd.DataFrame()` accepts exactly that - it makes one row per "
 "dictionary and one column per key. So it is a single line once "
 "`get_records()` has found the list."),

("Medium", "How does `company_info()` differ from the other methods?",
 "It sends a value with the request. The address needs to know which "
 "company you mean, so we pass `data={\"symbol\": \"SAMP.N0000\"}` in the "
 "POST. The others take no parameters.\n\n"
 "The reply also has several sections, and the company details are inside "
 "the one called `reqSymbolInfo`, so we take that part out."),

("Medium", "What does a symbol like `SAMP.N0000` mean?",
 "`SAMP` is the company - Sampath Bank. `N` means voting shares, where `X` "
 "would mean non-voting. `0000` is the share class number. A company can "
 "appear more than once if it has different classes of share listed."),

("Medium", "Why is `several_companies()` slow?",
 "Because each company is a separate request, and every request waits its "
 "1.5 seconds first. Fifteen companies takes a little over 20 seconds.\n\n"
 "That is deliberate. It is the only loop in the project that sends many "
 "requests in a row, so it is where politeness matters most."),

("Medium", "What is `to_datetime()` for?",
 "CSE sends dates as the number of milliseconds since 1970 - a number like "
 "`1786440420412`. That is unreadable, and worse, pandas would treat it as "
 "an ordinary number. `to_datetime()` divides by 1000 and converts it into "
 "a real date and time."),

("Hard", "Why is using the API better than scraping the page, and is it "
         "fair to CSE?",
 "It is better for us because it is faster, more reliable, and gives every "
 "company in one request instead of one page at a time.\n\n"
 "It is also easier on CSE, which is the part that matters ethically. "
 "Loading the page makes their server send the HTML, the JavaScript "
 "bundles, the fonts and the images, and then the browser calls that same "
 "data address at the end of it anyway. Going straight to the data address "
 "skips all of that work.\n\n"
 "The Week 6 lecture said it directly: use APIs where available, because "
 "they are more reliable and more structured than scraping."),

("Hard", "What are the limitations of relying on an API?",
 "Rate limits, if the provider sets them. Needing a key or an account for "
 "many APIs, although not this one. Only getting the data the provider "
 "chose to expose, which may be less than the website shows. And the "
 "biggest one for us: an API can change without warning, and ours is not "
 "officially documented, so CSE has no reason to tell anybody before "
 "changing it.\n\n"
 "The way we guard against that is keeping every address in `config.py`, so "
 "a change means editing one table."),

("Hard", "The reply for one company has several sections. How did you know "
         "which one to use?",
 "By printing the reply and looking at it. The top level keys were "
 "`reqSymbolInfo`, `reqSymbolBetaInfo`, `reqLogo` and `reqTagsLogo`.\n\n"
 "The prices and the market value were inside `reqSymbolInfo`, so that is "
 "the part we take. The others hold the logo image paths and a volatility "
 "figure we do not use."),

#=========================================================================#
#  SELENIUM                                                               #
#=========================================================================#

("Easy", "What is Selenium?",
 "A tool that controls a real web browser from code. It can open pages, "
 "click things, type into boxes and read what is on screen, exactly as a "
 "person would."),

("Easy", "Which browser does your code use?",
 "Microsoft Edge, because that is what is installed on this machine. The "
 "code tries Edge first, then Chrome, then Firefox, so it works on anybody's "
 "computer."),

("Easy", "What does headless mean?",
 "The browser runs without showing a window. It is faster and it does not "
 "interrupt a demonstration by popping up on screen. Our code can do "
 "either."),

("Medium", "How does Selenium solve the JavaScript problem?",
 "Because it is a real browser, the JavaScript actually runs. The browser "
 "loads the page, the scripts fetch the data, and the table gets built.\n\n"
 "We then ask the browser for the finished HTML with `driver.page_source`, "
 "which is the page after JavaScript. That is the key difference from "
 "`response.text` in the `requests` version.",
 "driver.get(url)                 # browser loads and runs the page\n"
 "html = driver.page_source       # the page AFTER JavaScript\n"
 "soup = BeautifulSoup(html, \"html.parser\")   # then as normal"),

("Medium", "What is `WebDriverWait`, and why not just use `sleep`?",
 "When the browser first opens the page the table does not exist yet, "
 "because JavaScript is still fetching the data. If we read the HTML "
 "immediately we would get the same empty page `requests` gets.\n\n"
 "`WebDriverWait` pauses until the element actually appears, then carries "
 "on straight away. A fixed `sleep` is worse in both directions - too short "
 "and it fails on a slow connection, too long and it wastes time on every "
 "run.",
 "WebDriverWait(driver, 15).until(\n"
 "    expected_conditions.presence_of_element_located(\n"
 "        (By.TAG_NAME, \"table\")))"),

("Medium", "Why is `driver.quit()` inside a `finally` block?",
 "So it always runs, even if something goes wrong in the middle. If the "
 "browser is not closed it keeps running in the background using memory, "
 "and after a few failed runs there would be several invisible browsers "
 "open."),

("Medium", "How do you turn the rendered table into a DataFrame?",
 "We find the `<table>` with BeautifulSoup, take the heading cells from the "
 "`<th>` tags, and then loop over the `<tr>` rows taking the `<td>` cells "
 "with `get_text(strip=True)`. That gives a list of rows, which "
 "`pd.DataFrame()` turns into a table.\n\n"
 "If the number of headings does not match the number of cells we number "
 "the columns instead, so we never lose the rows."),

("Medium", "Selenium needs a driver. How is that handled?",
 "Since Selenium 4.6 it handles it itself. Selenium Manager works out which "
 "browser is installed, downloads the matching driver the first time it "
 "runs, and remembers it. Older tutorials tell you to download chromedriver "
 "by hand and match the version, which is no longer necessary."),

("Hard", "Selenium works. Why is it not your main method?",
 "Three reasons.\n\n"
 "It is slow - several seconds against about one for the data address. It "
 "is heavy on CSE, because it makes them serve the whole page and all its "
 "assets. And it only gets part of the data, because the table on screen is "
 "paginated, so one load gives about 25 companies rather than all 290.\n\n"
 "We keep it because it proves the browser approach works, and because it "
 "would be our fallback if the data addresses ever changed."),

("Hard", "How would you use Selenium to get all 290 companies?",
 "You would have to work through the pagination - find the next page "
 "button, click it, wait for the table to reload, read it, and repeat until "
 "the button is disabled, collecting the rows as you go.\n\n"
 "That is perfectly doable, but it means one page load per 25 companies, "
 "so roughly twelve full page loads with a wait after each. Against a "
 "single request that returns everything, it is hard to justify."),

("Hard", "Why does your Selenium code set the same User-Agent as the rest "
         "of the project?",
 "So CSE sees one consistent visitor rather than two different unknown "
 "programs. If we identify ourselves honestly in the API requests but let "
 "the browser send its default Edge User-Agent, the same project would look "
 "like two separate things in their logs, and only one of them would be "
 "identifiable."),

("Hard", "What is the difference between what `requests` returns and what "
         "Selenium returns for the same page?",
 "The same address gives about 25,000 bytes with roughly 24 characters of "
 "text and no tables through `requests`, and about 140,000 bytes with "
 "roughly 4,000 characters of text and a real table through Selenium.\n\n"
 "Same URL, same parsing code afterwards. The only difference is that one "
 "of them ran the JavaScript."),

("Easy", "What does `warm_cache.py` do?",
 "It collects everything once and saves a copy of every reply to "
 "`data/cache/`. Running it before a demonstration means the app still "
 "works if the internet is unavailable, and it also means the "
 "demonstration itself sends almost no requests to CSE."),

]
