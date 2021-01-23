# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-

"""py.test for files in experimental.runandget"""


import os
import pytest
from pathlib import Path
from io import StringIO
import json
import bz2
from importlib import reload
import tempfile

from eppy import modeleditor
from eppy.pytest_helpers import do_integration_tests
from eppy.runner.run_functions import install_paths, EnergyPlusRunError
import witheppy.runandget as runandget
from eppy.results import readhtml

import pprint

pp = pprint.PrettyPrinter()


def makeidf():
    """return an idf"""
    reload(modeleditor)  # to make sure you have the right IDD
    iddfile = os.path.join(IDD_FILES, TEST_IDD)
    fname1 = os.path.join(IDF_FILES, TEST_IDF)
    modeleditor.IDF.setiddname(iddfile, testing=True)
    idf = modeleditor.IDF(fname1, TEST_EPW)
    # put a expidf object in.
    idf.newidfobject(
        "HVACTEMPLATE:THERMOSTAT",
        Name="TestThermostat",
        Cooling_Setpoint_Schedule_Name="",
        Heating_Setpoint_Schedule_Name="",
        Constant_Cooling_Setpoint=25,
        Constant_Heating_Setpoint=21,
    )
    # put and sql output
    idf.newidfobject(
        "Output:SQlite",
        Option_Type="simple",
    )
    return idf


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(THIS_DIR, os.pardir, "witheppy", "resources")
IDD_FILES = os.path.join(RESOURCES_DIR, "iddfiles")
IDF_FILES = os.path.join(RESOURCES_DIR, "idffiles")
try:
    VERSION = os.environ["ENERGYPLUS_INSTALL_VERSION"]  # used in CI files
except KeyError:
    VERSION = "8-9-0"  # current default for integration tests on local system
TEST_IDF = "V{}/smallfile.idf".format(VERSION[:3].replace("-", "_"))
TEST_EPW = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
TEST_IDD = "Energy+V{}.idd".format(VERSION.replace("-", "_"))
AN_IDF = makeidf()
RESULT_DIR = Path("./resultsdir")


@pytest.mark.parametrize(
    "filename, content, expected",
    [
        ("dummypath.txt", "content", "content"),
    ],  # filename, content, expected
)
def test_getfile(tmp_path, filename, content, expected):
    """py.test for getfile
    It generates a temp pathtofile so that it can be deleted
    after the test"""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / filename
    p.write_text(content)
    pathtofile = p.resolve()
    result = runandget.getfile(pathtofile)
    assert result == expected


@pytest.mark.parametrize(
    "filename, content, expected",
    [
        (
            "dummypath.txt",
            "content\ncontent\n",
            "content\n",
        ),  # filename, content, expected
    ],
)
def test_getfilehandle(tmp_path, filename, content, expected):
    """py.test for getfilehandle
    It generates a temp pathtofile so that it can be deleted
    after the test"""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / filename
    p.write_text(content)
    pathtofile = p.resolve()
    fhandle = runandget.getfilehandle(pathtofile)
    for line in fhandle:
        assert line == expected


@pytest.mark.parametrize(
    "whichresult, options, expected",
    [
        ("err", None, Path("eplusout.err")),  # whichresult, options, expected
        (
            "err",
            dict(output_suffix="L"),
            Path("eplusout.err"),
        ),  # whichresult, options, expected
        (
            "err",
            dict(output_suffix="D"),
            Path("eplus.err"),
        ),  # whichresult, options, expected
        (
            "htm",
            dict(output_suffix="C"),
            Path("eplusTable.htm"),
        ),  # whichresult, options, expected
        # include output_suffix
        (
            "htm",
            dict(output_suffix="C", output_prefix="Tens"),
            Path("TensTable.htm"),
        ),  # whichresult, options, expected
        # include output_directory
        (
            "htm",
            dict(
                output_suffix="D",
                output_prefix="Tens",
                output_directory="../gaby/under/",
            ),
            Path("../gaby/under/Tens-table.htm"),
        ),  # whichresult, options, expected
    ],
)
def test_options2filename(whichresult, options, expected):
    """py.test for options2filename"""
    result = runandget.options2filename(whichresult, options)
    assert result == expected


