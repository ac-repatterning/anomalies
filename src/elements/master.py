"""Module master.py"""
import typing

import pandas as pd


class Master(typing.NamedTuple):
    """
    The data type class ⇾ Master<br><br>

    Attributes<br>
    ----------<br>

    <b>data</b>: pandas.DataFrame<br>
        A gauge's frame of measures, etc.<br><br>
    <b>transforms</b>: pandas.DataFrame<br>
        In this case, the relevant fields of - data - have been transformed by a scaling function.<br><br>
    """

    data: pd.DataFrame
    transforms: pd.DataFrame
