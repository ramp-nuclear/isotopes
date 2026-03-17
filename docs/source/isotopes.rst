Reference Guide
===============

Isotope 
-------

.. automodule:: isotopes.isotope
   :members:
   :undoc-members:
   :show-inheritance:

ZAID
----

.. automodule:: isotopes.zaid
   :members:
   :undoc-members:
   :show-inheritance:

Extreme Magic
-------------
To make importing isotopes easier, we have some extreme magic going on in
our module's `__getattr__`. It ensures that isotopes are created when imported
by name.
The auto-completion is possible because we also include a `.pyi` file with all
of the possible isotope names.
We test by regression that the list is up to date, so we can be quite sure that
it represents all the possible Isotope values, too.

.. autofunction:: isotopes.__getattr__


