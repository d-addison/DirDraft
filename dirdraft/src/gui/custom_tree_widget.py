from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyle
from PyQt5.QtCore import Qt, QMimeData, QUrl, pyqtSignal, QRectF
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QDrag, QBrush, QTextDocument
from utils.styles import FOLDER_STYLE, FILE_STYLE, GENERATED_STYLE, TAG_STYLES, TAG_PRECEDENCE, NO_STYLE
from core.node import Node
import os
from utils.html_delegate import HTMLDelegate

class CustomTreeWidget(QTreeWidget):
   drop_signal = pyqtSignal(QTreeWidgetItem, list)
   
   def __init__(self, parent=None):
      super().__init__(parent)
      self.setDragEnabled(True)
      self.setAcceptDrops(True)
      self.setDropIndicatorShown(True)
      self.setColumnCount(3)
      self.setHeaderLabels(["Name", "Type", "Tags"])
      self.setSelectionMode(QTreeWidget.SingleSelection)
      self.setItemDelegate(HTMLDelegate())

   def drawRow(self, painter, option, index):
      item = self.itemFromIndex(index)
      if item is None:
         return

      node = item.data(0, Qt.UserRole)
      font = QFont()
      font.setStyleHint(QFont.Monospace)

      # Determine the tag style to apply based on precedence
      tag_style = self.get_tag_style(node)

      # Set the font and text styles based on the tag style
      option.font = font
      option.text_style = tag_style if tag_style else NO_STYLE

      # Handle column-specific content and styling
      if index.column() == 0:  # Name column
         print("Name tag_style: " + tag_style)
         option.text = self.get_styled_text(node.name, option.text_style)
         print("Name result: " + option.text)
      elif index.column() == 1:  # Type column
         print("Type tag_style: " + tag_style)
         option.text = self.get_styled_text(node.type, option.text_style)
         print("Type result: " + option.text)
      elif index.column() == 2:  # Tags column
         option.text = self.get_tags_html(node)
         print("Tags result: " + option.text)
      option.textElideMode = Qt.ElideNone  # Disable text eliding

      super().drawRow(painter, option, index)

      # Draw the text with the specified font and color
      painter.save()
      painter.setFont(option.font)

      doc = QTextDocument()
      doc.setHtml(option.text)
      doc.setDocumentMargin(0)
      painter.translate(option.rect.x(), option.rect.y())
      doc.drawContents(painter, QRectF(0, 0, option.rect.width(), option.rect.height()))

      painter.restore()

   def get_tag_style(self, node):
      for tag in TAG_PRECEDENCE:
         if tag in node.tags:
            return TAG_STYLES[tag]
      return None

   def get_styled_text(self, text, style):
      if style:
         return f"<span style='{style}'>{text}</span>"
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
               parent_node = parent_item.data(0, Qt.UserRole)
               new_node = Node(item_text, os.path.join(parent_node.path, item_text), 'folder')
               new_item = QTreeWidgetItem(parent_item, [new_node.name, new_node.type])
               new_item.setData(0, Qt.UserRole, new_node)
               parent_item.addChild(new_item)
               parent_node.add_child(new_node)
               # Update the template structure
               command = MoveNodeCommand(self.parent().template, new_node, parent_node)
               self.parent().observer.push_command(command)
               command.redo()
         else:
               new_item = QTreeWidgetItem(self, [item_text, "folder"])
               new_node = Node(item_text, os.path.join(self.parent().parent_dir, item_text), 'folder')
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
         if item.data(0, Qt.UserRole) == node:
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