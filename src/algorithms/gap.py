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

        self.__settings: dict = arguments.get('detecting').get('gap')

    @staticmethod
    def __get_boundaries(_data: pd.Series):

        # Set NaN points to 1?
        __values=_data.isna().astype(int)

        # Subsequently, the values that were not NaN values are set to NaN
        __set_irrelevant = __values.where(__values == 1, np.nan)

        # ...
        difference = __set_irrelevant.diff()

        # ...
        constants=np.where(difference == 0, 1, np.nan)
        conditionals = np.isnan(constants)
        exists = ~conditionals
        c_exists = np.cumsum(exists)
        boundaries = np.diff(np.concatenate(([0], c_exists[conditionals])))

        zeros = np.nan * np.zeros_like(constants)
        zeros[conditionals] = boundaries

        return np.concat([zeros[1:], [0]])

    def exc(self, estimates: pd.DataFrame) -> pd.DataFrame:
        """
        
        :param estimates:
        :return:
        """

        frame = estimates.copy()

        instances = pd.DataFrame(data={'original': frame[self.__settings.get('field')].values})
        instances['boundary'] = self.__get_boundaries(_data=instances['original'])
        instances['element'] = instances['boundary'].bfill()
        instances['gap'] = instances['element'].where(instances['element'] >= (self.__settings.get('length') - 1), 0)

        frame = frame.assign(gap=instances['gap'].values)

        return frame
