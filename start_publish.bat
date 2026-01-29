@echo off
chcp 65001 >nul
title XHS Batch Publish GUI V3.0

echo Starting XHS Batch Publish GUI V3.0...
echo.

C:\Python314\python.exe D:\20260127XHS\Auto-Redbook-Skills-main\scripts\publish_gui_v3.py

if errorlevel 1 (
    echo.
    echo Error occurred!
    pause
)
