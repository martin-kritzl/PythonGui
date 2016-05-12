from PySide.QtGui import QMainWindow, QApplication, QFileDialog, QUndoStack
import sys
from CSVHandler import CSVHandler
from Delegate import ItemDelegate
from TableModel import TableModel
from Command import AddRowCommand, RemoveRowsCommand, DuplicateRowCommand, EditCommand
import gui


class Controller(QMainWindow):
    """
    This class is used to connect the gui and the model. All logical
    tasks are done here.
    """
    def __init__(self, parent=None):
        """
        Initializes the gui, undoStack, tableModel, tableView and the csvHandler

        :param parent: The parent node
        :return: new Controller
        """
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
        """
        Connects the defined menu-entries with functions

        :return: None
        """
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

    def pushCommand(self, cmd, name):
        """
        This function pushes the given command to the undoStack.
        So the command will be scheduled and can be undone with the command pattern

        :param cmd: The Command that should be done
        :param name: The name this command has
        :return: None
        """
        self.undoStack.beginMacro(name)
        self.undoStack.push(cmd)
        self.undoStack.endMacro()
        self.changeUndoRedoMenu()

    def open(self):
        """
        Opens a file-manager where the user can choose an file to open.
        The content fill be filled in the model.

        :return: None
        """
        path = QFileDialog.getOpenFileName()[0]
        if path:
            self.model.accessor = path
            self.model.setHeaderAndContent(self.handler.getFile(path))

    def save(self):
        """
        Saves the tablemodel to the same location

        :return: None
        """
        self.handler.saveFile(self.model.accessor, self.model.getHeaderAndContent())

    def saveAs(self):
        """
        Saves the tableModel to a new location. In a file-manager the user
        could choose the destination

        :return: None
        """
        path = QFileDialog.getSaveFileName()[0]
        if path:
            self.model.accessor=path
            self.handler.saveFile(self.model.accessor, self.model.getHeaderAndContent())

    def getFirstSelectedIndex(self):
        """
        Returns the first selected index of the selected cells.

        :return: QModelIndex of the first selected index
        """
        return self.form.tableView.selectionModel().selectedIndexes()[0]

    def getClipboard(self):
        """
        Returns the text saved in the clipboard

        :return: The text in the clipboard
        """
        clipboard = QApplication.clipboard()
        return str(clipboard.text())

    def setClipboard(self, delete=False):
        """
        Sets the clipboard to the actual selected cell.

        :param delete: Specifies if the cell should be empty after coping
        :return: None
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(str(self.model.data(self.getFirstSelectedIndex())))
        if delete==True:
            self.pushCommand(EditCommand(self.model, self.getFirstSelectedIndex()),"Cutted Text")

    def copy(self):
        """
        Copies the actual selected cell to the clipboard.

        :return: None
        """
        self.setClipboard()

    def cut(self):
        """
        Cuts the actual selected cell to the clipboard.

        :return: None
        """
        self.setClipboard(True)

    def paste(self):
        """
        Pastes the clipboard to the actual selected cell.

        :return: None
        """
        self.pushCommand(EditCommand(self.model, self.getFirstSelectedIndex(), self.getClipboard()),"Pasted Text")

    def redo(self):
        """
        Redo to the next command

        :return: None
        """
        self.undoStack.redo()
        self.changeUndoRedoMenu()

    def undo(self):
        """
        Undo the actual command

        :return: None
        """
        self.undoStack.undo()
        self.changeUndoRedoMenu()

    def changeUndoRedoMenu(self):
        """
        Changes the menu-entry for redo and undo. So the user can see what the last and next command is.

        :return:
        """
        undo = "Undo"
        redo = "Redo"
        if self.undoStack.undoText():
            undo += " (" + self.undoStack.undoText() + ")"
        if self.undoStack.redoText():
            redo += " (" + self.undoStack.redoText() + ")"
        self.form.undo.setText(undo)
        self.form.redo.setText(redo)

    def getSelection(self):
        """
        Returns the row index of selection and the amount.

        :return: First selected row index and amount
        """
        selection = self.form.tableView.selectionModel().selectedIndexes()
        if selection:
            return selection[0].row(), len(selection)

    def addRow(self):
        """
        Adds a row to the table

        :return: None
        """
        index, amount = self.getSelection()
        self.pushCommand(AddRowCommand(self.model, index), "Added row")

    def duplicateRow(self):
        """
        Duplicates the selected row

        :return: None
        """
        index, amount = self.getSelection()
        self.pushCommand(DuplicateRowCommand(self.model, index), "Duplicated row")

    def removeRow(self):
        """
        Removes the selected rows

        :return: None
        """
        index, amount = self.getSelection()
        self.pushCommand(RemoveRowsCommand(self.model, index, amount), "Removed row(s)")

# Essential for running the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = Controller()
    c.show()
    sys.exit(app.exec_())