# coding:UTF-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui  import *
from PyQt4.QtCore  import *
from InsuranceItem import InsuranceItem
import View2
import SocketServer
import threading
import time
import codecs
import utils
import sqlite3


class Receiver(QThread):
    def run(self):
        HOST, PORT = utils.get_local_ip(), 8001

        # Create the server, binding to localhost on port 9999
        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        item = utils.get_insurance_from_json(data)
        utils.save_insurance_to_database(item)
        self.request.sendall('success')

class Refresher(QThread):
    def run(self):
        while True:
            result = []
            for row in self.database.execute('SELECT * FROM Insurances WHERE isDone = 0'):
                result.append(InsuranceItem(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            self.emit(SIGNAL("update_ui(PyQt_PyObject)"), result)
            time.sleep(3)

class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.ui = View2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(u'保险理赔处理')
        self.ui.act_cleardb.triggered.connect(self.clear_db)
        self.ui.act_clearlog.triggered.connect(self.clear_log)
        self.ui.btn_finish.clicked.connect(self.mark_done)
        self.ui.table_insurances.cellClicked.connect(self.copy)
        utils.init_database("date2.db")
        self.receiver = Receiver()
        self.refresher = Refresher()
        self.connect(self.refresher, QtCore.SIGNAL("update_ui(PyQt_PyObject)"), self.updateIt)
        self.receiver.start()
        self.refresher.start()

    def copy(self):
        row = self.ui.table_insurances.currentRow()
        apply_id = str(self.ui.table_insurances.item(row, 0).text())
        QtGui.QApplication.clipboard().setText(apply_id)

    def mark_done(self):
        row = self.ui.table_insurances.currentRow()
        item = self.insurances.pop(row)
        # apply_num = str(self.ui.table_insurances.item(row, 4).text())
        # insurance_id = str(self.ui.table_insurances.item(row, 0).text())
        utils.mark_done(item)
        self.ui.table_insurances.removeRow(row)

    def clear_db(self):
        utils.clear_db()

    def clear_log(self):
        self.database.execute("UPDATE Insurances SET isDone = 1")
        self.database.commit()
        self.ui.table_insurances.clear()

    def updateIt(self, insurances):
        self.insurances = insurances
        self.showIt()

    def showIt(self):
        insurances = self.insurances
        # 从这里开始改
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
