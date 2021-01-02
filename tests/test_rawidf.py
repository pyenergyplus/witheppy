# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for rawidf"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from witheppy.noteppy import rawidf
from six import StringIO


def test_readrawidf():
    """py.test for readrawidf"""
    # txt = """  version,9.0;
    # """
    txt = """  version,9.0;


    Timestep,4;

    ScheduleTypeLimits,
    Fraction,                !- Name
    0.0,                     !- Lower Limit Value
    1.0,                     !- Upper Limit Value
    CONTINUOUS;              !- Numeric Type

    ScheduleTypeLimits,
    Other,                !- Name
    0.0,                     !- Lower Limit Value
    1.0,                     !- Upper Limit Value
    CONTINUOUS;              !- Numeric Type
    """
    expected = {
        "version".upper(): [["version", "9.0"]],
        "Timestep".upper(): [["Timestep", "4"]],
        "ScheduleTypeLimits".upper(): [
            ["ScheduleTypeLimits", "Fraction", "0.0", "1.0", "CONTINUOUS"],
            ["ScheduleTypeLimits", "Other", "0.0", "1.0", "CONTINUOUS"],
        ],
    }
    result = rawidf.readrawidf(StringIO(txt))
    assert result == expected


def test_rawidf2str():
    """py.test rawidf2str"""
    rawdata = {"version".upper(): [["version", "9.0"]]}
    expected = """VERSION,
    9.0;
"""
    result = rawidf.rawidf2str(rawdata)
    assert result == expected
    rawdata = {
        "version".upper(): [["version", "9.0"]],
        "Timestep".upper(): [["Timestep", "4"]],
        "ScheduleTypeLimits".upper(): [
            ["ScheduleTypeLimits", "Fraction", "0.0", "1.0", "CONTINUOUS"],
            ["ScheduleTypeLimits", "Other", "0.0", "1.0", "CONTINUOUS"],
        ],
    }
    order = ["TIMESTEP", "VERSION", "SCHEDULETYPELIMITS", "badkey"]
    expected = """TIMESTEP,
    4;

VERSION,
    9.0;

SCHEDULETYPELIMITS,
     Fraction,
     0.0,
     1.0,
    CONTINUOUS;

SCHEDULETYPELIMITS,
     Other,
     0.0,
     1.0,
    CONTINUOUS;
"""
    result = rawidf.rawidf2str(rawdata, order)
    assert result == expected
