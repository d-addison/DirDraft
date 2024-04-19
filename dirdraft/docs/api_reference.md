# DirDraft API Reference

## Main Window

- `MainWindow`: The main window of the DirDraft application.

## GUI Components

- `FolderView`: Displays the folder structure and allows interaction with files and folders.
- `PreviewDialog`: Shows a preview of the changes before applying them.

## Core Functionality

- `FolderStructure`: Represents the folder structure and provides methods to load and save the structure.
- `FileOperations`: Handles file operations such as moving, renaming, and deleting files.
- `AIAssistant`: Provides AI-based suggestions for folder structure and file naming.

## Utilities

- `Config`: Manages the configuration settings for the application.
- `Logger`: Sets up logging for the application.

## Example Usage

```python
from core.folder_structure import FolderStructure
from core.file_operations import FileOperations

# Load folder structure
structure = FolderStructure()
structure.load_structure("/path/to/folder")

# Perform file operations
file_ops = FileOperations()
file_ops.move_file("/path/to/source", "/path/to/destination")
file_ops.rename_file("/path/to/old_name", "/path/to/new_name")
```
