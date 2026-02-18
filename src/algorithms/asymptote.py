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

    # pylint: disable=R0801
    @staticmethod
    def __get_boundaries(_data: pd.Series) -> np.ndarray:
        """
        This function determines the areas along a series whereby there are N or more consecutive non-changing values.

        :param _data: The series in focus.
        :return:
        """

        # Expectation: The difference between consecutive, and real, equal values will be zero
        difference = _data.copy().diff()

        # Boundary determination
        constants=np.where(difference == 0, 1, np.nan)
        conditionals = np.isnan(constants)
        exists = ~conditionals
        c_exists = np.cumsum(exists)
        __boundaries = np.diff(np.concatenate(([0], c_exists[conditionals])))

        boundaries = np.nan * np.zeros_like(constants)
        boundaries[conditionals] = __boundaries

        return np.concat([boundaries[1:], [0]])

    def exc(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        __frame['element'].where(__frame['element'] >= (self.__settings.get('length') - 1), 0)

        :param data:
        :return:
        """

        frame = data.copy()

        __frame = pd.DataFrame(data={'original': frame['original'].values})
        __frame['boundary'] = self.__get_boundaries(_data=__frame['original'])
        __frame['element'] = __frame['boundary'].bfill()
        __frame['asymptote'] = np.where(__frame['element'] >= (self.__settings.get('length') - 1),
                                        __frame['element'] + 1, 0)

        frame = frame.assign(asymptote=__frame['asymptote'].values)

        return frame
