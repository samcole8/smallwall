import helpers
from sys import argv

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
MOUNT_CONFIG_PATH = "/etc/nftables.conf"

def gen(config):

    qz = config["firewall"]["qz"]["interface"]
    lan = config["firewall"]["lan"]["interface"]
    netid_cidr = f'{config["firewall"]["lan"]["network_id"]}{config["firewall"]["lan"]["cidr"]}'
    gateway = config["firewall"]["lan"]["gateway"]

    return (
        "#!/usr/sbin/nft -f\n"
        "\n"
        "flush ruleset\n"
        "\n"
        "table inet smallwall {\n"
        "    chain input {\n"
        "        type filter hook input priority 0; policy drop;\n"
        "    }\n"
        "\n"
        "    chain forward {\n"
        "        type filter hook forward priority 0; policy drop;\n"
        f'        iifname "{qz}" oifname "{lan}" ip daddr { netid_cidr } drop\n'
        f'        iifname "{qz}" oifname "{lan}" ip daddr { gateway } accept\n'
        f'        iifname "{lan}" oifname "{qz}" ip saddr { gateway } accept\n'
        "    }\n"
        "\n"
        "    chain output {\n"
        "        type filter hook output priority 0; policy drop;\n"
        "    }\n"
        "}\n"
    )

def deploy(config):
    # Generate nftables config file
    nftables_to_write = gen(config)
    # Overwrite nftables config file on mount
    try:
        if f'{config["filesystem"]["mountpoint"]}{config["filesystem"]["nftables"]}' != "/etc/nftables":
            with open(f'{config["filesystem"]["mountpoint"]}{config["filesystem"]["nftables"]}', "w") as nftables_config:
                nftables_config.write(nftables_to_write)
            helpers.log(f'INFO: Successfully written nftables configuration to {config["filesystem"]["mountpoint"]}{config["filesystem"]["nftables"]}.')
    except FileNotFoundError:
        helpers.log(f'FATAL: Cannot find {config["filesystem"]["mountpoint"]}{config["filesystem"]["nftables"]}.')

def smallwall(device):
    print(SMALLWALL)
    # Log start
    helpers.log("INFO: Started smallwall.")
    # Load config
    config = helpers.load_toml(CONFIG_RPATH, auto_create=True, skeleton="default.toml")
    # Mount disk
    helpers.mount("m", device, config["filesystem"]["mountpoint"])
    # Modify iptables
    deploy(config)
    # Unmount disk
    helpers.mount("u", device, config["filesystem"]["mountpoint"])
    # Cleanup - remove mount dir

if __name__ == "__main__":
    try:
        smallwall(argv[1])
    except IndexError:
        print("Missing device name. (e.g. /dev/mmcblk0p1)")