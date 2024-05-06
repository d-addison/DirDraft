import sys
from PyQt5.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QStackedWidget, QToolButton, QAction
import logging
from gui.folder_structure_page import FolderStructurePage
from gui.template_design_page import TemplateDesignPage
from gui.main_menu_page import MainMenuPage
from utils.styles import FOCUSED_ACTION_STYLE, UNFOCUSED_ACTION_STYLE

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      
      # Set up the logger
      logging.basicConfig(filename="DirDraft.log", level=logging.INFO)
      self.logger = logging.getLogger(__name__)

      # Set up the main window
      self.setWindowTitle("DirDraft")
      self.setGeometry(100, 100, 800, 600)

      # Create a central widget and layout
      central_widget = QWidget(self)
      self.setCentralWidget(central_widget)
      layout = QVBoxLayout(central_widget)
      
      # Create a nav bar
      self.navbar = QToolBar("Navigation")
      self.addToolBar(self.navbar)

      # Create navigation bar actions
      self.action_main_menu = QAction("Main Menu", self)
      self.action_folder_structure = QAction("Folder Structure", self)
      self.action_template_design = QAction("Template Design", self)

      # Create tool buttons for the actions
      self.tool_button_main_menu = QToolButton(self)
      self.tool_button_main_menu.setDefaultAction(self.action_main_menu)
      self.navbar.addWidget(self.tool_button_main_menu)

      self.tool_button_folder_structure = QToolButton(self)
      self.tool_button_folder_structure.setDefaultAction(self.action_folder_structure)
      self.navbar.addWidget(self.tool_button_folder_structure)

      self.tool_button_template_design = QToolButton(self)
      self.tool_button_template_design.setDefaultAction(self.action_template_design)
      self.navbar.addWidget(self.tool_button_template_design)

      # Store the tool buttons and their styles
      self.action_styles = {
         self.tool_button_main_menu: FOCUSED_ACTION_STYLE,
         self.tool_button_folder_structure: UNFOCUSED_ACTION_STYLE,
         self.tool_button_template_design: UNFOCUSED_ACTION_STYLE
      }

      # Set initial styles for the tool buttons
      for tool_button, style in self.action_styles.items():
         tool_button.setStyleSheet(style)
         
      self.action_main_menu.triggered.connect(self.update_action_styles)
      self.action_folder_structure.triggered.connect(self.update_action_styles)
      self.action_template_design.triggered.connect(self.update_action_styles)

      # Connect navigation bar actions to slots
      self.action_main_menu.triggered.connect(self.show_main_menu)
      self.action_folder_structure.triggered.connect(self.show_folder_structure)
      self.action_template_design.triggered.connect(self.show_template_design)
      
      # Create a stacked widget to hold the main menu, folder structure, and template design pages
      self.stacked_widget = QStackedWidget()
      layout.addWidget(self.stacked_widget)

      # Create instances of the main menu, folder structure, and template design pages
      self.main_menu_widget = MainMenuPage(self)
      self.folder_structure_page = FolderStructurePage(self)
      self.template_design_page = TemplateDesignPage(self)

      # Add the pages to the stacked widget
      self.stacked_widget.addWidget(self.main_menu_widget)
      self.stacked_widget.addWidget(self.folder_structure_page)
      self.stacked_widget.addWidget(self.template_design_page)

   def show_main_menu(self):
      # Show the main menu widget
      self.logger.info("Displaying main menu page...")
      self.stacked_widget.setCurrentWidget(self.main_menu_widget)
      self.update_action_styles()
      

   def show_folder_structure(self):
      # Show the folder structure widget
      self.logger.info("Displaying folder structure page...")
      self.stacked_widget.setCurrentWidget(self.folder_structure_page)
      self.update_action_styles()

   def show_template_design(self):
      # Show the template design widget
      self.logger.info("Displaying template design page...")
      self.stacked_widget.setCurrentWidget(self.template_design_page)
      self.update_action_styles()
      
   def update_action_styles(self):
      action = self.sender()
      tool_button = None

      if action == self.action_main_menu:
         tool_button = self.tool_button_main_menu
      elif action == self.action_folder_structure:
         tool_button = self.tool_button_folder_structure
      elif action == self.action_template_design:
         tool_button = self.tool_button_template_design

      if tool_button:
         for btn, style in self.action_styles.items():
            if btn == tool_button:
                  btn.setStyleSheet(FOCUSED_ACTION_STYLE)
            else:
                  btn.setStyleSheet(UNFOCUSED_ACTION_STYLE)