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

    fit(df, fitter.get_common_distributions(), unnecessary_plots, 'fit_by_sc')
    fit(df, distributions, unnecessary_plots, 'fit_by_sc_2')


def fit(df, distributions, unnecessary_plots, path):
    for title in df:
        if title not in unnecessary_plots:
            sc_data = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

            f = Fitter(sc_data - sc_data.mean(), xmin=-150, xmax=150, bins=100,
                       distributions=distributions,  # considers only the 10 most common distributions
                       timeout=30, density=True)
            f.fit()
            print("fitting " + title)
            f.summary().to_csv(path + '\\Fitting' + title + '.csv', sep='\t', index=True)
