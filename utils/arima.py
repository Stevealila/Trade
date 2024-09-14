
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




def get_pdq_params_sarimax(data, target_col, seasonal=True, m=7, exog=None):
    import itertools
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from statsmodels.tsa.stattools import adfuller, kpss
    import warnings
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
    import numpy as np
    from sklearn.model_selection import TimeSeriesSplit
    from statsmodels.stats.diagnostic import acorr_ljungbox
    from concurrent.futures import ThreadPoolExecutor

    warnings.simplefilter("ignore", ConvergenceWarning)
    warnings.filterwarnings("ignore", category=UserWarning)

    # Helper to check stationarity
    def is_stationary(series):
        adf_p_value = adfuller(series.dropna())[1]
        kpss_p_value = kpss(series.dropna(), nlags="auto")[1]
        return adf_p_value < 0.05 and kpss_p_value > 0.05

    # Determine range for 'd' based on stationarity
    max_d = 0
    for d in range(3):  # Check up to 2nd difference
        differenced_data = data[target_col].diff(d).dropna()
        
        # Skip if the data is constant after differencing
        if differenced_data.std() == 0:
            continue
        
        # Use both ADF and KPSS for stationarity check
        if is_stationary(differenced_data):
            max_d = d
            break
    
    # Define reduced parameter ranges for quicker execution
    p = q = range(0, 2)  # Range for AR and MA terms
    d = [max_d]  # Differencing term is fixed based on stationarity check
    
    # Seasonal parameters
    if seasonal:
        P = D = Q = range(0, 2)  # Seasonal AR, differencing, and MA terms
    else:
        P = D = Q = [0]
    
    # Generate combinations
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = list(itertools.product(P, D, Q, [m]))

    best_aic = float("inf")
    best_order = None
    best_seasonal_order = None
    threshold = 0.1  # Early stopping threshold

    # Prepare data
    y = data[target_col].values
    if exog is not None:
        exog_values = exog.values
    else:
        exog_values = None

    # Time series cross-validation
    tscv = TimeSeriesSplit(n_splits=3)

    # Residual diagnostics
    def good_residuals(resid):
        lb_test_pvalue = acorr_ljungbox(resid, lags=[10], return_df=True)["lb_pvalue"].values[0]
        return np.abs(resid.mean()) < 0.1 and lb_test_pvalue > 0.05

    def evaluate_model(param, param_seasonal):
        nonlocal best_aic, best_order, best_seasonal_order

        cv_scores = []
        for train_index, test_index in tscv.split(y):
            y_train, y_test = y[train_index], y[test_index]
            exog_train, exog_test = (exog_values[train_index], exog_values[test_index]) if exog_values is not None else (None, None)

            model = SARIMAX(y_train, order=param, seasonal_order=param_seasonal, exog=exog_train,
                            enforce_stationarity=False, enforce_invertibility=False)
            results = model.fit(disp=False)
            pred = results.forecast(steps=len(y_test), exog=exog_test)
            cv_scores.append(np.mean((y_test - pred)**2))  # MSE

        avg_mse = np.mean(cv_scores)
        results = model.fit(disp=False)  # Refit model with full data for diagnostics

        # Check if this is the best model
        if avg_mse < best_aic:
            best_aic = avg_mse
            best_order = param
            best_seasonal_order = param_seasonal

            # Diagnostic checks
            resid = results.resid
            if good_residuals(resid):
                print(f"Good model found: SARIMA{param}x{param_seasonal}")

            # Early stopping if the error is below a threshold
            if avg_mse < threshold:
                print(f"Stopping early at SARIMA{param}x{param_seasonal}")
                return best_order, best_seasonal_order

    # Parallel processing to speed up model evaluation
    with ThreadPoolExecutor(max_workers=4) as executor:
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                executor.submit(evaluate_model, param, param_seasonal)

    return best_order, best_seasonal_order
