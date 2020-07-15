import pandas as pd
import quandl


# acquisition functions


def get_tickers(path):
    companies = pd.read_csv(path)
    ticker_list = companies['Ticker'].to_list()
    print('retrieved', str(len(ticker_list)), 'ticker symbols...')
    return ticker_list


def setup_quandl(api_key):
    quandl.ApiConfig.api_key = api_key


def get_prices(ticker):
    print(f'getting prices data for company: {ticker}...')

    prices_full = quandl.get(f'WIKI/{ticker}')
    prices_full.to_csv(f'./data/raw/{ticker}.csv', index=False)
    prices = prices_full['Adj. Close'].reset_index()
    prices['Ticker'] = ticker
    return prices


def acquire(path, api_key):
    print('setting quandl api key...')
    setup_quandl(api_key)

    print(f'reading data from {path}...')
    tickers = get_tickers(path)

    print('getting data from quandl...')
    prices_dfs = []
    for ticker in tickers:
        prices = get_prices(ticker)
        prices_dfs.append(prices)

    return prices_dfs
