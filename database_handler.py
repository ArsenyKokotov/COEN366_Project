import mysql.connector
import sqlite3

Registered_Client_db = sqlite3.connect('clientDB.db')
Files_db = sqlite3.connect('filesDB.db')

# field1: name of client field2: file name

mycursor_client = Registered_Client_db.cursor()
mycursor_files = Files_db.cursor()


def check_client(name, ip_address, udp_socket, tcp_socket):
    # return valid error message if client is not good
    # return ok is client is good
    if (name.isalpha()) and ip_address.isalpha() and udp_socket.isnumeric() and tcp_socket.isnumeric():
        print("Client format is VALID")
        return True
    else:
        print("Client format is INVALID")
        return False


def register_client(name, ip_address, udp_socket, tcp_socket):
    # check if client is already registered, check if the input values are valid, etc
    if check_client(name, ip_address, udp_socket, tcp_socket):
        alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE ip_address =?",
                                                    ip_address)
        if len(alreadyExistCheck) >= 1:
            return ["REGISTER-DENIED", "CLIENT ALREADY EXISTS"]
        else:
            print("CLIENT CAN BE REGISTERED")
            mycursor_client.execute("INSERT INTO clientDB (name, ip_address, udp_socket, tcp_socket) "
                                    "VALUES (?, ?, ?, ?)",
                                    (name, ip_address, udp_socket, tcp_socket))
            Registered_Client_db.commit()
            return ["REGISTERED"]

    else:
        print("Client format is INVALID")
        return ["REGISTER-DENIED", "Client format is INVALID"]

    # depending on answer from function, return either REGISTERED or REGISTER-DENIED and REASON


def update_client(name, ip_address, udp_socket, tcp_socket):
    # Check client connection
    # Update client information
    # Validate information change (correct types)
    # return UPDATE-CONFIRMED or UPDATE DENIED, REASON
    if check_client(name, ip_address, udp_socket, tcp_socket):
        mycursor_client.execute(
            "UPDATE clientDB SET name=?, ip_address=?, udp_socket=?, tcp_socket=? WHERE ip_address = ?",
            (name, ip_address, udp_socket, tcp_socket, ip_address))
        Registered_Client_db.commit()
        return ["UPDATE-CONFIRMED"]
    else:
        return ["UPDATE-DENIED", "Invalid input format type"]


def deregister(name):
    # delete client from client db
    # delete all files related to this user from files db
    # if client does not exist do nothing
    mycursor_client.execute("DELETE FROM clientDB WHERE name=?", name)
    Registered_Client_db.commit()
    mycursor_files.execute("DELETE FROM filesDB where name=?", name)
    Files_db.commit()
    print("Client and related Files deleted")
    return ["REMOVE"]


def publish_files(name, list_of_files):
    # insert each file in the list and name into file db
    # if all is well, return PUBLISHED
    # if name does not exist or something else go bad, return PUBLISH-DENIED and REASON
    alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE name=?", name)
    if len(alreadyExistCheck) >= 1:
        values = [[item] for item in list_of_files]
        mycursor_files.execute("INSERT INTO filesDB (name, files) VALUES (?,?)", (name, values))
        Files_db.commit()
        return ["PUBLISHED"]
    else:
        return ["PUBLISH-DENIED", "Client does not exist!"]


def remove_files(name, list_of_files):
    # delete files from list of files that are id with name of client
    # if all is well, return REMOVED
    # else return REMOVE-DENIED and Reason
    alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE name=?", name)
    if len(alreadyExistCheck) >= 1:
        values = [[item] for item in list_of_files]
        mycursor_files.execute("DELETE FROM filesDB WHERE name=?", name)
        Files_db.commit()
        return ["REMOVED"]
    else:
        return ["REMOVE-DENIED", "Client does not exist!"]


def retrieve_all():
    # if success
    # return RETRIEVE and list of list containing the following:
    # List of (Name, IP address, TCP socket#, list of available files)
    # if error return RETRIEVE-ERROR and REASON
    mycursor_files.execute("", )
    return ["RETRIEVE", ]


def retrieve_infot(name):
    # if success
    # return ["RETRIEVE-INFOT", "name", "ip", "tcp port",  ["file1", "file2, ...] ]
    mycursor_files.execute("SELECT name, ip_address, tcp_socket, file_name FROM filesDB WHERE name = ? ", name)
    output = mycursor_files.fetchall()

    return ["RETRIEVE-INFOT",  ]


def search_file(file_name):
    # find client(s) with this file from file db
    # if success, return SEARCH-FILE and List of (Name, IP address, TCP socket#)
    # else return SEARCH-ERROR and REASON
    length = mycursor_files.execute("SELECT name, ip_address, tcp_socket  "
                                    "FROM filesDB WHERE file_name = ? ", file_name)
    if len(length) >= 1:
        searchOutput = mycursor_files.fetchall()
        final_result = [i[0] for i in searchOutput]
        return ["SEARCH FILE", [final_result]]
    else:
        return ["SEARCH-ERROR", "File name does not exist!"]
