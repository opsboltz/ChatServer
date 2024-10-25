import threading
import socket

# Server configuration: localhost (127.0.0.1) and port 8227
host = '127.0.0.1'
port = 8227

# Create a socket object for the server using IPv4 (AF_INET) and TCP (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the server to the host and port
server.bind((host, port))
# Start listening for incoming connections (no limit on the queue size)
server.listen()

clients = []  # List to store client connections
nicknames = []  # List to store nicknames of connected clients

def broadcast(message):
    """
    Broadcasts a message to all connected clients.
    """
    for client in clients:
        client.send(message)

def handle(client):
    """
    Handles communication with a specific client. This function runs in a loop,
    receiving messages from the client and broadcasting them to others.
    If an error occurs (e.g., the client disconnects), the client is removed.
    """
    while True:
        try:
            # Receive messages from the client and broadcast them to all clients
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            # Remove the client from the list and close the connection on error
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    """
    Accepts incoming client connections, requests their nicknames, and starts a new
    thread to handle communication with each client.
    """
    while True:
        # Accept a new client connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Ask for and receive the client's nickname
        client.send('NICKNAME?'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of {address} is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Start a new thread to handle this client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start the server and begin accepting connections
print("Server is listening...")
receive()
