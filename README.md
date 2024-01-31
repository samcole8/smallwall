# smallwall

![](https://img.shields.io/badge/status-under%20development-orange)

*This project is currently under development and may not function as expected.*

smallwall is a configuration deployment tool for transparent firewalls. Using IP-based filtering to quarantine an internet-facing device, smallwall provides an alternative in situations where DMZ isn't available.

With immutability in mind, this tool configures Ubuntu on a removable disk, without the need for further configuration.

## Behaviour

smallwall follows the principle of least privilege:

- smallwall will **drop** QZ packets into the LAN unless they are destined outside of the LAN.
- smallwall will **drop** LAN packets into the QZ unless they come from the default gateway.
- smallwall will **drop** broadcast and multicast packets in either direction.

![](https://github.com/samcole8/smallwall/blob/master/smallwall.drawio.png?raw=true)

## Usage

Assuming `smallwall.toml` has been correctly modified, the following command will deploy the configuration:

`sudo python3 smallwall.py /dev/disk_id`
