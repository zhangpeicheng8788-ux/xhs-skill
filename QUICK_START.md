# Quick Start Guide - XHS Batch Publish Tool (Fixed Version)

## Problem: Login Error

If you see this error when starting the tool:
```
{'code': -1, 'success': False}
{'code': -100, 'msg': 'No login info', 'success': False}
```

**Don't worry! Follow these 3 steps to fix it:**

---

## Step 1: Re-login (2 minutes)

**Double-click to run:**
```
fix_cookie.bat
```

**What will happen:**
1. Browser will automatically open XHS login page
2. Scan QR code with XiaoHongShu APP
3. Cookie will be saved automatically

---

## Step 2: Start the tool (10 seconds)

**Double-click to run:**
```
start_publish_fixed.bat
```

---

## Step 3: Publish notes (1 minute)

**In the GUI:**
1. Click "Browse" to select folder (e.g., `D:\jieyue_work`)
2. Click "Detect Notes" to scan all notes
3. Click "Start Publish" to begin batch publishing

**That's it!** ✨

---

## Supported Directory Structure

The tool will **automatically detect notes in all subdirectories**!

### Example 1: Flat Structure
```
D:\jieyue_work\
├── note_1\
│   ├── cover.png      ← Required
│   ├── card_1.png
│   └── card_2.png
├── note_2\
│   ├── cover.png
│   └── card_1.png
└── note_3\
    ├── cover.png
    └── card_1.png
```

### Example 2: Grouped Structure
```
D:\jieyue_work\
├── drivingschool_notes\
│   ├── note_01\
│   │   ├── cover.png
│   │   └── card_1.png
│   └── note_02\
│       ├── cover.png
│       └── card_1.png
└── spring_notes\
    └── note_01\
        ├── cover.png
        └── card_1.png
```

### Example 3: Nested Structure
```
D:\jieyue_work\
└── batch_1\
    └── group_a\
        └── sub_group\
            └── note_01\
                ├── cover.png
                └── card_1.png
```

**Any folder containing `cover.png` will be detected!**

---

## Key Features

### ✅ Smart Deduplication
- Automatically skip published notes
- Create `.published` marker file in note directory
- Save all publish history to `publish_records.json`

### ✅ Recursive Detection
- Automatically scan all subdirectories
- Support unlimited nesting levels (max 10 levels)
- Skip system folders and hidden folders

### ✅ Publish Records
- View all published notes
- Show publish time and links
- Statistics for today and total

### ✅ Real-time Logs
- Show detailed publish progress
- Record success and failure
- Friendly error messages

---

## Configuration

### Publish Interval
- **Recommended**: 20 minutes (avoid rate limiting)
- **Minimum**: 5 minutes
- **Maximum**: 120 minutes

### Start From
- Which note to start from
- Default: 1 (start from first note)

---

## Common Issues

### Q1: "Cookie expired" error?
**A**: Cookie expired, run `fix_cookie.bat` to re-login.

### Q2: No notes detected?
**A**: Make sure note directory contains `cover.png`, the tool will scan all subdirectories.

### Q3: How to view published notes?
**A**: Click "Publish Records" button in GUI.

### Q4: How to re-publish a note?
**A**: Delete `.published` file in note directory.

### Q5: Will the tool publish duplicates?
**A**: No, it will automatically skip published notes.

---

## Files

### Core Files
- `start_publish_fixed.bat` - Fixed version startup script (recommended)
- `fix_cookie.bat` - Quick re-login script
- `scripts/publish_gui_v3_fixed.py` - Fixed version publish tool

### Config Files
- `.env` - Cookie config file (auto-generated)
- `publish_records.json` - Publish records file (auto-generated)

### Documentation (Chinese)
- `快速修复指南.md` - Quick fix guide
- `错误修复报告.md` - Detailed technical documentation
- `修复完成总结.md` - Fix summary

---

## Need Help?

### Diagnostic Tool
```bash
# Test if Cookie is valid
python test_cookie_loading.py
```

**Expected output:**
```
OK User info retrieved
   Nickname: Your Nickname
```

### Reinstall Dependencies
```bash
pip install --upgrade xhs python-dotenv playwright
playwright install chromium
```

---

## Note Requirements

### Required Files
- `cover.png` - Cover image

### Optional Files
- `card_1.png`, `card_2.png`, ... - Content cards (max 8 cards)
- `metadata.json` - Note metadata

### metadata.json Format
```json
{
  "title": "Note Title",
  "subtitle": "Subtitle or Description",
  "theme": "Theme Tag"
}
```

If no `metadata.json`, the tool will use folder name as title.

---

## Get Started

**Ready? Follow these steps:**

1. ✅ Run `fix_cookie.bat` to login
2. ✅ Run `start_publish_fixed.bat` to start
3. ✅ Select path and publish in GUI

**Enjoy!** 🚀

---

**Fixed Date**: 2026-01-29  
**Version**: V3.0 Fixed  
**Status**: ✅ Ready to use
