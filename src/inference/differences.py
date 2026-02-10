import logging
import os
import pandas as pd

import config
import src.functions.objects
import src.elements.specification as sc


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

    def __get_quantiles(self, uri: str):
        """

        :param uri:
        :return:
        """

        data = self.__objects.read(uri=uri)['q_testing']

        return {k: v for k, v in zip(data['columns'], data['data'])}

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

        logging.info(estimates.head())
