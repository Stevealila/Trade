def get_currency_pair_data_(
    currency_pair, 
    timeframe='D1', 
    years_back=3
):
    import MetaTrader5 as mt5
    import pytz
    from datetime import datetime
    import tzlocal
    import pandas as pd
    from utils.mt_5.login import login_

    login_()

    # Extended timeframe mapping
    timeframe_map = {
        "M1": mt5.TIMEFRAME_M1,
        "M2": mt5.TIMEFRAME_M2,
        "M3": mt5.TIMEFRAME_M3,
        "M4": mt5.TIMEFRAME_M4,
        "M5": mt5.TIMEFRAME_M5,
        "M6": mt5.TIMEFRAME_M6,
        "M10": mt5.TIMEFRAME_M10,
        "M12": mt5.TIMEFRAME_M12,
        "M15": mt5.TIMEFRAME_M15,
        "M20": mt5.TIMEFRAME_M20,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H2": mt5.TIMEFRAME_H2,
        "H3": mt5.TIMEFRAME_H3,
        "H4": mt5.TIMEFRAME_H4,
        "H6": mt5.TIMEFRAME_H6,
        "H8": mt5.TIMEFRAME_H8,
        "H12": mt5.TIMEFRAME_H12,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1,
    }

    if timeframe.upper() not in timeframe_map:
        return "Unsupported timeframe. Please choose a valid one."

    # Map the requested timeframe
    mt5_timeframe = timeframe_map[timeframe.upper()]
    days_in_year = 365.25  # Account for leap years

    # Estimate the number of bars
    if mt5_timeframe <= mt5.TIMEFRAME_M30:  # Timeframes in minutes
        minutes_per_bar = int(timeframe.upper()[1:])
        bars = int(years_back * days_in_year * 24 * 60 // minutes_per_bar)
    elif mt5_timeframe <= mt5.TIMEFRAME_H12:  # Hourly timeframes
        hours_per_bar = int(timeframe.upper()[1:])
        bars = int(years_back * days_in_year * 24 // hours_per_bar)
    elif mt5_timeframe == mt5.TIMEFRAME_D1:  # Daily
        bars = int(years_back * days_in_year)
    elif mt5_timeframe == mt5.TIMEFRAME_W1:  # Weekly
        bars = int(years_back * days_in_year // 7)
    elif mt5_timeframe == mt5.TIMEFRAME_MN1:  # Monthly
        bars = int(years_back * 12)
    else:
        return "Unsupported timeframe calculation logic."

    # Fetch historical data
    rates = mt5.copy_rates_from(
        currency_pair.upper() + "m",
        mt5_timeframe,
        datetime.now(pytz.timezone(str(tzlocal.get_localzone()))),
        bars
    )

    if rates is not None and len(rates):
        # Convert to DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)

        # Convert index to local timezone
        local_timezone = pytz.timezone(str(tzlocal.get_localzone()))
        df.index = df.index.tz_localize(pytz.UTC).tz_convert(local_timezone)
        df.index = df.index.tz_localize(None)  # Remove timezone info

        # Retain relevant columns
        df = df.drop(columns=['real_volume'], errors='ignore')
        df = df[['close']]
        return df
    else:
        print("No rates found!")
        return pd.DataFrame()
