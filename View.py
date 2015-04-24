# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'View.ui'
#
# Created: Fri Apr 24 16:27:26 2015
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(830, 726)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.box_supporters = QtGui.QComboBox(self.centralwidget)
        self.box_supporters.setObjectName(_fromUtf8("box_supporters"))
        self.gridLayout.addWidget(self.box_supporters, 0, 7, 1, 1)
        self.btn_distribute = QtGui.QPushButton(self.centralwidget)
        self.btn_distribute.setObjectName(_fromUtf8("btn_distribute"))
        self.gridLayout.addWidget(self.btn_distribute, 0, 8, 1, 1)
        self.date_start = QtGui.QDateEdit(self.centralwidget)
        self.date_start.setObjectName(_fromUtf8("date_start"))
        self.gridLayout.addWidget(self.date_start, 0, 0, 1, 1)
        self.table_insurances = QtGui.QTableWidget(self.centralwidget)
        self.table_insurances.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_insurances.setObjectName(_fromUtf8("table_insurances"))
        self.table_insurances.setColumnCount(0)
        self.table_insurances.setRowCount(0)
        self.gridLayout.addWidget(self.table_insurances, 1, 0, 1, 10)
        self.date_end = QtGui.QDateEdit(self.centralwidget)
        self.date_end.setObjectName(_fromUtf8("date_end"))
        self.gridLayout.addWidget(self.date_end, 0, 1, 1, 1)
        self.btn_refresh = QtGui.QPushButton(self.centralwidget)
        self.btn_refresh.setObjectName(_fromUtf8("btn_refresh"))
        self.gridLayout.addWidget(self.btn_refresh, 0, 9, 1, 1)
        self.btn_export = QtGui.QPushButton(self.centralwidget)
        self.btn_export.setObjectName(_fromUtf8("btn_export"))
        self.gridLayout.addWidget(self.btn_export, 0, 4, 1, 1)
        self.label_status = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy)
        self.label_status.setObjectName(_fromUtf8("label_status"))
        self.gridLayout.addWidget(self.label_status, 0, 5, 1, 1, QtCore.Qt.AlignRight)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 6, 1, 1)
        self.box_status = QtGui.QComboBox(self.centralwidget)
        self.box_status.setObjectName(_fromUtf8("box_status"))
        self.box_status.addItem(_fromUtf8(""))
        self.box_status.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.box_status, 0, 2, 1, 1)
        self.box_is_express = QtGui.QComboBox(self.centralwidget)
        self.box_is_express.setObjectName(_fromUtf8("box_is_express"))
        self.box_is_express.addItem(_fromUtf8(""))
        self.box_is_express.addItem(_fromUtf8(""))
        self.box_is_express.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.box_is_express, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.act_cleardb = QtGui.QAction(MainWindow)
        self.act_cleardb.setObjectName(_fromUtf8("act_cleardb"))
        self.act_clearlog = QtGui.QAction(MainWindow)
        self.act_clearlog.setObjectName(_fromUtf8("act_clearlog"))
        self.menu.addAction(self.act_cleardb)
        self.menu.addAction(self.act_clearlog)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_distribute.setText(_translate("MainWindow", "分配", None))
        self.btn_refresh.setText(_translate("MainWindow", "刷新", None))
        self.btn_export.setText(_translate("MainWindow", "导出", None))
        self.label_status.setText(_translate("MainWindow", "TextLabel", None))
        self.box_status.setItemText(0, _translate("MainWindow", "所有", None))
        self.box_status.setItemText(1, _translate("MainWindow", "提交", None))
        self.box_is_express.setItemText(0, _translate("MainWindow", "所有", None))
        self.box_is_express.setItemText(1, _translate("MainWindow", "邮寄-否", None))
        self.box_is_express.setItemText(2, _translate("MainWindow", "邮寄-是", None))
        self.menu.setTitle(_translate("MainWindow", "菜单", None))
        self.act_cleardb.setText(_translate("MainWindow", "清空分配记录", None))
        self.act_clearlog.setText(_translate("MainWindow", "清空我的操作记录", None))

