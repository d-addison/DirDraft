from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt

class MainMenuPage(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)

      # Set up the layout
      layout = QVBoxLayout()
      self.setLayout(layout)

      # Create a QTreeWidget
      self.tree_widget = QTreeWidget()
      self.tree_widget.setColumnCount(1)
      self.tree_widget.setHeaderLabels(["Main Menu"])
      layout.addWidget(self.tree_widget)