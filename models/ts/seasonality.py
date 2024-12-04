
def hourly(currency: str, years_back=1.25):
    """
    Models average rises and falls per trading hour using mt5's `H1` timeframe.
    """
    import seaborn as sns
    import matplotlib.pyplot as plt
    from utils.mt_5.data import get_currency_pair_data_

    df = get_currency_pair_data_(
        currency_pair=currency,
        timeframe='H1',
        years_back=years_back
    )
    # Add an 'hour' column
    df["hour"] = df.index.hour

    # Plot hourly average close prices
    sns.set_style('whitegrid')
    plt.figure(figsize=(12, 6))
    plot = sns.lineplot(
        data=df,
        x="hour",
        y="close",
        estimator="mean",
        errorbar=None,
        marker="o",
    )

    plt.title(f"Average Hourly Close Prices for {currency.upper()} (Last {int(years_back*12)} Months)")
    plt.xticks(range(24))  
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    return df, plot





def sessional(currency: str, years_back=1.25):
    """
    Models average rises and falls per trading session using mt5's `H3` timeframe.
    """
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from utils.mt_5.data import get_currency_pair_data_

    # Get data
    df = get_currency_pair_data_(
        currency_pair=currency, 
        timeframe="H3", 
        years_back=years_back
    )

    # Add `session` column
    session_order = ["Tokyo(0300)", "London(1100)", "New_York(1700)", "Sydney(2200)"]
    def create_sessional_df(df):
        def get_trading_session(hour):
            if 3 <= hour < 11:
                return session_order[0]
            elif 11 <= hour < 17:
                return session_order[1]
            elif 17 <= hour < 22:
                return session_order[2]
            else:
                return session_order[3]
        df["session"] = df.index.to_series().dt.hour.map(get_trading_session)
        return df

    df = create_sessional_df(df)

    # Sort the sessions for chronological observation
    df['session'] = pd.Categorical(df['session'], categories=session_order, ordered=True)

    # Ensure equal samples for each session
    min_samples = df['session'].value_counts().min()  
    df_balanced = (
        df.groupby('session', group_keys=False, observed=True)
        .apply(lambda group: group.iloc[:min_samples])
        )
    

    # Plot session-wise average close prices
    sns.set_style('whitegrid')
    plot = sns.lineplot(
        data=df_balanced,
        x="session",
        y="close",
        estimator="mean",
        errorbar=None,
        marker="o",
    )

    plt.title(f"Average Sessional Close Prices for {currency.upper()} (Last {int(years_back*12)} Months)")
    plt.tight_layout()

    return df_balanced, plot




def daily(currency: str, years_back=1.25):
    """
    Models average rises and falls per day using mt5's `D1` timeframe. 
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