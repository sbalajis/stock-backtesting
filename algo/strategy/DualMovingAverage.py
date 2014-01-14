from zipline.algorithm import TradingAlgorithm
from zipline.transforms import MovingAverage, batch_transform

class DualMovingAverage(TradingAlgorithm):
    """Dual Moving Average Crossover algorithm.

    This algorithm buys apple once its short moving average crosses
    its long moving average (indicating upwards momentum) and sells
    its shares once the averages cross again (indicating downwards
    momentum).

    """
    def initialize(self, symbol):
        # Add 2 mavg transforms, one with a long window, one
        # with a short window.
        self.add_transform(MovingAverage, 'short_mavg', ['price'],
                           window_length=50)

        self.add_transform(MovingAverage, 'long_mavg', ['price'],
                           window_length=200)

        # To keep track of whether we invested in the stock or not
        self.invested = False

        self.symbol = symbol
        self.short_mavg = []
        self.long_mavg = []
        self.buy_orders = []
        self.sell_orders = []

    def handle_data(self, data):
        if (data[self.symbol].short_mavg['price'] > data[self.symbol].long_mavg['price']) and not self.invested:
            self.order(self.symbol, 200)
            self.invested = True
            self.buy_orders.append(data[self.symbol].datetime)
            print "{dt}: Buying 100 {symbol} shares.".format(dt=data[self.symbol].datetime, symbol=self.symbol)
        elif (data[self.symbol].short_mavg['price'] < data[self.symbol].long_mavg['price']) and self.invested:
            self.order(self.symbol, -200)
            self.invested = False
            self.sell_orders.append(data[self.symbol].datetime)
            print "{dt}: Selling 100 {symbol} shares.".format(dt=data[self.symbol].datetime, symbol=self.symbol)

        # Save mavgs for later analysis.
        self.short_mavg.append(data[self.symbol].short_mavg['price'])
        self.long_mavg.append(data[self.symbol].long_mavg['price'])