# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for hvac.py"""

import pytest
from io import StringIO
from witheppy.eppyhelpers import hvac
import witheppy.eppyhelpers.extfields as extfields

idftxt = """!- Darwin Line endings 
Version,
9.6;
SimulationControl,
No,
No,
No,
Yes,
No,
No,
1;
Building,
NONE,
0.0,
Suburbs,
0.039999999,
0.4,
FullInteriorAndExterior,
25,
6;
SurfaceConvectionAlgorithm:Inside,
TARP;
SurfaceConvectionAlgorithm:Outside,
DOE-2;
HeatBalanceAlgorithm,
ConductionTransferFunction;
Timestep,
6;
Site:Location,
CHICAGO_IL_USA TMY2-94846,
41.78,
-87.75,
-6.0,
190.0;
SizingPeriod:DesignDay,
CHICAGO_IL_USA Annual Heating 99% Design Conditions DB,
1,
21,
WinterDesignDay,
-17.3,
0.0,
,
,
Wetbulb,
-17.3,
,
,
,
,
99063.0,
4.9,
270.0,
No,
No,
No,
ASHRAEClearSky,
,
,
,
,
0.0;
SizingPeriod:DesignDay,
CHICAGO_IL_USA Annual Cooling 1% Design Conditions DB/MCWB,
7,
21,
SummerDesignDay,
31.5,
10.7,
,
,
Wetbulb,
23.0,
,
,
,
,
99063.0,
5.3,
230.0,
No,
No,
No,
ASHRAEClearSky,
,
,
,
,
1.0;
Site:GroundTemperature:BuildingSurface,
20.03,
20.03,
20.13,
20.3,
20.43,
20.52,
20.62,
20.77,
20.78,
20.55,
20.44,
20.2;
ScheduleTypeLimits,
Any Number;
ScheduleTypeLimits,
Fraction,
0.0,
1.0,
CONTINUOUS;
ScheduleTypeLimits,
Temperature,
-60.0,
200.0,
CONTINUOUS,
Temperature;
ScheduleTypeLimits,
Control Type,
0.0,
4.0,
DISCRETE;
ScheduleTypeLimits,
On/Off,
0.0,
1.0,
DISCRETE;
Schedule:Compact,
Activity Sch,
Any Number,
Through: 12/31,
For: Alldays,
Until: 24:00,
131.80;
Schedule:Compact,
Work Eff Sch,
Any Number,
Through: 12/31,
For: Alldays,
Until: 24:00,
0.00;
Schedule:Compact,
Clothing Sch,
Any Number,
Through: 12/31,
For: Alldays,
Until: 24:00,
1.00;
Schedule:Compact,
Air Velo Sch,
Any Number,
Through: 12/31,
For: Alldays,
Until: 24:00,
0.137;
Schedule:Compact,
Office Occupancy,
Any Number,
Through: 12/31,
For: Weekdays,
Until: 6:00,
0.00,
Until: 7:00,
0.10,
Until: 8:00,
0.50,
Until: 12:00,
1.00,
Until: 13:00,
0.50,
Until: 16:00,
1.00,
Until: 17:00,
0.50,
Until: 18:00,
0.10,
Until: 24:00,
0.00,
For: Sunday Holidays Saturday,
Until: 24:00,
0.00,
For: SummerDesignDay WinterDesignDay,
Until: 6:00,
0.00,
Until: 7:00,
0.10,
Until: 8:00,
0.50,
Until: 12:00,
1.00,
Until: 13:00,
0.50,
Until: 16:00,
1.00,
Until: 17:00,
0.50,
Until: 18:00,
0.10,
Until: 24:00,
0.00,
For: CustomDay1 CustomDay2,
Until: 24:00,
0.00;
Schedule:Compact,
Intermittent,
Any Number,
Through: 12/31,
For: Weekdays,
Until: 8:00,
0.00,
Until: 18:00,
1.00,
Until: 24:00,
0.00,
For: Weekends Holidays,
Until: 24:00,
0.00,
For: SummerDesignDay WinterDesignDay,
Until: 8:00,
0.00,
Until: 18:00,
1.00,
Until: 24:00,
0.00,
For: CustomDay1 CustomDay2,
Until: 24:00,
0.00;
Schedule:Compact,
Office Lighting,
Any Number,
Through: 12/31,
For: Weekdaysy,
Until: 6:00,
5.00E-002,
Until: 7:00,
0.20,
Until: 17:00,
1.00,
Until: 18:00,
0.50,
Until: 24:00,
5.00E-002,
For: Weekends Holidays,
Until: 24:00,
5.00E-002,
For: SummerDesignDay WinterDesignDay,
Until: 6:00,
5.00E-002,
Until: 7:00,
0.20,
Until: 17:00,
1.00,
Until: 18:00,
0.50,
Until: 24:00,
5.00E-002,
For: CustomDay1 CustomDay2,
Until: 24:00,
5.00E-002;
Schedule:Compact,
On Peak,
Fraction,
Through: 12/31,
For: Alldays,
Until: 9:00,
0.00,
Until: 18:00,
1.00,
Until: 24:00,
0.00;
Schedule:Compact,
Off Peak,
Fraction,
Through: 12/31,
For: Alldays,
Until: 9:00,
1.00,
Until: 18:00,
0.00,
Until: 24:00,
1.00;
Schedule:Compact,
ON,
Fraction,
Through: 12/31,
For: Alldays,
Until: 24:00,
1.00;
Schedule:Compact,
SEASONAL RESET SUPPLY AIR TEMP SCH,
TEMPERATURE,
Through: 3/31,
For: Alldays,
Until: 24:00,
16.00,
Through: 9/30,
For: Alldays,
Until: 24:00,
13.00,
Through: 12/31,
For: Alldays,
Until: 24:00,
16.00;
Schedule:Compact,
SEASONAL RESET MIXED AIR TEMP SCH,
TEMPERATURE,
Through: 3/31,
For: Alldays,
Until: 24:00,
14.00,
Through: 9/30,
For: Alldays,
Until: 24:00,
11.00,
Through: 12/31,
For: Alldays,
Until: 24:00,
14.00;
Schedule:Compact,
CW LOOP TEMP SCHEDULE,
TEMPERATURE,
Through: 12/31,
For: Alldays,
Until: 24:00,
6.67;
Schedule:Compact,
HW LOOP TEMP SCHEDULE,
TEMPERATURE,
Through: 12/31,
For: Alldays,
Until: 24:00,
60.00;
Schedule:Compact,
FANANDCOILAVAILSCHED,
FRACTION,
Through: 3/31,
For: Alldays,
Until: 24:00,
1.00,
Through: 9/30,
For: Weekdays SummerDesignDay WinterDesignDay,
Until: 7:00,
0.00,
Until: 17:00,
1.00,
Until: 24:00,
0.00,
For: Weekends Holidays CustomDay1 CustomDay2,
Until: 24:00,
0.00,
Through: 12/31,
For: Alldays,
Until: 24:00,
1.00;
Schedule:Compact,
COOLINGCOILAVAILSCHED,
FRACTION,
Through: 3/31,
For: Alldays,
Until: 24:00,
0.00,
Through: 9/30,
For: Weekdays SummerDesignDay WinterDesignDay,
Until: 7:00,
0.00,
Until: 17:00,
1.00,
Until: 24:00,
0.00,
For: Weekends Holidays CustomDay1 CustomDay2,
Until: 24:00,
0.00,
Through: 12/31,
For: Alldays,
Until: 24:00,
0.00;
Schedule:Compact,
HEATING SETPOINTS,
TEMPERATURE,
Through: 12/31,
For: Alldays,
Until: 7:00,
15.00,
Until: 17:00,
20.00,
Until: 24:00,
15.00;
Schedule:Compact,
COOLING SETPOINTS,
TEMPERATURE,
Through: 12/31,
For: Alldays,
Until: 7:00,
30.00,
Until: 17:00,
24.00,
Until: 24:00,
30.00;
Schedule:Compact,
ZONE CONTROL TYPE SCHED,
CONTROL TYPE,
Through: 3/31,
For: Alldays,
Until: 24:00,
1,
Through: 9/30,
For: Alldays,
Until: 24:00,
2,
Through: 12/31,
For: Alldays,
Until: 24:00,
1;
Material,
A1 - 1 IN STUCCO,
Smooth,
0.025389841,
0.6918309,
1858.142,
836.8,
0.9,
0.92,
0.92;
Material,
C4 - 4 IN COMMON BRICK,
Rough,
0.1014984,
0.7264224,
1922.216,
836.8,
0.9,
0.76,
0.76;
Material,
E1 - 3 / 4 IN PLASTER OR GYP BOARD,
Smooth,
0.01905,
0.7264224,
1601.846,
836.8,
0.9,
0.92,
0.92;
Material,
C6 - 8 IN CLAY TILE,
Smooth,
0.2033016,
0.5707605,
1121.292,
836.8,
0.9,
0.82,
0.82;
Material,
C10 - 8 IN HW CONCRETE,
MediumRough,
0.2033016,
1.729577,
2242.585,
836.8,
0.9,
0.65,
0.65;
Material,
E2 - 1 / 2 IN SLAG OR STONE,
Rough,
0.012710161,
1.435549,
881.0155,
1673.6,
0.9,
0.55,
0.55;
Material,
E3 - 3 / 8 IN FELT AND MEMBRANE,
Rough,
0.0095402403,
0.1902535,
1121.292,
1673.6,
0.9,
0.75,
0.75;
Material,
B5 - 1 IN DENSE INSULATION,
VeryRough,
0.025389841,
0.04323943,
91.30524,
836.8,
0.9,
0.5,
0.5;
Material,
C12 - 2 IN HW CONCRETE,
MediumRough,
0.050901599,
1.729577,
2242.585,
836.8,
0.9,
0.65,
0.65;
WindowMaterial:Glazing,
WIN-LAY-GLASS-LIGHT,
SpectralAverage,
,
0.003,
0.9,
0.031,
0.031,
0.9,
0.05,
0.05,
0.0,
0.84,
0.84,
0.9;
Construction,
EXTWALL80,
A1 - 1 IN STUCCO,
C4 - 4 IN COMMON BRICK,
E1 - 3 / 4 IN PLASTER OR GYP BOARD;
Construction,
PARTITION06,
E1 - 3 / 4 IN PLASTER OR GYP BOARD,
C6 - 8 IN CLAY TILE,
E1 - 3 / 4 IN PLASTER OR GYP BOARD;
Construction,
FLOOR SLAB 8 IN,
C10 - 8 IN HW CONCRETE;
Construction,
ROOF34,
E2 - 1 / 2 IN SLAG OR STONE,
E3 - 3 / 8 IN FELT AND MEMBRANE,
B5 - 1 IN DENSE INSULATION,
C12 - 2 IN HW CONCRETE;
Construction,
WIN-CON-LIGHT,
WIN-LAY-GLASS-LIGHT;
GlobalGeometryRules,
UpperLeftCorner,
CounterClockWise,
World;
Zone,
West Zone,
0.0,
0.0,
0.0,
0.0,
1,
1,
autocalculate,
autocalculate;
Zone,
EAST ZONE,
0.0,
0.0,
0.0,
0.0,
1,
1,
autocalculate,
autocalculate;
Zone,
NORTH ZONE,
0.0,
0.0,
0.0,
0.0,
1,
1,
autocalculate,
autocalculate;
BuildingSurface:Detailed,
Zn001:Wall001,
Wall,
EXTWALL80,
West Zone,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
0.0,
0.0,
3.048,
0.0,
0.0,
0.0,
6.096,
0.0,
0.0,
6.096,
0.0,
3.048;
BuildingSurface:Detailed,
Zn001:Wall002,
Wall,
EXTWALL80,
West Zone,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
0.0,
6.096,
3.048,
0.0,
6.096,
0.0,
0.0,
0.0,
0.0,
0.0,
0.0,
3.048;
BuildingSurface:Detailed,
Zn001:Wall003,
Wall,
PARTITION06,
West Zone,
,
Surface,
Zn003:Wall004,
NoSun,
NoWind,
0.5,
4.0,
6.096,
6.096,
3.048,
6.096,
6.096,
0.0,
0.0,
6.096,
0.0,
0.0,
6.096,
3.048;
BuildingSurface:Detailed,
Zn001:Wall004,
Wall,
PARTITION06,
West Zone,
,
Surface,
Zn002:Wall004,
NoSun,
NoWind,
0.5,
4.0,
6.096,
0.0,
3.048,
6.096,
0.0,
0.0,
6.096,
6.096,
0.0,
6.096,
6.096,
3.048;
BuildingSurface:Detailed,
Zn001:Flr001,
Floor,
FLOOR SLAB 8 IN,
West Zone,
,
Surface,
Zn001:Flr001,
NoSun,
NoWind,
1.0,
4.0,
0.0,
0.0,
0.0,
0.0,
6.096,
0.0,
6.096,
6.096,
0.0,
6.096,
0.0,
0.0;
BuildingSurface:Detailed,
Zn001:Roof001,
Roof,
ROOF34,
West Zone,
,
Outdoors,
,
SunExposed,
WindExposed,
0.0,
4.0,
0.0,
6.096,
3.048,
0.0,
0.0,
3.048,
6.096,
0.0,
3.048,
6.096,
6.096,
3.048;
BuildingSurface:Detailed,
Zn002:Wall001,
Wall,
EXTWALL80,
EAST ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
12.192,
6.096,
3.048,
12.192,
6.096,
0.0,
9.144,
6.096,
0.0,
9.144,
6.096,
3.048;
BuildingSurface:Detailed,
Zn002:Wall002,
Wall,
EXTWALL80,
EAST ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
6.096,
0.0,
3.048,
6.096,
0.0,
0.0,
12.192,
0.0,
0.0,
12.192,
0.0,
3.048;
BuildingSurface:Detailed,
Zn002:Wall003,
Wall,
EXTWALL80,
EAST ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
12.192,
0.0,
3.048,
12.192,
0.0,
0.0,
12.192,
6.096,
0.0,
12.192,
6.096,
3.048;
BuildingSurface:Detailed,
Zn002:Wall004,
Wall,
PARTITION06,
EAST ZONE,
,
Surface,
Zn001:Wall004,
NoSun,
NoWind,
0.5,
4.0,
6.096,
6.096,
3.048,
6.096,
6.096,
0.0,
6.096,
0.0,
0.0,
6.096,
0.0,
3.048;
BuildingSurface:Detailed,
Zn002:Wall005,
Wall,
PARTITION06,
EAST ZONE,
,
Surface,
Zn003:Wall005,
NoSun,
NoWind,
0.5,
4.0,
9.144,
6.096,
3.048,
9.144,
6.096,
0.0,
6.096,
6.096,
0.0,
6.096,
6.096,
3.048;
BuildingSurface:Detailed,
Zn002:Flr001,
Floor,
FLOOR SLAB 8 IN,
EAST ZONE,
,
Surface,
Zn002:Flr001,
NoSun,
NoWind,
1.0,
4.0,
6.096,
0.0,
0.0,
6.096,
6.096,
0.0,
12.192,
6.096,
0.0,
12.192,
0.0,
0.0;
BuildingSurface:Detailed,
Zn002:Roof001,
Roof,
ROOF34,
EAST ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.0,
4.0,
6.096,
6.096,
3.048,
6.096,
0.0,
3.048,
12.192,
0.0,
3.048,
12.192,
6.096,
3.048;
BuildingSurface:Detailed,
Zn003:Wall001,
Wall,
EXTWALL80,
NORTH ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
0.0,
12.192,
3.048,
0.0,
12.192,
0.0,
0.0,
6.096,
0.0,
0.0,
6.096,
3.048;
BuildingSurface:Detailed,
Zn003:Wall002,
Wall,
EXTWALL80,
NORTH ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
9.144,
12.192,
3.048,
9.144,
12.192,
0.0,
0.0,
12.192,
0.0,
0.0,
12.192,
3.048;
BuildingSurface:Detailed,
Zn003:Wall003,
Wall,
EXTWALL80,
NORTH ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.5,
4.0,
9.144,
6.096,
3.048,
9.144,
6.096,
0.0,
9.144,
12.192,
0.0,
9.144,
12.192,
3.048;
BuildingSurface:Detailed,
Zn003:Wall004,
Wall,
PARTITION06,
NORTH ZONE,
,
Surface,
Zn001:Wall003,
NoSun,
NoWind,
0.5,
4.0,
0.0,
6.096,
3.048,
0.0,
6.096,
0.0,
6.096,
6.096,
0.0,
6.096,
6.096,
3.048;
BuildingSurface:Detailed,
Zn003:Wall005,
Wall,
PARTITION06,
NORTH ZONE,
,
Surface,
Zn002:Wall005,
NoSun,
NoWind,
0.5,
4.0,
6.096,
6.096,
3.048,
6.096,
6.096,
0.0,
9.144,
6.096,
0.0,
9.144,
6.096,
3.048;
BuildingSurface:Detailed,
Zn003:Flr001,
Floor,
FLOOR SLAB 8 IN,
NORTH ZONE,
,
Surface,
Zn003:Flr001,
NoSun,
NoWind,
1.0,
4.0,
0.0,
6.096,
0.0,
0.0,
12.192,
0.0,
9.144,
12.192,
0.0,
9.144,
6.096,
0.0;
BuildingSurface:Detailed,
Zn003:Roof001,
Roof,
ROOF34,
NORTH ZONE,
,
Outdoors,
,
SunExposed,
WindExposed,
0.0,
4.0,
0.0,
12.192,
3.048,
0.0,
6.096,
3.048,
9.144,
6.096,
3.048,
9.144,
12.192,
3.048;
FenestrationSurface:Detailed,
Zn001:Wall001:Win001,
Window,
WIN-CON-LIGHT,
Zn001:Wall001,
,
0.5,
,
1.0,
4.0,
0.548,
0.0,
2.5,
0.548,
0.0,
0.5,
5.548,
0.0,
0.5,
5.548,
0.0,
2.5;
People,
West Zone,
West Zone,
Office Occupancy,
people,
3.0,
,
,
0.3,
,
Activity Sch,
3.82e-08,
,
zoneaveraged,
,
Work Eff Sch,
ClothingInsulationSchedule,
,
Clothing Sch,
Air Velo Sch,
FANGER;
People,
EAST ZONE,
EAST ZONE,
Office Occupancy,
people,
3.0,
,
,
0.3,
,
Activity Sch,
3.82e-08,
,
zoneaveraged,
,
Work Eff Sch,
ClothingInsulationSchedule,
,
Clothing Sch,
Air Velo Sch,
FANGER;
People,
NORTH ZONE,
NORTH ZONE,
Office Occupancy,
people,
4.0,
,
,
0.3,
,
Activity Sch,
3.82e-08,
,
zoneaveraged,
,
Work Eff Sch,
ClothingInsulationSchedule,
,
Clothing Sch,
Air Velo Sch,
FANGER;
Lights,
EAST ZONE Lights 1,
EAST ZONE,
Office Lighting,
LightingLevel,
1464.375,
,
,
0.0,
0.2,
0.2,
0.0,
GeneralLights;
Lights,
NORTH ZONE Lights 1,
NORTH ZONE,
Office Lighting,
LightingLevel,
878.6252,
,
,
0.0,
0.2,
0.2,
0.0,
GeneralLights;
ElectricEquipment,
West Zone ElecEq 1,
West Zone,
Intermittent,
EquipmentLevel,
2928.751,
,
,
0.0,
0.3,
0.0;
ElectricEquipment,
EAST ZONE ElecEq 1,
EAST ZONE,
Intermittent,
EquipmentLevel,
1464.375,
,
,
0.0,
0.3,
0.0;
ElectricEquipment,
NORTH ZONE ElecEq 1,
NORTH ZONE,
Intermittent,
EquipmentLevel,
2928.751,
,
,
0.0,
0.3,
0.0;
ZoneControl:Thermostat,
Zone 1 Thermostat,
West Zone,
Zone Control Type Sched,
ThermostatSetpoint:SingleHeating,
Heating Setpoint with SB,
ThermostatSetpoint:SingleCooling,
Cooling Setpoint with SB;
ZoneControl:Thermostat,
Zone 2 Thermostat,
EAST ZONE,
Zone Control Type Sched,
ThermostatSetpoint:SingleHeating,
Heating Setpoint with SB,
ThermostatSetpoint:SingleCooling,
Cooling Setpoint with SB;
ZoneControl:Thermostat,
Zone 3 Thermostat,
NORTH ZONE,
Zone Control Type Sched,
ThermostatSetpoint:SingleHeating,
Heating Setpoint with SB,
ThermostatSetpoint:SingleCooling,
Cooling Setpoint with SB;
ThermostatSetpoint:SingleHeating,
Heating Setpoint with SB,
Heating Setpoints;
ThermostatSetpoint:SingleCooling,
Cooling Setpoint with SB,
Cooling Setpoints;
AirTerminal:SingleDuct:ConstantVolume:Reheat,
Reheat Zone 1,
FanAndCoilAvailSched,
Zone 1 Reheat Air Outlet Node,
Zone 1 Reheat Air Inlet Node,
0.47,
Coil:Heating:Water,
Reheat Coil Zone 1,
0.0013,
0.0,
0.001;
AirTerminal:SingleDuct:ConstantVolume:Reheat,
Reheat Zone 2,
FanAndCoilAvailSched,
Zone 2 Reheat Air Outlet Node,
Zone 2 Reheat Air Inlet Node,
0.36,
Coil:Heating:Water,
Reheat Coil Zone 2,
0.0012,
0.0,
0.001;
AirTerminal:SingleDuct:ConstantVolume:Reheat,
Reheat Zone 3,
FanAndCoilAvailSched,
Zone 3 Reheat Air Outlet Node,
Zone 3 Reheat Air Inlet Node,
0.47,
Coil:Heating:Water,
Reheat Coil Zone 3,
0.0013,
0.0,
0.001;
ZoneHVAC:AirDistributionUnit,
Zone1TermReheat,
Zone 1 Reheat Air Outlet Node,
AirTerminal:SingleDuct:ConstantVolume:Reheat,
Reheat Zone 1;
ZoneHVAC:AirDistributionUnit,
Zone2TermReheat,
Zone 2 Reheat Air Outlet Node,
AirTerminal:SingleDuct:ConstantVolume:Reheat,
Reheat Zone 2;
ZoneHVAC:AirDistributionUnit,
Zone3TermReheat,
Zone 3 Reheat Air Outlet Node,
AirTerminal:SingleDuct:ConstantVolume:Reheat,
Reheat Zone 3;
ZoneHVAC:EquipmentList,
Zone1Equipment,
SequentialLoad,
ZoneHVAC:AirDistributionUnit,
Zone1TermReheat,
1,
1,
,
;
ZoneHVAC:EquipmentList,
Zone2Equipment,
SequentialLoad,
Fan:ZoneExhaust,
Zone 2 Exhaust Fan,
2,
2,
,
,
ZoneHVAC:AirDistributionUnit,
Zone2TermReheat,
1,
1,
,
;
ZoneHVAC:EquipmentList,
Zone3Equipment,
SequentialLoad,
Fan:ZoneExhaust,
Zone 3 Exhaust Fan,
2,
2,
,
,
ZoneHVAC:AirDistributionUnit,
Zone3TermReheat,
1,
1,
,
;
ZoneHVAC:EquipmentConnections,
West Zone,
Zone1Equipment,
Zone1Inlets,
,
Zone 1 Node,
Zone 1 Outlet Node;
ZoneHVAC:EquipmentConnections,
EAST ZONE,
Zone2Equipment,
Zone2Inlets,
Zone 2 Exhausts,
Zone 2 Node,
Zone 2 Outlet Node;
ZoneHVAC:EquipmentConnections,
NORTH ZONE,
Zone3Equipment,
Zone3Inlets,
Zone 3 Exhausts,
Zone 3 Node,
Zone 3 Outlet Node;
Fan:ConstantVolume,
Supply Fan 1,
FanAndCoilAvailSched,
0.7,
600.0,
1.3,
0.9,
1.0,
Mixed Air Node,
Cooling Coil Air Inlet Node;
Fan:ZoneExhaust,
Zone 2 Exhaust Fan,
FanAndCoilAvailSched,
0.6,
125.0,
0.1,
Zone 2 Exhaust Node,
Zone 2 Exhaust Fan Outlet Node;
Fan:ZoneExhaust,
Zone 3 Exhaust Fan,
FanAndCoilAvailSched,
0.6,
125.0,
0.15,
Zone 3 Exhaust Node,
Zone 3 Exhaust Fan Outlet Node;
Coil:Cooling:Water:DetailedGeometry,
Detailed Cooling Coil,
CoolingCoilAvailSched,
0.0011,
6.23816,
6.20007018,
101.7158224,
0.810606367,
0.165097968,
0.43507152,
0.001499982,
0.014449958,
0.015879775,
385.764854,
203.882537,
0.001814292,
0.02589977,
6.0,
16.0,
Cooling Coil Water Inlet Node,
Cooling Coil Water Outlet Node,
Cooling Coil Air Inlet Node,
Air Loop Outlet Node;
Coil:Heating:Water,
Reheat Coil Zone 1,
FanAndCoilAvailSched,
400.0,
0.0013,
Zone 1 Reheat Water Inlet Node,
Zone 1 Reheat Water Outlet Node,
Zone 1 Reheat Air Inlet Node,
Zone 1 Reheat Air Outlet Node,
UFactorTimesAreaAndDesignWaterFlowRate,
autosize,
82.2,
16.6,
71.1,
32.2,
;
Coil:Heating:Water,
Reheat Coil Zone 2,
FanAndCoilAvailSched,
400.0,
0.0012,
Zone 2 Reheat Water Inlet Node,
Zone 2 Reheat Water Outlet Node,
Zone 2 Reheat Air Inlet Node,
Zone 2 Reheat Air Outlet Node,
UFactorTimesAreaAndDesignWaterFlowRate,
autosize,
82.2,
16.6,
71.1,
32.2,
;
Coil:Heating:Water,
Reheat Coil Zone 3,
FanAndCoilAvailSched,
400.0,
0.0018,
Zone 3 Reheat Water Inlet Node,
Zone 3 Reheat Water Outlet Node,
Zone 3 Reheat Air Inlet Node,
Zone 3 Reheat Air Outlet Node,
UFactorTimesAreaAndDesignWaterFlowRate,
autosize,
82.2,
16.6,
71.1,
32.2,
;
Controller:WaterCoil,
Main Cooling Coil Controller,
Temperature,
Reverse,
FLOW,
Air Loop Outlet Node,
Cooling Coil Water Inlet Node,
0.1,
0.0011,
0.0;
Controller:OutdoorAir,
OA Controller 1,
Relief Air Outlet Node,
Air Loop Inlet Node,
Mixed Air Node,
Outside Air Inlet Node,
0.4333,
1.3,
FixedDryBulb,
ModulateFlow,
19.0,
,
,
,
4.0,
NoLockout,
FixedMinimum;
AirLoopHVAC:ControllerList,
Reheat System 1 Controllers,
Controller:WaterCoil,
Main Cooling Coil Controller;
AirLoopHVAC:ControllerList,
OA Sys 1 Controllers,
Controller:OutdoorAir,
OA Controller 1;
AirLoopHVAC,
Typical Terminal Reheat 1,
Reheat System 1 Controllers,
Reheat System 1 Avail List,
1.3,
Air Loop Branches,
,
Air Loop Inlet Node,
Return Air Mixer Outlet,
Zone Equipment Inlet Node,
Air Loop Outlet Node;
AirLoopHVAC:OutdoorAirSystem:EquipmentList,
OA Sys 1 Equipment,
OutdoorAir:Mixer,
OA Mixing Box 1;
AirLoopHVAC:OutdoorAirSystem,
OA Sys 1,
OA Sys 1 Controllers,
OA Sys 1 Equipment;
OutdoorAir:Mixer,
OA Mixing Box 1,
Mixed Air Node,
Outside Air Inlet Node,
Relief Air Outlet Node,
Air Loop Inlet Node;
AirLoopHVAC:ZoneSplitter,
Zone Supply Air Splitter,
Zone Equipment Inlet Node,
Zone 1 Reheat Air Inlet Node,
Zone 2 Reheat Air Inlet Node,
Zone 3 Reheat Air Inlet Node;
AirLoopHVAC:SupplyPath,
TermReheatSupplyPath,
Zone Equipment Inlet Node,
AirLoopHVAC:ZoneSplitter,
Zone Supply Air Splitter;
AirLoopHVAC:ZoneMixer,
Zone Return Air Mixer,
Return Air Mixer Outlet,
Zone 1 Outlet Node,
Zone 2 Outlet Node,
Zone 3 Outlet Node;
AirLoopHVAC:ReturnPath,
TermReheatReturnPath,
Return Air Mixer Outlet,
AirLoopHVAC:ZoneMixer,
Zone Return Air Mixer;
Branch,
Air Loop Main Branch,
,
AirLoopHVAC:OutdoorAirSystem,
OA Sys 1,
Air Loop Inlet Node,
Mixed Air Node,
Fan:ConstantVolume,
Supply Fan 1,
Mixed Air Node,
Cooling Coil Air Inlet Node,
Coil:Cooling:Water:DetailedGeometry,
Detailed Cooling Coil,
Cooling Coil Air Inlet Node,
Air Loop Outlet Node;
Branch,
Cooling Demand Inlet,
,
Pipe:Adiabatic,
Demand Side Inlet Pipe,
CW Demand Inlet Node,
CW Demand Entrance Pipe Outlet Node;
Branch,
Cooling Coil Branch,
,
Coil:Cooling:Water:DetailedGeometry,
Detailed Cooling Coil,
Cooling Coil Water Inlet Node,
Cooling Coil Water Outlet Node;
Branch,
Demand Bypass Branch,
,
Pipe:Adiabatic,
Demand Side Bypass,
CW Demand Bypass Inlet Node,
CW Demand Bypass Outlet Node;
Branch,
Cooling Demand Outlet,
,
Pipe:Adiabatic,
CW Demand Side Outlet Pipe,
CW Demand Exit Pipe Inlet Node,
CW Demand Outlet Node;
Branch,
Cooling Supply Outlet,
,
Pipe:Adiabatic,
Supply Side Outlet Pipe,
Supply Side Exit Pipe Inlet Node,
CW Supply Outlet Node;
Branch,
CW Pump Branch,
,
Pump:VariableSpeed,
Circ Pump,
CW Supply Inlet Node,
CW Pump Outlet Node;
Branch,
Little Chiller Branch,
,
Chiller:ConstantCOP,
Little Chiller,
Little Chiller Inlet Node,
Little Chiller Outlet Node;
Branch,
Big Chiller Branch,
,
Chiller:Electric,
Big Chiller,
Big Chiller Inlet Node,
Big Chiller Outlet Node;
Branch,
Purchased Cooling Branch,
,
DistrictCooling,
Purchased Cooling,
Purchased Cooling Inlet Node,
Purchased Cooling Outlet Node;
Branch,
Supply Bypass Branch,
,
Pipe:Adiabatic,
Supply Side Bypass,
CW Supply Bypass Inlet Node,
CW Supply Bypass Outlet Node;
Branch,
Condenser Supply Inlet Branch,
,
Pump:VariableSpeed,
Cond Circ Pump,
Condenser Supply Inlet Node,
Condenser Pump Outlet Node;
Branch,
Condenser Supply Tower Branch,
,
CoolingTower:SingleSpeed,
Big Tower,
Condenser Tower Inlet Node,
Condenser Tower Outlet Node;
Branch,
Condenser Supply Bypass Branch,
,
Pipe:Adiabatic,
Condenser Supply Side Bypass,
Cond Supply Bypass Inlet Node,
Cond Supply Bypass Outlet Node;
Branch,
Condenser Supply Outlet Branch,
,
Pipe:Adiabatic,
Condenser Supply Outlet,
Condenser Supply Exit Pipe Inlet Node,
Condenser Supply Outlet Node;
Branch,
Condenser Demand Inlet Branch,
,
Pipe:Adiabatic,
Condenser Demand Inlet Pipe,
Condenser Demand Inlet Node,
Condenser Demand Entrance Pipe Outlet Node;
Branch,
Little Chiller Condenser Branch,
,
Chiller:ConstantCOP,
Little Chiller,
Little Chiller Condenser Inlet Node,
Little Chiller Condenser Outlet Node;
Branch,
Big Chiller Condenser Branch,
,
Chiller:Electric,
Big Chiller,
Big Chiller Condenser Inlet Node,
Big Chiller Condenser Outlet Node;
Branch,
Condenser Demand Bypass Branch,
,
Pipe:Adiabatic,
Condenser Demand Side Bypass,
Cond Demand Bypass Inlet Node,
Cond Demand Bypass Outlet Node;
Branch,
Condenser Demand Outlet Branch,
,
Pipe:Adiabatic,
Condenser Demand Outlet Pipe,
Condenser Demand Exit Pipe Inlet Node,
Condenser Demand Outlet Node;
Branch,
Heating Supply Inlet Branch,
,
Pump:VariableSpeed,
HW Circ Pump,
HW Supply Inlet Node,
HW Pump Outlet Node;
Branch,
Heating Purchased Hot Water Branch,
,
DistrictHeating,
Purchased Heating,
Purchased Heat Inlet Node,
Purchased Heat Outlet Node;
Branch,
Heating Supply Bypass Branch,
,
Pipe:Adiabatic,
Heating Supply Side Bypass,
Heating Supply Bypass Inlet Node,
Heating Supply Bypass Outlet Node;
Branch,
Heating Supply Outlet Branch,
,
Pipe:Adiabatic,
Heating Supply Outlet,
Heating Supply Exit Pipe Inlet Node,
HW Supply Outlet Node;
Branch,
Reheat Inlet Branch,
,
Pipe:Adiabatic,
Reheat Inlet Pipe,
HW Demand Inlet Node,
HW Demand Entrance Pipe Outlet Node;
Branch,
Reheat Outlet Branch,
,
Pipe:Adiabatic,
Reheat Outlet Pipe,
HW Demand Exit Pipe Inlet Node,
HW Demand Outlet Node;
Branch,
Zone 1 Reheat Branch,
,
Coil:Heating:Water,
Reheat Coil Zone 1,
Zone 1 Reheat Water Inlet Node,
Zone 1 Reheat Water Outlet Node;
Branch,
Zone 2 Reheat Branch,
,
Coil:Heating:Water,
Reheat Coil Zone 2,
Zone 2 Reheat Water Inlet Node,
Zone 2 Reheat Water Outlet Node;
Branch,
Zone 3 Reheat Branch,
,
Coil:Heating:Water,
Reheat Coil Zone 3,
Zone 3 Reheat Water Inlet Node,
Zone 3 Reheat Water Outlet Node;
Branch,
Reheat Bypass Branch,
,
Pipe:Adiabatic,
Reheat Bypass,
Reheat Bypass Inlet Node,
Reheat Bypass Outlet Node;
BranchList,
Air Loop Branches,
Air Loop Main Branch;
BranchList,
Cooling Supply Side Branches,
CW Pump Branch,
Little Chiller Branch,
Big Chiller Branch,
Purchased Cooling Branch,
Supply Bypass Branch,
Cooling Supply Outlet;
BranchList,
Cooling Demand Side Branches,
Cooling Demand Inlet,
Cooling Coil Branch,
Demand Bypass Branch,
Cooling Demand Outlet;
BranchList,
Condenser Supply Side Branches,
Condenser Supply Inlet Branch,
Condenser Supply Tower Branch,
Condenser Supply Bypass Branch,
Condenser Supply Outlet Branch;
BranchList,
Condenser Demand Side Branches,
Condenser Demand Inlet Branch,
Little Chiller Condenser Branch,
Big Chiller Condenser Branch,
Condenser Demand Bypass Branch,
Condenser Demand Outlet Branch;
BranchList,
Heating Supply Side Branches,
Heating Supply Inlet Branch,
Heating Purchased Hot Water Branch,
Heating Supply Bypass Branch,
Heating Supply Outlet Branch;
BranchList,
Heating Demand Side Branches,
Reheat Inlet Branch,
Zone 1 Reheat Branch,
Zone 2 Reheat Branch,
Zone 3 Reheat Branch,
Reheat Bypass Branch,
Reheat Outlet Branch;
Connector:Splitter,
CW Loop Splitter,
CW Pump Branch,
Little Chiller Branch,
Big Chiller Branch,
Purchased Cooling Branch,
Supply Bypass Branch;
Connector:Splitter,
CW Demand Splitter,
Cooling Demand Inlet,
Demand Bypass Branch,
Cooling Coil Branch;
Connector:Splitter,
Condenser Demand Splitter,
Condenser Demand Inlet Branch,
Big Chiller Condenser Branch,
Little Chiller Condenser Branch,
Condenser Demand Bypass Branch;
Connector:Splitter,
Condenser Supply Splitter,
Condenser Supply Inlet Branch,
Condenser Supply Tower Branch,
Condenser Supply Bypass Branch;
Connector:Splitter,
Reheat Splitter,
Reheat Inlet Branch,
Zone 1 Reheat Branch,
Zone 2 Reheat Branch,
Zone 3 Reheat Branch,
Reheat Bypass Branch;
Connector:Splitter,
Heating Supply Splitter,
Heating Supply Inlet Branch,
Heating Purchased Hot Water Branch,
Heating Supply Bypass Branch;
Connector:Mixer,
CW Loop Mixer,
Cooling Supply Outlet,
Little Chiller Branch,
Big Chiller Branch,
Purchased Cooling Branch,
Supply Bypass Branch;
Connector:Mixer,
CW Demand Mixer,
Cooling Demand Outlet,
Cooling Coil Branch,
Demand Bypass Branch;
Connector:Mixer,
Condenser Demand Mixer,
Condenser Demand Outlet Branch,
Big Chiller Condenser Branch,
Little Chiller Condenser Branch,
Condenser Demand Bypass Branch;
Connector:Mixer,
Condenser Supply Mixer,
Condenser Supply Outlet Branch,
Condenser Supply Tower Branch,
Condenser Supply Bypass Branch;
Connector:Mixer,
Reheat Mixer,
Reheat Outlet Branch,
Zone 1 Reheat Branch,
Zone 2 Reheat Branch,
Zone 3 Reheat Branch,
Reheat Bypass Branch;
Connector:Mixer,
Heating Supply Mixer,
Heating Supply Outlet Branch,
Heating Purchased Hot Water Branch,
Heating Supply Bypass Branch;
ConnectorList,
Cooling Supply Side Connectors,
Connector:Splitter,
CW Loop Splitter,
Connector:Mixer,
CW Loop Mixer;
ConnectorList,
Cooling Demand Side Connectors,
Connector:Splitter,
CW Demand Splitter,
Connector:Mixer,
CW Demand Mixer;
ConnectorList,
Condenser Supply Side Connectors,
Connector:Splitter,
Condenser Supply Splitter,
Connector:Mixer,
Condenser Supply Mixer;
ConnectorList,
Condenser Demand Side Connectors,
Connector:Splitter,
Condenser Demand Splitter,
Connector:Mixer,
Condenser Demand Mixer;
ConnectorList,
Heating Supply Side Connectors,
Connector:Splitter,
Heating Supply Splitter,
Connector:Mixer,
Heating Supply Mixer;
ConnectorList,
Heating Demand Side Connectors,
Connector:Splitter,
Reheat Splitter,
Connector:Mixer,
Reheat Mixer;
NodeList,
OutsideAirInletNodes,
Outside Air Inlet Node;
NodeList,
Chilled Water Loop Setpoint Node List,
CW Supply Outlet Node;
NodeList,
Hot Water Loop Setpoint Node List,
HW Supply Outlet Node;
NodeList,
Zone 2 Exhausts,
Zone 2 Exhaust Node;
NodeList,
Zone 3 Exhausts,
Zone 3 Exhaust Node;
NodeList,
Zone1Inlets,
Zone 1 Reheat Air Outlet Node;
NodeList,
Zone2Inlets,
Zone 2 Reheat Air Outlet Node;
NodeList,
Zone3Inlets,
Zone 3 Reheat Air Outlet Node;
NodeList,
Supply Air Temp Nodes,
Air Loop Outlet Node;
NodeList,
Mixed Air Nodes,
Mixed Air Node;
OutdoorAir:NodeList,
OutsideAirInletNodes;
Pipe:Adiabatic,
Demand Side Inlet Pipe,
CW Demand Inlet Node,
CW Demand Entrance Pipe Outlet Node;
Pipe:Adiabatic,
Demand Side Bypass,
CW Demand Bypass Inlet Node,
CW Demand Bypass Outlet Node;
Pipe:Adiabatic,
CW Demand Side Outlet Pipe,
CW Demand Exit Pipe Inlet Node,
CW Demand Outlet Node;
Pipe:Adiabatic,
Supply Side Outlet Pipe,
Supply Side Exit Pipe Inlet Node,
CW Supply Outlet Node;
Pipe:Adiabatic,
Supply Side Bypass,
CW Supply Bypass Inlet Node,
CW Supply Bypass Outlet Node;
Pipe:Adiabatic,
Condenser Supply Side Bypass,
Cond Supply Bypass Inlet Node,
Cond Supply Bypass Outlet Node;
Pipe:Adiabatic,
Condenser Supply Outlet,
Condenser Supply Exit Pipe Inlet Node,
Condenser Supply Outlet Node;
Pipe:Adiabatic,
Condenser Demand Inlet Pipe,
Condenser Demand Inlet Node,
Condenser Demand Entrance Pipe Outlet Node;
Pipe:Adiabatic,
Condenser Demand Side Bypass,
Cond Demand Bypass Inlet Node,
Cond Demand Bypass Outlet Node;
Pipe:Adiabatic,
Condenser Demand Outlet Pipe,
Condenser Demand Exit Pipe Inlet Node,
Condenser Demand Outlet Node;
Pipe:Adiabatic,
Heating Supply Side Bypass,
Heating Supply Bypass Inlet Node,
Heating Supply Bypass Outlet Node;
Pipe:Adiabatic,
Heating Supply Outlet,
Heating Supply Exit Pipe Inlet Node,
HW Supply Outlet Node;
Pipe:Adiabatic,
Reheat Inlet Pipe,
HW Demand Inlet Node,
HW Demand Entrance Pipe Outlet Node;
Pipe:Adiabatic,
Reheat Outlet Pipe,
HW Demand Exit Pipe Inlet Node,
HW Demand Outlet Node;
Pipe:Adiabatic,
Reheat Bypass,
Reheat Bypass Inlet Node,
Reheat Bypass Outlet Node;
Pump:VariableSpeed,
Circ Pump,
CW Supply Inlet Node,
CW Pump Outlet Node,
0.0011,
300000.0,
500.0,
0.87,
0.0,
0.0,
1.0,
0.0,
0.0,
0.0,
INTERMITTENT;
Pump:VariableSpeed,
Cond Circ Pump,
Condenser Supply Inlet Node,
Condenser Pump Outlet Node,
0.0011,
300000.0,
500.0,
0.87,
0.0,
0.0,
1.0,
0.0,
0.0,
0.0,
INTERMITTENT;
Pump:VariableSpeed,
HW Circ Pump,
HW Supply Inlet Node,
HW Pump Outlet Node,
0.0043,
300000.0,
2000.0,
0.87,
0.0,
0.0,
1.0,
0.0,
0.0,
0.0,
INTERMITTENT;
Chiller:Electric,
Big Chiller,
WaterCooled,
45000.0,
2.75,
Big Chiller Inlet Node,
Big Chiller Outlet Node,
Big Chiller Condenser Inlet Node,
Big Chiller Condenser Outlet Node,
0.15,
1.0,
0.65,
29.44,
2.682759,
6.667,
0.0011,
0.0005,
0.944836,
-0.0570088,
-0.00185486,
1.907846,
-1.204987,
0.2634623,
0.03303,
0.6852,
0.2818,
5.0,
LeavingSetpointModulated;
Chiller:ConstantCOP,
Little Chiller,
25000.0,
2.5,
0.0011,
0.0011,
Little Chiller Inlet Node,
Little Chiller Outlet Node,
Little Chiller Condenser Inlet Node,
Little Chiller Condenser Outlet Node,
WaterCooled,
LeavingSetpointModulated,
;
DistrictCooling,
Purchased Cooling,
Purchased Cooling Inlet Node,
Purchased Cooling Outlet Node,
680000.0;
DistrictHeating,
Purchased Heating,
Purchased Heat Inlet Node,
Purchased Heat Outlet Node,
1000000.0;
CoolingTower:SingleSpeed,
Big Tower,
Condenser Tower Inlet Node,
Condenser Tower Outlet Node,
0.0011,
16.0,
1000.0,
1750.0,
0.0,
,
0.0,
,
UFactorTimesAreaAndDesignWaterFlowRate,
,
,
,
;
PlantLoop,
Chilled Water Loop,
Water,
,
CW Loop Operation,
CW Supply Outlet Node,
98.0,
1.0,
0.0011,
0.0,
autocalculate,
CW Supply Inlet Node,
CW Supply Outlet Node,
Cooling Supply Side Branches,
Cooling Supply Side Connectors,
CW Demand Inlet Node,
CW Demand Outlet Node,
Cooling Demand Side Branches,
Cooling Demand Side Connectors,
Optimal;
PlantLoop,
Hot Water Loop,
Water,
,
Hot Loop Operation,
HW Supply Outlet Node,
100.0,
10.0,
0.0043,
0.0,
autocalculate,
HW Supply Inlet Node,
HW Supply Outlet Node,
Heating Supply Side Branches,
Heating Supply Side Connectors,
HW Demand Inlet Node,
HW Demand Outlet Node,
Heating Demand Side Branches,
Heating Demand Side Connectors,
Optimal;
CondenserLoop,
Chilled Water Condenser Loop,
Water,
,
Tower Loop Operation,
Condenser Supply Outlet Node,
80.0,
10.0,
0.0011,
0.0,
autocalculate,
Condenser Supply Inlet Node,
Condenser Supply Outlet Node,
Condenser Supply Side Branches,
Condenser Supply Side Connectors,
Condenser Demand Inlet Node,
Condenser Demand Outlet Node,
Condenser Demand Side Branches,
Condenser Demand Side Connectors,
SequentialLoad;
PlantEquipmentList,
Chiller Plant,
Chiller:ConstantCOP,
Little Chiller;
PlantEquipmentList,
Chiller Plant and Purchased,
Chiller:Electric,
Big Chiller,
DistrictCooling,
Purchased Cooling;
PlantEquipmentList,
Purchased Only,
DistrictCooling,
Purchased Cooling;
PlantEquipmentList,
All Chillers,
Chiller:Electric,
Big Chiller,
Chiller:ConstantCOP,
Little Chiller;
PlantEquipmentList,
heating plant,
DistrictHeating,
Purchased Heating;
CondenserEquipmentList,
All Towers,
CoolingTower:SingleSpeed,
Big Tower;
PlantEquipmentOperation:CoolingLoad,
Peak Operation,
0.0,
70000.0,
Chiller Plant,
70000.0,
245000.0,
Chiller Plant and Purchased,
245000.0,
500000.0,
Purchased Only;
PlantEquipmentOperation:CoolingLoad,
Off Peak Operation,
0.0,
900000.0,
All Chillers;
PlantEquipmentOperation:CoolingLoad,
Year Round Tower Operation,
0.0,
90000000.0,
All Towers;
PlantEquipmentOperation:HeatingLoad,
Purchased Only,
0.0,
1000000.0,
heating plant;
PlantEquipmentOperationSchemes,
CW Loop Operation,
PlantEquipmentOperation:CoolingLoad,
Peak Operation,
On Peak,
PlantEquipmentOperation:CoolingLoad,
Off Peak Operation,
Off Peak;
PlantEquipmentOperationSchemes,
Hot Loop Operation,
PlantEquipmentOperation:HeatingLoad,
Purchased Only,
ON;
CondenserEquipmentOperationSchemes,
Tower Loop Operation,
PlantEquipmentOperation:CoolingLoad,
Year Round Tower Operation,
ON;
AvailabilityManager:Scheduled,
Reheat System 1 Avail,
FanAndCoilAvailSched;
AvailabilityManagerAssignmentList,
Reheat System 1 Avail List,
AvailabilityManager:Scheduled,
Reheat System 1 Avail;
SetpointManager:Scheduled,
Chilled Water Loop Setpoint Manager,
Temperature,
CW Loop Temp Schedule,
Chilled Water Loop Setpoint Node List;
SetpointManager:Scheduled,
Big Chiller Setpoint Manager,
Temperature,
CW Loop Temp Schedule,
Big Chiller Outlet Node;
SetpointManager:Scheduled,
Little Chiller Setpoint Manager,
Temperature,
CW Loop Temp Schedule,
Little Chiller Outlet Node;
SetpointManager:Scheduled,
Hot Water Loop Setpoint Manager,
Temperature,
HW Loop Temp Schedule,
Hot Water Loop Setpoint Node List;
SetpointManager:Scheduled,
Supply Air Temp Manager,
Temperature,
Seasonal Reset Supply Air Temp Sch,
Supply Air Temp Nodes;
SetpointManager:Scheduled,
Mixed Air Temp Manager,
Temperature,
Seasonal Reset Mixed Air Temp Sch,
Mixed Air Nodes;
SetpointManager:FollowOutdoorAirTemperature,
MyCondenserControl,
Temperature,
OutdoorAirWetBulb,
0.0,
80.0,
10.0,
Condenser Supply Outlet Node;
Output:VariableDictionary,
Regular;
Output:Table:SummaryReports,
AllSummary;
OutputControl:Table:Style,
HTML;
Output:Variable,
*,
Zone Air System Sensible Cooling Rate,
hourly;
Output:Variable,
*,
Zone Air System Sensible Heating Rate,
hourly;
Output:Variable,
*,
Zone Air Temperature,
hourly;
Output:Variable,
*,
Cooling Coil Total Cooling Rate,
hourly;
Output:Variable,
*,
Heating Coil Heating Rate,
hourly;
Output:Variable,
*,
Site Outdoor Air Drybulb Temperature,
hourly;
Output:Variable,
Mixed Air Node,
System Node Mass Flow Rate,
hourly;
Output:Variable,
Mixed Air Node,
System Node Temperature,
hourly;
Output:Variable,
Outside Air Inlet Node,
System Node Mass Flow Rate,
hourly;
Output:Variable,
Outside Air Inlet Node,
System Node Temperature,
hourly;
Output:Variable,
Air Loop Outlet Node,
System Node Mass Flow Rate,
hourly;
Output:Variable,
Air Loop Outlet Node,
System Node Temperature,
hourly;
Output:Variable,
Air Loop Inlet Node,
System Node Mass Flow Rate,
hourly;
Output:Variable,
Air Loop Inlet Node,
System Node Temperature,
hourly;
Output:Variable,
Relief Air Outlet Node,
System Node Mass Flow Rate,
hourly;
Output:Variable,
Relief Air Outlet Node,
System Node Temperature,
hourly;
Output:Meter:MeterFileOnly,
Electricity:Facility,
monthly;
Output:Meter:MeterFileOnly,
Electricity:Building,
monthly;
Output:Meter:MeterFileOnly,
InteriorLights:Electricity,
monthly;
Output:Meter:MeterFileOnly,
Electricity:HVAC,
monthly;
Output:Meter:MeterFileOnly,
Electricity:Plant,
monthly;
Output:Meter:MeterFileOnly,
Electricity:Facility,
runperiod;
Output:Meter:MeterFileOnly,
Electricity:Building,
runperiod;
Output:Meter:MeterFileOnly,
InteriorLights:Electricity,
runperiod;
Output:Meter:MeterFileOnly,
Electricity:HVAC,
runperiod;
Output:Meter:MeterFileOnly,
Electricity:Plant,
runperiod;"""


