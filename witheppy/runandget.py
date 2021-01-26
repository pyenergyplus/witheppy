# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-

"""experimental code to runa n idf and get the results"""

# things that will not work - and have no exception handling
#
# - file does not exist
# - data in file does not exist
# - attempting json for binary data - htm and sqlite

from pathlib import Path
import collections
import tempfile
import json
import bz2


from eppy.results import readhtml
from eppy.results import fasthtml
from eppy.runner.run_functions import runIDFs


# fname = "/Applications/EnergyPlus-9-3-0/ExampleFiles/1ZoneEvapCooler.idf"
# idf.run(output_suffix='L')
# idf.run(output_suffix=None)
# Thambymtr.csv
# Thambyout.audit
# Thambyout.bnd
# Thambyout.csv
# Thambyout.dxf
# Thambyout.eio
# Thambyout.end
# Thambyout.err
# Thambyout.eso
# Thambyout.mdd
# Thambyout.mtd
# Thambyout.mtr
# Thambyout.rdd
# Thambyout.rvaudit
# Thambyout.shd
# Thambytbl.htm
# Thambytbl.tab
# sqlite.err
#
#
# fname = "/Applications/EnergyPlus-9-3-0/ExampleFiles/1ZoneEvapCooler.idf"
# idf.run(output_suffix='C')
# Thamby.audit
# Thamby.bnd
# Thamby.csv
# Thamby.dxf
# Thamby.eio
# Thamby.end
# Thamby.err
# Thamby.eso
# Thamby.mdd
# Thamby.mtd
# Thamby.mtr
# Thamby.rdd
# Thamby.rvaudit
# Thamby.shd
# ThambyMeter.csv
# ThambySqlite.err
# ThambyTable.htm
# ThambyTable.tab
#
# fname = "/Applications/EnergyPlus-9-3-0/ExampleFiles/1ZoneEvapCooler.idf"
# idf.run(output_suffix='D')
# Thamby-meter.csv
# Thamby-sqlite.err
# Thamby-table.htm
# Thamby-table.tab
# Thamby.audit
# Thamby.bnd
# Thamby.csv
# Thamby.dxf
# Thamby.eio
# Thamby.end
# Thamby.err
# Thamby.eso
# Thamby.mdd
# Thamby.mtd
# Thamby.mtr
# Thamby.rdd
# Thamby.rvaudit
# Thamby.shd

d_L = {
    "mcsv": "mtr.csv",
    "audit": "out.audit",
    "bnd": "out.bnd",
    "csv": "out.csv",
    "dxf": "out.dxf",
    "eio": "out.eio",
    "end": "out.end",
    "err": "out.err",
    "eso": "out.eso",
    "mdd": "out.mdd",
    "mtd": "out.mtd",
    "mtr": "out.mtr",
    "rdd": "out.rdd",
    "shd": "out.shd",
    "htm": "tbl.htm",
    "tab": "tbl.tab",
    "sqlerr": "sqlite.err",
    "expidf": "out.expidf",
    "sql": "out.sql",
    "rvaudit": "out.rvaudit",
}

d_C = {
    "audit": ".audit",
    "bnd": ".bnd",
    "csv": ".csv",
    "dxf": ".dxf",
    "eio": ".eio",
    "end": ".end",
    "err": ".err",
    "eso": ".eso",
    "mdd": ".mdd",
    "mtd": ".mtd",
    "mtr": ".mtr",
    "rdd": ".rdd",
    "shd": ".shd",
    "mcsv": "Meter.csv",
    "sqlerr": "Sqlite.err",
    "htm": "Table.htm",
    "tab": "Table.tab",
    "expidf": ".expidf",
    "sql": ".sql",
    "rvaudit": ".rvaudit",
}

d_D = {
    "mcsv": "-meter.csv",
    "sqlerr": "-sqlite.err",
    "htm": "-table.htm",
    "tab": "-table.tab",
    "audit": ".audit",
    "bnd": ".bnd",
    "csv": ".csv",
    "dxf": ".dxf",
    "eio": ".eio",
    "end": ".end",
    "err": ".err",
    "eso": ".eso",
    "mdd": ".mdd",
    "mtd": ".mtd",
    "mtr": ".mtr",
    "rdd": ".rdd",
    "shd": ".shd",
    "expidf": ".expidf",
    "sql": ".sql",
    "rvaudit": ".rvaudit",
}

fname_endswith_dict = dict(L=d_L, C=d_C, D=d_D)


resulttypes = [
    "audit",
    "bnd",
    "dxf",
    "eio",
    "end",
    "err",
    "eso",
    "mdd",
    "mtd",
    "mtr",
    "rdd",
    "shd",
    "htm",
    "tab",
    "sqlerr",
    "csv",
    "mcsv",
    "expidf",
    "sql",
    "rvaudit",
]


def getfile(pathtofile):
    """get the result file"""
    return open(pathtofile, "r").read()


def getfilehandle(pathtofile, mode="r"):
    """return a filehandle ope for read"""
    return open(pathtofile, mode)


def options2filename(whichresult, options=None):
    """get the filename from the options.
    whichresult should be an item from resulttypes"""
    if not options:
        options = dict()
    options = collections.defaultdict(lambda: None, options)
    if not options["output_suffix"]:
        options["output_suffix"] = "L"
    if not options["output_prefix"]:
        options["output_prefix"] = "eplus"
    if not options["output_directory"]:
        options["output_directory"] = ""
    output_suffix = options["output_suffix"]
    output_prefix = options["output_prefix"]
    if whichresult == "sqlerr":  # a special case
        if output_suffix == "L":
            output_prefix = ""
    therest = fname_endswith_dict[output_suffix][whichresult]
    filename = f"{output_prefix}{therest}"
    pth = Path(filename)
    output_directory = options["output_directory"]
    pth = output_directory / pth
    return pth


