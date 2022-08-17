import os


def calculate_params(df):
    if not os.path.exists("params"):
        os.mkdir("params")

    df1 = df.diff()
    df1 = df1.drop(labels=0, axis=0)
    # calculate_variance(df, "params\\variance.txt")
    # calculate_skewness(df, "params\\skewness.txt")
    # calculate_kurtosis(df, "params\\kurtosis.txt")
    calculate_variance(df1, "params\\increments_variance.txt")
    calculate_skewness(df1, "params\\increments_skewness.txt")
    calculate_kurtosis(df1, "params\\increments_kurtosis.txt")


def calculate_variance(df, path):
    to_print = ["VARIANCE\n"]
    for title in df:
        numerator = 0
        for data in df[title]:
            numerator += pow((data - df[title].mean()), 2)
        variance = numerator / (df[title].size - 1)
        to_print.append("\n" + title + ":\t" + str(variance))

    f = open(path, "w")
    for value in to_print:
        f.write(value)
    f.close()


def calculate_skewness(df, path):
    to_print = ["SKEWNESS\n"]
    for title in df:
        numerator = 0
        for data in df[title]:
            numerator += pow((data - df[title].mean()), 3)
        skewness = numerator / pow(df[title].std(), 3) / df[title].size
        to_print.append("\n" + title + ":\t" + str(skewness))

    f = open(path, "w")
    for value in to_print:
        f.write(value)
    f.close()


def calculate_kurtosis(df, path):
    to_print = ["KURTOSIS\n"]
    for title in df:
        numerator = 0
        for data in df[title]:
            numerator += pow((data - df[title].mean()), 4)
        skewness = (numerator / pow(df[title].std(), 4) / df[title].size) - 3
        to_print.append("\n" + title + ":\t" + str(skewness))

    f = open(path, "w")
    for value in to_print:
        f.write(value)
    f.close()
