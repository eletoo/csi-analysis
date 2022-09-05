from scipy.stats import chisquare


# todo: test not working yet
def test(df, distributions):
    # Null Hypothesis:
    # The data follow a specified distribution.

    # Alternate Hypothesis:
    # The data do not follow the specified distribution.

    # As an output, we get two values from the test:
    # - statistic value (which can be used to decide upon hypothesis when compared to the critical values)
    # - p-value

    # Assumed significance value = 0.05
    alpha = 0.05

    for title in df:
        for dist in distributions:
            stat, pval = chisquare(df[title], dist)
            if pval > alpha:
                print("Accepted null hypothesis for distribution " + dist)
