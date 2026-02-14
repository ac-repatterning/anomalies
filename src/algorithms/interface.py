"""Module inference/interface.py"""
import logging
import multiprocessing

import dask
import pandas as pd

import src.algorithms.attributes
import src.algorithms.data
import src.algorithms.gap
import src.algorithms.persist
import src.elements.attribute as atr
import src.elements.specification as sc
import src.inference.interface


class Interface:
    """
    Interface
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of arguments vis-à-vis computation & storage objectives.<br>
        """

        self.__arguments = arguments

        # Setting up
        self.__n_cores = multiprocessing.cpu_count()

    def exc(self, specifications: list[sc.Specification]):
        """

        :param specifications:
        :return:
        """

        __get_attributes = dask.delayed(src.algorithms.attributes.Attributes().exc)
        __get_data = dask.delayed(src.algorithms.data.Data(arguments=self.__arguments).exc)
        __get_special_anomalies = dask.delayed(src.inference.interface.Interface(arguments=self.__arguments).exc)
        __gap = dask.delayed(src.algorithms.gap.Gap(arguments=self.__arguments).exc)
        __persist = dask.delayed(src.algorithms.persist.Persist().exc)

        computations = []
        for specification in specifications:
            attribute: atr.Attribute = __get_attributes(specification=specification)
            data: pd.DataFrame = __get_data(specification=specification, attribute=attribute)
            estimates: pd.DataFrame = __get_special_anomalies(attribute=attribute, data=data, specification=specification)
            estimates: pd.DataFrame = __gap(estimates=estimates)

            message = __persist(specification=specification, estimates=estimates)
            computations.append(message)

        messages = dask.compute(computations, scheduler='processes', num_workers=int(0.5*self.__n_cores))[0]
        logging.info(messages)
