import socket

#target_host = "www.google.com"
target_host = "127.0.0.1"
#target_port = 80
target_port = 9999

#Create a socket object
#AF_INET says we are going to use a standard IPV4 address or hostname
#SOCK_STREAM indicates this will be a tcp client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the client
client.connect((target_host,target_port))

#Send some data
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#Recieve some data
response = client.recv(4096)

print response