@pytest.fixture(scope="function")
def idfsnippet(makeIDFfortesting):
    fIDF = makeIDFfortesting
    idf = fIDF(StringIO(idftxt))
    idf.saveas("a.idf")
    return idf


def test_findequipmentconnection(idfsnippet):
    """py.test for findequipmentconnection"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.findequipmentconnection(idf, zone)
    assert result.Zone_Name == zone.Name
    zone = idf.newidfobject("zone", "gumby")
    result = hvac.findequipmentconnection(idf, zone)
    assert result == None


def test_findequipmentlist(idfsnippet):
    """py.test for findequipmentlist"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.findequipmentlist(idf, zone)
    assert result[-1].Zone_Name == zone.Name
    assert result[-1].Zone_Conditioning_Equipment_List_Name == result[0].Name
    zone = idf.newidfobject("zone", "gumby")
    result = hvac.findequipmentlist(idf, zone)
    assert result == None
    econnction = idf.newidfobject("ZoneHVAC:EquipmentConnections", Zone_Name="gumby")
    result = hvac.findequipmentlist(idf, zone)
    assert result == None


def test_hasexhaust(idfsnippet):
    """py.test for hasexhaust"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.hasexhaust(idf, zone)
    assert result == False
    zone = idf.idfobjects["zone"][1]
    result = hvac.hasexhaust(idf, zone)
    assert result == "Zone 2 Exhausts"
    zone = idf.idfobjects["zone"][2]
    result = hvac.hasexhaust(idf, zone)
    assert result == "Zone 3 Exhausts"


def test_findexhaust(idfsnippet):
    """py.test for findexhaust"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    result = hvac.findexhaust(idf, zone)
    assert result == None
    # ---
    exfanname = "Zone 2 Exhaust Fan"
    zone = idf.idfobjects["zone"][1]
    result = hvac.findexhaust(idf, zone)
    assert result.Name == exfanname


