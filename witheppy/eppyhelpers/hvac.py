# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""useful hvac funtions"""

import witheppy.eppyhelpers.extfields as extfields


def hasexhaust(idf, zone):
    """return exhaust node name or nodelist if the zone has an exhaust fan"""
    econnection = findequipmentconnection(idf, zone)
    node = econnection.Zone_Air_Exhaust_Node_or_NodeList_Name
    if node:
        return node
    else:
        return False


def findequipmentconnection(idf, zone):
    """find the equipment connections for this zone"""
    econs = [
        con
        for con in idf.idfobjects["ZoneHVAC:EquipmentConnections"]
        if con.Zone_Name == zone.Name
    ]
    if econs:
        return econs[0]
    else:
        return None


def findequipmentlist(idf, zone):
    """find the equipment list for this zone
    return equipmentlist and equipmentconnection"""
    econnection = findequipmentconnection(idf, zone)
    if econnection:
        elistname = econnection.Zone_Conditioning_Equipment_List_Name
        elists = idf.idfobjects["ZoneHVAC:EquipmentList"]
        elists = [elist for elist in elists if elist.Name == elistname]
        if elists:
            return elists[0], econnection
        else:
            return None
    else:
        return None


def findexhaust(idf, zone):
    """finds the exhaust fan if zone has one"""
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


def putexhaust(idf, zone, exhaust):
    """put an exhaust fan if there is None"""
    # - in exhaust fan, complete
    #     - Air inlet node name
    #     - air outlet node name -> throwaway name
    exhaust.Air_Inlet_Node_Name = f"{exhaust.Name} Node"
    exhaust.Air_Outlet_Node_Name = f"{exhaust.Name} Outlet Node"
    # - make nodelist
    #     - make nodelist name
    #     - put f"{exhaust.Name} Node" in it as single item.
    nodelist = idf.newidfobject(
        "NodeList",
        Name=f"{exhaust.Name} Node List",
        Node_1_Name=f"{exhaust.Name} Node",
    )
    # - in ZONEHVAC:EQUIPMENTCONNECTIONS
    #     - put the nodelist name in "Zone Air Exhaust Node or NodeList Name"
    #     - it may ableady be there. In which case use that name in above nodelist and track it back to exhaust fan.
    econns = findequipmentconnection(idf, zone)
    econns.Zone_Air_Exhaust_Node_or_NodeList_Name = f"{exhaust.Name} Node List"
    # - in ZONEHVAC:EQUIPMENTLIST
    #     - put in the exhaust fan with priority 2
    eqlist, _ = findequipmentlist(idf, zone)
    extlist = extfields.extensiblefields2list(eqlist)
    # next two lines can break if IDD changes
    cooling_sequence_max = max([item[2] for item in extlist])
    heating_sequence_max = max([item[3] for item in extlist])
    exfanitem = [
        "Fan:ZoneExhaust",
        exhaust.Name,
        cooling_sequence_max + 1,
        heating_sequence_max + 1,
    ]
    extlist.append(exfanitem)
    extfields.list2extensiblefields(eqlist, extlist)
    return idf


def removeexhaust(idf, zone):
    """remove the exhaust fan if it exists"""
    nodelistname = hasexhaust(idf, zone)
    nlist = idf.getobject("nodelist", nodelistname)
    exhfan = findexhaust(idf, zone)
    econn = findequipmentconnection(idf, zone)
    econn.Zone_Air_Exhaust_Node_or_NodeList_Name = ""
    idf.removeidfobject(exhfan)
    idf.removeidfobject(nlist)
    # need to remove the exfan from the equipment list
    eqlist, _ = findequipmentlist(idf, zone)
    extlist = extfields.extensiblefields2list(eqlist)
    new_list = [
        item for item in extlist if item[0].upper() != "Fan:ZoneExhaust".upper()
    ]
    extfields.list2extensiblefields(eqlist, new_list)
    return exhfan

# TODO : findequipmentlist should not return 2 values. It is confusing
# TODO : add docstrings in fucntions
    # - mention that it is based on ex fans in TermReheatZoneExh.idf
