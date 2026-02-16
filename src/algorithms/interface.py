"""Module inference/interface.py"""
import logging
import multiprocessing

import dask
import pandas as pd

import src.algorithms.attributes
import src.algorithms.asymptote
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
        self.__get_attributes = dask.delayed(src.algorithms.attributes.Attributes().exc)
        self.__get_data = dask.delayed(src.algorithms.data.Data(arguments=self.__arguments).exc)
        self.__get_special_anomalies = dask.delayed(src.inference.interface.Interface(arguments=self.__arguments).exc)

    def exc(self, specifications: list[sc.Specification]):
        """

        :param specifications:
        :return:
        """

        __gap = dask.delayed(src.algorithms.gap.Gap(arguments=self.__arguments).exc)
        __asymptote = dask.delayed(src.algorithms.asymptote.Asymptote(arguments=self.__arguments).exc)
        __persist = dask.delayed(src.algorithms.persist.Persist().exc)

        computations = []
        for specification in specifications:
            attribute: atr.Attribute = self.__get_attributes(specification=specification)
            data: pd.DataFrame = self.__get_data(specification=specification, attribute=attribute)
            __estimates: pd.DataFrame = self.__get_special_anomalies(
                attribute=attribute, data=data, specification=specification)
            __appending_gap: pd.DataFrame = __gap(data=__estimates)
            __appending_asymptote: pd.DataFrame = __asymptote(data=__appending_gap)

            message = __persist(specification=specification, estimates=__appending_asymptote)
            computations.append(message)

        messages = dask.compute(computations, scheduler='processes', num_workers=int(0.75*self.__n_cores))[0]
        logging.info(messages)
