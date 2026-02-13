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

    def __plausible_anomalies(self, points: np.ndarray, specification: sc.Specification) -> np.ndarray:
        """

        :param points:
        :param specification:
        :return:
        """

        # Error quantiles
        uri = os.path.join(self.__configurations.data_, 'metrics', str(specification.ts_id) + '.json')
        data = self.__objects.read(uri=uri)['q_testing']
        quantiles = {k: v for k, v in zip(data['columns'], data['data'][0])}

        median = quantiles.get('median')
        l_boundary = quantiles.get('l_whisker_e') - (median - quantiles.get('l_whisker_e'))
        u_boundary = quantiles.get('u_whisker_e') + (quantiles.get('u_whisker_e') - median)

        # An anomaly vis-à-vis quantiles metrics?
        p_anomalies: np.ndarray = np.where((points < l_boundary) | (points > u_boundary), 1, 0)

        return p_anomalies

    def exc(self, estimates: pd.DataFrame, specification: sc.Specification):
        """

        :param estimates:
        :param specification:
        :return:
        """

        points: np.ndarray = estimates['p_error'].values
        p_anomalies = self.__plausible_anomalies(points=points, specification=specification)
        estimates = estimates.assign(p_anomaly=p_anomalies)

        return estimates
