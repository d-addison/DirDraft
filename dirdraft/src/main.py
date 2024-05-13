import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QImage, QPixmap
from gui.main_window import MainWindow
from utils.logger import setup_logger

def main(directory):
   # Set up the base logger configuration
   file_handler, console_handler = setup_logger()
   logger = logging.getLogger()  # Get the root logger
   logger.setLevel(logging.INFO)

   # Check if handlers are already added to the root logger
   if not logger.handlers:
      if not logger.handlers:
         # Create a formatter with the file path
         formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
         file_handler.setFormatter(formatter)
         console_handler.setFormatter(formatter)

         logger.addHandler(file_handler)
         logger.addHandler(console_handler)

   app = QApplication([])
   
   icon_path = "src/gui/icons/app_icon.png"
   pixmap = QPixmap(icon_path)
   app_icon = QIcon(pixmap)
   app.setWindowIcon(app_icon)
   
   main_window = MainWindow()
   main_window.show()
   sys.exit(app.exec_())

if __name__ == "__main__":
   main("")
