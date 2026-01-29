@echo off
title XHS Cookie Fix Tool

echo ============================================================
echo XHS Cookie Fix Tool
echo ============================================================
echo.
echo This tool will help you re-login to XiaoHongShu
echo.
echo Steps:
echo 1. Browser will open XHS login page
echo 2. Scan QR code with XHS APP
echo 3. Cookie will be saved automatically
echo.
echo ============================================================
echo.

pause

echo.
echo Starting login process...
echo.

C:\Python314\python.exe scripts\login_xhs.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Login Failed!
    echo ============================================================
    echo.
    echo Possible reasons:
    echo 1. playwright not installed
    echo 2. Browser not installed
    echo 3. Network connection issue
    echo.
    echo Please run:
    echo pip install playwright python-dotenv
    echo playwright install chromium
    echo.
    pause
) else (
    echo.
    echo ============================================================
    echo Login Success!
    echo ============================================================
    echo.
    echo Cookie saved! You can now use the publish tool
    echo.
    echo Run: start_publish_fixed.bat
    echo.
    pause
)
