"""Module perspective.py"""
import os

import pandas as pd

import config


class Perspective:
    """

    An overarching summary of the number of time points that each series' gaps, missing
    points, asymptotes, etc, spans.
    """

    def __init__(self):
        """

        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, vectors: list[dict]):
        """

        :param vectors:
        :return:
        """

        records = pd.DataFrame.from_records(vectors)
        records.drop(columns=['ts_name'], inplace=True)

        try:
            records.to_json(
                path_or_buf=os.path.join(self.__configurations.perspective_, 'perspective.json'),
                orient='split')
        except OSError as err:
            raise err from err
