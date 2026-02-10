"""Module differences.py"""
import logging
import os

import pandas as pd

import config
import src.elements.specification as sc
import src.functions.objects


class Differences:
    """
    Differences
    """

    def __init__(self):
        """
        Constructor
        """

        self.__objects = src.functions.objects.Objects()
        self.__configurations = config.Config()

    def __get_quantiles(self, uri: str) -> dict:
        """

        :param uri:
        :return:
        """

        data = self.__objects.read(uri=uri)['q_testing']

        return  dict(zip(data['columns'], data['data']))

    def exc(self, estimates: pd.DataFrame, specification: sc.Specification):
        """

        :param estimates:
        :param specification:
        :return:
        """

        uri = os.path.join(self.__configurations.data_, 'metrics', str(specification.ts_id) + '.json')
        logging.info(uri)

        quantiles = self.__get_quantiles(uri=uri)
        logging.info(quantiles)

        estimates.info()
        logging.info(estimates.head())
