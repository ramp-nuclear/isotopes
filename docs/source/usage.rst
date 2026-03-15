Usage
-----
Using this package is relatively straightforward.
There are two common paths that people take directly, and one common path
when deserializing data.

Named usage
^^^^^^^^^^^
First, if you are interactively looking to use or get information about an
isotope, you can simply import it.
This package lazily creates only those isotopes you actually use, and it uses
a singlton approach to limit the memory footprint, so you should feel safe in
importing any isotope you need.

.. code-block:: python

   from isotopes import U235, U238
   assert U235.Z == U238.Z
   assert U238.A > U235.A
   assert U238.abundance > U235.abundance

Z-A-m definition and ZAID promotion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to create an isotope not by strict naming but by its ZAID, you
can do so either through direct creation, or by promoting a ZAID. Promoting a
ZAID gives you a fallback option for when data for your isotope is missing and
we can only give you a ZAID object instead:

.. code-block:: python

   from isotopes import ZAID, Isotope, U235

   iso1 = Isotope(92, 235, 0)
   assert iso1 is U235
   iso2 = Isotope.from_zaid_with_fallback(ZAID(92, 235, 0))
   assert iso2 is iso1 is U235


Integer promotion
^^^^^^^^^^^^^^^^^
Sometimes, you already have a ZAID as its integer number. This is often the case
when you're deserialzing isotopes from some ascii or binary format.
In this case, you have an integer on your hand, which you want to promote back
to an Isotope, if possible, or a ZAID, if not.
In that case:

.. code-block:: python

   from isotopes import ZAID, Isotope, U235

   i = int(U235)
   iso = Isotope.from_int_with_fallback(i)
   assert iso is U235
