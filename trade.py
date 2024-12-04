from utils.mt_5.trade import *

t_type = input("Transaction Type (A: sell B: buy C: short_sell): ")

if t_type.upper()=="A":
    symbol = input("symbol: ").strip().upper()
    sell(symbol)
if t_type.upper()=="B" or t_type.upper()=="C":
    symbol = input("symbol: ").strip()
    target_profit = int(input("target_profit=10: ").strip()) or 10
    max_loss = int(input("max_loss=3: ").strip()) or 3
    if t_type.upper()=="B":
        buy(symbol, target_profit, max_loss)
    if t_type.upper()=="C":
        short_sell(symbol, target_profit, max_loss)