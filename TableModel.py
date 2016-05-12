import operator
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL


class TableModel(QAbstractTableModel):
    """
    This class is used to save the content of a tableView.
    """
    def __init__(self, parent):
        """
        Creates the TableModel

        :param parent: The parent node
        :return: The TableModel
        """
        super().__init__(parent)
        self.content = []
        self.header = []
        self.accessor = ""

    def setHeaderAndContent(self, data):
        """
        Sets the Header an the content with the given data.
        The first array is the header the other ones the content.

        :param data: Header and Content as an Array
        :return: None
        """
        self.beginResetModel()
        self.header = data[0]
        self.content = data[1:]
        self.endResetModel()

    def getHeaderAndContent(self):
        """
        Gets the Header an the content.
        The first array is the header the other ones the content.

        :return: Header and Content as an Array
        """
        return [self.header] + self.content

    def addRow(self, index):
        """
        Adds an emtpy row to the content on the specified index.

        :param index: The index where the row should be inserted
        :return: None
        """
        self.beginInsertRows(QModelIndex(), index, index)
        self.content.insert(index, [""] * len(self.header))
        self.endInsertRows()

    def removeRows(self, index, amount=1):
        """
        Removes the rows from index to index+amount.

        :param index: Index of the first row
        :param amount: How much rows should be deleted
        :return: None
        """
        self.beginRemoveRows(QModelIndex(), index, index+amount-1)
        i = 0
        for i in range(0,amount):
            self.content.pop(index)
        self.endRemoveRows()

    def dupplicateRow(self, index):
        """
        Duplicates the row with the given index.

        :param index: The index of the row
        :return: None
        """
        self.beginInsertRows(QModelIndex(), index, index)
        self.content.insert(index+1, self.content[index])
        self.endInsertRows()


    # All functions after are used by the tableView and are essential for diplaying the
    # content correctly

    def columnCount(self, parent=None):
        """
        Returns the column count.

        :param parent: The parent node
        :return: the column count
        """
        return len(self.header)

    def rowCount(self, parent=None):
        """
        Returns the row count

        :param parent: The parent node
        :return: the row count
        """
        return len(self.content)

    def data(self, index, role=Qt.DisplayRole):
        """
        Returns the data with the specified QModelIndex

        :param index: QModelIndex of the cell
        :param role: The role of access
        :return: the content of the cell
        """
        if index.isValid() and role == Qt.DisplayRole:
            return self.content[index.row()][index.column()]
        else:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        """
        Sets the value of an cell with the specified QModelIndex

        :param index: QModelIndex of the cell
        :param value: The new value
        :param role: The role of access
        :return: None
        """
        self.beginResetModel()
        self.content[index.row()][index.column()] = value
        self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Returns the Header.

        :param section: The index column of the header
        :param orientation: The orientation of the header
        :param role: The role of access
        :return: The Header
        """
        if orientation == Qt.Horizontal and role==Qt.DisplayRole:
            return self.header[section]

    def flags(self, index):
        """
        Returns the flags of a cell

        :param index: QModelIndex of a cell
        :return: the flags of a cell
        """
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def sort(self, col, order):
        """
        Make it possible to sort the content.

        :param col: index of column
        :param order: The order
        :return: None
        """
        self.beginResetModel()
        self.content = sorted(self.content,key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.content.reverse()
        self.endResetModel()