import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# reporting functions

def plot_returns(df, x, y, length=8, width=14, title=""):
    df = df.sort_values(x, ascending=False)
    plt.figure(figsize=(width, length))
    chart = sns.barplot(data=df, x=x, y=y)
    plt.title(title + "\n", fontsize=16)
    return chart


def correlation_plot(corr, title=""):
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    plt.subplots(figsize=(15, 10))
    cmap = sns.diverging_palette(6, 255, as_cmap=True)
    chart = sns.heatmap(corr,
                        mask=mask,
                        cmap=cmap,
                        center=0,
                        linewidths=.5,
                        annot=True,
                        fmt='.2f')
    plt.title(title, fontsize=16)
    return chart


def save_viz(chart, title):
    fig = chart.get_figure()
    fig.savefig(f'./data/results/{title}.png')


def report(top_return_risk_companies, returns_corr):
    bar_plot = plot_returns(top_return_risk_companies,
                            'Ratio',
                            'Company',
                            title='Stock Return vs. Risk Ratios')

    corr_plot = correlation_plot(returns_corr, title='Stock Return Correlation')

    save_viz(bar_plot, 'bar_plot_top_risk_companies')
    save_viz(corr_plot, 'corr_plot_stock_returns')
