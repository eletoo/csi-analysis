import os
from matplotlib import pyplot as pl
from statsmodels.graphics.tsaplots import plot_acf


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
    # plot_acf(df[title], lags=500, use_vlines=True, alpha=None)
    data = []
    var = float(df[title].std()) ** 2
    for tau in range(1, tau_max + 2):
        data.append(autocorrelation(df, title, tau_max, tau, var))
    pl.plot(data)
    pl.xlabel('Packet')
    pl.ylabel('Auto-correlation coefficient')
    pl.title("Auto-correlation " + str(title))
    pl.grid(visible=True)
    pl.savefig(os.path.join(os.getcwd(), path, 'auto-correlation_through_formulae', 'figure' + str(title) + '.png'))
    print("Plotting figure " + str(title))
    pl.close()


def autocovariance(df, title, tau_max, tau):
    mean = float(df[title].mean())
    coefficient = 1 / (df[title].size - (df[title].size - tau))  # (df[title].size - tau) = tau_max
    sum = 0
    for j in range(1, df[title].size - (df[title].size - tau) + 1):  # (df[title].size - tau) = tau_max
        sum = sum + (df[title][j] - mean) * (df[title][j + tau] - mean)
    return coefficient * sum


def autocorrelation(df, title, tau_max, tau, var):
    return autocovariance(df, title, tau_max, tau) / var
