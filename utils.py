# coding:UTF-8
from Constants import Constants
from InsuranceItem import InsuranceItem
from SupportPeople import SupportPeople
from bs4 import BeautifulSoup
import codecs

constants = Constants()

def get_supporters():
    result = []
    with codecs.open('support.ini', 'r', encoding='UTF-8') as f:
        for line in f:
            temp = line.split('|')
            people = SupportPeople(temp[0], temp[1])
            result.append(people)
    return result

def get_insuranceitems_from_html(html):
    result = []
    insuContactList = html.find(id='insuContactList')
    tbody = insuContactList.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        index = tds[1].text.strip()
        apply_num = tds[3].text.strip()
        rtnum = tds[4].find('div').text.strip()
        applyer = tds[5].text.strip()
        insurance_date = tds[6].text.strip()
        insurance_id = tds[7].text.strip()
        accident_type = tds[8].text.strip()
        claim_amount = tds[9].text.strip()
        express_num = tds[10].text.strip()
        exxpress_date = tds[11].text.strip()
        status  = tds[12].text.strip()
        insurance_item = InsuranceItem(index, apply_num, rtnum, applyer, insurance_date, insurance_id, accident_type, claim_amount, express_num, exxpress_date, status)
        result.append(insurance_item)
    return result

def do_search(httpHelper):
    dic = {}
    dic['applyId'] = ''
    dic['contractID'] = ''
    dic['applyer'] = ''
    dic['vinCode'] = ''
    dic['spouseName'] = ''
    dic['certNo'] = ''
    # 经销商代码和名字
    dic['afwBpId'] = ''
    dic['afwBpName'] = ''
    # 理赔申请状态
    dic['insurClaimStat'] = ''
    # 申请时间
    dic['appStartDate'] = '20150417'
    dic['appEndDate'] = ''
    # 牌照号码
    dic['lisencePlate'] = ''
    # 审核通过日期
    dic['approvedStartDate'] = ''
    dic['approvedEndDate'] = ''
    # 是否邮寄
    dic['isMailing'] = ''
    return BeautifulSoup(httpHelper.sendRequest('post', constants.baseurl+"/vfs2/innerpage/loanafterportlet/insurClaimApprovedQueryList.html", dic))

def get_cookies(httpHelper):
    fileHandle = open('acc.txt', 'r')
    line = fileHandle.readline()
    aList = line.split('|')
    dic = {}
    dic["loginName"] = aList[0]
    dic["password"] = aList[1]
    html = BeautifulSoup(httpHelper.sendRequest('post', constants.baseurl+"/vfs2/login.html", dic))
    print html.find('title').text.encode('UTF-8')
