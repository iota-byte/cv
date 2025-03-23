from scapy.all import sniff, IP, UDP, TCP, DNS, DNSQR, DNSRR, send
import subprocess
import logging
import time
import threading
import socket

# Set up logging to track blocked packets
logging.basicConfig(filename='firewall_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# List of known ad-serving domains (you can extend this list)
ad_domains = [
    "googlevideo.com",
    "ytimg.com",
    "doubleclick.net",
    "ads.youtube.com",
    "ads.google.com"
    "adservice.google.com",
    "pagead2.googlesyndication.com",
    "static.doubleclick.net"
]

# Function to load blocked IPs from a file into a set for fast lookups
def load_blocked_ips(file_path):
    with open(file_path, 'r') as file:
        # Read IPs and strip any extra spaces/newlines, then store them in a set for faster lookup
        blocked_ips = {line.strip() for line in file.readlines()}
    return blocked_ips

# Load the IPs into the script from the file (assuming the file is 'blocked_ips.txt')
blocked_ips = load_blocked_ips('blocked_ips.txt')

# Define the allowed ports (example: HTTP, HTTPS, SSH, etc.)
allowed_ports = [
    80,    # HTTP
    443,   # HTTPS
    22,    # SSH
    53,    # DNS (for DNS queries, but we block DNS for ads later)
    3306,  # MySQL
    8080,  # HTTP Alternate
]  # Modify this list as needed

# Function to block an IP using Windows Firewall (example for Windows)
def block_ip(ip_address):
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockIP", 
                    "dir=in", "action=block", "remoteip=" + ip_address])
    logging.info(f"Blocked IP: {ip_address}")

# Function to check if a domain is in the ad block list
def is_ad_domain(domain):
    return domain in ad_domains

# Function to block DNS queries for known ad domains
def block_dns_advertisements(packet):
    if packet.haslayer(DNSQR):  # Check if the packet contains a DNS query
        queried_domain = packet[DNSQR].qname.decode('utf-8')  # Extract the domain name from the query

        if is_ad_domain(queried_domain):
            print(f"Blocking DNS query for {queried_domain}")  # Log the blocked domain
            # Create a fake DNS response to block the query (send a fake IP like 0.0.0.0)
            dns_response = IP(src=packet[IP].dst, dst=packet[IP].src) / \
                           UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) / \
                           DNS(id=packet[DNS].id, qr=1, aa=1, qd=packet[DNSQR], ancount=1) / \
                           DNSRR(rrname=queried_domain, rdata="0.0.0.0")
            send(dns_response, verbose=0)  # Send fake DNS response
            return  # Block further processing of this packet

        # Allow DNS packets that are not ad-related (just forward them)
        print(f"Allowing DNS query for {queried_domain}")

# Function to capture packets and block based on conditions
def packet_callback(packet):
    if IP in packet:  # Check if the packet contains an IP layer
        src_ip = packet[IP].src
        
        # Block packets from specific IPs (if in blocked IP list)
        if src_ip in blocked_ips:
            logging.info(f"Blocked packet from {src_ip}")  # Log the blocked packet
            return  # Discard the packet (don't forward it)

        # If the packet is a DNS query, attempt to block ad-serving domains
        if UDP in packet and packet[UDP].dport == 53:  # DNS query
            block_dns_advertisements(packet)
        
        # If the packet has a TCP layer, check the destination port
        if TCP in packet:
            dport = packet[TCP].dport  # Get the destination port
            
            # If the destination port is not in the allowed list, block the packet
            if dport not in allowed_ports:
                logging.info(f"Blocked packet from {src_ip} to port {dport}")  # Log blocked packet
                return  # Discard the packet (don't forward it)
            
            # If it's an allowed port, permit the packet
            print(f"Permitting packet from {src_ip} to port {dport}")
            print(packet.summary())  # Print packet summary

# Start sniffing packets with the callback function
sniff(prn=packet_callback, store=0)

