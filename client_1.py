# Author : Ayesha S. Dina

import os
import socket
import ssl
import logging
import hashlib


# IP = "192.168.1.101" #"localhost"
IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024  ## byte .. buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
logging.basicConfig(level=logging.DEBUG)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    while True:  # multiple communications
        data = client.recv(SIZE).decode(FORMAT)  # data received will be like: OK@message
        cmd, msg = data.split("@")  # data will be split as: cmd:OK and msg:message

        if cmd == "OK": # If the cmd after the split is OK, print the message it received from the server, loop stays the same
            print(f"{msg}")
        elif cmd == "DISCONNECTED": # If the server tells the client to disconnect, then disconnect
            print(f"{msg}")
            break
        elif cmd == "PRINT": # only prints out the message, and does a new loop
            print(f"{msg}")
            continue

        data = input("> ").strip()  # Strip any leading/trailing spaces

        if data == "": # if the message from the server is empty, send a message stating it is empty, loop again
            client.send("EMPTY".encode(FORMAT))
            continue

        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":  # This will command server to return possible task the client can do
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT": # Tells the server it is disconnecting, and breaks the loop
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "SIGNUP": # Tells the server, that user is signing up, and sends the username and password used
            client.send(cmd.encode(FORMAT))

            username = input(f"Please enter your username: ")
            password = input("Please enter your password: ")
            hashedPassword = hashlib.sha256(password.encode(FORMAT)).hexdigest()

            client.send(username.encode(FORMAT))
            client.send(hashedPassword.encode(FORMAT))

            print("Waiting for response...")

        elif cmd == "LOGIN": # Tells the server, that user is logging in, with their username and password
            client.send(cmd.encode(FORMAT))

            username = input(f"Please enter your username: ")
            password = input("Please enter your password: ")
            hashedPassword = hashlib.sha256(password.encode(FORMAT)).hexdigest()

            client.send(username.encode(FORMAT))
            client.send(hashedPassword.encode(FORMAT))

            print("Waiting for response...")

        else: # sends a message to server, used to catch any non options
            client.send(cmd.encode(FORMAT))
            continue




    # Prints when the loop has ended
    print("Disconnected from the server.")
    client.close()  # close the connection


if __name__ == "__main__":
    main()
