"""Module asymptote.py"""
import numpy as np
import pandas as pd


# noinspection DuplicatedCode
class Asymptote:

    def __init__(self):
        pass

    @staticmethod
    def __get_boundaries(_data: pd.Series):
        """
        This function determines the areas along a series wherein there are N or more consecutive non-changing values.

        :param _data: The series in focus.
        :return:
        """

        difference = _data.copy().diff()

        constants=np.where(difference == 0, 1, np.nan)
        conditionals = np.isnan(constants)
        exists = ~conditionals
        c_exists = np.cumsum(exists)
        boundaries = np.diff(np.concatenate(([0], c_exists[conditionals])))

        zeros = np.nan * np.zeros_like(constants)
        zeros[conditionals] = boundaries

        return np.concat([zeros[1:], [0]])

    def exc(self, blob: pd.Series) -> np.ndarray:
        """

        :param blob:
        :return:
        """

        __frame = pd.DataFrame(data={'original': blob.values})
        __frame['boundary'] = self.__get_boundaries(_data=__frame['original'])
        __frame['element'] = __frame['boundary'].bfill()
        __frame['asymptote'] = __frame['element'].where(__frame['element'] >= 3, 0)

        return __frame['asymptote'].values
