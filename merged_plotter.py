import os
import pandas as pd

import histograms_plotter


def plot_merged_data(df):
    if not os.path.exists("merged_plot"):
        os.mkdir("merged_plot")

    new_df = pd.DataFrame(dtype=float)
    for title in df:
        new_df = new_df.assign(title=df[title])

    histograms_plotter.plot(new_df, new_df.mean(), "Merged data histogram", '\\merged_plot')
