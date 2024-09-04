# ....................................get time series data....................................
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv")

df['Month'] = pd.to_datetime(df['Month'])
df = df.set_index(['Month'])

"""df.tail():

	#Passengers
Month	
1960-08-01	606
1960-09-01	508
1960-10-01	461
1960-11-01	390
1960-12-01	432

"""


# ....................................create model....................................
import pmdarima as pm

model = pm.auto_arima(df[['#Passengers']], test='adf', m=12)





# ....................................predict.................................... 
n_periods = 24

pred, pred_ranges = model.predict(
    n_periods=n_periods, 
    return_conf_int=True,
)

"""pred[::-5]:

1962-12-01    499.858481
1962-07-01    688.437307
1962-02-01    454.177037
1961-09-01    540.883864
1961-04-01    491.840023
Freq: -5MS, dtype: float64

"""


# ....................................plot outcomes..................................
import matplotlib.pylab as plt

index_of_fc = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods=n_periods, freq='MS')
pred_series = pd.Series(pred, index=index_of_fc)

plt.figure(figsize=(15, 7))
plt.plot(df["#Passengers"], color='#1f76b4')
plt.plot(pred_series, color='darkgreen')
plt.title("SARIMAX - Forecast of Airline Passengers")
plt.show()