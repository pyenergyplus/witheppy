# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for hvac.py"""

import pytest
from io import StringIO
from witheppy.eppyhelpers import hvac
import witheppy.eppyhelpers.extfields as extfields

idftxt = """
Zone,
    West Zone,                !- Name
    0,                        !- Direction of Relative North
    0,                        !- X Origin
    0,                        !- Y Origin
    0,                        !- Z Origin
    1,                        !- Type
    1,                        !- Multiplier
    autocalculate,            !- Ceiling Height
    autocalculate;            !- Volume

Zone,
    EAST ZONE,                !- Name
    0,                        !- Direction of Relative North
    0,                        !- X Origin
    0,                        !- Y Origin
    0,                        !- Z Origin
    1,                        !- Type
    1,                        !- Multiplier
    autocalculate,            !- Ceiling Height
    autocalculate;            !- Volume

Zone,
    NORTH ZONE,               !- Name
    0,                        !- Direction of Relative North
    0,                        !- X Origin
    0,                        !- Y Origin
    0,                        !- Z Origin
    1,                        !- Type
    1,                        !- Multiplier
    autocalculate,            !- Ceiling Height
    autocalculate;            !- Volume

ZoneHVAC:EquipmentList,
    Zone1Equipment,           !- Name
    SequentialLoad,           !- Load Distribution Scheme
    ZoneHVAC:AirDistributionUnit,    !- Zone Equipment 1 Object Type
    Zone1TermReheat,          !- Zone Equipment 1 Name
    1,                        !- Zone Equipment 1 Cooling Sequence
    1,                        !- Zone Equipment 1 Heating or NoLoad Sequence
    ,                         !- Zone Equipment 1 Sequential Cooling Fraction Schedule Name
    ;                         !- Zone Equipment 1 Sequential Heating Fraction Schedule Name

ZoneHVAC:EquipmentList,
    Zone2Equipment,           !- Name
    SequentialLoad,           !- Load Distribution Scheme
    Fan:ZoneExhaust,          !- Zone Equipment 1 Object Type
    Zone 2 Exhaust Fan,       !- Zone Equipment 1 Name
    2,                        !- Zone Equipment 1 Cooling Sequence
    2,                        !- Zone Equipment 1 Heating or NoLoad Sequence
    ,                         !- Zone Equipment 1 Sequential Cooling Fraction Schedule Name
    ,                         !- Zone Equipment 1 Sequential Heating Fraction Schedule Name
    ZoneHVAC:AirDistributionUnit,    !- Zone Equipment 2 Object Type
    Zone2TermReheat,          !- Zone Equipment 2 Name
    1,                        !- Zone Equipment 2 Cooling Sequence
    1,                        !- Zone Equipment 2 Heating or NoLoad Sequence
    ,                         !- Zone Equipment 2 Sequential Cooling Fraction Schedule Name
    ;                         !- Zone Equipment 2 Sequential Heating Fraction Schedule Name

ZoneHVAC:EquipmentList,
    Zone3Equipment,           !- Name
    SequentialLoad,           !- Load Distribution Scheme
    Fan:ZoneExhaust,          !- Zone Equipment 1 Object Type
    Zone 3 Exhaust Fan,       !- Zone Equipment 1 Name
    2,                        !- Zone Equipment 1 Cooling Sequence
    2,                        !- Zone Equipment 1 Heating or NoLoad Sequence
    ,                         !- Zone Equipment 1 Sequential Cooling Fraction Schedule Name
    ,                         !- Zone Equipment 1 Sequential Heating Fraction Schedule Name
    ZoneHVAC:AirDistributionUnit,    !- Zone Equipment 2 Object Type
    Zone3TermReheat,          !- Zone Equipment 2 Name
    1,                        !- Zone Equipment 2 Cooling Sequence
    1,                        !- Zone Equipment 2 Heating or NoLoad Sequence
    ,                         !- Zone Equipment 2 Sequential Cooling Fraction Schedule Name
    ;                         !- Zone Equipment 2 Sequential Heating Fraction Schedule Name

ZoneHVAC:EquipmentConnections,
    West Zone,                !- Zone Name
    Zone1Equipment,           !- Zone Conditioning Equipment List Name
    Zone1Inlets,              !- Zone Air Inlet Node or NodeList Name
    ,                         !- Zone Air Exhaust Node or NodeList Name
    Zone 1 Node,              !- Zone Air Node Name
    Zone 1 Outlet Node;       !- Zone Return Air Node or NodeList Name

ZoneHVAC:EquipmentConnections,
    EAST ZONE,                !- Zone Name
    Zone2Equipment,           !- Zone Conditioning Equipment List Name
    Zone2Inlets,              !- Zone Air Inlet Node or NodeList Name
    Zone 2 Exhausts,          !- Zone Air Exhaust Node or NodeList Name
    Zone 2 Node,              !- Zone Air Node Name
    Zone 2 Outlet Node;       !- Zone Return Air Node or NodeList Name

ZoneHVAC:EquipmentConnections,
    NORTH ZONE,               !- Zone Name
    Zone3Equipment,           !- Zone Conditioning Equipment List Name
    Zone3Inlets,              !- Zone Air Inlet Node or NodeList Name
    Zone 3 Exhausts,          !- Zone Air Exhaust Node or NodeList Name
    Zone 3 Node,              !- Zone Air Node Name
    Zone 3 Outlet Node;       !- Zone Return Air Node or NodeList Name

Fan:ConstantVolume,
    Supply Fan 1,             !- Name
    FanAndCoilAvailSched,     !- Availability Schedule Name
    0.7,                      !- Fan Total Efficiency
    600,                      !- Pressure Rise
    1.3,                      !- Maximum Flow Rate
    0.9,                      !- Motor Efficiency
    1,                        !- Motor In Airstream Fraction
    Mixed Air Node,           !- Air Inlet Node Name
    Cooling Coil Air Inlet Node;    !- Air Outlet Node Name

Fan:ZoneExhaust,
    Zone 2 Exhaust Fan,       !- Name
    FanAndCoilAvailSched,     !- Availability Schedule Name
    0.6,                      !- Fan Total Efficiency
    125,                      !- Pressure Rise
    0.1,                      !- Maximum Flow Rate
    Zone 2 Exhaust Node,      !- Air Inlet Node Name
    Zone 2 Exhaust Fan Outlet Node;    !- Air Outlet Node Name

Fan:ZoneExhaust,
    Zone 3 Exhaust Fan,       !- Name
    FanAndCoilAvailSched,     !- Availability Schedule Name
    0.6,                      !- Fan Total Efficiency
    125,                      !- Pressure Rise
    0.15,                     !- Maximum Flow Rate
    Zone 3 Exhaust Node,      !- Air Inlet Node Name
    Zone 3 Exhaust Fan Outlet Node;    !- Air Outlet Node Name

  NodeList,
    Zone 2 Exhausts,         !- Name
    Zone 2 Exhaust Node;     !- Node 1 Name

  NodeList,
    Zone 3 Exhausts,         !- Name
    Zone 3 Exhaust Node;     !- Node 1 Name


"""


