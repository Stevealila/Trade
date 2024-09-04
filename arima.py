import MetaTrader5 as mt5
from utils.mt5_utils import create_dataframe
import pandas as pd
mt5.initialize()
df = create_dataframe(currency_pair='eurusd', timeframe="h1", years_back=1)
df.index = pd.DatetimeIndex(df.index).to_period('h')
print(df.tail())


from pmdarima import auto_arima
arima_params = auto_arima(df[['close']], test='adf')
print(arima_params)


from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
train, test = train_test_split(df, test_size=0.2, shuffle=False)
arima_model = ARIMA(train['close'], order=(0,1,0))
arima = arima_model.fit()
print(arima)


arima_pred = arima.forecast(steps=len(test))
print(arima_pred)