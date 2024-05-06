from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyle
from PyQt5.QtGui import QFont, QBrush, QColor, QPalette, QPixmap
from utils.styles import FOLDER_STYLE, FILE_STYLE
import os

class CustomTreeWidget(QTreeWidget):
   def __init__(self, parent=None):
      super().__init__(parent)
      self.setColumnCount(1)
      self.setHeaderLabels(["Folder Structure"])

   def drawRow(self, painter, option, index):
      item = self.itemFromIndex(index)
      if item is None:
         return

      directory_path = self.parent().directory_input.text()
      item_path = os.path.join(directory_path, item.text(0))

      if os.path.isdir(item_path):
         # Set custom styling for folders
         font = QFont()
         # font.setBold(True)
         # font.setItalic(True)
         font.setStyleHint(QFont.Monospace)
         option.font = font
         option.palette.setColor(QPalette.Text, QColor(FOLDER_STYLE))
      # elif os.path.isfile(item_path):
      else:
         # Set custom styling for files
         font = QFont()
         # font.setItalic(True)
         font.setStyleHint(QFont.Monospace)
         option.font = font
         option.palette.setColor(QPalette.Text, QColor(FILE_STYLE))

      super().drawRow(painter, option, index)