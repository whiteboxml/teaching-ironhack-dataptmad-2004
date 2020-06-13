# analysis functions


def compute_returns(stocks):
    returns = stocks.pct_change()
    return returns


def compute_risk_ratio(returns_df):
    risk_ratios = returns_df.tail(30).agg(['mean', 'std']).T.reset_index()
    risk_ratios.columns = ['Company', 'Mean', 'Std']
    risk_ratios['Ratio'] = risk_ratios['Mean'] / risk_ratios['Std']
    return risk_ratios


def compute_corr(returns_df):
    corr_matrix = returns_df.tail(30).corr()
    return corr_matrix
