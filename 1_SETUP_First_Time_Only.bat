@echo off
rem ======================================================================
rem  1_SETUP_First_Time_Only.bat
rem  Double-click this ONCE on a new computer. It gets everything ready.
rem
rem  DA 2009 - Assignment 2
rem  25ada072 - Pasindu  |  25ada073 - Sasini
rem  25ada141 - Salaama  |  24ada076 - Nuhan
rem
rem  What it does, step by step:
rem    1. Checks the project was unzipped properly.
rem    2. Finds Python 3.10 or newer. If there is none, it offers to
rem       install Python 3.12 with winget (the installer built into
rem       Windows 10 and 11).
rem    3. Makes a private Python folder for this project (.venv) and
rem       installs the packages listed in requirements.txt into it.
rem    4. Offers to install Tesseract, the program the OCR tab uses.
rem
rem  Running it again is safe. It skips the parts that are already done.
rem ======================================================================

setlocal
title Step 1 - Setting up the CSE project
cd /d "%~dp0"
color 07

echo ============================================================
echo   STEP 1 - SETTING UP   (only needed once on each computer)
echo ============================================================
echo.

rem ---- 1. Was the ZIP file unzipped? ------------------------------------
rem  If this file was opened from inside the ZIP, Windows copies only
rem  this one file to a temporary folder, so app.py is not next to it.
if not exist "app.py" goto not_unzipped
if not exist "requirements.txt" goto not_unzipped

rem ---- Is the folder buried too deep? -----------------------------------
rem  Windows cannot handle file paths longer than 260 letters, and some
rem  of the packages have long file names. If this folder's own path is
rem  already over 110 letters, the install would fail halfway.
set "HERE=%~dp0"
if not "%HERE:~110,1%"=="" goto too_deep

rem ---- OneDrive folders sync every file to the internet -----------------
rem  The packages are about 1 GB of small files. OneDrive would try to
rem  upload all of them and can lock files while pip is installing.
echo "%HERE%" | "%SystemRoot%\System32\find.exe" /i "OneDrive" >nul
if errorlevel 1 goto check_venv
echo This folder is inside OneDrive, which uploads every file to the
echo internet. Setup puts about 1 GB of files here, so it works better
echo in your Downloads folder.
echo.
choice /c YN /m "Continue here anyway"
if errorlevel 2 goto move_it
echo.

rem ---- 2. Is the project's Python environment already working? ---------
:check_venv
if not exist ".venv\Scripts\python.exe" goto need_python
rem  A .venv copied from another computer points at a Python that is
rem  not on this one, so its python.exe will not even start.
".venv\Scripts\python.exe" -c "import sys" >nul 2>&1
if errorlevel 1 goto venv_broken
".venv\Scripts\python.exe" -c "import gradio, pandas, requests, bs4, scrapy, selenium, pdfplumber, PyPDF2, cv2, pytesseract, plotly, openpyxl" >nul 2>&1
if errorlevel 1 goto install_packages
echo [OK] The project's Python environment is already set up.
echo.
goto tesseract

:venv_broken
echo The Python environment in the .venv folder is not working on this
echo computer (it may have been copied from another computer).
echo It will be built again.
echo.

rem ---- 3. Find Python 3.10 or newer --------------------------------------
:need_python
call :find_python
if defined PY goto have_python

echo Python is not installed on this computer.
echo Python is the free program this project is written in.
echo.
where winget >nul 2>&1
if errorlevel 1 goto python_by_hand

choice /c YN /m "Install Python 3.12 now? Press Y for yes, N for no"
if errorlevel 2 goto python_by_hand
echo.
echo Installing Python 3.12 - this takes a minute or two...
winget install --id Python.Python.3.12 -e --scope user --silent --accept-package-agreements --accept-source-agreements
call :find_python
if defined PY goto have_python
rem  Some computers only allow the "for all users" kind of install.
winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
call :find_python
if defined PY goto have_python
goto python_by_hand

:have_python
echo [OK] Found Python:
%PY% --version
echo.

rem ---- 4. Build the environment and install the packages ---------------
echo Making the project's own Python folder (.venv)...
%PY% -m venv --clear .venv
if errorlevel 1 goto venv_failed

