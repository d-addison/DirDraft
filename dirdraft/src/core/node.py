import os
import shutil

class Node:
   def __init__(self, name, path, node_type, tags=None, is_generated=False):
      self.name = name
      self.path = path
      self.type = node_type  # 'file' or 'folder'
      self.is_generated = is_generated
      self.children = []  # For folder nodes
      self.tags = tags or []

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
      
   def serialize(self):
      serialized_node = {
         'name': self.name,
         'path': self.path,
         'type': self.type,
         'is_generated': self.is_generated,
         'children': [child.serialize() for child in self.children]
      }
      return serialized_node

   @classmethod
   def deserialize(cls, serialized_data):
      name = serialized_data['name']
      path = serialized_data['path']
      node_type = serialized_data['type']
      is_generated = serialized_data['is_generated']
      node = cls(name, path, node_type, is_generated)
      for child_data in serialized_data['children']:
         child_node = cls.deserialize(child_data)
         node.add_child(child_node)
      return node