import os
from matplotlib import pyplot as pl
from statsmodels.graphics.tsaplots import plot_acf


def plot_autocorrelation(df):
    if not os.path.exists("auto-correlation_graphs"):
        os.mkdir("auto-correlation_graphs")

    if not os.path.exists("auto-correlation_through_formulae"):
        os.mkdir("auto-correlation_through_formulae")

    for title in df:
        plot(df, title, 500)


def plot(df, title, tau_max):
    # plot_acf(df[title], lags=500, use_vlines=True, alpha=None)
    data = []
    for tau in range(0, tau_max + 1):
        data.append(autocorrelation(df, title, tau_max, tau))
    pl.plot(data)
    pl.xlabel('Packet')
    pl.ylabel('Auto-correlation coefficient')
    pl.title("Auto-correlation " + title)
    pl.grid(visible=True)
    pl.savefig(os.path.join(os.getcwd(), 'auto-correlation_through_formulae', 'figure' + title + '.png'))
    print("Plotting figure " + title)
    pl.close()


def autocovariance(df, title, tau_max, tau):
    mean = float(df[title].mean())
    coefficient = 1 / (df[title].size - tau_max)
    sum = 0
    for j in range(0, df[title].size - tau_max):
        sum = sum + (df[title][j] - mean) * (df[title][j + tau] - mean)
    return coefficient * sum


def autocorrelation(df, title, tau_max, tau):
    return autocovariance(df, title, tau_max, tau) / float(df[title].std()) ** 2
