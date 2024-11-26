def buy(symbol, target_profit=20, max_loss=5):
    import MetaTrader5 as mt5
    from utils.mt5.login import login_
    
    login_()

    symbol += "m"
    symbol_info = mt5.symbol_info(symbol)
    
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        return
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, exit", symbol)
            mt5.shutdown()
            return

    lot = 0.01  # Standard lot size
    price = mt5.symbol_info_tick(symbol).ask
    
    # Calculate pip value based on symbol
    if "JPY" in symbol:
        pip_value = lot * 100000 * 0.01  

        pips_for_target = abs(target_profit / pip_value)
        pips_for_loss = abs(max_loss / pip_value)

        take_profit = price + pips_for_target
        stop_loss = price - pips_for_loss
    else:
        pip_value = lot * 100000 * 0.0001  

        pips_for_target = abs(target_profit / pip_value)
        pips_for_loss = abs(max_loss / pip_value)

        take_profit = price + pips_for_target * 0.0001  
        stop_loss = price - pips_for_loss * 0.0001

    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Cannot buy {symbol} of {lot} lots at {price} because of '{result.comment}'")
    else:
        print(f"{symbol} bought successfully!")
    
    mt5.shutdown()
