import os
from matplotlib import pyplot as pl
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf, acovf


def plot_autocorrelation(df, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "auto-correlation_graphs")):
        os.mkdir(os.path.join(path, "auto-correlation_graphs"))

    if not os.path.exists(os.path.join(path, "auto-correlation_through_formulae")):
        os.mkdir(os.path.join(path, "auto-correlation_through_formulae"))

    for title in df:
        plot(df, title, 200, path)


def plot(df, title, tau_max, path):
    data = []
    #df = df.diff().drop(labels=0, axis=0)  # uncomment this line to plot autocorrelation of increments
    # plot_acf(df[title], lags=tau_max, use_vlines=False, title=title, alpha=None, marker='o')
    var = float(df[title].STD()) ** 2
    for tau in range(0, tau_max):
        # data.append(autocorrelation(df, title, tau_max, tau, var))
        data = autocorrelation(df, title, tau_max, tau, var)
    pl.plot(data)
    pl.xlabel('Tau')
    pl.ylabel('Auto-correlation')
    pl.title("Auto-correlation " + str(title))
    pl.rcParams.update(
        {'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large', 'ytick.labelsize': 'large'})
    pl.grid(visible=True)
    #pl.savefig(os.path.join(os.getcwd(), path, 'auto-correlation_graphs', 'figure' + str(title) + '.pdf')) #
    # uncomment this line to plot autocorrelation of increments

    pl.savefig(os.path.join(os.getcwd(), path, 'auto-correlation_through_formulae', 'figure' + str(title) + '.pdf'))
    print("Plotting figure " + str(title))
    pl.close()


def autocovariance(df, title, tau_max, tau):
    mean = float(df[title].mean())
    coefficient = 1 / (df[title].size - tau_max)  # (df[title].size - tau) = tau_max
    sum = 0
    for j in range(1, df[title].size - tau_max):  # (df[title].size - tau) = tau_max
        sum = sum + (df[title][j] - mean) * (df[title][j + tau] - mean)
    return coefficient * sum


def autocorrelation(df, title, tau_max, tau, var):
    # return autocovariance(df, title, tau_max, tau) / var
    c = acovf(df[title], nlag=tau_max)
    return c / c[0]
