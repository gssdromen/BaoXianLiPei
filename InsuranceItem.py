# coding:UTF-8

class InsuranceItem():
    """docstring for InsuranceItem"""
    def __init__(self, index, apply_num, rtnum, applyer, insurance_date, insurance_id, accident_type, claim_amount, express_num, express_date, status, supporter=''):
        # super(ResultItem, self).__init__()
        self.index = index
        self.apply_num = apply_num
        self.rtnum = rtnum
        self.applyer = applyer
        self.insurance_date = insurance_date
        self.insurance_id = insurance_id
        self.accident_type = accident_type
        self.claim_amount = claim_amount
        self.express_num = express_num
        self.express_date = express_date
        self.status = status
        self.supporter = supporter

    def __str__(self):
        return '%s:%s' % (self.apply_num.encode('gbk'), self.applyer.encode('gbk'))
