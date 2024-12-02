#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading
import json
from database import database
import ssl


IP = "localhost"
PORT = 4450  # listening on this port
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"


### to handle the clients
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(
        "OK@Welcome to the server, if you don't have an account, please create one by entering SIGNUP".encode(FORMAT))

    def sendToClient(msg):
        conn.send(msg.encode(FORMAT))

    while True:

        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        if cmd == "LOGOUT":  # If LOGOUT is received from client, then send client DISCONNECTED@ message
            print(f"{addr} requested to LOGOUT.")  # This is for the server
            conn.send("DISCONNECTED@".encode(FORMAT))  # Exit the loop and disconnect the client.
            break
        elif len(str.encode(cmd)) > 0:
            if cmd == "TASK":  # If TASK is received from client, send the following message
                sendToClient("LOGOUT from the server. \nSIGNUP for the server.")
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

        elif cmd == "LOGIN":
            # Getting login credentials from the user.
            username = conn.recv(SIZE).decode(FORMAT)
            password = conn.recv(SIZE).decode(FORMAT)
            print("[ACCOUNT LOGIN] Checking credentials...")

            # If the user does not exist in the account directory,
            # make a directory folder for that user, then cd them into it
            user = database.checkForExistingUser(username)

            if user is not None:
                print(f"[ACCOUNT LOGIN] User {username} found successfully, checking password...")

                if user["password"] == password:
                    print(f"[ACCOUNT LOGIN] User {username} credentials valid, user authenticated.")

                    # Creating user directory from username
                    user_dir = os.path.join("user_files", username)
                    if not os.path.exists(user_dir):
                        os.makedirs(user_dir)

                    # Server State set to Authenticated

                    current_dir = user_dir

                    sendToClient(f"OK@Welcome to your directory {username}!\n" +
                                 f"Please enter TASK for a list of user commands.\n" +
                                 f"Current Directory: {current_dir}")

                    while True:

                        sendToClient(f"PRINT@Current Directory: {current_dir}")

                        user_cmd = conn.recv(SIZE).decode(FORMAT)
                        if user_cmd == "LOGOUT":
                            break

                        elif user_cmd == "ls":
                            files = os.listdir(current_dir)
                            if files:
                                file_list = "\n".join(files)
                                sendToClient(f"OK@{file_list}")
                            else:
                                sendToClient("OK@no files")


                        # TODO: make this shit work
                        elif user_cmd.startswith("cd"):

                            path = user_cmd.split(" ", 1)[1].strip()

                        else:
                            sendToClient("OK@[ERROR] Invalid command.\n")





                else:
                    print(f"[ACCOUNT LOGIN] User {username} password was invalid.")
                    sendToClient("OK@Invalid password, please try again.")
                    continue
            else:
                print(f"[ACCOUNT LOGIN] User {username} does not exist.")
                sendToClient("OK@User does not exist.")
                continue





        else:
            send_data += "[ERROR] Invalid command.\n"
            conn.send(send_data.encode(FORMAT))

    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## used IPV4 and TCP connection
    server.bind(ADDR)  # bind the address
    server.listen()  ## start listening
    print(f"server is listening on {IP}: {PORT}")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="private.key")

    context.set_ciphers('ALL')
    context.set_servername_callback(lambda s, c, h: print(f'SSL Handshake with client: {h}'))
    with context.wrap_socket(server, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept() ### accept a connection from a client
            thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
            thread.start()


if __name__ == "__main__":
    main()