htmltabletxt = """<!DOCTYPE html>
<html>
<head>
<title> Bldg RUN PERIOD 1 ** San Francisco Intl Ap CA USA TMY3 WMO#=724940
  2020-12-13
  18:29:57
 - EnergyPlus</title>
</head>
<body>
<p><a href="#toc" style="float: right">Table of Contents</a></p>
<a name=top></a>
<p>Program Version:<b>EnergyPlus, Version 9.3.0-baff08990c, YMD=2020.12.13 18:29</b></p>
<p>Tabular Output Report in Format: <b>HTML</b></p>
<p>Building: <b>Bldg</b></p>
<p>Environment: <b>RUN PERIOD 1 ** San Francisco Intl Ap CA USA TMY3 WMO#=724940</b></p>
<p>Simulation Timestamp: <b>2020-12-13
  18:29:57</b></p>
<hr>
<p><a href="#toc" style="float: right">Table of Contents</a></p>
<a name=AnnualBuildingUtilityPerformanceSummary::EntireFacility></a>
<p>Report:<b> Annual Building Utility Performance Summary</b></p>
<p>For:<b> Entire Facility</b></p>
<p>Timestamp: <b>2020-12-13
    18:29:57</b></p>
<b>Values gathered over      8760.00 hours</b><br><br>
<b></b><br><br>
<b>Site and Source Energy</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Site and Source Energy-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Total Energy [GJ]</td>
    <td align="right">Energy Per Total Building Area [MJ/m2]</td>
    <td align="right">Energy Per Conditioned Building Area [MJ/m2]</td>
  </tr>
  <tr>
    <td align="right">Total Site Energy</td>
    <td align="right">       18.06</td>
    <td align="right">       77.76</td>
    <td align="right">       77.76</td>
  </tr>
  <tr>
    <td align="right">Net Site Energy</td>
    <td align="right">       18.06</td>
    <td align="right">       77.76</td>
    <td align="right">       77.76</td>
  </tr>
  <tr>
    <td align="right">Total Source Energy</td>
    <td align="right">       57.20</td>
    <td align="right">      246.26</td>
    <td align="right">      246.26</td>
  </tr>
  <tr>
    <td align="right">Net Source Energy</td>
    <td align="right">       57.20</td>
    <td align="right">      246.26</td>
    <td align="right">      246.26</td>
  </tr>
</table>
<br><br>
<b>Site to Source Energy Conversion Factors</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Site to Source Energy Conversion Factors-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Site=>Source Conversion Factor</td>
  </tr>
  <tr>
    <td align="right">Electricity</td>
    <td align="right">       3.167</td>
  </tr>
  <tr>
    <td align="right">Natural Gas</td>
    <td align="right">       1.084</td>
  </tr>
  <tr>
    <td align="right">District Cooling</td>
    <td align="right">       1.056</td>
  </tr>
  <tr>
    <td align="right">District Heating</td>
    <td align="right">       3.613</td>
  </tr>
  <tr>
    <td align="right">Steam</td>
    <td align="right">       0.300</td>
  </tr>
  <tr>
    <td align="right">Gasoline</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Diesel</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Coal</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Fuel Oil #1</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Fuel Oil #2</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Propane</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Other Fuel 1</td>
    <td align="right">       1.000</td>
  </tr>
  <tr>
    <td align="right">Other Fuel 2</td>
    <td align="right">       1.000</td>
  </tr>
</table>
<br><br>
</body>
</html>
"""


