from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QInputDialog, QLineEdit, QFileDialog, QMenu, QPushButton, QHBoxLayout, QTextEdit, QUndoStack, QUndoCommand
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import os
import shutil

class TemplateDesignPage(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)

      # Set up the layout
      main_layout = QVBoxLayout()
      self.setLayout(main_layout)
      
      # Create a horizontal layout for the execute button
      button_layout = QHBoxLayout()
      main_layout.addLayout(button_layout)
      
      # Create an execute button
      self.execute_button = QPushButton("Execute")
      self.execute_button.clicked.connect(self.execute_template)
      button_layout.addWidget(self.execute_button)
      
      # Create undo and redo buttons
      self.undo_button = QPushButton("Undo")
      self.undo_button.clicked.connect(self.undo_action)
      button_layout.addWidget(self.undo_button)
      
      self.redo_button = QPushButton("Redo")
      self.redo_button.clicked.connect(self.redo_action)
      button_layout.addWidget(self.redo_button)

      # Create a QTreeWidget to display the template structure
      self.tree_widget = QTreeWidget()
      self.tree_widget.setColumnCount(1)
      self.tree_widget.setHeaderLabels(["Template Structure"])
      self.tree_widget.setDragEnabled(True)
      self.tree_widget.setDragDropMode(QTreeWidget.InternalMove)
      self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
      self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
      self.tree_widget.customContextMenuRequested.connect(self.on_item_right_click)
      main_layout.addWidget(self.tree_widget)
      
      # Create a QTextEdit to display the execution summary
      self.summary_text = QTextEdit()
      self.summary_text.setReadOnly(True)
      main_layout.addWidget(self.summary_text)

      # Set up signals and slots
      self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
      self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
      
      # Initialization
      self.parent_dir = None
      self.undo_stack = QUndoStack()
      self.tree_widget.model().dataChanged.connect(self.track_changes)
      
   def track_changes(self, top_left, bottom_right, roles):
      # Create a command to track the changes made to the QTreeWidget
      command = TreeWidgetCommand(self.tree_widget, top_left, bottom_right, Qt.EditRole)
      self.undo_stack.push(command)

   def undo_action(self):
      self.undo_stack.undo()
      print("Undo")

   def redo_action(self):
      self.undo_stack.redo()
      print("Redo")
      
   def showEvent(self, event):
      # Get the parent directory when the page is shown
      if not self.parent_dir:
         self.parent_dir = QFileDialog.getExistingDirectory(self, "Select Parent Directory")
         if self.parent_dir:
               self.populate_tree_widget(self.parent_dir, self.tree_widget.invisibleRootItem())
         
   def populate_tree_widget(self, directory_path, parent_item):
      # Iterate over the contents of the directory
      for item in os.listdir(directory_path):
         item_path = os.path.join(directory_path, item)

         # Create a QTreeWidgetItem for the current item
         item_widget = QTreeWidgetItem(parent_item, [item])

         # If the current item is a directory, recursively populate its children
         if os.path.isdir(item_path):
            self.populate_tree_widget(item_path, item_widget)

         # Track changes for the new item
         command = TreeWidgetCommand(self.tree_widget, self.tree_widget.model().index(0, 0), self.tree_widget.model().index(0, 0), Qt.EditRole)
         self.undo_stack.push(command)
   
   # Handles right clicking on an item, with the option to rename or delete the item
   def on_item_right_click(self, position):
      # Get the item at the right-click position
      item = self.tree_widget.itemAt(position)

      if item:
         # Create a context menu
         menu = QMenu(self)

         # Add actions to the context menu
         rename_action = menu.addAction("Rename")
         delete_action = menu.addAction("Delete")
         add_subdirectory = menu.addAction("Add Subdirectory")

         # Show the context menu and get the selected action
         action = menu.exec_(self.tree_widget.mapToGlobal(position))

         if action == rename_action:
            # Handle renaming the item
            new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=item.text(0))
            if ok and new_name:
                  item.setText(0, new_name)

         elif action == delete_action:
            # Handle deleting the item
            parent = item.parent()
            if parent:
                  parent.removeChild(item)
            else:
                  self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))
                  
         elif action == add_subdirectory:
            # Handle adding a subdirectory
            new_name, ok = QInputDialog.getText(self, "Add Subdirectory", "Enter new name:")
            if ok and new_name:
                  new_item = QTreeWidgetItem(item)
                  new_item.setText(0, new_name)
                  new_item.setFlags(new_item.flags() | Qt.ItemIsEditable)

   def on_item_double_clicked(self, item, column):
      # Handle double-clicking on an item
      if item.childCount() == 0:
         # If the item is a file, print its name
         print(f"Double-clicked on file: {item.text(column)}")
      else:
         # If the item is a directory, print its name
         print(f"Double-clicked on directory: {item.text(column)}")

   def show_context_menu(self, position):
      # Get the item at the right-click position
      item = self.tree_widget.itemAt(position)

      menu = QMenu(self)
      add_directory_action = menu.addAction("Add Directory")
      add_file_action = menu.addAction("Add File")

      if item:
         # If an item is selected, add the "Rename" and "Delete" actions
         rename_action = menu.addAction("Rename")
         delete_action = menu.addAction("Delete")

      action = menu.exec_(self.tree_widget.mapToGlobal(position))

      if action == add_directory_action:
         self.add_directory(item)
      elif action == add_file_action:
         self.add_file(item)
      elif item and action == rename_action:
         # Handle renaming the item
         new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=item.text(0))
         if ok and new_name:
            item.setText(0, new_name)
      elif item and action == delete_action:
         # Handle deleting the item
         parent = item.parent()
         if parent:
            parent.removeChild(item)
         else:
            self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))
         self.tree_widget.update()

   def add_directory(self, parent_item=None):
      # Add a new directory to the template structure
      directory_name, ok = QInputDialog.getText(self, "Add Directory", "Enter directory name:")

      if ok and directory_name:
         new_item = QTreeWidgetItem([directory_name])
         if parent_item:
            parent_item.addChild(new_item)
         else:
            self.tree_widget.addTopLevelItem(new_item)

   def add_file(self, parent_item=None):
      # Add a new file to the template structure
      file_name, ok = QInputDialog.getText(self, "Add File", "Enter file name:")

      if ok and file_name:
         new_item = QTreeWidgetItem([file_name])
         if parent_item:
            parent_item.addChild(new_item)
         else:
            self.tree_widget.addTopLevelItem(new_item)

   def execute_template(self):
      if self.parent_dir:
         self.summary_text.clear()
         # Create the directory structure based on the template
         self.create_directory_structure(self.tree_widget.invisibleRootItem(), self.parent_dir)
         
         self.tree_widget.clear()
         self.populate_tree_widget(self.parent_dir, self.tree_widget.invisibleRootItem())

   def create_directory_structure(self, parent_item, parent_dir):
      # Iterate over the children of the parent item
      for i in range(parent_item.childCount()):
         child_item = parent_item.child(i)
         child_name = child_item.text(0)
         child_path = os.path.join(parent_dir, child_name)
         old_child_path = None

         if child_item.childCount() > 0:
            # If the child item is a directory
            if os.path.exists(child_path):
                  # If the directory already exists, get the old path
                  old_child_path = child_path
            else:
                  # If the directory doesn't exist, create it
                  os.makedirs(child_path, exist_ok=True)
                  self.summary_text.append(f"Created directory: {child_path}")

            self.create_directory_structure(child_item, child_path)

            if old_child_path:
                  # If the directory was moved or renamed, update the summary
                  self.summary_text.append(f"Moved/renamed directory: {old_child_path} -> {child_path}")
         else:
            # If the child item is a file
            file_dir = os.path.dirname(child_path)
            if not os.path.exists(file_dir):
                  # If the parent directory doesn't exist, create it
                  os.makedirs(file_dir, exist_ok=True)
                  self.summary_text.append(f"Created directory: {file_dir}")

            if os.path.exists(child_path):
                  # If the file already exists, get the old path
                  old_child_path = child_path
            else:
                  # If the file doesn't exist, create an empty file
                  open(child_path, 'a').close()
                  self.summary_text.append(f"Created file: {child_path}")

            if old_child_path and old_child_path != child_path:
                  # If the file was moved or renamed, update the summary
                  self.summary_text.append(f"Moved/renamed file: {old_child_path} -> {child_path}")
                  # Move or rename the existing file
                  shutil.move(old_child_path, child_path)

   def mousePressEvent(self, event):
      # Handle mouse press events for drag and drop
      if event.button() == Qt.LeftButton:
         item = self.tree_widget.currentItem()
         if item:
               drag = QDrag(self)
               mime_data = QMimeData()
               mime_data.setText(item.text(0))
               drag.setMimeData(mime_data)
               drag.exec_(Qt.MoveAction)

   def dropEvent(self, event):
      # Handle drop events for drag and drop
      if event.mimeData().hasText():
         item_text = event.mimeData().text()
         parent_item = self.tree_widget.itemAt(event.pos())
         if parent_item:
               new_item = QTreeWidgetItem(parent_item, [item_text])
               parent_item.addChild(new_item)
         else:
               new_item = QTreeWidgetItem(self.tree_widget, [item_text])
               self.tree_widget.addTopLevelItem(new_item)
         event.acceptProposedAction()
         
