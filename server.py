import os
import socket
import threading
import json
import database_handler as dh


PORT = 5051
HOST = '127.0.0.1' #change IP to output of https://www.ipchicken.com/
UDPServerSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((HOST, PORT))

#TASK 1
def registration(message, address):
    
    response = dh.register_client(message['name'], message['IP'], message['UDP_socket'], message['TCP_socket'])

    reply={}

    if response[0] == "REGISTERED":
        reply['service']=response[0]
        reply['request_#']=message['request_#']
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address)


def derigistration(message):
    dh.deregister(message['name'])
   

def update_contact(message, address):
    
    response = dh.update_client(message['name'], message['IP'], message['UDP_socket'], message['TCP_socket'])

    reply={}

    if response[0] == "UPDATE-CONFIRMED":
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['name']=message['name']
        reply['IP']=message['IP']
        reply['UDP_socket']=message['UDP_socket']
        reply['TCP_socket']=message['TCP_socket']
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['name']=message['name']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address)

#TASK 2
def publishing(message, address):

    response = dh.publish_files(message['name'], message['list of files'])

    reply={}

    if response[0] == "PUBLISHED":
        reply['service']=response[0]
        reply['request_#']=message['request_#']
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address)
    

def file_removal(message, address):
    
    response = dh.remove_files(message['name'], message['list of files'])

    reply={}

    if response[0] == "REMOVED":
        reply['service']=response[0]
        reply['request_#']=message['request_#']
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address) 

#TASK 3
def retrieve_all(message, address):
    
    response = dh.retrieve_all()

    reply={}

    if response[0] == "RETRIEVE":
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['list']=response[1]
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address) 

def retrieve_infot(message, address):
   
    response = dh.retrieve_infot(message['name'])

    reply={}
   
    if response[0] == "RETRIEVE-INFOT":
       reply['service'] = response[0]
       reply['request_#']=message['request_#']
       reply['name']=response[1]
       reply['IP']=response[2]
       reply['TCP_socket']=response[3]
       reply['list']=response[4]
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address) 

def search_file(message, address):

    response = dh.search_file(message['File-name'])

    reply={}

    if response[0] == "SEARCH-FILE":
       reply['service'] = response[0]
       reply['request_#']=message['request_#']
       reply['list']=response[1]
    else:
        reply['service']=response[0]
        reply['request_#']=message['request_#']
        reply['reason']=response[1]
    
    msg=json.dumps(reply)
    
    UDPServerSocket.sendto(msg.encode(), address) 


def handle_client(message, address):

    print("[NEW CONNECTION]" + address + " connected.")
    print("Received message: " + message)
    
    message_json=json.loads(message[2:-1])
    service_type=message_json['service']

    end = address.find(",")
    CLIENT_HOST=address[2:end-1]
    CLIENT_PORT=address[end+1:-1]
    addr = (CLIENT_HOST, int(CLIENT_PORT)) 

    if service_type == "REGISTER":
        registration(message_json, addr)
    elif service_type == "DE-REGISTER":
        derigistration(message_json)
    elif service_type == "PUBLISH":
        publishing(message_json, addr)
    elif service_type == "REMOVE":
        file_removal(message_json, addr)
    elif service_type == "RETRIEVE-ALL":
        retrieve_all(message_json, addr)
    elif service_type == "RETRIEVE-INFOT":
        retrieve_infot(message_json, addr)
    elif service_type == "SEARCH-FILE":
        search_file(message_json, addr)
    elif service_type == "UPDATE-CONTACT":
        update_contact(message_json, addr)

    # msg="Message Received"
    # bytes_msg=msg.encode()
    # UDPServerSocket.sendto(bytes_msg, (CLIENT_HOST, int(CLIENT_PORT)))



def start():
    #UDPServerSocket.listen()
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(1024)
        message = format(bytesAddressPair[0])
        address = format(bytesAddressPair[1])
        thread = threading.Thread(target=handle_client, args=(message, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}" )


print("Server is starting...")
start()
