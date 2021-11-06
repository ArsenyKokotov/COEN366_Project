import mysql.connector
import database_handler

Registered_Client_db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)


#field1:name of client field2:ip_address field3:udp_socket  filed4:tcp_socket

Files_db = mysql.connector.connect (

    host="",
    user="",
    password="",
    database=""
)

# field1: name of client field2: file name 


mycursor_client = Registered_Client_db.cursor()
mycursor_files = Files_db.cursor()


def check_client(name,ip_address, udp_socket, tcp_socket):
    # return valid error message if client is not good
    # return ok is client is good

    pass

def register_client(name, ip_address, udp_socket, tcp_socket):
    # check if client is already registered, check if the input values are valid, etc
    check_client(name, ip_address, udp_socket, tcp_socket)
    # depending on answer from function, return either REGISTERED or REGISTER-DENIED and REASON 
    pass

def update_client(name, ip_address, udp_socket, tcp_socket):

    # Check client connection
    # Update client information
    # Validate information change (correct types)
    # return UPDATE-CONFIRMED or UPDATE DENIED, REASON

    pass

def derigister(name):
    # delete client from client db
    # delete all files related to this user from files db
    # if client does not exist do nothing
    pass

def publish_files(name, list_of_files):
    # insert each file in the list and name into file db
    # if all is well, return PUBLISHED
    # if name does not exist or something else go bad, return PUBLISH-DENIED and REASON  
    pass

def remove_files(name, list_of_files):
    # delete files from list of files that are id with name of client
    # if all is well, return REMOVED
    # else return REMOVE-DENIED and Reason
    pass

def retrieve_all():
    # if success
    # return RETRIEVE and list of list containing the following:
    # List of (Name, IP address, TCP socket#, list of available files)
    # if error return RETRIEVE-ERROR and REASON 
    pass

def retrieve_infot(name):
    # if success
    # return ["RETRIEVE-INFOT", "name", "ip", "tcp port",  ["file1", "file2, ...] ]
    pass

def search_file(file_name):
    # find client(s) with this file from file db
    # if success, return SEARCH-FILE and List of (Name, IP address, TCP socket#)
    # else return SEARCH-ERROR and REASON
    pass

