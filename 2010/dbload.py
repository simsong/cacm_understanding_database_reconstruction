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
import time

from sql import SLGSQL

CACHE_SIZE = -1024              # negative nubmer = multiple of 1024. So this is a 1MB cache.
SQL_SET_CACHE = "PRAGMA cache_size = {};".format(CACHE_SIZE)

SQL_SCHEMA=\
    """
CREATE TABLE IF NOT EXISTS blocks (state VARCHAR(2), county INTEGER, tract INTEGER, block INTEGER, logrecno INTEGER, pop INTEGER, houses INTEGER, occupied INTEGER);
CREATE UNIQUE INDEX IF NOT EXISTS blocks_idx0 ON blocks(state,logrecno);
CREATE UNIQUE INDEX IF NOT EXISTS blocks_idx2 ON blocks(state,county,tract,block);
CREATE INDEX IF NOT EXISTS blocks_idx3 ON blocks(tract);
CREATE INDEX IF NOT EXISTS blocks_idx4 ON blocks(pop);
CREATE INDEX IF NOT EXISTS blocks_idx5 ON blocks(houses);
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

DEBUG_BLOCK=None


def make_database(conn):
    conn.row_factory = sqlite3.Row
    conn.cursor().execute(SQL_SET_CACHE)
    SLGSQL.create_schema(conn,SQL_SCHEMA)

def decode_geo_line(conn,c,line):
    """Decode the hiearchical geography lines. These must be done before the other files are read
    to get the logrecno."""
    def ex(desc):
        return line[desc[0]-1:desc[0]+desc[1]-1]
    def exi(desc):
        return int(ex(desc))
    if exi(GEO_SUMLEV) in [750]:
        try:
            if DEBUG_BLOCK and exi(GEO_BLOCK)==DEBUG_BLOCK:
                print("INSERT INTO blocks (state,county,tract,block,logrecno) values ({},{},{},{},{})".format(
                    ex(GEO_STUSAB), exi(GEO_COUNTY), exi(GEO_TRACT), exi(GEO_BLOCK), exi(GEO_LOGRECNO)))
            c.execute("INSERT INTO blocks (state,county,tract,block,logrecno) values (?,?,?,?,?)",
                      (ex(GEO_STUSAB), exi(GEO_COUNTY), exi(GEO_TRACT), exi(GEO_BLOCK), exi(GEO_LOGRECNO)))
        except sqlite3.IntegrityError as e:
            conn.commit()          # save where we are
            print("INSERT INTO blocks (state,county,tract,block,logrecno) values ({},{},{},{},{})".format(
                ex(GEO_STUSAB), exi(GEO_COUNTY), exi(GEO_TRACT), exi(GEO_BLOCK), exi(GEO_LOGRECNO)))
            raise e
            

def decode_12010(conn,c,line):
    """Update the database for a line. Note that the logical record number may not be in the DB, because this line may not be for a block"""
    fields = line.split(",")
    (fileid,stusab,chariter,cifsn,logrecno,p0010001) = fields[0:6]
    assert fileid=='PLST'
    c.execute("UPDATE blocks set pop=? where state=? and logrecno=?",
              (p0010001,stusab,logrecno))

def decode_22010(conn,c,line):
    """Update the database for a line. Note that the logical record number may not be in the DB, because this line may not be for a block"""
    fields = line.split(",")
    (fileid,stusab,chariter,cifsn,logrecno) = fields[0:5]
    (h0010001,h0010002,h0010003) = fields[-3:]
    assert fileid=='PLST'
    c.execute("UPDATE blocks set houses=?,occupied=? where state=? and logrecno=?",
              (h0010001,h0010002,stusab,logrecno))

def load_file(conn,fname,func):
    print("starting {}".format(fname))
    t0 = time.time()
    ll = 0
    with open(fname,encoding='latin1') as f:
        c = conn.cursor()
        for line in f:
            #print(line)
            try:
                func(conn,c,line)
            except ValueError as e:
                print("{}: {}".format(ll,line))
                raise e
            ll += 1
            if ll%10000==0:
                print("{}...".format(ll),end='')
                sys.stdout.flush()
        conn.commit()
    t1 = time.time()
    print("Finished {}; {:,.0f} lines/sec".format(fname,ll/(t1-t0)))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compute file changes',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--db", help="Specify database location", default="data.sqlite3")
    parser.add_argument("files", help="Files to ingest", nargs="*")
    args = parser.parse_args()

    # open database and give me a big cache
    conn = sqlite3.connect(args.db)
    make_database(conn)
    for fname in args.files:
        (path,name) = os.path.split(fname)
        if name[2:]=='geo2010.pl':
            load_file(conn,fname,decode_geo_line)
        elif name[2:]=='000012010.pl':
            load_file(conn,fname,decode_12010)
        elif name[2:]=='000022010.pl':
            load_file(conn,fname,decode_22010)
        else:
            raise RuntimeError("Unknown file type: {}".format(fname))
