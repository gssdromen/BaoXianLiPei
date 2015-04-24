# coding:UTF-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui  import *
from PyQt4.QtCore  import *
from InsuranceItem import InsuranceItem
import View
import SocketServer
import threading
import time
import codecs
import utils


class Receiver(QThread):
    def run(self):
        # global count, mutex
        threadname = threading.currentThread().getName()

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
        self.request.sendall('success')
        with codecs.open('log.log', 'a') as f:
            f.write(data + '\n')
        # insurance = utils.get_insurance_from_json(self.data)
        # self.emit(SIGNAL("update_ui(QString)"), data)
        # print "{} wrote:".format(self.client_address[0])
        # print self.data
        # print utils.get_insurance_from_json(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())


class Refresher(QThread):
    def run(self):
        while True:
            l = QStringList()
            with codecs.open('log.log', 'r', encoding='UTF-8') as f:
                for line in f:
                    l.insert(0, QString.fromUtf8(line.strip()))
            self.emit(SIGNAL("update_ui(QStringList)"), l)
            time.sleep(3)

class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.ui = View.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(u'保险理赔处理')
        self.ui.act_cleardb.triggered.connect(self.clear_db)
        self.ui.act_clearlog.triggered.connect(self.clear_log)
        self.receiver = Receiver()
        self.refresher = Refresher()
        self.connect(self.refresher, SIGNAL("update_ui(QStringList)"), self.showIt)
        self.receiver.start()
        self.refresher.start()

    def clear_db(self):
        utils.clear_db()

    def clear_log(self):
        utils.clear_log()

    def showIt(self, l):
        insurances = []
        for string in l:
            # print string.toLocal8Bit().__str__
            insurances.append(utils.get_insurance_from_json(unicode(string)))
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
