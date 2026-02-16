"""Module plausible_anomalies.py"""
import os

import numpy as np
import pandas as pd

import config
import src.elements.specification as sc
import src.functions.objects


class PlausibleAnomalies:
    """
    Differences
    """

    def __init__(self):
        """

        Constructor
        """

        self.__objects = src.functions.objects.Objects()
        self.__configurations = config.Config()

    def __get_error_quantiles(self, ts_id: int):
        """
        {k: v for k, v in zip(data['columns'], data['data'][0])}

        :param ts_id:
        :return:
        """

        # Error quantiles
        uri = os.path.join(self.__configurations.data_, 'metrics', str(ts_id) + '.json')
        data = self.__objects.read(uri=uri)['q_testing']
        quantiles = dict(zip(data['columns'], data['data'][0]))

        return quantiles

    def __plausible_anomalies(self, estimates: pd.DataFrame, ts_id: int) -> np.ndarray:
        """

        :param estimates:
        :param ts_id:
        :return:
        """

        points: np.ndarray = estimates['p_error'].values
        real: np.ndarray = estimates['original'].notna().values

        # Quantiles & Boundaries
        quantiles = self.__get_error_quantiles(ts_id=ts_id)
        median = quantiles.get('median')
        l_boundary = quantiles.get('l_whisker_e') - (median - quantiles.get('l_whisker_e'))
        u_boundary = quantiles.get('u_whisker_e') + (quantiles.get('u_whisker_e') - median)

        # An anomaly vis-à-vis quantiles metrics?
        p_outliers = np.where((points < l_boundary) | (points > u_boundary), 1, 0)
        p_anomalies = np.where(p_outliers & real, 1, 0)

        return p_anomalies

    def exc(self, estimates: pd.DataFrame, specification: sc.Specification):
        """

        :param estimates:
        :param specification:
        :return:
        """

        p_anomalies = self.__plausible_anomalies(estimates=estimates.copy(), ts_id=specification.ts_id)
        estimates = estimates.assign(p_anomaly=p_anomalies)

        return estimates
