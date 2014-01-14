#!/usr/bin/env python

import datetime
import sys
sys.path.append('.')
sys.path.append('..')

from algo.strategy.DualMovingAverage import DualMovingAverage
from algo.DataLoader import DataLoader

import matplotlib.pyplot as plt

dl = DataLoader()
data = dl.load_symbols('stocks.dat', start=datetime.date(2012, 8, 1))

symbol = 'AAPL'
dma = DualMovingAverage(symbol)
results = dma.run(data)

ax1 = plt.subplot(311)
data['short'] = dma.short_mavg
data['long'] = dma.long_mavg
data[[symbol, 'short', 'long']].plot(ax=ax1)
plt.plot(dma.buy_orders, data['short'].ix[dma.buy_orders], '^', c='m', markersize=10, label='buy')
plt.plot(dma.sell_orders, data['short'].ix[dma.sell_orders], 'v', c='k', markersize=10, label='sell')
plt.legend(loc=0)

ax2 = plt.subplot(312)
results.portfolio_value.plot(ax=ax2, figsize=(18,12))

ax3 = plt.subplot(313)
data[symbol].plot(ax=ax3, figsize=(18,12))

plt.show()
