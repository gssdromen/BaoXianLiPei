# coding:UTF-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui  import *
from PyQt4.QtCore  import *
import View
from Constants import Constants
from xlwt.Workbook import *
import xlrd
import os
import shutil
import codecs
import time
import sys
import re
import urllib
import urllib2
import cookielib
import HTMLParser
import HttpHelper
import webbrowser
from bs4 import BeautifulSoup
import time
import utils


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.ui = View.Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始化httpHelper
        self.http = HttpHelper.HttpHelper()
        self.constants = Constants()
        # 得到操作者
        self.supporters = utils.get_supporters()
        # 得到Cookies
        utils.get_cookies(self.http)
        self.showIt(utils.get_insuranceitems_from_html(utils.do_search(self.http)))

    def showIt(self, insurances):
        labels = [u'序号', u'申请编号', u'合同号', u'申请人', u'出险日期', u'报案号', u'事故类型', u'理赔金额', u'快递单号', u'邮寄日起', u'状态', u'分配人']
        # self.ui.table_insurances.setColumnWidth(2, 200)
        self.ui.table_insurances.setColumnCount(len(labels))
        self.ui.table_insurances.setRowCount(len(insurances))
        self.ui.table_insurances.setHorizontalHeaderLabels(labels)
        for row in xrange(len(insurances)):
            self.ui.table_insurances.setItem(row, 0, QTableWidgetItem(insurances[row].index))
            self.ui.table_insurances.setItem(row, 1, QTableWidgetItem(insurances[row].apply_num))
            self.ui.table_insurances.setItem(row, 2, QTableWidgetItem(insurances[row].rtnum))
            self.ui.table_insurances.setItem(row, 3, QTableWidgetItem(insurances[row].applyer))
            self.ui.table_insurances.setItem(row, 4, QTableWidgetItem(insurances[row].insurance_date))
            self.ui.table_insurances.setItem(row, 5, QTableWidgetItem(insurances[row].insurance_id))
            self.ui.table_insurances.setItem(row, 6, QTableWidgetItem(insurances[row].accident_type))
            self.ui.table_insurances.setItem(row, 7, QTableWidgetItem(insurances[row].claim_amount))
            self.ui.table_insurances.setItem(row, 8, QTableWidgetItem(insurances[row].express_num))
            self.ui.table_insurances.setItem(row, 9, QTableWidgetItem(insurances[row].exxpress_date))
            self.ui.table_insurances.setItem(row, 10, QTableWidgetItem(insurances[row].status))
            charge_person_chooser = QComboBox()
            for item in self.supporters:
                charge_person_chooser.addItem(item.name)
            self.ui.table_insurances.setCellWidget (row, 11, charge_person_chooser)
        # self.ui.table_insurances.resizeColumnsToContents()


def main():
    app = QtGui.QApplication([])
    ex = Example()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
