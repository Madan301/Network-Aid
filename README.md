# Network-Aid

This tool can be deployed on individual hosts or on a network to monitor a bunch of hosts. The tool currently has two features, the first feature is it can monitor a host to detect DDOS attack upon detection it will immediately mail a notification to the concerned person or department along with a pcap file that was captured during the DDOS attack, now this pcap file can be used for analysis to update your networks black-listed ips or to construct new set of IDS rules using the IDS_homie tool.
The second feature is that the tool can be used to monitor the network usage of a host, the limit for the network usage and other credentials such as mail_ids, API key s must be mentioned in the project.conf file. Upon the exceeding of the network usage limit by a host automatically a mail will be sent to the concerned person or department along with the information on the amount of bytes used by the host.

# Usage steps

cd Network-Aid

pip3 install requirements.txt

python3 tool.py

# Use-Case

This tool can function as a DDOS detector and preventor

The network monitoring feature of this tool can be used as an indirect detector of certain attacks on a host like crypto jacking or if a host fell victim as becoming a botnet for a DDOS campain.

(Mainly can be used to protect your cloud instances) 

# NOTE

Kindly update your project.conf file with the appropriate credentials according to your needs.