def getresult(whichresult, options=None):
    """get the text of the result"""
    filepath = options2filename(whichresult, options=options)
    return getfile(filepath)


def getresulthandle(whichresult, options=None):
    """get the filehandle of the result"""
    filepath = options2filename(whichresult, options=options)
    if whichresult in ("htm", "sql"):
        return getfilehandle(filepath, mode="rb")
    else:
        return getfilehandle(filepath)


# delete
def geterr(idf, options=None):
    """get the err file"""
    fname = "eplusout.err"
    pth = Path(fname)
    fullpath = pth
    return getfile(fullpath)


getdict = dict(
    resultname=dict(
        whichfile="htm",
        entirefile=False,  # return the raw file
        tables=False,  # entire contents in tables format
        tableindex=1,  # or tablename
    )
)


def getfromhtm(fhandle, htm_options):
    """getdata from htm"""
    returndict = dict(htm_options)
    if htm_options.setdefault("as_tables", None):
        htables = readhtml.titletable(fhandle)
        returndict["result"] = [list(table) for table in htables]
        # made into a list for json conversion
        # json conversion makes it a list
        # so now testing is easier
    elif isinstance(htm_options.setdefault("tableindex", None), int):
        header, table = fasthtml.tablebyindex(fhandle, htm_options["tableindex"])
    elif htm_options.setdefault("tablename", None):
        header, table = fasthtml.tablebyname(fhandle, htm_options["tablename"])
    if htm_options.setdefault("table"):
        returndict["result"] = [header, table]
    elif htm_options.setdefault("rows"):
        irows = htm_options["rows"]
        parttable = list()
        for i in irows:
            parttable.append(table[i])
        returndict["result"] = [header, parttable]
    elif htm_options.setdefault("cols"):
        icols = htm_options["cols"]
        parttable = list()
        for row in table:
            partrow = list()
            for i in icols:
                partrow.append(row[i])
            parttable.append(partrow)
        returndict["result"] = [header, parttable]
    elif htm_options.setdefault("cells"):
        cells = htm_options["cells"]
        somecells = list()
        for cell in cells:
            somecells.append(table[cell[0]][cell[1]])
        returndict["result"] = [header, somecells]
    return returndict


def dict2json(thedict, json_it=False, compress_it=False):
    """if json_it convert thedict to json
    if compress_it, do a bzip2 compression on the json"""
    if compress_it:
        return bz2.compress(json.dumps(thedict).encode())
    elif json_it:
        return json.dumps(thedict)
    else:
        return thedict


def getrun(runoptions, getdict=None, json_it=False, compress_it=False):
    """get the results out of the run results"""
    if not getdict:
        returndict = None
        return dict2json(returndict, json_it, compress_it)
    returndict = dict(getdict)
    for key in getdict:
        thisdict = returndict[key]
        fhandle = getresulthandle(thisdict["whichfile"], runoptions)
        if thisdict.setdefault("entirefile", None):
            entirefiledata = fhandle.read()
            returndict[key]["result"] = entirefiledata
        elif thisdict["whichfile"] == "htm":
            returndict[key] = getfromhtm(fhandle, thisdict)
        elif thisdict["whichfile"] in ("csv", "mcsv"):
            col_list = thisdict["cols"]
            returndict[key]["result"] = list(getcsvcols(fhandle, col_list))
    return dict2json(returndict, json_it, compress_it)


def _col2index(row, colid):
    """get index in row from colid=index or colid=value"""
    try:
        # if colid is an index
        try:
            val = row[colid]
            return colid
        except (IndexError) as e:
            return None
    except TypeError as e:
        # if colid is not a int but a value
        try:
            return row.index(colid)
        except ValueError as e:
            return None


def _col_list2index(row, col_list):
    """return the column index from col_list"""
    return [_col2index(row, colid) for colid in col_list]


def getcsvcols(fhandle, col_list):
    """get all the columns in col_list
    col_list can be a mix of index and headers"""
    for line in fhandle:
        # header row.
        try:
            line = line.decode()
        except AttributeError as e:
            pass
        row = [cell.strip() for cell in line.split(",")]
        indices = _col_list2index(row, col_list)
        yield [row[index] for index in indices]
        break
    for line in fhandle:
        try:
            line = line.decode()
        except AttributeError as e:
            pass
        row = [cell.strip() for cell in line.split(",")]
        outrow = list()
        for index in indices:
            try:
                outrow.append(row[index])
            except IndexError as e:
                outrow.append("")
        yield outrow


def runandget(idf, runoptions, getdict, json_it=False, compress_it=False):
    """run the idf and return the results"""
    # idf.run(**runoptions)
    # idf.run() does not allow simultaeous runs. -> using runIDFs
    idfversion = idf.idfobjects["version"][0].Version_Identifier.split(".")
    idfversion.extend([0] * (3 - len(idfversion)))
    idfversionstr = "-".join([str(item) for item in idfversion])
    runoptions["ep_version"] = idfversionstr
    #
    runs = []
    runs.append([idf, runoptions])
    num_CPUs = 1
    runIDFs(runs, num_CPUs)
    return getrun(runoptions, getdict, json_it, compress_it)


def anon_runandget(idf, getdict, json_it=False, compress_it=False):
    """run the idf in a temp library and return results"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        runoptions = dict(
            output_directory=tmp_dir,
            readvars=True,
        )
        return runandget(idf, runoptions, getdict, json_it, compress_it)
