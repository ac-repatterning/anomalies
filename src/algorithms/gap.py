"""Module gap.py"""
import numpy as np
import pandas as pd


# noinspection DuplicatedCode
class Gap:
    """
    The focus is gaps.  Contexts whereby N or more consecutive points have a NaN value
    """

    def __init__(self):
        pass

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

    def exc(self, blob: pd.Series) -> np.ndarray:

        instances = pd.DataFrame(data={'original': blob.values})
        instances['boundary'] = self.__get_boundaries(_data=instances['original'])
        instances['element'] = instances['boundary'].bfill()
        instances['gap'] = instances['element'].where(instances['element'] >= 3, 0)

        return instances['gap'].values
