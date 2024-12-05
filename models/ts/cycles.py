def forecast_serials(currency: str, num_lags: int, minutes_timeframe: int):

    # .................................Get data for the timeframe..........................................

    from utils.mt_5.data import get_currency_pair_data_

    df = get_currency_pair_data_(currency, timeframe=f"m{minutes_timeframe}", years_back=.5)


    # .................................Train..........................................

    from sklearn.model_selection import train_test_split
    from sklearn.multioutput import MultiOutputRegressor
    from xgboost import XGBRegressor
    from utils.ts import make_lags, make_multistep_targets

    X = make_lags(ts=df, lags=num_lags).fillna(0.0)
    y = make_multistep_targets(ts=df, steps=num_lags).dropna()

    X = X.iloc[num_lags-1:].reset_index(drop=True)  
    y = y.reset_index(drop=True) 

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = MultiOutputRegressor(XGBRegressor())
    model.fit(X_train, y_train)

    
    # .................................Forecast..........................................

    import pandas as pd

    last_lags = X.iloc[-1].values.reshape(1, -1)
    y_fore = model.predict(last_lags) 

    forecast_df = pd.DataFrame({
        "time": pd.date_range(
                    df.index[-1] + pd.Timedelta(minutes=minutes_timeframe), 
                    periods=num_lags, 
                    freq=f"{minutes_timeframe}min"
                ),
        "predicted_close": y_fore.flatten()
    })

    forecast_df.index = forecast_df['time']
    forecast_df.drop('time', axis=1, inplace=True)

    return df, forecast_df




def trade_serials(currency, df, forecast_df):

    current_price = df['close'].iloc[-1] 
    predicted_close = float(f"{forecast_df['predicted_close'].iloc[-1]:.3f}")
    print("\n.....................................REQUEST:..........................................\n")

    # .................................Print trade to-be info..........................................

    if predicted_close > current_price: # buy
        target_profit = (predicted_close - current_price) * 100
        print(f"predicted_close is GREATER than current_close:\n")

    elif predicted_close < current_price: # short-sell
        target_profit = (current_price - predicted_close) * 100
        print(f"We will go SHORT by {target_profit:.0f} pips:\n")
        
    elif predicted_close == current_price:
        print(f"predicted_close == current_close:\n")
        target_profit = 0

    target_profit = int(float(f"{target_profit:.0f}")) 

    print(f"current_price   => {current_price}\npredicted_close => {predicted_close}\ntarget_profit   => {target_profit}")
    print("\n.....................................RESPONSE:..........................................\n")



    # .................................Trade conditionally..........................................


    from utils.mt_5.trade import buy, short_sell
    # import pandas as pd

    # past_2000hrs = df.index.time[-1] >= pd.Timestamp('20:00:00').time()

# if not past_2000hrs:
    if predicted_close > current_price: # buy
        print(f"\n\n.....................BUYING {currency}.....................\n\n")
        target_profit = round((predicted_close - current_price) * 100)
        buy(currency, target_profit=target_profit)

    elif predicted_close < current_price: # short-sell
        print(f"\n\n......................SHORT-SELLING {currency}......................\n\n")
        target_profit = round((current_price - predicted_close) * 100)
        short_sell(currency, target_profit=target_profit)
    else:
        print(".....................I DON'T KNOW HOW TO HELP YOU!.....................")
# else:
    # print("You CANNOT trade PAST 2000hrs!!!\n\n")