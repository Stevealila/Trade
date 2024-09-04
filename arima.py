import MetaTrader5 as mt5
from utils.mt5_utils import create_dataframe
import pandas as pd
mt5.initialize()
df = create_dataframe(currency_pair='eurusd', timeframe="h1", years_back=1)
df.index = pd.DatetimeIndex(df.index).to_period('h')
"""print(df.tail()):

                     open     high      low    close  tick_volume  spread
time
2024-09-04 11:00  1.10528  1.10537  1.10424  1.10498         1710       8
2024-09-04 12:00  1.10498  1.10523  1.10396  1.10520         2195       8
2024-09-04 13:00  1.10521  1.10589  1.10495  1.10569         2622       7
2024-09-04 14:00  1.10572  1.10949  1.10571  1.10892         5694       7
2024-09-04 15:00  1.10892  1.10898  1.10874  1.10880           58       8
"""