@pytest.mark.parametrize(
    "htm_txt, htm_options, expected",
    [
        (
            htmltabletxt,
            dict(
                whichfile="htm",
                as_tables=True,
            ),
            {
                "whichfile": "htm",
                "as_tables": True,
                "result": [
                    [
                        "Site and Source Energy",
                        [
                            [
                                "",
                                "Total Energy [GJ]",
                                "Energy Per Total Building Area [MJ/m2]",
                                "Energy Per Conditioned Building Area [MJ/m2]",
                            ],
                            ["Total Site Energy", 18.06, 77.76, 77.76],
                            ["Net Site Energy", 18.06, 77.76, 77.76],
                            ["Total Source Energy", 57.2, 246.26, 246.26],
                            ["Net Source Energy", 57.2, 246.26, 246.26],
                        ],
                    ],
                    [
                        "Site to Source Energy Conversion Factors",
                        [
                            ["", "Site=>Source Conversion Factor"],
                            ["Electricity", 3.167],
                            ["Natural Gas", 1.084],
                            ["District Cooling", 1.056],
                            ["District Heating", 3.613],
                            ["Steam", 0.3],
                            ["Gasoline", 1.05],
                            ["Diesel", 1.05],
                            ["Coal", 1.05],
                            ["Fuel Oil #1", 1.05],
                            ["Fuel Oil #2", 1.05],
                            ["Propane", 1.05],
                            ["Other Fuel 1", 1.0],
                            ["Other Fuel 2", 1.0],
                        ],
                    ],
                ],
            },
        ),
        # htm_txt, htm_options, expected
        (
            htmltabletxt,
            dict(
                whichfile="htm",
                tableindex=1,  # or tablename
                # tablename="Site and Source Energy",  # tableindex takes priority if both given
                table=True,
            ),
            {
                "whichfile": "htm",
                "tableindex": 1,  # or tablename
                "table": True,
                "result": [
                    "Site to Source Energy Conversion Factors",
                    [
                        ["", "Site=>Source Conversion Factor"],
                        ["Electricity", 3.167],
                        ["Natural Gas", 1.084],
                        ["District Cooling", 1.056],
                        ["District Heating", 3.613],
                        ["Steam", 0.3],
                        ["Gasoline", 1.05],
                        ["Diesel", 1.05],
                        ["Coal", 1.05],
                        ["Fuel Oil #1", 1.05],
                        ["Fuel Oil #2", 1.05],
                        ["Propane", 1.05],
                        ["Other Fuel 1", 1.0],
                        ["Other Fuel 2", 1.0],
                    ],
                ],
            },
        ),
        # htm_txt, htm_options, expected
        (
            htmltabletxt,
            dict(
                whichfile="htm",
                tableindex=0,  # or tablename
                tablename="Site and Source Energy",  # tableindex takes priority if both given
                rows=[0, 1, -1],  # will return 3 rows as indexed
                # cols=[0, 1, 3],  # will return 3 columns as indexed
                # cells=[[0, -1], [-1, -1]]  # will return 2 cells
            ),
            {
                "whichfile": "htm",
                "tableindex": 0,  # or tablename
                "tablename": "Site and Source Energy",  # tableindex takes priority if both given
                "rows": [0, 1, -1],
                "result": [
                    "Site and Source Energy",
                    [
                        [
                            "",
                            "Total Energy [GJ]",
                            "Energy Per Total Building Area [MJ/m2]",
                            "Energy Per Conditioned Building Area [MJ/m2]",
                        ],
                        ["Total Site Energy", 18.06, 77.76, 77.76],
                        ["Net Source Energy", 57.2, 246.26, 246.26],
                    ],
                ],
            },
        ),
        # htm_txt, htm_options, expected
        (
            htmltabletxt,
            dict(
                whichfile="htm",
                tableindex=0,  # or tablename
                tablename="Site and Source Energy",  # tableindex takes priority if both given
                cols=[0, 1, -1],  # will return 3 columns as indexed
            ),
            {
                "whichfile": "htm",
                "tableindex": 0,  # or tablename
                "tablename": "Site and Source Energy",  # tableindex takes priority if both given
                "cols": [0, 1, -1],  # will return 3 columns as indexed
                "result": [
                    "Site and Source Energy",
                    [
                        [
                            "",
                            "Total Energy [GJ]",
                            "Energy Per Conditioned Building Area [MJ/m2]",
                        ],
                        ["Total Site Energy", 18.06, 77.76],
                        ["Net Site Energy", 18.06, 77.76],
                        ["Total Source Energy", 57.2, 246.26],
                        ["Net Source Energy", 57.2, 246.26],
                    ],
                ],
            },
        ),
        # htm_txt, htm_options, expected
        (
            htmltabletxt,
            dict(
                whichfile="htm",
                tableindex=0,  # or tablename
                tablename="Site and Source Energy",  # tableindex takes priority if both given
                # rows=[0, 1, -1],  # will return 3 rows as indexed
                # cols=[0, 1, -1],  # will return 3 columns as indexed
                cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
            ),
            {
                "whichfile": "htm",
                "tableindex": 0,  # or tablename
                "tablename": "Site and Source Energy",
                "cells": [[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                "result": [
                    "Site and Source Energy",
                    ["Energy Per Conditioned Building Area [MJ/m2]", 77.76, 246.26],
                ],
            },
        ),
        # htm_txt, htm_options, expected
    ],
)
def test_getfromhtm(tmp_path, htm_txt, htm_options, expected):
    """py.test for getfromhtm"""
    tmpdir = tmp_path
    tmpfile = tmpdir / "tablefile.htm"
    tmpfile.write_text(htm_txt)
    pathtofile = tmpfile.resolve()
    fhandle = open(pathtofile, "rb")
    result = runandget.getfromhtm(fhandle, htm_options)
    assert result == expected


@pytest.mark.parametrize(
    "row, colid, expected",
    [
        (["c1", "c2", "c3"], 1, 1),  # row, colid, expected
        (["c1", "c2", "c3"], 10, None),  # row, colid, expected
        (["c1", "c2", "c3"], "c1", 0),  # row, colid, expected
        (["c1", "c2", "c3"], "c15", None),  # row, colid, expected
    ],
)
def test__col2index(row, colid, expected):
    """py.test for _col2index"""
    result = runandget._col2index(row, colid)
    assert result == expected


@pytest.mark.parametrize(
    "row, col_list, expected",
    [
        (["c1", "c2", "c3"], [0], [0]),  # row, col_list, expected
        (["c1", "c2", "c3"], [1, 0], [1, 0]),  # row, col_list, expected
        (["c1", "c2", "c3"], [1, "c1"], [1, 0]),  # row, col_list, expected
        (["c1", "c2", "c3"], ["c2", "c1"], [1, 0]),  # row, col_list, expected
    ],
)
def test_col_list2index(row, col_list, expected):
    """py.test for _col_list2index"""
    result = runandget._col_list2index(row, col_list)
    assert result == expected


@pytest.mark.parametrize(
    "csvtxt, col_list, expected",
    [
        (
            """col1, col2, col3
1, 2, 3
11, 22, 33""",
            [
                1,
            ],
            [["col2"], ["2"], ["22"]],
        ),  # csvtxt, col_list, expected
        (
            """col1, col2, col3
1, 2, 3
11, 22, 33""",
            ["col3", 0],
            [["col3", "col1"], ["3", "1"], ["33", "11"]],
        ),  # csvtxt, col_list, expected
        (
            """col1, col2, col3
1, 2
11, 22, 33""",
            ["col3", 0],
            [["col3", "col1"], ["", "1"], ["33", "11"]],
        ),  # csvtxt, col_list, expected
        (
            """col1, col2, col3
1, 2
11, 22""",
            ["col3"],
            [
                [
                    "col3",
                ],
                [
                    "",
                ],
                [
                    "",
                ],
            ],
        ),  # csvtxt, col_list, expected
    ],
)
def test_getcsvcols(csvtxt, col_list, expected):
    """docstring for getcsvcols"""
    fhandle = StringIO(csvtxt)
    result = list(runandget.getcsvcols(fhandle, col_list))
    assert result == expected


def runidf(pathtorun, output_suffix="D"):
    """just run the idf"""
    idf = AN_IDF
    runoptions = dict(
        output_suffix=output_suffix,
        output_prefix="Thumba",
        output_directory=pathtorun,
        readvars=True,
        expandobjects=True,
    )
    idf.run(**runoptions)
    return runoptions


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_result_exists(resultsdir, runsimulation):
    """py.test to see if the result files are found correctly
    tests for all the output_suffix and all available result files"""
    resulttypes = runandget.resulttypes
    for item in ("dxf", "mtr", "tab", "mcsv"):
        resulttypes.remove(item)  # our simple idf does not generate these files
    for output_suffix in ("L", "D", "C"):
        runoptions = dict(output_directory=RESULT_DIR / output_suffix, readvars=True)
        for rtype in resulttypes:
            getdict = dict(resultname=dict(whichfile=rtype, entirefile=True))
            try:
                byteresult = runandget.getrun(runoptions, getdict)
                assert byteresult["resultname"]["result"]  # test if it got some result
            except FileNotFoundError as e:
                assert False


def first10chars(txt):
    return txt[:10]


def last10chars(txt):
    return txt[-10:]


def firstcol(rows):
    return [row[0] for row in rows]


def lastcol(rows):
    return [row[-1] for row in rows]


def firstrow(rows):
    return rows[0]


def lastrow(rows):
    return rows[-1]


def firstcell(rows):
    return rows[0][0]


def lastcell(rows):
    return rows[-1][-1]


def tablelastcell(htable):
    return htable[-1][-1][-1]


def donothing(stuff):
    return stuff


@pytest.mark.parametrize(
    "getdict, func, expected",
    [
        # tableindex get cells
        (
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    tablename="Site and Source Energy",  # tableindex takes priority if both given
                    # rows=[0, 1, -1],  # will return 3 rows as indexed
                    # cols=[0, 1, -1],  # will return 3 columns as indexed
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            donothing,
            [
                "Site to Source Energy Conversion Factors",
                ["Site=>Source Conversion Factor", 3.167, 1.0],
            ],
        ),  # getdict, func, expected
        # tableindex get rows
        (
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    # tablename="Site and Source Energy",  # tableindex takes priority if both given
                    rows=[0, -1, 1],  # will return 3 rows as indexed
                    # cols=[0, 1, 3],  # will return 3 columns as indexed
                    # cells=[[0, -1], [-1, -1]]  # will return 2 cells
                )
            ),
            tablelastcell,
            3.167,
        ),  # getdict, func, expected
        # tableindex get cols
        (
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    # tablename="Site to Source Energy Conversion Factors",  # tableindex takes priority if both given
                    # rows=[0, 1, -1],  # will return 3 rows as indexed
                    cols=[0, 1, -1],  # will return 3 columns as indexed
                    # cells=[[0, -1], [-1, -1]]  # will return 2 cells
                )
            ),
            tablelastcell,
            1.0,
        ),  # getdict, func, expected
        # tablename
        (
            dict(
                resultname=dict(
                    whichfile="htm",
                    tablename="Schedules-SetPoints (Schedule Type=Temperature)",  # tableindextakes priority ifboth given
                    table=True,
                )
            ),
            tablelastcell,
            365.0,
        ),  # getdict, func, expected
        # csv cols
        (
            dict(
                resultname=dict(
                    whichfile="csv",
                    cols=[1, "Date/Time"],
                )
            ),
            firstrow,
            [
                "Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)",
                "Date/Time",
            ],
        ),  # getdict, func, expected
        # entirefile
        (
            dict(resultname=dict(whichfile="end", entirefile=True)),
            first10chars,
            "EnergyPlus Completed Successfully"[:10],
        ),  # getdict, func, expected
    ],
)
@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_getsome_results(resultsdir, runsimulation, getdict, func, expected):
    """py.test to test some getdicts"""
    resdir = RESULT_DIR
    # for folder in resdir.iterdir():
    for output_suffix in ["C", "L", "D"]:
        runoptions = dict(output_directory=RESULT_DIR / output_suffix)
        returned = runandget.getrun(runoptions, getdict)
        result = returned["resultname"]["result"]
        try:
            result = result.decode()
        except AttributeError as e:
            pass
        assert func(result) == expected


