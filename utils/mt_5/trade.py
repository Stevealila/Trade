


def sell(symbol):
    import MetaTrader5 as mt5
    from utils.mt_5.login import login_
    
    login_()

    symbol += "m"
    position_id = ""

    for position in mt5.positions_get():
        if position.symbol == symbol:
            position_id = position.ticket
    
    if not position_id:
        print(f"LOGICAL ERROR: {symbol} N-O-T yet b-o-u-g-h-t!")
        return

    lot = 0.01
    price = mt5.symbol_info_tick(symbol).bid

    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": deviation,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "position": position_id,
    }
    
    # send a trading request
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Cannot sell {symbol} of {lot} lots at {price} because of '{result.comment}'")
    else:
        print(f"{symbol} sold successfully!")

    mt5.shutdown()




def buy(symbol, target_profit=10, max_loss=3):
    import MetaTrader5 as mt5
    from utils.mt_5.login import login_
    from utils.mt_5.calculate_price_levels import calculate_sl_tp
    
    login_()

    symbol += "m"
    symbol_info = mt5.symbol_info(symbol)

    position_id = ""

    for position in mt5.positions_get():
        if position.symbol == symbol:
            position_id = position.ticket

    if position_id:
        print(f"{symbol} already bought!")
        return
    
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
    take_profit, stop_loss = calculate_sl_tp(
        symbol=symbol, 
        lot=lot, 
        target_profit=target_profit, 
        max_loss=max_loss, 
        price=price)
    
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




def short_sell(symbol, target_profit=10, max_loss=3):
    import MetaTrader5 as mt5
    from utils.mt_5.login import login_
    from utils.mt_5.calculate_price_levels import calculate_sl_tp

    login_()

    symbol += "m"
    symbol_info = mt5.symbol_info(symbol)

    for position in mt5.positions_get():
        if position.symbol == symbol:
            position_id = position.ticket

    if position_id:
        print(f"{symbol} already short-sold!")
        return
    
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
    price = mt5.symbol_info_tick(symbol).bid
    take_profit, stop_loss = calculate_sl_tp(
        symbol=symbol, 
        lot=lot, 
        target_profit=target_profit, 
        max_loss=max_loss, 
        price=price,
        order_type=mt5.ORDER_TYPE_SELL
    )
    
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script short sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Cannot short sell {symbol} of {lot} lots at {price} because of '{result.comment}'")
    else:
        print(f"{symbol} short sold successfully!")
    
    mt5.shutdown()