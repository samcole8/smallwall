from datetime import datetime
from pathlib import Path
import toml
import sys

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

def load_toml(rpath, apath=get_path()):
    """Open TOML file and return dictionary"""
    try:
        with open(apath / rpath, "r") as toml_file:
            toml_dict = toml.load(toml_file)
            return toml_dict
    except (FileNotFoundError, OSError, IOError):
        log(f"FATAL: Could not open {rpath}. Check file exists and permissions are set correctly.")
        sys.exit()
    except toml.decoder.TomlDecodeError as error:
        log(f"FATAL: Could not process {rpath}: {error}")