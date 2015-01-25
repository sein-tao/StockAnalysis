# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:48:41 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

class Security:
    def __init__(self, code, name=None, market=None):
        self.code = code
        self.name = name
        self.market = market
        if self.market == None:
            self.infer_market()

    def infer_market(self):
        if self.code[0] in ['0', '1', '3']:
            self.market = 'SZ'
        elif self.code[0] in ['6','7']:
            self.market = 'SS'
        else:
            self.market = ''

    def __str__(self):
        return self.code + "." + self.market + " " + self.name






