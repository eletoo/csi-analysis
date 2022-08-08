import os
from matplotlib import pyplot as pl
from statsmodels.graphics.tsaplots import plot_acf


def plot_autocorrelation(df):
    if not os.path.exists("auto-correlation_graphs"):
        os.mkdir("auto-correlation_graphs")

    for title in df:
        plot(df, title)


def plot(df, title):
    plot_acf(df[title], lags=500, use_vlines=True, alpha=None)
    pl.xlabel('Packet')
    pl.ylabel('Auto-correlation coefficient')
    pl.title("Auto-correlation " + title)
    pl.grid(visible=True)
    pl.savefig(os.getcwd() + '\\auto-correlation_graphs\\figure' + title + '.png')
    print("Plotting figure " + title)
    pl.close()
