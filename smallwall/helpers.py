from datetime import datetime
from pathlib import Path
from shutil import copyfile
import os
import toml
import sys
import sh

def get_path():
    """Return absolute file path"""
    return Path(__file__).parent

def log(message, logfile="smallwall.log", log=True):
    """Write message to log"""
    if log == True:
        try:
            with open(logfile, "a") as log:
                print(message)
                log.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " | " + message + "\n")
        except (FileNotFoundError, OSError, IOError):
            print("ERROR: Could not open log file. Check permissions are set correctly.")

def load_toml(rpath, apath=get_path(), auto_create=False, skeleton=False):
    """Open TOML file and return dictionary"""
    fpath = apath / rpath
    if not os.path.exists(rpath) and auto_create == True:
        if skeleton != False:
            copyfile(skeleton, rpath)
            log(f"INFO: {rpath} not found. Cloned from {skeleton}.")
        else:
            with open("rpath", "w") as file:
                file.write()
                log(f"INFO: {rpath} not found. File has been created.")
    try:
        with open(fpath, "r") as toml_file:
            toml_dict = toml.load(toml_file)
            log(f"INFO: Successfully loaded {fpath}.")
            return toml_dict
    except (FileNotFoundError, OSError, IOError):
        log(f"FATAL: Could not open {fpath}. Check file exists and permissions are set correctly.")
        sys.exit()
    except toml.decoder.TomlDecodeError as error:
        log(f"FATAL: Could not process {fpath}: {error}")

def mount(operation, device, mount_rpath):
    """Mount or unmount the specified disk"""
    mount_fpath = get_path() / mount_rpath
    if operation == "m":
        try:
            sh.mount(device, mount_rpath)
            log(f"INFO: Successfully mounted {device} on {mount_fpath}.")
        except sh.ErrorReturnCode_32:
            log("FATAL: This program must be run as root.")
    elif operation == "u":
        sh.umount(mount_rpath)
        log(f"INFO: Successfully umounted {mount_fpath}.")