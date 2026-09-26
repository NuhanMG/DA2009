@echo off
rem ======================================================================
rem  2_START_The_App.bat
rem  Double-click to start the CSE Data Collection app.
rem
rem  DA 2009 - Assignment 2
rem  25ada072 - Pasindu  |  25ada073 - Sasini
rem  25ada141 - Salaama  |  24ada076 - Nuhan
rem
rem  What it does:
rem    1. If the app is already running, it just opens the browser.
rem    2. Checks that 1_SETUP_First_Time_Only.bat has been run.
rem    3. Starts the app (python app.py --open), which opens the browser
rem       at http://127.0.0.1:7860 by itself.
rem  Close this window to stop the app.
rem ======================================================================

setlocal
title CSE Data Collection - DA 2009 (close this window to stop the app)
cd /d "%~dp0"
color 07

echo ============================================================
echo   Colombo Stock Exchange - Web Data Collection
echo   DA 2009 - Assignment 2
echo ============================================================
echo.

if not exist "app.py" goto not_unzipped

rem ---- 1. Already running? Then just open it. -------------------------
netstat -ano | findstr /r /c:":7860 .*LISTENING" >nul
if errorlevel 1 goto check_setup
echo The app is already running. Opening it in your browser...
start "" "http://127.0.0.1:7860"
"%SystemRoot%\System32\timeout.exe" /t 3 >nul
exit /b 0

rem ---- 2. Has setup been done? ------------------------------------------
:check_setup
if not exist ".venv\Scripts\python.exe" goto not_set_up
".venv\Scripts\python.exe" -c "import gradio, pandas, requests, bs4" >nul 2>&1
if errorlevel 1 goto not_set_up

rem ---- 3. A reminder about Tesseract, which pip cannot install ---------
".venv\Scripts\python.exe" -c "import sys; from src.ocr_extractor import tesseract_ready; sys.exit(0 if tesseract_ready()[0] else 1)" >nul 2>&1
if not errorlevel 1 goto start_app
echo Note: Tesseract is not installed, so the OCR tab will not work.
echo Every other tab works normally. To add it, run
echo 1_SETUP_First_Time_Only again and press Y for Tesseract.
echo.

rem ---- 4. Start ---------------------------------------------------------
:start_app
echo Starting the app. Your browser will open by itself in a moment.
echo If it does not, open your browser and go to:
echo.
echo       http://127.0.0.1:7860
echo.
echo ------------------------------------------------------------
echo   KEEP THIS WINDOW OPEN while you use the app.
echo   You can make it small (the _ button, top right).
echo   To STOP the app, close this window (the X, top right).
echo ------------------------------------------------------------
echo.
".venv\Scripts\python.exe" app.py --open

echo.
echo The app has stopped.
pause
exit /b 0


:not_unzipped
color 4F
echo STOP - the project has not been unzipped yet.
echo.
echo You opened this file from inside the ZIP file, and Windows cannot
echo run it from there.
echo.
echo How to fix it:
echo   1. Close this window.
echo   2. Go to your Downloads folder and find the ZIP file.
echo   3. Right-click it and choose "Extract All...", then click Extract.
echo   4. Open the new folder and double-click
echo      1_SETUP_First_Time_Only first.
echo.
pause
exit /b 1

:not_set_up
color 4F
echo STOP - setup has not been done on this computer yet.
echo.
echo How to fix it:
echo   1. Close this window.
echo   2. Double-click  1_SETUP_First_Time_Only  and wait until its
echo      window turns GREEN.
echo   3. Then double-click this file again.
echo.
pause
exit /b 1
