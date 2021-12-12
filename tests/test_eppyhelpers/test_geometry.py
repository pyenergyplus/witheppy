# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for eppyhelpers/geometry.py"""

from io import StringIO
import pytest
from witheppy.eppyhelpers import geometry
from witheppy.eppyhelpers import extfields


def putverticesinwindow(wind1, vertices):
    for i, (x, y, z) in zip(range(1, len(vertices) + 1), vertices):
        wind1[f"Vertex_{i}_Xcoordinate"] = x
        wind1[f"Vertex_{i}_Ycoordinate"] = y
        wind1[f"Vertex_{i}_Zcoordinate"] = z
    return wind1


@pytest.fixture(scope="function")
def idfsnippet(makeIDFfortesting):
    """generatea an idff snippet that can be used in this module"""
    # if we use a text snippet as the idf,
    # it may break in future versions of E+ (order of fields may change)
    # generating an idf proramatically will avoid that issue.
    vertices = [[j * i for j in (2, 5, 1)] for i in range(1, 5)]
    # actual vertix value is not important
    fIDF = makeIDFfortesting
    idf = fIDF(StringIO(""))
    zone1 = idf.newidfobject("zone", Name="ZONE1")

    # Make a wall belonging to zone1
    extwallzone1 = idf.newidfobject(
        "BuildingSurface:Detailed",
        Name="EXTWALLZONE1",
        Surface_Type="WALL",
        Construction_Name="WALL-1",
        Zone_Name="ZONE1",
        Outside_Boundary_Condition="Outdoors",
        Number_of_Vertices=4,
    )
    extfields.list2extensiblefields(extwallzone1, vertices)
    # make a window in EXTWALLZONE1
    wind1 = idf.newidfobject(
        "FenestrationSurface:Detailed",
        Name="WF-1",
        Surface_Type="WINDOW",
        Construction_Name="bouleglazed",
        Building_Surface_Name="EXTWALLZONE1",
        Number_of_Vertices=4,
    )
    wind1 = putverticesinwindow(wind1, vertices)
    # copy that window and rename
    wind2 = idf.copyidfobject(wind1)
    wind2.Name = "WF-2"
    # int walls
    intwall1zone1 = geometry.copyidfobject(
        idf,
        extwallzone1,
        Name="INTWALL1ZONE1",
        Outside_Boundary_Condition="Surface",
        Outside_Boundary_Condition_Object="INTWALL3ZONE2",
        Sun_Exposure="NoSun",
        Wind_Exposure="NoWind",
    )
    intwall2zone1 = geometry.copyidfobject(
        idf,
        intwall1zone1,
        Name="INTWALL2ZONE1",
        Outside_Boundary_Condition_Object="something",
    )
    intwall3zone1 = geometry.copyidfobject(
        idf,
        intwall1zone1,
        Name="INTWALL3ZONE1",
        Outside_Boundary_Condition_Object="INTWALL1ZONE2",
    )
    # ----
    # zone 2
    zone2 = idf.newidfobject("zone", Name="ZONE2")
    # ext wall for zone2
    extwallzone2 = geometry.copyidfobject(idf, extwallzone1, Zone_Name="ZONE2")
    # int walls for zone2
    intwall1zone2 = geometry.copyidfobject(
        idf,
        intwall1zone1,
        Name="INTWALL1ZONE2",
        Zone_Name="ZONE2",
        Outside_Boundary_Condition_Object="INTWALL3ZONE1",
    )
    intwall2zone2 = geometry.copyidfobject(
        idf,
        intwall1zone2,
        Name="INTWALL2ZONE2",
        Outside_Boundary_Condition_Object="something else",
    )
    intwall3zone2 = geometry.copyidfobject(
        idf,
        intwall1zone2,
        Name="INTWALL3ZONE2",
        Outside_Boundary_Condition_Object="INTWALL1ZONE1",
    )
    # ---
    # data for mergezones
    zone3 = idf.newidfobject("zone", Name="ZONE3", X_Origin=1, Y_Origin=2, Z_Origin=3)
    zone4 = idf.newidfobject("zone", Name="ZONE4")
    zone5 = idf.newidfobject("zone", Name="ZONE5", X_Origin=3, Y_Origin=2, Z_Origin=1)
    extwallzone3 = geometry.copyidfobject(
        idf, extwallzone1, Name="EXTWALLZONE3", Zone_Name="ZONE3"
    )
    extwallzone4 = geometry.copyidfobject(
        idf, extwallzone1, Name="EXTWALLZONE4", Zone_Name="ZONE4"
    )
    extwallzone5 = geometry.copyidfobject(
        idf, extwallzone1, Name="EXTWALLZONE5", Zone_Name="ZONE5"
    )
    intwall1zone4 = geometry.copyidfobject(
        idf,
        intwall1zone1,
        Name="INTWALLZONE4",
        Zone_Name="ZONE4",
        Outside_Boundary_Condition_Object="INTWALLZONE5",
    )
    intwall1zone5 = geometry.copyidfobject(
        idf,
        intwall1zone1,
        Name="INTWALLZONE5",
        Zone_Name="ZONE5",
        Outside_Boundary_Condition_Object="INTWALLZONE4",
    )
    return idf


