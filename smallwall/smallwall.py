import helpers
from sys import argv

SMALLWALL = """._______.
|___|___|
|_|___|_|
|___|___|
smallwall"""

CONFIG_RPATH = "smallwall.toml"
MOUNT_RPATH = "mount"

def smallwall(device):
    # Log start
    helpers.log("INFO: Started smallwall.")
    # Load config
    config = helpers.load_toml(CONFIG_RPATH, auto_create=True, skeleton="default.toml")
    # Mount disk
    helpers.mount("m", device, MOUNT_RPATH)
    # Modify iptables

    # Unmount disk
    helpers.mount("u", device, MOUNT_RPATH)

if __name__ == "__main__":
    print(SMALLWALL)
    smallwall(argv[1])