from PySide.QtGui import QUndoCommand


class EditCommand(QUndoCommand):
    def __init__(self, model, index):
        super().__init__()
        self.model = model
        self.index = index
        self.newValue = None
        self.oldValue = None

    def undo(self):
        self.newValue = self.model.data(self.index)
        self.model.setData(self.index, self.oldValue)

    def redo(self):
        self.oldValue = self.model.data(self.index)
        self.model.setData(self.index, self.newValue)
