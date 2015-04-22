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
import socket
import sqlite3


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.ui = View.Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始化
        self.http = HttpHelper.HttpHelper()
        self.constants = Constants()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 得到操作者
        self.supporters = utils.get_supporters()
        # 注入操作者
        for item in self.supporters:
            self.ui.box_supporters.addItem(item.name)
        # 初始化数据库
        utils.init_database()
        # 得到Cookies
        utils.get_cookies(self.http)
        # 绑定信号槽
        self.ui.btn_refresh.clicked.connect(self.refresh_data)
        self.ui.btn_distribute.clicked.connect(self.distribute_supporter)

    def distribute_supporter(self):
        if not self.insurances:
            print u'请先刷新列表'
        index = self.ui.box_supporters.currentIndex()
        supporter = self.supporters[index]
        row = self.ui.table_insurances.currentRow()
        insurance_item = self.insurances[row]
        try:
            self.socket.connect((supporter.ip, 8001))
        except Exception, e:
            # print u'操作者未上线'.encode('gbk')
            pass
        else:
            self.socket.send(utils.get_json_from_insurance(insurance_item))
            # 把当前row的操作者改掉
            self.ui.table_insurances.setItem(row, 11, QTableWidgetItem(supporter.name))
            insurance_item.supporter = supporter.name
            # 分配记录存入数据库
            utils.save_insurance_to_database(insurance_item)
        finally:
            pass

    def merge_net_and_local(self):
        pass

    def refresh_data(self):
        self.insurances = utils.get_insuranceitems_from_html(self.http)
        # self.merge_net_and_local(insurances)
        self.showIt(self.insurances)

    def showIt(self, insurances):
        labels = [u'序号', u'申请编号', u'合同号', u'申请人', u'出险日期', u'报案号', u'事故类型', u'理赔金额', u'快递单号', u'邮寄日起', u'状态', u'操作人']
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
            self.ui.table_insurances.setItem(row, 9, QTableWidgetItem(insurances[row].express_date))
            self.ui.table_insurances.setItem(row, 10, QTableWidgetItem(insurances[row].status))
        # self.ui.table_insurances.resizeColumnsToContents()


def main():
    app = QtGui.QApplication([])
    ex = Example()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
