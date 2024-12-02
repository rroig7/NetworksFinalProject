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

        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break
        elif cmd == "PRINT":
            print(f"{msg}")
            continue

        data = input("> ").strip()  # Strip any leading/trailing spaces

        if data == "":
            client.send("EMPTY".encode(FORMAT))
            continue



        data = input("> ")
        if data == "":
            client.send("Not".encode(FORMAT))
        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":  # This will command server to return possible task the client can do
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":  # This will send to server a command to log out of the server
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "SIGNUP":
            client.send(cmd.encode(FORMAT))

            username = input(f"Please enter your username: ")
            password = input("Please enter your password: ")
            hashedPassword = hashlib.sha256(password.encode(FORMAT)).hexdigest()

            client.send(username.encode(FORMAT))
            client.send(hashedPassword.encode(FORMAT))

            print("Waiting for response...")

        elif cmd == "LOGIN":
            client.send(cmd.encode(FORMAT))

            username = input(f"Please enter your username: ")
            password = input("Please enter your password: ")
            hashedPassword = hashlib.sha256(password.encode(FORMAT)).hexdigest()

            client.send(username.encode(FORMAT))
            client.send(hashedPassword.encode(FORMAT))

            print("Waiting for response...")

        else:
            client.send(cmd.encode(FORMAT))
            continue





    print("Disconnected from the server.")
    client.close()  # close the connection


if __name__ == "__main__":
    main()
