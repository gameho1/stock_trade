# -*- coding: utf-8 -*-
"""Day-14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zkStsdhKBlgLGFOU-98FM1cMleaDIGZW

# 引入函式庫
"""

#--------------------------
# 需要套件
# backtesting
#--------------------------
import datetime
import warnings
import pandas as pd
import requests

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from pandas.core.common import SettingWithCopyWarning

#--------------------------
# 自行開發的套件
#--------------------------
import strategy
#--------------------------

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
pd.set_option("display.max_columns", None)


class data_analysis(object):
    def __init__(self):
        print("Class init.")
        
    def get_data(self):
        """# 取得資料
        backtesting強制要求欄位名稱格式，
        所以需要先轉換欄位名稱
        """
        self.stock_index = 2340
        url = "https://api.finmindtrade.com/api/v4/data"
        parameter = {
            "dataset": "TaiwanStockPrice",
            "start_date": datetime.datetime(2012, 1, 1, 0, 0).strftime("%Y-%m-%d"),
            "end_date": datetime.datetime(2018, 1, 1, 0, 0).strftime("%Y-%m-%d"),
            "data_id": self.stock_index,
        }

        data = requests.get(url, params=parameter)
        data = data.json()

        self.df = pd.DataFrame(data["data"])

        self.df.index = pd.to_datetime(self.df["date"])
        self.df.rename(
            columns={
                "Trading_Volume": "Volume",
                "open": "Open",
                "max": "High",
                "min": "Low",
                "close": "Close",
            },
            inplace=True,
        )

        self.df.drop(
            columns=["stock_id", "date", "Trading_money", "spread", "Trading_turnover"],
            inplace=True,
        )

    def do_trade(self):
        """# 執行策略
        - cash：本金。
        - commission：交易費用。
        - exclusive_orders：是否禁止多頭操作(同時只能買空或賣空)。
        - trade_on_close：於收盤時交易，否則預設於開盤交易。
        """
        self.test = Backtest(
            self.df,
            strategy.SmaCross,
            cash=1000000,
            commission=0.004,
            exclusive_orders=True,
            trade_on_close=True,
        )
        self.result = self.test.run()

    def show_result(self):
        """# 分析結果
        將分析結果儲存，並利用預設瀏覽器開啟，
        result為詳細的分析結果。
        """
        self.test.plot(filename=f"./backtest_result/{self.stock_index}.html")
        print(self.result)

        """![https://ithelp.ithome.com.tw/upload/images/20210919/20141586nTsggfN69g.png](https://ithelp.ithome.com.tw/upload/images/20210919/20141586nTsggfN69g.png)

        欄位 | 說明
        ------------- | -------------
        Start                  |   起始時間
        End                    |   結束時間
        Duration               |   經過天數
        Exposure [%]           |   投資比率
        Equity Final [$]       |   最終資產
        Equity Peak [$]        |   最高資產
        Return [%]             |   報酬率
        Buy & Hold Return [%]  |   買入持有報酬率
        Max. Drawdown [%]      |   最大交易回落
        Avg. Drawdown [%]      |   平均交易回落
        Max. Drawdown Duration |   最長交易回落期間
        Avg. Drawdown Duration |   平均交易回落期間
        Win Rate [%]           |   勝率
        Best Trade [%]         |   最好交易報酬率
        Worst Trade [%]        |   最差交易報酬率
        Avg. Trade [%]         |   平均交易報酬率
        Max. Trade Duration    |   最長交易間隔
        Avg. Trade Duration    |   平均交易間隔
        Expectancy [%]         |   期望值
        SQN                    |   系統品質指標
        Sharpe Ratio           |   夏普比率
        Sortino Ratio          |   索丁諾比率
        Calmar Ratio           |   卡瑪比率
        _strategy              |   使用策略名稱
        *From https://hackmd.io/@s02260441/SkA7IWVJv*
        """

if(__name__ == "__main__"):
    data1 = data_analysis()
    data1.get_data()
    data1.do_trade()
    data1.show_result()
