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
    """Return None if there is no extensible fields
    return # if there is an extensible field, the format is extensible:#"""
    objidd0 = objidd[0]
    keys = objidd0.keys()
    ekey = [key for key in keys if key.startswith('extensible')]
    if ekey:
        ekey = ekey[0]
        ekey.strip()
        key, val = ekey.split(':')
        val = int(val)
        return val
    else:
        return None


def beginextensible_at(objidd):
    """return the index of the field that is the start of the extensible fields.
    In the idd, this is tagged by begin-extensible"""
    extensibleval = hasextensible(objidd)
    if extensibleval:
        for i, idditem in enumerate(objidd):
            if u'begin-extensible' in idditem:
                return i
                break
    return None
    

