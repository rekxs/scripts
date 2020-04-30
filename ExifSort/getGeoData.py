#!/usr/bin/env python

import os
import sys
import getopt
import shutil
import csv
import json
from helper/ExifTool import *


def scan_directory(dir, outfile, map):
    list = []
    with ExifTool() as e:
        metadata =  e.get_metadata_geo(dir)
        for file in metadata:
            source = file['SourceFile']


    if outfile != "":
        os.system(" ".join(['exiftool', '-gps*', '-r', dir, '-csv', '>', outfile]))

def main(argv):
    dir = ""
    outfile = ""
    map = False

    try:
        opts, args = getopt.getopt(argv,"hd:o:map")
    except Exception as e:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-d':
            dir = arg
        elif opt == '-o':
            outfile = arg
        elif opt == '-map':
            map = True

    if os.path.exists(dir):
        scan_directory(dir, outfile, map)
    else:
        print(
        """
        File Path does not exists.
        """, dir)

        usage()
        sys.exit()
#
#   Print out Usage
#
def usage():
    print("""
        #   Get Geodata from File By Metadata ( Exifdata )
        #   - Images -> Get Geodata if present
        #   - Create Location Map if wanted
    """)

    print("""
        Usage: getGeoData.py -d /path/to/scan [-o /target/path/out.csv -map]
            \t-d : Directory Path to be scanned
            \t-o : Write Geo Data to csv
            \t-map : Create Location Map
        """)



if __name__ == "__main__":
    main(sys.argv[1:])
