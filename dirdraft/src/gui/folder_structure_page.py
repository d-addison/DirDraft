from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTreeWidgetItem
from gui.custom_tree_widget import CustomTreeWidget
import os

class FolderStructurePage(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)

      # Set up the layout
      main_layout = QVBoxLayout()
      self.setLayout(main_layout)

      # Create a horizontal layout for the directory input and button
      input_layout = QHBoxLayout()
      main_layout.addLayout(input_layout)

      # Create a QLineEdit for directory input
      self.directory_input = QLineEdit()
      input_layout.addWidget(self.directory_input)

      # Create a QPushButton to update the folder structure
      self.update_button = QPushButton("Update")
      input_layout.addWidget(self.update_button)
      self.update_button.clicked.connect(self.update_folder_structure)

      # Create a CustomTreeWidget to display the folder structure
      self.tree_widget = CustomTreeWidget(self)
      main_layout.addWidget(self.tree_widget)

   def update_folder_structure(self):
      # Clear the existing tree widget items
      self.tree_widget.clear()

      # Get the directory path from the input line edit
      directory_path = self.directory_input.text()

      # Populate the tree widget with the folder structure
      self.populate_tree_widget(directory_path, self.tree_widget.invisibleRootItem())

   def populate_tree_widget(self, directory_path, parent_item):
      # Iterate over the contents of the directory
      for item in os.listdir(directory_path):
         item_path = os.path.join(directory_path, item)

         # Create a QTreeWidgetItem for the current item
         item_widget = QTreeWidgetItem(parent_item, [item])

         # If the current item is a directory, recursively populate its children
         if os.path.isdir(item_path):
               self.populate_tree_widget(item_path, item_widget)