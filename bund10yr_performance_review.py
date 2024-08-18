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


# Add rectangular patch
import matplotlib.patches as patches

def rect_patch_candle():
    start = '2024-08-09 09:15'
    enddt = '2024-08-10 04:10'
    flt = (df_1m.index >= start) & (df_1m.index <= enddt)
    
    # Filter and plot the candlestick chart
    fig, ax = plt.subplots(figsize=(12, 6))
    mavs = [mpf.make_addplot(df_1m.loc[flt]['m60'], color='g', ax=ax),
            mpf.make_addplot(df_1m.loc[flt]['m120'], color='r', ax=ax)]
    mpf.plot(df_1m.loc[flt], type='candle', ax=ax, style='charles', addplot=mavs)
    
    # Extract trade data within the time range
    trades_in_range = df_tr[(df_tr['진입일시'] >= start) & (df_tr['진입일시'] <= enddt)]
    
    for _, trade in trades_in_range.iterrows():
        entry_time = trade['진입일시']
        entry_price = trade['진입가격']
        result = trade['거래결과']
        exit_price = entry_price + 0.03 if trade['거래구분'] == '매수' else entry_price - 0.03
        
        # Define the time range for the rectangle
        entry_idx = df_1m.index.get_loc(entry_time, method='nearest')
        if entry_idx + 1 >= len(df_1m):
            continue
        
        # Find the index where the price first meets the exit price
        df_range = df_1m.iloc[entry_idx:]
        high_exit_idx = df_range[df_range['High'] >= exit_price].index.min()
        low_exit_idx = df_range[df_range['Low'] <= exit_price].index.max()
        
        if pd.isna(high_exit_idx) or pd.isna(low_exit_idx):
            continue
        
        end_time = min(high_exit_idx, low_exit_idx)
        
        # Plot the rectangle
        ax.add_patch(patches.Rectangle(
            (entry_time, min(entry_price, exit_price)),
            (end_time - entry_time).total_seconds() / 60 / 60,  # Width in hours
            abs(entry_price - exit_price),
            color='blue', alpha=0.3, edgecolor='blue'
        ))

    plt.show()

rect_patch_candle()


# save chart

print(df_1m.head())
#print(df_trade_log)