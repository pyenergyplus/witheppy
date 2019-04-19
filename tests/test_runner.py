# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for runner.py"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

from witheppy.runner import eplaunch_run
from six.moves import reload_module as reload
from eppy.runner.run_functions import install_paths

# TODO : set path names so that it runs on any computer - DONE
# TODO : make a copy of the file in another folder
    # TODO : first just make a folder then a copy

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCES_DIR = os.path.join(THIS_DIR, os.pardir, 'witheppy/resources')

IDD_FILES = os.path.join(RESOURCES_DIR, 'iddfiles')
IDF_FILES = os.path.join(RESOURCES_DIR, 'idffiles')
try:
    VERSION = os.environ["ENERGYPLUS_INSTALL_VERSION"]  # used in CI files
except KeyError:
    VERSION = '8-9-0'  # current default for integration tests on local system
TEST_IDF_NAME = 'smallfile.idf'
TEST_IDF = "V{}/{}".format(VERSION[:3].replace('-', '_'), TEST_IDF_NAME)
TEST_EPW = 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw'
TEST_IDD = "Energy+V{}.idd".format(VERSION.replace('-', '_'))
TEST_OLD_IDD = 'Energy+V7_2_0.idd'
eplus_exe, eplus_weather = install_paths(VERSION, os.path.join(IDD_FILES, TEST_IDD))

from eppy import modeleditor
from eppy.modeleditor import IDF
reload(modeleditor)
iddfile = os.path.join(IDD_FILES, TEST_IDD)
fname1 = os.path.join(IDF_FILES, TEST_IDF)
modeleditor.IDF.setiddname(iddfile, testing=True)
idf = modeleditor.IDF(fname1, TEST_EPW)

# IDF.setiddname(iddfile)
# idf = IDF(idfname, epw=wname)

class TestEPLaunch_Run(object):
    """docstring for TestEPLaunch_Run"""
    def setup(self):
        runfolder = "runfolder"
        self.runpath = os.path.join(THIS_DIR, runfolder)
        if os.path.exists(self.runpath):
            shutil.rmtree(self.runpath)
        os.mkdir(self.runpath)
        runidffile = os.path.join(self.runpath, TEST_IDF_NAME)
        shutil.copy(fname1, runidffile)
        self.idf = modeleditor.IDF(runidffile, TEST_EPW)
        expected_files = ['{}.audit',
                         '{}.eso',
                         '{}.shd',
                         '{}.bnd',
                         '{}.idf',
                         '{}Sqlite.err',
                         '{}.eio',
                         '{}.mdd',
                         '{}Table.htm',
                         '{}.end',
                         '{}.mtd',
                         '{}.err',
                         '{}.rdd']
        self.expected_files = [expected_file.format(TEST_IDF_NAME.split(".")[0]) for expected_file in expected_files]
        print(self.expected_files)

    def test_eplaunch_run(self):
        """py.test for eplaunch_run"""
        eplaunch_run(self.idf)
        # test_idf.run(output_directory='run_outputs')
        # assert not has_severe_errors()
        files = os.listdir(self.runpath)
        assert set(files) == set(self.expected_files)
        # assert True

    def teardown(self):
        shutil.rmtree(self.runpath)

