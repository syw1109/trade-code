import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=600)
df.to_excel("dd.xlsx")

