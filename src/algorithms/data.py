"""Module data.py"""

import dask.dataframe as ddf
import numpy as np
import pandas as pd

import src.elements.attribute as atr
import src.elements.specification as sc
import src.timings


class Data:
    """
    Data
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of arguments vis-à-vis computation & storage objectives.<br>
        """

        frequency = 1.0 if arguments.get('frequency') == "h" else float(arguments.get('frequency').removesuffix("h"))
        days = round(365 * arguments.get('spanning'))
        self.__n_samples = int(days * 24 / frequency)

        # Instances
        self.__timings: list = src.timings.Timings(arguments=arguments).exc()
        self.__endpoint: str = arguments.get('additions').get('modelling_data_source')

        # Focus
        self.__dtype = {'timestamp': np.float64, 'ts_id': np.float64, 'measure': float}

    def __get_data(self, listing: list[str]) -> pd.DataFrame:
        """

        :param listing:
        :return:
        """

        try:
            block: pd.DataFrame = ddf.read_csv(
                listing, header=0, usecols=list(self.__dtype.keys()), dtype=self.__dtype).compute()
        except OSError:
            return pd.DataFrame()

        block.reset_index(drop=True, inplace=True)
        block.sort_values(by='timestamp', ascending=True, inplace=True)
        block.drop_duplicates(subset='timestamp', keep='first', inplace=True)

        return block

    @staticmethod
    def __set_missing(data: pd.DataFrame) -> pd.DataFrame:
        """
        Forward filling.  In contrast, the variational model inherently deals with missing data, hence
                          it does not include this type of step.

        :param data:
        :return:
        """

        data['original'] = data.copy()['measure']
        data['measure'] = data['measure'].ffill().values

        return data

    def exc(self, specification: sc.Specification, attribute: atr.Attribute) -> pd.DataFrame:
        """

        :param specification:
        :param attribute:
        :return:
        """

        listing = [f'{self.__endpoint}/{specification.catchment_id}/{specification.ts_id}/{timing}.csv'
                   for timing in self.__timings ]

        # The data
        data = self.__get_data(listing=listing)
        if data.empty:
            return data

        # Missing
        data = self.__set_missing(data=data.copy())

        # Filter
        if attribute.scaling:
            n_samples_seen_ = attribute.scaling.get('n_samples_seen_')
            data = data.copy().tail(min(n_samples_seen_, self.__n_samples))
        else:
            data = data.copy().tail(self.__n_samples)

        # datetime
        data['date'] = pd.to_datetime(data['timestamp'], unit='ms')

        return data
