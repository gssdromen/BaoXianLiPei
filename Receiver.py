# coding:UTF-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui  import *
from PyQt4.QtCore  import *
from InsuranceItem import InsuranceItem
import View
import SocketServer
import threading
import time
import utils


class Receiver(QThread):
    def __init__(self):
        threading.Thread.__init__(self)
        # self._run_num = num

    def run(self):
        # global count, mutex
        threadname = threading.currentThread().getName()

        HOST, PORT = "localhost", 8001

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
        self.data = self.request.recv(1024).strip()
        insurance = utils.get_insurance_from_json(self.data)
        self.emit(SIGNAL("update_ui(InsuranceItem)"))
        # print "{} wrote:".format(self.client_address[0])
        # print self.data
        # print utils.get_insurance_from_json(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.ui = View.Ui_MainWindow()
        self.ui.setupUi(self)
        self.receiver = Receiver()
        self.connect(self.receiver, SIGNAL("update_ui(InsuranceItem)"), self.showIt)
        self.connect(self., Qt)

    def showIt(self, insurances):
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
