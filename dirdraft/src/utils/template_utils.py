import os
import json
import logging
from utils.singleton import Singleton

from core.node import Node
from core.template import Template

class TemplateManager(metaclass=Singleton):
   """
   Singleton class to manage templates. It can store up to 10 templates.
   """
   
   def __init__(self):
      self.templates = []
      self.logger = logging.getLogger(__name__)

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

   def save_template(self, template, file_path):
      template_data = {
         'name': template.name,
         'root_node': template.root_node.serialize()
      }
      with open(file_path, 'w') as file:
         json.dump(template_data, file, indent=4)
      self.logger.info(f"Saved template '{template.name}' to file '{file_path}'")

   def load_template(self, file_path):
      try:
         with open(file_path, 'r') as file:
               template_data = json.load(file)
         root_node = Node.deserialize(template_data['root_node'])
         template = Template(root_node, template_data['name'])
         self.logger.info(f"Loaded template '{template.name}' from file '{file_path}'")
         return template
      except Exception as e:
         self.logger.error(f"Error loading template from {file_path}: {e}")
         return None