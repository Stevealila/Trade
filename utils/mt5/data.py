def get_currency_pair_data_(currency_pair, timeframe='D1', period='D', years_back=3):
    
    import MetaTrader5 as mt5
    import pytz
    from datetime import datetime
    import pandas as pd

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
        return "Use a different timefame"
    
    # Calculate the number of bars based on timeframe and years_back
    mt5_timeframe = timeframe_map[timeframe.upper()]
    if mt5_timeframe == mt5.TIMEFRAME_M30:  # Every 30 minutes
        bars = years_back * 365 * 24 * 60 // 30
    if mt5_timeframe == mt5.TIMEFRAME_H1:  # Hourly
        bars = years_back * 365 * 24
    if mt5_timeframe == mt5.TIMEFRAME_H3:  # Every 3 hours
        bars = years_back * 365 * 24 // 3
    if mt5_timeframe == mt5.TIMEFRAME_H6:  # Every 6 hours
        bars = years_back * 365 * 24 // 6
    if mt5_timeframe == mt5.TIMEFRAME_H12:  # Every 12 hours
        bars = years_back * 365 * 24 // 12
    if mt5_timeframe == mt5.TIMEFRAME_D1:  # Daily
        bars = years_back * 365 
    if mt5_timeframe == mt5.TIMEFRAME_W1:  # Weekly
        bars = years_back * 52  
    if mt5_timeframe == mt5.TIMEFRAME_MN1:  # Monthly
        bars = years_back * 12  

    rates = mt5.copy_rates_from(
        currency_pair.upper()+"m", 
        mt5_timeframe, 
        datetime.now(pytz.timezone("Africa/Nairobi")), 
        bars
    )
    if rates is not None and len(rates):  
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index('time')
        df = df.drop('real_volume', axis=1)
        df = df[['close']].to_period(period)
        return df
    else:
        print("NO rates found!")
