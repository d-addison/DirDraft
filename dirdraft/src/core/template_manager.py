import os
from core.template import Template
from core.node import Node
import json

class TemplateManager:
   def __init__(self):
      self.templates = []

   def add_template(self, template):
      if len(self.templates) < 10:
         self.templates.append(template)

   def remove_template(self, index):
      if 0 <= index < len(self.templates):
         del self.templates[index]

   def get_template(self, index):
      if 0 <= index < len(self.templates):
         return self.templates[index]
      return None

   def save_template(self, directory_path, template_name):
      print(f"Saving templates to {directory_path}")
      if not os.path.exists(directory_path):
         os.makedirs(directory_path)
      for i, template in enumerate(self.templates):
         file_path = os.path.join(directory_path, f"{directory_path + template_name}.json")
         template.save_to_file(file_path)

   # In the TemplateManager class
   # Loads the template specified by the directory path using load_from_file and returns the index of the template
   def load_template(self, directory_path):
      isLoaded = self.load_from_file(directory_path)
      if isLoaded is not None:
         for i, template in enumerate(self.templates):
            if template.name == isLoaded:
               return i
      else:
         return 0

   # In the Template class
   @classmethod
   def load_from_file(cls, file_path):
      try:
         with open(file_path, 'r') as file:
               template_data = json.load(file)
         root_node = Node.deserialize(template_data['root_node'])
         return cls(root_node)
      except Exception as e:
         print(f"Error loading template from {file_path}: {e}")
         return None