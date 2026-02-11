"""Module metrics.py"""
import logging
import os

import dask

import config
import src.elements.s3_parameters as s3p
import src.elements.specification as sc
import src.s3.directives


class Metrics:
    """
    Unloads gauge station model metrics
    """

    def __init__(self, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments:
        """

        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

        self.__configurations = config.Config()
        self.__directives =  src.s3.directives.Directives()

    def __get_metrics(self, specification: sc.Specification):
        """

        :param specification: Refer to src.elements.specification.py
        :return:
        """

        origin = (f'{self.__arguments.get('prefix').get('metrics')}/metrics/disaggregates/points/'
                  f'{specification.ts_id}.json')
        target = os.path.join(
            self.__configurations.data_, 'metrics')

        return self.__directives.unload(
            source_bucket=self.__s3_parameters.external, origin=origin, target=target, recursive='')

    def exc(self, specifications: list[sc.Specification]):
        """

        :param specifications: A list items of type Specification; refer to src.elements.specification.py
        :return:
        """

        # Or
        computations = [dask.delayed(self.__get_metrics)(specification=specification)
                        for specification in specifications]

        # Compute
        states = dask.compute(computations, scheduler='threads')[0]
        logging.info(states)
