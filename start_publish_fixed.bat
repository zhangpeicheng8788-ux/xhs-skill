@echo off
title XHS Batch Publish GUI V3.0 Fixed

echo ============================================================
echo XHS Batch Publish Tool V3.0 Fixed (With Author Info)
echo ============================================================
echo.
echo Checking dependencies...
echo.

REM Check if pillow is installed
C:\Python314\python.exe -c "import PIL" 2>nul
if errorlevel 1 (
    echo Installing Pillow for QR code display...
    C:\Python314\python.exe -m pip install pillow
    echo.
)

echo Starting...
echo.

C:\Python314\python.exe scripts\publish_gui_v3_fixed.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Error occurred!
    echo ============================================================
    echo.
    echo Possible reasons:
    echo 1. Cookie expired - need to re-login
    echo 2. Missing dependencies
    echo 3. Network connection issue
    echo.
    echo Solutions:
    echo 1. Run fix_cookie.bat to re-login
    echo 2. Run: pip install xhs python-dotenv pillow
    echo 3. Check network connection
    echo.
    pause
)
