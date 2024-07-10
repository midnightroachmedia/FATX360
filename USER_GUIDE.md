# FATX360 User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [FAQs](#faqs)

## Introduction

FATX360 is a Python application with a graphical user interface (GUI) that allows users to rename files and folders to be compatible with the FATX file system. This tool is particularly useful for users working with Xbox systems or other platforms that use the FATX file system.

## Installation

1. Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. Save the `fatx360.py` script to your local machine.
3. No additional libraries are required as the application uses Python's standard libraries.

## Getting Started

To run the FATX360:

1. Open a command prompt or terminal.
2. Navigate to the directory containing `fatx360.py`.
3. Run the command: `python fatx360.py`

The application window should appear, ready for use.

## Features

- Select a directory to rename files and folders.
- Choose specific files or folders for renaming.
- "Select All" functionality to easily select or deselect all items.
- Option to rename folders only without affecting their contents.
- Rename items to be FATX compatible (42 character limit, restricted character set).
- Copy renamed items to a new directory, preserving the original files.
- Progress bar to track the renaming process.
- Error handling for various scenarios (permission issues, file not found, etc.).

## Usage Guide

1. **Select Directory**: 
   - Click the "Select Directory" button.
   - Choose the directory containing the files and folders you want to rename.

2. **Select Items to Rename**:
   - Use the listbox to select individual items.
   - Click the "Select All" button to select or deselect all items at once.

3. **Set Options**:
   - Check "Rename folders only" if you want to rename only folders without affecting their contents.

4. **Start Renaming**:
   - Click the "Rename Selected" button.
   - Choose a destination folder for the renamed items when prompted.

5. **Monitor Progress**:
   - The progress bar will show the status of the renaming process.

6. **Review Results**:
   - Once complete, a success message will appear.
   - Check the "RENAMED" folder in your chosen destination directory for the renamed items.

## Troubleshooting

- **Permission Error**: Ensure you have the necessary permissions to access the selected directory and create new files/folders.
- **Files Not Appearing**: Make sure the selected directory contains files or folders.
- **Renaming Not Starting**: Verify that you've selected at least one item to rename.
- **Application Not Starting**: Confirm that Python is correctly installed and the script is in the correct directory.

## FAQs

1. **Q: What is FATX compatibility?**
   A: FATX compatibility ensures file and folder names are no longer than 42 characters and only use allowed characters (A-Z, a-z, 0-9, and some special characters).

2. **Q: Does this tool modify my original files?**
   A: No, the original files are preserved. Renamed items are copied to a new "RENAMED" folder.

3. **Q: Can I undo the renaming process?**
   A: The renaming process creates copies, so your original files remain unchanged. To "undo", simply use the original files.

4. **Q: Why can't I select a file or folder?**
   A: Ensure you have permission to access the file/folder. Also, check if the "Rename folders only" option is selected when trying to select files.

5. **Q: The application is slow with many files. What can I do?**
   A: For large directories, consider renaming in smaller batches by selecting fewer items at a time.

For any additional questions or issues, please refer to the script comments or contact the developer.
