
import socket
import threading

# Choosing Nickname
nickname=input("choose a nickname:")

# Connecting To Server
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',44446))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message=client.recv(1024).decode('ascii')
            if message=="NICK":
                client.send(nickname.encode('ascii'))
            else:
                print(message)
                #It constantly tries to receive messages and to print them onto the screen.
                #If the message is ‘NICK’ however, it doesn’t print it but it sends its nickname to the server
        except:
            # Close Connection When Error
            print("An error occured!!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message=f'{nickname}:{input("")}'
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread=threading.Thread(target=receive)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()
