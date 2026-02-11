# isotopes
isotopes is a relatively low level python code used to define integer representations for nuclides.
It is supposed to be used as part of the RAMP project, but it may be general enough for other purposes
as well.

isotopes includes two main classes, the ZAID class and the Isotope class.

ZAID objects are just integer representations of nuclides, such as the ones used by the ENDF library.
They help as python based, low memory footprint, hashable objects for dictionaries of nuclide->values.
Isotope objects actually represent physical isotopes in nature, and include physical information about
these, such as their abundance, mass, etc.
Isotopes are primarily designed for use when defining material mixtures, and for an easy representation
as a ZAID when dealing with low level data such as ENDF or transport codes that use ZAIDs for material
representation.
