# COEN366_Project

<h3>Task Plan:</h3>
<u>Create server.py</u>
-must either use threads or select function to allow multiple clients
-must use UDP sockets
-must contain a link to a database
-must be able to receive and send messages from/to clients

<u>Create a client.py</u>
-must use UDP soockets to communicate with server
-must use TCP sockets to communicate with peers


<b>Step 1</b> <u>Client-Server registration/derigistration:</u>
-Client must register with server before sending any requests: To register client must send a message containing the following to the server: 
<ul>
  <li>REGISTER</li>
  <li>RQ#</li>
  <li>Name</li>
  <li>IP Address</li>
  <li>UDP socket#</li>
  <li>TCP socket#</li>
</ul>
Server will then put into its database and send a reply to client. The reply will contain the following:
<ul>
  <li>REGISTERED</li>
   <li>RQ#</li>
</ul>
If registration is for some reason denied (e.g.: invalid inputs or user already exists) then server sends the following reply to client:
<ul>
  <li>REGISTER-DENIED</li>
   <li>RQ#</li>
   <li>Reason</li>
</ul>



Server communication
- python client and server
- json data exchange format
- represent the fundamental parts of the protocol as classes/objects in python (each kind of message, a client class, a server class, etc)
- Design for LAN only (so only need to keep track of LAN IPs)
- No auth / GUI (the bonus marks) 
The server needs to keep track of the client data persistently so idk maybe an sqlite db or some other DB (maybe nosql of some kind since there is some variability in data stored for each client)
