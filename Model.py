from PySide.QtCore import QAbstractTableModel, Qt, SIGNAL, QObject, QModelIndex


class TableModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.content = []
        self.header = []
        self.accessor = ""

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return self.content[index.row()][index.column()]
        else:
            return None

    def setHeaderAndContent(self, data):
        self.beginResetModel()
        self.header = data[0]
        self.content = data[1:]
        self.endResetModel()

    def getHeaderAndContent(self):
        return [self.header] + self.content

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role==Qt.DisplayRole:
            return self.header[section]

    def columnCount(self, parent=None):
        return len(self.header)

    def rowCount(self, parent=None):
        return len(self.content)

    def setData(self, index, value, role=Qt.EditRole):
        self.beginResetModel()
        self.content[index.row()][index.column()] = value
        self.endResetModel()

    def addRow(self, index):
        self.beginInsertRows(QModelIndex(), index, index)
        self.content.insert(index, [""] * len(self.header))
        self.endInsertRows()

    def removeRows(self, index, amount=1):
        self.beginRemoveRows(QModelIndex(), index, index+amount-1)
        i = 0
        for i in range(0,amount):
            self.content.pop(index+i)
        self.endRemoveRows()

    def dupplicateRow(self, index):
        self.beginInsertRows(QModelIndex(), index, index)
        self.content.insert(index+1, self.content[index])
        self.endInsertRows()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
