import os
import pandas as pd


def calculate_params(df, unnecessary_plots):
    if not os.path.exists("params"):
        os.mkdir("params")

    calculate_variance(df, unnecessary_plots)
    calculate_skewness(df, unnecessary_plots)
    calculate_kurtosis(df, unnecessary_plots)


def calculate_variance(df, unnecessary_plots):
    to_print = ["VARIANCE\n"]
    for title in df:
        numerator = 0
        if title not in unnecessary_plots:
            sc_data = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])
            for data in sc_data:
                numerator += pow((data - sc_data.mean()), 2)
            variance = numerator / (df[title].size - 1)
            to_print.append("\n" + title + ":\t" + str(variance.values))
    f = open("params\\variance.txt", "w")
    for value in to_print:
        f.write(value)
    f.close()


def calculate_skewness(df, unnecessary_plots):
    to_print = ["SKEWNESS\n"]
    for title in df:
        numerator = 0
        if title not in unnecessary_plots:
            sc_data = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])
            for data in sc_data:
                numerator += pow((data - sc_data.mean()), 3)
            skewness = numerator / pow(sc_data.std(), 3) / df[title].size
            to_print.append("\n" + title + ":\t" + str(skewness.values))
    f = open("params\\skewness.txt", "w")
    for value in to_print:
        f.write(value)
    f.close()


def calculate_kurtosis(df, unnecessary_plots):
    to_print = ["KURTOSIS\n"]
    for title in df:
        numerator = 0
        if title not in unnecessary_plots:
            sc_data = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])
            for data in sc_data:
                numerator += pow((data - sc_data.mean()), 4)
            skewness = (numerator / pow(sc_data.std(), 4) / df[title].size) - 3
            to_print.append("\n" + title + ":\t" + str(skewness.values))
    f = open("params\\kurtosis.txt", "w")
    for value in to_print:
        f.write(value)
    f.close()
