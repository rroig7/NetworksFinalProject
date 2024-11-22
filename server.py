#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading

IP = "localhost"
PORT = 4450  # listening on this port
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

active_connections = []


def print_connections():
    print("\n--- Active Connections ---")
    if len(active_connections) == 0:
        print("No active connections.")
    else:
        for conn in active_connections:
            addr = conn.getpeername()
            print(f"IP: {addr[0]}, Port: {addr[1]}")
    print("---------------------------\n")


### to handle the clients
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))
    active_connections.append(conn)
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        if data == "":
            continue

        # data = data.split("@")
        # print(f"{data} this is with data split\n")

        send_data = "OK@"

        cmd = data

        if cmd == "LOGOUT":
            print(f"{addr} requested to LOGOUT.")
            conn.send("DISCONNECTED@".encode(FORMAT))  # Exit the loop and disconnect the client.
            break
        if len(str.encode(cmd)) > 0:
            if cmd == "TASK":
                send_data += "LOGOUT from the server.\n"
                conn.send(send_data.encode(FORMAT))
            else:
                send_data += "Not a valid command"
                conn.send(send_data.encode(FORMAT))

    print(f"{addr} disconnected")
    active_connections.remove(conn)
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
