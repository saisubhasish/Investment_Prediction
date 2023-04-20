import sys

from analysis import *
from investment_prediction import utils
from investment_prediction.config import DATABASE_NAME
from investment_prediction.config import collection_name
from investment_prediction.exception import InvestmentPredictionException

try:
    df = utils.get_collection_as_dataframe(database_name=DATABASE_NAME, collection_name=collection_name)
    df_close = df[['Date', 'Price']]
    df_close = utils.set_index_as_Date(df_close)

    plot_sma(df= df_close, window_size= 50)
    plot_ema(df= df_close, window_size= 100)
    plot_bollinger_band(df= df_close)
    plot_macd(df= df_close)
    plot_volume(df= df)
    plot_candle_stick(df= df)
except Exception as e:
    raise InvestmentPredictionException(e, sys)
