from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyle
from PyQt5.QtCore import Qt, QMimeData, QUrl, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QDrag, QBrush
from utils.styles import FOLDER_STYLE, FILE_STYLE, GENERATED_STYLE
from core.node import Node
import os

class CustomTreeWidget(QTreeWidget):
   drop_signal = pyqtSignal(QTreeWidgetItem, list)
   
   def __init__(self, parent=None):
      super().__init__(parent)
      self.setDragEnabled(True)
      self.setAcceptDrops(True)
      self.setDropIndicatorShown(True)
      self.setColumnCount(2)
      self.setHeaderLabels(["Name", "Type"])
      self.setSelectionMode(QTreeWidget.SingleSelection)

   def drawRow(self, painter, option, index):
      item = self.itemFromIndex(index)
      if item is None:
         return

      node = item.data(0, Qt.UserRole)
      font = QFont()
      font.setStyleHint(QFont.Monospace)

      if node.is_generated:
         option.font = font
         option.palette.setColor(QPalette.Text, QColor(GENERATED_STYLE))
      elif node.type == "folder":
         font.setBold(True)
         option.font = font
         option.palette.setColor(QPalette.Text, QColor(FOLDER_STYLE))
      elif node.type == "file":
         font.setItalic(True)
         option.font = font
         option.palette.setColor(QPalette.Text, QColor(FILE_STYLE))

      super().drawRow(painter, option, index)

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