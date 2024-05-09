from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTreeWidgetItem, QSpinBox, QLabel
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
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
      self.directory_input.returnPressed.connect(self.update_folder_structure)
      input_layout.addWidget(self.directory_input)
      
      # Create a QLabel and QSpinBox for depth input
      depth_label = QLabel("Depth:")
      input_layout.addWidget(depth_label)
      self.depth_input = QSpinBox()
      self.depth_input.setMinimum(1)
      self.depth_input.setValue(1)
      input_layout.addWidget(self.depth_input)

      # Create a QPushButton to update the folder structure
      self.update_button = QPushButton("Update")
      input_layout.addWidget(self.update_button)
      self.update_button.clicked.connect(self.update_folder_structure)

      # Create a CustomTreeWidget to display the folder structure
      self.tree_widget = CustomTreeWidget(self)
      self.tree_widget.itemExpanded.connect(self.load_children)
      main_layout.addWidget(self.tree_widget)

   def update_folder_structure(self):
      # Clear the existing tree widget items
      self.tree_widget.clear()

      # Get the directory path from the input line edit
      directory_path = self.directory_input.text()
      
      # Get the depth from the depth input
      depth = self.depth_input.value()

      # Populate the tree widget with the folder structure
      self.populate_tree_widget(directory_path, self.tree_widget.invisibleRootItem(), depth=depth)

   def populate_tree_widget(self, directory_path, parent_item, depth=0):
      # Iterate over the contents of the directory
      for item in os.listdir(directory_path):
         try:
               item_path = os.path.join(directory_path, item)
               item_extension = os.path.splitext(item)[1]
               
               # Create a QTreeWidgetItem for the current item
               if os.path.isdir(item_path):
                  item_type = "folder"
               elif os.path.isfile(item_path):
                  item_type = "file"
               else:
                  item_type = "other"

               item_widget = QTreeWidgetItem(parent_item, [item, item_type, item_extension])

               # If the current item is a directory and depth is greater than 0, populate its children
               if item_type == "folder" and depth > 0:
                  self.populate_tree_widget(item_path, item_widget, depth=depth - 1)
         except PermissionError:
               # Create a disabled, red-colored QTreeWidgetItem for inaccessible paths
               item_widget = QTreeWidgetItem(parent_item, [item, "inaccessible"])
               item_widget.setFlags(item_widget.flags() & ~Qt.ItemIsEnabled)
               item_widget.setForeground(0, QBrush(QColor("red")))
         except:
               print("Error reading directory")

   def load_children(self, item):
      # Get the directory path of the expanded item
      directory_path = self.directory_input.text()
      if item.parent() is not None:
         parent_path = os.path.join(self.directory_input.text(), item.parent().text(0))
         directory_path = os.path.join(parent_path, item.text(0))
      else:
         directory_path = os.path.join(directory_path, item.text(0))

      # Check if the directory path is valid
      if os.path.isdir(directory_path):
         # Populate the children of the expanded item
         self.populate_tree_widget(directory_path, item, depth=float('inf'))
      else:
         print(f"Invalid directory path: {directory_path}")