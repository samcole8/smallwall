import helpers
from sys import argv

SMALLWALL = (
    "._______."
    "|___|___|"
    "|_|___|_|"
    "|___|___|"
    "smallwall"
    )

CONFIG_RPATH = "smallwall.toml"
MOUNT_RPATH = "/mnt/smallwall"
MOUNT_CONFIG_PATH = "/etc/nftables.conf"

def gen(config):

    qz = config["firewall"]["qz"]["if"]
    lan = config["firewall"]["lan"]["if"]
    netid_cidr = f'{config["firewall"]["lan"]["id"]}/{config["firewall"]["lan"]["cidr"]}'
    gateway = config["firewall"]["lan"]["gateway"]

    print(qz, lan, netid_cidr, gateway)

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

def deploy(chroot_path, chroot_config):
    # Generate nftables config file
    nftables_to_write = gen(chroot_config)
    # Overwrite nftables config file on mount
    try:
        if f"{chroot_path}{MOUNT_CONFIG_PATH}" != "/etc/nftables":
            print(nftables_to_write)
            with open(f'{chroot_path}{MOUNT_CONFIG_PATH}', "w") as nftables_config:
                nftables_config.write(nftables_to_write)
    except FileNotFoundError:
        helpers.log(f"FATAL: Cannot find {chroot_path}{MOUNT_CONFIG_PATH}.")

def smallwall(device):
    print(SMALLWALL)
    # Log start
    helpers.log("INFO: Started smallwall.")
    # Load config
    config = helpers.load_toml(CONFIG_RPATH, auto_create=True, skeleton="default.toml")
    # Mount disk
    helpers.mount("m", device, MOUNT_RPATH)
    # Modify iptables    
    deploy(MOUNT_RPATH, config)
    # Unmount disk
    helpers.mount("u", device, MOUNT_RPATH)
    # Cleanup - remove mount dir

if __name__ == "__main__":
    try:
        smallwall(argv[1])
    except IndexError:
        print("Missing device name. (e.g. /dev/mmcblk0p1)")