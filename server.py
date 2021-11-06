import socket
import threading

PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
UDPServerSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((HOST, PORT))

#CREATE DATABASES
#################

#################

#TASK 1
def registration(data):
    # data: RQ#, Name, IP Address, UDP socket#, TCP socket #
    # insert data into client database
    # depending on results either send ACK or Error: 
            # ACK = REGISTERED, RQ#  
            # Error = REGISTER-DENIED, RQ#, Reason
    # reply = ACK or Error
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass

def derigistration(data):
    # data: RQ#, Name
    # either remove from database or ignore message
    pass

def update_contact(data):
    # data: RQ#, Name, IP Address, UDP socket#, TCP socket#
    # update client database
    # if updated then reply = UPDATE CONFIRMED, RQ#, Name, IP Address, UDP socket#, TCP socket#
    # else reply = UPDATE DENIED, RQ#, Name, Reason
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass

#TASK 2
def publishing(data):
    # data: RQ#, Name, List of files, IP Address, UDP socket#
    # update file database (be careful about not repeating file values)
    # if updated then reply = PUBLISHED, RQ#
    # else if error then reply = PUBLISH-DENIED, RQ#, Reason
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass

def file_removal(data):
    # data: RQ#, Name, List of files to remove, IP Address, UDP socket#
    # update file database
    # if updated then reply = REMOVED, RQ#
    # else if error then reply = REMOVE-DENIED, RQ#, Reason
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass

#TASK 3
def retrieve_all(data):
    # data: RQ#, IP Address, UDP socket#
    # retrieve client database 
    # reply = RETRIEVE RQ# List of (Name, IP address, TCP socket#, list of available files)
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass

def retrieve_infot(data):
    # data: RQ#,  Name,  IP Address, UDP socket#
    # retrieve from client+file databases
    # if success, reply = RETRIEVE-INFOT, RQ#, Name, IP Address, TCP socket#, List of available files
    # else if error, reply = RETRIEVE-ERROR, RQ#, Reason
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass

def search_file(data):
    # data: RQ#,  File-name, IP Address, UDP socket#
    # retrieve from client+file database
    # if success, reply = SEARCH-FILE RQ# List of (Name, IP address, TCP socket#)
    # else if error, reply = SEARCH-ERROR, RQ#, Reason
    # addr=(IP Address, UDP socket#)
    # UDPServerSocket.sendto(reply, addr)
    pass


def handle_client(message, address):
    print("[NEW CONNECTION]" + address + " connected.")

    print("Received message: " + message)
    
    msg="Message Received"
    bytes_msg=msg.encode()

    end = address.find(",")
    CLIENT_HOST=address[2:end-1]
    CLIENT_PORT=address[end+1:-1]

    
    UDPServerSocket.sendto(bytes_msg, (CLIENT_HOST, int(CLIENT_PORT)))

    # depending on type
    # possible types: REGISTER, DE-REGISTER, PUBLISH, REMOVE, RETRIEVE-ALL, RETRIEVE-INFOT, SEARCH-FILE, UPDATE CONTACT
    # execute appropriate function 


def start():
    #UDPServerSocket.listen()
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(1024)
        message = format(bytesAddressPair[0])
        address = format(bytesAddressPair[1])
        thread = threading.Thread(target=handle_client, args=(message, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}" )

print("Server is strarting ,,,")
start()
