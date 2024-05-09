from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyle
from PyQt5.QtGui import QFont, QBrush, QColor, QPalette, QPixmap
from utils.styles import FOLDER_STYLE, FILE_STYLE, INACCESSIBLE_STYLE, OTHER_STYLE
import os

class CustomTreeWidget(QTreeWidget):
   def __init__(self, parent=None):
      super().__init__(parent)
      self.setColumnCount(3)
      self.setHeaderLabels(["Name", "Type", "Extension"])

   def drawRow(self, painter, option, index):
      item = self.itemFromIndex(index)
      if item is None:
         return

      item_type = item.text(1)
      directory_path = self.parent().directory_input.text()
      item_path = os.path.join(directory_path, item.text(0))

      if item_type == "folder":
         self.setItemStyle(option, FOLDER_STYLE)
      elif item_type == "file":
         self.setItemStyle(option, FILE_STYLE)
      elif item_type == "inaccessible" or item.isDisabled():
         self.setItemStyle(option, INACCESSIBLE_STYLE)
      else:
         self.setItemStyle(option, OTHER_STYLE)

      super().drawRow(painter, option, index)
   
   def setItemStyle(self, option, style):
      font = QFont()
      font.setBold(style.get("font-weight") == "bold")
      font.setItalic(style.get("font-style") == "italic")
      font.setFamily(style.get("font-family", ""))
      option.font = font
      option.palette.setColor(QPalette.Text, QColor(style["color"]))