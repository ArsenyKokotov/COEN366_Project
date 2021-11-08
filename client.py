# Usage:
# python client.py --udpport 5060 --tcpport 5070 --mode client --folder client_file_storage --name test1

import socket
import sys
import threading
import random
import string
import json
import os
import argparse
import time

PORT_UDP = 5060
PORT_TCP = 5070
client_directory = 'client_file_storage/'
client_name = 'no_name'

HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = socket.gethostbyname(socket.gethostname())

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((HOST, PORT_UDP))

TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPServerSocket.bind((HOST, PORT_TCP))


# generate a random string for RQ#
def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


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
        name = input("Enter your name: ")
        json_request['name'] = name
        json_request['IP'] = HOST
        json_request['UDP_socket'] = PORT_UDP
        json_request['TCP_socket'] = PORT_TCP

    elif service_type == "DE-REGISTER":
        name = input("Enter your name: ")
        json_request['name'] = name

    elif service_type == "PUBLISH":
        name = input("Enter your name: ")
        json_request['name'] = name
        file_list = []
        while True:
            print("To stop adding files, write EXIT")
            file_name = input("Input name of txt file you want to add (e.g: example.txt) : ")
            check = os.path.isfile(client_directory + file_name)
            if check:
                file_list.append(file_name)
                print("File " + file_name + " added to publish list")
            elif file_name == "EXIT":
                break
            else:
                print("File does not exist in your client file storage")
        json_request['list of files'] = file_list

    elif service_type == "REMOVE":
        name = input("Enter your name: ")
        json_request['name'] = name
        file_list = []
        while True:
            print("To stop adding files, write EXIT")
            file_name = input("Input name of txt file you want to remove (e.g: example.txt) : ")
            check = os.path.isfile(client_directory + file_name)
            if check:
                file_list.append(file_name)
                print("File " + file_name + " added to removal list")
            elif file_name == "EXIT":
                break
            else:
                print("File does not exist in your client file storage")
        json_request['list of files'] = file_list

    elif service_type == "RETRIEVE-INFOT":
        peer_name = input("Enter name of peer: ")
        json_request['name'] = peer_name

    elif service_type == "SEARCH-FILE":
        file_name = input("Enter name of file you're looking for: ")
        json_request['File-name'] = file_name

    msg = json.dumps(json_request)
    UDPServerSocket.sendto(msg.encode(), (SERVER_HOST, 5050))


def peer_request():
    # want to send messages to specific client
    pass


def CommandlineThread():
    while True:
        identity = input("Enter SERVER or PEER depending on who you want to contact: ")
        if identity == "SERVER":
            server_request()
            break
        elif identity == "PEER":
            peer_request()
            break
        else:
            print("No such service exists. Please repeat.")


# Handled by command line arguments instead
# def user_request():
#     while True:
#         identity = input("Enter SERVER or CLIENT depending on who you want to contact: ")
#         if identity == "SERVER":
#             server_request()
#             break
#         elif identity == "CLIENT":
#             client_request()
#             break
#         else:
#             print("No such service exists. Please repeat.")


# This thread listens for TCP connections and starts a new thread for each one
def PeerListenerThread():
    # client receiving messages from other clients
    # conn, addr = TCPServerSocket.accept()
    # thread = threading.Thread(target=handle_client, args=(conn, addr))
    # thread.start()

    while True:
        # We accept any incoming TCP connections
        conn, addr = TCPServerSocket.accept()

        # And spawn a new thread to handle them
        thread = threading.Thread(target=peer_connection_handler(), args=(conn, addr))
        thread.start()


# Handler for TCP connections from a peer, spawned for each peer connection
# Peer will send us a DOWNLOAD request
# To which we will respond in small chunks not exceeding 200 characters of FILE, FILE, ..., FILE_END messages
# If file does not exist or cannot be delivered for some other reason, sent DOWNLOAD-ERROR
def peer_connection_handler(conn, addr):
    data_chunk_size_limit = 200  # send no more than 200 chars of file at a time

    file_message = {'service': 'FILE', 'request_#': -1, 'filename': '', 'chunk_#': -1, 'Text': ''}
    file_end_message = {'service': 'FILE-END', 'request_#': -1, 'filename': '', 'chunk_#': -1, 'Text': ''}
    download_error_message = {'service': 'DOWNLOAD-ERROR', 'request_#': -1, 'Reason': 'unspecified'}

    data = conn.recv(1024)
    print('received data from peer: ', data, addr)

    try:
        data_json = json.loads(data.decode('utf-8'))
        message_type = data_json['service']

        if message_type != 'DOWNLOAD':
            download_error_message['Reason'] = 'Peer can only provide DOWNLOAD service'
            msg_bytes = json.dumps(download_error_message).encode('utf-8')
            conn.sendall(msg_bytes)
            return False

        request_number = data_json['request_#']
        request_filename = data_json['filename']

        # TODO: also need to check if this file was published?
        if not os.path.isfile(os.path.join(client_directory, request_filename)):
            download_error_message['Reason'] = 'Requested file does not exist'
            msg_bytes = json.dumps(download_error_message).encode('utf-8')
            return False

    except:
        download_error_message['Reason'] = 'Expected valid JSON request for DOWNLOAD'
        msg_bytes = json.dumps(download_error_message).encode('utf-8')
        conn.sendall(msg_bytes)
        conn.close()
        return False




# This thread listens for UDP datagrams from the server
def ServerListenerThread():
    while True:
        # client receiving messages from server
        bytesAddressPair = UDPServerSocket.recvfrom(1024)  # message from server
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        msg1 = "From:{}".format(address)
        msg2 = " Message:{}".format(message)
        print(msg1 + msg2)


def start():
    global PORT_UDP, PORT_TCP, client_name, client_directory

    # parse arguments
    # UDP port, TCP port, folder for this client
    parser = argparse.ArgumentParser(description='COEN366 Project Client')
    parser.add_argument('--udpport', type=int, required=True)
    parser.add_argument('--tcpport', type=int, required=True)
    parser.add_argument('--folder', type=str, required=True)
    parser.add_argument('--mode', type=str, choices=['client', 'peer'], required=True)
    parser.add_argument('--name', type=str, required=True)

    args = parser.parse_args()
    print('Arguments given: ', args)

    PORT_UDP = args.udpport
    PORT_TCP = args.tcpport
    client_directory = args.folder
    mode = args.mode
    client_name = args.name

    # TCPServerSocket.listen()

    if (mode == 'client'):
        # thread for client sending messages to server or another client as specified by user input
        cli_thread = threading.Thread(target=CommandlineThread)
        cli_thread.start()

        # thread to listen for UDP messages from the server
        server_listen_thread = threading.Thread(target=ServerListenerThread())
        server_listen_thread.start()

    elif (mode == 'peer'):
        # thread to listen for TCP connections from peers
        peer_listen_thread = threading.Thread(target=PeerListenerThread())
        peer_listen_thread.start()


print("Client is starting ...")
print("HOST value: ", HOST)
start()
