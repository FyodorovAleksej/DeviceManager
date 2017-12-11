import re
import subprocess
import sys

import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

from DeviceAdapter import DeviceAdapter
from mainwindow import Ui_MainWindow


# Main Window class
class MyWin(QtWidgets.QMainWindow):
    # USB Adapter for working with USB devices
    deviceAdapter = DeviceAdapter()

    # construct window
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # default column size
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
        # connecting eject button
        self.ui.enableButton.clicked.connect(self.connect)

    # close action
    def closeEvent(self, event):
        event.accept()

    # append 3 strings in table in 3 columns
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
        # getting flesh-memory
        deviceList = self.deviceAdapter.getDeviceList()
        nameList = []
        # flag for finding this device
        flag = -1
        for deviceInfo in deviceList:
            nameList.append(deviceInfo["GUID"])
            # iterate all names in table
            for index in range(self.ui.deviceTable.rowCount()):
                if (self.ui.deviceTable.item(index, 1) != None):
                    if (self.ui.deviceTable.item(index, 1).text() == deviceInfo["GUID"]):
                        # save index of equals item
                        flag = index
            # if table don't contain this device
            if (flag == -1):
                if (deviceInfo != None):
                    self.errorInfo("append")
                    self.appendText(deviceInfo["Name"], deviceInfo["GUID"], deviceInfo["HardwareID"], deviceInfo["Manufacture"], deviceInfo["Provider"], deviceInfo["Description"], deviceInfo["sys file"], deviceInfo["Device Path"])
            else:
                # update device information (size)
                self.errorInfo("update'")
                self.updateRow(flag, deviceInfo)
        # checking ejecting devices
        for i in range(0, self.ui.deviceTable.rowCount()):
            if (self.ui.deviceTable.item(i, 1) != None):
                if (not (self.ui.deviceTable.item(i, 1).text() in nameList)):
                    # remove device from table
                    self.errorInfo("remove")
                    self.ui.deviceTable.removeRow(i)

    def connect(self):
        # getting selected row
        indexes = self.ui.deviceTable.selectionModel().selectedRows()
        for index in sorted(indexes):
            # eject selected device
            message = self.wifiAdapter.connect(self.ui.deviceTable.item(index.row(), 0).text())
            # print error message if can't eject device
            self.errorInfo(message)

    def ping(self):
        # getting selected row
        indexes = self.ui.deviceTable.selectionModel().selectedRows()
        for index in sorted(indexes):
            # eject selected device
            message = self.wifiAdapter.ping(self.ui.deviceTable.item(index.row(), 0).text())
            # print error message if can't eject device
            self.errorInfo(message)

    # print info about ejecting
    def errorInfo(self, message):
        if (message != None):
            print(message)
            self.ui.infoLabel.setText("info: " + message)

    # update information about input device
    def updateRow(self, row, wifiInfo):
        # creating new item
        item1 = QTableWidgetItem(wifiInfo["Name"])
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(wifiInfo["GUID"])
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(wifiInfo["HardwareID"])
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item4 = QTableWidgetItem(wifiInfo["Manufacture"])
        item4.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item5 = QTableWidgetItem(wifiInfo["Provider"])
        item5.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item6 = QTableWidgetItem(wifiInfo["Description"])
        item6.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item7 = QTableWidgetItem(wifiInfo["sys file"])
        item7.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item8 = QTableWidgetItem(wifiInfo["Device Path"])
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
    timer = QTimer()
    timer.timeout.connect(window.refreshDevices)
    timer.start(3600000)
    window.refreshDevices()
    sys.exit(app.exec_())
    exit()
