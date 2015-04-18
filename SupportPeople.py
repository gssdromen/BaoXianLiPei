# coding:UTF-8

class SupportPeople():
    """docstring for InsuranceItem"""
    def __init__(self, name, ip):
        # super(ResultItem, self).__init__()
        self.name = name
        self.ip = ip

    def __str__(self):
        return '%s:%s' % (self.name.encode('gbk'), self.ip.encode('gbk'))
