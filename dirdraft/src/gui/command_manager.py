import logging

from gui.ui_commands import AddNodeCommand, RemoveNodeCommand, MoveNodeCommand, RenameNodeCommand
from PyQt5.QtWidgets import QTreeWidgetItem

class CommandManager:
   def __init__(self, tree_widget, template_design_page):
      self.command_stack = []
      self.logger = logging.getLogger(__name__)
      self.tree_widget = tree_widget
      self.template_design_page = template_design_page

   def push_command(self, command):
      self.command_stack.append(command)
      node_name = command.new_node.name if isinstance(command, AddNodeCommand) else command.node.name if hasattr(command, 'node') else 'N/A'
      parent_node_name = command.parent_node.name if hasattr(command, 'parent_node') and command.parent_node else 'N/A'
      command_details = f"Command: {command.__class__.__name__}, Node: {node_name}, Parent Node: {parent_node_name}"
      self.logger.info(f"Pushed command: {command_details}")

      # Execute the command immediately
      self.execute_command(command)

   def execute_command(self, command):
      template = self.template_design_page.template
      if isinstance(command, AddNodeCommand):
         template.add_node(command.parent_node, command.new_node)
         if command.parent_node is None:
               self.logger.info(f"Added node '{command.new_node.name}' to root")
               self.template_design_page.summary_text.append(f"Added node '{command.new_node.name}' to root")
         else:
               self.logger.info(f"Added node '{command.new_node.name}' to '{command.parent_node.name}'")
               self.template_design_page.summary_text.append(f"Added node '{command.new_node.name}' to '{command.parent_node.name}'")
         self.update_tree_widget_item(command)
      elif isinstance(command, RemoveNodeCommand):
         template.remove_node(command.node)
         self.logger.info(f"Removed node '{command.node.name}'")
         self.template_design_page.summary_text.append(f"Removed node '{command.node.name}'")
         self.update_tree_widget_item(command)
      elif isinstance(command, RenameNodeCommand):
         command.node.rename(command.new_name)
         self.logger.info(f"Renamed node from '{command.node.name}' to '{command.new_name}'")
         self.template_design_page.summary_text.append(f"Renamed node from '{command.node.name}' to '{command.new_name}'")
         self.update_tree_widget_item(command)
      elif isinstance(command, MoveNodeCommand):
         old_parent_node = self.template.find_parent_node(command.node)
         old_parent_node.remove_child(command.node)
         command.new_parent_node.add_child(command.node)
         self.logger.info(f"Moved node '{command.node.name}' from '{old_parent_node.name}' to '{command.new_parent_node.name}'")
         self.template_design_page.summary_text.append(f"Moved node '{command.node.name}' from '{old_parent_node.name}' to '{command.new_parent_node.name}'")
         self.update_tree_widget_item(command)

   def undo(self):
      if self.command_stack:
         command = self.command_stack.pop()
         self.undo_command(command)
      else:
         
         self.logger.info("Command stack is empty. Nothing to undo.")

   def undo_command(self, command):
      template = self.template_design_page.template
      if isinstance(command, AddNodeCommand):
         template.remove_node(command.new_node)
         self.logger.info(f"Undid adding node '{command.new_node.name}'")
      elif isinstance(command, RemoveNodeCommand):
         template.add_node(command.parent_node, command.node)
         self.logger.info(f"Undid removing node '{command.node.name}'")

   def redo(self):
      if self.command_stack:
         command = self.command_stack[-1]
         self.execute_command(command)
      else:
         self.logger.info("Command stack is empty. Nothing to redo.")

   def update_tree_widget(self, command):
      # Update the QTreeWidget based on the command
      if isinstance(command, AddNodeCommand):
         self.update_add_node(command.parent_node, command.new_node)
      elif isinstance(command, RemoveNodeCommand):
         self.update_remove_node(command.node)
      elif isinstance(command, MoveNodeCommand):
         self.update_move_node(command.node, command.new_parent_node)
         
   def update_tree_widget_item(self, command):
      if isinstance(command, AddNodeCommand):
         parent_item = self.tree_widget.find_item_by_node(command.parent_node)
         new_item = self.tree_widget.find_or_create_item(command.new_node, parent_item)
      elif isinstance(command, RemoveNodeCommand):
         item = self.tree_widget.find_item_by_node(command.node)
         if item:
               parent = item.parent()
               if parent:
                  parent.removeChild(item)
               else:
                  self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))
      elif isinstance(command, RenameNodeCommand):
         item = self.tree_widget.find_item_by_node(command.node)
         if item:
               item.setText(0, command.new_name)
      elif isinstance(command, MoveNodeCommand):
         node = command.node
         new_parent_item = self.tree_widget.find_item_by_node(command.new_parent_node)
         item = self.tree_widget.find_item_by_node(node)
         if item and new_parent_item:
               old_parent = item.parent()
               if old_parent:
                  old_parent.removeChild(item)
               new_parent_item.addChild(item)

   def update_add_node(self, parent_node, new_node):
      parent_item = self.tree_widget.find_item_by_node(parent_node)
      if parent_item:
         new_item = self.tree_widget.create_item(new_node, parent_item)

   def update_remove_node(self, node):
      item = self.tree_widget.find_item_by_node(node)
      if item:
         parent = item.parent()
         if parent:
               parent.removeChild(item)
         else:
               self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(item))

   def update_move_node(self, node, new_parent_node):
      item = self.tree_widget.find_item_by_node(node)
      new_parent_item = self.tree_widget.find_item_by_node(new_parent_node)
      if item and new_parent_item:
         old_parent = item.parent()
         if old_parent:
               old_parent.removeChild(item)
         new_parent_item.addChild(item)