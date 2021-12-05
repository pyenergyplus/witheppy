# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""needs documenatation"""

from io import StringIO
import pytest
from eppy.modeleditor import IDDAlreadySetError
from witheppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF


@pytest.fixture(scope="session")
def makeIDFfortesting():
    """make IDF for testing"""
    iddtxt = iddcurrent.iddtxt
    iddfhandle = StringIO(iddcurrent.iddtxt)
    try:
        IDF.setiddname(iddfhandle)
    except IDDAlreadySetError as e:
        pass
    return IDF
