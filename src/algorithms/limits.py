"""Module limits.py"""
import boto3

import numpy as np
import pandas as pd

import src.s3.serials
import src.elements.s3_parameters as s3p
import src.elements.specification as sc

class Limits:
    """

    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: An instance of boto3.session.Session<br>
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        :param arguments
        """

        key_name = arguments.get('edges').get('key_name')
        bucket_name = s3_parameters._asdict().get(arguments.get('edges').get('p_bucket'))
        self.__edges = src.s3.serials.Serials(
            connector=connector, bucket_name=bucket_name).objects(key_name=key_name)

    def exc(self, data: pd.DataFrame, specification: sc.Specification):
        """

        :param data:
        :param specification:
        :return:
        """

        definitions: dict = self.__edges.get(str(specification.ts_id))

        frame = data.copy()
        points: np.ndarray = frame['original'].values
        booleans: np.ndarray = (points < definitions.get('e_l_whisker')) | (points > definitions.get('e_u_whisker'))
        frame = frame.assign(extreme=booleans.astype(int))

        return frame
