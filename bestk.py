import pybithumb
import datetime
import numpy as np
import time

my_ticker = "AGI"

def get_target_price(ticker, k):
    df = pybithumb.get_ohlcv(ticker)[-1:]
    target_price = df.iloc[0]['low'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)[-6:]
    ma5 = df['low'].rolling(5).mean().iloc[-1]
    return ma5


def get_current_price(ticker):
    return pybithumb.get_current_price(ticker)


def get_ror(ticker, k):
    df = pybithumb.get_ohlcv(ticker)[-8:]
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.04
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod().iloc[-2]
    return ror

#최적의 k값 계산
def find_best_k(ticker):
    best_k, best_ror = -1, 0
    for k in np.arange(0.05, 1.01, 0.05):
        ror = get_ror(ticker, k)
        if ror > best_ror:
            best_ror = ror
            best_k = k
    return best_k


bk = find_best_k(my_ticker)
target_price = get_target_price(my_ticker, bk)
ma5 = get_ma5(my_ticker)
current_price = get_current_price(my_ticker)

print("bk : ", bk)
print("target price : ", target_price, "ma5 : ", ma5, "current_price : ", current_price)
