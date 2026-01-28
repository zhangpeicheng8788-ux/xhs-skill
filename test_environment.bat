@echo off
REM Auto-Redbook Skill V6.6 - Environment Test Tool
REM Test Python environment and dependencies

echo ========================================
echo Auto-Redbook Skill V6.6
echo Environment Test Tool
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python...
C:\Python314\python.exe --version
if errorlevel 1 (
    echo [ERROR] Python not found at C:\Python314\
    echo [INFO] Please install Python 3.14 or update the path
    pause
    exit /b 1
)
echo [OK] Python found
echo.

echo [2/3] Checking syntax...
C:\Python314\python.exe -m py_compile scripts\publish_gui.py
if errorlevel 1 (
    echo [ERROR] Syntax error in publish_gui.py
    pause
    exit /b 1
)
C:\Python314\python.exe -m py_compile scripts\progress_viewer_gui.py
if errorlevel 1 (
    echo [ERROR] Syntax error in progress_viewer_gui.py
    pause
    exit /b 1
)
echo [OK] Syntax check passed
echo.

echo [3/3] Checking dependencies...
C:\Python314\python.exe -c "import tkinter; import xhs; import dotenv; print('[OK] All dependencies installed')"
if errorlevel 1 (
    echo [WARNING] Missing dependencies
    echo [INFO] Installing dependencies...
    C:\Python314\python.exe -m pip install xhs python-dotenv
    echo.
    echo [INFO] Please run this test again to verify
)
echo.

echo ========================================
echo Test completed!
echo You can now run: start_publish.bat
echo ========================================
echo.

pause
