
import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BCH", count=15)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

df = pyupbit.get_ohlcv("KRW-BCH", count=15)
df['KE'] = abs(df['close'] - df['open'])/(df['high'] - df['low'])




df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

def get_ma15E(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15E = df['close'].rolling(15).mean().iloc[-1]
    return ma15E

def get_KE(ticker):
    """20 일 노이즈"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    KE = df[1-abs('close'-'open')/('high'-'low')].rolling(20).mean().iloc[-1]
    return KE                        
print(df['KE'])
df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("bch.xlsx")