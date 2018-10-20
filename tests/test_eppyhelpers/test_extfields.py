# Copyright (c) 2018 Santosh Philip
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
# from six import string_types

from witheppy.eppyhelpers import extfields
from eppy.modeleditor import IDF

iddtxt = """!IDD_Version 8.9.0
!IDD_BUILD 40101eaafd
Version,
  \\memo Specifies the EnergyPlus version of the IDF file.
  \\unique-object
  \\format singleLine
A1 ; \\field Version Identifier
  \\default 8.9
BranchList,
\\extensible:1 Just duplicate last field and comments (changing numbering, please)
\\memo Branches MUST be listed in Flow order: Inlet branch, then parallel branches, then Outlet branch.
\\memo Branches are simulated in the order listed.  Branch names cannot be duplicated within a single branch list.
A1,  \\field Name
   \\required-field
   \\reference BranchLists
A2, \\field Branch 1 Name
   \\begin-extensible
   \\required-field
   \\type object-list
   \\object-list Branches
A3, \\field Branch 2 Name
   \\type object-list
   \\object-list Branches
A4, \\field Branch 3 Name
   \\type object-list
   \\object-list Branches
A5, \\field Branch 4 Name
   \\type object-list
   \\object-list Branches
A6, \\field Branch 5 Name
   \\type object-list
   \\object-list Branches
A7, \\field Branch 6 Name
   \\type object-list
   \\object-list Branches
A8, \\field Branch 7 Name
   \\type object-list
   \\object-list Branches
A9; \\field Branch 8 Name
   \\type object-list
   \\object-list Branches
BuildingSurface:Detailed,
\\memo Allows for detailed entry of building heat transfer surfaces.  Does not include subsurfaces such as windows or doors.
\\extensible:3 -- duplicate last set of x,y,z coordinates (last 3 fields), remembering to remove ; from "inner" fields.
\\format vertices
\\min-fields 19
A1 , \\field Name
   \\required-field
   \\type alpha
   \\reference SurfaceNames
   \\reference SurfAndSubSurfNames
   \\reference AllHeatTranSurfNames
   \\reference OutFaceEnvNames
   \\reference AllHeatTranAngFacNames
   \\reference RadiantSurfaceNames
   \\reference AllShadingAndHTSurfNames
   \\reference FloorSurfaceNames
A2 , \\field Surface Type
   \\required-field
   \\type choice
   \\key Floor
   \\key Wall
   \\key Ceiling
   \\key Roof
A3 , \\field Construction Name
   \\required-field
   \\note To be matched with a construction in this input file
   \\type object-list
   \\object-list ConstructionNames
A4 , \\field Zone Name
   \\required-field
   \\note Zone the surface is a part of
   \\type object-list
   \\object-list ZoneNames
A5 , \\field Outside Boundary Condition
   \\required-field
   \\type choice
   \\key Adiabatic
   \\key Surface
   \\key Zone
   \\key Outdoors
   \\key Foundation
   \\key Ground
   \\key GroundFCfactorMethod
   \\key OtherSideCoefficients
   \\key OtherSideConditionsModel
   \\key GroundSlabPreprocessorAverage
   \\key GroundSlabPreprocessorCore
   \\key GroundSlabPreprocessorPerimeter
   \\key GroundBasementPreprocessorAverageWall
   \\key GroundBasementPreprocessorAverageFloor
   \\key GroundBasementPreprocessorUpperWall
   \\key GroundBasementPreprocessorLowerWall
A6,  \\field Outside Boundary Condition Object
   \\type object-list
   \\object-list OutFaceEnvNames
   \\note Non-blank only if the field Outside Boundary Condition is Surface,
   \\note Zone, OtherSideCoefficients or OtherSideConditionsModel
   \\note If Surface, specify name of corresponding surface in adjacent zone or
   \\note specify current surface name for internal partition separating like zones
   \\note If Zone, specify the name of the corresponding zone and
   \\note the program will generate the corresponding interzone surface
   \\note If Foundation, specify the name of the corresponding Foundation object and
   \\note the program will calculate the heat transfer appropriately
   \\note If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
   \\note If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel
A7 , \\field Sun Exposure
   \\type choice
   \\key SunExposed
   \\key NoSun
   \\default SunExposed
A8,  \\field Wind Exposure
   \\type choice
   \\key WindExposed
   \\key NoWind
   \\default WindExposed
N1,  \\field View Factor to Ground
   \\type real
   \\note From the exterior of the surface
   \\note Unused if one uses the "reflections" options in Solar Distribution in Building input
   \\note unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
   \\note autocalculate will automatically calculate this value from the tilt of the surface
   \\autocalculatable
   \\minimum 0.0
   \\maximum 1.0
   \\default autocalculate
N2 , \\field Number of Vertices
   \\note shown with 120 vertex coordinates -- extensible object
   \\note  "extensible" -- duplicate last set of x,y,z coordinates (last 3 fields),
   \\note remembering to remove ; from "inner" fields.
   \\note for clarity in any error messages, renumber the fields as well.
   \\note (and changing z terminator to a comma "," for all but last one which needs a semi-colon ";")
   \\autocalculatable
   \\minimum 3
   \\default autocalculate
   \\note vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
   \\note are "relative" to the Zone Origin.  If world, then building and zone origins are used
   \\note for some internal calculations, but all coordinates are given in an "absolute" system.
N3,  \\field Vertex 1 X-coordinate
   \\begin-extensible
   \\required-field
   \\units m
   \\type real
N4 , \\field Vertex 1 Y-coordinate
   \\required-field
   \\units m
   \\type real
N5 , \\field Vertex 1 Z-coordinate
   \\required-field
   \\units m
   \\type real
N6,  \\field Vertex 2 X-coordinate
   \\required-field
   \\units m
   \\type real
N7,  \\field Vertex 2 Y-coordinate
   \\required-field
   \\units m
   \\type real
N8,  \\field Vertex 2 Z-coordinate
   \\required-field
   \\units m
   \\type real
N9,  \\field Vertex 3 X-coordinate
   \\required-field
   \\units m
   \\type real
N10, \\field Vertex 3 Y-coordinate
   \\required-field
   \\units m
   \\type real
N11, \\field Vertex 3 Z-coordinate
   \\required-field
   \\units m
   \\type real
N12, \\field Vertex 4 X-coordinate
   \\units m
   \\type real
N13, \\field Vertex 4 Y-coordinate
   \\type real
   \\units m
N14, \\field Vertex 4 Z-coordinate
   \\units m
   \\type real
N15, \\field Vertex 5 X-coordinate
   \\units m
   \\type real
N16, \\field Vertex 5 Y-coordinate
   \\type real
   \\units m
N17, \\field Vertex 5 Z-coordinate
   \\units m
   \\type real
N18, \\field Vertex 6 X-coordinate
   \\units m
   \\type real
N19, \\field Vertex 6 Y-coordinate
   \\type real
   \\units m
N20, \\field Vertex 6 Z-coordinate
   \\units m
   \\type real
N21, \\field Vertex 7 X-coordinate
   \\units m
   \\type real
N22, \\field Vertex 7 Y-coordinate
   \\type real
   \\units m
N23, \\field Vertex 7 Z-coordinate
   \\units m
   \\type real
N24, \\field Vertex 8 X-coordinate
   \\units m
   \\type real
N25, \\field Vertex 8 Y-coordinate
   \\type real
   \\units m
N26; \\field Vertex 8 Z-coordinate
   \\units m
   \\type real"""  # noqa: E501

