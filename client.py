import socket
import threading
import random
import string
import json
import os
import argparse
import time
import ctypes

# Usage:
# To launch client CLI and peer listener
# python client.py --udpport 5060 --tcpport 5070 --mode both --folder client_file_storage --name test1
#
# To launch only client CLI
# python client.py --udpport 5060 --tcpport 5070 --mode client --folder client_file_storage --name test1
#
# To launch only peer listener
# python client.py --udpport 5060 --tcpport 5070 --mode peer --folder client_file_storage --name test1
#
# and to specify your IP and database server IP to use in either mode: --host "127.0.0.1" --server_host "127.0.0.1"
# specify server UDP port with --server_udpport 5051
#
# Example usages
# python client.py --udpport 5054 --tcpport 5070 --mode both --folder client_file_storage --name test1 --host "127.0.0.1" --server_host "127.0.0.1" --server_udpport 5051
# python client.py --udpport 5061 --tcpport 5071 --mode both --folder client2 --name test1 --host "127.0.0.1" --server_host "127.0.0.1" --server_udpport 5051
def start():
    #global PORT_UDP, PORT_TCP, client_name, client_directory

    # parse arguments
    # UDP port, TCP port, folder, mode (CLI or peer listener) for this client
    parser = argparse.ArgumentParser(description='COEN366 Project Client')
    parser.add_argument('--udpport', type=int, required=True)
    parser.add_argument('--tcpport', type=int, required=True)
    parser.add_argument('--folder', type=str, required=True)
    parser.add_argument('--mode', type=str, choices=['client', 'peer', 'both'], required=True)
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--host', type=str, required=False)
    parser.add_argument('--server_host', type=str, required=False)
    parser.add_argument('--server_udpport', type=int, required=False, default=5051)

    args = parser.parse_args()
    print('Arguments given: ', args)

    port_udp = args.udpport
    port_tcp = args.tcpport
    client_directory = args.folder
    mode = args.mode
    client_name = args.name

    # Our IP interface to bind on / use
    if not args.host:
        host = socket.gethostbyname(socket.gethostname())
    else:
        host = args.host

    print("Client interface: ", host)

    # Server IP address
    if not args.server_host:
        server_host = socket.gethostbyname(socket.gethostname())
        print("No server_host param, assuming local server\nSERVER_HOST value: ", server_host)
    else:
        server_host = args.server_host
        print("Server IP: ", server_host)

    # Server UDP port
    server_udpport = args.server_udpport

    # Launch CLI environment
    if (mode == 'client'):
        UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPServerSocket.bind((host, port_udp))

        # thread for client sending messages to server or another client as specified by user input
        cli_thread = threading.Thread(target=CommandlineThread,
                                      args=(UDPServerSocket, host, server_host, server_udpport, port_udp, port_tcp, client_directory, client_name),
                                      daemon=True)
        cli_thread.start()

        # thread to listen for UDP messages from the server
        server_listen_thread = threading.Thread(target=server_listener_thread, args=(UDPServerSocket,))
        server_listen_thread.start()

    # Launch listener for peer requests
    elif (mode == 'peer'):
        # thread to listen for TCP connections from peers
        peer_listen_thread = threading.Thread(target=peer_listener_thread, args=(host, port_tcp, client_directory),
                                              daemon=True)
        peer_listen_thread.start()

    elif (mode == 'both'):
        UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPServerSocket.bind((host, port_udp))

        # thread for client sending messages to server or another client as specified by user input
        cli_thread = threading.Thread(target=CommandlineThread,
                                      args=(UDPServerSocket, host, server_host, server_udpport, port_udp, port_tcp, client_directory, client_name),
                                      daemon=True)
        cli_thread.start()

        # thread to listen for UDP messages from the server
        server_listen_thread = threading.Thread(target=server_listener_thread, args=(UDPServerSocket,))
        server_listen_thread.start()

        # thread to listen for TCP connections from peers
        peer_listen_thread = threading.Thread(target=peer_listener_thread, args=(host, port_tcp, client_directory),
                                              daemon=True)
        peer_listen_thread.start()


    while True:
        try:
            time.sleep(1)
        except (EOFError, KeyboardInterrupt):
            # Crude, but means we can actually exit the program
            # sys.exit does not work as it tries to cleanly release the resources - including the blocked sockets
            # https://stackoverflow.com/a/49819404/9421977
            os._exit(0)


# Store configuration constants for the client and peer here
class ClientConfig(object):
    def __init(self):
        pass

    MAX_CHUNK_COUNT_LIMIT = 1000


# generate a random string for RQ#
def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

