# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""helper functions to work with the idd"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from six import StringIO
# from six import string_types


def hasextensible(objidd):
    """Return the value of # in extensible:<#>if there is an extensible field.
    Return None if there is no extensible fields

    from the documentation in the file Energy+.idd:

    extensible:<#>

    This object is dynamically extensible -- meaning, if you
    change the IDD appropriately (if the object has a simple list
    structure -- just add items to the list arguments (i.e. BRANCH
    LIST). These will be automatically redimensioned and used during
    the simulation. <#> should be entered by the developer to signify
    how many of the last fields are needed to be extended (and EnergyPlus
    will attempt to auto-extend the object).  The first field of the first
    instance of the extensible field set is marked with begin-extensible.

    Return the value of #

    Parameters
    ----------
    objidd : list
        The idd for a specific idfobject

    Returns
    -------
    lastfields: int
        number of fields that are extended fields that repeat
    lastfields: None
        if there are no extended fields
    """
    objidd0 = objidd[0]
    keys = objidd0.keys()
    ekey = [key for key in keys if key.startswith("extensible")]
    if ekey:
        ekey = ekey[0]
        ekey.strip()
        key, val = ekey.split(":")
        val = int(val)
        return val
    else:
        return None


def beginextensible_at(objidd):
    """Return the index of the field that is the start of the extensible fields.

    In the idd, this is tagged by begin-extensible

    from the documentation in the file Energy+.idd:

    begin-extensible

    Marks the first field at which the object accepts an extensible
    field set.  A fixed number of fields from this marker define the
    extensible field set,  see the object code extensible for
    more information.

    Parameters
    ----------
    objidd : list
        The idd for a specific idfobject

    Returns
    -------
    int
        index of the field that is the start of the extensible fields
    """
    extensibleval = hasextensible(objidd)
    if extensibleval:
        for i, idditem in enumerate(objidd):
            if "begin-extensible" in idditem:
                return i
    return None
