def hourly(currency: str, years_back=.5):
    """
    Models average rises and falls per trading session using mt5's `H1` timeframe.
    The idea is to help you choose a suitable `session` to trade the given `currency`. 
    """
    import pandas as pd
    import seaborn as sns
    from utils.mt_5.data import get_currency_pair_data_

    # Get data
    df = get_currency_pair_data_(
        currency_pair=currency, 
        timeframe="H1", 
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
        errorbar=None
    )

    return df_balanced, plot