class TreeWidgetCommand(QUndoCommand):
   def __init__(self, tree_widget, top_left, bottom_right, role):
      super().__init__()
      self.tree_widget = tree_widget
      self.top_left = top_left
      self.bottom_right = bottom_right
      self.role = role
      self.old_data = {}
      self.new_data = {}
      self.old_paths = {}
      self.new_paths = {}

      # Store the old data and paths
      for row in range(top_left.row(), bottom_right.row() + 1):
         for column in range(top_left.column(), bottom_right.column() + 1):
               index = self.tree_widget.model().index(row, column)
               self.old_data[(row, column)] = self.tree_widget.model().data(index, self.role)
               item = self.tree_widget.itemFromIndex(index)
               if item:
                  parent_dir = self.tree_widget.parent().parent_dir
                  old_path = os.path.join(parent_dir, item.text(0))
                  self.old_paths[(row, column)] = old_path

   def undo(self):
      # Restore the old data and paths
      for (row, column), data in self.old_data.items():
         index = self.tree_widget.model().index(row, column)
         self.new_data[(row, column)] = self.tree_widget.model().data(index, self.role)
         self.tree_widget.model().setData(index, data, self.role)
         item = self.tree_widget.itemFromIndex(index)
         if item:
               parent_dir = self.tree_widget.parent().parent_dir
               new_path = os.path.join(parent_dir, item.text(0))
               self.new_paths[(row, column)] = new_path
               if (row, column) in self.old_paths:
                  old_path = self.old_paths[(row, column)]
                  if old_path != new_path:
                     shutil.move(new_path, old_path)

   def redo(self):
      # Restore the new data and paths
      for (row, column), data in self.new_data.items():
         index = self.tree_widget.model().index(row, column)
         self.tree_widget.model().setData(index, data, self.role)
         item = self.tree_widget.itemFromIndex(index)
         if item:
               parent_dir = self.tree_widget.parent().parent_dir
               new_path = os.path.join(parent_dir, item.text(0))
               if (row, column) in self.old_paths:
                  old_path = self.old_paths[(row, column)]
                  if old_path != new_path:
                     shutil.move(old_path, new_path)