def test_shiftwindows(idfsnippet):
    """py.test for shiftwindows"""
    shift = (1, 2, 3)
    sx, sy, sz = shift
    idf = idfsnippet
    idfwindow = idf.idfobjects["FenestrationSurface:Detailed"][0]
    coords = idfwindow.coords
    expected = [(x - sx, y - sy, z - sz) for x, y, z in coords]
    result = geometry.shiftwindows(idfwindow, shift)
    rcoords = result.coords
    assert rcoords == expected


def test_shiftsurface(idfsnippet):
    """py.test for shiftsurface"""
    shift = (1, 2, 3)
    sx, sy, sz = shift
    idf = idfsnippet
    idfsurface = idf.idfobjects["BuildingSurface:Detailed"][0]
    coords = idfsurface.coords
    expected = [(x - sx, y - sy, z - sz) for x, y, z in coords]
    result = geometry.shiftsurface(idfsurface, shift)
    rcoords = result.coords
    assert rcoords == expected


def test_shiftsurfacewithwindows(idfsnippet):
    """docstring for shiftsurfacewithwindows"""
    idf = idfsnippet
    shift = (1, 2, 3)
    sx, sy, sz = shift
    surfs = idf.idfobjects["BuildingSurface:Detailed"]
    winds = idf.idfobjects["FenestrationSurface:Detailed"]
    scoords = surfs[0].coords
    w1coords = winds[0].coords
    w2coords = winds[1].coords
    s_expected = [(x - sx, y - sy, z - sz) for x, y, z in scoords]
    w1_expected = [(x - sx, y - sy, z - sz) for x, y, z in w1coords]
    w2_expected = [(x - sx, y - sy, z - sz) for x, y, z in w2coords]
    surf, windows = geometry.shiftsurfacewithwindows(idf, surfs[0], shift)
    assert surf.coords == s_expected
    assert windows[0].coords == w1_expected
    assert windows[1].coords == w2_expected


def test_commonsurfaces(idfsnippet):
    """py.test for commonsurfaces"""
    idf = idfsnippet
    zones = idf.idfobjects["zone"]
    result = geometry.commonsurfaces(idf, zones[0], zones[1])
    intwall1z1 = idf.getobject("BuildingSurface:Detailed", "INTWALL1ZONE1")
    intwall3z2 = idf.getobject("BuildingSurface:Detailed", "INTWALL3ZONE2")
    intwall3z1 = idf.getobject("BuildingSurface:Detailed", "INTWALL3ZONE1")
    intwall1z2 = idf.getobject("BuildingSurface:Detailed", "INTWALL1ZONE2")
    expected = [(intwall1z1, intwall3z2), (intwall3z1, intwall1z2)]
    assert result == expected


def test_mergezones(idfsnippet):
    """py.test for mergezones"""
    idf = idfsnippet
    extwallzone5 = idf.getobject("BuildingSurface:Detailed", "EXTWALLZONE5")
    # --
    coords = extwallzone5.coords
    sx, sy, sz = (1 - 3, 2 - 2, 3 - 1)
    expectedcoords = [(x - sx, y - sy, z - sz) for x, y, z in coords]
    # --
    idf = geometry.mergezones(idf, ["ZONE3", "ZONE4", "ZONE5"])
    print(extwallzone5.coords)
    zones = idf.idfobjects["zone"]
    znames = [zone.Name for zone in zones]
    # check if the merged zones are gone
    assert "ZONE4" not in znames
    assert "ZONE5" not in znames
    # check if ext wall of merges zones exist, but int walls are gone
    surfs = idf.idfobjects["BuildingSurface:Detailed"]
    mergedwalls = [
        surf for surf in surfs if surf.Zone_Name in ["ZONE3", "ZONE4", "ZONE5"]
    ]
    assert len(mergedwalls) == 3
    extwallzone5 = idf.getobject("BuildingSurface:Detailed", "EXTWALLZONE5")
    # check if the walls have shifted
    assert extwallzone5.coords == expectedcoords
