from decimal import Decimal


# def normpdf(x, mean, sd):
#     var = float(sd) ** 2
#     denom = (2 * math.pi * var) ** .5
#     num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
#     return num / denom


def mutual_info(mean_csi, csi, q_inc, q_ampl, problist):
    # conditional probability of P(A|A_mean) is computed as the probability of drawing the increment delta_t from the
    # gaussian distribution of the increments and obtaining A by adding delta_t to A_mean
    pcsi_given_mean_csi = Decimal(1)
    for i in range(len(csi)):
        val = Decimal(csi[i] - mean_csi.iloc[0][i])
        if val < -2 ** (q_inc - 1) + 1 or val >= 2 ** (
                q_inc - 1):  # TODO: all CSIs satisfy this condition at some point
            # pcsi_given_mean_csi *= Decimal(10 ** -10)
            pcsi_given_mean_csi = Decimal(0)
            break
        # else:
        pcsi_given_mean_csi *= Decimal(problist[int(val)])

    # pcsi
    pcsi = Decimal(1 / (2 ** (
            Decimal(q_ampl) * Decimal(len(csi)))))  # TODO: len(csi) == 242, this is always going to be equal to 0
    # pmeancsi
    pmean = Decimal(1 / (2 ** (
            Decimal(q_ampl) * Decimal(len(csi)))))  # TODO: len(csi) == 242, this is always going to be equal to 0

    # logapprox = 2 * ((pcsi_given_mean_csi - pcsi) / (pcsi_given_mean_csi + pcsi))
    # return pcsi_given_mean_csi * pmean * Decimal.ln(pcsi_given_mean_csi) - pcsi_given_mean_csi * pcsi * Decimal.ln(
    #         pcsi) if pcsi_given_mean_csi != 0 else 0
    # logapprox = pcsi_given_mean_csi / pcsi - 1
    return pcsi_given_mean_csi * (pcsi_given_mean_csi - pmean)


def int_mi(df_quant_A, mean_csi_A, q_inc, q_ampl, problist):
    """
    Compute the mutual information between each row of the input dataframe (CSI) and a reference CSI of the same df
    :param mean_csi_A: reference CSI
    :param df_quant_A: input dataframe
    :param q_inc: number of bits used to quantize the incrments
    :param q_ampl: number of bits used to quantize the amplitude
    :param problist: list of probabilities of extracting an increment from the quantized distribution
    :return: internal mutual information
    """
    int_info = 0
    for i in range(len(df_quant_A) - 1):
        int_info += mutual_info(mean_csi_A, df_quant_A.iloc[i], q_inc, q_ampl, problist)
    return int_info

# def ext_mi(df_quant_A, mean_csi_A, df_quant_B, mean_csi_B):
#     """
#     Compute the mutual information between each row of the input df (CSI) and a reference CSI from a different df
#     :param df_quant_A: input dataframe representing experiment A
#     :param mean_csi_A: reference CSI of experiment A
#     :param df_quant_B: input dataframe representing experiment B
#     :param mean_csi_B: reference CSI of experiment B
#     :return: external mutual information I(mean_A, B) and I(mean_B, A)
#     """
#     ext_info_AB = 0
#     for i in range(len(df_quant_B)):
#         ext_info_AB += mutual_info(mean_csi_A, df_quant_B.iloc[i])
#
#     ext_info_BA = 0
#     for i in range(len(df_quant_A)):
#         ext_info_BA += mutual_info(mean_csi_B, df_quant_A.iloc[i])
#     return ext_info_AB, ext_info_BA
