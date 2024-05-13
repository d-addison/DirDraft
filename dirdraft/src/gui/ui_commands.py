import os
import shutil
import logging

from PyQt5.QtWidgets import QUndoCommand

class AddNodeCommand(QUndoCommand):
   def __init__(self, template, parent_node, new_node, tree_widget):
      self.logger = logging.getLogger(__name__)
      self.template = template
      self.parent_node = parent_node
      self.new_node = new_node
      self.tree_widget = tree_widget

   def undo(self):
      self.template.remove_node(self.new_node)
      self.logger.info(f"Undid adding node '{self.new_node.name}'")

   def redo(self):
      self.template.add_node(self.parent_node, self.new_node)
      if self.parent_node is None:
         self.logger.info(f"Redid adding node '{self.new_node.name}' to root")
      else:
         self.logger.info(f"Redid adding node '{self.new_node.name}' to '{self.parent_node.name}'")

class RemoveNodeCommand(QUndoCommand):
   def __init__(self, template, node, tree_widget):
      self.template = template
      self.node = node
      self.parent_node = template.find_parent_node(node)
      self.tree_widget = tree_widget
      self.node_path = os.path.join(self.tree_widget.parent().parent_dir, self.node.name)

   def undo(self):
      self.template.add_node(self.parent_node, self.node)
      if self.parent_node is None:
         self.logger.info(f"Undid removing node '{self.node.name}' from root")
      else:  
         self.logger.info(f"Undid removing node '{self.node.name}' from '{self.parent_node.name}'")

   def redo(self):
      self.template.remove_node(self.node)
      self.logger.info(f"Redid removing node '{self.node.name}'")

class RenameNodeCommand(QUndoCommand):
   def __init__(self, template, node, new_name, tree_widget):
      self.template = template
      self.node = node
      self.old_name = node.name
      self.new_name = new_name
      self.tree_widget = tree_widget

   def undo(self):
      self.node.rename(self.old_name)
      self.logger.info(f"Undid renaming node from '{self.new_name}' to '{self.old_name}'")

   def redo(self):
      self.node.rename(self.new_name)
      self.logger.info(f"Redid renaming node from '{self.old_name}' to '{self.new_name}'")

class MoveNodeCommand:
   def __init__(self, template, node, new_parent_node, tree_widget):
      self.template = template
      self.node = node
      self.new_parent_node = new_parent_node
      self.old_parent_node = template.find_parent_node(node)
      self.tree_widget = tree_widget

   def undo(self):
      self.new_parent_node.remove_child(self.node)
      self.old_parent_node.add_child(self.node)
      self.logger.info(f"Undid moving node '{self.node.name}' from '{self.old_parent_node.name}' to '{self.new_parent_node.name}'")

   def redo(self):
      self.old_parent_node.remove_child(self.node)
      self.new_parent_node.add_child(self.node)
      self.logger.info(f"Redid moving node '{self.node.name}' from '{self.old_parent_node.name}' to '{self.new_parent_node.name}'")

class DeleteFileCommand(QUndoCommand):
   def __init__(self, template_design_page, node, description):
      super().__init__(description)
      self.template_design_page = template_design_page
      self.node = node

   def undo(self):
      path = os.path.join(self.template_design_page.parent_dir, self.node.path)
      if not os.path.exists(path):
         if self.node.type == 'file':
               with open(path, 'w') as f:
                  pass
               self.template_design_page.summary_text.append(f"Restored file: {path}")
         elif self.node.type == 'folder':
               os.makedirs(path)
               self.template_design_page.summary_text.append(f"Restored directory: {path}")

   def redo(self):
      path = os.path.join(self.template_design_page.parent_dir, self.node.path)
      if os.path.exists(path):
         if self.node.type == 'file':
               os.remove(path)
               self.template_design_page.summary_text.append(f"Deleted file: {path}")
         elif self.node.type == 'folder':
               shutil.rmtree(path, ignore_errors=True)
               self.template_design_page.summary_text.append(f"Deleted directory: {path}")