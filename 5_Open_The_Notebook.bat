@echo off
rem ======================================================================
rem  5_Open_The_Notebook.bat
rem  Opens notebooks\CSE_Data_Collection.ipynb in Jupyter Notebook, in
rem  your browser. The notebook walks through the whole project one
rem  small step at a time, using the same code as the app.
rem
rem  The first time, it installs Jupyter Notebook into the project's
rem  .venv folder (needs internet, about 1 to 3 minutes).
rem  Close this window to stop Jupyter.
rem ======================================================================

setlocal
title Step 5 - Jupyter Notebook (close this window to stop it)
cd /d "%~dp0"
color 07

if not exist "app.py" goto not_unzipped
if not exist ".venv\Scripts\python.exe" goto not_set_up
".venv\Scripts\python.exe" -c "import gradio, pandas, requests, bs4" >nul 2>&1
if errorlevel 1 goto not_set_up

rem ---- Install Jupyter the first time -------------------------------------
".venv\Scripts\python.exe" -c "import notebook" >nul 2>&1
if not errorlevel 1 goto open_it
echo Installing Jupyter Notebook - only the first time.
echo This needs internet and takes 1 to 3 minutes.
echo.
".venv\Scripts\python.exe" -m pip install notebook --disable-pip-version-check --timeout 120 --retries 10
if errorlevel 1 goto install_failed
echo.

:open_it
echo ============================================================
echo   OPENING THE NOTEBOOK IN YOUR BROWSER
echo ============================================================
echo.
echo How to use it:
echo   - Click a grey box of code, then press Shift + Enter to run it.
echo     Its result appears underneath. Go down one box at a time.
echo   - Or use the menu:  Run  then  Run All Cells.
echo.
echo ------------------------------------------------------------
echo   KEEP THIS WINDOW OPEN while you use the notebook.
echo   To STOP Jupyter, close this window.
echo ------------------------------------------------------------
echo.
".venv\Scripts\python.exe" -m notebook "notebooks\CSE_Data_Collection.ipynb"

echo.
echo Jupyter has stopped.
pause
exit /b 0

:install_failed
color 4F
echo.
echo Jupyter did not install. Check the internet is working, then
echo double-click this file again.
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
