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