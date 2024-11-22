# Author : Ayesha S. Dina

import os
import socket

# IP = "192.168.1.101" #"localhost"
IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024  ## byte .. buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    while True:  ### multiple communications
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        if cmd == "OK":
            print(f"{msg} whatsup")
        elif cmd == "DISCONNECTED":
            print(f"{msg} x")
            break

        data = input("> ").strip()  # Strip any leading/trailing spaces
        if not data:  # If input is empty, continue to next iteration
            continue
        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))


    print("Disconnected from the server.")
    client.close()  ## close the connection


if __name__ == "__main__":
    main()
