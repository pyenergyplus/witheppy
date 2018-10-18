# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""functions to work with extensiblefields"""


def extensiblefields2list(idfobject):
    """return the extensible field as a list"""
    pass
    
from witheppy.eppyhelpers import iddhelpers
def simplelist(idfobject):
    # iddhelpers.hasextensible(blist1(objidd))
    if iddhelpers.hasextensible(idfobject.objidd):
        start = iddhelpers.beginextensible_at(idfobject.objidd)
        return idfobject.fieldvalues[start:]
    else:
        return None


#
# from eppy.easyopen import easyopen
# fname = "/Applications/EnergyPlus-8-9-0/ExampleFiles/5ZoneDDCycOnOne.idf"
# idf = easyopen(fname)
# blists = idf.idfobjects("branchlist".upper())
# blists = idf.idfobjects["branchlist".upper()]
# len(blist)
# len(blists)
# blist[0]
# blists[0]
# blists[1]
# blist1 - blists[1]
# blist1 = blists[1]
# blist1
# from witheppy.eppyhelpers import iddhelpers
# iddhelpers.hasextensible(blist1(objidd))
# iddhelpers.hasextensible(blist1.objidd)
# iddhelpers.hasextensible(blist1.objidd)
# iddhelpers.beginextensible_at(blist1.objidd)
# blist1.fieldvalues
# blist1.fieldvalues[2:]
# blist1.fieldvalues[2-1:]
# hist
#
#
#



#
# from eppy.easyopen import easyopen
# fname = "/Applications/EnergyPlus-8-9-0/ExampleFiles/5ZoneDDCycOnOne.idf"
# idf = easyopen(fname)
# blists = idf.idfobjects("branchlist".upper())
# blists = idf.idfobjects["branchlist".upper()]
# len(blist)
# len(blists)
# blist[0]
# blists[0]
# blists[1]
# blist1 - blists[1]
# blist1 = blists[1]
# blist1
# from witheppy.eppyhelpers import iddhelpers
# iddhelpers.hasextensible(blist1(objidd))
# iddhelpers.hasextensible(blist1.objidd)
# iddhelpers.hasextensible(blist1.objidd)
# iddhelpers.beginextensible_at(blist1.objidd)
# blist1.fieldvalues
# blist1.fieldvalues[2:]
# blist1.fieldvalues[2-1:]
# hist
# %paste
# simplelist(blist1)
# %paste
# simplelist(blist1)
# %paste
# simplelist(blist1)
# blist1
# surfs = idf.idfobjects["BuildingSurface:Detailed".upper()]
# surfs[0]
# surf0 = surfs[0]
# surf0
# simplelist(surf0)
# %paste
# simplelist(surf0)
# surf0
# start = iddhelpers.beginextensible_at(surf0.objidd)
# strt
# start
# surf0.fieldnames[11]
# surf0.fieldnames
# blist1.fieldnames[1]
# blist1.fieldnames[:5]
# start = iddhelpers.beginextensible_at(blist1.objidd)
# start
# %paste
# simplelist(blist1)
# blist1
# simplelist(surf0)
# iddhelpers.hasextensible(surf0.objidd)
# hist
#
