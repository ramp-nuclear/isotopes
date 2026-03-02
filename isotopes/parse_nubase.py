#!/bin/env python
"""
script to parse nubase file and generate standard csv.
The NuBase2020 file can be found at (Checked 11.2.2026):
    https://www.anl.gov/sites/www/files/2022-11/nubase_4.mas20.txt
"""
import re
from io import StringIO
from math import inf, nan

import numpy as np
import pandas as pd
import parse
from more_itertools import unzip
from scipy.constants import (
    atomic_mass,
    atto,
    c,
    day,
    eV,
    exa,
    femto,
    giga,
    hour,
    kilo,
    mega,
    micro,
    milli,
    minute,
    nano,
    peta,
    pico,
    tera,
    yotta,
    zepto,
    zetta,
)

isomers = {0: '',
           1: 'm',
           2: 'n',
           3: 'p',
           4: 'q',
           5: 'r',
           6: 'x',
           8: 'i',
           9: 'j',
           }

UNITS = {
    '': 1.0,
    'm': milli,
    'u': micro,
    'n': nano,
    'p': pico,
    'f': femto,
    'a': atto,
    'z': zepto,
    'y': 1e-24,  # yocto
    'k': kilo,
    'M': mega,
    'G': giga,
    'T': tera,
    'P': peta,
    'E': exa,
    'Z': zetta,
    'Y': yotta,
}

TIME_UNITS = {
    's': 1.0,  # seconds
    'm': minute,
    'h': hour,
    'd': day,
    'y': 365.2422 * day,  # annoying nubase-defined year (taken from the paper)
}


@np.vectorize
def parse_time_unit(x: str, /):
    """
    parse time unit from nubase format
    >>> parse_time_unit('My')
    31556926080000.0
    >>> parse_time_unit('s')
    1.0
    """
    if not x:
        return np.nan
    unit_char, time_unit_char = re.match(r'([a-zA-Z]?)([a-zA-Z])', x).groups()
    try:
        return UNITS[unit_char] * TIME_UNITS[time_unit_char]
    except LookupError:
        return np.nan


def calc_mass(A: int, mass_excess: float) -> float:
    """Calculate the mass of a nucleus given the number of nuclei.

    Parameters
    ----------
    A: the number of nucleons in the nucleus
    mass_excess: The excess mass, in keV. This is physically the nuclear bonding
                 energy.

    Returns
    -------
    The mass of the nucleus

    """
    kev = kilo * eV
    eu = atomic_mass * c ** 2
    return A + (mass_excess * kev / eu)


def nubase_colspecs(format):
    """
    return NUBASE column specifications according to format.
    """
    level = {
        '1997': 0,
        '2003': 0,
        '2012': 1,
        '2016': 1,
        '2020': 2,
    }[format]
    columns = [
        ('a', 3, int),
        (None, 1, None),
        ('zzzi', 4, int),
        (None, 3, None),
        ('name', 6, str),
        (None, 1, None),
        ('mass', 11 if level <= 1 else 13, float),
        ('dmass', 9 if level <= 1 else 11, float),
        ('exc', 10 if level <= 1 else 12, float),
        ('dexc', 8 if level <= 1 else 11, float),
        ('or', 2, str),
        ('u', 1, str),
        ('i', 1, str),
        ('T', 9, half_life),
        ('Tu', 2, str),
        (None, 1, None),
        ('dT', 7, None),
        ('jpi', 14, str),
        ('ey', 2, str),
        (None, 10, None),
        ('disc', 0 if level <= 0 else 4, str),
        (None, 1, None),
        ('BR', 90, str),
    ]
    i = -1
    colspecs = []
    for name, length, dtype in columns:
        if name and length and dtype:
            colspecs.append(
                (name, (i + 1, i + 1 + length), dtype)
            )
        i += length
    return colspecs


def half_life(string):
    if not string or 'R' in string:
        return nan
    string = string.strip(' #<>~')
    if string in ('stbl','contamnt'):
        return inf
    elif not string or string == 'p-unst':
        return 0.0
    else:
        return float(string)


def optional_float(string):
    if not string:
        return nan
    string = string.strip(' #<>~')
    if string in ('non-exist',):
        return nan
    return float(string)


@np.vectorize
def parse_name(name, i):
    match = parse.search('{:d}{:l}', name.replace(' ', ''))
    if i > 0:
        return match[1].removesuffix(isomers[i]).rstrip('x') + str(match[0]) + isomers[i]
    else:
        return match[1].capitalize() + str(match[0])


@np.vectorize
def parse_abundance(string):
    if not string:
        return 0.0
    if match := parse.search('IS={:g}', string):
        return match[0] / 100.0
    else:
        return 0.0


def ispositive(x):
    return np.isfinite(x) & (x > 0)


def parse_nubase(input, output, format):
    (*names,), (*colspecs,), (*dtypes,) = unzip(nubase_colspecs(format))
    converters = {
        'mass': optional_float,
        'dmass': optional_float,
        'exc': optional_float,
        'dexc': optional_float,
        'T': half_life,
    }
    with open(input) as file:
        str_io = StringIO(''.join(line for line in file if not line.startswith('#')))
        df = pd.read_fwf(str_io,
                         colspecs=colspecs,
                         names=names,
                         converters=converters,
                         keep_default_na=False,
                         )
    df = df[~np.isin(df['or'], ['EU', 'RN'])]
    Z, m = np.divmod(df['zzzi'], 10)
    df['T'] = np.nan_to_num(df['T'], nan=0.0, posinf=inf)
    A = df['a']
    mass = calc_mass(A, df['mass'])
    hl = np.where(ispositive(df['T']),
                  df['T'] * parse_time_unit(df['Tu']),
                  df['T'])
    decay = np.log(2) / hl
    abundance = parse_abundance(df['BR'])
    zaid = Z * 10000 + A * 10 + m
    dg = pd.DataFrame({'z': Z.values,
                       'a': A.values,
                       'm': m.values,
                       'name': parse_name(df['name'], m),
                       'mass': mass.values,
                       'decay': decay,
                       'abundance': abundance
                       }, index=zaid)
    dg = dg.loc[(dg['m'] <= 6) & (dg['mass'] > 0.0)]
    dn = {}
    for z, dd in dg.groupby('z'):
        if dd['abundance'].sum() == 0.0:
            continue
        if np.isclose(dd['abundance'].sum(), 1.0, atol=1e-4, rtol=0.0):
            dd = dd[dd['abundance'] > 0.0]
            dn[z * 10000] = {
                'z': z,
                'a': 0,
                'm': 0,
                'name': parse.search('{:l}', dd['name'].iloc[0])[0],
                'mass': np.average(dd['mass'],
                                   weights=dd['abundance']),
                'decay': 0.0,
                'abundance': np.nan
            }
        else:
            raise ValueError('Wrong sum of abundances')
    dn = pd.DataFrame.from_dict(dn, orient='index')
    dg = pd.concat((dg, dn)).sort_index()
    dg.to_csv(output)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('format', choices=['1997',
                                           '2003',
                                           '2012',
                                           '2016',
                                           '2020'],
                        help='nubase file format')
    parser.add_argument('inp', help='input nubase file')
    parser.add_argument('out', help='output csv file')
    args = parser.parse_args()

    parse_nubase(args.inp, args.out, args.format)

