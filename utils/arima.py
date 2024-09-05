
def check_stationarity(df):
    from statsmodels.tsa.stattools import adfuller
    
    adf_result = adfuller(df)
    if(adf_result[1] < 0.05):
        return True
    else:
        return False
    



def get_pdq_params(data, target_col):
    import itertools
    from statsmodels.tsa.arima.model import ARIMA
    import warnings
    from statsmodels.tools.sm_exceptions import ConvergenceWarning

    # Ignore specific warnings
    warnings.simplefilter("ignore", ConvergenceWarning)
    warnings.filterwarnings("ignore", message="Non-stationary starting autoregressive parameters found")
    warnings.filterwarnings("ignore", message="Non-invertible starting MA parameters found")

    # Define the p, d and q parameters
    p = q = range(0, 5)
    d = range(1, 2)

    # Generate all different combinations of p, d and q triplets
    pdq = list(itertools.product(p, d, q))

    best_aic = float("inf")
    best_pdq_combination = None

    for param in pdq:
        try:
            model = ARIMA(data[target_col].values, order=param)
            model_fit = model.fit()
            if model_fit.aic < best_aic:
                best_pdq_combination = param
                best_aic = model_fit.aic
        except:
            continue
    return best_pdq_combination