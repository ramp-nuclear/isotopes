"""Here we define an isotope, which is a more defined ZAID with physical attributes.
Unlike ZAID, which should only be thought of as a fancy number that could, on a
good day, represent an actual physical thing, Isotopes are a representation of
the physical concept of an isotope. They are named appropriately, they can only
be generated if they are known to exist, and they contain physical attributes.

Currently, these physical attributes are limited in scope, to limit the memory
footprint of using these isotopes.

"""
from functools import lru_cache
from importlib.resources import path as resource_path

import pandas as pd

from isotopes.zaid import ZAID


class UnknownIsotopeError(ValueError):
    """An error for when the required Isotope for creation isn't in the database.

    """
    pass


class Isotope(ZAID):
    """An Isotope is a ZAID that has special information, because it is
    actually a physical isotope, like O16 or U235. It contains physical
    information about the physical isotope to assist in material generation.
    As a convention, an Isotope with Z>0 and A=m=0 represents the natural element
    with Z protons. While it is useful for material generation, and thus supported,
    users should use them with caution, since they do not actually represent
    objects that can be assigned nuclear properties, which is what most users
    of this package are expected to eventually want to do.

    See Also
    --------
    :class:`isotopes.zaid.ZAID`: For ZAID representation with Z, A and m

    Attributes
    ----------
    mass: float
        Mass of a nucleus of this isotope, in unified atomic mass units (1u = 1g/mol).
        For elements, it is the abundance-weighted mass.
    decay: float
        Decay rate (1/s) of the isotope. That is ln(2)/half-life.
    abundance: float or dict[Isotope, float]
        Fractional natural abundance of the isotope in nature.
        For elements, this is a dictionary for its naturally occuring isotopes.

    Examples
    --------
    >>> from math import floor
    >>> i1 = Isotope(6, 0, 0)
    >>> floor(i1.mass)
    12
    >>> i1.abundance
    {C12: 0.9894, C13: 0.0106}
    >>> type(i1.mass)
    <class 'float'>

    """
    with resource_path(__name__, "nubase2020.csv") as path:
        _df = pd.read_csv(path, index_col=0)

    # noinspection PyPep8Naming
    @lru_cache(maxsize=None)
    def __new__(cls, Z: int, A: int, m: int, /):
        obj = super().__new__(cls, Z, A, m)
        try:
            obj.mass = float(cls._df.loc[obj]['mass'])
        except KeyError as e:
            raise UnknownIsotopeError(f"Unknown isotope for {(Z, A, m)=}") from e
        obj.decay = float(cls._df.loc[obj]['decay'])
        if A == 0:
            df = cls._df[cls._df['z'] == Z].set_index(['z', 'a', 'm'])
            obj.abundance = {Isotope(z, a, n): float(val) for (z, a, n), val in
                             df[df['abundance'] > 0.0]['abundance'].to_dict().items()}
        else:
            obj.abundance = float(cls._df.loc[obj]['abundance'])
        return obj

    @classmethod
    def from_zaid(cls, zaid: ZAID) -> "Isotope":
        """Creates an Isotope from a ZAID.

        Parameters
        ----------
        zaid: ZAID
            The ZAID to transform.

        """
        return cls(zaid.Z, zaid.A, zaid.m)

    @classmethod
    def from_zaid_with_fallback(cls, zaid: ZAID) -> "Isotope | ZAID":
        """Tries to return an Isotope from a ZAID, and if fails reverts to ZAID.

        Parameters
        ----------
        zaid: ZAID
            The ZAID to try and transform.

        """
        try:
            return cls.from_zaid(zaid)
        except UnknownIsotopeError:
            return zaid

    @classmethod
    def from_int_with_fallback(cls, num: int) -> "Isotope | ZAID":
        """Tries to return an Isotope from an integer, and if fails reverts to ZAID.

        Parameters
        ----------
        num: int
            The number to try to transform

        """
        return cls.from_zaid_with_fallback(ZAID.from_int(num))

    def __str__(self) -> str:
        """For Isotopes, symbol names will always exist, so they are safe and
        better to use for user readability.

        """
        return self.symbol

    __repr__ = __str__

    def __getstate__(self):
        return None
