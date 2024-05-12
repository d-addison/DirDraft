from PyQt5.QtWidgets import QUndoCommand, QUndoStack, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QInputDialog, QLineEdit, QFileDialog, QMenu, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDrag
from core.node import Node
from core.template import Template
from core.observer import Observer
from core.commands import AddNodeCommand, RemoveNodeCommand, RenameNodeCommand, DeleteFileCommand, MoveNodeCommand
from gui.custom_tree_widget import CustomTreeWidget
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
      self.tree_widget = CustomTreeWidget(self)
      self.tree_widget.setColumnCount(1)
      self.tree_widget.setHeaderLabels(["Template Structure"])
      self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
      self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
      main_layout.addWidget(self.tree_widget)

      # Create a QTextEdit to display the execution summary
      self.summary_text = QTextEdit()
      self.summary_text.setReadOnly(True)
      main_layout.addWidget(self.summary_text)

      # Set up signals and slots
      self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
      self.tree_widget.itemExpanded.connect(self.load_children)

      # Initialization
      self.parent_dir = None
      self.template = None
      self.observer = Observer(self.tree_widget)
      self.undo_stack = QUndoStack()
      self.tree_widget.model().dataChanged.connect(self.track_changes)
      self.deleted_nodes = []
      
   def track_changes(self, top_left, bottom_right, roles):
      # Create a QUndoCommand to track the changes made to the QTreeWidget
      command = QUndoCommand()
      command.setText(f"Edit item at ({top_left.row()}, {top_left.column()})")
      self.undo_stack.push(command)

   def showEvent(self, event):
      # Get the parent directory when the page is shown
      if not self.parent_dir:
         self.parent_dir = QFileDialog.getExistingDirectory(self, "Select Parent Directory")
         if self.parent_dir:
               self.template = Template(None)
               self.template.build_from_directory(self.parent_dir)
               self.populate_tree_widget(self.template.root_node)

   def populate_tree_widget(self, parent_node, parent_item=None):
      for child_node in parent_node.children:
         child_item = self.find_or_create_item(child_node, parent_item)

         if child_node.type == 'folder':
               child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
               child_item.setExpanded(True)  # Set the folder item to be expanded by default
               self.populate_tree_widget(child_node, child_item)

   def find_or_create_item(self, node, parent_item):
      # Search for an existing item with the same node
      for i in range(self.tree_widget.topLevelItemCount() if parent_item is None else parent_item.childCount()):
            item = self.tree_widget.topLevelItem(i) if parent_item is None else parent_item.child(i)
            existing_node = item.data(0, Qt.UserRole)
            if existing_node == node:
               return item

      # If no existing item is found, create a new one
      child_item = QTreeWidgetItem([node.name, node.type])
      child_item.setData(0, Qt.UserRole, node)

      if parent_item:
            parent_item.addChild(child_item)
      else:
         self.tree_widget.addTopLevelItem(child_item)

      return child_item

   def on_item_double_clicked(self, item, column):
      # Handle double-clicking on an item
      node = item.data(0, Qt.UserRole)
      if node.type == 'file':
         # If the item is a file, print its name
         print(f"Double-clicked on file: {node.name}")
      else:
         # If the item is a directory, print its name
         print(f"Double-clicked on directory: {node.name}")

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
         self.add_directory(item, self.template.root_node if item is None else item.data(0, Qt.UserRole))
      elif action == add_file_action:
         self.add_file(item, self.template.root_node if item is None else item.data(0, Qt.UserRole))
      elif item and action == rename_action:
         # Handle renaming the item
         node = item.data(0, Qt.UserRole)
         self.rename_node(item, node)
      elif item and action == delete_action:
         # Handle deleting the item
         node = item.data(0, Qt.UserRole)
         self.delete_node(item, node)

   def add_directory(self, parent_item, parent_node):
      # Add a new directory to the template structure
      directory_name, ok = QInputDialog.getText(self, "Add Directory", "Enter directory name:")

      if ok and directory_name:
         new_node = Node(directory_name, os.path.join(parent_node.path, directory_name), 'folder')
         if parent_item:
               new_item = QTreeWidgetItem(parent_item, [directory_name, "folder"])
         else:
               new_item = QTreeWidgetItem(self.tree_widget, [directory_name, "folder"])
         new_item.setData(0, Qt.UserRole, new_node)
         new_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
         new_item.setExpanded(True)
         command = AddNodeCommand(self.template, parent_node, new_node, self.tree_widget)
         self.observer.push_command(command)
         command.redo()

   def add_file(self, parent_item, parent_node):
      # Add a new file to the template structure
      file_name, ok = QInputDialog.getText(self, "Add File", "Enter file name:")

      if ok and file_name:
         new_node = Node(file_name, os.path.join(parent_node.path, file_name), 'file')
         if parent_item:
               new_item = QTreeWidgetItem(parent_item, [file_name, "file"])
         else:
               new_item = QTreeWidgetItem(self.tree_widget, [file_name, "file"])
         new_item.setData(0, Qt.UserRole, new_node)
         command = AddNodeCommand(self.template, parent_node, new_node, self.tree_widget)
         self.observer.push_command(command)
         command.redo()

   def rename_node(self, item, node):
      # Rename the node
      new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=node.name)
      if ok and new_name:
         command = RenameNodeCommand(self.template, node, new_name, self.tree_widget)
         command.item = item  # Store the associated QTreeWidgetItem
         self.observer.push_command(command)
         command.redo()

   def delete_node(self, item, node):
      # Delete the node if the file already exists, otherwise remove from deleted_nodes queue
      if os.path.exists(node.path):
         self.deleted_nodes.append(node)
      parent = item.parent()
      if parent:
         parent.removeChild(item)
      else:
         self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))
      command = RemoveNodeCommand(self.template, node, self.tree_widget)
      self.observer.push_command(command)
      command.redo()
      
   def load_children(self, item):
      # Get the node associated with the expanded item
      node = item.data(0, Qt.UserRole)

      # Clear the existing children of the expanded item
      item.takeChildren()

      # Populate the children of the expanded item
      self.populate_tree_widget(node, item)

   def execute_template(self):
      # Clear the summary text
      self.summary_text.clear()
      
      # Delete the files in the deleted_nodes list
      for node in self.deleted_nodes:
         file_path = os.path.join(self.parent_dir, node.path)
         command = DeleteFileCommand(self, node, f"Delete file: {node.name}")
         self.observer.push_command(command)
         command.redo()
      
      # Clear the deleted_nodes list
      self.deleted_nodes.clear()

      # Create the directory structure based on the template
      self.create_directory_structure(self.template.root_node, self.parent_dir)

      # Clear the existing tree widget items
      self.tree_widget.clear()

      # Populate the tree widget with the updated directory structure
      self.template = Template(None)
      self.template.build_from_directory(self.parent_dir)
      self.populate_tree_widget(self.template.root_node)

   def create_directory_structure(self, parent_node, parent_dir):
      # Iterate over the children of the parent node
      for child_node in parent_node.children:
         child_path = os.path.join(parent_dir, child_node.name)
         old_child_path = None

         if child_node.type == 'folder':
               # If the child node is a directory
               if os.path.exists(child_path):
                  # If the directory already exists, get the old path
                  old_child_path = child_path
               else:
                  # If the directory doesn't exist, create it
                  os.makedirs(child_path, exist_ok=True)
                  self.summary_text.append(f"Created directory: {child_path}")

               # Recursively create the directory structure for the child node
               self.create_directory_structure(child_node, child_path)

               if old_child_path and old_child_path != child_path:
                  # If the directory was renamed or moved, update the summary
                  self.summary_text.append(f"Renamed/moved directory: {old_child_path} -> {child_path}")
                  child_node.move(child_path)
                  child_node.rename(os.path.basename(child_path))
         else:
               # If the child node is a file
               file_dir = os.path.dirname(child_path)
               if not os.path.exists(file_dir):
                  # If the parent directory doesn't exist, create it
                  os.makedirs(file_dir, exist_ok=True)
                  self.summary_text.append(f"Created directory: {file_dir}")

               # If the file doesn't exist, create it
               if not os.path.exists(child_path):
                  with open(child_path, 'w') as f:
                     pass
                  self.summary_text.append(f"Created file: {child_path}")

   def undo_action(self):
      self.observer.undo()

   def redo_action(self):
      self.observer.redo()