idftxt = """Version,8.9;


BuildingSurface:Detailed,
WALL-1PF,                !- Name
WALL,                    !- Surface Type
WALL-1,                  !- Construction Name
PLENUM-1,                !- Zone Name
Outdoors,                !- Outside Boundary Condition
,                        !- Outside Boundary Condition Object
SunExposed,              !- Sun Exposure
WindExposed,             !- Wind Exposure
0.50000,                 !- View Factor to Ground
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

IDF.setiddname(StringIO(iddtxt))


def test_extensiblefields2list():
    """py.test for extensiblefields2list"""
    tdata = ((
        "branchlist", False,
        [
            "Heating Supply Inlet Branch",
            "Central Boiler Branch",
            "Heating Supply Bypass Branch",
            "Heating Supply Outlet Branch"
        ]),  # idfkey, nested, expected
        (
        "BuildingSurface:Detailed", False,
        [
            0.0, 0.0, 3.0,
            0.0, 0.0, 2.4,
            30.5, 0.0, 2.4,
            30.5, 0.0, 3.0
        ]),  # idfkey, nested, expected
        (
        "BuildingSurface:Detailed", True,
        [
            (0.0, 0.0, 3.0),
            (0.0, 0.0, 2.4),
            (30.5, 0.0, 2.4),
            (30.5, 0.0, 3.0)
        ]),  # idfkey, nested, expected
        (
        "version", False, None),  # idfkey, nested, expected
    )
    for idfkey, nested, expected in tdata:
        idf = IDF(StringIO(idftxt))
        idfobject = idf.idfobjects[idfkey.upper()][0]
        result = extfields.extensiblefields2list(idfobject, nested=nested)
        assert result == expected


def test_list2extensiblefields():
    """py.test for list2extensiblefields"""
    tdata = (
        ("branchlist", [11, 22, 33], False, [11, 22, 33]),  # idfkey, nlst, nested, expected
        ("BuildingSurface:Detailed",
            [11, 22, 33], False, [11, 22, 33]),  # idfkey, nlst, nested, expected
        ("BuildingSurface:Detailed",
            [(1,2,3),(11, 22, 33)], True, [(1,2,3), (11, 22, 33)]),  # idfkey, nlst, nested, expected
    )
    for idfkey, nlst, nested, expected in tdata:
        idf = IDF(StringIO(idftxt))
        idfobject = idf.idfobjects[idfkey.upper()][0]
        extfields.list2extensiblefields(idfobject, nlst, nested=nested)
        result = extfields.extensiblefields2list(idfobject, nested=nested)
        assert result == expected
