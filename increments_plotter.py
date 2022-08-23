import os

import matplotlib.pyplot as pl


def plot_increments_for_sc(df):
    if not os.path.exists("increments_hist"):
        os.mkdir("increments_hist")

    plot(df.diff())


def plot(df):
    for title in df:
        df[title].hist(bins=100)
        pl.xlabel('Increment')
        pl.ylabel('Frequency')
        pl.title(title)
        pl.savefig(os.path.join(os.getcwd(), 'increments_hist', 'figure' + title + '.png'))
        print("Plotting histogram " + title)
        pl.close()
