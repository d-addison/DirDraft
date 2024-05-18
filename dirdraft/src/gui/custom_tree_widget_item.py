from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QUrl, pyqtSignal, QRectF
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QDrag, QBrush, QTextDocument
from utils.styles import FOLDER_STYLE, FILE_STYLE, GENERATED_STYLE, TAG_STYLES, TAG_PRECEDENCE, NO_STYLE, NAME_COLUMN, TYPE_COLUMN, TAGS_COLUMN, PATH_COLUMN
from core.node import Node
import os
from utils.html_delegate import HTMLDelegate
from gui.ui_commands import MoveNodeCommand

import logging

class CustomTreeWidgetItem(QTreeWidgetItem):
   def __init__(self, node):
      QTreeWidgetItem.__init__(self)
      #super().__init__(self)
      self.logger = logging.getLogger(__name__)
      self.node = node
      self.styling_enabled = False
      self.setText(NAME_COLUMN, self.node.name)
      self.setText(TYPE_COLUMN, self.node.type)
      #tags_with_styles = self.apply_tag_styles()
      tags = ", ".join(self.node.tags)
      self.setText(TAGS_COLUMN, str(tags))
      
      self.setText(PATH_COLUMN, self.node.path)

      # Associate the Node object with the item
      self.setData(0, Qt.UserRole, self.node)
      
      self.logger.info(f"Created CustomTreeWidgetItem for node: {self.node.name}, path: {self.node.path}, type: {self.node.type}, tags: {self.node.tags}")

   def apply_tag_styles(self):
      self.logger.info(F"Entering apply_tag_styles with args: arg1={self.node.tags}")
      
      tag_styles = []
      for tag in self.node.tags:
         if self.styling_enabled and tag in TAG_STYLES:
            tag_styles.append(f"<span style='{TAG_STYLES[tag]}'>{tag}</span>")
         else:
            tag_styles.append(tag)
      tags_with_styles = ", ".join(tag_styles)
      
      self.logger.info(F"Exiting apply_tag_styles with result: {tags_with_styles}")
      return tags_with_styles

   def toggle_styling(self):
      self.logger.info(f"Entering toggle_styling with args: arg1={self.styling_enabled}")
      
      self.styling_enabled = not self.styling_enabled
      self.emitDataChanged()
      
      self.logger.info(f"Exiting toggle_styling with result: {self.styling_enabled}")