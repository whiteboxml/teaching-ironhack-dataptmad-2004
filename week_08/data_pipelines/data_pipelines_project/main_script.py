import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man
from p_reporting import m_reporting as mre


def argument_parser():
    parser = argparse.ArgumentParser(description='Set chart type')
    parser.add_argument("-p", "--path", help="specify companies list file", type=str)
    parser.add_argument("-k", "--key", help="quandl API key", type=str)
    args = parser.parse_args()
    return args


def main(arguments):

    print('starting pipeline...')

    prices_dfs = mac.acquire(arguments.path, arguments.key)

    stocks = mwr.build_data(prices_dfs)

    returns = man.compute_returns(stocks)
    risk_ratios = man.compute_risk_ratio(returns)

    top_return_risk_companies = risk_ratios.nlargest(10, 'Ratio')
    returns_corr = man.compute_corr(returns[top_return_risk_companies['Company'].to_list()])

    mre.report(top_return_risk_companies, returns_corr)

    print('========================= Pipeline is complete. You may find the results in the folder '
          './data/results =========================')


if __name__ == '__main__':
    main(argument_parser())
