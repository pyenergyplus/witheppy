# Copyright (c) 2018, 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for extfields"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import StringIO
from witheppy.iddcurrent import iddcurrent
import pytest

# from six import string_types

from witheppy.eppyhelpers import extfields
from eppy.modeleditor import IDF
from eppy.modeleditor import IDDAlreadySetError


idftxt = """Version,8.9;


BuildingSurface:Detailed,
Zn001:Wall001,           !- Name
Wall,                    !- Surface Type
R13WALL,                 !- Construction Name
Main Zone,               !- Zone Name
,                        !- Space Name
Outdoors,                !- Outside Boundary Condition
,                        !- Outside Boundary Condition Object
SunExposed,              !- Sun Exposure
WindExposed,             !- Wind Exposure
0.5000000,               !- View Factor to Ground
4,                       !- Number of Vertices
0.0,0.0,3.0,  !- X,Y,Z ==> Vertex 1 {m}
0.0,0.0,2.4,  !- X,Y,Z ==> Vertex 2 {m}
30.5,0.0,2.4,  !- X,Y,Z ==> Vertex 3 {m}
30.5,0.0,3.0;  !- X,Y,Z ==> Vertex 4 {m}
BranchList,
Heating Supply Side Branches,  !- Name
Heating Supply Inlet Branch,  !- Branch 1 Name
Central Boiler Branch,   !- Branch 2 Name
Heating Supply Bypass Branch,  !- Branch 3 Name
Heating Supply Outlet Branch;  !- Branch 4 Name
"""


def test_extensiblefields2list(makeIDFfortesting):
    """py.test for extensiblefields2list"""
    tdata = (
        (
            "branchlist",
            False,
            [
                "Heating Supply Inlet Branch",
                "Central Boiler Branch",
                "Heating Supply Bypass Branch",
                "Heating Supply Outlet Branch",
            ],
        ),  # idfkey, nested, expected
        (
            "BuildingSurface:Detailed",
            False,
            [0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0],
        ),  # idfkey, nested, expected
        (
            "BuildingSurface:Detailed",
            True,
            [(0.0, 0.0, 3.0), (0.0, 0.0, 2.4), (30.5, 0.0, 2.4), (30.5, 0.0, 3.0)],
        ),  # idfkey, nested, expected
        (
            "branchlist",
            True,
            [
                "Heating Supply Inlet Branch",
                "Central Boiler Branch",
                "Heating Supply Bypass Branch",
                "Heating Supply Outlet Branch",
            ],
        ),  # idfkey, nested, expected
        ("version", False, None),  # idfkey, nested, expected
    )
    for idfkey, nested, expected in tdata:
        fIDF = makeIDFfortesting
        idf = fIDF(StringIO(idftxt))
        idfobject = idf.idfobjects[idfkey.upper()][0]
        result = extfields.extensiblefields2list(idfobject, nested=nested)
        print(result)
        print(expected)
        assert result == expected
    # test for edge conditions
    # there no values in the extensible fields
    key = "Schedule:Week:Compact".upper()
    idfobject = idf.newidfobject(key)
    result = extfields.extensiblefields2list(idfobject)
    assert result == []


def test_list2extensiblefields(makeIDFfortesting):
    """py.test for list2extensiblefields"""
    tdata = (
        (
            "branchlist",
            ["11", "22", "33"],
            ["11", "22", "33"],
        ),  # idfkey, nlst, expected
        (
            "BuildingSurface:Detailed",
            [11, 22, 33, 1, 2, 3],
            [(11, 22, 33), (1, 2, 3)],
        ),  # idfkey, nlst, expected
        (
            "BuildingSurface:Detailed",
            [(1, 2, 3), (11, 22, 33)],
            [(1, 2, 3), (11, 22, 33)],
        ),  # idfkey, nlst, expected
        (
            "BuildingSurface:Detailed",
            [(1, 2, 3), (11, 22, 33)],
            [(1, 2, 3), (11, 22, 33)],
        ),  # idfkey, nlst, expected
        (
            "BuildingSurface:Detailed",
            [(1, 2, 3), (11, 22, 33)],
            [(1, 2, 3), (11, 22, 33)],
        ),  # idfkey, nlst, expected
        (
            "branchlist",
            ["11", "22", "33"],
            ["11", "22", "33"],
        ),  # idfkey, nlst, expected
    )
    for idfkey, nlst, expected in tdata:
        fIDF = makeIDFfortesting
        idf = fIDF(StringIO(idftxt))
        idfobject = idf.idfobjects[idfkey.upper()][0]
        extfields.list2extensiblefields(idfobject, nlst)
        result = extfields.extensiblefields2list(idfobject, nested=True)
        assert result == expected
    # test for edge conditions
    # there no values in the extensible fields
    # and the field just before begin-extensible field has no value
    key = "Schedule:Week:Compact".upper()
    idfobject = idf.newidfobject(key)
    nlst = [1, 2, 3, 4]
    expected = [1, 2, 3, 4]
    extfields.list2extensiblefields(idfobject, nlst)
    result = extfields.extensiblefields2list(idfobject, nested=False)
    assert result == expected


def extendlist():
    """py.test for extendlist"""
    tdata = (
        ([1, 2, 3], 5, "", [1, 2, 3, "", ""]),  # lst, size, fillwith, expected
        ([1, 2, 3], 3, "", [1, 2, 3]),  # lst, size, fillwith, expected
        ([1, 2, 3], 2, "", [1, 2, 3]),  # lst, size, fillwith, expected
    )
    for lst, size, fillwith, expected in tdata:
        result = extfields.extendlist(lst, size, fillwith=fillwith)
        assert result == expected


def test_grouper():
    """py.test for grouper"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx""
    result = list(extfields.grouper([1, 2, 3, 4, 5, 6, 7], 3, 9))
    assert result == [(1, 2, 3), (4, 5, 6), (7, 9, 9)]
