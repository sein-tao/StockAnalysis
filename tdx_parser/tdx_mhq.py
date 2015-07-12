# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 21:11:56 2015

@author: xuyu
"""

import numpy as np
import pandas as pd
import os

data_base = "E:/Stock/tdx/data"
data_dir = os.path.join(data_base,"yxhj/g2_day/")
mhq, ref = [],[]
for dirpath, subdir, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".mhq"):
            mhq.append(os.path.getsize(os.path.join(dirpath,file)))
        elif file.endswith(".ref"):
            ref.append(os.path.getsize(os.path.join(dirpath,file)))
#print mhq
#print ref

import fractions
mhq_u = reduce(fractions.gcd, mhq)
ref_u = reduce(fractions.gcd, ref)
print mhq_u, ref_u


import struct
up = struct.unpack_from
mhq_file = os.path.join(data_dir, "sz150112.mhq")
ref_file = os.path.join(data_dir, "sz150112.ref")
rf = open(ref_file, 'rb')
#"6cff"
mf = open(mhq_file, 'rb')
t = mf.read(mhq_u * 1000)
mdata = [mf.read(mhq_u) for i in xrange(100)]
t = rf.read(ref_u * 1000)
rdata = [rf.read(ref_u) for i in xrange(100)]
r = rdata[0]

m = mdata[0]
up("6cff",r)
up("6cfffff",r)
up('ifffff',m)


