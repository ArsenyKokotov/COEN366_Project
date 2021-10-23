# COEN366_Project
Server communication
- python client and server
- json data exchange format
- represent the fundamental parts of the protocol as classes/objects in python (each kind of message, a client class, a server class, etc)
- Design for LAN only (so only need to keep track of LAN IPs)
- No auth / GUI (the bonus marks) 
The server needs to keep track of the client data persistently so idk maybe an sqlite db or some other DB (maybe nosql of some kind since there is some variability in data stored for each client)



# Server Design
- Port 3366
- Runs as a daemon
- Accepts (or refuses) clients registrations
- Accepts (or refuses) client deregistrations
- Accepts (or refuses) file list publications
- Sends available file names to registered users
  - retrieve_all
  - retrieve (one)
- Respond (or refuse) to searches of file names
- Communicates with clients over UDP


# Client Design
- Send registration requests to server
- Runs as a daemon, plus a command line to the client/peer daemon
- Keep track of local files (all in one folder)
- Publish info about local files to server (tries several times before giving up)
- Send request to remove file from server list (if deleted locally? why not just publish new list of files?)
- Send request to server to get information about the files available from other peers
- Downloads files from peers
- Sends files on request to peers
- (Mobility) updates IP / UDP socket / TCP socket if they have changed
- Communicates with server over UDP
- Communicates with other clients (peers) over TCP



