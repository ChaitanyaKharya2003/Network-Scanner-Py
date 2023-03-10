#/usr/bin/python
# Network Scanner
import re
import scapy.all as scapy
import subprocess

# Function to scan the network
def scan(ip):
    arp_request = scapy.ARP(pdst=ip) # ARP Packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # broadcast mac address
    req_broadcast = broadcast/arp_request # combine the two packets

    ans_list = scapy.srp(req_broadcast, timeout=1, verbose=0)[0]
    clients = []
    for ans in ans_list:
        # Store the IP and MAC address in a dictionary
        client_dict = {"ip":ans[1].psrc, "mac":ans[1].hwsrc}
        clients.append(client_dict)
    # Return the list of clients(devices connected to the network)
    return clients


# Function to print the client IP and MAC address
def resPrint(ans_list):
    print("#IP\t\t\t#MAC ADDR.")
    for ans in ans_list:
        print(ans["ip"]+"\t\t"+ans["mac"])


# Get the router IP------------------
ip_res = subprocess.check_output(["route", "-n"])
ip = re.search(r"\d\d\d.\d\d\d.\d\d\d.\d", str(ip_res))
#------------------------------------
resPrint(scan(ip.group(0) + "/24")) # Scan the subnet and Print the output
