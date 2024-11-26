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
        # print("Connected to MetaTrader5 successfully!")
    except:
        print("Failed to connect to MetaTrader5!")