@pytest.mark.parametrize(
    "subdir, getdict, json_it, compress_it, expected",
    [
        (
            "sub1",
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            False,
            False,
            {
                "resultname": {
                    "whichfile": "htm",
                    "tableindex": 1,
                    "cells": [[0, -1], [1, -1], [-1, -1]],
                    "entirefile": None,
                    "result": [
                        "Site to Source Energy Conversion Factors",
                        ["Site=>Source Conversion Factor", 3.167, 1.0],
                    ],
                }
            },
        ),  # subdir, getdict, json_it, expected
        (
            "sub2",
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            True,
            False,
            {
                "resultname": {
                    "whichfile": "htm",
                    "tableindex": 1,
                    "cells": [[0, -1], [1, -1], [-1, -1]],
                    "entirefile": None,
                    "result": [
                        "Site to Source Energy Conversion Factors",
                        ["Site=>Source Conversion Factor", 3.167, 1.0],
                    ],
                }
            },
        ),  # subdir, getdict, json_it, expected
        (
            "sub3",
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            True,
            False,
            {
                "resultname": {
                    "whichfile": "htm",
                    "tableindex": 1,
                    "cells": [[0, -1], [1, -1], [-1, -1]],
                    "entirefile": None,
                    "result": [
                        "Site to Source Energy Conversion Factors",
                        ["Site=>Source Conversion Factor", 3.167, 1.0],
                    ],
                }
            },
        ),  # subdir, getdict, json_it, expected
    ],
)
@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_runandget(tmp_path, subdir, getdict, json_it, compress_it, expected):
    """py.test for runandget"""
    idf = AN_IDF
    temp_folder = tmp_path / subdir
    temp_folder.mkdir()
    runoptions = dict(output_directory=temp_folder)
    fullresult = runandget.runandget(idf, runoptions, getdict, json_it, compress_it)
    reverse_result = reverseresult(fullresult, json_it, compress_it)
    assert reverse_result == expected


