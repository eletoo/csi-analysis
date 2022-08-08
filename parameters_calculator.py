import os


def calculate_params(df):
    if not os.path.exists("params"):
        os.mkdir("params")

    calculate_variance(df)
    calculate_skewness(df)
    calculate_kurtosis(df)


def calculate_variance(df):
    to_print = ["VARIANCE\n"]
    for title in df:
        numerator = 0
        for data in df[title]:
            numerator += pow((data - df[title].mean()), 2)
        variance = numerator / (df[title].size - 1)
        to_print.append("\n" + title + ":\t" + str(variance))

    f = open("params\\variance.txt", "w")
    for value in to_print:
        f.write(value)
    f.close()


def calculate_skewness(df):
    to_print = ["SKEWNESS\n"]
    for title in df:
        numerator = 0
        for data in df[title]:
            numerator += pow((data - df[title].mean()), 3)
        skewness = numerator / pow(df[title].std(), 3) / df[title].size
        to_print.append("\n" + title + ":\t" + str(skewness))

    f = open("params\\skewness.txt", "w")
    for value in to_print:
        f.write(value)
    f.close()


def calculate_kurtosis(df):
    to_print = ["KURTOSIS\n"]
    for title in df:
        numerator = 0
        for data in df[title]:
            numerator += pow((data - df[title].mean()), 4)
        skewness = (numerator / pow(df[title].std(), 4) / df[title].size) - 3
        to_print.append("\n" + title + ":\t" + str(skewness))

    f = open("params\\kurtosis.txt", "w")
    for value in to_print:
        f.write(value)
    f.close()
