"""Module interface.py"""
import argparse
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.groups
import src.functions.service
import src.preface.arguments
import src.preface.setup
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, args: argparse.Namespace) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :param args: Wherein -> codes: list[int] | None, stage: either 'initial' or 'live'
        :return:
        """

        connector = boto3.session.Session()
        groups = src.functions.groups.Groups(
            connector=connector).exc(project_key_name=self.__configurations.project_key_name)

        # Interaction Instances: Amazon
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(
            connector=connector, groups=groups).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()
        arguments = src.preface.arguments.Arguments(
            connector=connector, s3_parameters=s3_parameters).exc(args=args)

        # Setting up
        src.preface.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

        return connector, s3_parameters, service, arguments
