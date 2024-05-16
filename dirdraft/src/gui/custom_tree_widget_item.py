from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QUrl, pyqtSignal, QRectF
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QDrag, QBrush, QTextDocument
from utils.styles import FOLDER_STYLE, FILE_STYLE, GENERATED_STYLE, TAG_STYLES, TAG_PRECEDENCE, NO_STYLE
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
      # Set the node name
      self.setText(0, self.node.name)

      # Set the node type
      self.setText(1, self.node.type)

      # Set the tags with styles
      tags_with_styles = self.apply_tag_styles()
      self.setText(2, tags_with_styles)

      # Associate the Node object with the item
      self.setData(0, Qt.UserRole, self.node)
      
      if self.node.type == 'folder':
         self.setExpanded(True)
         self.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
      
      self.logger.info(f"Created CustomTreeWidgetItem for node: {self.node.name}, type: {self.node.type}, tags: {self.node.tags}")

   def apply_tag_styles(self):
      tag_styles = []
      for tag in self.node.tags:
         if self.styling_enabled and tag in TAG_STYLES:
               tag_styles.append(f"<span style='{TAG_STYLES[tag]}'>{tag}</span>")
         else:
               tag_styles.append(tag)
      tags_with_styles = ", ".join(tag_styles)
      return tags_with_styles

   def toggle_styling(self):
      self.styling_enabled = not self.styling_enabled
      self.emitDataChanged()