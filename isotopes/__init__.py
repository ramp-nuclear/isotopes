r"""
Isotopes
========

A minimal python interface to isotope data based on NUbase 2020, and to
integer representations of isotopes, as used by libraries such as ENDF.
Two distinct objects are defined:

- :class:`~zaid.ZAID`, which is an encoding of isotope enumeration by 
  its atomic number (Z), nucleon number (A) and isomeric state.
- :class:`~isotope.Isotope`, which builds upon :class:`~zaid.ZAID` and adds data
  such as mass, natural abundance and decay rates.


For ease of use, all known isotopes are available to be imported directly from
the top package level.


Examples
--------
>>> from isotopes import ZAID, H, H3, Hydrogen2, Xenon135m1
>>> ZAID(92, 235, 0)
922350
>>> H.name
'Hydrogen'
>>> H.mass
1.0079709420259335
>>> H.abundance
{H1: 0.999855, H2: 0.000145}
>>> H3.decay
1.782871574100462e-09
>>> Hydrogen2.A
2
>>> Xenon135m1.m
1
"""

from scipy.constants import Avogadro

from ._format import _isomer_symbols, _isotope_symbols, _isotope_names
from .isotope import Isotope
from .zaid import ZAID


# The naming using uppercase letters here is preferable since these are known
# scientific notations.
# noinspection PyPep8Naming
def __getattr__(name):
    """This is somewhat a magic piece of code.
    Instead of having the entire landscape of possible isotopes in the namespace,
    this function only creates for you the isotopes you import directly.
    Using the __init__.pyi file, the user gets automatic completion from most
    static programs for all available isotopes.

    """
    try:
        return Isotope.from_name(name)
    except (KeyError, ValueError):
        raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


avogadro = Avogadro * 1e-24
