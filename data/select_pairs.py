

def by_spread_volatility(pairs, target_count):
    from utils.mt5 import get_currency_pair_data_
    import concurrent.futures
    import numpy as np

    def fetch_pair_data(pair):
        data = get_currency_pair_data_(pair, timeframe='D1', years_back=1)
        if data is not None and not data.empty:
            last_7_days_data = data.tail(7)
            volatility = np.std(last_7_days_data['close'])
            average_spread = last_7_days_data['spread'].mean()
            return pair, average_spread, volatility
        return pair, None, None
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_pair_data, pairs))

    # Filter out pairs that didn't return valid data
    valid_results = np.array([(pair, spread, volatility) for pair, spread, volatility in results if spread is not None])

    if len(valid_results) == 0:
        return []

    # Extract spreads and volatilities
    spreads = valid_results[:, 1].astype(float)
    volatilities = valid_results[:, 2].astype(float)

    # Normalize spreads and volatilities
    normalized_spreads = (spreads - spreads.min()) / (spreads.max() - spreads.min())
    normalized_volatilities = (volatilities - volatilities.min()) / (volatilities.max() - volatilities.min())
    combined_scores = (normalized_spreads + normalized_volatilities) / 2

    # sort according to combined_scores (of spreads and volatilities)
    sorted_indices = np.argsort(combined_scores)

    # Select the top target_count pairs
    return valid_results[sorted_indices[:target_count], 0].tolist()
