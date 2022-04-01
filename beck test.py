import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=600)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)







print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")

