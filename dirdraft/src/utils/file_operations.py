import os
import shutil
import logging

class FileOperations:
   def __init__(self):
      self.logger = logging.getLogger(__name__)

   def create_directory(self, path):
      try:
         os.makedirs(path, exist_ok=True)
         self.logger.info(f"Created directory: {path}")
      except Exception as e:
         self.logger.error(f"Error creating directory {path}: {e}")

   def create_file(self, path):
      try:
         with open(path, 'w') as f:
               pass
         self.logger.info(f"Created file: {path}")
      except Exception as e:
         self.logger.error(f"Error creating file {path}: {e}")

   def delete_file(self, path):
      try:
         os.remove(path)
         self.logger.info(f"Deleted file: {path}")
      except Exception as e:
         self.logger.error(f"Error deleting file {path}: {e}")

   def delete_directory(self, path):
      try:
         shutil.rmtree(path, ignore_errors=True)
         self.logger.info(f"Deleted directory: {path}")
      except Exception as e:
         self.logger.error(f"Error deleting directory {path}: {e}")