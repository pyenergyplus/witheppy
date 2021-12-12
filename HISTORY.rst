=======
History
=======


Releases
--------

release 0.1.8
-------------

:Date:   Sun Dec 12 11:20:53 2021 -0800


- fixed issue #53
	- :Problem: Need guidance on how to do a release
	- :Solution: Steps for release are documented on CONTRIBUTIONS.rst

:Date:   Sat Dec 11 19:35:58 2021 -0800

- fixed issue #11
	- :Problem: CONTRIBUTIONS.rst page needs to use the C4 contract
	- :Solutions: CONTRIBUTIONS.rst page updated to list the steps in the C4 Contract
	
	

release 0.1.6
-------------

:Date:   Mon Dec 6 14:37:38 2021 -0800

- fixed issue #42
	- :Problem: Need a function to add or remove exhaust fans from a zone
	- :Solution: putexhaust(), removeexhaust(), hasexhaust(), findexhaust() in eppyhelpers.hvac

release 0.1.5
-------------

2021-12-04
~~~~~~~~~~

- fixed issue #39
	- :Problem: Need a function to merge 2 or more zones
	- :Solution: wrote eppyhelpers.mergezones(idf, mergeznames)


release 0.1.4
-------------

2021-01-25
~~~~~~~~~~

- fixed issue #32
	- :Problem: runandget get uses idf.run() which does not allow runs simultaneously
	- :Solution: use idfRUNs() which allows multiple runs simultaneously 

2021-01-22
~~~~~~~~~~

- fixed issue #30
	- :Problem: remove ephtml - this functionality is present in eppy
	- :Solution: removed ephtml- now using eppy.results.fasthtml


2021-01-01
~~~~~~~~~~

- fixed issue #27
    - **Problem:** experimental.runadget() was written in eppy. It should be in witheppy
    - **Solution:** moved runadget() to witheppy

2019-05-23
~~~~~~~~~~

- removed the optional arg weather from eplaunch
    - fix for issue #24


release 0.1.0
-------------

2018-10-15
~~~~~~~~~~

* First release on PyPI.
