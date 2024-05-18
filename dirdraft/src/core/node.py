import logging
import os
import re
from core.component import Component

class Node(Component):
   """ 
   A class to represent a node in the directory tree. 
   
   Attributes:
      name (str): The name of the node.
      path (str): The path to the node.
      type (str): The type of the node. Can be 'file' or 'folder'.
      root (bool): Whether the node is the root node or not.
      children (list): A list of children nodes.
      
   Pattern: Composite
   """
   
   def __init__(self, name, path, node_type, tags=None, root=False):
      super().__init__(name, path, node_type, tags, root)
      self.logger = logging.getLogger(__name__)
      self._validate_name(name)
      self._validate_path(path)
      self.children = []  # Initialize an empty list for children
      
      self.logger.info(f"Created node: {self}")
      
      
   def __repr__(self):
      children_count = len(self.children)
      tags_str = ", ".join(self.tags)
      return (
         f"Node(\n"
         f"  Name: {self.name}\n"
         f"  Path: {self.path}\n"
         f"  Type: {self.type}\n"
         f"  Children: {children_count}\n"
         f"  Tags: {tags_str}\n"
         f"  Root: {self.root}\n"
         f")"
      )

   def __del__(self):
      self.logger.info(f"Deleted node: {self.name}")
      
   def set_root_status(self, status):
      self.logger.info(f"Entering set_root_status with args: arg1={status}")
      self.root = status
      self.logger.info(f"Exiting set_root_status with result: {status}")
      
   def get_root_status(self):
      self.logger.info(f"Entering get_root_status.")
      self.logger.info(f"Exiting get_root_status with result: {self.root}")
      return self.root
      
   def _validate_name(self, name):
      self.logger.info(f"Entering _validate_name with args: arg1={name}")
      # Check if the name is empty or contains only whitespace characters
      if not name or name.isspace():
         raise ValueError(f"Invalid node name: {name}")

      # Define a regular expression pattern to match valid file/folder names
      pattern = r'^[^\\/:\*\?"<>\|]+'
      if not re.match(pattern, name):
         raise ValueError(f"Invalid node name: {name}")
      self.logger.info(f"Exiting _validate_name.")

   def _validate_path(self, path):
      self.logger.info(f"Entering _validate_path with args: arg1={path}")
      # Check if the path is a valid absolute path
      if not path or (not os.path.isabs(path) and not path.startswith(".")):
         raise ValueError(f"Invalid node path: {path}")
      self.logger.info(f"Exiting _validate_path.")

   def add_child(self, child):
      self.logger.info(f"Entering add_child with args: arg1={child}")
      if isinstance(child, Node):
         if self.root:
            # If the current node is the root node, skip the duplicate check
            self.children.append(child)
            child.parent = self  # Set the parent reference
            child.path = os.path.join(self.path, child.name)  # Update the child's path
            self.logger.info(f"Added root node: {child.name}")
         else:
            # Check for duplicate child node names within the same parent directory
            if child.name in [c.name for c in self.children]:
               raise ValueError(f"Duplicate child node name '{child.name}' in parent '{self.name}'")
            self.children.append(child)
            child.parent = self  # Set the parent reference
            child.path = os.path.join(self.path, child.name)  # Update the child's path
            self.logger.info(f"Added child node: {child.name} to parent: {self.name}")
      else:
         raise TypeError("Child must be an instance of Node")
      self.logger.info(f"Exiting add_child.")

   def remove_child(self, child):
      self.logger.info(f"Entering remove_child with args: arg1={child}")
      if child in self.children:
         self.children.remove(child)
         self.logger.info(f"Removed child node '{child.name}' from '{self.name}'")
      else:
         self.logger.warning(f"Child node '{child.name}' not found in '{self.name}'")
      self.logger.info(f"Exiting remove_child.")

   def rename(self, new_name):
      self.logger.info(f"Entering rename with args: arg1={new_name}")
      old_name = self.name
      self.name = new_name
      try:
         self.logger.info(f"Renamed node from '{old_name}' to '{new_name}'")
      except AttributeError:
         pass
      self.logger.info(f"Exiting rename.")

   def move(self, new_path):
      self.logger.info(f"Entering move with args: arg1={new_path}")
      old_path = self.path
      self.path = new_path
      try:
         self.logger.info(f"Moved node from '{old_path}' to '{new_path}'")
      except AttributeError:
         pass
      self.logger.info(f"Exiting move.")
      
   def insert_tags(self, new_tags):
      # Add the default tag based on node type
      if self.type == 'folder' and 'folder' not in self.tags:
         self.tags.append('folder')
         self.logger.info(f"Added default 'folder' tag to node '{self.name}'")
      elif self.type == 'file' and 'file' not in self.tags:
         self.tags.append('file')
         self.logger.info(f"Added default 'file' tag to node '{self.name}'")

      # Add the new tags
      for tag in new_tags:
         if tag not in self.tags:
            self.tags.append(tag)
            self.logger.info(f"Added tag '{tag}' to node '{self.name}'")
      
   def serialize(self):
      serialized_node = {
         'name': self.name,
         'path': self.path,
         'type': self.type,
         'tags': self.tags,
         'children': [child.serialize() for child in self.children]
      }
      return serialized_node

   @classmethod
   def deserialize(cls, serialized_data):
      name = serialized_data['name']
      path = serialized_data['path']
      node_type = serialized_data['type']
      tags = serialized_data.get('tags', [])
      node = cls(name, path, node_type, tags)
      children_data = serialized_data.get('children', [])
      for child_data in children_data:
         child_node = cls.deserialize(child_data)
         node.add_child(child_node)
      return node