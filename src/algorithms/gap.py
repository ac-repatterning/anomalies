"""Module gap.py"""
import numpy as np
import pandas as pd


# noinspection DuplicatedCode
class Gap:
    """

    <b>Vis-à-vis raw measures series</b>
    --------------------------------<br>

    Context: Cases whereby N or more consecutive points have a NaN value.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__settings: dict = arguments.get('detecting').get('gap')

    # pylint: disable=R0801
    @staticmethod
    def __get_boundaries(_data: pd.Series) -> np.ndarray:
        """

        :param _data:
        :return:
        """

        # Set NaN points to 1?
        __values=_data.isna().astype(int)

        # Subsequently, the values that were not NaN values are set to NaN
        __set_irrelevant = __values.where(__values == 1, np.nan)

        # The difference between real values; always zero because all the real values are 1
        difference = __set_irrelevant.diff()

        # In aid of boundary determination
        constants=np.where(difference == 0, 1, np.nan)

        # Therefore
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
        __frame['gap'] = np.where(__frame['element'] >= (self.__settings.get('length') - 1),
                                  __frame['element'] + 1, 0)

        frame = frame.assign(gap=__frame['gap'].values, missing=__frame['original'].isna())

        return frame
