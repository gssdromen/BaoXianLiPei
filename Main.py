# coding:UTF-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui  import *
from PyQt4.QtCore  import *
import View
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
        self.setWindowTitle(u'保险理赔分发')
        # 得到今天日期
        self.today = QDate.currentDate ()
        self.ui.date_start.setDate(self.today)
        self.ui.date_end.setDate(self.today)
        # 得到操作者
        self.supporters = utils.get_supporters()
        # 注入操作者
        for item in self.supporters:
            self.ui.box_supporters.addItem(item.name)
        self.insurances = []
        # 初始化数据库
        utils.init_database()
        # 得到Cookies
        utils.get_cookies()
        # 绑定信号槽
        self.ui.btn_refresh.clicked.connect(self.refresh_data)
        self.ui.btn_distribute.clicked.connect(self.distribute_supporter)
        self.ui.btn_export.clicked.connect(self.export_log)
        self.ui.act_cleardb.triggered.connect(self.clear_db)
        self.ui.act_clearlog.triggered.connect(self.clear_log)

    def clear_db(self):
        utils.clear_db()

    def clear_log(self):
        utils.clear_log()

    def export_log(self):
        sdate = self.ui.date_start.date().toString('yyyyMMdd')
        edate = self.ui.date_end.date().toString('yyyyMMdd')
        if self.insurances:
            utils.export_to_excel(self.insurances, os.path.join(utils.get_desktop(),'%s-%s.xls' % (sdate, edate)))
            QtGui.QMessageBox.question(self, 'Message', u"导出成功", QtGui.QMessageBox.Yes)
        else:
            print u'请先刷新列表'.encode('UTF-8')
            self.show_status(u'请先刷新列表')

    def show_status(self, s):
        self.ui.label_status.setText(s)

    def distribute_supporter(self):
        self.show_status(u'')
        if not self.insurances:
            print u'请先刷新列表'.encode('UTF-8')
            self.show_status(u'请先刷新列表')
            return
        index = self.ui.box_supporters.currentIndex()
        supporter = self.supporters[index]
        row = self.ui.table_insurances.currentRow()
        insurance_item = self.insurances[row]
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print supporter.ip.strip()
            self.socket.connect((supporter.ip.strip(), 8001))
        except Exception, e:
            print u'操作者未上线'.encode('UTF-8')
            self.show_status(u'操作者未上线')
            print e
        else:
            self.socket.send(utils.get_json_from_insurance(insurance_item).encode('UTF-8'))
            re = self.socket.recv(1024)
            print re
            if re == 'success':
                # 把当前row的操作者改掉
                self.ui.table_insurances.setItem(row, 10, QTableWidgetItem(supporter.name))
                insurance_item.supporter = supporter.name
                # 分配记录存入数据库
                utils.save_insurance_to_database(insurance_item)
        finally:
            self.socket.close()

    def merge_net_and_local(self, net, local):
        result = []
        # for item in net:
        #     print item.apply_num
        for net_item in net:
            flag = False
            for local_item in local:
                if net_item.insurance_id == local_item.insurance_id:
                    result.append(local_item)
                    flag = True
                if local_item.apply_num == '491451':
                    print 'net:'+net_item.insurance_id
                    print 'local:'+local_item.insurance_id
            if not flag:
                result.append(net_item)
        return result

    def refresh_data(self):
        sdate = self.ui.date_start.date().toString('yyyyMMdd')
        edate = self.ui.date_end.date().toString('yyyyMMdd')
        if self.ui.box_status.currentIndex() == 0:
            status = ''
        elif self.ui.box_status.currentIndex() == 1:
            status = 'Submit'
        if self.ui.box_is_express.currentIndex() == 0:
            is_express = ''
        elif self.ui.box_is_express.currentIndex() == 1:
            is_express = '0'
        elif self.ui.box_is_express.currentIndex() == 2:
            is_express = '1'
        net = utils.get_insuranceitems_from_html(sdate, edate, status, is_express)
        local = utils.get_insurances_from_database()
        self.insurances = self.merge_net_and_local(net, local)
        self.showIt(self.insurances)
        self.show_status(u'刷新完毕')

    def showIt(self, insurances):
        labels = [u'申请编号', u'合同号', u'申请人', u'出险日期', u'报案号', u'事故类型', u'理赔金额', u'快递单号', u'邮寄日期', u'状态', u'操作人']
        # self.ui.table_insurances.setColumnWidth(2, 200)
        self.ui.table_insurances.setColumnCount(len(labels))
        self.ui.table_insurances.setRowCount(len(insurances))
        self.ui.table_insurances.setHorizontalHeaderLabels(labels)
        for row in xrange(len(insurances)):
            # self.ui.table_insurances.setItem(row, 0, QTableWidgetItem(insurances[row].index))
            self.ui.table_insurances.setItem(row, 0, QTableWidgetItem(insurances[row].apply_num))
            self.ui.table_insurances.setItem(row, 1, QTableWidgetItem(insurances[row].rtnum))
            self.ui.table_insurances.setItem(row, 2, QTableWidgetItem(insurances[row].applyer))
            self.ui.table_insurances.setItem(row, 3, QTableWidgetItem(insurances[row].insurance_date))
            self.ui.table_insurances.setItem(row, 4, QTableWidgetItem(insurances[row].insurance_id))
            self.ui.table_insurances.setItem(row, 5, QTableWidgetItem(insurances[row].accident_type))
            self.ui.table_insurances.setItem(row, 6, QTableWidgetItem(insurances[row].claim_amount))
            self.ui.table_insurances.setItem(row, 7, QTableWidgetItem(insurances[row].express_num))
            self.ui.table_insurances.setItem(row, 8, QTableWidgetItem(insurances[row].express_date))
            self.ui.table_insurances.setItem(row, 9, QTableWidgetItem(insurances[row].status))
            self.ui.table_insurances.setItem(row, 10, QTableWidgetItem(insurances[row].supporter))
        # self.ui.table_insurances.resizeColumnsToContents()


def main():
    app = QtGui.QApplication([])
    ex = Example()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
