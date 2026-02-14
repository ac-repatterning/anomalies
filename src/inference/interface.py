"""Module inference/interface.py"""
import logging
import multiprocessing

import dask
import pandas as pd

import src.elements.attribute as atr
import src.elements.master as mr
import src.elements.specification as sc
import src.inference.approximating
import src.inference.scaling


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
        self.__scaling = src.inference.scaling.Scaling()
        self.__n_cores = multiprocessing.cpu_count()

    def __set_transforms(self, data: pd.DataFrame, scaling: dict) -> mr.Master:
        """

        :param data:
        :param scaling:
        :return:
        """

        transforms = self.__scaling.transform(data=data, scaling=scaling)

        return mr.Master(data=data, transforms=transforms)

    def exc(self, attribute: atr.Attribute, data: pd.DataFrame, specification: sc.Specification):
        """

        :param attribute:
        :param data:
        :param specification:
        :return:
        """

        __approximating = dask.delayed(src.inference.approximating.Approximating().exc)

        master: mr.Master = self.__set_transforms(data=data, scaling=attribute.scaling)
        estimates: pd.DataFrame = __approximating(
            specification=specification, attribute=attribute, master=master)

        return estimates
