import os

import matplotlib.pyplot as pl


def plot_increments_for_sc(df, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "increments_hist")):
        os.mkdir(os.path.join(path, "increments_hist"))

    plot(df.diff(), path)


def plot(df, path):
    for title in df:
        df[title].hist(bins=100)
        pl.xlabel('Increment')
        pl.ylabel('Frequency')
        pl.title(title)
        pl.savefig(os.path.join(os.getcwd(), path, 'increments_hist', 'figure' + title + '.png'))
        print("Plotting histogram " + title)
        pl.close()
