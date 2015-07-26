# -*- coding: utf-8 -*-
"""
Dump tdx_flow files to pickle
Created on Sun Jul 26 18:51:24 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

import sys
sys.path.append("..")
import os
import pickle
import datetime
import dateutil.relativedelta
from parse_flow import parse_tdx_flow

datadir="D:\Personal\Finnance\Stock\Flow"

def dump_flow(month_start, month_end, outfile, datadir=datadir):
    """Dump tdx_flow files to pickle"""
    str2date = lambda x: datetime.datetime.strptime(x, '%Y%m')
    date2str = lambda x: datetime.datetime.strftime(x, '%Y%m')
    one_month = dateutil.relativedelta.relativedelta(months=1)
    start, end = str2date(month_start), str2date(month_end)
    if start > end:
        raise ValueError("start month should be less than end month")
    recs = []
    current = start
    while current <= end:
        file = os.path.join(datadir, 'flow'+date2str(current)+".xls")
        recs.extend(parse_tdx_flow(file))
        current += one_month
    with open(outfile, 'wb') as fh:
        pickle.dump(recs, fh)

 
        
if __name__ == '__main__':
    #data_file = os.path.join(datadir, '2014.pickle')
    #dump_flow('201405', '201412', data_file)    
    #data = pickle.load(open(data_file, 'rb'))
    import unittest
    class Test(unittest.TestCase):
        def test_dump(self):
            import filecmp
            data_file = os.path.join(datadir, '2014.pickle')
            tmp_file = "../tmp/flow.pickle"
            dump_flow('201405', '201412', tmp_file)
            self.assertTrue(filecmp.cmp(data_file, tmp_file))  
    from util import runTestCase
    runTestCase(Test)

    
    