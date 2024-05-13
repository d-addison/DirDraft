import os
import shutil

class Node:
   def __init__(self, name, path, node_type, tags=None, is_generated=False):
      self.name = name
      self.path = path
      self.type = node_type  # 'file' or 'folder'
      self.is_generated = is_generated
      self.children = []  # For folder nodes
      # Initialize empty tags list if tags is None otherwise add unique tags to list
      if tags is None:
         self.tags = []
      else:
         self.tags = list(set(tags))
      
   def __repr__(self):
      return f"Node(\nName: {self.name}, \nPath: {self.path}, \nType: {self.type}, \nChildren: {self.children}, \nTags: {self.tags}, \nGenerated: {self.is_generated}\n)"

   def add_child(self, child_node):
      if self.type == 'folder':
         self.children.append(child_node)

   def remove_child(self, child_node):
      if self.type == 'folder':
         self.children.remove(child_node)

   def rename(self, new_name):
      self.name = new_name

   def move(self, new_path):
      self.path = new_path
      
   def insert_tags(self, new_tags):
      # Add the default tag based on node type
      if self.type == 'folder' and 'folder' not in self.tags:
         self.tags.append('folder')
      elif self.type == 'file' and 'file' not in self.tags:
         self.tags.append('file')

      # Add the new tags
      for tag in new_tags:
         if tag not in self.tags:
               self.tags.append(tag)
      
   def serialize(self):
      serialized_node = {
         'name': self.name,
         'path': self.path,
         'type': self.type,
         'is_generated': self.is_generated,
         'tags': self.tags,  # Include tags in the serialized data
         'children': [child.serialize() for child in self.children]
      }
      return serialized_node

   @classmethod
   def deserialize(cls, serialized_data):
      name = serialized_data['name']
      path = serialized_data['path']
      node_type = serialized_data['type']
      is_generated = serialized_data['is_generated']
      tags = serialized_data.get('tags', [])  # Get tags from the serialized data, or use an empty list as default
      node = cls(name, path, node_type, tags, is_generated)
      children_data = serialized_data.get('children', [])  # Get children data from the serialized data, or use an empty list as default
      for child_data in children_data:
         child_node = cls.deserialize(child_data)
         node.add_child(child_node)
      return node