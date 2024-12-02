#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading
from database import database

IP = "localhost"
PORT = 4450  # listening on this port
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"


def sendToClient(conn, msg):
    cmd, message = msg.split("@")
    if cmd == "PRINT":
        print(message)
    elif cmd == "FLORIDA":
        print(message)
    else:
        send_data = "OK@" + message
        conn.send(send_data.encode(FORMAT))


# to handle the clients
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))



    while True:
        data = conn.recv(SIZE).decode(FORMAT)

        cmd = data

        if cmd == "LOGOUT":  # If LOGOUT is received from client, then send client DISCONNECTED@ message
            print(f"{addr} requested to LOGOUT.")  # This is for the server
            conn.send("DISCONNECTED@".encode(FORMAT))  # Exit the loop and disconnect the client.
            break
        elif len(str.encode(cmd)) > 0:
            if cmd == "TASK":  # If TASK is received from client, send the following message
                sendToClient(conn, "LOGOUT from the server. \nSIGNUP for the server.")
            elif cmd == "SIGNUP":
                print("[ACCOUNT CREATION] Starting process...")
                username = conn.recv(SIZE).decode(FORMAT)
                password = conn.recv(SIZE).decode(FORMAT)

                user = {
                    "username": username,
                    "password": password
                }

                if not database.checkForExistingUser(username):
                    database.saveUser(user)
                    print(f"[ACCOUNT CREATION] {username} created successfully.")
                    sendToClient(conn, "Account creation successful.")
                else:
                    print(f"[EXISTING USER] {username} account not created.")
                    sendToClient(conn, "[ERROR] This account already exists.")
            else:
                sendToClient(conn, "[Error] Invalid command.")

    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## used IPV4 and TCP connection
    server.bind(ADDR)  # bind the address
    server.listen()  ## start listening
    print(f"server is listening on {IP}: {PORT}")

    while True:
        conn, addr = server.accept()  ### accept a connection from a client
        thread = threading.Thread(target=handle_client, args=(conn, addr))  ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()
