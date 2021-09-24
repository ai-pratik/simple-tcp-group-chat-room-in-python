#implementing the server first.
# For this we will need to import two libraries,
# namely socket and threading.

import socket # used for the network connection
import threading #for performing various tasks at the same time.

#The next task is to define our connection data and to initialize our socket.
# We will need an IP-address for the host and a free port number for our server.

# Connection Data
host='127.0.0.1'#localhost
port=44446

# Starting Server
#The first one (AF_INET) indicates that we are using an internet socket rather than an unix socket. The second parameter stands for the protocol we want to use. SOCK_STREAM indicates that we are using TCP and not UDP.
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))#we bind it to our host and the specified port by passing a tuple that contains both value
server.listen()#We then put our server into listening mode, so that it waits for clients to connect.

# Lists For Clients and Their Nicknames
#At the end we create two empty lists, which we will use to store the connected clients and their nicknames later on.
clients=[]
nicknames=[]

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message) #What it does is just sending a message to each client that is connected and therefore in the clients list

# Handling Messages From Clients
#The function accepts a client as a parameter.
#Everytime a client connects to our server we run this function for it and it starts an endless loop.
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message=client.recv(1024)#receiving the message from the client
            broadcast(message)#broadcasting it to all connected clients
        except:
            # Removing And Closing Clients
            # Now if for some reason there is an error with the connection to this client,
            # we remove it and its nickname, close the connection and broadcast that this client has left the chat.
            # After that we break the loop and this thread comes to an end.
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client,address =server.accept()
        print(f"Connected with{str(address)}")

        # Request And Store Nickname
        #Once a client is connected it sends the string ‘NICK’ to it,
        #which will tell the client that its nickname is requested.
        client.send('NICK'.encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        #After that it waits for a response (which hopefully contains the nickname) and
        #appends the client with the respective nickname to the lists.
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f'nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat'.encode("ascii"))
        client.send('\nconnected to the server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

print("server is Listning !!!")
receive()

