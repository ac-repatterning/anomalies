"""Module specifications.py"""
import pandas as pd

import src.elements.specification as sc


class Specifications:
    """
    Creates an attributes collection per gauge
    """

    def __init__(self):
        pass

    @staticmethod
    def __anomalies(specification: sc.Specification) -> sc.Specification:
        """

        :param specification: A gauge's collection of attributes
        :return:
        """

        specification = specification._replace(catchment_id=int(specification.catchment_id),
                                               station_id=int(specification.station_id),
                                               ts_id=int(specification.ts_id))

        return specification

    def exc(self, reference: pd.DataFrame) -> list[sc.Specification]:
        """

        :param reference:
        :return:
        """

        frame = reference.copy().drop(columns='uri')


        dictionaries = [frame.iloc[i, :].squeeze() for i in range(frame.shape[0])]
        specifications = [sc.Specification(**dictionary) for dictionary in dictionaries]
        specifications = [self.__anomalies(specification=specification)
                          for specification in specifications]

        return specifications
