
def initialize_():
    import MetaTrader5 as mt5
    mt5.initialize()




def login_():
    import MetaTrader5 as mt5
    from dotenv import load_dotenv 
    import os

    load_dotenv()

    EXNESS_PASSWORD = os.getenv("EXNESS_PASSWORD")
    EXNESS_SERVER = os.getenv("EXNESS_SERVER")
    EXNESS_MT5_LOGIN = os.getenv("EXNESS_MT5_LOGIN")
    try:
        initialize_()
        mt5.login(login=int(EXNESS_MT5_LOGIN), password=EXNESS_PASSWORD, server=EXNESS_SERVER)
        print("Connected to MetaTrader5 successfully!")
    except:
        print("Failed to connect to MetaTrader5.")




def get_currency_pair_data_(currency_pair, timeframe='D1', years_back=3):
    
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
        df.drop('real_volume', axis=1, inplace=True)
        return df
    else:
        print("NO rates found!")






def place_buy_order(symbol, lot_size, stop_loss=None, take_profit=None):
    
    import MetaTrader5 as mt5
    
    price = mt5.symbol_info_tick(symbol).ask
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,  # Maximum deviation in points
        "magic": 234000,  # Arbitrary ID for identification
        "comment": "Buy order",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"Buy order failed: {result.retcode} {result.comment}")
    print(f"Buy order placed successfully: {result}")
    return result




def place_sell_order(symbol, lot_size, stop_loss=None, take_profit=None):
    
    import MetaTrader5 as mt5

    price = mt5.symbol_info_tick(symbol).bid
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,  # Maximum deviation in points
        "magic": 234000,  # Arbitrary ID for identification
        "comment": "Sell order",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"Sell order failed: {result.retcode} {result.comment}")
    print(f"Sell order placed successfully: {result}")
    return result




def stop_loss_take_profit(order_id, symbol, stop_loss=None, take_profit=None):
    
    import MetaTrader5 as mt5

    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": symbol,
        "position": order_id,
        "sl": stop_loss,
        "tp": take_profit,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"Failed to modify order: {result.retcode} {result.comment}")
    print(f"Order modified successfully: {result}")
    return result