@pytest.mark.parametrize(
    "idf, getdict, json_it, compress_it, expected",
    [
        (
            AN_IDF,
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            False,
            False,
            {
                "resultname": {
                    "whichfile": "htm",
                    "tableindex": 1,
                    "cells": [[0, -1], [1, -1], [-1, -1]],
                    "entirefile": None,
                    "result": [
                        "Site to Source Energy Conversion Factors",
                        ["Site=>Source Conversion Factor", 3.167, 1.0],
                    ],
                }
            },
        ),  # idf, getdict, json_it, compress_it, expected
        (
            AN_IDF,
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            True,
            False,
            {
                "resultname": {
                    "whichfile": "htm",
                    "tableindex": 1,
                    "cells": [[0, -1], [1, -1], [-1, -1]],
                    "entirefile": None,
                    "result": [
                        "Site to Source Energy Conversion Factors",
                        ["Site=>Source Conversion Factor", 3.167, 1.0],
                    ],
                }
            },
        ),  # idf, getdict, json_it, compress_it, expected
        (
            AN_IDF,
            dict(
                resultname=dict(
                    whichfile="htm",
                    tableindex=1,  # or tablename
                    cells=[[0, -1], [1, -1], [-1, -1]],  # will return 2 cells
                ),
            ),
            True,
            True,
            {
                "resultname": {
                    "whichfile": "htm",
                    "tableindex": 1,
                    "cells": [[0, -1], [1, -1], [-1, -1]],
                    "entirefile": None,
                    "result": [
                        "Site to Source Energy Conversion Factors",
                        ["Site=>Source Conversion Factor", 3.167, 1.0],
                    ],
                }
            },
        ),  # idf, getdict, json_it, compress_it, expected
    ],
)
@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_anon_runandget(idf, getdict, json_it, compress_it, expected):
    """py.test for anon_runandget"""
    fullresult = runandget.anon_runandget(idf, getdict, json_it, compress_it)
    reverse_result = reverseresult(fullresult, json_it, compress_it)
    assert reverse_result == expected
    # assert fullresult == expected


