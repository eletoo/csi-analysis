import os
import pandas as pd
import matplotlib.pyplot as pl
from fitter import Fitter, get_common_distributions
from fitting_by_sc import fit_distributions_and_save_params

import histograms_plotter


def plot_merged_data(df, distributions):
    if not os.path.exists("merged_plot"):
        os.mkdir("merged_plot")

    new_df = pd.DataFrame(dtype=float)
    for title in df:
        new_df = new_df.assign(title=df[title])

    histograms_plotter.plot(new_df, new_df.mean(), "Merged data histogram", '\\merged_plot')
    fit_merged_data(new_df, os.getcwd() + '\\merged_plot', distributions)
    plot_increments_histogram(new_df)


def fit_merged_data(df, path, distributions):
    df1 = df.diff().drop(labels=0, axis=0)
    f = Fitter(df1 - df1.mean(), xmin=-150, xmax=150, bins=100,
               distributions=distributions.keys(),
               timeout=30, density=True)
    file = open(path + '\\Fitting Increments of merged Data.txt', "w")
    fit_distributions_and_save_params(distributions, f, file)
    f.summary().to_csv(path + '\\Fitting Increments of Merged Data.csv', sep='\t', index=True)


def plot_increments_histogram(df):
    df.diff().hist(bins=100)
    pl.xlabel('Increment')
    pl.ylabel('Frequency')
    pl.title('Merged data Increments')
    pl.savefig(os.getcwd() + '\\merged_plot\\figure Merged data Increments.png')
    pl.close()
