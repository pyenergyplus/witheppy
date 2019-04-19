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


def eplaunch_run(idf, weather=None):
    """run the way eplaunch would run one simulation"""
    # TODO : function docs
    fname = idf.idfname
    if not weather:
        wfile = idf.epw
    else:
        wfile = weather
    folder = os.path.dirname(fname)
    noext = os.path.splitext(os.path.basename(fname))[0]
    idf.run(weather=wfile,
            expandobjects=True,
            output_directory=folder,
            output_prefix=noext,
            output_suffix="C")
