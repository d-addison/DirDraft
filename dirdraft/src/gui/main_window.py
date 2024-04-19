from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QToolBar, QAction
from PyQt5.QtGui import QIcon
from gui.folder_view import FolderView

import logging

"""
The main window of the DirDraft application.

Classes:
- MainWindow: Represents the main window of the application.

Methods:
- __init__(): Initializes the main window, sets up the UI elements, and connects signals to slots.
- on_main_window_clicked(): Slot for handling the 'Main Window' button click event.
- on_folder_view_clicked(): Slot for handling the 'Folder View' button click event.
- on_preview_dialogue_clicked(): Slot for handling the 'Preview Dialogue' button click event.
- on_new_triggered(): Slot for handling the 'New' action triggered event.
- on_open_triggered(): Slot for handling the 'Open' action triggered event.
"""

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      
      # Set the icon for the main window
      self.setWindowIcon(QIcon('./icons/app_icon.png'))
      
      # Set up logging
      logging.basicConfig(level=logging.INFO)
      self.logger = logging.getLogger(__name__)
      
      # Set up the main window
      self.setWindowTitle("DirDraft")
      self.setGeometry(100, 100, 800, 600)

      # Create a central widget and layout
      central_widget = QWidget(self)
      self.setCentralWidget(central_widget)
      layout = QVBoxLayout(central_widget)

      # Create a navigation view
      navbar = QToolBar("Navigation")
      self.addToolBar(navbar)
      
      # Create navigation bar actions
      self.action_new = navbar.addAction("New")
      self.action_open = navbar.addAction("Open")
      self.action_save = navbar.addAction("Save")
      
      # Add actions to the navigation bar
      navbar.addAction(self.action_new)
      navbar.addAction(self.action_open)
      navbar.addAction(self.action_save)
      
      # Connect navigation bar actions to slots
      self.action_new.triggered.connect(self.on_new_triggered)
      self.action_open.triggered.connect(self.on_open_triggered)
      self.action_save.triggered.connect(self.on_save_triggered)
      
      # Create a label for displaying the current path
      self.label_path = QLabel("Ahoy there matey! Welcome to DirDraft!")
      layout.addWidget(self.label_path)
      
      # Create buttons
      button_layout = QHBoxLayout()
      self.button_main_window = QPushButton("Main Window")
      self.button_folder_view = QPushButton("Folder View")
      self.button_preview_dialogue = QPushButton("Preview Dialogue")
      button_layout.addWidget(self.button_main_window)
      button_layout.addWidget(self.button_folder_view)
      button_layout.addWidget(self.button_preview_dialogue)
      layout.addLayout(button_layout)
      
      # Create a folder view
      self.folder_view = FolderView(self)
      layout.addWidget(self.folder_view)
      
      # Connect signals and slots
      self.button_main_window.clicked.connect(self.on_main_window_clicked)
      self.button_folder_view.clicked.connect(self.on_folder_view_clicked)
      self.button_preview_dialogue.clicked.connect(self.on_preview_dialogue_clicked)
      
   def on_main_window_clicked(self):
      self.logger.info("'Main Window' button clicked")
   
   def on_folder_view_clicked(self):
      self.logger.info("'Folder view' button clicked")

   def on_preview_dialogue_clicked(self):
      self.logger.info("'Preview dialogue' button clicked")
      
   def on_new_triggered(self):
      self.logger.info("New action triggered")
      
   def on_open_triggered(self):
      self.logger.info("Open action triggered")
      
   def on_save_triggered(self):
      self.logger.info("Save action triggered")