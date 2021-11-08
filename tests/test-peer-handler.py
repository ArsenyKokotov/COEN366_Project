import sys
import os
import threading
import socket
import time

sys.path.append('..')
import client

def main():
    host = '127.0.0.1'
    server_host = '127.0.0.1'
    port_tcp_peer = 5070
    #port_tcp_client = 5071
    client_directory = 'client2'

    os.chdir('..')  # want to have same default dir as client.py

    # start the client peer handler
    print('[TEST] Starting peer listener thread\n')
    peer_listen_thread = threading.Thread(target=client.peer_listener_thread, args=(server_host, port_tcp_peer, client_directory))
    peer_listen_thread.start()

    ask_for('example2.txt', server_host, port_tcp_peer)
    ask_for('205char.txt', server_host, port_tcp_peer)




def ask_for(ask_filename, server_host, port_tcp_peer):
    dl_req = {'service': 'DOWNLOAD', 'request_#': 1, 'filename': ask_filename}


    print('\n[TCP CLIENT] Connecting to server on port', server_host, port_tcp_peer)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((server_host, port_tcp_peer))
    print('[TCP CLIENT] TCP connection: ', tcp_socket)

    print('[TCP CLIENT] Sending ', dl_req)
    client.send_lengthprefix_json(dl_req, tcp_socket)

    result = client.receive_lengthprefix_json(tcp_socket)

    # todo: decode the result
    # todo: keep calling receive_lengthprefix_json until we get a FILE END message

    print('[TCP CLIENT] Result: \n', result)

    tcp_socket.close()

main()