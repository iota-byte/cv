import os
import threading
from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
import time

# Create packets directory if it doesn't exist
packets_dir = "packets"
os.makedirs(packets_dir, exist_ok=True)
mine_dir =  "mine"
os.makedirs(mine_dir, exist_ok=True)
# Dictionary to track unique communications between IP addresses
connections = defaultdict(lambda: {'packets': 0, 'bytes': 0, 'protocol': None})
unique_ips = set()  # To store unique IPs
stream_to_follow = {'src_ip': None, 'dst_ip': None, 'protocol': None}
tcp_streams = defaultdict(list)  # To hold TCP streams
my_ip = "192.168.159.72"



def packet_capture(interface="Wireless LAN adapter Wi-Fi"):
    def packet_callback(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Assuming your computer's IP is stored in `my_ip`
            my_ip = "192.168.159.72"  
            if TCP in packet:
                protocol = "TCP"
                payload = bytes(packet[TCP].payload)
                # Store TCP stream packets
                tcp_streams[(src_ip, dst_ip)].append(payload)
            elif UDP in packet:
                protocol = "UDP"
                payload = bytes(packet[UDP].payload) if UDP in packet else b''
            else:
                protocol = "Other"
                payload = b''

            # Track unique IPs
            unique_ips.add(src_ip)
            unique_ips.add(dst_ip)

            # Track the connection details
            connections[(src_ip, dst_ip, protocol)]['packets'] += 1
            connections[(src_ip, dst_ip, protocol)]['bytes'] += len(packet)
            connections[(src_ip, dst_ip, protocol)]['protocol'] = protocol

            # Save the captured packet to a .txt file if it involves your computer's IP
            if src_ip == my_ip or dst_ip == my_ip:
                packet_file = os.path.join(mine_dir, f"{int(time.time())}_{src_ip}_{dst_ip}.txt")
                with open(packet_file, 'w', encoding='utf-8', errors='replace') as f:  # Use replace for encoding errors
                    f.write(f"Source IP: {src_ip}\n")
                    f.write(f"Destination IP: {dst_ip}\n")
                    f.write(f"Protocol: {protocol}\n")
                    # Attempt to decode payload, replace invalid characters
                    payload_str = payload.decode('utf-8', errors='replace')
                    f.write(f"Payload: {payload_str}\n")
                    f.write("-" * 50 + "\n")

                print(f"Packet saved to mine: {packet_file}")  # Debug statement

    print("Starting packet capture...")
    if interface:
        print(f"Using interface: {interface}")  # Debug statement
    else:
        print("No interface specified.")  # Debug statement

    sniff(iface=interface, prn=packet_callback, store=False)


# Function to analyze the stored packets
def analyze_packets():
    print("\nAnalyzing stored packets...\n")
    packet_files = os.listdir(packets_dir)
    if not packet_files:
        print("No packets to analyze.")
        return

    unique_combinations = set()  # To store unique (src, dst) combinations

    for packet_file in packet_files:
        file_path = os.path.join(packets_dir, packet_file)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.readlines()
            # Extract relevant information
            src_ip = content[0].strip().split(": ")[1]
            dst_ip = content[1].strip().split(": ")[1]
            protocol = content[2].strip().split(": ")[1]
            payload = content[3].strip() if len(content) > 3 else ""

            # Create a unique key for the (src, dst) combination
            key = (src_ip, dst_ip)

            # Only print if this combination has not been seen before
            if key not in unique_combinations:
                unique_combinations.add(key)

                # Print the details in a structured format
                print(f"Source IP: {src_ip}")
                print(f"Destination IP: {dst_ip}")
                print(f"Protocol: {protocol}")
                print("Payload:")
                
                # Check if the payload is non-empty
                if payload:
                    print(payload)
                else:
                    print("No payload available.")
                
                print("-" * 50)  # Separator for readability



# Function to follow a TCP stream between two IPs after the user selects
def follow_selected_stream():
    print("\nWaiting for stream selection...")
    while True:
        if stream_to_follow['src_ip'] and stream_to_follow['dst_ip']:
            src_ip = stream_to_follow['src_ip']
            dst_ip = stream_to_follow['dst_ip']
            protocol = stream_to_follow['protocol']

            print(f"\nFollowing stream between {src_ip} and {dst_ip} using {protocol}...\n")
            
            # Display the complete TCP stream
            if (src_ip, dst_ip) in tcp_streams:
                stream_data = tcp_streams[(src_ip, dst_ip)]
                for i, payload in enumerate(stream_data[:10]):  # Limit to first 10 packets
                    try:
                        payload_str = payload.decode('utf-8', errors='replace')
                        print(f"Packet {i + 1}:")
                        print(payload_str)
                        print("-" * 50)  # Separator for readability
                    except Exception as e:
                        print(f"Error decoding packet {i + 1}: {e}")
            else:
                print("No TCP stream found for the selected IPs.")

            break

# Function to ask the user which stream to follow
def choose_stream():
    while True:
        # Display available connections
        print("\nAvailable IP communications:")
        for (src, dst, protocol), data in connections.items():
            print(f"{src} -> {dst} | Protocol: {protocol} | Packets: {data['packets']} | Bytes: {data['bytes']}")

        # Prompt for stream selection
        follow = input("\nDo you want to follow any communication stream? (yes/no): ").lower()
        if follow == "yes":
            # Display unique source IPs
            available_src_ips = set(src for src, _, _ in connections.keys())
            print("\nAvailable Source IPs:")
            for ip in available_src_ips:
                print(ip)

            src_ip = input("Enter the source IP: ")
            dst_ip = input("Enter the destination IP: ")
            protocol = input("Enter the protocol (TCP/UDP): ").upper()

            # Validate input
            if (src_ip, dst_ip, protocol) in connections:
                stream_to_follow['src_ip'] = src_ip
                stream_to_follow['dst_ip'] = dst_ip
                stream_to_follow['protocol'] = protocol
                break  # Exit the loop after valid selection
            else:
                print("Invalid stream selection. Please try again.")
        elif follow == "no":
            print("No stream selected. Analyzing stored packets...")
            analyze_packets()  # Analyze packets after user says "no"
            return  # Exit the function to stop prompting for streams
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# Main function to initiate threads
if __name__ == "__main__":
    try:
        # Start the packet capture thread
        capture_thread = threading.Thread(target=packet_capture, args=("Wi-Fi",))  # Specify your interface here
        capture_thread.daemon = True  # Set as daemon so it exits on script termination
        capture_thread.start()

        # Continuous stream following logic
        while True:
            choose_stream()  # Prompt user to choose a stream

            # Start the stream-following thread after user selects
            if stream_to_follow['src_ip'] and stream_to_follow['dst_ip']:  # Only follow if a stream was selected
                stream_thread = threading.Thread(target=follow_selected_stream)
                stream_thread.daemon = True
                stream_thread.start()
            else:
                print("Continuing packet capture...")  

    except KeyboardInterrupt:
        print("\nCapture interrupted.")