def reverseresult(result, json_it=False, compress_it=False):
    if compress_it:
        reverse_result = json.loads(bz2.decompress(result).decode())
    elif json_it:
        reverse_result = json.loads(result)
    else:
        reverse_result = result
    return reverse_result


@pytest.mark.parametrize(
    "thedict, json_it, compress_it",
    [
        (dict(a=1, b=2), False, False),  # thedict, json_it, compress_it
        (dict(a=1, b=2), True, False),  # thedict, json_it, compress_it
        (dict(a=1, b=2), True, True),  # thedict, json_it, compress_it
        (dict(a=1, b=2), False, True),  # thedict, json_it, compress_it
    ],
)
def test_dict2json(thedict, json_it, compress_it):
    """py.test for dict2json"""
    result = runandget.dict2json(thedict, json_it, compress_it)
    reverse_result = reverseresult(result, json_it, compress_it)
    assert reverse_result == thedict


@pytest.fixture(scope="module")
def runsimulation_old(request):
    marker = request.node.get_closest_marker("runoptions_data")
    if marker is None:
        # Handle missing marker in some way...
        data = None
    else:
        data = marker.args[0]
    runoptions = data
    idf = AN_IDF
    idf.run(**runoptions)
    print("ran sumulation")
    return runoptions


@pytest.fixture(scope="module")
def runsimulation_old1():
    runoptions = data
    idf = AN_IDF
    idf.run(**runoptions)
    print("ran sumulation")
    return runoptions


