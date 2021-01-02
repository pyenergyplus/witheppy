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


def eplaunch_run(idf):
    """Run the E+ simulation exactly as EPLaunch would run a single file
    with it's default setting

    EPLaunch does the following by default:

        - expands the Template objects
        - puts the out output files in the same folder as the idf
        - Uses idf filename as the output prefix
        - Uses Capitals for the output suffix

    Parameters
    ----------
    idf : modelbuilder.IDF
        the idf file. The idf file needs a weather file when opened
    Returns
    -------
    NoneType
    """
    fname = idf.idfname
    weather = None  # add weather args after bugfix for issue #236
    if not weather:
        wfile = idf.epw
    else:
        wfile = weather
    folder = os.path.dirname(fname)
    noext = os.path.splitext(os.path.basename(fname))[0]
    idf.run(
        weather=wfile,
        expandobjects=True,
        output_directory=folder,
        output_prefix=noext,
        output_suffix="C",
    )
