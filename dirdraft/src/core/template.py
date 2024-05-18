import os
import logging

from core.node import Node
from utils.file_operations import FileOperations
from collections import defaultdict

class Template:
   """ 
   A template is a node that contains other nodes. It is used to represent the structure of a directory tree.
   
   Attributes:
      name (str): The name of the template.
      root_node (Node): The root node of the template.
      children (list): A list of children nodes.
   
   Pattern: Composite
   """
   
   def __init__(self, root_node, name=None):
      self.logger = logging.getLogger(__name__)
      self.file_operations = FileOperations()

      if root_node is None:
         root_node = Node("Root", ".", "folder", tags=["root_node"], root=True)
         self.logger.info(f"No root node specified. Creating a root node with name: {root_node.name}, path: {root_node.path}")
      else:
         self._validate_root_node(root_node)

      if not name or name.isspace():
         raise ValueError("Template name cannot be empty or contain only whitespace characters")

      self.name = name
      self.root_node = root_node

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
   
   def _validate_root_node(self, root_node):
      if not isinstance(root_node, Node):
         raise TypeError("Root node must be an instance of Node")
      if root_node.type != 'folder':
         raise ValueError("Root node must be a folder")

   def get_structure(self):
      print(self)
      
   def execute(self, base_dir):
      # Update the root node path with the provided base directory
      self.root_node.path = base_dir

      # Recursively update the paths of all child nodes
      self._update_node_paths(self.root_node)

      # Perform topological sort on the nodes
      sorted_nodes = self.topological_sort(self.root_node)

      # Recursively create the directory structure and files
      for node in sorted_nodes:
         self._create_structure(node)
      
   def _update_node_paths(self, node):
      self.logger.info(f"Entering _update_node_paths with args: arg1={node}")
      # Update the node's path based on its parent's path
      if node.parent:
         node.path = os.path.join(node.parent.path, node.name)

      # Recursively update the paths of child nodes
      for child in node.children:
         self._update_node_paths(child)
      self.logger.info(f"Exiting _update_node_paths.")
         
   def topological_sort(self, root_node):
      """
      Perform a topological sort on the nodes of the template.
      """
      in_degree = defaultdict(int)
      graph = defaultdict(list)
      sorted_nodes = []

      # Calculate the in-degree of each node
      def calculate_in_degree(node):
         for child in node.children:
               in_degree[child] += 1
               graph[node].append(child)
               calculate_in_degree(child)

      calculate_in_degree(root_node)

      # Perform topological sort
      queue = [node for node in in_degree if in_degree[node] == 0]
      while queue:
         node = queue.pop(0)
         sorted_nodes.append(node)
         for neighbor in graph[node]:
               in_degree[neighbor] -= 1
               if in_degree[neighbor] == 0:
                  queue.append(neighbor)

      return sorted_nodes
      
   def _create_structure(self, node):
      self.logger.info(f"Entering _create_structure with args: arg1={node}")
      node_path = node.path

      if node.type == 'folder':
         self.file_operations.create_directory(node_path)
      else:
         # Create the file
         self.file_operations.create_file(node_path)
      self.logger.info(f"Exiting _create_structure.")

   def build_from_directory(self, directory_path):
      if self.root_node is None:
         # Create the root node
         root_name = os.path.basename(directory_path)
         self.root_node = Node(root_name, directory_path, 'folder', tags=["generated"])
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
         node = Node(item, item_path, node_type, tags=["generated"])

         # Add the node to the parent node
         parent_node.add_child(node)
         self.logger.info(f"Added node '{node.name}' to '{parent_node.name}'")

         # If the current item is a directory, recursively build its children
         if node_type == 'folder':
            self._build_nodes(item_path, node)
               
   def get_root_node(self):
      self.logger.info(f"Entering get_root_node")
      self.logger.info(f"Exiting get_root_node with result: {self.root_node}")
      return self.root_node

   def add_node(self, parent_node, new_node):
      self.logger.info(f"Entering add_node with args: arg1={parent_node}, arg2={new_node}")
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

      parent_node.add_child(new_node)
      self.logger.info(f"Added node '{new_node.name}' to '{parent_node.name}'")
      self.logger.info(f"Exiting add_node.")

   def find_parent_node(self, node):
      self.logger.info(f"Entering find_parent_node with args: arg1={node}")
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
         self.logger.info(f"Exiting find_parent_node with result: None")
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
      self.logger.info(f"Entering set_name with args: arg1={name}")
      old_name = self.name
      self.name = name
      self.logger.info(f"Renamed template from '{old_name}' to '{name}'")
      self.logger.info(f"Exiting set_name.")