import threading
import socket

# Prompt the user to input a nickname
nickname = input("Type in a Nickname: ")

# Create a socket object for the client using IPv4 and TCP protocol
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server at the specified IP address and port
client.connect(("127.0.0.1", 44444))

# Function to handle receiving messages from the server


def receive():
    while True:
        try:
            # Receive message from server and decode it
            message = client.recv(1024).decode("ascii")

            # Check if the message is asking for a nickname, in which case we do nothing
            if message == "NICK":
                pass
            else:
                # Print the message from the server
                print(message)
        except:
            # If an error occurs, print an error message and close the connection
            print("An error occurred!")
            client.close()
            break

# Function to handle sending messages to the server


def write():
    while True:
        # Format the message to include the nickname
        message = f"{nickname}: {input('')}"

        # Send the formatted message to the server
        client.send(message.encode("ascii"))


# Create a thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Create a thread for writing and sending messages
write
