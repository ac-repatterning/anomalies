"""
Module config.py
"""
import os


class Config:
    """
    Description
    -----------

    A class for configurations
    """

    def __init__(self) -> None:
        """
        <b>Notes</b><br>
        ------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, *key, etc.<br><br>
        """

        self.s3_parameters_key = 's3_parameters.yaml'
        self.arguments_key = f'data/anomalies/arguments.json'
        self.metadata_ = ''


        '''
        Project Metadata
        '''
        self.project_tag = 'hydrography'
        self.project_key_name = 'HydrographyProject'


        '''
        Local Paths
        '''
        self.data_ = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        self.pathway_ = self.warehouse
        self.points_ = os.path.join(self.pathway_, 'points')
        self.menu_ = os.path.join(self.pathway_, 'menu')
        self.perspective_ = os.path.join(self.pathway_, 'perspective')
