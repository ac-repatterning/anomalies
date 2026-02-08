"""Module approximations.py"""
import typing

import pandas as pd


class Approximations(typing.NamedTuple):
    """
    The data type class ⇾ Approximations<br><br>

    Attributes<br>
    ----------<br>

    <b>estimates</b>: pandas.DataFrame<br>
        Estimates.<br><br>
    <b>forecasts</b>: pandas.DataFrame<br>
        Forecasts<br><br>
    """

    estimates: pd.DataFrame
    forecasts: pd.DataFrame
