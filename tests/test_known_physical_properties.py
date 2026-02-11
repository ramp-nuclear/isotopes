"""Tests that the data contained in some Isotopes fits the known values.

If these tests break, it could be because the underlying data was updated,
but in any other case this is probably a big no-no.

"""
import isotopes
import pytest


# noinspection PyPep8Naming
def test_u235_properties():
    U235 = isotopes.U235
    assert U235.symbol == 'U235'
    assert U235.name == 'Uranium235'
    assert U235.abundance == pytest.approx(0.0072, 1e-3)
    assert U235.mass == pytest.approx(235.044, 1e-6)


# noinspection PyPep8Naming
def test_al_properties():
    Al27 = isotopes.Al27
    assert Al27.symbol == 'Al27'
    assert Al27.name == 'Aluminium27'
    assert Al27.abundance == 1.0
    assert Al27.mass == pytest.approx(27, 1e-2)
