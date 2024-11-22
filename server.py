#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading
import json
from database import database

IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"



### to handle the clients
def handle_client (conn,addr):

    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server, if you don't have an account, please create one by entering SIGNUP".encode(FORMAT))

    def sendToClient(msg):
        conn.send(msg.encode(FORMAT))

    while True:

        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
       
        send_data = "OK@"

        if cmd == "LOGOUT":
            break

        elif cmd == "TASK": 
            send_data += "LOGOUT from the server.\n"
            send_data += "SIGNUP for the server.\n"

            conn.send(send_data.encode(FORMAT))
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
                send_data += "Account creation successful."
                conn.send(send_data.encode(FORMAT))
            else:
                print(f"[EXISTING USER] {username} account not created.")
                send_data += "[ERROR] This account already exists."
                conn.send(send_data.encode(FORMAT))


        else:
            send_data += "[ERROR] Invalid command.\n"
            conn.send(send_data.encode(FORMAT))








    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()

