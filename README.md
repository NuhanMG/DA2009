# 📈 CSE Data Collection — DA 2009 Group Project

**READ ME FIRST.** This page tells you, step by step, how to get our project
working on your own computer. You do not need to know anything about
computers or programming. Just do the steps in order, one at a time.

**What the project does:** it collects share prices, company details and
company announcements from the Colombo Stock Exchange website
([cse.lk](https://www.cse.lk)) and shows them in an app that opens in your
web browser.

**Group:** 24ada076 - Nuhan · 25ada072 - Pasindu · 25ada073 - Sasini · 25ada141 - Salaama
**Course:** DA 2009 — Data Collection Methods II · Assignment 2 · University of Colombo

---

## ✅ What you need

- A **Windows 10 or Windows 11** computer (not a Mac, not a phone)
- **Internet**
- About **2 GB of free space**
- About **30 minutes** the first time. After that, starting the app takes
  about 10 seconds.

## 🗺️ The steps at a glance

| Step | What you do | How often |
|---|---|---|
| **1** | Download the project | Only once |
| **2** | Unblock and unzip it | Only once |
| **3** | Double-click `1_SETUP_First_Time_Only` | Only once |
| **4** | Double-click `2_START_The_App` | Every time you want to use the app |
| **5** | Try each tab of the app | |
| **6** | Learn how it works | |

---

## Step 1 — Download the project

1. You are on the project's GitHub page right now.
2. Scroll to the **top** of this page. Find the **green button** that says
   **`<> Code`**. Click it.
3. A small box opens. Click **Download ZIP** at the bottom of the box.
4. Your browser downloads a file called
   **`DA2009-CSE-Data-Collection-main.zip`** into your **Downloads** folder.

> 📦 A **ZIP file** is like a box with all the project's files packed
> inside. We have to unpack it before we can use it. That is Step 2.

---

## Step 2 — Unblock and unzip

Windows is careful with files that come from the internet. If we
**unblock** the ZIP file first, Windows will not stop you with a warning
every time you open one of the project's files.

1. Open your **Downloads** folder:
   press the **Windows key** and the **E** key together. A File Explorer
   window opens. Click **Downloads** on the left side.
2. **Right-click** the file `DA2009-CSE-Data-Collection-main.zip` and click
   **Properties** (near the bottom of the list).
3. Look at the bottom of the window that opens. If you see the word
   **Unblock** with a small box next to it, **tick the box**. Then click
   **OK**.
   *(If there is no Unblock box, that is fine. Just click OK.)*
4. **Right-click** the ZIP file again and click **Extract All...**
5. A window opens. Do not change anything. Just click **Extract**.
6. A new folder opens. Inside it there is **another folder with the same
   name**, `DA2009-CSE-Data-Collection-main`. **Double-click it** to go
   inside.
7. You are in the right place when you can see files called
   **`1_SETUP_First_Time_Only`**, **`2_START_The_App`** and so on.

> 💡 Windows may hide the end of the file names. `1_SETUP_First_Time_Only`
> and `1_SETUP_First_Time_Only.bat` are the same file. In the **Type**
> column it says **Windows Batch File**.

---

## Step 3 — Set up (only the first time)

1. **Double-click** `1_SETUP_First_Time_Only`.
2. A **black window** opens. That is normal. It is where the computer shows
   you what it is doing.
3. Windows might show a warning first:
   - A blue box, **"Windows protected your PC"** → click **More info**,
     then click **Run anyway**.
   - A box, **"Open File – Security Warning"** → click **Run**.
4. **If it asks "Install Python 3.12 now?"** → press the **Y** key on your
   keyboard. *(Python is the free program our project is written in.)*
   Wait 1 to 2 minutes.
5. Now it installs the project's packages. **Lots of text scrolls past —
   that is normal.** This takes **5 to 15 minutes** — or longer on slow
   internet. Do not close the window. ☕ Go and get a cup of tea.
   If the internet drops for a moment, it tries again by itself.
6. **If it asks "Install Tesseract now?"** → press **Y**.
   *(Tesseract reads words from pictures of pages. The OCR tab needs it.)*
   Windows then asks **"Do you want to allow this app to make changes to
   your device?"** → click **Yes**.
7. When the window turns **🟩 GREEN** and says **ALL DONE - SETUP WORKED!**,
   press any key to close it. 🎉 You never have to do Step 3 again on this
   computer.

> 🟥 If the window turns **RED**, read what it says. It tells you exactly
> what to do. Also see [Something went wrong?](#-something-went-wrong)
> below.

---

## Step 4 — Start the app (every time)

1. **Double-click** `2_START_The_App`.
2. A black window opens. After about **10 to 20 seconds** your web browser
   opens the app by itself.
   - If the browser does not open, open **Chrome** or **Edge** yourself,
     click the address bar at the very top, type this and press **Enter**:

     ```
     http://127.0.0.1:7860
     ```

3. **Keep the black window open** while you use the app. You can make it
   small with the **`_`** button in its top-right corner — just do not
   close it.
4. When you are finished: close the browser tab, then close the black
   window with the **X** in its top-right corner. That stops the app.

> 🏠 The app runs on **your own computer**. `127.0.0.1` means "this
> computer". Nobody else can see it.

---

## Step 5 — Try the app, tab by tab

The **tabs** are the words along the top of the app. Click each one in
turn and do what the table says. Each tab also shows which member's part it
is.

| Tab | What to click | What you will see | Whose part |
|---|---|---|---|
| **Home** | Nothing — just read it | What the project collects, and who did what | Everyone |
| **Ethics** | **Read robots.txt**, then **Show the request log** | The website's rules for robots, and a list of every request we sent | Nuhan |
| **Market Data** | **Get the market data**, then wait about 15 seconds | Today's price for every company, the index, and the sectors | Pasindu |
| **Companies** | **Load the company list** → choose a company → **Get details**. Or move the slider and click **Collect them** | Details for one company, or for many at once | Pasindu |
| **Announcements** | **Get the announcements** → **Download** → choose a document → **Read the text** | Company notices, their PDF files, and the words inside the PDFs | Sasini and Nuhan |
| **OCR** | Choose a scanned document → **Read it** | The computer reading words from a *picture* of a page | Salaama |
| **Data & Export** | **Clean and check** → **Draw the charts** → **Save** | Tidied data, charts, and the data saved as CSV, Excel and JSON files | Sasini and Salaama |

💡 **Good to know**

- **It is slow on purpose.** The project waits 1.5 seconds between requests
  so it does not overload the website. That is part of "ethical scraping".
- Do **Market Data** before **Data & Export**. Data & Export cleans the
  data that Market Data collected.
- On **weekends and public holidays** the stock market is closed, so you
  see the numbers from the last day it was open.
- The **OCR** list only shows *scanned* documents. If it is empty, go to
  **Announcements**, move the slider to **10**, click **Download**, then
  press **F5** to refresh the page. Not every document is scanned, so the
  list can still be empty — that is OK.
- Files you save go into the **`data\exports`** folder inside the project
  folder.
- The **Light theme** button at the top makes the app easier to see on a
  projector.

---

## Step 6 — Learn how it works

These files help you understand what is happening inside the project.
Double-click them the same way.

| File | What it does | When to use it |
|---|---|---|
| `3_Collect_Fresh_Data` | Collects everything from the website in one go (1 to 2 minutes) and saves a copy, so the app still works later **without internet** | Before showing the app somewhere with bad internet — like the viva |
| `4_Run_Each_Members_Part` | A **menu**. Type a number and press Enter to run **one member's part on its own** and see what it prints. Then press **Y** to open that part's code in Notepad | To learn **your own part** |
| `5_Open_The_Notebook` | Opens a step-by-step walkthrough of the whole project in your browser. The first time, it installs Jupyter (1 to 3 minutes) | To follow the whole project from start to end |
| `6_Run_The_Scrapy_Spider` | Runs the Scrapy spider, which collects the list of announcements | To see Scrapy working |
| `Run_CSE_App` | Exactly the same as `2_START_The_App`. It is here because the team guides mention it | |

### 📚 A good order to learn in

1. **Use the app**, tab by tab (Step 5).
2. Open **`4_Run_Each_Members_Part`** and run **your own numbers** (see the
   table below). Read what it prints. Then press **Y** to read the code.
3. Read **your own member document** in the `docs\member_documents` folder,
   and the team guide `docs\CSE_Team_Guide.pdf`.
4. Open **`5_Open_The_Notebook`**. Click the first grey box of code and
   press **Shift + Enter** to run it. Keep going, one box at a time.
5. For the full technical explanation, read
   **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)**.

### 👥 Who wrote what

| Member | Their part | Menu numbers in `4_Run_Each_Members_Part` | Their code files |
|---|---|---|---|
| **24ada076 - Nuhan** | Ethical scraping and robots.txt, BeautifulSoup, reading PDFs | 1, 2, 3 | `src\ethics.py`, `src\static_scraper.py`, `src\pdf_extractor.py` |
| **25ada072 - Pasindu** | Getting the data from the website, Selenium | 4, 5 (and file `3_Collect_Fresh_Data`) | `src\api_client.py`, `src\selenium_scraper.py`, `config.py`, `warm_cache.py` |
| **25ada073 - Sasini** | Crawling for documents, cleaning the data | 6, 7, 8 | `src\crawler.py`, `src\cleaner.py`, the `scrapy_project` folder |
| **25ada141 - Salaama** | OCR, saving the files, the charts | 9, 10, 11 | `src\ocr_extractor.py`, `src\storage.py`, `src\analysis.py` |

> ⚠️ **To read a code file** (a file ending in `.py`): **right-click** it →
> **Open with** → **Notepad**. Do **not** double-click `.py` files — that
> tries to run them instead of showing them.

---

## 🆘 Something went wrong?

**Running `1_SETUP_First_Time_Only` again fixes most problems.** It is
always safe to run it again.

| What you see | What to do |
|---|---|
| **"Windows protected your PC"** | Click **More info**, then **Run anyway**. Our `.bat` files are plain text — you can read them: right-click → **Edit** (or Open with → Notepad). |
| **"Open File – Security Warning"** every time | Click **Run**. To stop it asking, do the **Unblock** part of Step 2 on a fresh download. |
| 🟥 RED: *"the project has not been unzipped yet"* | You opened the file from inside the ZIP. Do Step 2 (**Extract All**). |
| 🟥 RED: *"setup has not been done"* | Double-click `1_SETUP_First_Time_Only` first and wait for 🟩 GREEN. |
| 🟥 RED: *"the packages did not finish installing"* | This is almost always the internet. Check the internet works, then run `1_SETUP_First_Time_Only` again. It carries on from where it stopped. |
| 🟥 RED: *"this folder is inside too many other folders"* | Move the project folder into your **Downloads** folder (right-click → **Cut**, open Downloads, right-click → **Paste**), then run `1_SETUP_First_Time_Only` again. |
| The **Python download page** opens | Your computer could not install Python by itself. On that page click **Download Python**, open the file, **tick "Add python.exe to PATH"** at the bottom of the first screen, and click **Install Now**. Then run `1_SETUP_First_Time_Only` again. |
| The browser did not open | Type `http://127.0.0.1:7860` into your browser's address bar and press Enter. |
| Browser says **"This site can't be reached"** | The black window was closed, so the app stopped. Double-click `2_START_The_App` again. |
| Tables are empty, or it says **"No data"** | Check your internet. The CSE website may be down — try again later. |
| The **OCR** tab says Tesseract is not installed | Close the app. Run `1_SETUP_First_Time_Only` again and press **Y** for Tesseract. Start the app again. |
| Something else | Take a photo of the black window and send it to the group. |

---

## 🔄 Getting a newer version

If the project is updated, do **Step 1** and **Step 2** again (you get a new
folder), then **Step 3** inside the new folder. You can delete the old
folder afterwards.

## 🗑️ Removing everything

Delete the project folder. Python and Tesseract can be removed in
**Settings → Apps → Installed apps**, like any other program.

---

## 📁 What is in this folder

| Name | What it is |
|---|---|
| `1_...` to `6_...` | The files you double-click |
| `app.py` | The app itself |
| `src` | Each member's code — one file for each job |
| `docs` | The team guide, each member's document, the slides, the ethics statement and viva notes |
| `notebooks` | The step-by-step walkthrough notebook |
| `scrapy_project` | The Scrapy spider |
| `config.py` | All the settings, in one place |
| `requirements.txt` | The list of packages that setup installs |
| `HOW_IT_WORKS.md` | The technical explanation of the project |
| `.venv` | Made by setup. Holds Python and the packages for this project only |
| `data` | Made when you collect data. Everything you collect and save goes here |
| `logs` | Made when you collect data. `request_log.csv` lists every request sent |

## 📖 Words you might meet

| Word | What it means |
|---|---|
| **Folder** | A place on the computer where files are kept, like a drawer |
| **Double-click** | Click the left mouse button twice, quickly |
| **Right-click** | Click the right mouse button once. A menu appears |
| **ZIP file** | One file with many files packed inside it |
| **.bat file** | A list of instructions the computer follows by itself, one after another. Ours are plain text, so you can read them in Notepad |
| **Black window** | Also called the Command Prompt. It shows what a `.bat` file is doing |
| **Browser** | The program you use for websites: Chrome, Edge or Firefox |
| **Python** | The programming language our project is written in |
| **Package** | Ready-made code someone else wrote that our project uses — for example **pandas** for tables |
| **Scraping** | Collecting information from a website with a program, instead of copying it by hand |
| **OCR** | Optical Character Recognition — the computer reading words from a picture |

---

**Data source:** Colombo Stock Exchange (https://www.cse.lk). Collected for
academic purposes only — DA 2009, University of Colombo. This is not
investment advice.
