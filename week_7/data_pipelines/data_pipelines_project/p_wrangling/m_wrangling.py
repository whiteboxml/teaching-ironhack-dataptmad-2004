import pandas as pd


# wrangling functions

def build_data(prices_dfs):
    print('building data...')
    prices_df = pd.concat(prices_dfs, sort=True).reset_index()
    prices_df_clean = prices_df.pivot_table(values='Adj. Close',
                                            index='Date',
                                            columns='Ticker')
    return prices_df_clean
