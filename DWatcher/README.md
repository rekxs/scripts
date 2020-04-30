# File Moving Script with Watch Modus

Move File Structure in Media Folder Sorted by extensions.

## Config:

On first run this script creates an Config Yaml File at 
```
$HOME/.config/dir_watcher/config.yaml	
```

The Config contains a Dictionary with the media folder name and the extensions 
to be sorted in to this folder.

Example:

|name|extensions|
|----|----------|
|text|'.INDD','.PCT','.PDF','.XLR','.XLS','.XLSX','.DOC','.DOCX','.LOG','.MSG','.ODT','.PAGES','.RTF','.TEX','.TXT','.WPD','.WPS'|

This will create the folder text inside the target Directory and move every File with the specified extension 
together with its folder sturcutre over to the text folder.

## Usage: 

```
sort_deep.py -d /path/to/scan -t /target/path [-w]
```
|Param|Description|
|-----|-----------|
|-d|Path to Directory that gets Scanned|
|-t|Target Directory, all Files will be moved here|
|-w|Start Script in Watchmode, only moves changed and new Files| 
|-h|print Usage| 

!!! Watch mode is Experimental 
Does Move Files before they are fully copied.

If you still want to use this script to Move/Sort Files. 
Use the script as a cronjob. 
!!!

TODO: Correctly Build Watch mode.
	
