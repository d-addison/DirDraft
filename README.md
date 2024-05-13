# DirDraft

## Overview
The Folder Structure Visualization and Restructuring Utility is a cross-platform tool designed to help users visualize and reorganize their folder structures efficiently. It provides a user-friendly interface that allows users to drag and drop folders, preview changes, and execute the restructuring operations in a single step.

## Goals
- Provide a clear and intuitive visualization of folder structures
- Enable users to easily reorganize folders using drag-and-drop functionality
- Offer a range of features to enhance the folder management experience
- Support cross-platform compatibility (Windows and Linux)

## Features
1. **Folder Structure Visualization**
   - Display folder structures in a tree-like view
   - Show folder and file details (e.g., name, size, modification date)
   - Provide customizable visualization options (color schemes, icon sets, themes)

2. **Drag-and-Drop Restructuring**
   - Allow users to drag and drop folders to reorganize the structure
   - Provide visual feedback during the drag-and-drop process
   - Update the underlying data structure in real-time

3. **Preview and Comparison**
   - Enable users to preview the changes before applying them
   - Provide a side-by-side comparison view of the original and modified structures
   - Highlight differences (moved, renamed, or deleted folders and files)

4. **Undo and Redo**
   - Implement undo and redo functionality to revert or reapply changes
   - Maintain a history of modifications made by the user

5. **Filtering and Searching**
   - Allow users to filter the view based on file types, sizes, or modification dates
   - Provide a search functionality to locate specific files or folders

6. **Disk Space Analysis**
   - Integrate disk space analysis features similar to WinDirStat
   - Display disk space consumption using visual representations (treemaps, pie charts)
   - Identify and manage large files or folders

7. **Batch Operations**
   - Support batch operations on multiple selected folders or files
   - Implement mass renaming, copying, or moving of selected items

8. **Integration with Cloud Storage**
   - Extend the utility to support popular cloud storage services
   - Enable users to visualize and restructure cloud folder structures

9. **Folder Templates and Presets**
   - Provide predefined folder structure templates for common use cases
   - Allow users to create and save custom folder structure presets

10. **Collaboration and Sharing**
    - Implement features for collaboration and sharing of folder structures
    - Allow exporting and importing of folder structure configurations
    - Provide options to generate shareable links or invite others

11. **Version Control and Backup**
    - Integrate version control capabilities to track changes over time
    - Automatically create backups before applying significant changes
    - Allow reverting to previous versions of the structure

12. **Cross-Platform Synchronization**
    - Enable synchronization of folder structures across multiple devices or platforms
    - Automatically detect and merge changes made on different devices

## Development Phases

### Phase 1: Setup and UI Design
- Set up the development environment with Python and necessary libraries
- Design the user interface using PyQt or PySide
- Implement the basic folder structure visualization

### Phase 2: Drag-and-Drop and Restructuring
- Implement drag-and-drop functionality for folder restructuring
- Update the underlying data structure based on user actions
- Provide visual feedback during the drag-and-drop process

### Phase 3: Preview, Comparison, and Undo/Redo
- Develop the preview and comparison feature
- Implement undo and redo functionality
- Enhance the user interface with these features

### Phase 4: Filtering, Searching, and Disk Space Analysis
- Integrate filtering options based on file types, sizes, or modification dates
- Implement search functionality to locate files or folders
- Add disk space analysis features and visual representations

### Phase 5: Batch Operations and Cloud Storage Integration
- Implement batch operations for multiple selected items
- Extend the utility to support popular cloud storage services
- Enable visualization and restructuring of cloud folder structures

### Phase 6: Templates, Presets, and Collaboration
- Develop predefined folder structure templates and preset functionality
- Implement collaboration and sharing features
- Allow exporting and importing of folder structure configurations

### Phase 7: AI Intergration
- Implement intelligent suggestions for folder organization based on file types and usage patterns
- Develop an AI-based naming convention assistant to suggest consistent and meaningful folder and file names
- Integrate machine learning algorithms to predict and recommend frequently accessed folders and files
- Utilize natural language processing (NLP) techniques to enable voice-based commands and search functionality
- Implement an AI-powered duplicate file detector to identify and suggest removal of duplicate files across folders
- Develop an intelligent file categorization system that automatically organizes files into relevant folders based on their content and metadata

### Phase 8: Version Control, Backup, and Synchronization
- Integrate version control capabilities to track changes over time
- Implement automatic backup functionality before applying significant changes
- Develop cross-platform synchronization features to keep folder structures consistent across devices

### Phase 9: Testing, Refinement, and Documentation
- Conduct thorough testing of all implemented features
- Gather user feedback and refine the utility based on insights
- Prepare user documentation and guides for the utility

### Phase 10: Packaging and Distribution
- Package the utility into executable formats for Windows and Linux
- Create installers or setup scripts for easy distribution
- Prepare release notes and distribution channels

## Current Development Phase
### [Phase 1](#Phase 1: Setup and UI Design)
- Development environment has been setup
- Working on making a mockup/wireframe using Balsamiq

## Diagrams
@startuml

class Node {
    -name: str
    -path: str
    -type: str ("file" or "folder")
    -is_generated: bool
    -children: list
    -tags: list
    +__init__(name, path, node_type, tags=None, is_generated=False)
    +add_child(child_node)
    +remove_child(child_node)
    +rename(new_name)
    +move(new_path)
    +serialize()
    +deserialize(serialized_data)
    +insert_tags(new_tags)
}

class Template {
    -root_node: Node
    -name: str
    +__init__(root_node, name)
    +build_from_directory(directory)
    +save_to_file(file_path)
    +load_from_file(file_path)
}

class TemplateDesignPage {
    -parent_dir: str
    -template: Template
    -observer: Observer
    -undo_stack: QUndoStack
    -deleted_nodes: list
    -unsaved_changes: bool
    +__init__(parent=None)
    +populate_tree_widget(parent_node, parent_item=None)
    +find_or_create_item(node, parent_item)
    +on_item_double_clicked(item, column)
    +show_context_menu(position)
    +add_directory(parent_item, parent_node)
    +add_file(parent_item, parent_node)
    +rename_node(item, node)
    +delete_node(item, node)
    +load_children(item)
    +load_templates()
    +create_new_template()
    +save_current_template()
    +execute_template()
    +create_directory_structure(parent_node, parent_dir)
    +set_unsaved_changes(unsaved_changes)
    +update_window_title()
    +undo_action()
    +redo_action()
    +show_tag_selection_dialog(existing_tags=None)
}

class Observer {
    -tree_widget: QTreeWidget
    -parent: TemplateDesignPage
    +__init__(tree_widget, parent)
    +push_command(command)
    +undo()
    +redo()
}

Node "1" *-- "0..*" Node
Template "1" *-- "1" Node
TemplateDesignPage "1" *-- "1" Template
TemplateDesignPage "1" *-- "1" Observer

@enduml

## Technologies and Tools
- Programming Language: Python
- GUI Framework: PyQt or PySide
- File System Manipulation: Python's `os` and `shutil` modules
- Packaging Tools: PyInstaller or cx_Freeze
- Version Control: Git
- Documentation: Markdown, Sphinx, or ReadTheDocs
- Wireframes: Balsamiq

## Contribution Guidelines
- Fork the repository and create a new branch for each feature or bug fix
- Follow the coding style and conventions used in the project
- Write clear and concise commit messages
- Submit pull requests with detailed descriptions of the changes made
- Participate in code reviews and address feedback constructively

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any questions, suggestions, or collaborations, please contact the project maintainer at [daa.addison@gmail.com](mailto:daa.addison@gmail.com).
