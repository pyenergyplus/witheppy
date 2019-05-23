# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""read and save idf files without using eppy"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def removecomment(astr, cphrase):
    """
    the comment is similar to that in python.
    any charachter after the # is treated as a comment
    until the end of the line
    astr is the string to be de-commented
    cphrase is the comment phrase"""
    # linesep = mylib3.getlinesep(astr)
    alist = astr.splitlines()
    for i in range(len(alist)):
        alist1 = alist[i].split(cphrase)
        alist[i] = alist1[0]

    # return string.join(alist, linesep)
    return '\n'.join(alist)

def readrawidf(fhandle):
    """read the idf file as a dict. Dict keys are idfobjkeys, dict values are list in list"""
    astr = fhandle.read()
    nocom = removecomment(astr, '!')
    idfst = nocom
    scount = 0
    alist = idfst.split(';')
    rawidf = {}
    for element in alist:
        lst = element.split(',')
        lst = [item.strip() for item in lst]
        key = lst[0].strip().upper()
        if not key:
            continue
        rawidf.setdefault(key, [])
        rawidf[key].append(lst)
    return rawidf

def rawidf2str(rawidf, order=None): # rname var rawidf -> potential nameclash
    """string rep of rawidf"""
    lst = []
    if order:
        keys = order
    else:
        keys = rawidf.keys()
    for key in keys:
        try:
            for vals in rawidf[key]:
                lst.append('{},'.format(key))
                for val in vals[1:]:
                    lst.append('     {},'.format(val))
                lst.pop(-1)
                lst.append('    {};'.format(val))
                lst.append('')
        except KeyError as e:
            continue
    return '\n'.join(lst)


