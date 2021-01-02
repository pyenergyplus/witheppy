# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for iidhelpers"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from six import StringIO
# from six import string_types

from witheppy.eppyhelpers import iddhelpers


def test_hasextensible():
    """py.test for hasextensible"""
    tdata = (
        (
            [
                {
                    "extensible:2": [
                        '- repeat last two fields, remembering to remove ; from "inner" fields.'
                    ],  # noqa: E501
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                    "memo": [
                        "A Schedule:Day:Interval contains a full day of values with specified end times for each value",  # noqa: E501
                        "Currently, is set up to allow for 10 minute intervals for an entire day.",
                    ],  # noqa: E501
                    "min-fields": ["5"],
                },
                {
                    "field": ["Name"],
                    "reference": ["DayScheduleNames"],
                    "required-field": [""],
                    "type": ["alpha"],
                },
            ],
            2,
        ),  # iddobj, hasit
        (
            [
                {
                    "extensible:1": [""],
                    "group": "Simulation Parameters",
                    "idfobj": "ShadowCalculation",
                    "memo": [
                        "This object is used to control details of the solar, shading, and daylighting models"
                    ],  # noqa: E501
                    "unique-object": [""],
                },
                {
                    "default": ["AverageOverDaysInFrequency"],
                    "field": ["Calculation Method"],
                    "key": ["AverageOverDaysInFrequency", "TimestepFrequency"],
                    "note": [
                        "choose calculation method. note that TimestepFrequency is only needed for certain cases",  # noqa: E501
                        "and can increase execution time significantly.",
                    ],
                    "type": ["choice"],
                },
            ],
            1,
        ),  # iddobj, expected
        (
            [
                {
                    "group": "Simulation Parameters",
                    "idfobj": "Building",
                    "memo": [
                        "Describes parameters that are used during the simulation",
                        "of the building. There are necessary correlations between the entries for",  # noqa: E501
                        "this object and some entries in the Site:WeatherStation and",
                        "Site:HeightVariation objects, specifically the Terrain field.",
                    ],
                    "min-fields": ["8"],
                    "required-object": [""],
                    "unique-object": [""],
                },
                {"default": ["NONE"], "field": ["Name"], "retaincase": [""]},
            ],
            None,
        ),  # noqa: E501  # iddobj, expected
    )
    for iddobj, expected in tdata:
        result = iddhelpers.hasextensible(iddobj)
        assert result == expected


def test_beginextensible_at():
    """py.test for beginextensible_at"""
    tdata = (
        (
            [
                {
                    "extensible:2": [
                        '- repeat last two fields, remembering to remove ; from "inner" fields.'
                    ],  # noqa: E501
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                    "memo": [
                        "A Schedule:Day:Interval contains a full day of values with specified end times for each value",  # noqa: E501
                        "Currently, is set up to allow for 10 minute intervals for an entire day.",
                    ],  # noqa: E501
                    "min-fields": ["5"],
                },
                {
                    "field": ["Name"],
                    "reference": ["DayScheduleNames"],
                    "required-field": [""],
                    "type": ["alpha"],
                },
                {
                    "field": ["Schedule Type Limits Name"],
                    "object-list": ["ScheduleTypeLimitsNames"],
                    "type": ["object-list"],
                    "validobjects": {"SCHEDULETYPELIMITS"},
                },
                {
                    "default": ["No"],
                    "field": ["Interpolate to Timestep"],
                    "key": ["Average", "Linear", "No"],
                    "note": [
                        "when the interval does not match the user specified timestep a Average choice will average between the intervals request (to",  # noqa: E501
                        "timestep resolution. A No choice will use the interval value at the simulation timestep without regard to if it matches",  # noqa: E501
                        "the boundary or not. A Linear choice will interpolate linearly between successive values.",
                    ],  # noqa: E501
                    "type": ["choice"],
                },
                {
                    "begin-extensible": [""],
                    "field": ["Time 1"],
                    "note": ['"until" includes the time entered.'],
                    "units": ["hh:mm"],
                },
            ],
            4,
        ),  # objidd, expected
        (
            [
                {
                    "group": "Simulation Parameters",
                    "idfobj": "Building",
                    "memo": [
                        "Describes parameters that are used during the simulation",
                        "of the building. There are necessary correlations between the entries for",  # noqa: E501
                        "this object and some entries in the Site:WeatherStation and",
                        "Site:HeightVariation objects, specifically the Terrain field.",
                    ],
                    "min-fields": ["8"],
                    "required-object": [""],
                    "unique-object": [""],
                },
                {"default": ["NONE"], "field": ["Name"], "retaincase": [""]},
            ],
            None,
        ),  # noqa: E501 # objidd, expected
    )
    for objidd, expected in tdata:
        result = iddhelpers.beginextensible_at(objidd)
        assert result == expected
