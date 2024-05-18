import logging

class Component:
   def __init__(self, name, path, component_type, tags=None, root=False):
      self.logger = logging.getLogger(__name__)
      self.name = name
      self.path = path
      self.type = component_type
      self.root = root
      self.tags = tags or []
      
      self.logger.info(f"Created {self.__class__.__name__}: {self.name}")

   def add_child(self, child):
      raise NotImplementedError("add_child method must be implemented in subclasses")

   def remove_child(self, child):
      raise NotImplementedError("remove_child method must be implemented in subclasses")

   def __repr__(self):
      return f"{self.__class__.__name__}(Name: {self.name}, Path: {self.path}, Type: {self.type}, Tags: {self.tags}, Root: {self.root})"