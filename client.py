import socket
import threading
import random
import string
import json
import os


PORT_UDP = 5060
PORT_TCP = 5070

HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = socket.gethostbyname(socket.gethostname())

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((HOST, PORT_UDP))

TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPServerSocket.bind((HOST, PORT_TCP))


# generate a random string for RQ#
def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


def handle_client(conn, addr):
    # want to receive messages from peers
    pass


def server_request():
    # communication with server
    json_request = {}

    while True:
        service_type = input("Enter (DE)-REGISTER/PUBLISH/REMOVE/RETRIEVE-(ALL/INFOT)/SEARCH-FILE: ")
        if service_type in ["REGISTER", "DE-REGISTER", "PUBLISH", "REMOVE", "RETRIEVE-ALL", "RETRIEVE-INFOT",
                            "SEARCH-FILE"]:
            break
        else:
            print("No such service exists. Try again.")

    request_number = randStr()
    json_request['service'] = service_type
    json_request['request_#'] = request_number

    if service_type == "REGISTER":
        name=input("Enter your name: ")
        json_request['name']=name
        json_request['IP']=HOST
        json_request['UDP_socket']=PORT_UDP
        json_request['TCP_socket']=PORT_TCP

    elif service_type == "DE-REGISTER":
        name=input("Enter your name: ")
        json_request['name']=name

    elif service_type == "PUBLISH":
        name=input("Enter your name: ")
        json_request['name']=name
        file_list=[]
        while True:
            print("To stop adding files, write EXIT")
            file_name=input("Input name of txt file you want to add (e.g: example.txt) : ")
            check=os.path.isfile('client_file_storage/' + file_name)
            if check==True:
                file_list.append(file_name)
                print("File " + file_name + " added to publish list")
            elif file_name=="EXIT":
                break
            else:
                print("File does not exist in your client file storage")
        json_request['list of files'] = file_list

    elif service_type == "REMOVE":
        name=input("Enter your name: ")
        json_request['name']=name
        file_list=[]
        while True:
            print("To stop adding files, write EXIT")
            file_name=input("Input name of txt file you want to remove (e.g: example.txt) : ")
            check=os.path.isfile('client_file_storage/' + file_name)
            if check==True:
                file_list.append(file_name)
                print("File " + file_name + " added to removal list")
            elif file_name=="EXIT":
                break
            else:
                print("File does not exist in your client file storage")
        json_request['list of files'] = file_list

    elif service_type == "RETRIEVE-INFOT":
        peer_name=input("Enter name of peer: ")
        json_request['name']=peer_name

    elif service_type == "SEARCH-FILE":
        file_name = input("Enter name of file you're looking for: ")
        json_request['File-name'] = file_name

    msg = json.dumps(json_request)
    UDPServerSocket.sendto(msg.encode(), (SERVER_HOST, 5050))


def client_request():
    # want to send messages to specific client
    pass


def user_request():
    while True:
        identity = input("Enter SERVER or CLIENT depending on who you want to contact: ")
        if identity == "SERVER":
            server_request()
            break
        elif identity == "CLIENT":
            client_request()
            break
        else:
            print("No such service exists. Please repeat.")


def start():
    # TCPServerSocket.listen()

    while True:
        # client sending messages to server or another client
        # if CLIENT_SERVER_REQUEST_ACTIVE == False:
        thread = threading.Thread(target=user_request)
        thread.start()

        # client receiving messages from server
        bytesAddressPair = UDPServerSocket.recvfrom(1024)  # message from server
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        msg1 = "From:{}".format(address)
        msg2 = " Message:{}".format(message)
        print(msg1 + msg2)

        # client receiving messages from other clients
        # conn, addr = TCPServerSocket.accept()
        # thread = threading.Thread(target=handle_client, args=(conn, addr))
        # thread.start()


print("Client is strarting ,,,")
start()
