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

from witheppy.runner import eplaunch_run
from six.moves import reload_module as reload

# TODO : just get e+ running during the test

iddname = "/Users/santoshphilip/Documents/coolshadow/github/witheppy/witheppy/resources/iddfiles/Energy+V8_9_0.idd"
idfname = "/Users/santoshphilip/Documents/coolshadow/github/witheppy/witheppy/resources/idffiles/V8_9/smallfile.idf"
wname = "/Users/santoshphilip/Documents/coolshadow/github/witheppy/witheppy/resources/weather/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"



from eppy import modeleditor
from eppy.modeleditor import IDF
reload(modeleditor)
IDF.setiddname(iddname)
idf = IDF(idfname, epw=wname)

def test_eplaunch_run():
    """py.test for eplaunch_run"""
    
    eplaunch_run(idf)
    # test_idf.run(output_directory='run_outputs')
    # assert not has_severe_errors()
    # files = os.listdir('run_outputs')
    # assert set(files) == set(self.expected_files)
    assert True
    