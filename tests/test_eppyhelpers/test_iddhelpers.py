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
    tdata = (([{u'extensible:2': [u'- repeat last two fields, remembering to remove ; from "inner" fields.'],  # noqa: E501
  u'group': u'Schedules',
  u'idfobj': u'Schedule:Day:Interval',
  u'memo': [u'A Schedule:Day:Interval contains a full day of values with specified end times for each value',  # noqa: E501
   u'Currently, is set up to allow for 10 minute intervals for an entire day.'],  # noqa: E501
  u'min-fields': [u'5']},
 {u'field': [u'Name'],
  u'reference': [u'DayScheduleNames'],
  u'required-field': [u''],
  u'type': [u'alpha']}], 2),  # iddobj, hasit
([{u'extensible:1': [u''],
  u'group': u'Simulation Parameters',
  u'idfobj': u'ShadowCalculation',
  u'memo': [u'This object is used to control details of the solar, shading, and daylighting models'],  # noqa: E501
  u'unique-object': [u'']},
 {u'default': [u'AverageOverDaysInFrequency'],
  u'field': [u'Calculation Method'],
  u'key': [u'AverageOverDaysInFrequency', u'TimestepFrequency'],
  u'note': [u'choose calculation method. note that TimestepFrequency is only needed for certain cases',  # noqa: E501
   u'and can increase execution time significantly.'],
  u'type': [u'choice']}], 1),  # iddobj, expected
([{u'group': u'Simulation Parameters',
  u'idfobj': u'Building',
  u'memo': [u'Describes parameters that are used during the simulation',
   u'of the building. There are necessary correlations between the entries for',  # noqa: E501
   u'this object and some entries in the Site:WeatherStation and',
   u'Site:HeightVariation objects, specifically the Terrain field.'],
  u'min-fields': [u'8'],
  u'required-object': [u''],
  u'unique-object': [u'']},
 {u'default': [u'NONE'], u'field': [u'Name'], u'retaincase': [u'']}], None),  # noqa: E501  # iddobj, expected
    )
    for iddobj, expected in tdata:
        result = iddhelpers.hasextensible(iddobj)
        assert result == expected


def test_beginextensible_at():
    """py.test for beginextensible_at"""
    tdata = (([{u'extensible:2': [u'- repeat last two fields, remembering to remove ; from "inner" fields.'],  # noqa: E501
    u'group': u'Schedules',
  u'idfobj': u'Schedule:Day:Interval',
  u'memo': [u'A Schedule:Day:Interval contains a full day of values with specified end times for each value',  # noqa: E501
   u'Currently, is set up to allow for 10 minute intervals for an entire day.'],  # noqa: E501
  u'min-fields': [u'5']},
 {u'field': [u'Name'],
  u'reference': [u'DayScheduleNames'],
  u'required-field': [u''],
  u'type': [u'alpha']},
 {u'field': [u'Schedule Type Limits Name'],
  u'object-list': [u'ScheduleTypeLimitsNames'],
  u'type': [u'object-list'],
  u'validobjects': {u'SCHEDULETYPELIMITS'}},
 {u'default': [u'No'],
  u'field': [u'Interpolate to Timestep'],
  u'key': [u'Average', u'Linear', u'No'],
  u'note': [u'when the interval does not match the user specified timestep a Average choice will average between the intervals request (to',  # noqa: E501
   u'timestep resolution. A No choice will use the interval value at the simulation timestep without regard to if it matches',  # noqa: E501
   u'the boundary or not. A Linear choice will interpolate linearly between successive values.'],  # noqa: E501
  u'type': [u'choice']},
 {u'begin-extensible': [u''],
  u'field': [u'Time 1'],
  u'note': [u'"until" includes the time entered.'],
  u'units': [u'hh:mm']}], 4),  # objidd, expected
([{u'group': u'Simulation Parameters',
  u'idfobj': u'Building',
  u'memo': [u'Describes parameters that are used during the simulation',
   u'of the building. There are necessary correlations between the entries for',  # noqa: E501
   u'this object and some entries in the Site:WeatherStation and',
   u'Site:HeightVariation objects, specifically the Terrain field.'],
  u'min-fields': [u'8'],
  u'required-object': [u''],
  u'unique-object': [u'']},
 {u'default': [u'NONE'], u'field': [u'Name'], u'retaincase': [u'']}], None),  # noqa: E501 # objidd, expected
    )
    for objidd, expected in tdata:
        result = iddhelpers.beginextensible_at(objidd)
        assert result == expected
