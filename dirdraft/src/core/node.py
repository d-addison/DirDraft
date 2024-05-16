import logging
import os
import re

class Node:
   def __init__(self, name, path, node_type, tags=None, is_generated=False, root=False):
      self.logger = logging.getLogger(__name__)
      
      # Validate node name
      if not self.is_valid_name(name):
         raise ValueError(f"Invalid node name: {name}")

      # Validate node path
      if not self.is_valid_path(path):
         raise ValueError(f"Invalid node path: {path}")

      self.name = name
      self.path = path
      self.type = node_type  # 'file' or 'folder'
      self.is_generated = is_generated
      self.children = []  # For folder nodes
      self.root = root

      # Initialize empty tags list if tags is None otherwise add unique tags to list
      if tags is None:
         self.tags = []
      else:
         tags.append(node_type)
         self.tags = list(set(tags))

      self.logger.info(f"Created node: Name: {self.name}, Path: {self.path}, Type: {self.type}, Tags: {self.tags}, Generated: {self.is_generated}, Root: {self.root}")
      
   def __repr__(self):
      return f"Node(\nName: {self.name}, \nPath: {self.path}, \nType: {self.type}, \nChildren: {len(self.children)}, \nTags: {self.tags}, \nGenerated: {self.is_generated}\n)"

   def __del__(self):
      self.logger.info(f"Deleted node: {self.name}")
      
   def set_root_status(self, status):
      self.root = status
      
   def get_root_status(self):
      return self.root
      
   def is_valid_name(self, name):
      # Check if the name is empty or contains only whitespace characters
      if not name or name.isspace():
         return False

      # Define a regular expression pattern to match valid file/folder names
      pattern = r'^[^\\/:\*\?"<>\|]+$'
      return bool(re.match(pattern, name))

   def is_valid_path(self, path):
      # TODO: Properly implement this function
      # Check if the path is a valid absolute path
      return True
      #return os.path.isabs(path)

   def add_child(self, child_node):
      if self.type == 'folder':
            self.children.append(child_node)
            self.logger.info(f"Added child node '{child_node.name}' to '{self.name}'")
      else:
         self.logger.warning(f"Cannot add child node to a file node: {self.name}")

   def remove_child(self, child_node):
      if self.type == 'folder':
            self.children.remove(child_node)
            self.logger.info(f"Removed child node '{child_node.name}' from '{self.name}'")
      else:
         self.logger.warning(f"Cannot remove child node from a file node: {self.name}")

   def rename(self, new_name):
      old_name = self.name
      self.name = new_name
      self.logger.info(f"Renamed node from '{old_name}' to '{new_name}'")

   def move(self, new_path):
      old_path = self.path
      self.path = new_path
      self.logger.info(f"Moved node from '{old_path}' to '{new_path}'")
      
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
         'is_generated': self.is_generated,
         'tags': self.tags,
         'children': [child.serialize() for child in self.children]
      }
      return serialized_node

   @classmethod
   def deserialize(cls, serialized_data):
      name = serialized_data['name']
      path = serialized_data['path']
      node_type = serialized_data['type']
      is_generated = serialized_data['is_generated']
      tags = serialized_data.get('tags', [])
      node = cls(name, path, node_type, tags, is_generated)
      children_data = serialized_data.get('children', [])
      for child_data in children_data:
         child_node = cls.deserialize(child_data)
         node.add_child(child_node)
      return node