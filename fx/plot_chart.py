import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from mpl_finance import candlestick_ohlc
from mpl_finance import candlestick_ohlc, candlestick2_ohlc, candlestick2_ochl
import datetime
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import talib
import configparser

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('config.ini')

access_token = config.get("oanda", "access_token")

api = API(access_token=access_token, environment="practice")
 
params = {
    "granularity": "M1",  # 取得する足
    "count": 200,         # 取得する足数
    "price": "B",        # Bid
}
 
instrument = "USD_JPY"   # 通貨ペア
 
instruments_candles = instruments.InstrumentsCandles(instrument=instrument, params=params)
 
api.request(instruments_candles)
response = instruments_candles.response
 
df = pd.DataFrame(response["candles"])
 
ohlc = []
for r in response["candles"]:
    time = r["time"].replace(".000000000Z", "")
    time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    time = mdates.date2num(time)
    r["bid"]["time"] = time
    ohlc.append(r["bid"])
 
df = pd.DataFrame(ohlc)
df = df.astype(np.float64)
 
# ローソク足のチャートの表示
fig, ax = plt.subplots(figsize=(10, 5))
# df = df[["time", "o", "h", "l", "c"]]
df = df[["time", "o", "h", "l", "c"]]
# opens = df["o"].values
# highs = df["h"].values
# lows = df["l"].values
# closes = df["c"].values

df["time"] = np.arange(len(df["time"].values))
candlestick_ohlc(ax, df.values, colorup="green", colordown="red")

# candlestick2_ochl(ax, opens, closes, highs, lows, colorup="green", colordown="red")
# candlestick2_ochl(ax, opens, highs, lows, closes, colorup="green", colordown="red")
 
# candlestick2_ochl(ax, opens, closes, highs, lows, colorup="red", colordown="blue")

times = df["time"].values

# 移動平均を計算する
sma_25 = talib.SMA(df["c"].values, 25)  # 25移動平均
ax.plot(times, sma_25, label="25")

sma_75 = talib.SMA(df["c"].values, 75)  # 75移動平均
ax.plot(times, sma_75, label="75")

sma_200 = talib.SMA(df["c"].values, 200)    # 200移動平均
ax.plot(times, sma_200, label="200")

# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

plt.show()
