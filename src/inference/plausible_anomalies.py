"""Module plausible_anomalies.py"""
import logging
import os

import boto3
import numpy as np
import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.specification as sc
import src.functions.objects
import src.s3.serials


class PlausibleAnomalies:
    """
    Differences
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: An instance of boto3.session.Session<br>
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        :param arguments: A set of arguments vis-à-vis computation & storage objectives.<br>
        """

        self.__arguments = arguments

        # Instances
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Future
        key_name = f'{self.__arguments.get('prefix').get('metrics')}/metrics/aggregates/aggregates.json'
        self.__aggregates = src.s3.serials.Serials(
            connector=connector, bucket_name=s3_parameters.external).objects(key_name=key_name)
        logging.info(self.__aggregates)

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
