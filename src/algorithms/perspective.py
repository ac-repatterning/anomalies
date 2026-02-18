
import pandas as pd

import src.elements.specification as sc


class Perspective:

    def __init__(self):

        self.__names = ['p_anomaly', 'gap', 'missing', 'asymptote', 'extreme']

    def exc(self, frame: pd.DataFrame, specification: sc.Specification):

        data: pd.DataFrame = frame.copy()[self.__names]
        matrix: pd.DataFrame = data.gt(0)

        vector = dict(matrix.sum(axis=0))
        print(vector.update(specification._asdict()))

        return vector
