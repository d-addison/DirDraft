class TemplateStructure:
   def __init__(self):
      self.structure = {}
   
   def add_directory(self, parent_path, directory_name):
      """
      Add a new directory to the template structure.
      
      Args:
      - parent_path: The path of the parent directory.
      - directory_name: The name of the new directory.
      """
      
      if parent_path not in self.structure:
         self.structure[parent_path] = []
         
      self.structure[parent_path][directory_name] = {}
      
   def remove_directory(self, parent_path, directory_name):
      """
      Remove a directory from the template structure.

      Args:
      - parent_path: The path of the parent directory.
      - directory_name: The name of the directory to remove.
      """

      if parent_path in self.structure:
         if directory_name in self.structure[parent_path]:
            del self.structure[parent_path][directory_name]
      
   def add_file(self, parent_path, file_name):
      """
      Add a new file to the template structure.

      Args:
      - parent_path: The path of the parent directory.
      - file_name: The name of the new file.
      """

      if parent_path not in self.structure:
         self.structure[parent_path] = []

      self.structure[parent_path][file_name] = None
   
   def remove_file(self, parent_path, file_name):
      """
      Remove a file from the template structure.
      
      Args:
      - parent_path: The path of the parent directory.
      - file_name: The name of the file to remove.
      """
         
      if parent_path in self.structure:
         if file_name in self.structure[parent_path]:
            del self.structure[parent_path][file_name]
      
   def get_structure(self):
      """
      Get the template structure.

      Returns:
      - A dictionary containing the template structure.
      """

      return self.structure