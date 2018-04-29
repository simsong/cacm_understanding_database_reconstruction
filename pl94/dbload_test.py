import os
from dbload import *

LINE="""PLST  AK75000000  00046434902013H1  01598Z5  9999999  00010011000  9999999  9999999999999999999999999999901570E799999  9999999999999  9999999999         0000S03737-712A               999999999900007             0     107119025Block 1000                                                                                S         0        0+55.4330770-162.7240868BK       999990178553301419964019399339999999999999999999999999999999902419297                                      99                       """


def ex(desc):
    return LINE[desc[0]-1:desc[0]+desc[1]-1]

def exi(desc):
    return int(ex(desc))

def test_fields():
    assert ex(GEO_FILEID)=='PLST  '
    assert ex(GEO_STUSAB)=='AK'
    assert ex(GEO_SUMLEV)=='750'
    assert exi(GEO_SUMLEV)==750
    assert ex(GEO_LOGRECNO)=='0004643'
    assert ex(GEO_COUNTY) == '013'
    assert ex(GEO_TRACT) == '000100'
    

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
