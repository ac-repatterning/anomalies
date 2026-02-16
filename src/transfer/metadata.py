"""Module metadata.py"""

import boto3

import config
import src.functions.objects
import src.s3.configurations


class Metadata:
    """
    Notes<br>
    ------<br>

    This class reads-in the metadata of this project's data & references.<br><br>

    """

    def __init__(self, connector: boto3.session.Session, groups: dict):
        """

        :param connector: An instance of boto3.session.Session
        :param groups:
        """

        self.__connector = connector
        self.__groups = groups

        self.__configurations = config.Config()

    def exc(self, name: str) -> dict:
        """

        :param name:
        :return:
        """

        dictionary = src.s3.configurations.Configurations(
            connector=self.__connector, groups=self.__groups).objects(
            key_name=self.__configurations.metadata_ + '/' + name)

        return dictionary
