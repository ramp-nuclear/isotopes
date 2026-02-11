"""A ZAID

"""

from functools import lru_cache
from typing import Optional, TypeVar, Type

from isotopes._format import (_isomer_symbols,
                              _isotope_symbols,
                              _isotope_names,
                              _isotope_regex,
                              _isotope_regex_isomer_m_format)

T = TypeVar('T')


def _represent_isotope(symbol: str, a: int, m: int) -> str:
    m = f'm{m}' if m else ''
    return f'{symbol}{a or ""}{m}'


# noinspection PyPep8Naming,PyUnresolvedReferences
class ZAID(int):
    """This is a numeric representation of a nuclear structure, i.e. the number
    of protons, nucleons and the isomeric state of the nucleus.
    Since this is only a representation, the value might not correspond to an
    actual physical isotope. A more rigid, and more memory-heavy implementation
    is given in Isotope.

    Users should be aware that not all possible ZAIDs represent objects that
    can be used in all cases. Some programs/libraries do not include data even
    for XXXX isotopes like C14, and some ZAIDs could be used by a user for their
    own purposes and be ill-suited when encountered by other programs.
    For example, if one's library does not contain an isotope in a mixture
    you defined, you could have a problem when using a Monte Carlo program such
    as OpenMC, unless these isotopes are filtered out before use.

    Parameters
    ----------
    Z: int
        The number of protons.
    A: int
        The total number of nucleons.
    m: int
        The isomeric state of the nucleus. 0 is the ground state, and up it goes.
        See the wikipedia page on the subject of isomers.
    """

    # noinspection PyInitNewSignature
    @lru_cache(maxsize=None)
    def __new__(cls, Z: int, A: int, m: int, /):
        if Z < 0:
            raise ValueError(f"{Z=} must be non-negative.")
        if A not in (r := range(999)):
            raise ValueError(f"{A=} must be in {r}.")
        if m not in (r := range(10)):
            raise ValueError(f"{m=} must be in {r}.")
        return super().__new__(cls, Z * 10000 + A * 10 + m)

    def __getnewargs__(self):
        return self.Z, self.A, self.m

    @classmethod
    def from_int(cls: Type[T], num: int) -> T:
        """Creates the object representation from its corresponding integer value.

        """
        Z, res = divmod(num, 10000)
        A, m = divmod(res, 10)
        # noinspection PyArgumentList
        return cls(Z, A, m)

    @classmethod
    def from_name(cls: Type[T], s: str) -> T:
        """Creates the object representation from its corresponding symbol value or name.
        """
        try:
            name, A, isomer_symbol = _isotope_regex.fullmatch(s).groups()
            m = _isomer_symbols.inverse[isomer_symbol]
        except AttributeError:
            name, A, m = _isotope_regex_isomer_m_format.fullmatch(s).groups()
            m = int(m)
        if name in _isotope_names.values():
            Z = _isotope_names.inverse[name]
        else:
            Z = _isotope_symbols.inverse[name]
        A = int(A or 0)
        # noinspection PyArgumentList
        return cls(Z, A, m)

    @property
    def Z(self) -> int:
        """Number of protons in the nucleus.
        """
        return self // 10000

    @property
    def A(self) -> int:
        """Number of nucleons in the nucleus.
        """
        return (self % 10000) // 10

    @property
    def m(self) -> int:
        """Isomeric energy level. Isomers are two nuclei in different nuclear
        states, with the same number of each nucleon.
        They have different cross-sections and nuclear properties, like
        their decay modes. The 0 state is often the only stable isomer, though
        some materials have isomers that are more stable than their base state.

        """
        return self % 10

    @property
    def symbol(self) -> Optional[str]:
        """The symbolic representation of this isotope, if it makes sense.
        Not all ZAIDs are actually representations of known isotopes.

        Returns
        -------
        str or None
            Returns None iff this doesn't represent a known isotope. For example,
            ZAID(15000,0,0) would not be recognized.

        """
        try:
            return _represent_isotope(_isotope_symbols[self.Z], self.A, self.m)
        except KeyError:
            return

    @property
    def name(self) -> Optional[str]:
        """The full name of this isotope, if it makes sense. Not all ZAIDs are
        actually representations of known isotopes.

        """
        try:
            return _represent_isotope(_isotope_names[self.Z], self.A, self.m)
        except KeyError:
            return
