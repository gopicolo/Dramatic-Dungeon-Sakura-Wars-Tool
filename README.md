This tool was created by **gopicolo** for extracting and reinserting text in the game *Dramatic Dungeon: Sakura Taisen - Kimi Aru ga Tame* for **Nintendo DS**.

# Dramatic Dungeon: Sakura Taisen – Extraction, Refinement and Repacking Tools

This repository contains custom Python scripts created to enable the **extraction**, **editing**, and **repacking** of text from the Nintendo DS game *Dramatic Dungeon: Sakura Taisen - Kimi Aru ga Tame*, with a focus on fan translation and localization efforts.

## Project Overview

### 🛠 Tools Included

- **`extract.py`**  
  Extracts text entries from the game’s overlay `.bin` files and outputs `.json` files with pointer data and encoded text.

- **`refine.py`**  
  Cleans and refines the extracted `.json` files by:
  - Removing invalid or unwanted entries
  - Replacing tag codes with readable characters
  - Re-indexing IDs
  - Fixing the `shared_with` field that tracks reused strings

- **`repack.py`**  
  Re-inserts the translated text back into the overlay `.bin` files, reusing duplicated strings when possible and updating pointers accordingly. It also updates the `y9.bin` file with the new file sizes.

## 📁 Folder Structure

The scripts expect the following folder structure:

```
input/           → Original overlay .bin files from the game
y9/              → Original y9.bin (used to update sizes)
output/          → Extracted JSON files (output from `extract.py`)
refined_json/    → Cleaned-up JSON files (output from `refine.py`)
translated/      → Translated JSON files ready for reinsertion
repacked/        → Final repacked overlay files (output from `repack.py`)
```

## 🔄 Workflow

1. **Extract text**
   ```bash
   python extract.py
   ```
   Outputs `.json` files to the `output/` folder.

2. **Refine extracted files**
   ```bash
   python refine.py
   ```
   Outputs cleaned files to the `refined_json/` folder.

3. **Translate**  
   Edit the files in `refined_json/` and save your translations in the `translated/` folder.

4. **Repack translated text**
   ```bash
   python repack.py
   ```
   Repacked `.bin` files and an updated `y9.bin` are saved in the `repacked/` folder.

## 📝 Notes

- The scripts automatically detect and reuse duplicate strings by using the `shared_with` field, minimizing file size and avoiding redundant entries.
- Certain overlays use a forced starting offset for string data to prevent overlap with other data sections. These are preconfigured in the scripts.
- You must provide the correct original files in the `input/` and `y9/` folders for the tools to work correctly.
- The game has a kind of automatic line break, but it is not perfect for adding line breaks in texts add {0A}

## 🈁 Shift-JIS Font Note

The game uses a Shift-JIS–based font. To add new characters (e.g. accented letters or symbols), you must edit the file:

LD937714.dat

This file contains the bitmap font used by the game. You can view and edit it using CrystalTile2 with the following settings:

Format: NDS 1bpp

Width: 12 pixels

Height: 12 pixels

Byte jump: 2

Be sure to map any new characters to unused Shift-JIS codes if you plan to expand the font.

## ℹ️ Additional Info

The main script files containing translatable text are:
- **`overlay_0001.bin`** to **`overlay_0034.bin`**

## 📦 Requirements

- Python 3.6 or higher
- No external dependencies (pure Python)

These tools were developed as part of a fan translation project. If you have any questions or feedback, feel free to reach out!
