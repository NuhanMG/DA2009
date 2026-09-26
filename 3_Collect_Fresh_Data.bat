@echo off
rem ======================================================================
rem  3_Collect_Fresh_Data.bat
rem  Collects today's data from the CSE website in one go and saves a
rem  copy of every reply, so the app also works without internet.
rem
rem  It runs:  python warm_cache.py        (written by 25ada072 - Pasindu)
rem
rem  It waits 1.5 seconds between requests on purpose, so it is polite
rem  to the website. That is why it takes a minute or two.
rem ======================================================================

setlocal
title Step 3 - Collecting fresh data from cse.lk
cd /d "%~dp0"
color 07

if not exist "app.py" goto not_unzipped
if not exist ".venv\Scripts\python.exe" goto not_set_up
".venv\Scripts\python.exe" -c "import gradio, pandas, requests, bs4" >nul 2>&1
if errorlevel 1 goto not_set_up

echo ============================================================
echo   COLLECTING FRESH DATA FROM THE CSE WEBSITE
echo ============================================================
echo.
echo This needs internet and takes about 1 to 2 minutes.
echo It waits 1.5 seconds between requests on purpose - that is
echo the "polite scraping" rule from our ethics section.
echo.

".venv\Scripts\python.exe" warm_cache.py
if errorlevel 1 goto failed

color 2F
echo.
echo ============================================================
echo   DONE!
echo.
echo   A folder window will open now so you can see what was saved:
echo     data\cache   a copy of every reply from the website
echo     data\pdfs    the announcement documents it downloaded
echo.
echo   Every request that was sent is listed in logs\request_log.csv
echo ============================================================
echo.
start "" "data"
pause
exit /b 0

:failed
color 4F
echo.
echo Something went wrong - the message above says what.
echo Check the internet is working, then try again.
echo.
pause
exit /b 1

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
