# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for extfields"""

from witheppy.eppyhelpers import extfields


def test_add():
    """py.test for add"""
    result = extfields.add(1, 2)
    assert result == 3


def test_extensiblefields2list():
    """py.test for extensiblefields2list"""
    pass