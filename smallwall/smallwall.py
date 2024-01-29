import helpers

SMALLWALL = """._______.
|___|___|
|_|___|_|
|___|___|
smallwall"""

CONFIG_RPATH = "smallwall.py"


def smallwall():
    # Log start
    helpers.log("INFO: Started smallwall.")
    # Load config
    config = helpers.load_toml(CONFIG_RPATH)
    # Mount disk
    # Modify iptables
    # Unmount disk

if __name__ == "__main__":
    print(SMALLWALL)
    smallwall()