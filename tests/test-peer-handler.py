import json
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
    peer_listen_thread = threading.Thread(target=client.peer_listener_thread, args=(server_host, port_tcp_peer, client_directory), daemon=True)
    peer_listen_thread.start()

    client.ask_for_file('example2.txt', server_host, port_tcp_peer)
    client.ask_for_file('205char.txt', server_host, port_tcp_peer)






main()