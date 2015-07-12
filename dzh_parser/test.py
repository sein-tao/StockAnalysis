#!/usr/bin/env python

#import dzh

from struct import unpack
import numpy as np
import datetime
class DzhDividend(object):
    '''大智慧除权数据'''
    # _PATH = '/platform/download/PWR/full.PWR'
    def __init__(self, path):
        self.f = open(path, 'rb')
        self._fetched = True


    def read(self):
        """Generator of 大智慧除权数据
        分红送股均为每股数据
        
        Example of yield data:
    
        symbol: 'SZ000001'
        dividends: [{ :date_ex_dividend => '1992-03-23',
                      :split => 0.500,
                      :purchase => 0.000,
                      :purchase_price => 0.000,
                      :dividend => 0.200 }... ]
        """

        
        # skip head
        self.f.seek(12, 0)

        try:
            while True:
                yield self._read_symbol()
        except EOFError:
            raise StopIteration
        finally:
            self.f.close()
        #except Exception as e:
        #    print(e)

    def _read_symbol(self):
        dividends = []

        rawsymbol = self.f.read(16)
        if rawsymbol == b'':
            raise EOFError
        
        symbol = unpack('16s', rawsymbol)[0].replace(b'\x00', b'')

        rawdate = self.f.read(4)

        dt = np.dtype([('time', np.int32),
                       ('split', np.float32),
                       ('purchase', np.float32),
                       ('purchase_price', np.float32),
                       ('dividend', np.float32)])
        while (rawdate) != b"\xff" * 4:
            dividend = np.frombuffer(rawdate + self.f.read(16), dtype=dt)
            dividends.append(dividend)
            
            rawdate = self.f.read(4)
            if rawdate == b'':
                break

        return (symbol, np.fromiter(dividends, dtype=dt))

date = datetime.datetime.fromtimestamp

if __name__ == '__main__':
    file = "../test_data/full.PWR"
    data = DzhDividend(file)

    f = open(file, 'rb')
    f.seek(12, 0)
    rawsymbol = f.read(16)
    if rawsymbol == '':
            raise EOFError
    symbol = unpack('16s', rawsymbol)[0].replace(b'\x00', b'')
    print(symbol)
    dtype = np.dtype([('time', np.int32),
               ('split', np.float32),
               ('purchase', np.float32),
               ('purchase_price', np.float32),
               ('dividend', np.float32)])
    rawdate = f.read(4)
    dividend = np.frombuffer(rawdate + f.read(16), dtype=dtype)
    date = datetime.datetime.fromtimestamp(dividend[0][0])
    print(dividend, date)
    """
    m = data.read()
    print(next(m))
    #for d in data.read():
    #    print(d)
    
    """

    