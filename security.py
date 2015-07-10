# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:48:41 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

def account2market(account):
    if account.startswith('A'):
        return 'SS'
    elif account.startswith('0'):
        return 'SZ'
    else:
        return None

class Security(object):
    def __init__(self, code, market=None, name=None):
        if not isinstance(code, str): #basestring for str and unicode
            raise TypeError("code should be string")
        if self.__class__._like_rep(code):
            self.__init__(*self.__class__._rep_to_arg(code))
        else:
            self.code = code
            self.market = market
            self.name = name
            if self.market is None:
                self.infer_market()

    def infer_market(self):
        if self.code[0] in ['0', '1', '3']:
            self.market = 'SZ'
        elif self.code[0] in ['6','7']:
            self.market = 'SS'
        else:
            self.market = None

    # IMPORTANT: __hash__ is used for indexing,
    # so it should be self defined for index-able type
    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        return "%s.%s %s" % (self.code, self.market, self.name)

    def __repr__(self):
        return self.__class__.__name__ + "(%s)" % self.__str__()

    def __eq__(self, other):
        if isinstance(other, str):
            other = self.__class__(other)
        return self.market == other.market and self.code == other.code

    @staticmethod
    def _like_rep(s):
        return "." in s
    @staticmethod
    def _rep_to_arg(s):
        return s.strip().replace("."," ").split(" ",2)

if __name__ == '__main__':
    import unittest
    class Test(unittest.TestCase):
        def test_security(self):
                code, market, name = ["002230", 'SZ', "科大讯飞"]
                stock = Security(code, market, name)
                self.assertEqual(stock.name, "科大讯飞")
                self.assertEqual(stock, code)
                self.assertEqual(stock, Security(code))
                self.assertEqual(stock, Security(".".join((code, market))))
                self.assertEqual(stock, Security(str(stock)))
    #unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(Test))

    unittest.main(verbosity=2, exit=False)

#    code, market, name = ["002230", 'SZ', "科大讯飞"]
#    stock = Security(code, market, name)
#    print("str:\t", stock)
#    print("repr:\t", repr(stock))
#    print("equal to code:",  stock == code)
#    print("init from code:", stock == Security(code))
#    print("init from mark:", stock == Security(code + "." + market))
#    print("init from str", stock == Security(str(stock)))
