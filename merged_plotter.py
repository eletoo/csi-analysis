import os
import pandas as pd
import matplotlib.pyplot as pl
from fitter import Fitter, get_common_distributions

import histograms_plotter


def plot_merged_data(df):
    if not os.path.exists("merged_plot"):
        os.mkdir("merged_plot")

    new_df = pd.DataFrame(dtype=float)
    for title in df:
        new_df = new_df.assign(title=df[title])

    histograms_plotter.plot(new_df, new_df.mean(), "Merged data histogram", '\\merged_plot')
    fit_merged_data(new_df, os.getcwd() + '\\merged_plot')
    plot_increments_histogram(new_df)


def fit_merged_data(df, path):
    distributions = ['beta',
                     'cauchy',
                     'chi',
                     'chi2',
                     'dgamma',
                     'f',
                     'foldcauchy',
                     'foldnorm',
                     'gamma',
                     'gennorm',
                     'halfcauchy',
                     'halfnorm',
                     'invgamma',
                     'invgauss',
                     'loggamma',
                     'lognorm',
                     'norm',
                     'powerlaw',
                     'powerlognorm',
                     'powernorm',
                     'rayleigh',
                     'wrapcauchy'
                     ]
    # distributions = get_common_distributions()

    f = Fitter(df - df.mean(), xmin=-150, xmax=150, bins=100,
               distributions=distributions,
               timeout=30, density=True)
    f.fit()
    f.summary().to_csv(path + '\\Fitting Merged Data.csv', sep='\t', index=True)


def plot_increments_histogram(df):
    df.hist(bins=100)
    pl.xlabel('Increment')
    pl.ylabel('Frequency')
    pl.title('Merged data Increments')
    pl.savefig(os.getcwd() + '\\merged_plot\\figure Merged data Increments.png')
    pl.close()
