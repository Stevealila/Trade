def daily(currency: str, years_back=1):
    """
    Models average rises and falls per day using mt5's `D1` timeframe.
    Days are sorted from Mon-Fri.
    The idea is to help you choose the best day to trade the given `currency`. 
    """
    import pandas as pd 
    import seaborn as sns
    from utils.mt_5.data import get_currency_pair_data_

    # get data
    df = get_currency_pair_data_(
            currency_pair=currency, 
            timeframe="D1", 
            years_back=years_back
        )

    # construct trading days [Mon-Fri]
    df["day"] = df.index.day_name()
    df = df[df.index.dayofweek < 5]
    
    # Sort the days for chronological observation
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)

    return df, sns.lineplot(x=df['day'], y=df['close'])