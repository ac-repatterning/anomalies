"""Module metadata.py"""

import pandas as pd

import src.assets.cases
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache


class Metadata:
    """
    Retrieves the metadata of the gauges in focus.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param service: A suite of services for interacting with Amazon Web Services.<br>
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.<br>
        :param arguments: A set of arguments vis-à-vis computation & storage objectives.<br>
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__arguments = arguments

    def __filter(self, cases: pd.DataFrame) -> pd.DataFrame:
        """

        :return:
        """

        values: list = self.__arguments.get('series').get('excerpt')

        if values is None:
            return cases

        frame = cases.copy().loc[cases['ts_id'].isin(values), :]

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # the identification codes of gauge stations vis-à-vis existing model artefacts
        cases = src.assets.cases.Cases(
            service=self.__service, s3_parameters=self.__s3_parameters, arguments=self.__arguments).exc()

        return self.__filter(cases=cases)
