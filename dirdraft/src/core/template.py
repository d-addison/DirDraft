from core.node import Node
import os

class Template:
   def __init__(self, root_node):
      self.root_node = root_node

   def build_from_directory(self, directory_path):
      # Create the root node
      root_name = os.path.basename(directory_path)
      self.root_node = Node(root_name, directory_path, 'folder', is_generated=True)

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

         # If the current item is a directory, recursively build its children
         if node_type == 'folder':
               self._build_nodes(item_path, node)

   def add_node(self, parent_node, new_node):
      # Add a new node to the template
      parent_node.add_child(new_node)

   def remove_node(self, node):
      # Remove a node from the template
      parent_node = self.find_parent_node(node)
      if parent_node:
         parent_node.remove_child(node)

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