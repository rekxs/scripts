# Sort Scripts using Exifdata 

## metaSort Sort Files By Metadata ( Exifdata )

   
Can run in three different modes.

Usage: 
```
metaSort.py -d /path/to/scan -t /target/path -m [i|v|m]
```
|Param|Description|
|-----|-----------|
|-d|Directory Path to be scanned|
|-t|Directory the Files get Moved|
|-m|Mode to scan in  [ i: images, v: videos, m: music]|
|-c|Copy instead of Moving|
|-h|Print Usage and Params|

###   - Images -> Sort by Create Date "year/month"

Move/Copy Images into Year/month File Structure

Uses CreateDate if this is absent filemodifydate will be used.

If this is the only Function you need, you can use the exiftool command alone:

Move:
```
$ exiftool '-directory<filemodifydate' '-Directory<CreateDate' -d /target/path/%Y/%m -r /path/to/images 
```
Copy:
```
$ exiftool -o . '-directory<filemodifydate' '-Directory<CreateDate' -d /target/path/%Y/%m -r /path/to/images 
```

###   - Music -> Sort by Genre/Interpret/Album

Move/Copy all Music Files from Directory into "target/Genre/Artist/Album/file" structure.

Fallback if no Metadata present -> /target/UnknownGenre/UnknownArtist/UnknownAlbum/file

###   - Videos -> Sort by Genre/Name/Season

Not yet Implemented.

TODO: Implement

## getGeoData - Get GPS Data from Images

Load GPS Exifdata from Images. 

Target is to create an Map from the Longitude and Latitude data that
shows where you have been taking Images. 

Problem -> not that much Images with GPSLongitude and GPSLatitude present. 

TODO: Implement function to Create Map with GPS Points

Usage:
```
getGeoData.py -d /path/to/scan [-o /target/path/out.csv -map]
```

|Param|Description|
|-----|-----------|
|-d|Directory Path to be scanned|
|-o|Write Geo Data to Csv|
|-map|Create Location Map|
|-h|Print Usage|
 
