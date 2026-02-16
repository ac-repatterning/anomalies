"""Module asymptote.py"""
import numpy as np
import pandas as pd


# noinspection DuplicatedCode
class Asymptote:
    """

    <b>Vis-à-vis raw measures series</b>
    --------------------------------<br>

    Context: Cases whereby there are N or more consecutive non-changing values.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__settings: dict = arguments.get('detecting').get('asymptote')


    @staticmethod
    def __get_boundaries(_data: pd.Series) -> np.ndarray:
        """
        This function determines the areas along a series whereby there are N or more consecutive non-changing values.

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

    def exc(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        frame = data.copy()

        __frame = pd.DataFrame(data={'original': frame['original'].values})
        __frame['boundary'] = self.__get_boundaries(_data=__frame['original'])
        __frame['element'] = __frame['boundary'].bfill()
        __frame['asymptote'] = __frame['element'].where(__frame['element'] >= (self.__settings.get('length') - 1), 0)

        frame = frame.assign(asymptote=__frame['asymptote'].values)

        return frame
