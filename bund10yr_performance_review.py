import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Bund10yr 데이터 및 거래로그 입수
# df_1m.index.to_series().agg(['min', 'max'])
# 24.5.15 14:45:00 ~ 24.8.10 05:00:00, 74802건
def read_bund10yr_1m(src):
       df = pd.read_csv(src, 
                    delimiter='\t', 
                    encoding='euc-kr',
                    names=['Date','Open','High','Low','Close',
                           'm5','m10','m20','m60','m120','Volume'],
                    thousands=',',
                    skiprows=1)

       return df


SRC_LST = ['bund10yr_1m_240810.txt',
           'bund10yr_1m_240717.txt',
           'bund10yr_1m_240711.txt',
           'bund10yr_1m_240702.txt',
           'bund10yr_1m_240607.txt',
           ]
df_1m = pd.concat([read_bund10yr_1m(txt) for txt in SRC_LST]).drop_duplicates()
df_1m['Date']=pd.to_datetime(df_1m['Date'], format='%Y/%m/%d,%H:%M')
df_1m.set_index('Date', inplace=True)
df_1m = df_1m.sort_index(ascending=True)

# Bund10yr 거래로그 입수
def read_trade_log(src):
       df = pd.read_csv(src, 
                        delimiter='\t', 
                        thousands=',')       
       df['진입일시'] = pd.to_datetime(df['진입일시'], format='%Y-%m-%d %H:%M')
       df['청산일시'] = pd.to_datetime(df['청산일시'], format='%Y-%m-%d %H:%M')
       df['거래결과'] = df['청산손익'].apply(lambda x: '1익절' if x > 0 else ('2손절' if x < 0 else '3똔똔'))
       return df

 
df_tr = read_trade_log('bund10yr_trade_log_240810.tsv')


# Draw candle
# 차트시작 / 종료일시
def draw_candle():
       start = '2024-08-09 09:15'
       enddt = '2024-08-10 04:10'
       flt = (df_1m.index >= start) & (df_1m.index <= enddt)
       
       fig, ax = plt.subplots(figsize=(12, 6))
       # 이평선 추가
       mavs = [mpf.make_addplot(df_1m.loc[flt]['m60'], color='g', ax=ax),
              mpf.make_addplot(df_1m.loc[flt]['m120'], color='r', ax=ax)]
       mpf.plot(df_1m.loc[flt], type='candle', ax=ax, style='charles', addplot=mavs)


draw_candle()
#mpf.plot(df_1m.loc[flt], type='candle', style='charles', title='bund10yr', ylabel='Price', savefig='bund10yr_1m_candle{start}.png')


# Annotate trade log
def annotate_trade_log(tr):
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