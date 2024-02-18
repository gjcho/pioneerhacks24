import os
from flask import Flask,  render_template, request

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
# bt.plot()
print(stats)
trades = stats["_trades"]
price_paid = trades["Size"]  * trades["EntryPrice"]
total_invested = price_paid.sum()

current_shares = trades["Size"].sum() #microshares
current_equity = current_shares * GOOG.Close.iloc[-1]

app = Flask(__name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-started', methods = ['GET', 'POST'])
def func():
    if request.method == "POST":
        goal = request.form.get("goal")
        fname = request.form.get("fname")
        bt.plot()
        return render_template("index3.html", g=goal, n=fname, stats=stats)
    return render_template("index2.html")

@app.route('/summary', methods = ['GET', 'POST'])
def func2():
    return render_template("index4.html", t=total_invested, s=current_shares/10**6, e=current_equity, r=current_equity / total_invested, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
