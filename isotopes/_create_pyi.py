#!/usr/bin/env python3
"""A short script that generates the .pyi file contents and prints them to screen.

"""
from isotopes import Isotope


def pyi_string() -> str:
    # noinspection PyProtectedMember
    df = Isotope._df
    df = df[df['z'] > 0]
    s1 = '''from .isotope import Isotope
from .zaid import ZAID

avogadro: float
ZAID = ZAID
Isotope = Isotope'''
    isos = (Isotope.from_name(name) for name in df['name'])
    isostrings = (f"\n{iso.symbol}: Isotope" + (f"\n{iso.name}: Isotope" if iso.name else "") for iso in isos)
    return s1 + ''.join(isostrings) + '\n'


if __name__ == '__main__':
    print(pyi_string())
