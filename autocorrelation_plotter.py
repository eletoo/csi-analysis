import os
import pandas as pd
from matplotlib import pyplot as pl
from statsmodels.graphics.tsaplots import plot_acf


def plot_autocorrelation(df, unnecessary_plots):
    if not os.path.exists("auto-correlation_graphs"):
        os.mkdir("auto-correlation_graphs")

    for title in df:
        if title in unnecessary_plots:
            del df[title]

    for title in df:
        df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])
        plot(df, title)


def plot(df, title):
    plot_acf(df[title], lags=(df[title].size - 1))
    pl.xlabel('Packet')
    pl.ylabel('Auto-correlation coefficient')
    pl.title("Auto-correlation " + title)
    pl.savefig(os.getcwd() + '\\auto-correlation_graphs\\figure' + title + '.png')
    print("Plotting figure " + title)
    pl.close()
