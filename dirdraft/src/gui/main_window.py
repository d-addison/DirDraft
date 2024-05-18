from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from gui.template_design_page import TemplateDesignPage

import logging

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.logger = logging.getLogger(__name__)
      # Set up the main window
      self.setWindowTitle("DirDraft")
      self.setGeometry(100, 100, 800, 600)

      # Create a central widget and layout
      central_widget = QWidget(self)
      self.setCentralWidget(central_widget)
      layout = QVBoxLayout(central_widget)

      # Create the "Get Started" button
      self.get_started_button = QPushButton("Get Started")
      layout.addWidget(self.get_started_button)

      # Connect the "Get Started" button to the show_template_design_page method
      self.get_started_button.clicked.connect(self.show_template_design_page)

      # Create a stacked widget to hold the main menu and template design page
      self.stacked_widget = QStackedWidget()
      layout.addWidget(self.stacked_widget)

      # Create an instance of TemplateDesignPage
      self.template_design_page = TemplateDesignPage(self)

      # Add the template design page to the stacked widget
      self.stacked_widget.addWidget(self.get_started_button)
      self.stacked_widget.addWidget(self.template_design_page)
      
      # Hide the TemplateDesignPage widget on boot
      #self.template_design_page.hide()
      self.stacked_widget.setCurrentWidget(self.get_started_button)

   def show_template_design_page(self):
      # Show the TemplateDesignPage
      # TODO: adjust logic here so that user can back out of template design page
      self.logger.info("Showing Template Design Page")
      self.stacked_widget.setCurrentWidget(self.template_design_page)
      self.template_design_page.prompt_directory_selection()