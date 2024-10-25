import threading
import socket

# Get nickname input from the user
nickname = input("Choose a nickname: ")

# Create a socket object for the client using IPv4 (AF_INET) and TCP (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server at localhost (127.0.0.1) on port 8227
client.connect(('127.0.0.1', 8227))

def receive():
    """
    Function to continuously listen for messages from the server.
    Handles receiving the nickname request and printing incoming messages.
    """
    while True:
        try:
            # Receiving a message from the server
            message = client.recv(1024).decode('ascii')

            # If the server requests a nickname, send it
            if message == 'NICKNAME?':
                client.send(nickname.encode('ascii'))
            else:
                # Print any other message received from the server
                print(message)
        except Exception as e:
            # Handle errors and close the connection
            print("Connection closed due to an error:", e)
            client.close()
            break

def write():
    """
    Function to send messages to the server. It continually waits for user input
    and sends the message to the server, prefixed by the user's nickname.
    """
    while True:
        # Continuously get input from the user
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# Start the thread responsible for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start the thread responsible for sending messages
write_thread = threading.Thread(target=write)
write_thread.start()
