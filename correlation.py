import os

from matplotlib import pyplot as pl
from statsmodels.tsa.stattools import acovf


def save_intercorr(df, path: str = "", mode: int = 0):
    """
    :param df: dataframe containing the data to be processed. If mode is 0, the dataframe must contain the increments of
                the original data (i.e. df.diff(axis=1)). If mode is 1, the dataframe must contain the original data
                (i.e. CSI packets).
    :param path: where to save the output of the code, can be an empty string
    :param mode: 0 for correlation of increments across adjacent subcarriers,
                1 for correlation of amplitude across subcarriers
    :return: None
    """
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "freq_correlation")):
        os.mkdir(os.path.join(path, "freq_correlation"))
    path = path + "/freq_correlation"

    if mode == 0:  # mode 0: plot correlation of increments across adjacent subcarriers
        df = df.diff(axis=1).drop(df.columns[0], axis=1)  # df.diff(axis=1)
        if not os.path.exists(os.path.join(path, "increments")):
            os.mkdir(os.path.join(path, "increments"))
        path = path + "/increments"
    elif mode == 1:  # mode 1: plot correlation of amplitude across subcarriers
        if not os.path.exists(os.path.join(path, "amplitude")):
            os.mkdir(os.path.join(path, "amplitude"))
        path = path + "/amplitude"

    for row in df.index:  # for each row (i.e. CSI) in the dataframe
        plot_interSC_corr(df, row, 200, path)


def save_autocorrelation(df, path: str = ""):
    """
    :param df: dataframe containing the data to be processed
    :param path: path where to save the output of the code, can be an empty string
    :return: None
    """
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "autocorrelation")):
        os.mkdir(os.path.join(path, "autocorrelation"))

    for title in df:
        plot_autocorrelation(df, title, 200, path)


def plot_autocorrelation(df, title, tau_max, path):
    """
    :param df: dataframe containing the data to be processed; columns are the subcarriers, rows are the time samples/CSI
    :param title: title of the figure to save, normally the name of the subcarrier for which we compute the ACF
    :param tau_max: maximum size of the window over which to compute the correlation (i.e. the lag parameter of the ACF)
    :param path: path where to save the figure
    :return: None
    """
    pl.plot(autocorrelation(df, title, tau_max, mode=1))
    pl.xlabel('Tau')
    pl.ylabel('Auto-correlation')
    pl.title("Auto-correlation " + str(title))
    pl.rcParams.update(
        {'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large', 'ytick.labelsize': 'large'})
    pl.grid(visible=True)
    pl.savefig(os.path.join(os.getcwd(), path, 'autocorrelation', 'figure' + str(title) + '.pdf'))
    # print("Plotting figure " + str(title))
    pl.close()


def plot_interSC_corr(df, ind, tau_max, path):
    """
    Computes the correlation of the data contained in the dataframe at position "ind" with the data at position "ind+1".
    :param df: dataframe containing the data to be processed; columns are the subcarriers, rows are either the time
                samples/CSI or the increments of the amplitude between two adjacent subcarriers
    :param ind: index of the dataframe to be processed (i.e. the CSI index)
    :param tau_max: maximum value of tau, the lag parameter of the autocorrelation function (i.e. "window" over which to
                    compute the correlation)
    :param path: where to save the output of the code, can be an empty string
    :return: None
"""
    pl.plot(autocorrelation(df, ind, tau_max, mode=0))
    pl.xlabel('Tau')
    pl.ylabel('Auto-correlation')
    pl.title("Inter-SC Correlation of CSI " + str(ind))
    pl.rcParams.update(
        {'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large', 'ytick.labelsize': 'large'})
    pl.grid(visible=True)
    pl.savefig(os.path.join(os.getcwd(), path, 'CSI' + str(ind) + '.pdf'))
    # print("Plotting figure " + str(ind))
    pl.close()


def autocorrelation(df, index, tau_max, mode: int = 0):
    """
    :param df: dataframe containing the data to be processed; columns are the subcarriers, rows are either the time
                samples/CSI or the increments of the amplitude between two adjacent subcarriers
    :param index: if mode is 0, column index of the dataframe to be processed (i.e. the subcarrier index); if mode is 1,
                    row index of the dataframe to be processed (i.e. the CSI index)
    :param tau_max: maximum value of tau, the lag parameter of the autocorrelation function (i.e. "window" over which to
                    compute the correlation)
    :param mode: 1 for autocorrelation of data contained in df (amplitude or increments depending on what is passed to
                    the method) at column index "index",
                0 for autocorrelation of the data contained in df at row index "index" (i.e. CSI number "index")
    :return: autocorrelation of data in df at position specified by index and according to the mode passed to the method
    """
    if mode == 0:
        c = acovf(df.iloc[index], nlag=tau_max)  # autocorrelation of the data of CSI "index" in the dataframe
    elif mode == 1:
        c = acovf(df[index], nlag=tau_max)  # autocorrelation of the data on subcarrier "index" in the dataframe
    return c / c[0]
