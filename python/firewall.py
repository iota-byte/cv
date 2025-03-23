from scapy.all import sniff, IP, TCP
import subprocess
import logging
import time
import threading

# Set up logging to track blocked packets
logging.basicConfig(filename='firewall_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

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
    20,    # FTP Data Transfer (FTP)
    21,    # FTP Control (FTP)
    22,    # SSH (Secure Shell)
    23,    # Telnet
    25,    # SMTP (Simple Mail Transfer Protocol)
    53,    # DNS (Domain Name System)
    67,    # DHCP Server
    68,    # DHCP Client
    80,    # HTTP (HyperText Transfer Protocol)
    110,   # POP3 (Post Office Protocol)
    443,   # HTTPS (Secure HTTP)
    445,   # Microsoft-DS (Windows File Sharing)
    3306,  # MySQL Database
    3389,  # Remote Desktop Protocol (RDP)
    5900,  # VNC (Virtual Network Computing)
    8080,  # HTTP Alternative (often used for proxy servers)
    8888,  # HTTP Alternative (commonly used for local dev servers)
    49152, # Dynamic Windows Ports
    49153,
    49154,
    49155,
]  # Add or remove ports as needed

# Function to block an IP using Windows Firewall (example for Windows)
def block_ip(ip_address):
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockIP", 
                    "dir=in", "action=block", "remoteip=" + ip_address])
    logging.info(f"Blocked IP: {ip_address}")

# Function to periodically reload blocked IPs from the file (reload every 24 hours)
def periodic_reload_ips():
    global blocked_ips
    while True:
        blocked_ips = load_blocked_ips('blocked_ips.txt')  # Reload the IPs from the file
        print("Blocked IPs reloaded.")
        time.sleep(86400)  # Reload every 24 hours (86400 seconds)

# Start a separate thread to reload the blocked IPs every 24 hours
reload_thread = threading.Thread(target=periodic_reload_ips)
reload_thread.daemon = True  # Run in the background
reload_thread.start()

# The main callback function that processes sniffed packets
def packet_callback(packet):
    # Check if the packet has an IP layer
    if IP in packet:
        src_ip = packet[IP].src
        
        # If the source IP is in the blocked IP list, log and discard the packet
        if src_ip in blocked_ips:
            logging.info(f"Blocked packet from {src_ip}")  # Log the blocked packet
            return  # Discard the packet (don't forward it)
        
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
        else:
            # If it's not a TCP packet, just print the summary
            print(packet.summary())

# Start sniffing packets with the callback function
sniff(prn=packet_callback, store=0)
