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


# TODO : update the docstrings for nested=True
# TODO : run lint
# TODO : will fail on branchlist if nested=True

# from six import StringIO
# from six import string_types
from witheppy.eppyhelpers import iddhelpers

from itertools import chain
try:
    from itertools import zip_longest  # python3
except ImportError as e:
    from itertools import izip_longest as zip_longest

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def extensiblefields2list(idfobject, nested=True):
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
        extvalues = idfobject.fieldvalues[start:]
        if nested:
            ext_n = iddhelpers.hasextensible(idfobject.objidd)
            return list(grouper(extvalues, ext_n))
        else:
            return extvalues
    else:
        return None


def list2extensiblefields(idfobject, lst, nested=True):
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
    if nested:
        ulst = list(chain.from_iterable(lst))  # unpack nesting
    else:
        ulst = lst
    idfobject.obj = idfobject.obj[:start] + ulst
    return idfobject
