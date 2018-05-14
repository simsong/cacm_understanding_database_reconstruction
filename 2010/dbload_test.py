import os
from dbload import *

GEO_LINE="""PLST  AK75000000  00046434902013H1  01598Z5  9999999  00010011000  9999999  9999999999999999999999999999901570E799999  9999999999999  9999999999         0000S03737-712A               999999999900007             0     107119025Block 1000                                                                                S         0        0+55.4330770-162.7240868BK       999990178553301419964019399339999999999999999999999999999999902419297                                      99                       """


PART1_LINE="""PLST,AK,000,01,0000001,710231,658356,473576,23263,104871,38135,7409,11102,51875,47286,4685,26127,6915,1095,2211,1777,530,213,409,1200,431,429,782,368,114,4181,1415,252,85,68,1103,177,233,529,67,13,50,17,47,30,5,3,60,14,3,10,361,153,21,33,24,13,1,79,14,1,12,5,4,0,0,1,47,39,8,0,0,0,0,0,0,710231,39249,670982,625614,455320,21949,102556,37459,7219,1111,45368,41711,4155,24741,6498,1028,284,1643,484,174,118,1119,395,115,730,193,34,3387,1219,217,75,18,975,164,61,448,26,6,48,17,20,25,1,2,56,3,1,5,234,117,16,11,13,2,0,65,2,0,1,5,2,0,0,0,36,36,0,0,0,0,0,0,0"""


def ex(line,desc):
    return line[desc[0]-1:desc[0]+desc[1]-1]

def exi(line,desc):
    return int(ex(desc))

def test_geo_fields():
    assert ex(GEO_LINE,GEO_FILEID)=='PLST  '
    assert ex(GEO_LINE,GEO_STUSAB)=='AK'
    assert ex(GEO_LINE,GEO_SUMLEV)=='750'
    assert exi(GEO_LINE,GEO_SUMLEV)==750
    assert ex(GEO_LINE,GEO_LOGRECNO)=='0004643'
    assert ex(GEO_LINE,GEO_COUNTY) == '013'
    assert ex(GEO_LINE,GEO_TRACT) == '000100'
    
def test_part1_fields():
    

def test_load_geo_file():
    # Test numbers taken from various places
    # We use Alaska (AK)
    fname = "ak.sqlite3"
    if os.path.exists(fname):
        os.unlink(fname)
    conn = sqlite3.connect(fname)
    make_database(conn)
    load_geo_file(conn,"data/akgeo2010.pl")

    c = conn.cursor()

    # https://www.census.gov/geo/maps-data/data/tallies/tractblock.html
    queries = [("SELECT count (distinct county) from blocks",29),
               ("select count(*) from (select distinct county,tract from blocks)",167),
               ("select count(*) from (select distinct county,tract,block from blocks)",45292),
               ]

    for (query,result) in queries:
        print("{} should be {}".format(query,result))
        c.execute(query)
        assert c.fetchone()[0]==result
