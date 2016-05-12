import copy
from PySide.QtGui import QUndoCommand


class EditCommand(QUndoCommand):
    """
    This class is used for editing one specific cell.
    It is also used from the class ItemDelegate.
    """
    def __init__(self, model, index, newValue=None):
        """
        Initializes a new EditCommand

        :param model: The model of the tableView
        :param index: The QModelIndex of the cell
        :param newValue: Optional new value (can be set later)
        :return: new Command
        """
        super().__init__()
        self.model = model
        self.index = index
        self.newValue = newValue
        self.oldValue = None

    def undo(self):
        """
        Undo the EditCommand

        :return: None
        """
        self.newValue = self.model.data(self.index)
        self.model.setData(self.index, self.oldValue)

    def redo(self):
        """
        Redo the EditCommand

        :return: None
        """
        self.oldValue = self.model.data(self.index)
        self.model.setData(self.index, self.newValue)

class AddRowCommand(QUndoCommand):
    """
    This class is used for adding an empty cell.
    """
    def __init__(self, model, index):
        """
        Initializes a new AddRowCommand

        :param model: The model of the tableView
        :param index: The index of the row
        :return: new Command
        """
        super().__init__()
        self.model = model
        self.index = index

    def undo(self):
        """
        Undo the AddRowCommand

        :return: None
        """
        self.model.removeRows(self.index)

    def redo(self):
        """
        Redo the AddRowCommand

        :return: None
        """
        self.model.addRow(self.index)

class RemoveRowsCommand(QUndoCommand):
    """
    This class is used for removing one ore more rows.
    Saving all changes would be to difficult so the whole model is saved
    """
    def __init__(self, model, index, amount):
        """
        Initializes a new RemoveRowCommand

        :param model: The model of the tableView
        :param index: The index of the row
        :param amount: The number of rows that should be deleted
        :return: new Command
        """
        super().__init__()
        self.oldModel = model
        self.model = model
        self.index = index
        self.amount = amount

    def undo(self):
        """
        Undo the RemoveRowCommand

        :return: None
        """
        self.model.setHeaderAndContent(self.oldModel.getHeaderAndContent())

    def redo(self):
        """
        Redo the RemoveRowCommand

        :return: None
        """
        # hard copy of the actual model
        self.oldModel = copy.deepcopy(self.model)
        self.model.removeRows(self.index, self.amount)

class DuplicateRowCommand(QUndoCommand):
    """
    This class is used for duplicating one row.
    """
    def __init__(self, model, index):
        """
        Initializes a new DuplicateRowCommand

        :param model: The model of the tableView
        :param index: The index of the row
        :return: new Command
        """
        super().__init__()
        self.model = model
        self.index = index

    def undo(self):
        """
        Undo the DuplicateRowCommand

        :return: None
        """
        self.model.removeRows(self.index+1)

    def redo(self):
        """
        Redo the DuplicateRowCommand

        :return: None
        """
        self.model.dupplicateRow(self.index)