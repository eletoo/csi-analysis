import os

import pandas as pd
import matplotlib.pyplot as pl


def plot_increments_for_sc(df, unnecessary_plots):
    if not os.path.exists("increments_hist"):
        os.mkdir("increments_hist")

    for title in df:
        if title in unnecessary_plots:
            del df[title]

    for title in df:
        df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

    plot(df.diff())


def plot(df):
    for title in df:
        df[title].hist(bins=100)
        pl.xlabel('Increment')
        pl.ylabel('Frequency')
        pl.title(title)
        pl.savefig(os.getcwd() + '\\increments_hist\\figure' + title + '.png')
        print("Plotting histogram " + title)
        pl.close()
