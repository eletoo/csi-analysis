# I used the Fitter library which uses SciPy library for distribution fitting and supports 80 distributions
import os

import fitter
from fitter import Fitter, get_common_distributions, get_distributions
import pandas as pd


def fit_by_sc(df, unnecessary_plots):
    if not os.path.exists("fit_by_sc_2"):
        os.mkdir("fit_by_sc_2")

    if not os.path.exists("fit_by_sc"):
        os.mkdir("fit_by_sc")

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

    fit(df, fitter.get_common_distributions(), 'fit_by_sc')
    fit(df, distributions, 'fit_by_sc_2')


def fit(df, distributions, path):
    for title in df:

        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions,
                   timeout=30, density=True)
        f.fit()
        print("fitting " + title)
        f.summary().to_csv(path + '\\Fitting' + title + '.csv', sep='\t', index=True)
