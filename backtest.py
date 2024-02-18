import pandas as pd
from backtesting import Backtest, Strategy

from backtesting.test import GOOG
import math

class DCA(Strategy):
    amount_to_invest = 10
    def init(self):
        #print(self.data.Close.s.index.dayofweek)
        self.day_of_week = self.I(
            lambda x:x,
            self.data.Close.s.index.dayofweek, 
            plot = False,
        )
    def next(self):
       if self.day_of_week[-1] == 1: #tuesday - buy signal on closing price
            self.buy(size = math.floor(self.amount_to_invest / self.data.Close[-1]))
            if len(self.data.Close > 30): # if the price had gone down by more than 6 percent in the past month, buy by the same amount
                if self.data.Close[-1]/self.data.Close[-3]<0.95:
                    self.buy(size = math.floor(self.amount_to_invest / self.data.Close[-1]))
       #print(len(self.data.Close[-1]))



print(GOOG)

GOOG = GOOG * 10**-6

bt = Backtest(
    GOOG, 
    DCA, 
    trade_on_close = True,
)

stats = bt.run()
bt.plot()
print(stats)
trades = stats["_trades"]
price_paid = trades["Size"]  * trades["EntryPrice"]
total_invested = price_paid.sum()

current_shares = trades["Size"].sum() #microshares
current_equity = current_shares * GOOG.Close.iloc[-1]

print("Total investment: ", total_invested)
print("Current Shares: ", current_shares/10**6)
print("current equity: ", current_equity)
print("Return: ", current_equity / total_invested)