def test_removeexhaust(idfsnippet):
    """py.test for removeexhaust"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][1]
    eqlist, _ = hvac.findequipmentlist(idf, zone)
    exfan = hvac.removeexhaust(idf, zone)
    expectedname = "Zone 2 Exhaust Fan"
    assert exfan.Name == expectedname
    assert hvac.hasexhaust(idf, zone) == False
    # test if exhaust fan has been removed from 'ZONEHVAC:EQUIPMENTLIST'
    extlist = extfields.extensiblefields2list(eqlist)
    eqlistitems = [
        item for item in extlist if item[0].upper() == "Fan:ZoneExhaust".upper()
    ]
    assert not eqlistitems  # list should be empty


def test_putexhaust(idfsnippet):
    """py.test for putexhaust"""
    idf = idfsnippet
    zone = idf.idfobjects["zone"][0]
    exfan = idf.newidfobject("Fan:ZoneExhaust", Name="zone1_exhaust_fan")
    idf = hvac.putexhaust(idf, zone, exfan)
    assert hvac.hasexhaust(idf, zone) == "zone1_exhaust_fan Node List"
    assert hvac.findexhaust(idf, zone) == exfan
    # test if ex fan is in equiplist
    eqlist, _ = hvac.findequipmentlist(idf, zone)
    extlist = extfields.extensiblefields2list(eqlist)
    objecttypes = [item for item in extlist if item[0].upper() == "FAN:ZONEEXHAUST"]
    idf.saveas("b.idf")
    assert objecttypes # has an item in it ie. "FAN:ZONEEXHAUST"

# TODO : make an idf generator that does not depend on the large idftext 
# - either generate it prgramatically as in test_geometry
# - or remove all the unneeded objects
#     - this may is easier as a first pass
#     - and better since the hvac code depends on IDD not changing

# TODO add and remove exhaust fans in multiple example files - to see how robust it is.
# TODO use the functions to change TermReheatZoneExh.idf and run the changed file - DONE