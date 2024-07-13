# FATX360 User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Features](#features)
4. [Usage Guide](#usage-guide)
5. [Troubleshooting](#troubleshooting)
6. [FAQs](#faqs)

## Introduction

FATX360 is a Python application with a graphical user interface (GUI) that allows users to rename files and folders to be compatible with the FATX file system. This tool is particularly useful for users working with Xbox 360 systems or other platforms that use the FATX file system.

## Getting Started

To run FATX360:

1. Ensure you have Python 3.x installed on your system.
2. Open a command prompt or terminal.
3. Navigate to the directory containing `fatx360.py`.
4. Run the command: `python fatx360.py`

The application window should appear, ready for use.

## Features

- Select a directory to rename files and folders.
- Choose specific files or folders for renaming.
- "Select All" functionality to easily select or deselect all items.
- Option to rename only top-level folders.
- Option to rename subfolders with customizable depth.
- Option to rename files.
- Copy renamed items to a new directory, preserving the original files.
- Progress bar to track the renaming process.
- Cancel button to stop the operation mid-process.
- Error handling for various scenarios (permission issues, file not found, etc.).

## Usage Guide

1. **Select Directory**: 
   - Click the "Select Directory" button.
   - Choose the directory containing the files and folders you want to rename.

2. **Select Items to Rename**:
   - Use the listbox to select individual items.
   - Click the "Select All" button to select or deselect all items at once.

3. **Set Options**:
   - Check "Rename top-level folders" to rename only the main folders.
   - Check "Rename subfolders" to rename folders within the main folders.
     - Use the depth slider to specify how many levels of subfolders to rename.
   - Check "Rename files" to rename individual files.

4. **Start Renaming**:
   - Click the "Rename Selected" button.
   - Choose a destination folder for the renamed items when prompted.

5. **Monitor Progress**:
   - The progress bar will show the status of the renaming process.
   - The label next to the progress bar shows the number of processed items and total items.

6. **Cancel Operation** (if needed):
   - Click the "Cancel" button to stop the renaming process.

7. **Review Results**:
   - Once complete, a success message will appear.
   - Check the "RENAMED" folder in your chosen destination directory for the renamed items.

## Troubleshooting

- **Permission Error**: Ensure you have the necessary permissions to access the selected directory and create new files/folders.
- **Files Not Appearing**: Make sure the selected directory contains files or folders.
- **Renaming Not Starting**: Verify that you've selected at least one item to rename and set at least one renaming option.
- **Application Not Starting**: Confirm that Python is correctly installed and the script is in the correct directory.
- **Operation Cancelled**: If you cancel the operation, the interface will reset. You can start a new operation as needed.

## FAQs

1. **Q: What is FATX compatibility?**
   A: FATX compatibility ensures file and folder names are no longer than 42 characters and only use allowed characters (A-Z, a-z, 0-9, and some special characters).

2. **Q: Does this tool modify my original files?**
   A: No, the original files are preserved. Renamed items are copied to a new "RENAMED" folder.

3. **Q: Can I undo the renaming process?**
   A: The renaming process creates copies, so your original files remain unchanged. To "undo", simply use the original files.

4. **Q: What happens if I don't select any renaming options?**
   A: If no options are selected, all folders, subfolders, and files will be renamed to be FATX compatible.

5. **Q: How does the subfolder depth slider work?**
   A: The slider lets you choose how many levels of subfolders to rename. A value of 1 renames only immediate subfolders, while higher values rename deeper levels of subfolders.

For any additional questions or issues, please refer to the script comments or contact the developer.
