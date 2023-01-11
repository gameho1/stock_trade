import pandas_datareader as web
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import matplotlib.pyplot as plt
from talib import abstract
import numpy as np

# download stock history data
#df = web.DataReader(name='0050.TW', data_source='yahoo', start='2014-07-25', end='2022-07-25') 
#df.to_csv("stock_0050_2014_2022_0725.csv")

# build data from csv and select target data
df = pd.read_csv('C:/Users/MFT/Desktop/backtest_result/0050.TW.csv')
df = df.interpolate()                #flll empty data
date_sel = df['Date']>='2014-07-25'  #select target data 
df_sel = df[date_sel]
df_sel['Date'] = pd.to_datetime(df_sel['Date']) #convert type to datetime
df_sel = df_sel.set_index('Date') # set date as index


#calculate KD signal with talib
df_tmp = df_sel
df_tmp.rename(columns = {'High':'high', 'Low':'low','Adj Close':'close','Close':'non_adj close'}, inplace = True) #rename for talib
kd = abstract.STOCH(df_tmp)
kd.index=df_tmp.index
fnl_df = df_tmp.join(kd).dropna() #merge two data frame
fnl_df.rename(columns = {'high':'High', 'low':'Low','close':'Close'}, inplace = True) #rename column name for backtest

def I_bypass(data): # bypass data in Strategy
    return data

class KDCross(Strategy): 
    lower_bound = 20  
    upper_bound = 80  

    def init(self):
        self.k = self.I(I_bypass, self.data.slowk) #K 
        self.d = self.I(I_bypass, self.data.slowd) #D

    def next(self):
        if crossover(self.k, self.d) and self.k<self.lower_bound and self.d<self.lower_bound and not self.position: #long position
            self.buy() 
        elif crossover(self.d, self.k) and self.k>self.upper_bound and self.d>self.upper_bound: 
            if self.position and self.position.is_long:
                self.position.close()
#run backtest
bt = Backtest(fnl_df, KDCross, cash=10000, commission=.002)
rslt = bt.run()
print(rslt)
bt.plot()