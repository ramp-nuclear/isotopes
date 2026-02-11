"""Tests for the external package API.

"""
import pickle

import hypothesis.strategies as st
import pytest
from hypothesis import given

import isotopes


@pytest.mark.parametrize(
    "name",
    ["Th232",
     "Pa233",
     "Ge72",
     "Ge73",
     "Ge74",
     "Ge76",
     "As75",
     "Se76",
     "Se77",
     "Se78",
     "Se80",
     "Se82",
     "Br79",
     "Br81",
     "Kr80",
     "Kr82",
     "Kr83",
     "Kr84",
     "Kr86",
     "Rb85",
     "Rb87",
     "Sr86",
     "Sr87",
     "Sr88",
     "Zr90",
     "Zr91",
     "Zr92",
     "Y89",
     "Zr93",
     "Zr94",
     "Zr96",
     "Nb94",
     "Mo95",
     "Mo96",
     "Mo97",
     "Tc99",
     "Ru99",
     "Ru101",
     "Ru102",
     "Ru103",
     "Ru104",
     "Ru106",
     "Rh105",
     "Pd107",
     "Pd108",
     "Pd110",
     "Ag109",
     "Cd111",
     "Cd112",
     "Cd113",
     "Cd114",
     "Cd116",
     "In113",
     "In115",
     "Sn115",
     "Sn117",
     "Sn118",
     "Sn119",
     "Sn126",
     "Sb121",
     "Sb123",
     "Sb125",
     "Te122",
     "Te124",
     "Te125",
     "Te126",
     "Te127m",
     "Te128",
     "Te130",
     "I127",
     "I129",
     "I135",
     "Xe131",
     "Xe132",
     "Xe134",
     "Xe135",
     "Xe136",
     "Cs133",
     "Cs134",
     "Cs135",
     "Cs137",
     "Ba136",
     "Ba137",
     "Ba138",
     "Ce140",
     "Ce142",
     "Pr141",
     "Nd143",
     "Nd144",
     "Nd145",
     "Nd146",
     "Nd148",
     "Nd150",
     "Pm147",
     "Pm149",
     "Sm150",
     "Sm151",
     "Sm152",
     "Sm154",
     "Eu153",
     "Eu155",
     "Gd156",
     "Gd157",
     "Gd158",
     "Gd160",
     "Tb159",
     "Dy161",
     "Dy162",
     "Dy163",
     "Dy164",
     "Ho165",
     "Er166",
     "Er167",
     "U232",
     "U233",
     "Ru100",
     "Pd106",
     "Xe128",
     "Xe130",
     "Ba134",
     "Ba135",
     "Nd142",
     "Pm148",
     "Pm148m",
     "Sm147",
     "Sm148",
     "Sm149",
     "Eu151",
     "Eu152",
     "Eu154",
     "Gd152",
     "Gd154",
     "Gd155",
     "Tb160",
     "Dy160",
     "Rh103",
     "Pa231",
     "U234",
     "U235",
     "U236",
     "Te123",
     "Pd104",
     "U237",
     "U238",
     "Np239",
     "Pd105",
     "Np237",
     "Pu238",
     "Pu240",
     "Pu239",
     "Pu241",
     "Pu242",
     "Am243",
     "Am241",
     "Am242",
     "Am242m",
     "Cm242",
     "Cm243",
     "Cm244",
     "Li7",
     "H3",
     "B10",
     "He3",
     "Li6",
     "He4",
     "Helium4",
     "Lithium7"
     ],
)
def test_import_isotope_by_name_does_not_fail(name):
    getattr(isotopes, name)


badZ = st.integers(max_value=-1)
badA = st.one_of(st.integers(min_value=1000), st.integers(max_value=-1))
badm = st.one_of(st.integers(min_value=10), st.integers(max_value=-1))


# noinspection PyPep8Naming
@given(badZ, st.integers(), st.integers())
def test_making_zaids_outside_Z_range_fails(Z, A, m):
    with pytest.raises(ValueError):
        _ = isotopes.ZAID(Z, A, m)


# noinspection PyPep8Naming
@given(st.integers(), badA, st.integers())
def test_making_zaids_outside_A_range_fails(Z, A, m):
    with pytest.raises(ValueError):
        _ = isotopes.ZAID(Z, A, m)


# noinspection PyPep8Naming
@given(st.integers(), st.integers(), badm)
def test_making_zaids_outside_m_range_fails(Z, A, m):
    with pytest.raises(ValueError):
        _ = isotopes.ZAID(Z, A, m)


# noinspection PyUnresolvedReferences
def test_importing_non_existent_isotope_raises_attribute_error():
    with pytest.raises(AttributeError):
        _ = isotopes.Chukumuku146m
    with pytest.raises(AttributeError):
        _ = isotopes.H56


# noinspection PyPep8Naming
@pytest.mark.parametrize(
    ("Z", "A", "m"),
    [(92, 235, 0), (94, 239, 0), (1, 2, 0), (4, 10, 0)])
def test_isotope_is_not_a_zaid(Z: int, A: int, m: int):
    zaid = isotopes.ZAID(Z, A, m)
    isotope = isotopes.Isotope(Z, A, m)
    assert zaid is not isotope
    assert zaid == isotope


def test_illegal_isotope_parameters_cause_valueerror():
    with pytest.raises(ValueError):
        _ = isotopes.Isotope(546, 43, 0)


# noinspection PyPep8Naming
def test_isotopes_are_cached_as_singletons_by_U235_example():
    U235 = isotopes.U235
    assert U235 is isotopes.Isotope(92, 235, 0)
    assert U235 is isotopes.Uranium235


# noinspection PyPep8Naming
@pytest.mark.regression
def test_isotope_has_same_pickle_value_by_regression_of_U238(data_regression):
    data_regression.check({'u238': pickle.dumps(isotopes.U238)})


# noinspection PyPep8Naming
@pytest.mark.regression
def test_unpickled_isotope_has_correct_isotope_data_by_Pu239_example():
    # noinspection PyPep8
    Pu239 = pickle.loads(
        b'\x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00\x8c\x10isotopes.isotope\x94\x8c'
        b'\x07Isotope\x94\x93\x94K^K\xefK\x00\x87\x94\x81\x94.')
    pu = isotopes.ZAID(94, 239, 0)
    assert Pu239.mass == isotopes.Isotope._df.loc[pu]['mass']
    assert Pu239.abundance == isotopes.Isotope._df.loc[pu]['abundance']
    assert Pu239.decay == isotopes.Isotope._df.loc[pu]['decay']


@pytest.mark.parametrize("z", range(1, 93))
def test_element_abundance_is_a_dictionary_with_element_isotopes_keys_and_fraction_values(
        z: int):
    try:
        iso = isotopes.Isotope(z, 0, 0)
    except ValueError:
        return
    assert (all(x.Z == z and isinstance(x, isotopes.Isotope) and 0 <= v <= 1.
                for x, v in iso.abundance.items())
            )


def test_different_name_formats_give_the_same_isotope_by_example():
    assert isotopes.Isotope.from_name("Am242n") == isotopes.Isotope.from_name(
        "Am242m2") == isotopes.Isotope.from_name("Americium242m2") == isotopes.Isotope.from_name(
        "Americium242n")
    assert isotopes.Isotope.from_name("U216m") == isotopes.Isotope.from_name(
        "U216m1") == isotopes.Isotope.from_name("Uranium216m1") == isotopes.Isotope.from_name("Uranium216m")
