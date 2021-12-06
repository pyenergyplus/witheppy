# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""geometry things in for eppy"""
# note: not attempting to do python2 at all.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from itertools import combinations
from witheppy.eppyhelpers import extfields
from eppy.bunch_subclass import BadEPFieldError


def shiftwindows(awind, shift):
    """returns the window `awind` shifted by shift

    The values in shift (x, y, z) are subtracted from the coordinates
    of the corneres of the window


    Parameters
    ----------
    awind : eppy.bunch_subclass.EpBunch
         The window to be shifted (type FENESTRATIONSURFACE:DETAILED)
    shift: tuple, list
        tuple or list of 3 values for xshift, yshift, zshift

    Returns
    -------
    window: eppy.bunch_subclass.EpBunch
        The window (type FENESTRATIONSURFACE:DETAILED) shifted by xhift, xshift, zshift
    """
    shiftx, shifty, shiftz = shift
    for i in range(1, 4):
        awind[f"Vertex_{i}_Xcoordinate"] -= shiftx
        awind[f"Vertex_{i}_Ycoordinate"] -= shifty
        awind[f"Vertex_{i}_Zcoordinate"] -= shiftz
    if awind.Number_of_Vertices == 4:
        i = 4
        awind[f"Vertex_{i}_Xcoordinate"] -= shiftx
        awind[f"Vertex_{i}_Ycoordinate"] -= shifty
        awind[f"Vertex_{i}_Zcoordinate"] -= shiftz
    return awind


def shiftsurface(asurf, shift):
    """returns the surface `asurf` shifted by shift

    The values in shift (x, y, z) are subtracted from the coordinates
    of the corneres of the surface


    Parameters
    ----------
    asurf : eppy.bunch_subclass.EpBunch
         the surface that you want to shift (type BUILDINGSURFACE:DETAILED)
    shift: tuple, list
        tuple or list of 3 values for xshift, yshift, zshift

    Returns
    -------
    surface: eppy.bunch_subclass.EpBunch
        The surface shifted by xhift, xshift, zshift
    """
    # shift the surface
    shiftx, shifty, shiftz = shift
    coords = [[x, y, z] for x, y, z in extfields.extensiblefields2list(asurf)]
    ncoords = [[x - shiftx, y - shifty, z - shiftz] for x, y, z in coords]
    extfields.list2extensiblefields(asurf, ncoords)
    return asurf


def shiftsurfacewithwindows(idf, asurf, shift):
    """returns the surface and it's windows shifted by shift

    The values in shift (x, y, z) are subtracted from the coordinates
    of the corneres of the surface and from all the surfaces's
    windows

    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    asurf : eppy.bunch_subclass.EpBunch
        The surface that you want to shift (type BUILDINGSURFACE:DETAILED)
    shift: tuple, list
        tuple or list of 3 values for xshift, yshift, zshift

    Returns
    -------
    surface: eppy.bunch_subclass.EpBunch
        The surface shifted by xhift, yshift, zshift
    windowlist: list
        a list of shifted windows belonging to surface
    """
    surf = shiftsurface(asurf, shift)
    surfwinds = [
        wind
        for wind in idf.idfobjects["FenestrationSurface:Detailed"]
        if wind.Building_Surface_Name == surf.Name
    ]
    windows = [shiftwindows(wind, shift) for wind in surfwinds]
    return surf, windows


def commonsurfaces(idf, zone1, zone2):
    """return the interior surfaces that are common between the two zones


    - zone1
        - extwall1
        - intwall1z1->common->intwall3z2
        - intwall2
        - intwall3z1->common->intwall1z2
    - zone2
        - extwall1
        - intwall1z2->common->intwall3z1
        - intwall2
        - intwall3z2->common->intwall1z1
    - return ((intwall1z1, intwall3z2), (intwall3z1, intwall1z2))
    - limitation: common surfaces have to be of type BUILDINGSURFACE:DETAILED with Outside_Boundary_Condition == "Surface"


    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        this idf model
    zone1: eppy.bunch_subclass.EpBunch
         first zone (type ZONE)
    zone2: eppy.bunch_subclass.EpBunch
         second zone (type ZONE)

    Returns
    -------
    list
        [(wallinzone1, touchingwallinzone2), (wallinzone1, touchingwallinzone2)]
    """
    surfs = idf.idfobjects["BuildingSurface:Detailed"]
    intws = [
        surf
        for surf in surfs
        if surf.Outside_Boundary_Condition.upper() == "SURFACE"
        and surf.Outside_Boundary_Condition_Object.strip()
    ]
    zone1_intws = {
        (surf.Name, surf.Outside_Boundary_Condition_Object): surf
        for surf in intws
        if surf.Zone_Name == zone1.Name
    }
    zone2_intws = {  # flip the key
        (surf.Outside_Boundary_Condition_Object, surf.Name): surf
        for surf in intws
        if surf.Zone_Name == zone2.Name
    }
    return [
        (zone1_intws[key], zone2_intws[key])
        for key in zone1_intws
        if key in zone2_intws
    ]


