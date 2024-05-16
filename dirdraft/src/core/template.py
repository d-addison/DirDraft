from core.node import Node
import os
import logging

class Template:
   def __init__(self, root_node, name=None):
      self.logger = logging.getLogger(__name__)
      
      if root_node is None:
         root_node = Node("Root", "", "folder", tags=["root_node"], is_generated=True, root=True)
         self.logger.info(f"No root node specified. Creating a root node with name: {root_node.name}")
      else:
         # Validate root node
         if not isinstance(root_node, Node):
            raise TypeError("Root node must be an instance of Node")
         if root_node.type != 'folder':
            raise ValueError("Root node must be a folder")
         
      if name and (not name or name.isspace()):
         raise ValueError("Template name cannot be empty or contain only whitespace characters")
      
      self.root_node = root_node
      self.name = name
      self.logger.info(f"Created template: {self.name}")
      
   def __repr__(self):
      return self._recursive_repr(self.root_node, 0)

   def __del__(self):
      self.logger.info(f"Deleted template: {self.name}")

   def _recursive_repr(self, node, indent_level):
      indent = '  ' * indent_level
      node_repr = f"{indent}{repr(node)}\n"

      for child in node.children:
         node_repr += self._recursive_repr(child, indent_level + 1)

      return node_repr

   def get_structure(self):
      print(self)

   def build_from_directory(self, directory_path):
      if self.root_node is None:
         # Create the root node
         root_name = os.path.basename(directory_path)
         self.root_node = Node(root_name, directory_path, 'folder', is_generated=True)
         self.logger.info(f"No root node specified. Creating a root node with name: {self.root_node.name}")

      # Recursively build the template structure
      self._build_nodes(directory_path, self.root_node)

   def _build_nodes(self, directory_path, parent_node):
      # Iterate over the contents of the directory
      for item in os.listdir(directory_path):
         item_path = os.path.join(directory_path, item)

         # Create a Node instance for the current item
         if os.path.isdir(item_path):
               node_type = 'folder'
         else:
               node_type = 'file'
         node = Node(item, item_path, node_type, is_generated=True)

         # Add the node to the parent node
         parent_node.add_child(node)
         self.logger.info(f"Added node '{node.name}' to '{parent_node.name}'")

         # If the current item is a directory, recursively build its children
         if node_type == 'folder':
               self._build_nodes(item_path, node)
               
   def get_root_node(self):
      return self.root_node

   def add_node(self, parent_node, new_node):
      # Add a new node to the template
      if parent_node is None:
         # If no parent node is specified, set the new node as the root node
         # if the template doesn't have a root node yet
         if self.root_node is None:
               new_node.set_root_status(True)
               self.root_node = new_node
               self.logger.info(f"Set '{new_node.name}' as the root node")
         else:
               # Otherwise, add the new node as a child of the root node
               parent_node = self.root_node
               self.logger.info(f"No parent node specified. Adding node to root node: {parent_node.name}")
      else:
         # Validate parent node
         if not isinstance(parent_node, Node):
               raise TypeError("Parent node must be an instance of Node")
         if parent_node.type != 'folder':
               raise ValueError("Parent node must be a folder")

         # Check for duplicate node names within the same parent directory
         if parent_node != self.root_node and any(child.name == new_node.name for child in parent_node.children):
            raise ValueError(f"Duplicate node name '{new_node.name}' in parent directory '{parent_node.name}'")

      parent_node.add_child(new_node)
      self.logger.info(f"Added node '{new_node.name}' to '{parent_node.name}'")

   def find_parent_node(self, node):
      # Helper function to find the parent node of a given node
      def traverse(current_node):
         if current_node.children:
               for child in current_node.children:
                  if child == node:
                     return current_node
                  else:
                     parent = traverse(child)
                     if parent:
                           return parent
         return None

      return traverse(self.root_node)

   def traverse(self, callback):
      # Traverse the template and call the callback function for each node
      def traverse_nodes(node):
         callback(node)
         for child in node.children:
               traverse_nodes(child)

      traverse_nodes(self.root_node)

   def set_name(self, name):
      old_name = self.name
      self.name = name
      self.logger.info(f"Renamed template from '{old_name}' to '{name}'")