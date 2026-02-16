"""Module inference/interface.py"""

import pandas as pd

import src.elements.attribute as atr
import src.elements.master as mr
import src.elements.specification as sc
import src.inference.approximating
import src.inference.plausible_anomalies
import src.inference.scaling


class Interface:
    """
    Interface
    """

    def __init__(self):
        """

        Constructor
        """

        # Setting up
        self.__scaling = src.inference.scaling.Scaling()
        self.__approximating = src.inference.approximating.Approximating()
        self.__plausible_anomalies = src.inference.plausible_anomalies.PlausibleAnomalies()

    def exc(self, attribute: atr.Attribute, data: pd.DataFrame, specification: sc.Specification) -> pd.DataFrame:
        """

        :param attribute:
        :param data:
        :param specification:
        :return:
        """

        transforms: pd.DataFrame = self.__scaling.transform(data=data, scaling=attribute.scaling)
        master: mr.Master = mr.Master(data=data, transforms=transforms)
        estimates: pd.DataFrame = self.__approximating.exc(
            specification=specification, attribute=attribute, master=master)
        estimates: pd.DataFrame = self.__plausible_anomalies.exc(
            estimates=estimates.copy(), specification=specification)

        return estimates
