#!/usr/bin/env python3
#
# create an SQLite3 database from PL94 data

__version__ = '0.0.1'
import datetime
import json
import os
import os.path
import re
import sqlite3
import sys

from sql import SLGSQL

CACHE_SIZE = 2000000
SQL_SET_CACHE = "PRAGMA cache_size = {};".format(CACHE_SIZE)




SQL_SCHEMA=\
    """
CREATE TABLE IF NOT EXISTS blocks (state VARCHAR(2), county INTEGER, tract INTEGER, block INTEGER, logrecno INTEGER, blockcount INTEGER, houses INTEGER);
CREATE INDEX IF NOT EXISTS blocks_idx0 ON blocks(state,county);
CREATE INDEX IF NOT EXISTS blocks_idx1 ON blocks(tract);
CREATE INDEX IF NOT EXISTS blocks_idx1 ON blocks(state,logrecno);
CREATE INDEX IF NOT EXISTS blocks_idx2 ON blocks(blockcount);
CREATE INDEX IF NOT EXISTS blocks_idx3 ON blocks(houses);
"""

GEO_FILEID=(1,6)
GEO_STUSAB=(7,2)
GEO_SUMLEV=(9,3)
GEO_LOGRECNO=(19,7)
GEO_COUNTY=(30,3)
GEO_PLACE=(46,5)            
GEO_TRACT=(55,6)            
GEO_BLKGRP=(61,1)
GEO_BLOCK=(62,4)        # first digit of block is blockgroup


def make_database(conn):
    conn.row_factory = sqlite3.Row
    conn.cursor().execute(SQL_SET_CACHE)
    SLGSQL.create_schema(conn,SQL_SCHEMA)

def load_geo_file(conn,fname):
    c = conn.cursor()
    with open(fname) as f:
        ll = 0
        for line in f:
            def ex(desc):
                return line[desc[0]-1:desc[0]+desc[1]-1]

            def exi(desc):
                return int(ex(desc))

            ll += 1
            if exi(GEO_SUMLEV) in [750,755]:
                try:
                    c.execute("INSERT INTO blocks (state,county,tract,block,logrecno) values (?,?,?,?,?)",
                              (ex(GEO_STUSAB), exi(GEO_COUNTY), exi(GEO_TRACT), exi(GEO_BLOCK), exi(GEO_LOGRECNO)))
                except ValueError as e:
                    print("{}: {}".format(ll,line))
                    raise e
    conn.commit()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compute file changes',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--db", help="Specify database location", default="data.sqlite3")
    args = parser.parse_args()

    # open database and give me a big cache
    conn = sqlite3.connect(args.db)
    make_database(conn)

