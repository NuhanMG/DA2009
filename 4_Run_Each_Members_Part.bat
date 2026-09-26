@echo off
rem ======================================================================
rem  4_Run_Each_Members_Part.bat
rem  A menu that runs each member's part of the project on its own, so
rem  you can see what that one file does. After it runs, it can open
rem  the code in Notepad so you can read how it works.
rem
rem  Each choice runs one line, for example:
rem      python -m src.ethics
rem  which is the same as the "Running each part on its own" list in
rem  HOW_IT_WORKS.md.
rem ======================================================================

setlocal
title Step 4 - Run each member's part on its own
cd /d "%~dp0"

if not exist "app.py" goto not_unzipped
if not exist ".venv\Scripts\python.exe" goto not_set_up
".venv\Scripts\python.exe" -c "import gradio, pandas, requests, bs4" >nul 2>&1
if errorlevel 1 goto not_set_up

:menu
cls
color 07
echo ============================================================
echo   RUN EACH MEMBER'S PART ON ITS OWN
echo ============================================================
echo   Each part is one Python file. Pick one to run it and see
echo   what it prints. Afterwards you can open its code to read it.
echo.
echo   NUHAN - 24ada076      ethics, BeautifulSoup and PDFs
echo     1   Ethics - reads robots.txt, sends one polite request
echo     2   Static scraper - requests + BeautifulSoup
echo     3   PDF reader - PyPDF2 and pdfplumber     [do 6 first]
echo.
echo   PASINDU - 25ada072    getting the data, and Selenium
echo     4   API client - share prices, one company, circulars
echo     5   Selenium - opens the page in a hidden browser
echo.
echo   SASINI - 25ada073     crawling and cleaning
echo     6   Crawler - finds and downloads announcement PDFs
echo     7   Cleaner - cleans and checks the share prices
echo     8   Scrapy spider - collects announcements with Scrapy
echo.
echo   SALAAMA - 25ada141    OCR, saving files, and charts
echo     9   OCR - reads a scanned PDF page         [do 6 first]
echo     10  Storage - saves a table as CSV, Excel and JSON
echo     11  Analysis - summary figures and charts
echo.
echo     0   Close this window
echo ============================================================
echo.
set "PICK="
set "MOD="
set "CODE="
set /p "PICK=Type a number and press Enter: "

if "%PICK%"=="0" exit /b 0
if "%PICK%"=="1"  (set "MOD=src.ethics"          & set "CODE=src\ethics.py")
if "%PICK%"=="2"  (set "MOD=src.static_scraper"  & set "CODE=src\static_scraper.py")
if "%PICK%"=="3"  (set "MOD=src.pdf_extractor"   & set "CODE=src\pdf_extractor.py")
if "%PICK%"=="4"  (set "MOD=src.api_client"      & set "CODE=src\api_client.py")
if "%PICK%"=="5"  (set "MOD=src.selenium_scraper" & set "CODE=src\selenium_scraper.py")
if "%PICK%"=="6"  (set "MOD=src.crawler"         & set "CODE=src\crawler.py")
if "%PICK%"=="7"  (set "MOD=src.cleaner"         & set "CODE=src\cleaner.py")
if "%PICK%"=="8"  goto scrapy
if "%PICK%"=="9"  (set "MOD=src.ocr_extractor"   & set "CODE=src\ocr_extractor.py")
if "%PICK%"=="10" (set "MOD=src.storage"         & set "CODE=src\storage.py")
if "%PICK%"=="11" (set "MOD=src.analysis"        & set "CODE=src\analysis.py")
if not defined MOD goto bad_pick

cls
echo ============================================================
echo   Running:  python -m %MOD%
echo   Code in:  %CODE%
echo ============================================================
echo.
".venv\Scripts\python.exe" -m %MOD%
goto after_run

:scrapy
set "CODE=scrapy_project\cse_crawler\spiders\cse_announcements.py"
cls
echo ============================================================
echo   Running the Scrapy spider
echo   Code in:  %CODE%
echo ============================================================
echo.
echo Scrapy prints a lot of lines while it works - that is normal.
echo.
pushd scrapy_project
"..\.venv\Scripts\python.exe" -m scrapy crawl cse_announcements -O ../data/scrapy_output.json
popd
echo.
echo The spider saved what it collected to  data\scrapy_output.json
goto after_run

:after_run
echo.
echo ------------------------------------------------------------
echo   Finished. Scroll up to read everything it printed.
echo   The code for this part is in:  %CODE%
echo ------------------------------------------------------------
echo.
choice /c YN /m "Open that code in Notepad so you can read it"
if errorlevel 2 goto menu
start "" notepad "%CODE%"
goto menu

:bad_pick
echo.
echo That is not one of the numbers on the list. Try again.
"%SystemRoot%\System32\timeout.exe" /t 2 >nul
goto menu


:not_unzipped
color 4F
echo STOP - the project has not been unzipped yet.
echo Right-click the ZIP file, choose "Extract All...", then open the
echo new folder and double-click 1_SETUP_First_Time_Only first.
echo.
pause
exit /b 1

:not_set_up
color 4F
echo STOP - setup has not been done on this computer yet.
echo.
echo Double-click  1_SETUP_First_Time_Only  first and wait until its
echo window turns GREEN. Then double-click this file again.
echo.
pause
exit /b 1
