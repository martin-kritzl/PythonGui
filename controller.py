from PySide.QtGui import QMainWindow, QApplication, QFileDialog, QUndoStack
import sys
from CSVHandler import CSVHandler
from Delegate import ItemDelegate
from Model import TableModel
from command import AddRowCommand, RemoveRowsCommand, DuplicateRowCommand, EditCommand
import gui


class Controller(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.form = gui.Ui_MainWindow()
        self.form.setupUi(self)

        self.undoStack = QUndoStack()

        self.model = TableModel(self)
        self.form.tableView.setModel(self.model)
        self.form.tableView.setItemDelegate(ItemDelegate(self.undoStack, self.pushCommand))
        self.form.tableView.resizeColumnsToContents()

        self.handler = CSVHandler()

        self.connectUi()

    def connectUi(self):
        self.form.open.triggered.connect(self.open)
        self.form.save.triggered.connect(self.save)
        self.form.saveAs.triggered.connect(self.saveAs)
        self.form.copy.triggered.connect(self.copy)
        self.form.cut.triggered.connect(self.cut)
        self.form.paste.triggered.connect(self.paste)
        self.form.redo.triggered.connect(self.redo)
        self.form.undo.triggered.connect(self.undo)
        self.form.addRow.triggered.connect(self.addRow)
        self.form.duplicateRow.triggered.connect(self.duplicateRow)
        self.form.removeRow.triggered.connect(self.removeRow)

    def editedSomething(self):
        self.form.tableView.reset()

    def pushCommand(self, cmd, name):
        self.undoStack.beginMacro(name)
        self.undoStack.push(cmd)
        self.undoStack.endMacro()
        self.changeUndoRedoMenu()
        self.editedSomething()

    def open(self):
        path = QFileDialog.getOpenFileName()[0]
        if path:
            self.model.accessor = path
            self.model.setHeaderAndContent(self.handler.getFile(path))
            self.editedSomething()

    def save(self):
        self.handler.saveFile(self.model.accessor, self.model.getHeaderAndContent())

    def saveAs(self):
        path = QFileDialog.getSaveFileName()[0]
        if path:
            self.model.accessor=path
            self.handler.saveFile(self.model.accessor, self.model.getHeaderAndContent())

    def getClipboard(self):
        clipboard = QApplication.clipboard()
        return str(clipboard.text())

    def setClipboard(self, delete=False):
        clipboard = QApplication.clipboard()
        selection = self.form.tableView.selectionModel().selectedIndexes()[0]
        clipboard.setText(str(self.model.data(selection)))
        if delete==True:
            self.pushCommand(EditCommand(self.model, selection),"Cutted Text")

    def copy(self):
        self.setClipboard()

    def cut(self):
        self.setClipboard(True)

    def paste(self):
        self.pushCommand(EditCommand(self.model, self.form.tableView.selectionModel().selectedIndexes()[0], self.getClipboard()),"Pasted Text")

    def redo(self):
        self.undoStack.redo()
        self.changeUndoRedoMenu()

    def undo(self):
        self.undoStack.undo()
        self.changeUndoRedoMenu()

    def changeUndoRedoMenu(self):
        undo = "Undo"
        redo = "Redo"
        if self.undoStack.undoText():
            undo += " (" + self.undoStack.undoText() + ")"
        if self.undoStack.redoText():
            redo += " (" + self.undoStack.redoText() + ")"
        self.form.undo.setText(undo)
        self.form.redo.setText(redo)

    def getSelection(self):
        selection = self.form.tableView.selectionModel().selectedIndexes()
        if selection:
            return selection[0].row(), len(selection)


    def addRow(self):
        index, amount = self.getSelection()
        self.pushCommand(AddRowCommand(self.model, index), "Added row")

    def duplicateRow(self):
        index, amount = self.getSelection()
        self.pushCommand(DuplicateRowCommand(self.model, index), "Duplicated row")

    def removeRow(self):
        index, amount = self.getSelection()
        self.pushCommand(RemoveRowsCommand(self.model, index, amount), "Removed row(s)")


app = QApplication(sys.argv)
c = Controller()
c.show()
sys.exit(app.exec_())