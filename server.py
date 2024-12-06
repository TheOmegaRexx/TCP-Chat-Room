import threading
import socket

host = "127.0.0.1"  # localhost IP address
port = 44444  # Port to listen for connections

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))  # Bind the server to the host and port
server.listen()  # Start listening for incoming connections

clients = []  # List to store connected clients
nicknames = []  # List to store nicknames of the connected clients

# Function to broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle communication with each client
def handle(client):
    while True:
        try:
            # Receive messages from the client
            message = client.recv(1024)
            broadcast(message)  # Broadcast the message to all other clients
        except:
            # Handle client disconnections
            index = clients.index(client)  # Find the index of the disconnected client
            clients.remove(client)  # Remove the client from the list of connected clients
            client.close()  # Close the connection to the client
            nickname = nicknames[index]  # Get the nickname of the disconnected client
            nicknames.remove(nickname)  # Remove the nickname from the list
            # Broadcast a message notifying other clients of the disconnection
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            break

# Function to receive new client connections
def receive():
    while True:
        # Accept new client connections
        client, adress = server.accept()
        print(f"New connection made: {str(adress)}")

        # Send a prompt asking for a nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")  # Receive the nickname from the client
        nicknames.append(nickname)  # Add the nickname to the list of nicknames
        clients.append(client)  # Add the client to the list of connected clients

        print(f"Nickname of the client is {nickname}!")
        # Broadcast a message that a new client has joined the chat
        broadcast(f"{nickname} joined the chat!".encode("ascii"))

        # Send a welcome message to the client
        client.send("Connected to the server!".encode("ascii"))

        # Start a new thread to handle communication with the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Print that the server is running and waiting for connections
print("Server is running...")
receive()  # Start receiving client connections
