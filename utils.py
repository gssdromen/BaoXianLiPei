# coding:UTF-8
from Constants import Constants
from HttpHelper import HttpHelper
from InsuranceItem import InsuranceItem
from SupportPeople import SupportPeople
from bs4 import BeautifulSoup
import codecs
import json
import sqlite3
import datetime
import xlwt
import os
import _winreg
import socket

class Utils(object):
    constants = Constants()
    http = HttpHelper()

    def __init__(self):
        super(Utils, self).__init__()

    def clear_db(self):
        self.database.execute("DELETE FROM Insurances")
        self.database.commit()

    def clear_log(self):
        with open('log.log', 'w') as f:
            pass

    def get_desktop(self):
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Volatile Environment')
        return os.path.join(_winreg.QueryValueEx(key, "USERPROFILE")[0], 'Desktop')

    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())#得到本地ip

    def init_self.database(self, self.database_name):
        self.database = sqlite3.connect(self.database_name, check_same_thread = False)
        # 初始化数据库
        self.database.execute("CREATE TABLE IF NOT EXISTS Insurances(ID INTEGER PRIMARY KEY AUTOINCREMENT, applyNum TEXT, rtnum TEXT, applyer TEXT, insuranceDate TEXT, insuranceId TEXT UNIQUE, accidentType TEXT, claimAmount TEXT, expressNum TEXT, expressDate TEXT, status TEXT, supporter TEXT, updateAt DATE, isDone BOOLEAN)")
        self.database.commit()

    def get_insurances_from_self.database(self):
        result = []
        for row in self.database.execute('SELECT * FROM Insurances'):
            result.append(InsuranceItem(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        return result

    def get_undone_insurances_from_self.database(self):
        result = []
        for row in self.database.execute('SELECT * FROM Insurances WHERE isDone = 0'):
            result.append(InsuranceItem(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        return result

    def save_insurance_to_self.database(self, item):
        self.database.execute("INSERT INTO Insurances VALUES (null, ?,?,?,?,?,?,?,?,?,?,?,?,False)", (item.apply_num, item.rtnum, item.applyer, item.insurance_date, item.insurance_id, item.accident_type, item.claim_amount, item.express_num, item.express_date, item.status, item.supporter, datetime.date.today(),False))
        self.database.commit()

    def update_insurance_in_self.database(self, item):
        self.database.execute("UPDATE Insurances SET status=? WHERE insuranceId=? and applyNum=?",(item.status, item.insurance_id, item.apply_num))
        # self.database.execute("INSERT INTO Insurances VALUES (null, ?,?,?,?,?,?,?,?,?,?,?,?)", (item.apply_num, item.rtnum, item.applyer, item.insurance_date, item.insurance_id, item.accident_type, item.claim_amount, item.express_num, item.express_date, item.status, item.supporter, datetime.date.today()))
        self.database.commit()

    def mark_done(self, item):
        self.database.execute("UPDATE Insurances SET isDone = ? WHERE insuranceId = ? and applyNum = ?", (True, item.insurance_id, item.apply_num))
        self.database.commit()

    def export_to_excel(self, insurances, path):
        workbook = xlwt.Workbook(encoding = 'UTF-8')
        sheet = workbook.add_sheet(u'分配情况')
        labels = [u'申请编号', u'合同号', u'申请人', u'出险日期', u'报案号', u'事故类型', u'理赔金额', u'快递单号', u'邮寄日起', u'状态', u'操作人']
        for i in xrange(len(labels)):
            sheet.write(0, i, labels[i])
        line = 1
        for item in insurances:
            sheet.write(line, 0, item.apply_num)
            sheet.write(line, 1, item.rtnum)
            sheet.write(line, 2, item.applyer)
            sheet.write(line, 3, item.insurance_date)
            sheet.write(line, 4, item.insurance_id)
            sheet.write(line, 5, item.accident_type)
            sheet.write(line, 6, item.claim_amount)
            sheet.write(line, 7, item.express_num)
            sheet.write(line, 8, item.express_date)
            sheet.write(line, 9, item.status)
            sheet.write(line, 10, item.supporter)
            line += 1
        workbook.save(path)

    def get_insurance_from_json(self, s):
        dic = get_dict_from_json(s)
        insurance = InsuranceItem(dic['index'], dic['apply_num'], dic['rtnum'], dic['applyer'], dic['insurance_date'], dic['insurance_id'], dic['accident_type'], dic['claim_amount'], dic['express_num'], dic['express_date'], dic['status'])
        return insurance

    def get_json_from_insurance(self, item):
        dic = {}
        dic['index'] = item.index
        dic['apply_num'] = item.apply_num
        dic['rtnum'] = item.rtnum
        dic['applyer'] = item.applyer
        dic['insurance_date'] = item.insurance_date
        dic['insurance_id'] = item.insurance_id
        dic['accident_type'] = item.accident_type
        dic['claim_amount'] = item.claim_amount
        dic['express_num'] = item.express_num
        dic['express_date'] = item.express_date
        dic['status'] = item.status
        return get_json_from_dict(dic)

    def get_json_from_dict(self, dic):
        return json.dumps(dic, ensure_ascii=False)

    def get_dict_from_json(self, s):
        return json.loads(s)

    def get_supporters(self):
        result = []
        with codecs.open('support.ini', 'r', encoding='UTF-8') as f:
            for line in f:
                temp = line.strip().split('|')
                people = SupportPeople(temp[0], temp[1])
                result.append(people)
        return result

    def get_insuranceitems_from_html(self, sdate, edate, status_, is_express):
        result = []
        page = 1
        html = do_search(page, sdate, edate, status_, is_express)
        while not html.find(class_ = 'empty'):
            insuContactList = html.find(id='insuContactList')
            tbody = insuContactList.find('tbody')
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                index = unicode(tds[1].text.strip())
                apply_num = unicode(tds[3].text.strip())
                rtnum = unicode(tds[4].find('div').text.strip())
                applyer = unicode(tds[5].text.strip())
                insurance_date = unicode(tds[6].text.strip())
                insurance_id = unicode(tds[7].text.strip())
                accident_type = unicode(tds[8].text.strip())
                claim_amount = unicode(tds[9].text.strip())
                express_num = unicode(tds[10].text.strip())
                express_date = unicode(tds[11].text.strip())
                status  = unicode(tds[12].text.strip())
                insurance_item = InsuranceItem(index, apply_num, rtnum, applyer, insurance_date, insurance_id, accident_type, claim_amount, express_num, express_date, status)
                result.append(insurance_item)
            print 'page:%d' % (page)
            page += 1
            html = do_search(page, sdate, edate, status_, is_express)
        return result

    def do_search(self, page, sdate, edate, status, is_express):
        # dic = {}
        # dic['applyId'] = ''
        # dic['contractID'] = ''
        # dic['applyer'] = ''
        # dic['vinCode'] = ''
        # dic['spouseName'] = ''
        # dic['certNo'] = ''
        # # 经销商代码和名字
        # dic['afwBpId'] = ''
        # dic['afwBpName'] = ''
        # # 理赔申请状态
        # dic['insurClaimStat'] = ''
        # # 申请时间
        # dic['appStartDate'] = '20150422'
        # dic['appEndDate'] = ''
        # # 牌照号码
        # dic['lisencePlate'] = ''
        # # 审核通过日期
        # dic['approvedStartDate'] = ''
        # dic['approvedEndDate'] = ''
        # # 是否邮寄
        # dic['isMailing'] = ''
        # return BeautifulSoup(httpHelper.sendRequest('post', constants.baseurl+"/vfs2/innerpage/loanafterportlet/insurClaimApprovedQueryList.html", dic))
        get_pram = '?applyId=&applyer=&appStartDate=%s&imsauthFuncCode=LAB_ISCAQC&approvedEndDate=&afwBpId=&d-7248057-p=%d&spouseName=&afwBpName=&lisencePlate=&approvedStartDate=&vinCode=&isMailing=%s&certNo=&appEndDate=%s&contractID=&insurClaimStat=%s' % (sdate, page, is_express, edate, status)
        return BeautifulSoup(self.http.sendRequest('get', self.constants.baseurl+"/vfs2/innerpage/loanafterportlet/insurClaimApprovedQueryList.html" + get_pram))

    def get_cookies(self):
        fileHandle = open('acc.txt', 'r')
        line = fileHandle.readline()
        aList = line.split('|')
        dic = {}
        dic["loginName"] = aList[0]
        dic["password"] = aList[1]
        html = BeautifulSoup(self.http.sendRequest('post', self.constants.baseurl+"/vfs2/login.html", dic))
        print html.find('title').text.encode('UTF-8')
