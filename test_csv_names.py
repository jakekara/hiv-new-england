#
# test that CSVs in data/atlas are named properly
# according to the following convention.
#
# They have three segments, A, B and C in the form:
#
#     A-B-C.csv
#
# A is the geography  level [us, state, county];
#
# B is the indicator [prev, newdx] for prevalence or
# new diagnoses;
# 
# C is the subgroup category:
# [overall, race, race-gender, transmission-overall,
#  transmission-race]
#
# To just print errors, run:
#     $ python test_csv_names.py | grep ERROR
#
# To see all output, don't pipe to grep.
#

import os

SUCCESS = 0
FAILURE = 1
atlas_dir = os.path.join("data","atlas")
levels = ["us","state","county"]
indicators = ["prev","newdx"]
subgroups = ["overall","race","race-gender",
             "transmission-overall","transmission-race"]

def fname(a, b, c):

    """ Form a file CSV name """
    return "-".join([a, b, c]) + ".csv"

def describe(fpath):

    f = open(fpath, "r")
    # Skip the first line
    f.readline()

    # Print the start of the second line
    line = f.readline()
    print (line[:77] + "...")

    return [ x.strip() for x in line.split("|")]

def test_subgroup(c, arr):

    subgroups = {
        "overall":["All races/ethnicities","Both sexes","All transmission categories"],
        "race":["Black/African American"],
        "race-gender":["Black/African American","Male"],
        "transmission-overall":["All races/ethnicities","Both sexes","Injection drug use"],
        "transmission-race":["Black/African American","Both sexes","Injection drug use"]
    }

    terms = subgroups[c]
    for term in terms:
        if term not in arr:
            print ("ERROR: Subgroup not found: " + term)
            return FAILURE
        else:
            print ("SUCCESS: Subgroup found: " + term)
        
    
    return SUCCESS
    

def test_geography(a, arr):

    """ Check if the expected geography is in the array """

    geographies = {
        "us":"United States",
        "state":"Connecticut",
        "county":"Litchfield County, CT"
    }

    if geographies[a] not in arr:
        print ("ERROR: Expected geography (" + geographies[a] + ") not found!")
        return FAILURE
    else:
        print ("SUCCESS: Geography found")
        return SUCCESS


def test_title(b, arr):

    """ Check that the file has an expected title (arr[0]) """
    
    titles = {
        "prev":"HIV prevalence",
        "newdx":"HIV diagnoses" 
    }

    if arr[0] != "Title: " + titles[b]:
        print "ERROR: title mismatch!!"
        return FAILURE
    else:
        print "SUCCESS: title OK"
        return SUCCESS

def test_fname(a, b, c):
    """ Test a given CSV """
    
    file_name = fname(a, b, c)
    path = os.path.join(atlas_dir, file_name)

    if not os.path.exists(path): return

    print 
    print (file_name)
    arr = describe(path)
    test_geography(a, arr)
    test_title(b, arr)
    test_subgroup(c, arr)

    
    

for l in levels:
    for i in indicators:
        for s in subgroups:
            test_fname(l, i, s)
            