# CLI input handler
# Make a request to server using UDP
def server_request(UDPServerSocket, host, server_host, server_port_udp, port_udp, port_tcp, client_directory, client_name):
    # communication with server
    json_request = {}

    while True:
        service_type = input("Enter (DE)-REGISTER/PUBLISH/REMOVE/RETRIEVE-(ALL/INFOT)/SEARCH-FILE/UPDATE-CONTACT: ")
        if service_type in ["REGISTER", "DE-REGISTER", "PUBLISH", "REMOVE", "RETRIEVE-ALL", "RETRIEVE-INFOT",
                            "SEARCH-FILE", "UPDATE-CONTACT"]:
            break
        else:
            print("No such service exists. Try again.")

    request_number = randStr()
    json_request['service'] = service_type
    json_request['request_#'] = request_number

    if service_type == "REGISTER":
        # name = input("Enter your name: ")
        name = client_name
        json_request['name'] = name
        json_request['IP'] = host
        json_request['UDP_socket'] = port_udp
        json_request['TCP_socket'] = port_tcp
    
    elif service_type == "UPDATE-CONTACT":
        name = client_name
        json_request['name'] = name
        
        while True:
            # TODO: Don't actually need to send new IP in body. Sending the request is enough.
            q=input("Do you want to change IP address (Y/N)?: ")
            if q == "Y":
                json_request['IP'] = input("Input new IP address: ")
                break
            elif q=="N":
                json_request['IP'] = host
                break
            else:
                print("Please answer Y or N")
        
        while True:
            q=input("Do you want to change UDP_socket (Y/N)?: ")
            if q == "Y":
                json_request['UDP_socket'] = input("Input new UDP socket: ")
                break
            elif q=="N":
                json_request['UDP_socket'] = port_udp
                break
            else:
                print("Please answer Y or N")
        
        while True:
            q=input("Do you want to change TCP_socket (Y/N)?:  ")
            if q == "Y":
                json_request['TCP_socket'] = input("Input new TCP socket: ")
                break
            elif q=="N":
                json_request['TCP_socket'] = port_tcp
                break
            else:
                print("Please answer Y or N")

    elif service_type == "DE-REGISTER":
        #name = input("Enter your name: ")
        #json_request['name'] = name
        json_request['name'] = client_name

    elif service_type == "PUBLISH":
        #name = input("Enter your name: ")
        #json_request['name'] = name
        json_request['name'] = client_name

        file_list = []
        while True:
            print("To stop adding files, write EXIT")
            file_name = input("Input name of txt file you want to add (e.g: example.txt) : ")
            check = os.path.isfile(os.path.join(client_directory, file_name))
            if check:
                file_list.append(file_name)
                print("File " + file_name + " added to publish list")
            elif file_name == "EXIT":
                break
            else:
                print("File does not exist in your client file storage")
        json_request['list of files'] = file_list

    elif service_type == "REMOVE":
        # name = input("Enter your name: ")
        # json_request['name'] = name
        json_request['name'] = client_name
        file_list = []
        while True:
            print("To stop adding files, write EXIT")
            file_name = input("Input name of txt file you want to remove (e.g: example.txt) : ")
            check = os.path.isfile(os.path.join(client_directory, file_name))
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
    UDPServerSocket.sendto(msg.encode(), (server_host, server_port_udp))


# want to send messages to specific client
def peer_request(client_directory, peer_name):
    download_message = {'service': 'DOWNLOAD', 'request_#': -1, 'filename': ''}

    # TODO get peer name and resolve it to IP/port instead of manually entering
    #target_peer = input('What peer would you like to download a file from?')
    peer_ip = input('[CLIENT] What is IP of peer?: ')
    port_tcp = int(input('[CLIENT] What is port of peer?: '))

    target_file = input('[CLIENT] What file would you like to download from the peer?: ')

    file = ask_for_file(target_file, peer_ip, port_tcp)

    # Write the file to our storage directory
    target_file_path = os.path.join(client_directory, target_file)
    if(os.path.isfile(target_file_path)):
        print('[CLIENT] You already have a file called {f}, cannot save to your storage directory'.format(f=target_file))
    else:
        with open(target_file_path, 'w') as f:
            print('[CLIENT] Writing downloaded file to', target_file_path)
            f.write(file)


