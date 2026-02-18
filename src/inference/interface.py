"""Module inference/interface.py"""

import boto3
import pandas as pd

import src.elements.attribute as atr
import src.elements.master as mr
import src.elements.s3_parameters as s3p
import src.elements.specification as sc
import src.inference.approximating
import src.inference.plausible_anomalies
import src.inference.scaling


class Interface:
    """
    Interface
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: An instance of boto3.session.Session<br>
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        :param arguments: A set of arguments vis-à-vis computation & storage objectives.<br>
        """

        # Setting up
        self.__scaling = src.inference.scaling.Scaling()
        self.__approximating = src.inference.approximating.Approximating()
        self.__plausible_anomalies = src.inference.plausible_anomalies.PlausibleAnomalies(
            connector=connector, s3_parameters=s3_parameters, arguments=arguments)

    def exc(self, attribute: atr.Attribute, data: pd.DataFrame, specification: sc.Specification) -> pd.DataFrame:
        """

        :param attribute:
        :param data:
        :param specification:
        :return:
        """

        if data.empty | (not attribute.scaling) | (not attribute.modelling) :
            return data

        transforms: pd.DataFrame = self.__scaling.transform(data=data, scaling=attribute.scaling)
        master: mr.Master = mr.Master(data=data, transforms=transforms)
        estimates: pd.DataFrame = self.__approximating.exc(
            specification=specification, attribute=attribute, master=master)
        estimates: pd.DataFrame = self.__plausible_anomalies.exc(
            estimates=estimates.copy(), specification=specification)

        return estimates
