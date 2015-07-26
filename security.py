# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:48:41 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

def account2market(account):
    if account.startswith('A'):
        return 'SH'
    elif account.startswith('0'):
        return 'SZ'
    else:
        return None

# import re
#def dzh2Security(dzh_id):
#    market, code = dzh_id[0:2], dzh_id[2:]
#    if market == 'SH':
#        market = 'SS'
#    return Security(code, market)     
    
class Security:

    def __init__(self, code, market=None, name=None):
        if not isinstance(code, str): #basestring for str and unicode
            raise TypeError("code should be string")
        code = code.upper()
        if code.startswith("S") and market is None:
            self.market = code[0:2]
            self.code = code[2:]
            self.name = name
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
            self.market = 'SH'
        else:
            self.market = None

    # IMPORTANT: __hash__ is used for indexing,
    # so it should be self defined for index-able type
    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        return "%s%s %s" % (self.market, self.code, self.name)
    
    def symbol(self):
        return "%s%s" % (self.market, self.code)
        

    def __repr__(self):
        return self.__class__.__name__ + "(%s)" % self.__str__()

    def __eq__(self, other):
        if isinstance(other, str):
            other = self.__class__(other)
        if isinstance(other, self.__class__):
            return self.market == other.market and self.code == other.code
        else:
            return False


    # not used in this version
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
                self.assertEqual(stock, Security("".join((market, code))))
                self.assertEqual(stock, Security(stock.symbol()))
                #self.assertRaises(TypeError,stock.__eq__, 0)
                self.assertNotEqual(stock, 0)
#        def test_dzh2security(self):
#            code, market, name = ["002230", 'SZ', "科大讯飞"]
#            self.assertEqual(dzh2Security(market+code), Security(code,market, name))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(unittest.makeSuite(Test))