class TreeWidgetCommand(QUndoCommand):
   def __init__(self, tree_widget, top_left, bottom_right, roles):
      super().__init__()
      self.tree_widget = tree_widget
      self.top_left = top_left
      self.bottom_right = bottom_right
      self.roles = roles
      self.old_data = {}
      self.new_data = {}
      self.old_paths = {}
      self.new_paths = {}

      # Store the old data and paths
      for row in range(top_left.row(), bottom_right.row() + 1):
         for column in range(top_left.column(), bottom_right.column() + 1):
               index = self.tree_widget.model().index(row, column)
               self.old_data[(row, column)] = self.tree_widget.model().data(index, self.roles[0])
               item = self.tree_widget.itemFromIndex(index)
               if item:
                  parent_dir = self.tree_widget.parent().parent_dir
                  old_path = os.path.join(parent_dir, item.text(0))
                  self.old_paths[(row, column)] = old_path

   def undo(self):
      # Restore the old data and paths
      for (row, column), data in self.old_data.items():
         index = self.tree_widget.model().index(row, column)
         self.new_data[(row, column)] = self.tree_widget.model().data(index, self.roles[0])
         self.tree_widget.model().setData(index, data, self.roles[0])
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
         self.tree_widget.model().setData(index, data, self.roles[0])
         item = self.tree_widget.itemFromIndex(index)
         if item:
               parent_dir = self.tree_widget.parent().parent_dir
               new_path = os.path.join(parent_dir, item.text(0))
               if (row, column) in self.old_paths:
                  old_path = self.old_paths[(row, column)]
                  if old_path != new_path:
                     shutil.move(old_path, new_path)