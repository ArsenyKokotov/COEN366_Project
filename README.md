# COEN366_Project

<h3>Task Plan:</h3>
<br>
<b>Task 0:</b> <u>Client-Server registration/derigistration:</u> 
<br>(Must be done in the begining by all, other steps can be done individually by teammates and then merged together)
<br>
<u>Create server.py</u>
<ul>
  <li>Must either use threads or select function to allow multiple clients.
  <li>Must use UDP sockets.
  <li>Must contain a link to a database (database will be described in a following section).
  <li>Must be able to receive and send messages from/to clients.
</ul>

<u>Create a client.py</u>
<br>
Client is also a server and not just a single executable python script because we want to be able to mantain communication between clients.  
<ul>
  <li>Must use UDP soockets to communicate with server.
  <li>Must use TCP sockets to communicate with peers.
  <li>Must have a database containing files.
</ul>

<br>
<b>Task 1:</b> <u>Client-Server registration/derigistration:</u>
<ul>
  <li>Client must register with server before sending any requests.
  <li>Server will then put into its database and send an ACK to client. 
  <li>If registration is for some reason denied (e.g.: invalid inputs or user already exists) then server sends an error message to client.
    <li> Client must be able to update their info (IP, TCP/UDP ports) and receive either an ACK or an error.
  <li> Use JSON strings to send messages
</ul>

<br>
<b>Task 2:</b> <u>Publishing file related information:</u>
<ul>
    <li> When client is registered with server, client can now send information about its files to the server.
    <li> When recieving the previous message, server send ACK to client.
    <li> If info message is denied because of some error, then server sends an error message to client.
    <li> If client remove file from its database then it sends a message to server, server must either ACk or reply with an error message.
    <li> Use JSON strings to send messages
</ul>

<br>
<br>
<b>Task 3:</b> <u>Retrieving information from the server:</u>
<br> Basically searching for info about clients and files (do they exist or not), no file transfer in this step
<br>

<br>
<b>Task 4:</b> <u>File transfer between peers:</u>
<br> If you know file and you knwo user who have this file, set up TCP connection and transfer that file in chinks of 200 characters. Will need a specific function to do that, cannot just use sendall(). So we need to describe a transfer protocol ourselves (easier than it sounds actually). 
<br>
<br>
<b> Task 5: Making a GUI
<br> Only if we want to. 

 


