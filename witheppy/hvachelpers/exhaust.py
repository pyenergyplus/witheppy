# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""useful hvac funtions

Exhaust Fan code has been written based on 'TermReheatZoneExh.idf' from the ExampleFiles in E+ v9.6.0"""

import witheppy.eppyhelpers.extfields as extfields

class HasExhaustFanError(Exception):
    pass


def hasexhaust(idf, zone):
    """return False if the zone has no exhaust fan
    
    Returns field 'Zone Air Exhaust Node or NodeList Name' from ZONEHVAC:EQUIPMENTCONNECTIONS for this zone if it has an exhaust fan. If there is no Exhaust fan, it returns False

    Usage:: 
    
        if hasexhaust(idf, zone):
            dosomething()
        # OR
        if not hasexhaust(idf, zone):
            dosomethingelse()


    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone : eppy.bunch_subclass.EpBunch
        the zone you are checking for exhaust (type ZONE)

    Returns
    -------
    node: string, boolean:
        field 'Zone Air Exhaust Node or NodeList Name' from ZONEHVAC:EQUIPMENTCONNECTIONS for this zone if it has an exhaust fan. If there is no Exhaust fan, it returns False
    
    """
    
    econnection = findequipmentconnection(idf, zone)
    node = econnection.Zone_Air_Exhaust_Node_or_NodeList_Name
    if node:
        return node
    else:
        return False


def findequipmentconnection(idf, zone):
    """return ZONEHVAC:EQUIPMENTCONNECTIONS object for this zone
        
    Returns None if the zone does not have a ZONEHVAC:EQUIPMENTCONNECTIONS object

    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone : eppy.bunch_subclass.EpBunch
        the zone you are checking for exhaust (type ZONE)

    Returns
    -------
    equip_connections: eppy.bunch_subclass.EpBunch
        ZONEHVAC:EQUIPMENTCONNECTIONS object for this zone
    
    """
    econs = [
        con
        for con in idf.idfobjects["ZoneHVAC:EquipmentConnections"]
        if con.Zone_Name == zone.Name
    ]
    if econs:
        return econs[0]
    else:
        return None


def findequipmentlist(idf, zone, testing=False):
    """return ZONEHVAC:EQUIPMENTLIST object for this zone
        
    Returns None if the zone does not have a ZONEHVAC:EQUIPMENTLIST object

    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone : eppy.bunch_subclass.EpBunch
        the zone you are checking for exhaust (type ZONE)

    Returns
    -------
    equip_list: eppy.bunch_subclass.EpBunch
        ZONEHVAC:EQUIPMENTLIST object for this zone
    
    """
    econnection = findequipmentconnection(idf, zone)
    if econnection:
        elistname = econnection.Zone_Conditioning_Equipment_List_Name
        elists = idf.idfobjects["ZoneHVAC:EquipmentList"]
        elists = [elist for elist in elists if elist.Name == elistname]
        if elists:
            if testing:
                return elists[0], econnection
            else:
                return elists[0]
        else:
            return None
    else:
        return None


def findexhaust(idf, zone):
    """return FAN:ZONEEXHAUST object for this zone
        
    Returns None if the zone does not have a FAN:ZONEEXHAUST object

    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone : eppy.bunch_subclass.EpBunch
        the zone you are checking for exhaust (type ZONE)

    Returns
    -------
    exhaust_fan: eppy.bunch_subclass.EpBunch
        FAN:ZONEEXHAUST object for this zone
    """
    if hasexhaust(idf, zone):
        exh_nodelist_name = hasexhaust(idf, zone)  # will fail if it is just node
        nlist = idf.getobject("NodeList", exh_nodelist_name)
        nname = nlist.Node_1_Name  # things may break here. is it first node item ?
        exfans = idf.idfobjects["Fan:ZoneExhaust"]
        myfans = [fan for fan in exfans if fan.Air_Inlet_Node_Name == nname]
        myfan = myfans[0]
        return myfan
    else:
        return None


def putexhaust(idf, zone, exhaust_fan):
    """plug the exhaust_fan into the zone
    
    Will raise HasExhaustFanError exception, the zone has and exhaust fan
    
    Usage::
    
        greatexhaust = idf.newidfobject(FAN:ZONEEXHAUST, Name='Great Exhaust', ) # with other fields
        zones = idf.idfobjects['zone']
        zone = zones[2] # the 3rd zone
        putexhaust(idf, zone, greatexhaust)

    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone : eppy.bunch_subclass.EpBunch
        the zone you are checking for exhaust (type ZONE)
    exhaust_fan: eppy.bunch_subclass.EpBunch
        type FAN:ZONEEXHAUST. This should be made or copied to this idf

    Returns
    -------
    exhaust_fan: eppy.bunch_subclass.EpBunch
        FAN:ZONEEXHAUST object for this zone
    
    """
    if hasexhaust(idf, zone):
        raise HasExhaustFanError
        
    # - in exhaust fan, complete
    #     - Air inlet node name
    #     - air outlet node name -> throwaway name
    exhaust_fan.Air_Inlet_Node_Name = f"{exhaust_fan.Name} Node"
    exhaust_fan.Air_Outlet_Node_Name = f"{exhaust_fan.Name} Outlet Node"
    # - make nodelist
    #     - make nodelist name
    #     - put f"{exhaust_fan.Name} Node" in it as single item.
    nodelist = idf.newidfobject(
        "NodeList",
        Name=f"{exhaust_fan.Name} Node List",
        Node_1_Name=f"{exhaust_fan.Name} Node",
    )
    # - in ZONEHVAC:EQUIPMENTCONNECTIONS
    #     - put the nodelist name in "Zone Air Exhaust Node or NodeList Name"
    #     - it may ableady be there. In which case use that name in above nodelist and track it back to exhaust fan.
    econns = findequipmentconnection(idf, zone)
    econns.Zone_Air_Exhaust_Node_or_NodeList_Name = f"{exhaust_fan.Name} Node List"
    # - in ZONEHVAC:EQUIPMENTLIST
    #     - put in the exhaust fan with priority lowest
    eqlist = findequipmentlist(idf, zone)
    extlist = extfields.extensiblefields2list(eqlist)
    # next two lines can break if IDD changes
    cooling_sequence_max = max([item[2] for item in extlist])
    heating_sequence_max = max([item[3] for item in extlist])
    exfanitem = [
        "Fan:ZoneExhaust",
        exhaust_fan.Name,
        cooling_sequence_max + 1,
        heating_sequence_max + 1,
    ]
    extlist.append(exfanitem)
    extfields.list2extensiblefields(eqlist, extlist)
    return exhaust_fan


def removeexhaust(idf, zone):
    """remove the exhaust fan from zone if the zone has one
    
    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone : eppy.bunch_subclass.EpBunch
        the zone you are checking for exhaust (type ZONE)

    Returns
    -------
    exhaust_fan: eppy.bunch_subclass.EpBunch 
        FAN:ZONEEXHAUST object removed from this zone
    
    """
    if hasexhaust(idf, zone):
        nodelistname = hasexhaust(idf, zone)
        nlist = idf.getobject("nodelist", nodelistname)
        exhfan = findexhaust(idf, zone)
        econn = findequipmentconnection(idf, zone)
        econn.Zone_Air_Exhaust_Node_or_NodeList_Name = ""
        idf.removeidfobject(exhfan)
        idf.removeidfobject(nlist)
        # need to remove the exfan from the equipment list
        eqlist = findequipmentlist(idf, zone)
        extlist = extfields.extensiblefields2list(eqlist)
        new_list = [
            item for item in extlist if item[0].upper() != "Fan:ZoneExhaust".upper()
        ]
        extfields.list2extensiblefields(eqlist, new_list)
        return exhfan
    else:
        return None
        
# - Possible new functions
#     - disconnectfan
#     - removefan
#     - fanzonemap
        

# TODO putexhaust has a frigle point related to IDD. See:
    # next two lines can break if IDD changes (see in putexhaust())
    # find a way to harden this to IDD changes.

# DONE
# DONE : findequipmentlist should not return 2 values. It is confusing - DONE
# DONE : some functions have to be tested with hasexhaust() before running - DONE
# DONE : add docstrings in fucntions - DONE
