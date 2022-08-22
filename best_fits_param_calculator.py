import os

import pandas as pd
from fitter import Fitter


def calculate_best_params(df: pd.DataFrame, distributions):
    if not os.path.exists("best_fits_params"):
        os.mkdir("best_fits_params")

    if not os.path.exists(os.path.join("best_fits_params", "subcarriers")):
        os.mkdir(os.path.join("best_fits_params", "subcarriers"))

    df1 = df.diff().drop(labels=0, axis=0)

    for title in df:  # columns stay the same in df and df1
        f = Fitter(df1[title] - df1[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)
        f.fit()
        print("fitting increments of " + title)
        file = open(os.path.join(
            'best_fits_params', 'subcarriers', 'Parameters of best five distributions on ' + title + 'Increments.txt'),
            "w")
        for dist, values in f.fitted_param.items():
            if dist in distributions.keys():
                file.write(f"{dist} - (")
                params = [x.name for x in distributions.get(dist)._shape_info()] + ["location", "scale"]
                for pname, pval in zip(params, values):
                    file.write("{}:\t{:.8f}\t".format(pname, pval))
                file.write(")\n")
        file.close()
