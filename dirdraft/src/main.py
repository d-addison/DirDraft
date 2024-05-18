import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QImage, QPixmap
from gui.main_window import MainWindow
from utils.logger import setup_logger

def main(directory):
   # Set up the base logger configuration
   logger = setup_logger()
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