@pytest.mark.parametrize(
    "getdict, expected",
    [
        (
            dict(
                end_file=dict(whichfile="shd", entirefile=True, table=True),
                HTML_file=dict(whichfile="htm", tableindex=0, table=True),
            ),
            {
                "HTML_file": {
                    "whichfile": "htm",
                    "tableindex": 0,
                    "table": True,
                    "entirefile": None,
                    "result": [
                        "Site and Source Energy",
                        [
                            [
                                "",
                                "Total Energy [GJ]",
                                "Energy Per Total Building Area [MJ/m2]",
                                "Energy Per Conditioned Building Area [MJ/m2]",
                            ],
                            ["Total Site Energy", 0.0, "\xa0", "\xa0"],
                            ["Net Site Energy", 0.0, "\xa0", "\xa0"],
                            ["Total Source Energy", 0.0, "\xa0", "\xa0"],
                            ["Net Source Energy", 0.0, "\xa0", "\xa0"],
                        ],
                    ],
                },
                "end_file": {
                    "whichfile": "shd",
                    "entirefile": True,
                    "table": True,
                    "result": "Shadowing Combinations\n..Solar Distribution=FullInteriorAndExterior\n..In the following, only the first 10 reference surfaces will be shown.\n..But all surfaces are used in the calculations.\n",
                },
            },
        ),  # getdict, expected
        (
            dict(
                end_file=dict(whichfile="shd", entirefile=True, table=True),
                HTML_file=dict(whichfile="htm", tableindex=0, table=True),
            ),
            {
                "HTML_file": {
                    "whichfile": "htm",
                    "tableindex": 0,
                    "table": True,
                    "entirefile": None,
                    "result": [
                        "Site and Source Energy",
                        [
                            [
                                "",
                                "Total Energy [GJ]",
                                "Energy Per Total Building Area [MJ/m2]",
                                "Energy Per Conditioned Building Area [MJ/m2]",
                            ],
                            ["Total Site Energy", 0.0, "\xa0", "\xa0"],
                            ["Net Site Energy", 0.0, "\xa0", "\xa0"],
                            ["Total Source Energy", 0.0, "\xa0", "\xa0"],
                            ["Net Source Energy", 0.0, "\xa0", "\xa0"],
                        ],
                    ],
                },
                "end_file": {
                    "whichfile": "shd",
                    "entirefile": True,
                    "table": True,
                    "result": "Shadowing Combinations\n..Solar Distribution=FullInteriorAndExterior\n..In the following, only the first 10 reference surfaces will be shown.\n..But all surfaces are used in the calculations.\n",
                },
            },
        ),  # getdict, expected
    ],
)
def test_multipleresults(resultsdir, runsimulation, getdict, expected):
    """py.test for multiple results"""
    for output_suffix in [
        "C",
    ]:  # ["C", "L", "D"]:
        runoptions = dict(output_directory=RESULT_DIR / output_suffix)
        fullresult = runandget.getrun(runoptions, getdict)
        assert fullresult == expected
        for key in fullresult:
            result = fullresult[key]["result"]
            assert result


# TODO : write runandget(, json_it=False, zip=True) -> DONE.
# pytest -> DONE
# (dict, json_it, zip) -> DONE. pytested
# TODO : write anon_runandget() ->DONE
# pytest -> DONE
# (dict, json_it, zip) -> DONE. pytested
# TODO : write an example file with main and an example notebook
# start with anonymous and then go to others.
# then do the many getdicts
# TODO : use the notebook in documentation.
# much later

# TODO : error in ../../temprget.py
# make an unit test to ensure this is tested and fixed


# def test_getrun_multiple(resultsdir, runsimulation, getdict, expected):
#     """get multiple results with getrun"""
#     runoptions = dict(output_directory=RESULT_DIR / "C")
#     result = runandget.getrun(runoptions, getdict)
#     assert result == expected


@pytest.fixture(scope="module")
def resultsdir():
    """create a results dir and teardown"""
    if not RESULT_DIR.exists():
        RESULT_DIR.mkdir()
    yield RESULT_DIR
    for folder in RESULT_DIR.iterdir():
        if folder.is_dir():
            for afile in folder.iterdir():
                afile.unlink()
            folder.rmdir()
        else:
            folder.unlink()
    RESULT_DIR.rmdir()


@pytest.fixture(scope="module")
def runsimulation():
    """Run the simulation once into results folder"""
    idf = AN_IDF
    for output_suffix in ["C", "L", "D"]:
        resultfolder = RESULT_DIR / output_suffix
        runoptions = dict(output_directory=resultfolder, readvars=True)
        idf.run(**runoptions)


# things that will not work - and have no exception handling
#
# - file does not exist
# - data in file does not exist
# - attempting json for binary data - htm and sqlite
