"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.elements.specification as sc
import src.functions.objects


class Persist:
    """
    Persist
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # An instance for writing JSON objects
        self.__objects = src.functions.objects.Objects()

    @staticmethod
    def __get_node(blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        string: str = blob.to_json(orient='split')

        return json.loads(string)

    def __persist(self, nodes: dict, name: str) -> str:
        """

        :param nodes: Dictionary of data.
        :param name: A name for the file.
        :return:
        """

        return self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.points_, f'{name}.json'))

    def exc(self, specification: sc.Specification, estimates: pd.DataFrame) -> str:
        """

        :param specification: <br>
        :param estimates: <br>
        :return:
        """

        gaps = estimates.copy().loc[estimates['gap'] != 0, ['timestamp', 'original', 'measure', 'gap']]
        asymptotes = estimates.copy().loc[estimates['asymptote'] != 0, ['timestamp', 'original', 'measure', 'asymptote']]
        extremes = estimates.copy().loc[estimates['extreme'] != 0, ['timestamp', 'original', 'measure', 'extreme']]

        nodes = {
            'estimates': self.__get_node(blob=estimates.drop(columns=['date', 'ts_id'])),
            'gaps': self.__get_node(blob=gaps),
            'asymptotes': self.__get_node(blob=asymptotes),
            'extremes': self.__get_node(blob=extremes)
        }
        nodes.update(specification._asdict())

        return self.__persist(nodes=nodes, name=str(specification.ts_id))
