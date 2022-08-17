# I used the Fitter library which uses SciPy library for distribution fitting and supports 80 distributions
import os

from fitter import Fitter, get_common_distributions, get_distributions
import scipy.stats as s


def fit_data_by_sc(df):
    if not os.path.exists("fit_by_sc_2"):
        os.mkdir("fit_by_sc_2")

    if not os.path.exists("fit_by_sc"):
        os.mkdir("fit_by_sc")

    if not os.path.exists("fit_increments\\Values"):
        os.mkdir("fit_increments\\Values")

    distributions = {
        "beta": s.beta,
        "cauchy": s.cauchy,
        "chi": s.chi,
        "chi2": s.chi2,
        "dgamma": s.dgamma,
        "f": s.f,
        "foldcauchy": s.foldcauchy,
        "foldnorm": s.foldnorm,
        "gamma": s.gamma,
        "gennorm": s.gennorm,
        "halfcauchy": s.halfcauchy,
        "halfnorm": s.halfnorm,
        "invgauss": s.invgauss,
        "invgamma": s.invgamma,
        "loggamma": s.loggamma,
        "lognorm": s.lognorm,
        "norm": s.norm,
        "powerlaw": s.powerlaw,
        "powerlognorm": s.powerlognorm,
        "powernorm": s.powernorm,
        "rayleigh": s.rayleigh,
        "wrapcauchy": s.wrapcauchy
    }

    # fit(df, fitter.get_common_distributions(), 'fit_by_sc')
    # fit(df, distributions, 'fit_by_sc_2')
    fit_increments(df.diff().drop(labels=0, axis=0), distributions, 'fit_increments')


def fit(df, distributions, path):
    for title in df:
        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)
        f.fit()
        print("fitting " + title)
        f.summary().to_csv(path + '\\Fitting' + title + '.csv', sep='\t', index=True)


def fit_increments(df, distributions, path):
    for title in df:
        print("fitting " + title)
        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)
        file = open(path + '\\Values\\Fitting' + title + 'Increments.txt', "w")
        f.fit()
        for dist, values in f.fitted_param.items():
            file.write(f"{dist} - (")
            params = [x.name for x in distributions.get(dist)._shape_info()] + ["location", "scale"]
            for pname, pval in zip(params, values):
                file.write("{}:\t{:.8f}\t".format(pname, pval))
            file.write(")\n")
        file.close()
        f.summary().to_csv(path + '\\Fitting' + title + 'Increments.csv', sep='\t', index=True)
