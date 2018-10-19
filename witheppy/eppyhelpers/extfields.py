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

# TODO
#
# - numpy type doc comments
# - common idd reader for tests
# - now extensiblefields2list returns flat list - can return nested lists
# - useful to return first field names - first_extfieldnames(idfobject)


def extensiblefields2list(idfobject):
    """get the list of extensible fields from the idfobject"""
    if iddhelpers.hasextensible(idfobject.objidd):
        start = iddhelpers.beginextensible_at(idfobject.objidd)
        return idfobject.fieldvalues[start:]
    else:
        return None


def list2extensiblefields(idfobject, lst):
    """push a list of extensible fields into the idfobject"""
    start = iddhelpers.beginextensible_at(idfobject.objidd)
    idfobject.obj = idfobject.obj[:start] + lst
    return idfobject