def ask_for_file(ask_filename, peer_ip, port_tcp_peer):
    dl_req = {'service': 'DOWNLOAD', 'request_#': 1, 'filename': ask_filename}

    print('\n[TCP CLIENT] Connecting to server on port', peer_ip, port_tcp_peer)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(5)  # set 5s timeout
    tcp_socket.connect((peer_ip, port_tcp_peer))
    print('[TCP CLIENT] TCP connection: ', tcp_socket)

    print('[TCP CLIENT] Sending ', dl_req)
    send_lengthprefix_json(dl_req, tcp_socket)

    file_end = False
    chunks = []
    count = 0
    while not file_end:
        result = receive_lengthprefix_json(tcp_socket)
        decoded = json.loads(result.decode(('utf-8')))
        chunks.append(decoded)
        print('[TCP CLIENT] Got chunk: ', decoded)
        if(decoded['service'] == 'FILE-END'):
            file_end = True
        elif(decoded['service'] == 'FILE'):
            # loop around and get next chunk
            pass
        elif(decoded['service'] == 'DOWNLOAD-ERROR'):
            print('[TCP CLIENT] Received DOWNLOAD-ERROR')
            raise RuntimeError
        else:
            print('[TCP CLIENT] Received invalid service from peer in chunk: ', decoded['service'])
            raise ValueError

        count += 1
        if(count > ClientConfig.MAX_CHUNK_COUNT_LIMIT):
            print('[TCP CLIENT] File exceeded maximum chunk count of ', ClientConfig.MAX_CHUNK_COUNT_LIMIT)
            raise RuntimeError

    reassembled = ''.join([x['Text'] for x in chunks])
    print('[TCP CLIENT] Reassembled file {f}: {r}'.format(f=chunks[-1]['filename'], r=reassembled))

    tcp_socket.close()

    return reassembled


def CommandlineThread(UDPServerSocket, host, server_host, server_port_udp, port_udp, port_tcp, client_directory, client_name):
    while True:
        try:
            identity = input("Enter SERVER or PEER depending on who you want to contact: ")
            if identity == "SERVER":
                server_request(UDPServerSocket, host, server_host, server_port_udp, port_udp, port_tcp, client_directory, client_name)
                #break
            elif identity == "PEER":
                peer_request(client_directory, client_name)
                #break
            else:
                print("No such service exists. Please repeat.")
        except Exception as e:
            print('[CLI] Error in CLI handler, returning to top level: ', e)


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
def peer_listener_thread(host, port_tcp, client_directory):
    print('[PEER] Peer listener thread starting')

    # client receiving messages from other clients
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPServerSocket.bind((host, port_tcp))
    TCPServerSocket.listen(1)

    while True:
        # We accept any incoming TCP connections
        conn, addr = TCPServerSocket.accept()

        # And spawn a new thread to handle them
        thread = threading.Thread(target=peer_connection_handler, args=(conn, addr, client_directory), daemon=True)
        thread.start()


