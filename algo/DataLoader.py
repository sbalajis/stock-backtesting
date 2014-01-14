import os
import datetime
from datetime import date

import pandas as pd
from zipline.utils.factory import load_from_yahoo

class DataLoader:
    def __init__(self, path=None):
        self.data = None
        self.path = path

    def load_symbols(self, name, symbols=['AAPL','FB','CSCO','INTC'], start=None, end=None):
        start = start or date.today() - datetime.timedelta(days=1*365)
        end   = end   or date.today()
        name  = "%s%s" % (self.path, name)
        print "Loading %s from %s to %s into %s" % (",".join(symbols), start, end, name)
        if os.path.isfile(name):
            self.data = pd.read_pickle(name)
        else:
            self.data = load_from_yahoo(stocks=symbols, start=start, end=end)
            self.data.to_pickle(name)
        return self.data
