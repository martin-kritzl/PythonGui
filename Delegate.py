from PySide.QtGui import QLineEdit, QStyledItemDelegate
from Command import EditCommand


class ItemDelegate(QStyledItemDelegate):
    """
    Allows a delegation of a cell editing to this class. So the command pattern could be
    implemented.
    """
    def __init__(self, undoStack, updatefunc):
        """
        Ititializes the ItemDelegate

        :param undoStack: The undoStack of the table
        :param updatefunc: The function that should be called when a cell was edited.
        :return: The ItemDelegate
        """
        super().__init__()
        self.undoStack = undoStack
        self.updatefunc = updatefunc
        self.edit = None

    def setModelData(self, editor, model, index):
        """
        Sets the new value of the cell.

        :param editor: The tableView
        :param model: The model of the tableView
        :param index: The QModelIndex of the edited cell
        :return: None
        """
        self.edit.newValue = editor.text()
        self.updatefunc(self.edit, "Edited cell")

    def editorEvent(self, QEvent, QAbstractItemModel, QStyleOptionViewItem, QModelIndex):
        """
        Creates a new EditCommand for the changing value.

        :param QEvent: The event
        :param QAbstractItemModel: The model of the tableView
        :param QStyleOptionViewItem: None
        :param QModelIndex: The QModelIndex of the edited cell
        :return:
        """
        self.edit = EditCommand(QAbstractItemModel, QModelIndex)
        return False

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        """
        Returns the editor for editing a cell

        :param QWidget: The tableView
        :param QStyleOptionViewItem: None
        :param QModelIndex: The QModelIndex of the edited cell
        :return: QLineEdit - The editor
        """
        return QLineEdit(QWidget)