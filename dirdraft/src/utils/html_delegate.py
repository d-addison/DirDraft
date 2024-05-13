from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle, QApplication
from PyQt5.QtGui import QTextDocument, QPalette, QAbstractTextDocumentLayout, QBrush
from PyQt5.QtCore import Qt

class HTMLDelegate(QStyledItemDelegate):
   def paint(self, painter, option, index):
      options = QStyleOptionViewItem(option)
      self.initStyleOption(options, index)

      style = options.widget.style() if options.widget else QApplication.style()

      doc = QTextDocument()
      doc.setHtml(options.text)
      doc.setDocumentMargin(2)  # Add a small margin around the text

      options.text = ""
      style.drawControl(QStyle.CE_ItemViewItem, options, painter)

      ctx = QAbstractTextDocumentLayout.PaintContext()
      blackBrush = QBrush(Qt.black)
      ctx.palette.setBrush(QPalette.Text, blackBrush)

      textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options)
      painter.save()
      painter.translate(textRect.topLeft())
      painter.setClipRect(textRect.translated(-textRect.topLeft()))
      doc.documentLayout().draw(painter, ctx)
      painter.restore()
