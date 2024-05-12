import logging
from core.commands import AddNodeCommand, RemoveNodeCommand, RenameNodeCommand, MoveNodeCommand
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt

class Observer:
   def __init__(self, tree_widget):
      self.command_stack = []
      self.logger = logging.getLogger("dirdraft")
      self.tree_widget = tree_widget

   def push_command(self, command):
      self.command_stack.append(command)
      command_details = f"Command: {command.__class__.__name__}, Node: {command.node.name if hasattr(command, 'node') else 'N/A'}, Parent Node: {command.parent_node.name if hasattr(command, 'parent_node') else 'N/A'}"
      self.logger.info(f"Pushed command: {command_details}")
      print(f"Pushed command: {command_details}")

   def undo(self):
      if self.command_stack:
         command = self.command_stack.pop()
         self.logger.info(f"Undoing command: {command.__class__.__name__}")
         command.undo()
         self.update_tree_widget(command)

   def redo(self):
      if self.command_stack:
         command = self.command_stack[-1]
         self.logger.info(f"Redoing command: {command.__class__.__name__}")
         command.redo()
         self.update_tree_widget(command)

   def update_tree_widget(self, command):
      # Update the QTreeWidget based on the command
      if isinstance(command, AddNodeCommand):
            self.update_add_node(command.parent_node, command.new_node)
      elif isinstance(command, RemoveNodeCommand):
         self.update_remove_node(command.node)
      elif isinstance(command, RenameNodeCommand):
         self.update_rename_node(command.node, command.new_name)
      elif isinstance(command, MoveNodeCommand):
         self.update_move_node(command.node, command.new_parent_node)

   def update_add_node(self, parent_node, new_node):
      parent_item = self.tree_widget.find_item_by_node(parent_node)
      if parent_item:
         new_item = QTreeWidgetItem(parent_item, [new_node.name, new_node.type])
         new_item.setData(0, Qt.UserRole, new_node)
         parent_item.addChild(new_item)

   def update_remove_node(self, node):
      item = self.tree_widget.find_item_by_node(node)
      if item:
         parent = item.parent()
         if parent:
               parent.removeChild(item)
         else:
               self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))

   def update_rename_node(self, node, new_name):
      item = self.tree_widget.find_item_by_node(node)
      if item:
         item.setText(0, new_name)

   def update_move_node(self, node, new_parent_node):
      item = self.tree_widget.find_item_by_node(node)
      new_parent_item = self.tree_widget.find_item_by_node(new_parent_node)
      if item and new_parent_item:
         old_parent = item.parent()
         if old_parent:
               old_parent.removeChild(item)
         new_parent_item.addChild(item)