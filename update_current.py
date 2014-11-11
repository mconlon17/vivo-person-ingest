#!/usr/bin/env/python

"""
    update_current.py: Update the UFCurrentEntity status for all people in VIVO. For
    each person in VIVO, determine if the person is in the position file.  If not,
    subtract current.  If so, add current.

    Version 0.1 MC 2014-08-30
     -- works as expected
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"


from datetime import datetime
from vivopeople import make_ufid_dictionary
from vivofoundation import read_csv
from vivofoundation import assert_resource_property
from vivofoundation import untag_predicate
from vivofoundation import rdf_header
from vivofoundation import rdf_footer

#   Start here

print datetime.now(), "Start"

ardf = rdf_header()
srdf = rdf_header()

vivo_ufids = make_ufid_dictionary()
print datetime.now(), "VIVO has ", len(vivo_ufids), "ufids"

#   Prepare a set of current ufids by reading the position data and adding
#   each ufid to the set

position_data = read_csv('position_data.csv')
current_ufids = set()
for row_number, row in position_data.items():
    current_ufids.add(row['UFID'])
print datetime.now(), "UF has ", len(current_ufids), "ufids on the pay list"

#   Compare each ufid in VIVO to the ufids in the set of current ufids.  If
#   current, mark as current.  If not current, subtract current

k = 0
current_uri = untag_predicate('ufVivo:UFCurrentEntity')
for ufid in vivo_ufids.keys():
    k += 1
    if k % 1000 == 0:
        print datetime.now(), k
    if ufid in current_ufids:
        ardf += assert_resource_property(vivo_ufids[ufid], 'rdf:type', current_uri)
    else:
        srdf += assert_resource_property(vivo_ufids[ufid], 'rdf:type', current_uri)

ardf += rdf_footer()
srdf += rdf_footer()

add_file = open("current_add.rdf", "w")
sub_file = open("current_sub.rdf", "w")
print >>add_file, ardf
print >>sub_file, srdf
add_file.close()
sub_file.close()
print datetime.now(), "End"
