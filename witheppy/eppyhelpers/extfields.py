# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""functions to work with extensiblefields"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from six import StringIO
# from six import string_types
from witheppy.eppyhelpers import iddhelpers


def extensiblefields2list(idfobject):
    """returns extensible fields of idfobject as a list

    It is useful to have the fields as a list. It is easy to manipulate
    the items in the list, by using the list functions such as pop, insert,
    remove etc. This list can be put back in the idfobject by using the
    function list2extensiblefields(...)

    Parameters
    ----------
    idfobject : eppy.bunch_subclass.EpBunch
        an idfobject such as BRANCHLIST, BUILDINGSURFACE:DETAILED etc.

    Returns
    -------
    list
        all the extended field values as a list
    """
    if iddhelpers.hasextensible(idfobject.objidd):
        start = iddhelpers.beginextensible_at(idfobject.objidd)
        return idfobject.fieldvalues[start:]
    else:
        return None


def list2extensiblefields(idfobject, lst):
    """Replaces the items in the extensible fields with items in lst

    This function is a counterpart to the function extensiblefields2list().
    The list returned by extensiblefields2list can be changed and put back into
    the idfobject by this function

    Parameters
    ----------
    idfobject : eppy.bunch_subclass.EpBunch
        an idfobject such as BRANCHLIST, BUILDINGSURFACE:DETAILED etc.
    lst: list
        This list will replace the items in the extended fields
        of the idfobject

    Returns
    -------
    eppy.bunch_subclass.EpBunch
        the idfobject is changed in place and returned by the function
    """
    start = iddhelpers.beginextensible_at(idfobject.objidd)
    idfobject.obj = idfobject.obj[:start] + lst
    return idfobject
