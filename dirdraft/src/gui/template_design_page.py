import os
import shutil
import logging

from PyQt5.QtWidgets import QCheckBox, QListWidget, QListWidgetItem, QAbstractItemView, QDialogButtonBox, QDialog, QMessageBox, QUndoCommand, QUndoStack, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QInputDialog, QLineEdit, QFileDialog, QMenu, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDrag, QColor

from core.node import Node
from core.template import Template
from gui.command_manager import CommandManager
from gui.ui_commands import AddNodeCommand, RemoveNodeCommand, RenameNodeCommand, DeleteFileCommand, MoveNodeCommand
from gui.custom_tree_widget import CustomTreeWidget, CustomTreeWidgetItem
from utils.template_utils import TemplateManager
from utils.styles import FOLDER_STYLE, FILE_STYLE, GENERATED_STYLE, TAG_STYLES

PREDEFINED_TAGS = [
   "image", "text", "video", "audio", "document", "code",
   "starred", "important", "draft", "final", "backup",
   "large_file", "small_file", "generated", "user_created"
]
class TemplateDesignPage(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)
      
      self.logger = logging.getLogger(__name__)
      # Set up the layout
      main_layout = QVBoxLayout()
      self.setLayout(main_layout)

      # Create a horizontal layout for the buttons
      button_layout = QHBoxLayout()
      main_layout.addLayout(button_layout)
      #self.setWindowTitle("Template Structure Page")

      # Create buttons
      self.execute_button = QPushButton("Execute")
      self.undo_button = QPushButton("Undo")
      self.redo_button = QPushButton("Redo")
      self.new_template_button = QPushButton("New Template")
      self.load_template_button = QPushButton("Load Template")
      self.save_template_button = QPushButton("Save Template")
      self.stylized_checkbox = QCheckBox("Stylized")

      # Add buttons to the button layout
      button_layout.addWidget(self.execute_button)
      button_layout.addWidget(self.undo_button)
      button_layout.addWidget(self.redo_button)
      button_layout.addWidget(self.new_template_button)
      button_layout.addWidget(self.load_template_button)
      button_layout.addWidget(self.save_template_button)
      button_layout.addWidget(self.stylized_checkbox)

      # Create a QTreeWidget to display the template structure
      self.tree_widget = CustomTreeWidget(self)
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
      self.new_template_button.clicked.connect(self.create_new_template)
      self.load_template_button.clicked.connect(self.load_templates)
      self.save_template_button.clicked.connect(self.save_current_template)
      self.execute_button.clicked.connect(self.execute_template)
      self.undo_button.clicked.connect(self.undo_action)
      self.redo_button.clicked.connect(self.redo_action)
      self.stylized_checkbox.stateChanged.connect(self.toggle_display_mode)

      # Initialization
      self.parent_dir = None
      self.template = None
      self.observer = CommandManager(self.tree_widget, self)
      self.template_manager = TemplateManager()
      self.current_template_index = None
      self.undo_stack = QUndoStack()
      self.tree_widget.model().dataChanged.connect(self.track_changes)
      self.deleted_nodes = []
      self.unsaved_changes = False
      self.stylized_checkbox.setChecked(False)
      
   def track_changes(self, top_left, bottom_right, roles):
      # Create a QUndoCommand to track the changes made to the QTreeWidget
      command = QUndoCommand()
      command.setText(f"Edit item at ({top_left.row()}, {top_left.column()})")
      self.undo_stack.push(command)

   def prompt_directory_selection(self):
      # Prompt the user to select a directory
      self.parent_dir = QFileDialog.getExistingDirectory(self, "Select Parent Directory")

      if self.parent_dir:
         # Check if there are any existing templates
         templates_dir = os.path.join(self.parent_dir, "templates")
         if os.path.exists(templates_dir):
               json_files = [f for f in os.listdir(templates_dir) if f.endswith(".json")]
               if json_files:
                  # If there are existing templates, prompt the user to load one or create a new one
                  message_box = QMessageBox(self)
                  message_box.setWindowTitle("Template Selection")
                  message_box.setText("What would you like to do?")
                  load_button = message_box.addButton("Load Existing Template", QMessageBox.ActionRole)
                  new_button = message_box.addButton("Create New Template", QMessageBox.ActionRole)
                  message_box.exec_()

                  if message_box.clickedButton() == load_button:
                     self.load_templates()
                  elif message_box.clickedButton() == new_button:
                     self.create_new_template()
               else:
                  # If there are no existing templates, prompt the user to create a new one
                  self.create_new_template()
         else:
               # If the templates directory doesn't exist, create it and prompt the user to create a new template
               os.makedirs(templates_dir, exist_ok=True)
               self.create_new_template()
               
   def create_new_template(self):
      template_name, ok = QInputDialog.getText(self, "New Template", "Enter template name:")
      if ok and template_name:
         # Create a new template with a root node
         root_node = Node("Root", "", "folder", tags=["folder", "generated"])
         new_template = Template(root_node, template_name)

         self.template_manager.add_template(new_template)
         self.current_template_index = len(self.template_manager.templates) - 1
         self.template = self.template_manager.get_template(self.current_template_index)
         
         # Push the AddNodeCommand for the root node
         add_root_node_command = AddNodeCommand(new_template, None, root_node, self.tree_widget)
         self.observer.push_command(add_root_node_command)
         
         self.tree_widget.clear()
         self.tree_widget.populate_tree_widget(self.template.root_node)

         # Update the header label with the template name
         #self.tree_widget.setWindowTitle([f"Template Structure: {template_name}"])
         # TODO: Have window title displayed somewhere else

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
         if isinstance(item, CustomTreeWidgetItem) and item.node == node:
            return item

      # If no existing item is found, create a new one
      child_item = self.tree_widget.create_item(node, parent_item)

      return child_item
      
   def toggle_display_mode(self):
      self.tree_widget.set_styling_mode(self.stylized_checkbox.isChecked())
      self.tree_widget.clear()
      self.tree_widget.populate_tree_widget(self.template.root_node)

   def on_item_double_clicked(self, item, column):
      # Handle double-clicking on an item
      node = item.data(0, Qt.UserRole)
      print(node)

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
      while True:
         # Add a new directory to the template structure
         directory_name, ok = QInputDialog.getText(self, "Add Directory", "Enter directory name:")

         if not ok:
               return  # User canceled the input dialog

         # Check if a directory with the same name already exists as a child of the parent node
         existing_child = next((child for child in parent_node.children if child.type == 'folder' and child.name == directory_name), None)
         if existing_child:
               QMessageBox.warning(self, "Duplicate Name", f"A directory with the name '{directory_name}' already exists.")
         else:
               new_node = Node(directory_name, os.path.join(parent_node.path, directory_name), 'folder', tags=['folder', 'generated'])
               selected_tags = self.show_tag_selection_dialog()
               if selected_tags is not None:
                  new_node.tags.extend(selected_tags)
               else:
                  return

               # Create a new QTreeWidgetItem using the find_or_create_item method
               new_item = self.find_or_create_item(new_node, parent_item)
               new_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
               new_item.setExpanded(True)

               command = AddNodeCommand(self.template, parent_node, new_node, self.tree_widget)
               self.observer.push_command(command)
               break  # Exit the loop if the name is valid

   def add_file(self, parent_item, parent_node):
      while True:
         # Add a new file to the template structure
         file_name, ok = QInputDialog.getText(self, "Add File", "Enter file name:")

         if not ok:
               return  # User canceled the input dialog

         # Check if a file with the same name already exists as a child of the parent node
         existing_child = next((child for child in parent_node.children if child.type == 'file' and child.name == file_name), None)
         if existing_child:
               QMessageBox.warning(self, "Duplicate Name", f"A file with the name '{file_name}' already exists.")
         else:
               new_node = Node(file_name, os.path.join(parent_node.path, file_name), 'file', tags=['file', 'generated'])
               selected_tags = self.show_tag_selection_dialog()
               if selected_tags is not None:
                  new_node.tags.extend(selected_tags)
               else:
                  return

               # Create a new QTreeWidgetItem using the find_or_create_item method
               new_item = self.find_or_create_item(new_node, parent_item)

               command = AddNodeCommand(self.template, parent_node, new_node, self.tree_widget)
               self.observer.push_command(command)
               break  # Exit the loop if the name is valid
         
   def rename_node(self, item, node):
      # Rename the node
      new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=node.name)
      if ok and new_name:
         selected_tags = self.show_tag_selection_dialog(existing_tags=node.tags)
         if selected_tags is not None:
               node.insert_tags(['renamed'])
               node.insert_tags(selected_tags)
               node.rename(new_name)

               # Update the QTreeWidgetItem with the new node data
               parent_item = item.parent()
               self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))
               new_item = self.find_or_create_item(node, parent_item)

               command = RenameNodeCommand(self.template, node, new_name, self.tree_widget)
               command.item = new_item  # Store the new QTreeWidgetItem
               self.observer.push_command(command)

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
      
   def load_children(self, item):
      # Get the node associated with the expanded item
      node = item.data(0, Qt.UserRole)

      # Clear the existing children of the expanded item
      item.takeChildren()

      # Populate the children of the expanded item
      self.tree_widget.populate_tree_widget(node, item)
      
   def load_templates(self):
      templates_dir = os.path.join(self.parent_dir, "templates")
      if os.path.exists(templates_dir):
         json_files = [f for f in os.listdir(templates_dir) if f.endswith(".json")]
         file_dialog = QFileDialog(self)
         file_dialog.setNameFilter("JSON Files (*.json)")
         file_dialog.setFileMode(QFileDialog.ExistingFile)
         file_dialog.setDirectory(templates_dir)
         if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                  file_path = selected_files[0]
                  try:
                     template = self.template_manager.load_template(file_path)
                     self.template_manager.add_template(template)
                     self.current_template_index = len(self.template_manager.templates) - 1
                     self.template = self.template_manager.get_template(self.current_template_index)
                     self.tree_widget.clear()
                     self.tree_widget.populate_tree_widget(self.template.root_node)
                     
                     self.logger.info(f"Loaded template from {file_path}")

                     # Update the header label with the template name
                     #self.tree_widget.setHeaderLabels([f"Template Structure: {self.template.name}"])
                  except Exception as e:
                     self.logger.error(f"Error loading template from {file_path}: {e}")
      else:
         self.logger.error(f"Templates directory not found: {templates_dir}")

   def save_current_template(self):
      if self.current_template_index is not None:
         template = self.template_manager.templates[self.current_template_index]
         template.name = self.template.name
         template.root_node = self.template.root_node

         templates_dir = os.path.join(self.parent_dir, "templates")
         file_path = os.path.join(templates_dir, f"{template.name}.json")

         if os.path.exists(file_path):
               overwrite_confirmation = QMessageBox.question(self, "Overwrite Template", f"A template with the name '{template.name}' already exists. Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No)
               if overwrite_confirmation == QMessageBox.No:
                  return
               
         self.template_manager.save_template(template, file_path)
         self.set_unsaved_changes(False)
         #self.update_window_title()
      else:
         self.logger.error("No template loaded")
         
   def rename_template(self):
      if self.current_template_index is not None:
         current_template = self.template_manager.templates[self.current_template_index]
         new_name, ok = QInputDialog.getText(self, "Rename Template", "Enter new template name:", text=current_template.name)
         if ok and new_name:
               current_template.name = new_name
               self.template.name = new_name
               #self.tree_widget.setHeaderLabels([f"Template Structure: {new_name}"])
               self.set_unsaved_changes(True)
               #self.update_window_title()
      else:
         self.logger.error("No template loaded")

   def execute_template(self):
      # Save the current template before executing
      # self.save_current_template()
      
      # Clear the summary text
      self.summary_text.clear()
      
      # Delete the files in the deleted_nodes list
      for node in self.deleted_nodes:
         file_path = os.path.join(self.parent_dir, node.path)
         command = DeleteFileCommand(self, node, f"Delete file: {node.name}")
         self.observer.push_command(command)
      
      # Clear the deleted_nodes list
      self.deleted_nodes.clear()

      # Create the directory structure based on the template
      self.create_directory_structure(self.template.root_node, self.parent_dir)

      # Clear the existing tree widget items
      self.tree_widget.clear()

      # Populate the tree widget with the updated directory structure
      self.template = Template(None)
      self.template.build_from_directory(self.parent_dir)
      self.tree_widget.populate_tree_widget(self.template.root_node)

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
                  
   def set_unsaved_changes(self, unsaved_changes):
      self.unsaved_changes = unsaved_changes
      
   def update_window_title(self):
      title = "Template Structure: " + self.template.name
      if self.unsaved_changes:
         title += " *"  # Add an asterisk to indicate unsaved changes
      self.tree_widget.setHeaderLabels([title])

   # Undo the action, push QUndoCommand to the undo stack
   def undo_action(self):
      if self.undo_stack.canUndo():
         self.undo_stack.undo()
         self.observer.undo()
         self.undo_button.setEnabled(self.undo_stack.canUndo())
         self.redo_button.setEnabled(self.undo_stack.canRedo())

   def redo_action(self):
      if self.undo_stack.canRedo():
         self.undo_stack.redo()
         self.observer.redo()
         self.undo_button.setEnabled(self.undo_stack.canUndo())
         self.redo_button.setEnabled(self.undo_stack.canRedo())
      
   def show_tag_selection_dialog(self, existing_tags=None):
      dialog = QDialog(self)
      dialog.setWindowTitle("Select Tags")
      dialog_layout = QVBoxLayout(dialog)

      tag_list = QListWidget()
      tag_list.setSelectionMode(QAbstractItemView.MultiSelection)

      for tag in PREDEFINED_TAGS:
         item = QListWidgetItem(tag)
         item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
         if existing_tags is not None and tag in existing_tags:
            item.setCheckState(Qt.Checked)
         else:
            item.setCheckState(Qt.Unchecked)
         tag_list.addItem(item)

      dialog_layout.addWidget(tag_list)

      button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      button_box.accepted.connect(dialog.accept)
      button_box.rejected.connect(dialog.reject)
      dialog_layout.addWidget(button_box)

      if dialog.exec_() == QDialog.Accepted:
         selected_tags = [item.text() for item in tag_list.findItems('', Qt.MatchContains) if item.checkState() == Qt.Checked]
         return selected_tags
      else:
         return None
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