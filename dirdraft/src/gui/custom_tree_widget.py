from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QUrl, pyqtSignal, QRectF
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QDrag, QBrush, QTextDocument
from utils.styles import FOLDER_STYLE, FILE_STYLE, GENERATED_STYLE, TAG_STYLES, TAG_PRECEDENCE, NO_STYLE, NAME_COLUMN, TYPE_COLUMN, TAGS_COLUMN, PATH_COLUMN
from core.node import Node
import os
from utils.html_delegate import HTMLDelegate
from gui.ui_commands import MoveNodeCommand
from gui.custom_tree_widget_item import CustomTreeWidgetItem

import logging
class CustomTreeWidget(QTreeWidget):
   drop_signal = pyqtSignal(QTreeWidgetItem, list)

   def __init__(self, parent=None):
      super().__init__(parent)
      self.logger = logging.getLogger(__name__)
      self.setDragEnabled(True)
      self.setAcceptDrops(True)
      self.setDropIndicatorShown(True)
      self.setColumnCount(4)
      self.setHeaderLabels(["Name", "Type", "Tags", "Path"])
      self.setSelectionMode(QTreeWidget.SingleSelection)
      self.setItemDelegate(HTMLDelegate())
      self.stylized_display = False
      self.populated_nodes = set()
      self.logger.info("Created CustomTreeWidget with headers: %s", self.headerItem().text(0))

   def create_item(self, node, parent_item=None):
      self.logger.info(f"Entering create_item with args: arg1={node}, arg2={parent_item}")
      
      child_item = CustomTreeWidgetItem(node)

      if parent_item:
         parent_item.addChild(child_item)
      else:
         self.addTopLevelItem(child_item)
         
      self.logger.info(f"Exiting create_item with result: {child_item}")
      return child_item

   def populate_tree_widget(self, parent_node, parent_item=None):
      self.logger.info(f"Entering populate_tree_widget with args: arg1={parent_node}, arg2={parent_item}")

      if parent_node.children is None:
         self.logger.info(f"No children found for node: {parent_node.name}")
         return

      if parent_node.get_root_status():
         self.logger.info(f"Node is root node: {parent_node.name}")
         root_item = self.create_item(parent_node)
         self.addTopLevelItem(root_item)
         self.logger.info(f"Created root item: {root_item}")

      for child_node in parent_node.children:
         if child_node not in self.populated_nodes:
            child_item = self.find_or_create_item(child_node, parent_item)
            self.populated_nodes.add(child_node)

            if child_node.type == 'folder':
               self.populate_tree_widget(child_node, child_item)
      
      # Expand the root item after adding its child items
      if parent_item is None:
         root_item.setExpanded(True)
         root_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

   def find_or_create_item(self, node, parent_item):
      self.logger.info(f"Entering find_or_create_item with args: arg1={node}, arg2={parent_item}")
      
      # Search for an existing item with the same node
      for i in range(self.topLevelItemCount() if parent_item is None else parent_item.childCount()):
         item = self.topLevelItem(i) if parent_item is None else parent_item.child(i)
         if isinstance(item, CustomTreeWidgetItem) and item.node == node:
            self.logger.info(f"Exiting find_or_create_item with result: {item}")
            return item

      # If no existing item is found, create a new one
      child_item = self.create_item(node, parent_item)
      
      self.logger.info(f"Exiting find_or_create_item with result: {child_item}")

      return child_item

   def set_styling_mode(self, enabled):
      self.logger.info(f"Entering set_styling_mode with arg: arg1={enabled}")
      
      self.stylized_display = enabled
      self.clear()
      self.populate_tree_widget(self.parent().template.root_node)
      
      self.logger.info(f"Exiting set_styling_mode with result: {self.stylized_display}")

   def toggle_item_styling(self, item):
      self.logger.info(f"Entering toggle_item_styling with arg: arg1={item}")
      item.toggle_styling()
      for i in range(item.childCount()):
         child_item = item.child(i)
         self.toggle_item_styling(child_item)
      self.repaint()
      
      self.logger.info(f"Exiting toggle_item_styling with result: {item}")

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
      if index.column() == NAME_COLUMN:  # Name column
         item.setText(NAME_COLUMN, self.get_styled_text(node.name, option.text_style))
      elif index.column() == TYPE_COLUMN:  # Type column
         item.setText(TYPE_COLUMN, self.get_styled_text(node.type, option.text_style))
      elif index.column() == TAGS_COLUMN:  # Tags column
         item.setText(TAGS_COLUMN, self.get_tags_html(node))
      elif index.column() == PATH_COLUMN:  # Path column
         item.setText(PATH_COLUMN, self.get_styled_text(node.path, option.text_style))

      # Draw the text with the specified font and color
      painter.save()
      painter.setFont(option.font)

      doc = QTextDocument()
      doc.setHtml(item.text(index.column()))
      doc.setDocumentMargin(0)
      painter.translate(option.rect.x(), option.rect.y())
      doc.drawContents(painter, QRectF(0, 0, option.rect.width(), option.rect.height()))

      painter.restore()

      super().drawRow(painter, option, index)

   def get_tag_style(self, node):
      self.logger.info(f"Entering get_tag_style with arg: arg1={node}")
      
      for tag in TAG_PRECEDENCE:
         if tag in node.tags:
            self.logger.info(f"Exiting get_tag_style with result: {TAG_STYLES[tag]}")
            return TAG_STYLES[tag]
      self.logger.info(f"Exiting get_tag_style with result: {None}")
      return None

   def get_styled_text(self, text, style):
      self.logger.info(f"Entering get_styled_text with args: arg1={text}, arg2={style}")
      
      result = text
      
      if style:
         result = f"<span style='{style}'>{text}</span>"
      
      self.logger.info(f"Exiting get_styled_text with result: {result}")
      return result

   def get_tags_html(self, node):
      self.logger.info(f"Entering get_tags_html with arg: arg1={node}")
      
      tag_styles = []
      for tag in node.tags:
         if tag in TAG_STYLES:
            tag_styles.append(f"<span style='{TAG_STYLES[tag]}'>{tag}</span>")
            self.logger.info(f"Added tag '{tag}' with style '{TAG_STYLES[tag]}'")
         else:
            tag_styles.append(tag)
            self.logger.info(f"Added tag '{tag}' with no style")
      tags_with_styles = ", ".join(tag_styles)
      
      self.logger.info(f"Exiting get_tags_html with result: {tags_with_styles}")
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
      self.info.logger(f"Entering find_node_by_name with arg: arg1={name}")
      
      def traverse(node):
         if node.name == name:
            self.info.logger(f"Exiting find_node_by_name>traverse with result: {node}")
            return node
         for child in node.children:
            found_node = traverse(child)
            if found_node:
               self.info.logger(f"Exiting find_node_by_name>traverse with result: {found_node}")
               return found_node
         self.info.logger(f"Exiting find_node_by_name>traverse with result: {None}")
         return None

      return traverse(self.parent().template.root_node)

   def find_item_by_node(self, node):
      self.logger.info(f"Entering find_item_by_node with arg: arg1={node}")
      
      def traverse(item):
         if isinstance(item, CustomTreeWidgetItem) and item.node == node:
            self.logger.info(f"Exiting find_item_by_node>traverse with result: {item}")
            return item
         for i in range(item.childCount()):
            child_item = item.child(i)
            found_item = traverse(child_item)
            if found_item:
               self.logger.info(f"Exiting find_item_by_node>traverse with result: {found_item}")
               return found_item
         self.logger.info(f"Exiting find_item_by_node>traverse with result: {None}")
         return None

      for i in range(self.topLevelItemCount()):
         top_level_item = self.topLevelItem(i)
         found_item = traverse(top_level_item)
         if found_item:
            self.logger.info(f"Exiting find_item_by_node with result: {found_item}")
            return found_item
      self.logger.info(f"Exiting find_item_by_node with result: {None}")
      return None
