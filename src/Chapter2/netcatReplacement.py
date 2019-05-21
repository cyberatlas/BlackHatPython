import sys
import socket
import getopt
import threading
import subprocess

#Define some global variables
#Fun fact: learned you can use tabs to make good spacing in python
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

# Gives info on how to use the program 
def usage():
    print "BHP Net Tool"
    #TODO why is this here???
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l, --listen              - listen on [host]:[port] for"\
                                     "incoming connections"
    print "-e. --execute=file_to_run - execute the given file"\
                                     "upon receiving a connection"
    print "-c --command             - initialize a command shell"
    print "-u --upload=destination  - upon receiving connection upload a \
                                      file and write to [destination]"
    #TODO why is this here? Can we delete it?
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)

# Main function responsible for handling command line args and calling functions
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[:1]):
        usage()
    #Read in the command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu", \
        ["help", "listen", "execute", "target", "port", "command", "upload"])
    # If the user sends in the wrong input, throw an error
    # Tell them how to use the program
    except getopt.GetoptError as err:
            print str(err)
            usage()
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = TRUE
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in  ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # Are going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # Read in the buffer from the command line
        # This will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # Send data off
        client_sender(buffer)

    # We are going to listen and potentially 
    # upload things, execute commands, and drop a shell back
    # depening on our command line options above
    if listen:
        # Detect that we are to set up a listening socket and process further commands
        server_loop()
main()

def client_sender(buffer):
    # Set up TCP socket 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to our target host
        client.connect((target, port))

        # See if we have received any input from stdin
        if len(buffer):
            client.send(buffer)
        while True:
            # Now wait for data back 
            recv_len = 1
            response = ""

            # If all is well, send the data to the remote target and receive data back 
            while recv_len:
                data        = client_recv(4096)
                recv_len    = len(data)
                response    += data

                if recv_len < 4096:
                    break

            print response,

            # Wait for more input
            # Continue sending and receiving data till user kills the script
            buffer = raw_input("")
            # The extra is specifically attached to user input so that way 
            # our client will be compatible with our command shell
            buffer += "\n"
            # Send it off 
            client.send(buffer)

    except:
        print"[*] Exception! Exiting."
        # Tear down the connection
        client.close

# Now we create our primary server loop and stub function that will handle both 
# our command execution and our full command shell

def server_loop():
    global target
    # If no target is defined, we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target_port))
    





