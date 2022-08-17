# I used the Fitter library which uses SciPy library for distribution fitting and supports 80 distributions
import os

import fitter
from fitter import Fitter, get_common_distributions, get_distributions


def fit_data_by_sc(df):
    if not os.path.exists("fit_by_sc_2"):
        os.mkdir("fit_by_sc_2")

    if not os.path.exists("fit_by_sc"):
        os.mkdir("fit_by_sc")

    if not os.path.exists("fit_increments"):
        os.mkdir("fit_increments")

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

    # fit(df, fitter.get_common_distributions(), 'fit_by_sc')
    # fit(df, distributions, 'fit_by_sc_2')
    fit_increments(df.diff().drop(labels=0, axis=0), distributions, 'fit_increments')


def fit(df, distributions, path):
    for title in df:
        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions,
                   timeout=30, density=True)
        f.fit()
        print("fitting " + title)
        f.summary().to_csv(path + '\\Fitting' + title + '.csv', sep='\t', index=True)


def fit_increments(df, distributions, path):
    for title in df:
        f = Fitter(df[title], bins=100,
                   distributions=distributions,
                   timeout=30)
        f.fit()
        print("fitting " + title)
        f.summary().to_csv(path + '\\Fitting' + title + 'Increments.csv', sep='\t', index=True)
