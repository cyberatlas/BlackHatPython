import socket

target_host = "127.0.0.1"
target_port = 80

# create a socket object - DATAGRAM is FOR UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#
client.bind((target_host, target_port))

# Because UDP is connectionless there is no connect() method needed.
client.sendto("AAABBBBCCC", (target_host, target_port))

# recieve some data
data, addr = client.recvfrom(4096)
print data, addr