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
        These are percentage error quantiles vis-à-vis forecasting models.

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

        # Read-in the testing stage percentage error quantiles
        uri = os.path.join(self.__configurations.data_, 'metrics', str(specification.ts_id) + '.json')
        quantiles = self.__get_quantiles(uri=uri)

        # An anomaly vis-à-vis quantiles metrics?
        points: np.ndarray = estimates['p_error'].values
        median = quantiles.get('median')
        l_boundary = quantiles.get('l_whisker_e') - (median - quantiles.get('l_whisker_e'))
        u_boundary = quantiles.get('u_whisker_e') + (quantiles.get('u_whisker_e') - median)
        print('BOUNDARIES: ', l_boundary, ', ', u_boundary, ', (', median, ')')

        states: np.ndarray = np.where((points < l_boundary) | (points > u_boundary),
                                      1, 0)
        estimates = estimates.assign(f_anomaly=states)

        print('ANOMALIES: ', estimates['f_anomaly'].sum())
        print(estimates.loc[estimates['f_anomaly'] == 1, :])

        return estimates
