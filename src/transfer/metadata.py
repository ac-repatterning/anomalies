"""Module metadata.py"""

import boto3

import config
import src.elements.s3_parameters as s3p
import src.functions.objects
import src.s3.configurations


class Metadata:
    """
    Notes<br>
    ------<br>

    This class reads-in the metadata of this project's data & references.<br><br>

    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters):
        """

        :param connector: An instance of boto3.session.Session
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters

        self.__configurations = config.Config()

    def exc(self, name: str) -> dict:
        """

        :param name:
        :return:
        """

        dictionary = src.s3.configurations.Configurations(
            connector=self.__connector, bucket_name=self.__s3_parameters.configurations).objects(
            key_name=self.__configurations.metadata_ + '/' + name)

        return dictionary
