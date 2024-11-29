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


# # deposit => 20 USD, margin => 1:200

# buy(symbol="EURJPY", target_profit=50, max_loss=10) # price: 159.908, stop_loss: 158.908, take_profit: 164.908 => +5,-1
# buy(symbol="USDCHF", target_profit=50, max_loss=10) # price: 0.88353, stop_loss: 0.87353, take_profit: 0.93353 => +0.05,-0.01
# buy(symbol="USDJPY", target_profit=50, max_loss=10) # price: 151.691, stop_loss: 150.691, take_profit: 156.691 => +5,-1
