import os

import pandas
import pandas as pd
import matplotlib.pyplot as pl
from fitter import Fitter, get_common_distributions
from fitting_by_sc import fit_distributions_and_save_params

import histograms_plotter


def plot_merged_data(df: pandas.DataFrame, distributions, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "merged_plot")):
        os.mkdir(os.path.join(path, "merged_plot"))

    new_df = pd.DataFrame(dtype=float)
    for title in df:
        new_df = new_df.assign(title=df[title])

    histograms_plotter.plot(new_df, new_df.mean(), "Merged data histogram", os.path.join(path, 'merged_plot'))
    fit_merged_data_increments(new_df, os.path.join(os.getcwd(), path, 'merged_plot'), distributions)
    plot_merged_increments_histogram(new_df, path)


def fit_merged_data_increments(df: pandas.DataFrame, path: str, distributions):
    df1 = df.diff().drop(labels=0, axis=0)
    f = Fitter(df1 - df1.mean(), xmin=-150, xmax=150, bins=100,
               distributions=distributions.keys(),
               timeout=30, density=True)
    file = open(os.path.join(path, 'Parameters of distributions after fitting Increments of merged Data.txt'), "w")
    fit_distributions_and_save_params(distributions, f, file)
    f.summary().to_csv(os.path.join(path, 'Best five distributions fitting Increments of Merged Data.csv'), sep='\t',
                       index=True)


def plot_merged_increments_histogram(df: pandas.DataFrame, path):
    df.diff().hist(bins=100)
    pl.xlabel('Increment')
    pl.ylabel('Frequency')
    pl.title('Merged data Increments')
    pl.savefig(os.path.join(os.getcwd(), path, 'merged_plot', 'figure Merged data Increments.png'))
    pl.close()
