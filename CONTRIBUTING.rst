============
Contributing
============

Collective Code Construction Contract
-------------------------------------

The protocol for contributing is based on the Collective Code Construction Contract https://rfc.zeromq.org/spec:42/C4/


Instructions for making contributions
-------------------------------------

Steps for making updates to the software, based on C4 document above:

Definitions
~~~~~~~~~~~

:User: Anyone who uses the software. Sometimes the user runs into an issue with the software
:Contributor: From **C4** Contract: A “Contributor” is a person who wishes to provide a patch, being a set of commits that solve some clearly identified problem. Everyone, without distinction or discrimination, SHALL have an equal right to become a Contributor under the C4 Contract.
:Maintainer: From the **C4** Contract: A “Maintainer” is a person who merges patches to the project. Maintainers are not developers; their job is to enforce process.

Steps on Contributing
~~~~~~~~~~~~~~~~~~~~~

- *User*:
    - Opens an issue in issue tracker, describing problem (called issue #n)
- *Contributor*:
    - forks the repository
    - makes changes
    - commits with appropriate commit following message
      ::
      
        fixed issue #n (*on first line*)
        
        Problem: describe Problem
        Solution: describe Solution

    - Make a pull request
- *Maintainer*:
    - Merge pull request into master
- *User*:
    - Closes issue #n in issue tracker

After the merge, The *Contributor* may want to take the following steps:

- *Contributor*: pull the changes from `pyenergyplus/witheppy` after *Maintainer* has completed the merge
    - This has to be done in the command line
      ::

        git pull --rebase upstream master


    - To do the above you need a remote called `upstream`. You can set this up by the following line in the command line
      ::

        git remote add upstream https://github.com/pyenergyplus/witheppy.git
        # this needs to be done only once
		
Instructions for making a Release
---------------------------------

Releases are made by a designated **Maintainer**. The steps for making a release are listed here for ease of reference. You are welcome to follow a different protocol as long as it achieves the end goals. If there is a better way of doing a release, this section of the document can be updated.


On the local copy (master branch) of the repository:

- rebase master on local # make sure you have the latest:: 

	git pull --rebase upstream master
	
- Update the HISTORY.rst document. You can use commit messages that say "fixed issue #n" to guide you.
- run "make docs" and review the generated documentation
- do bumpversion on master (can be patch, minor or major)::

	bumpversion patch # 0.1.6 -> 0.1.7
	bumpversion minor # 0.1.6 -> 0.2.0
	bumpversion major # 0.1.6 -> 1.0.0

- push master to maintainer's account
- Maintainer does a pull request
- Merge the pull request

on the github website at pytenergyplus/witheppy

- make new release and tag with version number (matching the change made by bumpversion)
	- version 0.1.6 will have a tag `r0.1.6`
	- make release here https://github.com/pyenergyplus/witheppy/releases

On the local copy (master branch) of the repository:

- use "make release" to release to pypi

on https://readthedocs.org website

- build the new docs manually (in case the webhooks did not work)   

	