def d1_timeframe(currency, trading_timeframe="D1", years_back=1):

    import pandas as pd 
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    from utils.mt_5.data import get_currency_pair_data_


    # get data
    df = get_currency_pair_data_(
            currency_pair=currency, 
            timeframe=trading_timeframe, 
            years_back=years_back,
            timezone="Africa/Nairobi"
        )


    # construct trading days [Mon-Fri]
    df["day"] = df.index.day_name()
    df = df[df.index.dayofweek < 5]


    # create attach signal to each day
    dummied_columns = pd.get_dummies(df['day'], drop_first=True).astype(int)
    df = pd.concat([df[['close']], dummied_columns], axis=1)


    # train LR to attach weight to each daily signal
    X = df.iloc[:, 1:]
    y = df["close"]

    model = LinearRegression()
    model.fit(X, y)


    # create new df containing day, closing price and predicted closing price
    df["y_pred"] = model.predict(X)

    df = df.copy()
    df["day"] = df.index.day_name() # re-adding cos were removed at dummying stage
    df = df[["day", "close", "y_pred"]]
    

    # Sort the days for chronological observation
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)


    # return predicted seasonality
    predicted_trend = sns.lineplot(x=df['day'], y=df['close'])

    return df, predicted_trend