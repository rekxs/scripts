import os
import json
import shutil
import yaml
import sys
import getopt
import time
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

##
##  Functions
##

class Watcher:

    def __init__(self):
        self.observer = Observer()

    def watch_directory(self, path, target):
        event_handler = Handler(path, target)
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):

    path = ""
    target = ""
    extension_map = []

    def __init__(self, path, target):
        self.path = path
        self.target = target
        self.extension_map = self.load_extensions()

    def load_extensions(self):
        # get Home Path
        home = os.path.expanduser("~")
        config_dir = os.path.join(home, ".config", "dir_watcher")
        # create Folder if not exists
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)


        filename = "config.yaml"
        fullpath = os.path.join(config_dir, filename)
        if not os.path.exists(fullpath):
            self.create_config(fullpath)

        # init dictionary
        stream = open(fullpath, 'r')
        dictionary = yaml.safe_load(stream)
        return dictionary

    def create_config(self, configpath):
        print("create "+ configpath)
        dictionary = {}
        dictionary['text'] = [
               '.INDD',
               '.PCT',
               '.PDF',
               '.XLR',
               '.XLS',
               '.XLSX',
               '.DOC',
               '.DOCX',
               '.LOG',
               '.MSG',
               '.ODT',
               '.PAGES',
               '.RTF',
               '.TEX',
               '.TXT',
               '.WPD',
               '.WPS'
        ]
        dictionary['data'] = [
                '.CSV',
                '.DAT',
                '.GED',
                '.KEY',
                '.KEYCHAIN',
                '.PPS',
                '.PPT',
                '.PPTX',
                '.SDF',
                '.TAR',
                '.TAX2016',
                '.TAX2019',
                '.VCF',
                '.XML'
                ]
        dictionary['music'] = [
                '.AIF',
                '.IFF',
                '.M3U',
                '.M4A',
                '.MID',
                '.MP3',
                '.MPA',
                '.WAV',
                '.WMA'
                ]
        dictionary['video'] = [
                '.3G2',
                '.3GP',
                '.ASF',
                '.AVI',
                '.FLV',
                '.M4V',
                '.MOV',
                '.MP4',
                '.MPG',
                '.RM',
                '.SRT',
                '.SWF',
                '.VOB',
                '.WMV'
                ]
        dictionary['images'] = [
                '.3DM',
                '.3DS',
                '.MAX',
                '.OBJ',
                '.BMP',
                '.DDS',
                '.GIF',
                '.HEIC',
                '.JPG',
                '.PNG',
                '.PSD',
                '.PSPIMAGE',
                '.TGA',
                '.THM',
                '.TIF',
                '.TIFF',
                '.YUV',
                '.AI',
                '.EPS',
                '.SVG'
                ]
        dictionary['database'] = [
              '.ACCDB',
              '.DB',
                '.DBF',
               '.MDB',
               '.PDB',
               '.SQL'
               ]
        dictionary['archives'] = ['.7Z','.CBR','.DEB','.GZ','.PKG','.RAR','.RPM','.SITX','.TAR.GZ','.ZIP','.ZIPX']

        self.write_yaml_to_file(dictionary, configpath)

    # write Config to Yaml File
    def write_yaml_to_file(self, data, filepath):
        stream = open(filepath, 'w')
        yaml.dump(data, stream)


    # get Extension and name from Filepath
    def get_extension(self, file):
       name, extension = os.path.splitext(file)
       return name, extension

    # move File to New Folder
    def move(self, subfolder, filename, path, copy=False):
        folder = path.partition(self.path + "/")[2]
        newpath = os.path.join(self.target, subfolder, folder)
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        try:
            if os.path.exists(filename):
                oldfilepath = filename
            else:
                oldfilepath = os.path.join(path, filename)
            if copy:
                parts = filename.split(".")
                filename = parts[0] + "_copy_" + ".".join(parts[1:len(parts)])

            newfilepath = os.path.join(newpath, filename)
            if not os.path.exists(newfilepath):
                print("Olldpath "  + oldfilepath)
                print("Newpath "  + newfilepath)
                shutil.move(oldfilepath, newfilepath)
        except Exception as e:
            print("Ollpath "  + oldfilepath)
            print("Newpath "  + newfilepath)
            raise

    #scan directoy and move files according to Filetype
    def scan_files(self):
        count = 0

        for (path, dirs, files) in os.walk(self.path):
            for file in files:
                filename ,curr_ext = self.get_extension(file)
                for key, exts in self.extension_map.items():
                    if curr_ext.upper() in exts:
                        self.move(key, file, path)



    def on_any_event(self, event):
        if event.is_directory:
            return None
        else:

            if event.event_type == 'moved':
                new_path = event.dest_path
                if not os.path.exists(event.dest_path):
                    return
            elif event.event_type == 'deleted':
                return
            else:
                new_path = event.src_path
            name, extension = self.get_extension(new_path)
            for key, exts in self.extension_map.items():
                if extension.upper() in exts:
                    parts = new_path.split("/")
                    filename = parts[len(parts)-1]
                    path = "/".join(parts[0:len(parts)-1])
                    self.move(key, filename, path)




def main(argv):
    watch = False
    watchpath = ""
    targetpath = ""

    try:
        opts, args = getopt.getopt(argv,"hd:t:w")
    except Exception as e:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-d':
            watchpath = arg
        elif opt == '-t':
            targetpath = arg
        elif opt == '-w':
            watch = True

    if not watch:
        handler = Handler(watchpath, targetpath)
        handler.scan_files()
    else:
        watcher = Watcher()
        watcher.watch_directory(watchpath, targetpath)

def usage():
    print("Usage: sort_deep.py -d /path/to/scan -t /target/path [-w]")
    print("\t-d : Directory Path to be scanned")
    print("\t-t : Directory the Files get Moved")
    print("\t-w : Enables Watch mode - moves All new Files to Target Directory")



if __name__ == "__main__":
    main(sys.argv[1:])