def mergezones(idf, mergeznames):
    """merges the geometry of zones into the first zone in list mergeznames

    - mergeznames is a list of zone names [zname1, zname2, zname3, ...]
    - The zones named by mergeznames [zone1, zone2, zone3, ...] are merged so that there is only one zone -> zone1
    - zone2, zone3 and the rest are deleted
    - Any common surfaces between the zones are deleted, with the follwoing limitation:
        - common surfaces have to be of type BUILDINGSURFACE:DETAILED
        - with Outside_Boundary_Condition == "Surface"
    - all other surfaces are moved to aone1

    Parameters
    ----------
    idf: eppy.modeleditor.IDF
        the idf model
    mergeznames : list
        list of zone names [zname1, zname2, zname3, ...]

    Returns
    -------
    idf: eppy.modeleditor.IDF
        the idf is changed in place and returned
    """
    zones = idf.idfobjects["zone"]
    surfs = idf.idfobjects["BuildingSurface:Detailed"]

    mergezones = [idf.getobject("zone", zname) for zname in mergeznames]
    zonecoords = {
        zone.Name: (zone.X_Origin, zone.Y_Origin, zone.Z_Origin) for zone in mergezones
    }

    # remove zones that will be merged into the first zone
    for zone in mergezones[1:]:
        idf.removeidfobject(zone)

    # remove common interior surfaces
    combs = combinations(mergezones, 2)
    for z1, z2 in combs:
        thecommonsurfaces = commonsurfaces(idf, z1, z2)
        for s1, s2 in thecommonsurfaces:
            idf.removeidfobject(s1)
            idf.removeidfobject(s2)

    # shift the surfaces and windows in the trailing zones
    # to match the first zone origin
    for thiszonename in mergeznames[1:]:
        shiftx, shifty, shiftz = [
            c1 - c2
            for c1, c2 in zip(zonecoords[mergeznames[0]], zonecoords[thiszonename])
        ]
        thiszonesurfs = [surf for surf in surfs if surf.Zone_Name == thiszonename]
        for asurf in thiszonesurfs:
            # shift surface and windows
            shiftsurfacewithwindows(idf, asurf, (shiftx, shifty, shiftz))

    surfstomerge = [surf for surf in surfs if surf.Zone_Name in mergeznames[1:]]
    #  move  surfaces into first zone
    for surf in surfstomerge:
        surf.Zone_Name = mergeznames[0]

    # set first zone volume and area to autocalculate
    # empty field is autocalculate
    mergezones[0].Volume = ""
    mergezones[0].Floor_Area = ""
    return idf


def copyidfobject(idf, idfobject, **kwargs):
    """Add an IDF object to the IDF, with field modifiers

    opetional named arguments can change the fields of the copied item.
    An example of the this can look like this::

        copyidfobject(idf, zone, Name='A NewName')

    Parameters
    ----------
    idfobject : EpBunch object
        The IDF object to add. This usually comes from another idf file,
        or it can be used to copy within this idf file.

    Returns
    -------
    idfobject: EpBunch object
        This will be added object with any fields modified

    """
    for key in kwargs:
        try:
            _ = idfobject[key]
        except BadEPFieldError as e:
            raise BadEPFieldError(f"unknown filed name: {key}")
    newobject = idf.copyidfobject(idfobject)
    for key in kwargs:
        newobject[key] = kwargs[key]
    return newobject
