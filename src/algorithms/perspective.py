import os

import pandas as pd

import config


class Perspective:

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
        records.drop(columns=['ts_name', 'starting'], inplace=True)

        try:
            records.to_json(
                path_or_buf=os.path.join(self.__configurations.perspective_, 'perspective.json'),
                orient='index')
        except OSError as err:
            raise err from err
