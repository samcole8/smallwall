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

def log(message, file="smallwall.log"):
    """Write message to log"""
    try:
        with open(file, "a") as log:
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
        sys.exit()

def mount(operation, device, mountpoint):
    if os.geteuid() != 0:
        log("FATAL: This script must run as root.")
        sys.exit()
    """Mount or unmount the specified disk"""
    mount_fpath = get_path() / mountpoint
    if operation == "m":
        try:
            try:
                sh.mkdir (mountpoint)
            except sh.ErrorReturnCode_1:
                pass
            sh.mount(device, mountpoint)
            log(f"INFO: Successfully mounted {device} on {mount_fpath}.")
        except sh.ErrorReturnCode_32:
            log(f"FATAL: The filesystem '{device}' could not be mounted.")
            sys.exit()
    elif operation == "u":
        sh.umount(mountpoint)
        log(f"INFO: Successfully umounted {mount_fpath}.")