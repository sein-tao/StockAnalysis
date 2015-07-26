# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:34:49 2015

@author: xuyu
"""
import datetime
from collections import namedtuple, defaultdict
import dzh
import sys
sys.path.append("..")
from security import Security
int2date = datetime.datetime.fromtimestamp

import pandas as pd

class DivRec(namedtuple('DividenedRecBase', 
            ['security', 'date', 'split', 'div', 'purchase', 'purchase_price'])):
    """ split, div, etc are per share, data in datetime.date format"""

                    

"""
        symbol: 'SZ000001'
        dividends: [{ :date_ex_dividend => '1992-03-23',
                      :split => 0.500,
                      :purchase => 0.000,
                      :purchase_price => 0.000,
                      :dividend => 0.200 }... ]
"""
def dzh2DivRec(dzh_rec):
    """convert function"""

    stamp2date = datetime.datetime.fromtimestamp
    sec = Security(dzh_rec[0])
    return [DivRec(sec,
                     stamp2date(rec[0]).date(),
                     rec[1], rec[4], rec[2], rec[3]
            ) for rec in dzh_rec[1]]

#def dzhDivParser(file):
#     return (rec for line in dzh.DzhDividend(file).read()
#        for rec in dzh2DivRec(line))

def parse_dzh_div(file):
    result = defaultdict(dict)
    for line in dzh.DzhDividend(file).read():
        for rec in dzh2DivRec(line):
            result[rec.security][rec.date] = rec
    return result

        
if __name__ == '__main__':
    from pprint import pprint
    file = "../test_data/full.PWR"
    for i, rec in parse_dzh_div(file).items():
        print(i)
        pprint(rec)
        break
        
    