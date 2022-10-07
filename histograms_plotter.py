import os

import matplotlib
import pandas
from matplotlib import pyplot as pl


def is_stationary(batch_mean, column_mean):
    return abs(batch_mean - column_mean) < 0.1 * column_mean


def process_batch(column_mean, batch, size):
    sum = 0
    for value in batch:
        sum += abs(value)

    batch_mean = sum / size
    print(batch_mean)
    if not is_stationary(batch_mean, column_mean):
        print("Non stationary process")
        return False
    else:
        return True


def create_batches(data, length):
    return [data[i:i + length] for i in range(0, len(data), length)]


def plot_histogram_for_sc(title, df, size, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    col = df[title]

    print(title)
    column_mean = float(col.mean())
    print("Column mean:", column_mean)

    # plottable = True
    # for batch in create_batches(df, size):
    #   if process_batch(column_mean, batch[title], size):
    #      continue
    #   plottable = False

    # if plottable:
    #   plot(c, column_mean, title)

    # remove previous comments and instead comment the following three lines if the plot is only needed for
    # stationary processes
    for batch in create_batches(df, size):
        process_batch(column_mean, batch[title], size)
    plot(col, column_mean, title, 'histograms', path)


def plot(c: pandas.DataFrame, column_mean: float, title: str, dir_name: str, path: str):
    c = c - column_mean
    c.hist(bins=100, density=True)
    pl.xlabel('Magnitude')
    pl.ylabel('Relative frequency')
    pl.title(title)
    pl.xlim(-150, 150)
    # pl.show()
    pl.rcParams.update(
        {'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large', 'ytick.labelsize': 'large'})
    if not os.path.exists(os.path.join(path, "histograms")):
        os.mkdir(os.path.join(path, "histograms"))
    pl.savefig(os.path.join(os.getcwd(), path, dir_name, 'figure' + str(title) + '.pdf'))
    pl.close()
