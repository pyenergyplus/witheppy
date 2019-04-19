# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""helpers that enhance idf.run"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import eppy

def eplaunch_run(idf, weather=None):
    """run the way eplaunch would run one simulation"""
    fname = idf.idfname
    if not weather:
        wfile = idf.epw
    else:
        wfile = weather
    folder = os.path.dirname(fname)
    noext = os.path.splitext(os.path.basename(fname))[0]
    print("*" * 15, noext, "*" * 15)
    idf.run(expandobjects=True, output_directory=folder, output_prefix=noext, output_suffix="C")


# TODO : Use this function to build a bunch of things that are needed:
# - read idd from disk for testing
# - see how eppy does testing for run
# - then test this function and all the edge conditions for this function.

# --
# fname = "/Users/santosh/Documents/temp/eppyz-run/run2/1ZoneDataCenterCRAC_wPumpedDXCoolingCoil.idf"
# wfile = "/Users/santosh/Documents/temp/eppyz-run/USA_CO_Denver/USA_CO_Denver.Intl.AP.725650_TMY3.epw"
# idf = eppy.openidf(fname, epw=wfile)
# eplaunch_run(idf)
#
