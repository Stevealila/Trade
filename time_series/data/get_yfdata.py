

def fx_data_of(currency="USDJPY", days=90):
    """
    Get historical forex data for `currency` X for the past Y `days`.
    """

    import datetime as dt 
    import yfinance as yf 

    start_date = dt.datetime.today()- dt.timedelta(days) 
    end_date = dt.datetime.today()

    stock =f"{currency}=X"
    data = yf.download(stock, start_date, end_date)

    return data