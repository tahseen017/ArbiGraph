@echo off
:: ArbiGraph Dashboard -- Windows runner (University-PC Safe Edition)
cd /d "%~dp0"

echo ================================================
echo   ArbiGraph -- FX ^& Crypto Arbitrage Terminal
echo ================================================
echo.

:: -------------------------------------------------------
:: Find a working Python 3.10+ interpreter.
:: Try: py -3  ->  py  ->  python3  ->  python
:: Each candidate is tested by actually running Python so
:: the Microsoft Store stub (which opens the Store instead
:: of running) is automatically skipped.
:: -------------------------------------------------------
set PY=

:: Candidate 1: py -3  (Windows Python Launcher -- most reliable on uni PCs)
py -3 -c "import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    set PY=py -3
    goto :found
)

:: Candidate 2: py  (launcher without explicit version flag)
py -c "import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    set PY=py
    goto :found
)

:: Candidate 3: python3
python3 -c "import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    set PY=python3
    goto :found
)

:: Candidate 4: python  (Microsoft Store stub exits non-zero, so this is safe)
python -c "import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    set PY=python
    goto :found
)

:: None of the candidates worked
echo.
echo  ERROR: Could not find Python 3.10 or higher on this machine.
echo.
echo  Tried: "py -3", "py", "python3", "python" -- all failed.
echo.
echo  HOW TO FIX (choose one):
echo.
echo  Option A -- Install Python from the web (recommended):
echo    1. Go to https://www.python.org/downloads/
echo    2. Download the latest Python 3.x installer
echo    3. Run the installer and CHECK "Add python.exe to PATH"
echo    4. Close this window and double-click run_dashboard.bat again
echo.
echo  Option B -- Use Microsoft Store:
echo    1. Open Start menu, search "Python"
echo    2. Install Python 3.x from Microsoft Store
echo    3. Close this window and double-click run_dashboard.bat again
echo.
pause
exit /b 1

:found
echo Python found ^(%PY%^):
%PY% --version
echo.

:: -------------------------------------------------------
:: Pick port 8000, fall back to 8001 if already occupied
:: -------------------------------------------------------
set PORT=8000
netstat -an 2>nul | find ":8000 " >nul 2>&1
if %errorlevel% equ 0 (
    echo Port 8000 is busy -- switching to port 8001...
    set PORT=8001
)

echo Starting ArbiGraph dashboard on port %PORT%...
echo.
echo   Open your browser to:  http://localhost:%PORT%
echo   Press Ctrl+C in this window to stop the server.
echo.

:: Auto-open the browser after 2 seconds
start /b cmd /c "timeout /t 2 >nul && start http://localhost:%PORT%"

:: Launch the server
%PY% app.py --host 0.0.0.0 --port %PORT%

echo.
echo Server stopped.
pause
