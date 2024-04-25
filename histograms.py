import os

import pandas
from matplotlib import pyplot as pl


def is_stationary(batch_mean, column_mean):
    """
    :param batch_mean: mean of the batch of data
    :param column_mean: mean of the column
    :return: true if the process (data) is stationary, false otherwise
    """
    # process is stationary if the mean of each portion of data (batch) is the same as mean of all the dataset (column)
    # we consider the means to be the same if they lie within 10% of each other
    return abs(batch_mean - column_mean) < 0.1 * column_mean


def create_batches(data, length):
    # create batches of data of size length
    return [data[i:i + length] for i in range(0, len(data), length)]


def plot_histogram_for_sc(title, df, size, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    col = df[title]

    # print(title)
    column_mean = float(col.mean())
    # print("Column mean:", column_mean)
    # print("Column std:", col.std())
    # print("Column kurtosis:", col.kurtosis())
    # print("Column skewness:", col.skew())
    for batch in create_batches(df, size):
        s = 0
        for value in batch[title]:
            s += abs(value)

        batch_mean = s / size
        # print(batch_mean)
        if not is_stationary(batch_mean, column_mean):
            print(title + " Non stationary process")
        else:
            print(title + " Stationary process")
    plot(col, column_mean, title, 'histograms', path)


def plot(c: pandas.DataFrame, column_mean: float, title: str, dir_name: str, path: str):
    c = c - column_mean
    c.hist(bins=100, density=True)
    pl.xlabel('Magnitude')
    pl.ylabel('Relative frequency')
    pl.title(title)
    # pl.xlim(-500, 500)
    # pl.show()
    pl.rcParams.update(
        {'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large', 'ytick.labelsize': 'large'})
    if not os.path.exists(os.path.join(path, "histograms")):
        os.mkdir(os.path.join(path, "histograms"))
    pl.savefig(os.path.join(os.getcwd(), path, dir_name, 'figure' + str(title) + '.pdf'))
    pl.close()
