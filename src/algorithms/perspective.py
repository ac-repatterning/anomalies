
import pandas as pd

import src.elements.specification as sc


class Perspective:

    def __init__(self):

        self.__names = ['p_anomaly', 'gap', 'asymptote', 'extreme']

    def exc(self, frame: pd.DataFrame, specification: sc.Specification):

        data = frame.copy()[self.__names]
        data.info()
