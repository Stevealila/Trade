def calculate_sl_tp(symbol, lot, target_profit, max_loss, price):
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

    return take_profit, stop_loss



def calculate_sl_tp_short_sell(symbol, lot, target_profit, max_loss, price):
    if "JPY" in symbol: 
        pip_value = lot * 100000 * 0.01  

        pips_for_target = abs(target_profit / pip_value)
        pips_for_loss = abs(max_loss / pip_value)

        take_profit = price - pips_for_target  
        stop_loss = price + pips_for_loss      
    else: 
        pip_value = lot * 100000 * 0.0001  

        pips_for_target = abs(target_profit / pip_value)
        pips_for_loss = abs(max_loss / pip_value)

        take_profit = price - pips_for_target * 0.0001  
        stop_loss = price + pips_for_loss * 0.0001      

    return take_profit, stop_loss