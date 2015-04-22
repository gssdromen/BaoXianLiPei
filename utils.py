# coding:UTF-8
from Constants import Constants
from InsuranceItem import InsuranceItem
from SupportPeople import SupportPeople
from bs4 import BeautifulSoup
import codecs
import json
import sqlite3

constants = Constants()
database = sqlite3.connect("date.db")

def init_database():
    # 读取数据库
    database.execute("CREATE TABLE IF NOT EXISTS Insurances(ID INTEGER PRIMARY KEY AUTOINCREMENT, applyNum TEXT, rtnum TEXT, applyer TEXT, insuranceDate TEXT, insuranceId TEXT UNIQUE, accidentType TEXT, claimAmount TEXT, expressNum TEXT UNIQUE, expressDate TEXT, status TEXT, supporter TEXT)")
    database.commit()

def get_insurances_from_database():
    database.execute('SELECT * FROM Insurances')
    database.commit()

def save_insurance_to_database(item):
    database.execute("INSERT INTO Insurances VALUES (null, ?,?,?,?,?,?,?,?,?,?,?)", (item.apply_num, item.rtnum, item.applyer, item.insurance_date, item.insurance_id, item.accident_type, item.claim_amount, item.express_num, item.express_date, item.status, item.supporter))
    database.commit()

def get_json_from_insurance(item):
    dic = {}
    dic['index'] = item.index.encode('UTF-8')
    dic['apply_num'] = item.apply_num.encode('UTF-8')
    dic['rtnum'] = item.rtnum.encode('UTF-8')
    dic['applyer'] = item.applyer.encode('UTF-8')
    dic['insurance_date'] = item.insurance_date.encode('UTF-8')
    dic['insurance_id'] = item.insurance_id.encode('UTF-8')
    dic['accident_type'] = item.accident_type.encode('UTF-8')
    dic['claim_amount'] = item.claim_amount.encode('UTF-8')
    dic['express_num'] = item.express_num.encode('UTF-8')
    dic['express_date'] = item.express_date.encode('UTF-8')
    dic['status'] = item.status.encode('UTF-8')
    return get_json_from_dict(dic)

def get_json_from_dict(dic):
    return json.dumps(dic, ensure_ascii=False)

def get_dict_from_json(s):
    return json.loads(s)

def get_supporters():
    result = []
    with codecs.open('support.ini', 'r', encoding='UTF-8') as f:
        for line in f:
            temp = line.split('|')
            people = SupportPeople(temp[0], temp[1])
            result.append(people)
    return result

def get_insuranceitems_from_html(html):
    # return BeautifulSoup(httpHelper.sendRequest('post', constants.baseurl+"/vfs2/innerpage/loanafterportlet/insurClaimApprovedQueryList.html", dic))
    page = 1
    '?applyId=&applyer=&appStartDate=%s&imsauthFuncCode=LAB_ISCAQC&approvedEndDate=&afwBpId=&d-7248057-p=%d&spouseName=&afwBpName=&lisencePlate=&approvedStartDate=&vinCode=&isMailing=&certNo=&appEndDate=&contractID=&insurClaimStat=Submit' % ('20150422', page)
    result = []
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
    return result

def do_search(httpHelper):
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

    ?applyId=&applyer=&appStartDate=20150422&imsauthFuncCode=LAB_ISCAQC&approvedEndDate=&afwBpId=&d-7248057-p=2&spouseName=&afwBpName=&lisencePlate=&approvedStartDate=&vinCode=&isMailing=&certNo=&appEndDate=&contractID=&insurClaimStat=Submit


def get_cookies(httpHelper):
    fileHandle = open('acc.txt', 'r')
    line = fileHandle.readline()
    aList = line.split('|')
    dic = {}
    dic["loginName"] = aList[0]
    dic["password"] = aList[1]
    html = BeautifulSoup(httpHelper.sendRequest('post', constants.baseurl+"/vfs2/login.html", dic))
    print html.find('title').text.encode('UTF-8')
