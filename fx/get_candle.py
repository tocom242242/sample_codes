import pandas as pd 
from oandapyV20 import API 
import oandapyV20.endpoints.instruments as instruments
import configparser

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('config.ini')


access_token = config.get("oanda", "access_token")

api = API(access_token=access_token, environment="practice")

params = {
    "granularity": "D",  # 取得する足
    "count": 50,         # 取得する足数
    "price": "B",        # Bid
}

instrument = "USD_JPY"   # 通貨ペア

instruments_candles = instruments.InstrumentsCandles(instrument=instrument, params=params)

api.request(instruments_candles)
response = instruments_candles.response

print(response.keys())

df = pd.DataFrame(response["candles"])
print(df.head())