# Handler for TCP connections from a peer, spawned for each peer connection
# Peer will send us a DOWNLOAD request
# To which we will respond in small chunks not exceeding 200 characters of FILE, FILE, ..., FILE_END messages
# If file does not exist or cannot be delivered for some other reason, sent DOWNLOAD-ERROR
def peer_connection_handler(tcp_conn, addr, client_directory):
    data_chunk_size_limit = 200  # send no more than 200 chars of file at a time

    file_message = {'service': 'FILE', 'request_#': -1, 'filename': '', 'chunk_#': -1, 'Text': ''}
    file_end_message = {'service': 'FILE-END', 'request_#': -1, 'filename': '', 'chunk_#': -1, 'Text': ''}
    download_error_message = {'service': 'DOWNLOAD-ERROR', 'request_#': -1, 'Reason': 'unspecified'}

    #data = conn.recv(1024)
    data = receive_lengthprefix_json(tcp_conn)
    print('\n[PEER][TCP Listen] received request: ', data, addr)

    # Parse the request
    try:
        data_json = json.loads(data.decode('utf-8'))
        message_type = data_json['service']

        if message_type != 'DOWNLOAD':
            download_error_message['Reason'] = 'Peer can only provide DOWNLOAD service'
            #msg_bytes = json.dumps(download_error_message).encode('utf-8')
            #conn.sendall(msg_bytes)
            send_lengthprefix_json(download_error_message, tcp_conn)
            return False

        request_number = data_json['request_#']
        request_filename = data_json['filename']


    except:
        download_error_message['Reason'] = 'Expected valid JSON request for DOWNLOAD'
        #msg_bytes = json.dumps(download_error_message).encode('utf-8')
        #conn.sendall(msg_bytes)
        send_lengthprefix_json(download_error_message, tcp_conn)
        #conn.close() #not closing connection here since according to doc client is meant to do that
        return False

    # Respond to the request
    # TODO: also need to check if this file was published?
    # Check that the requested file exists
    requested_file = os.path.join(client_directory, request_filename)
    print('[PEER] Received request for file', requested_file)
    if not os.path.isfile(requested_file):
        download_error_message['Reason'] = 'Requested file does not exist'
        download_error_message['request_#'] = request_number
        #msg_bytes = json.dumps(download_error_message).encode('utf-8')
        #conn.sendall(msg_bytes)
        send_lengthprefix_json(download_error_message, tcp_conn)
        #conn.close()
        return False


    # File does exist, so read it, split it into chunks (if needed) and send it
    # TODO: empty file behaviour?
    with open(os.path.join(client_directory, request_filename), 'r') as f:
        text = f.read()

    # https://pythonexamples.org/python-split-string-into-specific-length-chunks/
    # https://stackoverflow.com/questions/13673060/split-string-into-strings-by-length
    chunks = [text[i:i+data_chunk_size_limit] for i in range(0, len(text), data_chunk_size_limit)]
    chunk_count = len(chunks)

    # Only one chunk to send, so only send FILE-END chunk
    if(chunk_count == 1):
        file_end_message['filename'] = request_filename
        file_end_message['request_#'] = request_number
        file_end_message['chunk_#'] = 0
        file_end_message['Text'] = text
        #msg_bytes = json.dumps(file_end_message).encode('utf-8')
        #conn.sendall(msg_bytes)
        send_lengthprefix_json(file_end_message, tcp_conn)
        tcp_conn.close()
        return True
    # More than one chunk:
    else:
        file_message['filename'] = request_filename
        file_message['request_#'] = request_number
        file_end_message['filename'] = request_filename
        file_end_message['request_#'] = request_number

        # Send chunks 0 to second last
        for i in range(0, chunk_count-1):
            file_message['chunk_#'] = i
            file_message['Text'] = chunks[i]
            #msg_bytes = json.dumps(file_message).encode('utf-8')
            #conn.sendall(msg_bytes)
            send_lengthprefix_json(file_message, tcp_conn)

        # send last chunk
        file_end_message['chunk_#'] = chunk_count-1
        file_end_message['Text'] = chunks[chunk_count-1]
        send_lengthprefix_json(file_end_message, tcp_conn)
        #conn.close()  # Up to client to close connection
        return True

# Given a json-serializable object, send the json with a 4 byte length prefix over a TCP connection
def send_lengthprefix_json(message, tcp_conn):
    json_text = json.dumps(message)
    json_text_len = len(json_text)
    #prefixed_text = json_text_len.to_bytes(4, 'big') + json_text.encode('utf-8')  # Send 4 bytes, big endian
    # Send 4 bytes for length, big endian, followed by the message
    msg_bytes = json_text_len.to_bytes(4, 'big') + json_text.encode('utf-8')
    tcp_conn.sendall(msg_bytes)

    return True

# function to return one JSON message at a time from the connection
def receive_lengthprefix_json(tcp_conn):
    # buffer = []
    # read_count = 0

    length_prefix_bytes = recvall(tcp_conn, 4)  # get the length, use recvall because we need all 4 bytes at once

    # if there is no message
    if not length_prefix_bytes:
        return None

    # if there is the length prefix for a message, use recvall again to get exactly the length of the message
    length_prefix = int.from_bytes(length_prefix_bytes, byteorder='big')
    #print('[RECVJSON] Got JSON length prefix of ', length_prefix)

    message = recvall(tcp_conn, length_prefix)
    return message

    # # read until we get entire message but not a single byte more
    # while read_count < length_prefix:
    #     received = conn.recv(1024)
    #     # If we received less bytes than the JSON length, add them all to the buffer
    #     # If we received more (likely the start of the next JSON message), only add as many
    #     buffer += received[0, min(length_prefix-read_count, len(received))]
    #     read_count = len(buffer)


# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
# Receive all from recv request
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# Used to show popups without blocking receiver thread
def pop_up_thread(msg, title):
    ctypes.windll.user32.MessageBoxW(0, msg, title, 1)

# This thread listens for UDP datagrams from the server
def server_listener_thread(UDPServerSocket):
    while True:
        # client receiving messages from server
        bytesAddressPair = UDPServerSocket.recvfrom(1024)  # message from server
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        msg1 = "\n[UDP Listen] From:{}".format(address)
        msg2 = "[UDP Listen] Message:{}".format(message)

        popup_thread = threading.Thread(target=pop_up_thread, args=(msg2, msg1))
        popup_thread.start()

        ctypes.windll.user32.MessageBoxW(0, msg2, msg1 , 1)
        #print(msg1 + msg2)




# Only run the start function if the script is being run directly (allows tests to import this file)
if __name__ == '__main__':
    print("Client is starting ...")
    start()
