#!/usr/bin/env python
#
#   Sort File By Metadata ( Exifdata )
#   - Images -> Create date year/month
#   - Videos -> Genre/Name/Season
#   - Music -> Genre/Interpret/Album
#
#
import os
import sys
import getopt
import shutil
from helper/ExifTool import *

# Sort Images into year/month folder structure
def handleImages(dir, target, copy):
    command = "exiftool"
    if copy:
        command = "exiftool -o ."

    tags = "'-directory<filemodifydate' '-Directory<CreateDate'"
    d = "-d"
    format = "/".join([dir, "%Y", "%m"])
    r = "-r"
    cmd = " ".join([command, tags, d, format, r, target])
    os.system(cmd)

# sort Music in Genre/Artist/Album Structure
def handleMusic(dir, target, copy):

    with ExifTool() as e:
        metadata = e.get_metadata_rec(dir)
        for file in metadata:
            if 'MIMEType' in file:
                mtype = file['MIMEType']
                parts = mtype.split('/')
                if parts[0] == 'image':
                    continue
            # get SourceFile
            if 'SourceFile' in file:
                source = file['SourceFile']
            else:
                continue
            # get Genre
            if 'Genre' in file:
                genre = "-".join(file['Genre'].split('/'))
            elif 'ProviderStyle' in file:
                genre = "-".join(file['ProviderStyle'].split('/'))
            elif 'GenreID' in file:
                genre = file['GenreID'].split('|')[1]
            else:
                genre = 'UnknownGenre'
            # Artist
            if 'Artist' in file:
                artist = file['Artist']
            elif 'Band' in file:
                artist = file['Band']
            elif 'AlbumArtist' in file:
                artist = file['AlbumArtist']
            elif 'Composer' in file:
                artist = file['Composer']
            else:
                artist = "UnknownArtist"

            # album
            if 'Album' in file:
                album = file['Album']
            else:
                album = 'UnknownAlbum'

            filename = file['FileName']
            newpath = "/".join([target, genre, artist, album])
            handleFile(source, newpath, filename, copy)

# sort Videos by Metadata
def handleVideos(dir, target, copy):
    print("Todo: Implement")
# move or copy file
def handleFile(source, to, filename, copy):
    fullpath = os.path.join(to, filename)
    if not os.path.exists(fullpath):
        if not os.path.exists(to):
            os.makedirs(to)
    else:
        return

    if copy:
        print("Copy "+ source + " to " + fullpath)
        shutil.copy2(source, fullpath)
    else:
        print("Move "+ source + " to " + fullpath)
        shutil.move(source, fullpath)


def main(argv):
    dir = ""
    target = ""
    mode = ""
    copy = False

    try:
        opts, args = getopt.getopt(argv,"hd:t:m:c")
    except Exception as e:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-d':
            dir = arg
        elif opt == '-t':
            target = arg
        elif opt == '-m':
            mode = arg
        elif opt == '-c':
            copy = True

    if mode == "m":
        print("mode music")
        handleMusic(dir, target, copy)
    elif mode == "v":
        print("mode videos")
        handleVideos(dir, target, copy)
    elif mode == "i":
        print("mode images")
        handleImages(dir, target, copy)
    else:
        usage()
        sys.exit(2)

#
#   Print out Usage
#
def usage():
    print("""
        #   Sort File By Metadata ( Exifdata )
        #   - Images -> Sort by Create Date "year/month"
        #   - Videos -> Sort by Genre/Name/Season
        #   - Music -> Sort by Genre/Interpret/Album
    """)

    print("""
        Usage: metaSort.py -d /path/to/scan -t /target/path -m [i|v|m]
            \t-d : Directory Path to be scanned
            \t-t : Directory the Files get Moved
            \t-m : Mode to scan in  [ i: images, v: videos, m: music]
            \t-c : Copy instead of Moving
        """)



if __name__ == "__main__":
    main(sys.argv[1:])