@pytest.fixture(scope="function")
def idfsnippet(makeIDFfortesting):
    fIDF = makeIDFfortesting
    idf = fIDF(StringIO(idftxt))
    return idf


def test_findequipmentconnection(idfsnippet):
    """py.test for findequipmentconnection"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.findequipmentconnection(idf, zone)
    assert result.Zone_Name == zone.Name
    zone = idf.newidfobject("zone", "gumby")
    result = hvac.findequipmentconnection(idf, zone)
    assert result == None


def test_findequipmentlist(idfsnippet):
    """py.test for findequipmentlist"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.findequipmentlist(idf, zone, testing=True)
    assert result[-1].Zone_Name == zone.Name
    assert result[-1].Zone_Conditioning_Equipment_List_Name == result[0].Name
    zone = idf.newidfobject("zone", "gumby")
    result = hvac.findequipmentlist(idf, zone)
    assert result == None
    econnction = idf.newidfobject("ZoneHVAC:EquipmentConnections", Zone_Name="gumby")
    result = hvac.findequipmentlist(idf, zone)
    assert result == None


def test_hasexhaust(idfsnippet):
    """py.test for hasexhaust"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.hasexhaust(idf, zone)
    assert result == False
    zone = idf.idfobjects["zone"][1]
    result = hvac.hasexhaust(idf, zone)
    assert result == "Zone 2 Exhausts"
    zone = idf.idfobjects["zone"][2]
    result = hvac.hasexhaust(idf, zone)
    assert result == "Zone 3 Exhausts"


def test_findexhaust(idfsnippet):
    """py.test for findexhaust"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.findexhaust(idf, zone)
    assert result == None
    # ---
    exfanname = "Zone 2 Exhaust Fan"
    zone = idf.idfobjects["zone"][1]
    result = hvac.findexhaust(idf, zone)
    assert result.Name == exfanname


def test_removeexhaust(idfsnippet):
    """py.test for removeexhaust"""
    idf = idfsnippet
    zones = idf.idfobjects["zone"]
    zone = zones[1]
    eqlist = hvac.findequipmentlist(idf, zone)
    exfan = hvac.removeexhaust(idf, zone)
    expectedname = "Zone 2 Exhaust Fan"
    assert exfan.Name == expectedname
    assert hvac.hasexhaust(idf, zone) == False
    # test if exhaust fan has been removed from 'ZONEHVAC:EQUIPMENTLIST'
    extlist = extfields.extensiblefields2list(eqlist)
    eqlistitems = [
        item for item in extlist if item[0].upper() == "Fan:ZoneExhaust".upper()
    ]
    assert not eqlistitems  # list should be empty
    # test when you try to remove a nonexistent 
    zone = zones[0]
    exfan = hvac.removeexhaust(idf, zone)
    assert exfan == None

def test_putexhaust(idfsnippet):
    """py.test for putexhaust"""
    idf = idfsnippet
    zones = idf.idfobjects["zone"]
    zone = zones[0]
    exfan = idf.newidfobject("Fan:ZoneExhaust", Name="zone1_exhaust_fan")
    hvac.putexhaust(idf, zone, exfan)
    assert hvac.hasexhaust(idf, zone) == "zone1_exhaust_fan Node List"
    assert hvac.findexhaust(idf, zone) == exfan
    # test if ex fan is in equiplist
    eqlist = hvac.findequipmentlist(idf, zone)
    extlist = extfields.extensiblefields2list(eqlist)
    objecttypes = [item for item in extlist if item[0].upper() == "FAN:ZONEEXHAUST"]
    assert objecttypes # has an item in it ie. "FAN:ZONEEXHAUST"
    # test when there is an existing exhaust
    with pytest.raises(hvac.HasExhaustFanError):
        zone = zones[1]
        exfan = idf.newidfobject("Fan:ZoneExhaust", Name="zone2_exhaust_fan")
        hvac.putexhaust(idf, zone, exfan)
        

# TODO add and remove exhaust fans in multiple example files - to see how robust it is.
# DONE use the functions to change TermReheatZoneExh.idf and run the changed file
