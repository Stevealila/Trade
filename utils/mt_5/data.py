def get_currency_pair_data_(
    currency_pair, 
    timeframe='D1', 
    years_back=3, 
    timezone="Africa/Nairobi"
):    
    import MetaTrader5 as mt5
    import pytz
    from datetime import datetime
    import pandas as pd
    from utils.mt5.login import login_

    login_()

    timeframe_map = {
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H3": mt5.TIMEFRAME_H3,
        "H6": mt5.TIMEFRAME_H6,
        "H12": mt5.TIMEFRAME_H12,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "M": mt5.TIMEFRAME_MN1,
    }

    if timeframe.upper() not in timeframe_map:
        return "Use a different timeframe"
    
    # Calculate the number of bars based on timeframe and years_back
    mt5_timeframe = timeframe_map[timeframe.upper()]
    days_in_year = 365.25  # Account for leap years

    if mt5_timeframe == mt5.TIMEFRAME_M30:  # Every 30 minutes
        bars = int(years_back * days_in_year * 24 * 60 // 30)
    elif mt5_timeframe == mt5.TIMEFRAME_H1:  # Hourly
        bars = int(years_back * days_in_year * 24)
    elif mt5_timeframe == mt5.TIMEFRAME_H3:  # Every 3 hours
        bars = int(years_back * days_in_year * 24 // 3)
    elif mt5_timeframe == mt5.TIMEFRAME_H6:  # Every 6 hours
        bars = int(years_back * days_in_year * 24 // 6)
    elif mt5_timeframe == mt5.TIMEFRAME_H12:  # Every 12 hours
        bars = int(years_back * days_in_year * 24 // 12)
    elif mt5_timeframe == mt5.TIMEFRAME_D1:  # Daily
        bars = int(years_back * days_in_year)
    elif mt5_timeframe == mt5.TIMEFRAME_W1:  # Weekly
        bars = int(years_back * days_in_year // 7)
    elif mt5_timeframe == mt5.TIMEFRAME_MN1:  # Monthly
        bars = int(years_back * 12)
    else:
        return "Unsupported timeframe"

    rates = mt5.copy_rates_from(
        currency_pair.upper() + "m", 
        mt5_timeframe, 
        datetime.now(pytz.timezone(timezone)), 
        bars
    )
    if rates is not None and len(rates):  
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index('time')
        df = df.drop('real_volume', axis=1)
        df = df[['close']]
        # df = df.to_period(period)
        return df
    else:
        print("No rates found!")
