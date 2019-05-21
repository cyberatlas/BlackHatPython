import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Passing in the IP address and port we want to listen on 
server.bind((bind_ip, bind_port))
#Tell the server to start listening with a maximum backlog of 5  connections 
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

# This is our our client-handling thread
def handle_client(client_socket):

    #Performs the recv function  
    request = client_socket.recv(1024)

    #Print out what the client sends
    print "[*] Received %s" % request

    #Send back a packet 
    client_socket.send("ACK!")

    client_socket.close()

while True:
    #When the client connects, save the client socket into client variable 
    #Save the remote connection details into the addr variable
    client, addr = server.accept()

    print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])

    #Spin up up our client thread to handle incoming data
    #Then our server is ready to handle another connection
    client_handler = threading.Thread(target=handle_client, args=(client,))
    #Start the client handler
    client_handler.start()



