from PySide.QtGui import QLineEdit, QStyledItemDelegate
from command import EditCommand


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, undoStack, updatefunc):
        super().__init__()
        self.undoStack = undoStack
        self.updatefunc = updatefunc
        self.edit = None

    def setModelData(self, editor, model, index):
        self.edit.newValue = editor.text()
        self.updatefunc(self.edit, "Edited cell")

    def editorEvent(self, QEvent, QAbstractItemModel, QStyleOptionViewItem, QModelIndex):
        self.edit = EditCommand(QAbstractItemModel, QModelIndex)
        return False

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return QLineEdit(QWidget)