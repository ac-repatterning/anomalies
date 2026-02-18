"""Module arguments"""

import argparse

import boto3

import config
import src.elements.s3_parameters as s3p
import src.s3.serials


class Arguments:
    """

    Arguments
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters):
        """

        :param connector:
        :param s3_parameters:
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters

        self.__configurations = config.Config()

    def __set_source(self, arguments: dict) -> dict:
        """

        :param arguments:
        :return:
        """

        objects = self.__s3_parameters._asdict()
        bucket = objects[arguments.get('s3').get('p_bucket')]
        prefix = objects[arguments.get('s3').get('p_prefix')]

        source = f's3://{bucket}/{prefix}{arguments.get('s3').get('affix')}'

        arguments['additions'] = {'modelling_data_source': source}

        return arguments

    @staticmethod
    def __set_prefix(arguments: dict) -> dict:
        """

        :param arguments:
        :return:
        """

        match arguments.get('stage'):
            case 'initial':
                arguments['prefix'] = arguments.get('inference').get('initial')
            case 'live':
                arguments['prefix'] = arguments.get('inference').get('live')
            case _:
                raise ValueError(f'Unknown stage: {arguments.get('stage')}')

        return arguments

    def __get_arguments(self, args: argparse.Namespace) -> dict:
        """

        :return:
        """

        key_name = self.__configurations.arguments_key
        arguments = src.s3.serials.Serials(
            connector=self.__connector, bucket_name=self.__s3_parameters.configurations).objects(key_name=key_name)

        arguments['series'] = {'excerpt': args.codes} if args.codes is not None else {'excerpt': None}
        arguments['stage'] = args.stage

        return arguments

    def exc(self, args: argparse.Namespace):
        """

        :param args:
        :return:
        """

        # Arguments
        arguments: dict = self.__get_arguments(args=args)
        arguments: dict = self.__set_source(arguments=arguments.copy())
        arguments: dict = self.__set_prefix(arguments=arguments.copy())

        return arguments
