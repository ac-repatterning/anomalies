"""Module inference/attributes.py"""
import json
import os

import config
import src.elements.attribute as atr
import src.elements.specification as sc


class Attributes:
    """
    Attributes
    """

    def __init__(self):
        """

        Constructor
        """

        # Instances
        self.__configurations = config.Config()

    @staticmethod
    def __get_request(uri: str) -> dict | list[dict]:
        """

        :param uri: A file's uniform resource identifier.
        :return:
        """

        try:
            with open(file=uri, mode='r', encoding='utf-8') as disk:
                return json.load(fp=disk)
        except ImportError:
            return {}

    def exc(self, specification: sc.Specification) -> atr.Attribute:
        """

        :param specification: Refer to src.elements.specification.py
        :return:
        """

        path = os.path.join(
            self.__configurations.data_, 'artefacts', str(specification.catchment_id), str(specification.ts_id))

        attribute = atr.Attribute(
            modelling=self.__get_request(uri=os.path.join(path, 'modelling.json')),
            scaling=self.__get_request(uri=os.path.join(path, 'scaling.json')))

        return attribute
