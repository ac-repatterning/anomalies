"""Module differences.py"""
import logging
import os

import pandas as pd
import numpy as np

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

        return  {k: v for k, v in zip(data['columns'], data['data'][0])}

    def exc(self, estimates: pd.DataFrame, specification: sc.Specification):
        """

        :param estimates:
        :param specification:
        :return:
        """

        uri = os.path.join(self.__configurations.data_, 'metrics', str(specification.ts_id) + '.json')
        quantiles = self.__get_quantiles(uri=uri)

        points: np.ndarray = estimates['p_error'].values
        states: np.ndarray = np.where((points < quantiles.get('l_whisker_e')) | (points > quantiles.get('u_whisker_e')),
                                      1, 0)
        estimates = estimates.assign(f_anomaly=states)

        return estimates
