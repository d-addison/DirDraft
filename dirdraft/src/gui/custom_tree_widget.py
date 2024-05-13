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
      super().__init__()
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

class CustomTreeWidget(QTreeWidget):
   drop_signal = pyqtSignal(QTreeWidgetItem, list)

   def __init__(self, parent=None):
      super().__init__(parent)
      self.logger = logging.getLogger(__name__)
      self.setDragEnabled(True)
      self.setAcceptDrops(True)
      self.setDropIndicatorShown(True)
      self.setColumnCount(3)
      self.setHeaderLabels(["Name", "Type", "Tags"])
      self.setSelectionMode(QTreeWidget.SingleSelection)
      self.setItemDelegate(HTMLDelegate())
      self.stylized_display = False

   def data(self, index, role):
      if role == Qt.DisplayRole:
         item = self.itemFromIndex(index)
         if item is not None and index.column() == 2:  # Tags column
               node = item.data(0, Qt.UserRole)
               return item.apply_tag_styles()
      return super().data(index, role)

   def create_item(self, node, parent_item=None):
      child_item = CustomTreeWidgetItem(node)

      if parent_item:
         parent_item.addChild(child_item)
         if node.type == 'folder':
            child_item.setExpanded(True)
      else:
         self.addTopLevelItem(child_item)

      return child_item

   def populate_tree_widget(self, parent_node, parent_item=None):
      for child_node in parent_node.children:
         child_item = self.find_or_create_item(child_node, parent_item)

         if child_node.type == 'folder':
               child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
               child_item.setExpanded(True)  # Set the folder item to be expanded by default
               self.populate_tree_widget(child_node, child_item)

   def find_or_create_item(self, node, parent_item):
      # Search for an existing item with the same node
      for i in range(self.topLevelItemCount() if parent_item is None else parent_item.childCount()):
         item = self.topLevelItem(i) if parent_item is None else parent_item.child(i)
         if isinstance(item, CustomTreeWidgetItem) and item.node == node:
               return item

      # If no existing item is found, create a new one
      child_item = self.create_item(node, parent_item)

      return child_item

   def set_styling_mode(self, enabled):
      self.stylized_display = enabled
      self.clear()
      self.populate_tree_widget(self.parent().template.root_node)

   def toggle_item_styling(self, item):
      item.toggle_styling()
      for i in range(item.childCount()):
         child_item = item.child(i)
         self.toggle_item_styling(child_item)
      self.repaint()

   def drawRow(self, painter, option, index):
      item = self.itemFromIndex(index)
      if item is None:
         return

      node = item.node
      font = QFont()
      font.setStyleHint(QFont.Monospace)

      # Determine the tag style to apply based on precedence
      tag_style = self.get_tag_style(node)

      # Set the font and text styles based on the tag style
      option.font = font
      option.text_style = tag_style if tag_style else NO_STYLE

      # Handle column-specific content and styling
      if index.column() == 0:  # Name column
         option.text = self.get_styled_text(node.name, option.text_style)
      elif index.column() == 1:  # Type column
         option.text = self.get_styled_text(node.type, option.text_style)
      elif index.column() == 2:  # Tags column
         option.text = self.get_tags_html(node)
      option.textElideMode = Qt.ElideNone  # Disable text eliding

      # Draw the text with the specified font and color
      painter.save()
      painter.setFont(option.font)

      doc = QTextDocument()
      doc.setHtml(option.text)
      doc.setDocumentMargin(0)
      painter.translate(option.rect.x(), option.rect.y())
      doc.drawContents(painter, QRectF(0, 0, option.rect.width(), option.rect.height()))

      painter.restore()

      super().drawRow(painter, option, index)

   def get_tag_style(self, node):
      for tag in TAG_PRECEDENCE:
         if tag in node.tags:
               return TAG_STYLES[tag]
      return None

   def get_styled_text(self, text, style):
      if style:
         return f"<span style='color:{style}'>{text}</span>"
      else:
         return text

   def get_tags_html(self, node):
      tag_styles = []
      for tag in node.tags:
         if tag in TAG_STYLES:
               tag_styles.append(f"<span style='{TAG_STYLES[tag]}'>{tag}</span>")
         else:
               tag_styles.append(tag)
      tags_with_styles = ", ".join(tag_styles)
      return tags_with_styles

   def mousePressEvent(self, event):
      item = self.itemAt(event.pos())
      if item:
         self.clearSelection()
         item.setSelected(True)
      else:
         self.clearSelection()
      super().mousePressEvent(event)

   def dropEvent(self, event):
      if event.mimeData().hasText():
         item_text = event.mimeData().text()
         parent_item = self.itemAt(event.pos())
         if parent_item:
               parent_node = parent_item.node
               new_node = Node(item_text, os.path.join(parent_node.path, item_text), 'folder')
               new_item = CustomTreeWidgetItem(new_node)
               new_item.setData(0, Qt.UserRole, new_node)
               parent_item.addChild(new_item)
               parent_node.add_child(new_node)
               # Update the template structure
               command = MoveNodeCommand(self.parent().template, new_node, parent_node)
               self.parent().observer.push_command(command)
         else:
               new_item = CustomTreeWidgetItem(Node(item_text, os.path.join(self.parent().parent_dir, item_text), 'folder'))
               new_item.setData(0, Qt.UserRole, new_node)
               self.addTopLevelItem(new_item)
         event.acceptProposedAction()

   def find_node_by_name(self, name):
      def traverse(node):
         if node.name == name:
               return node
         for child in node.children:
               found_node = traverse(child)
               if found_node:
                  return found_node
         return None

      return traverse(self.parent().template.root_node)

   def find_item_by_node(self, node):
      def traverse(item):
         if isinstance(item, CustomTreeWidgetItem) and item.node == node:
               return item
         for i in range(item.childCount()):
               child_item = item.child(i)
               found_item = traverse(child_item)
               if found_item:
                  return found_item
         return None

      for i in range(self.topLevelItemCount()):
         top_level_item = self.topLevelItem(i)
         found_item = traverse(top_level_item)
         if found_item:
               return found_item
      return None
