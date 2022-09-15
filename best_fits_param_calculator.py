import os

import pandas as pd
from fitter import Fitter
import matplotlib.pyplot as pl


def calculate_best_params(df: pd.DataFrame, distributions, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(os.getcwd(), path, "best_fits_params")):
        os.mkdir(os.path.join(os.getcwd(), path, "best_fits_params"))

    if not os.path.exists(os.path.join(os.getcwd(), path, "best_fits_params", "subcarriers")):
        os.mkdir(os.path.join(os.getcwd(), path, "best_fits_params", "subcarriers"))

    df1 = df.diff().drop(labels=0, axis=0)

    fitted_results = {}

    for title in df:  # columns stay the same in df and df1
        f = Fitter(df1[title] - df1[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)
        f.fit()
        fitted_results[title] = f.fitted_param
        print("fitting increments of " + title)
        file = open(os.path.join(path,
                                 'best_fits_params', 'subcarriers',
                                 'Parameters of best five distributions on ' + title + 'Increments.txt'),
                    "w")
        for dist, values in f.fitted_param.items():
            if dist in distributions.keys():
                file.write(f"{dist} - (")
                params = [x.name for x in distributions.get(dist)._shape_info()] + ["location", "scale"]
                for pname, pval in zip(params, values):
                    file.write("{}:\t{:.8f}\t".format(pname, pval))
                file.write(")\n")

        file.close()

    plot_parameters(distributions, fitted_results, path)


def plot_parameters(distributions, fitted_results, path):
    for distribution in distributions.keys():
        params = [x.name for x in distributions.get(distribution)._shape_info()] + ["location", "scale"]
        for i, param in enumerate(params):
            data = []
            for sc in fitted_results.keys():
                data.append(fitted_results[sc][distribution][i])
            pl.plot(data)
            pl.xlabel('Sub-carriers')
            pl.ylabel(param)
            pl.title(distribution)
            if not os.path.exists(os.path.join(os.getcwd(), path, "best_fits_params", distribution)):
                os.mkdir(os.path.join(os.getcwd(), path, "best_fits_params", distribution))
            pl.savefig(os.path.join(os.getcwd(), path, "best_fits_params", distribution, f"{param}.png"))
            pl.close()
