"""Module attribute.py"""
import typing

class Attribute(typing.NamedTuple):
    """
    The data type class ⇾ Attribute<br><br>

    Attributes<br>
    ----------<br>

    modelling : dict
        The dictionary of a model's settings.
    scaling : dict
        The dictionary of the scaling arguments due to, derived from, a model's training data
    """

    modelling: dict
    scaling: dict
