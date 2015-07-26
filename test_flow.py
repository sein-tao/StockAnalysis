# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:25:37 2015

@author: xuyu
"""
import unittest
import os
from parse_flow import parse_tdx_flow
from pprint import pprint



class dumpTest(unittest.TestCase):
    def setUp(self):
        datadir="D:\Personal\Finnance\Stock\Flow"
        tmpfile = "tmp/dump"
        flow = parse_tdx_flow(os.path.join(datadir, 'flow201405.xls'))
        #pprint(flow)
        self.data = flow
        self.dumpfile = tmpfile
    def test_pickle(self):
        import pickle
        pickle.dump(self.data, open(self.dumpfile, 'wb'))
        pick = pickle.load(open(self.dumpfile,'rb'))
        self.assertEqual(pick, self.data)
        
#import json
        
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    tests = unittest.TestLoader().loadTestsFromTestCase(dumpTest)
    suite = unittest.TestSuite(tests)
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(dumpTest))
    #suite.addTest(dumpTest('test_pickle'))
    runner.run(suite)
