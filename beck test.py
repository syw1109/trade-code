import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=20)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df['total'] = df['close'].shift(1) + df['close'].shift(2)+ df['close'].shift(3)+ df['close'].shift(4)+ df['close'].shift(5)
df['5ave'] = df['total']/5



fee = 0.05
df['ror'] = np.where(df['high'] > df['target']and df['target'] > df['5ave'],
                     df['close'] / df['target'] - fee,
                     1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")