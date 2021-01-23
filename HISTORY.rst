=======
History
=======

2021-01-22
----------

fixed issue #30

:Problem: remove ephtml - this functionality is present in eppy
:Solution: removed ephtml- now using eppy.results.fasthtml


2021-01-01
----------

- fixed issue #27
    - **Problem:** experimental.runadget() was written in eppy. It should be in witheppy
    - **Solution:** moved runadget() to witheppy

2019-05-23
----------

- removed the optional arg weather from eplaunch
    - fix for issue #24


0.1.0 (2018-10-15)
------------------

* First release on PyPI.
