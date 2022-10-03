import os

import matplotlib.pyplot as pl


def plot_increments_for_sc(df, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "increments_hist")):
        os.mkdir(os.path.join(path, "increments_hist"))

    plot(df.diff(), path)
    sum = 0
    for column in df.diff().drop(labels=0, axis=0):
        sum = sum + df.diff().drop(labels=0, axis=0)[column].mean()
    with open(os.path.join(path, "mean_increments.txt"), "w") as f:
        f.write(str(sum / len(df.columns)))


def plot(df, path):
    for title in df:
        df[title].hist(bins=100)
        pl.xlabel('Increment')
        pl.ylabel('Frequency')
        pl.title(title)
        pl.savefig(os.path.join(os.getcwd(), path, 'increments_hist', 'figure' + str(title) + '.png'))
        print("Plotting histogram " + str(title))
        pl.close()
