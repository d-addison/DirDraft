import sys
from pathlib import Path
from PyQt5.QtWidgets import QTreeWidgetItem, QFileSystemModel

"""
Finds the files and folders in a given directory.
"""
def find_files_and_folders(directory):
   files = []
   folders = []
   print(directory)
   directory = Path(directory)
   for file in directory.iterdir():
      if file.is_file():
         files.append(file)
      elif file.is_dir():
         folders.append(file)
   return files, folders

"""
Generates PyQt nodes for the given list of files and folders.
"""
def generate_nodes(files, folders):
   nodes = []
   for file in files:
      nodes.append(QTreeWidgetItem([file.name]))
   for folder in folders:
      nodes.append(QTreeWidgetItem([folder.name]))
   return nodes

"""
Takes a directory and generates a tree of files and folders.
"""
def generate_tree(directory):
   files, folders = find_files_and_folders(directory)
   nodes = generate_nodes(files, folders)
   return nodes

"""
Populates the QApplication with the given nodes so they're visible in the application.
"""
def populate_app(nodes, folder_view, directory="C:\\2024"):
   model = QFileSystemModel()
   model.setRootPath(directory)
   folder_view.setModel(model)
   folder_view.setRootIndex(model.index(directory))
   for node in nodes:
      node.setExpanded(True)