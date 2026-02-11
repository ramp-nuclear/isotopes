"""Tests that the .pyi magic file did not change."""

import difflib
from pathlib import Path

import pytest

from isotopes._create_pyi import pyi_string


@pytest.mark.regression
def test_pyi_file_meets_automatic_generation():
    s = pyi_string()
    fname = Path(__file__)
    pyi_file = fname.parent.parent / 'isotopes' / '__init__.pyi'
    with pyi_file.open('r') as f:
        file_s = f.read()
    assert s == file_s, [li for li in difflib.ndiff(s, file_s) if li[0] != " "]
