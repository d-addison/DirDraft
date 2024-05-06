from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt

class TemplateDesignPage(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)

      # Set up the layout
      layout = QVBoxLayout()
      self.setLayout(layout)

      # Create a QTreeWidget to display the template structure
      self.tree_widget = QTreeWidget()
      self.tree_widget.setColumnCount(1)
      self.tree_widget.setHeaderLabels(["Template Structure"])
      layout.addWidget(self.tree_widget)

      # Set up signals and slots
      self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
      self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)

   def on_item_double_clicked(self, item, column):
      # Handle double-clicking on an item
      if item.childCount() == 0:
         # If the item is a file, print its name
         print(f"Double-clicked on file: {item.text(column)}")
      else:
         # If the item is a directory, print its name
         print(f"Double-clicked on directory: {item.text(column)}")

   def show_context_menu(self, position):
      # Show a context menu when right-clicking on the tree widget
      menu = self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
      add_directory_action = menu.addAction("Add Directory")
      add_file_action = menu.addAction("Add File")

      action = menu.exec_(self.tree_widget.mapToGlobal(position))

      if action == add_directory_action:
         self.add_directory()
      elif action == add_file_action:
         self.add_file()

   def add_directory(self):
      # Add a new directory to the template structure
      parent_item = self.tree_widget.currentItem()
      directory_name, ok = QInputDialog.getText(self, "Add Directory", "Enter directory name:")

      if ok and directory_name:
         new_item = QTreeWidgetItem(parent_item, [directory_name])
         parent_item.addChild(new_item)

   def add_file(self):
      # Add a new file to the template structure
      parent_item = self.tree_widget.currentItem()
      file_name, ok = QInputDialog.getText(self, "Add File", "Enter file name:")

      if ok and file_name:
         new_item = QTreeWidgetItem(parent_item, [file_name])
         parent_item.addChild(new_item)