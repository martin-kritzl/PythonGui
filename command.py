import copy
from PySide.QtGui import QUndoCommand


class EditCommand(QUndoCommand):
    def __init__(self, model, index, newValue=None):
        super().__init__()
        self.model = model
        self.index = index
        self.newValue = newValue
        self.oldValue = None

    def undo(self):
        self.newValue = self.model.data(self.index)
        self.model.setData(self.index, self.oldValue)

    def redo(self):
        self.oldValue = self.model.data(self.index)
        self.model.setData(self.index, self.newValue)

class AddRowCommand(QUndoCommand):
    def __init__(self, model, index):
        super().__init__()
        self.model = model
        self.index = index

    def undo(self):
        self.model.removeRows(self.index)

    def redo(self):
        self.model.addRow(self.index)

class RemoveRowsCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        super().__init__()
        self.oldModel = model
        self.model = model
        self.index = index
        self.amount = amount

    def undo(self):
        self.model.setHeaderAndContent(self.oldModel.getHeaderAndContent())

    def redo(self):
        self.oldModel = copy.deepcopy(self.model)
        self.model.removeRows(self.index, self.amount)

class DuplicateRowCommand(QUndoCommand):
    def __init__(self, model, index):
        super().__init__()
        self.model = model
        self.index = index

    def undo(self):
        self.model.removeRows(self.index+1)

    def redo(self):
        self.model.dupplicateRow(self.index)