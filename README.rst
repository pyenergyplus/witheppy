========
witheppy
========


.. image:: https://img.shields.io/pypi/v/witheppy.svg
        :target: https://pypi.python.org/pypi/witheppy

.. image:: https://img.shields.io/travis/pyenergyplus/witheppy.svg
        :target: https://travis-ci.org/pyenergyplus/witheppy

.. image:: https://readthedocs.org/projects/witheppy/badge/?version=latest
        :target: https://witheppy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python packages built using eppy


* Free software: MIT license
* Documentation: https://witheppy.readthedocs.io.


Features
--------

* includes additional functionality that can be used with `eppy <https://github.com/santoshphilip/eppy>`_

What is witheppy
----------------

Witheppy is a python package that gathers all the useful functions written with eppy. Many people have used eppy and some have written functions that may be useful to practitioners at large. This becomes an organized place to upload this code.

More will be written on where to upload the code and how to document it. The functions will fall under multiple categories, such as idfhelpers, geometry, HVAC, JSON reader. 

The JSON reader may be the most critical functionality. E+ is transitioning towards using a JSON file format instead of the IDD/IDF text format. At one point all E+ files will be in the JSON format. Right now eppy cannot read the JSON format. The intent is to have JSON reader in witheppy for eppy.

Witheppy to eppy
----------------

Any code put into witheppy proves to be useful, it will be transitioned into eppy. To ensure that witheppy is working as intended, the maintainers of eppy will not write code directly into eppy. All code intended for eppy will be first written in witheppy and then if it proves to be useful, it will be transitioned into eppy.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage