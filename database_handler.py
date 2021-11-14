import sqlite3

Registered_Client_db = sqlite3.connect('clientDB.db', check_same_thread=False)
Files_db = sqlite3.connect('filesDB.db', check_same_thread=False)

# field1: name of client field2: file name

mycursor_client = Registered_Client_db.cursor()
mycursor_files = Files_db.cursor()


def check_client(name, ip_address, udp_socket, tcp_socket):
    # return valid error message if client is not good
    # return ok is client is good
    if (name.isalnum()) and ip_address.isascii() and str(udp_socket).isnumeric() and str(tcp_socket).isnumeric():
        print("Client format is VALID")
        return True
    else:
        print("Client format is INVALID")
        return False


def register_client(name, ip_address, udp_socket, tcp_socket):
    # check if client is already registered, check if the input values are valid, etc
    if check_client(name, ip_address, udp_socket, tcp_socket):
        alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE name =?", [name], )
        if len(list(alreadyExistCheck)) >= 1:
            print("Address already exists!")
            return ["REGISTER-DENIED", "CLIENT ALREADY EXISTS"]
        else:
            print("CLIENT CAN BE REGISTERED")
            mycursor_client.execute("INSERT INTO clientDB (name, ip_address, udp_socket, tcp_socket) "
                                    "VALUES (?, ?, ?, ?)",
                                    (name, ip_address, udp_socket, tcp_socket))
            Registered_Client_db.commit()
            return ["REGISTERED"]

    # depending on answer from function, return either REGISTERED or REGISTER-DENIED and REASON


def update_client(name, ip_address, udp_socket, tcp_socket):
    # Check client connection
    # Update client information
    # Validate information change (correct types)
    # return UPDATE-CONFIRMED or UPDATE DENIED, REASON
    if check_client(name, ip_address, udp_socket, tcp_socket):
        mycursor_client.execute(
            "UPDATE clientDB SET udp_socket=?, tcp_socket=? WHERE name = ?",
            (int(udp_socket), int(tcp_socket), name))
        Registered_Client_db.commit()
        return ["UPDATE-CONFIRMED"]
    else:
        return ["UPDATE-DENIED", "Invalid input format type"]


def deregister(name):
    # delete client from client db
    # delete all files related to this user from files db
    # if client does not exist do nothing
    mycursor_client.execute("DELETE FROM clientDB WHERE name=?", [name])
    Registered_Client_db.commit()
    mycursor_files.execute("DELETE FROM filesDB where name=?", [name])
    Files_db.commit()
    print("Client and related Files deleted")
    return ["REMOVE"]


def publish_files(name, list_of_files):
    # insert each file in the list and name into file db
    # if all is well, return PUBLISHED
    # if name does not exist or something else go bad, return PUBLISH-DENIED and REASON
    list_of_files = [list_of_files]
    alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE name=?", [name])
    if len(list(alreadyExistCheck)) >= 1:
        for item in list_of_files:
            mycursor_files.execute("INSERT INTO filesDB (name, file_name) VALUES (?,?)", (name, item))
            Files_db.commit()
        return ["PUBLISHED"]
    else:
        print("User does not exist!")
        return ["PUBLISH-DENIED", "Client does not exist!"]


def remove_files(name, list_of_files):
    # delete files from list of files that are id with name of client
    # if all is well, return REMOVED
    # else return REMOVE-DENIED and Reason
    alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE name=?", [name])
    if len(list(alreadyExistCheck)) >= 1:
        for files in list_of_files:
            mycursor_files.execute("DELETE FROM filesDB WHERE name=? AND file_name=?", (name, files))
            Files_db.commit()
        return ["REMOVED"]
    else:
        return ["REMOVE-DENIED", "Client does not exist!"]


