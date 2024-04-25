import os

import numpy as np


def save_mutual_info(df, path: str = ""):
    """
    :param df: dataframe containing the data to be processed
    :param path: folder path where to save the output of the code, can be an empty string
    :return: None
    """
    # compute mutual information between two consecutive rows of the dataframe
    mi = []
    for i in range(len(df) - 1):
        # todo: we have to compute probabilities, we can't use pure data to compute mutual information
        mi.append(mutual_information(df.iloc[i], df.iloc[i + 1]))
    # save mutual information to a file
    np.savetxt(os.path.join(path, 'mutual_info.txt'), mi, delimiter='\n')


def mutual_information(prob: float, joint_prob: float) -> float:
    """
    :param prob: probability of x
    :param joint_prob: probability of x given y
    :return: mutual information between x and y, symmetric to the mutual information between y and x
    """
    for i in range(len(prob)):
        if prob[i] < 0:
            raise Exception("Probability must be greater than 0")
        if prob[i] > 1:
            raise Exception("Probability must be less than 1")
    for i, j in range(len(joint_prob)):
        if joint_prob[i, j] < 0:
            raise Exception("Probability must be greater than 0")
        if joint_prob[i, j] > 1:
            raise Exception("Probability must be less than 1")
    return entropy(prob) - conditional_entropy(joint_prob, prob)


def entropy(prob: float) -> float:
    """
    :param prob: probability of the event
    :return: entropy of the event
    """
    for i in range(len(prob)):
        if prob[i] < 0:
            raise Exception("Probability must be greater than 0")
        if prob[i] > 1:
            raise Exception("Probability must be less than 1")
    return -np.sum(prob * np.log2(prob))  # H(X) = -sum(p(x) * log2(p(x)))


def conditional_entropy(joint_prob: float, y_prob: float) -> float:
    """
    :param joint_prob: joint probability of x and y
    :param y_prob: probability of event y
    :return: conditional entropy of x given y
    """
    for i in range(len(joint_prob)):
        if joint_prob[i] < 0 or y_prob < 0:
            raise Exception("Probability must be greater than 0")
        if joint_prob[i] > 1 or y_prob > 1:
            raise Exception("Probability must be less than 1")
    # joint_prob has dimension (n, m) where n is the number of events of x and m is the number of events of y
    # todo: it's never going to work because joint_prob is bidimensional and sum cannot be applied to it
    return -np.sum(joint_prob * np.log2(joint_prob / y_prob))  # H(X|Y) = -sum(p(x,y) * log2(p(x,y)/p(y)))
