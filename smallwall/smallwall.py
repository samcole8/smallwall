import helpers
from sys import argv
import os

SMALLWALL = (
    "._______.\n"
    "|___|___|\n"
    "|_|___|_|\n"
    "|___|___|\n"
    "smallwall\n"
    )

# Relative path to configuration file
CONFIG_RPATH = "smallwall.toml"


MOUNT_RPATH = "/mnt/smallwall"
MOUNT_CONFIG_PATH = "/etc/iptables.conf"

def gen(config):

    qz = config["firewall"]["qz"]["interface"]
    lan = config["firewall"]["lan"]["interface"]
    netid_cidr = f'{config["firewall"]["lan"]["network_id"]}{config["firewall"]["lan"]["cidr"]}'
    gateway = config["firewall"]["lan"]["gateway"]

    return (
f"""#!/bin/bash

# Flush existing rules
iptables -F

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# FORWARD chain rules
iptables -A FORWARD -i {qz} -o {lan} -d {netid_cidr} -j DROP
iptables -A FORWARD -i {qz} -o {lan} -d {gateway} -j ACCEPT
iptables -A FORWARD -i {lan} -o {qz} -j ACCEPT\n"""
)

def deploy(config, device):
    # Generate iptables config file
    iptables_to_write = gen(config)
    # Overwrite iptables config file on mount
    iptables = config["filesystem"]["iptables"]
    mountpoint = config["filesystem"]["mountpoint"]
    try:
        if f'{mountpoint}{iptables}' != "/etc/iptables/rules.v4":
            os.makedirs(os.path.dirname(f"{mountpoint}{iptables}"), exist_ok=True)
            with open(f'{mountpoint}{iptables}', "w") as iptables_file:
                iptables_file.write(iptables_to_write)
            helpers.log(f'INFO: Successfully written iptables configuration to {mountpoint}{iptables}.')
    except FileNotFoundError:
        helpers.log(f'FATAL: Cannot find {mountpoint}{iptables}.')

def smallwall(device):
    print(SMALLWALL)
    # Log start
    helpers.log("INFO: Started smallwall.")
    # Load config
    config = helpers.load_toml(CONFIG_RPATH, auto_create=True, skeleton="default.toml")
    # Mount disk
    mountpoint = config["filesystem"]["mountpoint"]
    helpers.mount("m", device, mountpoint)
    # Modify iptables
    deploy(config, device)
    # Unmount disk
    helpers.mount("u", device, mountpoint)
    # Cleanup - remove mount dir

if __name__ == "__main__":
    try:
        smallwall(argv[1])
    except IndexError:
        print("Missing device name. (e.g. /dev/mmcblk0p1)")