def retrieve_all():
    # if success
    # return RETRIEVE and list of list containing the following:
    # List of (Name, IP address, TCP socket#, list of available files)
    # if error return RETRIEVE-ERROR and REASON
    # length = mycursor_files.execute("SELECT * FROM filesDB")
    # rows = mycursor_files.fetchall()
    # print(rows)
    # if len(list(length))>=1:
    #     rows = mycursor_files.fetchall()
    #     # for row in rows:
    #     #     return ["RETRIEVE", row["name"], row["ip_address"], row["tcp_socket"], [row["file_name"]]]
    #     return ["RETRIEVE", rows]
    # else:
    #     return ["RETRIEVE-ERROR", "No entries in filesDB"]

    #find all names and ip and tcp and udp in client database 
    # [(name, ip, udp, tcp), (...), (...), ...]

    emptyTableCheck = mycursor_client.execute("SELECT COUNT(*) FROM clientDB")
    count=mycursor_client.fetchone()
    if count != 0:

        cursor=mycursor_client.execute("SELECT * FROM clientDB")
        cli_rows=mycursor_client.fetchall()

        # get list of all inputs inside file database 
        # [(name, ..., file), [(name, ..., file), ...]

        cursor = mycursor_files.execute("SELECT * FROM filesDB")
        file_rows = mycursor_files.fetchall()

        list_of_list=[]

        for cli_tuple in cli_rows:
            # list=[]
            # list.append(cli_tuple)
            list_of_list.append(list(cli_tuple))
            for file_tuple in file_rows:
                if cli_tuple[0] == file_tuple[0]:
                    file_list=list(file_tuple)
                    del file_list[0]
                    list_of_list[-1].extend(file_list)


        print(list_of_list)
        return ["RETRIEVE", list_of_list]
    else:
        return ["RETRIEVE-ERROR", "No such client exists"]


def retrieve_infot(name):
    # if success
    # return ["RETRIEVE-INFOT", "name", "ip", "tcp port",  ["file1", "file2, ...] ]
    # mycursor_files.execute("SELECT * FROM filesDB WHERE name = ? ", [name])
    # rows = mycursor_files.fetchall()
    # for row in rows:
    #     return ["RETRIEVE-INFOT", row["name"], row["ip_address"], row["tcp_socket"], [row["file_name"]]]

    alreadyExistCheck = mycursor_client.execute("SELECT * FROM clientDB WHERE name=?", [name])
    if len(list(alreadyExistCheck)) >= 1:

        cursor=mycursor_client.execute("SELECT name, ip_address, udp_socket, tcp_socket FROM clientDB WHERE name = ?", [name])
        cli_row=mycursor_client.fetchall()

        cursor = mycursor_files.execute("SELECT * FROM filesDB WHERE name = ?", [name])
        file_rows = mycursor_files.fetchall()

    

        file_list=[]
        
        for file_tuple in file_rows:
            file_list.append(file_tuple[-1])
        

        return ["RETRIEVE-INFOT", cli_row[0][0], cli_row[0][1], cli_row[0][3], file_list]
    else:
        return ["RETRIEVE-ERROR", "No such client exists"]


def search_file(file_name):
    # find client(s) with this file from file db
    # if success, return SEARCH-FILE and List of (Name, IP address, TCP socket#)
    # else return SEARCH-ERROR and REASON
    cursor = mycursor_files.execute("SELECT name FROM filesDB WHERE file_name = ? ", [file_name])
    file_rows = mycursor_files.fetchall()

    name_array=[]
    
    for file_tuple in file_rows:
        name_array.append(file_tuple[0])

    list_of_search=[]

    if len(name_array)!=0:
        for name in name_array:
            cursor = mycursor_client.execute("SELECT name, ip_address, udp_socket, tcp_socket FROM clientDB WHERE name = ?", [name])
            cli_row=mycursor_client.fetchall()
            list_of_search.append(cli_row)
        return ["SEARCH-FILE", list_of_search]
    else:
        return ["SEARCH-ERROR", "File name does not exist!"]


    # print(rows)
    # if len(list(length)) >= 1:
    #     searchOutput = mycursor_files.fetchall()
    #     final_result = [i[0] for i in searchOutput]
    #     return ["SEARCH FILE", [final_result]]
    # else:
    #     return ["SEARCH-ERROR", "File name does not exist!"]
