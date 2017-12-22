import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

from DeviceAdapter import DeviceAdapter
from mainwindow import Ui_MainWindow


# https://github.com/FyodorovAleksej/DeviceManager


# Main Window class
class MyWin(QtWidgets.QMainWindow):
    # device Adapter for working with devices
    deviceAdapter = DeviceAdapter()

    # construct window
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #"Name": None, "GUID": None, "HardwareID": None, "Manufacture": None, "Provider": None,"Description": None, "sys file": None, "Device Path": None
        self.ui.deviceTable.setColumnCount(8)
        self.ui.deviceTable.insertRow(self.ui.deviceTable.rowCount())
        # initialize headers of table
        header1 = QTableWidgetItem("Name")
        header2 = QTableWidgetItem("GUID")
        header3 = QTableWidgetItem("HardwareID")
        header4 = QTableWidgetItem("Manufacture")
        header5 = QTableWidgetItem("Provider")
        header6 = QTableWidgetItem("Description")
        header7 = QTableWidgetItem("Sys files")
        header8 = QTableWidgetItem("Device Path")
        # set headers
        self.ui.deviceTable.setHorizontalHeaderItem(0, header1)
        self.ui.deviceTable.setHorizontalHeaderItem(1, header2)
        self.ui.deviceTable.setHorizontalHeaderItem(2, header3)
        self.ui.deviceTable.setHorizontalHeaderItem(3, header4)
        self.ui.deviceTable.setHorizontalHeaderItem(4, header5)
        self.ui.deviceTable.setHorizontalHeaderItem(5, header6)
        self.ui.deviceTable.setHorizontalHeaderItem(6, header7)
        self.ui.deviceTable.setHorizontalHeaderItem(7, header8)
        # settings for table items
        self.ui.deviceTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        headers = self.ui.deviceTable.horizontalHeader()
        headers.setStretchLastSection(True)
        # set 0 rows as default
        self.ui.deviceTable.setRowCount(0)
        # connecting buttons
        self.ui.enableButton.clicked.connect(self.enableCur)
        self.ui.disableButton.clicked.connect(self.disableCur)

    # close action
    def closeEvent(self, event):
        event.accept()

    # append 8 strings in table in 8 columns
    def appendText(self, name, guid, hardwareid, manufacture, provider, description, sys, path):
        # creating new TableItem and setting it parametres
        item1 = QTableWidgetItem(name)
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(guid)
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(hardwareid)
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item4 = QTableWidgetItem(manufacture)
        item4.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item5 = QTableWidgetItem(provider)
        item5.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item6 = QTableWidgetItem(description)
        item6.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item7 = QTableWidgetItem(sys)
        item7.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item8 = QTableWidgetItem(path)
        item8.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        # validate last item
        table = self.ui.deviceTable
        item = table.item(table.rowCount() - 1, 0)
        if (item != None):
            # adding new row in table
            table.insertRow(table.rowCount())
        # if table is empty
        if (table.rowCount() == 0):
            table.setRowCount(1)
        table.setItem(table.rowCount() - 1, 0, item1)
        table.setItem(table.rowCount() - 1, 1, item2)
        table.setItem(table.rowCount() - 1, 2, item3)
        table.setItem(table.rowCount() - 1, 3, item4)
        table.setItem(table.rowCount() - 1, 4, item5)
        table.setItem(table.rowCount() - 1, 5, item6)
        table.setItem(table.rowCount() - 1, 6, item7)
        table.setItem(table.rowCount() - 1, 7, item8)

    def refreshDevices(self):
        self.errorInfo("refreshing")
        # getting all devices info
        deviceList = self.deviceAdapter.getDeviceList()
        nameList = []
        # flag for finding this device
        flag = -1
        for deviceInfo in deviceList:
            nameList.append(deviceInfo["HardwareID"])
            # iterate all names in table
            for index in range(self.ui.deviceTable.rowCount()):
                if (self.ui.deviceTable.item(index, 2) != None):
                    if (self.ui.deviceTable.item(index, 2).text() == deviceInfo["HardwareID"]):
                        # save index of equals item
                        flag = index
            # if table don't contain this device
            if (flag == -1):
                if (deviceInfo != None):
                    self.appendText(deviceInfo["Name"], deviceInfo["GUID"], deviceInfo["HardwareID"], deviceInfo["Manufacture"], deviceInfo["Provider"], deviceInfo["Description"], deviceInfo["sys file"], deviceInfo["Device Path"])
            else:
                # update device information (size)
                self.updateRow(flag, deviceInfo)
        # checking ejecting devices
        for i in range(0, self.ui.deviceTable.rowCount()):
            if (self.ui.deviceTable.item(i, 2) != None):
                if (not (self.ui.deviceTable.item(i, 2).text() in nameList)):
                    # remove device from table
                    self.ui.deviceTable.removeRow(i)

    def refreshStatus(self):
        # refresh status of all devices
        for i in range(0, self.ui.deviceTable.rowCount()):
            if (self.ui.deviceTable.item(i, 2) != None):
                if (self.deviceAdapter.refreshStatus(self.ui.deviceTable.item(i, 2).text())):
                    self.ui.deviceTable.item(i, 0).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 1).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 2).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 3).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 4).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 5).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 6).setBackground(QColor(125, 225, 125))
                    self.ui.deviceTable.item(i, 7).setBackground(QColor(125, 225, 125))
                else:
                    self.ui.deviceTable.item(i, 0).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 1).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 2).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 3).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 4).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 5).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 6).setBackground(QColor(225, 125, 125))
                    self.ui.deviceTable.item(i, 7).setBackground(QColor(225, 125, 125))


    def enableCur(self):
        # getting selected row
        indexes = self.ui.deviceTable.selectionModel().selectedRows()
        for index in sorted(indexes):
            #  enable selected device
            message = self.deviceAdapter.enable(self.ui.deviceTable.item(index.row(), 2).text())
            # print info when device was enabled
            self.errorInfo(message)

    def disableCur(self):
        # getting selected row
        indexes = self.ui.deviceTable.selectionModel().selectedRows()
        for index in sorted(indexes):
            # disabling selected device
            message = self.deviceAdapter.disable(self.ui.deviceTable.item(index.row(), 2).text())
            # print error message if can't disable device
            self.errorInfo(message)

    # print info about enabling/disabling
    def errorInfo(self, message):
        if (message != None):
            print(message)
            self.ui.infoLabel.setText("info: " + message)

    # update information about input device
    def updateRow(self, row, deviceInfo):
        # creating new item
        item1 = QTableWidgetItem(deviceInfo["Name"])
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(deviceInfo["GUID"])
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(deviceInfo["HardwareID"])
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item4 = QTableWidgetItem(deviceInfo["Manufacture"])
        item4.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item5 = QTableWidgetItem(deviceInfo["Provider"])
        item5.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item6 = QTableWidgetItem(deviceInfo["Description"])
        item6.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item7 = QTableWidgetItem(deviceInfo["sys file"])
        item7.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item8 = QTableWidgetItem(deviceInfo["Device Path"])
        item8.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        table = self.ui.deviceTable
        if (row < table.rowCount()):
            table.setItem(row, 0, item1)
            table.setItem(row, 1, item2)
            table.setItem(row, 2, item3)
            table.setItem(row, 3, item4)
            table.setItem(row, 4, item5)
            table.setItem(row, 5, item6)
            table.setItem(row, 6, item7)
            table.setItem(row, 7, item8)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()

    # creating timer for refresh main window
    window.refreshDevices()
    timer = QTimer()
    timer.timeout.connect(window.refreshStatus)
    timer.start(40000)
    sys.exit(app.exec_())
    exit()
