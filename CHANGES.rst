Changelog
=========

0.3.1 (upcoming)
----------------

Enhancements
~~~~~~~~~~~~
- Bump minimum Blosc version to support zero-copy decompression in our ASDF fork

0.3.0 (2020-08-11)
------------------

Enhancements
~~~~~~~~~~~~
- Use 4 Blosc threads for decompression by default

Fixes
~~~~~
- Specify minimum Astropy version to avoid
  ``AttributeError: 'numpy.ndarray' object has no attribute 'info'``
  
0.2.0 (2020-07-08)
------------------

New Features
~~~~~~~~~~~~
- Add pipe_asdf.py script as an example of using Python to deal with file container
  so that C/Fortran/etc don't have to know about ASDF or blosc

0.1.0 (2020-06-24)
------------------

New Features
~~~~~~~~~~~~
- CompaSOHaloCatalog accepts ``fields`` keyword to limit the IO and unpacking to
  the requsted halo catalog columns

0.0.5 (2020-05-26)
------------------

- First stable release
