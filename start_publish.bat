@echo off
REM Auto-Redbook Skill V6.6 - Batch Publish Tool Launcher
REM Start the GUI tool for batch publishing Xiaohongshu notes

cd /d "%~dp0"
C:\Python314\python.exe scripts\publish_gui.py --notes-dir "%~dp0" --start-from 1 --wait-minutes 10
pause
