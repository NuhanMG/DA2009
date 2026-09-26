@echo off
rem ======================================================================
rem  6_Run_The_Scrapy_Spider.bat
rem  Runs the Scrapy spider, which collects the list of CSE announcements
rem  and their PDF links.                    (written by 25ada073 - Sasini)
rem
rem  It runs, from inside the scrapy_project folder:
rem      scrapy crawl cse_announcements -O ../data/scrapy_output.json
rem ======================================================================

setlocal
title Step 6 - The Scrapy spider
cd /d "%~dp0"
color 07

if not exist "app.py" goto not_unzipped
if not exist ".venv\Scripts\python.exe" goto not_set_up
".venv\Scripts\python.exe" -c "import scrapy" >nul 2>&1
if errorlevel 1 goto not_set_up

echo ============================================================
echo   RUNNING THE SCRAPY SPIDER
echo ============================================================
echo.
echo This needs internet. Scrapy prints a lot of lines while it
echo works - that is normal. It finishes with some statistics.
echo.
pushd scrapy_project
"..\.venv\Scripts\python.exe" -m scrapy crawl cse_announcements -O ../data/scrapy_output.json
set "RESULT=%errorlevel%"
popd
if not "%RESULT%"=="0" goto failed

color 2F
echo.
echo ============================================================
echo   DONE!
echo   What the spider collected is in:  data\scrapy_output.json
echo   The spider's code is in:
echo     scrapy_project\cse_crawler\spiders\cse_announcements.py
echo ============================================================
echo.
choice /c YN /m "Open the results in Notepad"
if errorlevel 2 goto end
start "" notepad "data\scrapy_output.json"
:end
exit /b 0

:failed
color 4F
echo.
echo The spider stopped with an error - the lines above say why.
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