:install_packages
echo.
echo Installing the packages from requirements.txt.
echo This downloads about 300 MB and usually takes 5 to 15 minutes
echo (longer on slow internet).
echo Lots of text will scroll past - that is normal. Please wait.
echo.
rem  --timeout 120 --retries 10: on a slow connection some package lists
rem  (cryptography's is 2 MB) take longer than pip's usual 15 seconds, and
rem  pip then wrongly says "no matching distribution". So we wait longer.
set "PIP_OPTIONS=--disable-pip-version-check --timeout 120 --retries 10"
".venv\Scripts\python.exe" -m pip install --upgrade pip %PIP_OPTIONS%
".venv\Scripts\python.exe" -m pip install -r requirements.txt %PIP_OPTIONS%
if not errorlevel 1 goto check_packages

rem  One more go by itself - a dropped connection is the usual reason.
echo.
echo The internet stopped for a moment. Trying once more...
echo.
".venv\Scripts\python.exe" -m pip install -r requirements.txt %PIP_OPTIONS%
if errorlevel 1 goto pip_failed

:check_packages
".venv\Scripts\python.exe" -c "import gradio, pandas, requests, bs4, scrapy, selenium, pdfplumber, PyPDF2, cv2, pytesseract, plotly, openpyxl" >nul 2>&1
if errorlevel 1 goto pip_failed
echo.
echo [OK] All the Python packages are installed.
echo.

rem ---- 5. Tesseract, for the OCR tab --------------------------------------
:tesseract
call :tesseract_check
if not errorlevel 1 goto tesseract_ok

echo The OCR tab needs a free program called Tesseract, and it is not
echo installed yet. Everything else works without it.
echo.
where winget >nul 2>&1
if errorlevel 1 goto tesseract_by_hand

choice /c YN /m "Install Tesseract now? Press Y for yes, N for no"
if errorlevel 2 goto tesseract_skipped
echo.
echo Installing Tesseract. Windows will ask "Do you want to allow this
echo app to make changes to your device?" - click YES.
echo.
winget install --id UB-Mannheim.TesseractOCR -e --silent --accept-package-agreements --accept-source-agreements
call :tesseract_check
if not errorlevel 1 goto tesseract_ok
echo.
echo Tesseract did not install. If you clicked NO on the Windows
echo question, you can run this file again and click YES.
goto tesseract_by_hand

:tesseract_ok
echo [OK] Tesseract is installed, so the OCR tab will work.
goto all_done

:tesseract_by_hand
echo.
echo To install Tesseract by hand, open this page, download the
echo "tesseract-ocr-w64-setup" file, and install it with the normal
echo settings:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo.
:tesseract_skipped
echo Skipped Tesseract. The OCR tab will not work until it is
echo installed, but every other tab will. You can run this file again
echo later to install it.

rem ---- Finished ---------------------------------------------------------
:all_done
color 2F
echo.
echo ============================================================
echo.
echo   ALL DONE - SETUP WORKED!
echo.
echo   Next: close this window and double-click
echo         2_START_The_App
echo.
echo ============================================================
echo.
pause
exit /b 0


rem ======================================================================
rem  HELPERS
rem ======================================================================

rem ---- Looks for a Python that is 3.10 or newer, puts it in PY ----------
:find_python
set "PY="
call :try_python py -3.12
if not defined PY call :try_python py -3.13
if not defined PY call :try_python py -3.11
if not defined PY call :try_python py -3
if not defined PY call :try_python python
rem  Just after winget installs Python, this window does not know about
rem  it yet, so we also look in the places the installer puts it.
if not defined PY call :try_python "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY call :try_python "%ProgramFiles%\Python312\python.exe"
exit /b 0

:try_python
rem  Plain "python" can be a Microsoft Store shortcut that does nothing,
rem  so every one is tested by actually running it.
%* -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if not errorlevel 1 set "PY=%*"
exit /b 0

rem ---- Exit code 0 if Tesseract can be used, 1 if not -------------------
:tesseract_check
rem  Uses the project's own check, the same one the OCR tab uses.
".venv\Scripts\python.exe" -c "import sys; from src.ocr_extractor import tesseract_ready; sys.exit(0 if tesseract_ready()[0] else 1)" >nul 2>&1
exit /b %errorlevel%


rem ======================================================================
rem  PROBLEMS - each one explains what to do
rem ======================================================================

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
echo   4. Open the new folder and double-click this file again.
echo.
pause
exit /b 1

:too_deep
color 4F
echo STOP - this folder is inside too many other folders.
echo.
echo Its location is too long for Windows:
echo   "%HERE%"
echo.
echo How to fix it:
echo   1. Close this window.
echo   2. Move the project folder to your Downloads folder
echo      (right-click it, Cut, open Downloads, right-click, Paste).
echo   3. Double-click this file again from its new place.
echo.
pause
exit /b 1

:move_it
color 4F
echo.
echo OK. To move it:
echo   1. Close this window.
echo   2. Move the project folder to your Downloads folder
echo      (right-click it, Cut, open Downloads, right-click, Paste).
echo   3. Double-click this file again from its new place.
echo.
pause
exit /b 1

:python_by_hand
color 4F
echo.
echo Python needs to be installed by hand:
echo   1. Your browser will now open the Python download page.
echo   2. Click the yellow "Download Python" button.
echo   3. Open the file you downloaded.
echo   4. IMPORTANT: on the first screen, tick the box
echo      "Add python.exe to PATH", then click "Install Now".
echo   5. When it says "Setup was successful", close it.
echo   6. Double-click this file (1_SETUP_First_Time_Only) again.
echo.
start "" "https://www.python.org/downloads/"
pause
exit /b 1

:venv_failed
color 4F
echo.
echo Could not make the .venv folder. The message above says why.
echo Try running this file again. If it fails again, send a photo of
echo this window to the group.
echo.
pause
exit /b 1

:pip_failed
color 4F
echo.
echo ============================================================
echo   The packages did not finish installing.
echo ============================================================
echo.
echo This is nearly always the internet connection. Please:
echo   1. Check the internet is working (open any website).
echo   2. Close this window and double-click this file again.
echo      It carries on where it stopped.
echo.
echo If it fails again, send a photo of this window to the group.
echo.
pause
exit /b 1
