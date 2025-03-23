import socket
from smb.SMBConnection import SMBConnection
from scapy.all import sr1, IP, ICMP, TCP

# Function for Ping Scan (ICMP)
def ping_host(host):
    packet = IP(dst=host)/ICMP()
    response = sr1(packet, timeout=1, verbose=0)
    if response is not None:
        return True
    else:
        return False

# Function for Port Scanning
def scan_ports(host):
    open_ports = []
    ports = [139, 445]  # Common SMB ports
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

# Function for SMB Enumeration
def smb_enum(host, username="", password=""):
    try:
        conn = SMBConnection(username, password, "", "", use_ntlm_v2=True)
        conn.connect(host, 445)
        shares = conn.listShares()
        print(f"Shares on {host}:")
        for share in shares:
            print(share.name)
        conn.close()
    except Exception as e:
        print(f"Failed to connect to SMB on {host}: {e}")

# Main function
def main():
    target_ip = input("Enter target IP: ")
    
    # Check if host is alive
    if ping_host(target_ip):
        print(f"{target_ip} is alive!")
        
        # Scan for SMB ports
        open_ports = scan_ports(target_ip)
        if open_ports:
            print(f"Open SMB ports on {target_ip}: {open_ports}")
            
            # Attempt SMB enumeration
            smb_enum(target_ip)
        else:
            print("No SMB ports open.")
    else:
        print(f"{target_ip} is not reachable.")

main()