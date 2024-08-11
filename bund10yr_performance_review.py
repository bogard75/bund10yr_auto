import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Bund10yr 데이터 및 거래로그 입수
df_1m = pd.read_csv('bund10yr_1m_240810.txt', 
                    delimiter='\t', 
                    encoding='euc-kr',
                    names=['Date','Open','High','Low','Close',
                           'm5','m10','m20','m60','m120','Volume'],
                    thousands=',',
                    skiprows=1)

df_1m['Date']=pd.to_datetime(df_1m['Date'], format='%Y/%m/%d,%H:%M')
df_1m.set_index('Date', inplace=True)
df_1m = df_1m.sort_index(ascending=True)

df_tr = pd.read_csv('bund10yr_trade_log_240810.tsv', 
                     delimiter='\t', 
                     thousands=',')

df_tr['진입일시'] = pd.to_datetime(df_tr['진입일시'], format='%Y-%m-%d %H:%M')
df_tr['청산일시'] = pd.to_datetime(df_tr['청산일시'], format='%Y-%m-%d %H:%M')

# Draw candle
start = '2024-08-09 09:15'
enddt = '2024-08-10 04:10'
flt = (df_1m.index >= start) & (df_1m.index <= enddt)

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title('Hello')
mpf.plot(df_1m.loc[flt], type='candle', ax=ax, style='charles')

#mpf.plot(df_1m.loc[flt], type='candle', style='charles', title='bund10yr', ylabel='Price', savefig='bund10yr_1m_candle{start}.png')

# Annotate trade log
def annotate_trade_log():
       trades = []
       for trade in trades:
              trade_time = pd.to_datetime(trade['time'])
              trade_price = trade['price']
              trade_type = trade['type']
       ax.annotate(f'{trade_type}({trade_price}) {trade_time.strftime("%H:%M")}', 
                     xy=(trade_time, trade_price), 
                     xytext=(trade_time, trade_price - 1), 
                     arrowprops=dict(facecolor='blue', shrink=0.05),
                     fontsize=8, color='blue')

# save chart

print(df_1m.head())
#print(df_trade_log)