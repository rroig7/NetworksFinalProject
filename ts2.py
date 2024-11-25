#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading
import ssl

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        if cmd == "LOGOUT":
            break
        if cmd == "UPLOAD":

            filename = conn.recv(SIZE).decode(FORMAT)  # Receive the file name
            print(f"Receiving file from {addr} with filename {filename}")
            with open(f"received_{filename}", "wb") as f:
                while True:
                    filedata = conn.recv(SIZE)
                    if filedata == b'EOF':
                        break
                    f.write(filedata)
                    #print(filedata)
            print(f"File {filename} received successfully.")
        elif cmd == "DOWNLOAD":
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"Preparing to send file {filename} to {addr}")

            try:
                with open(filename, "rb") as fileToSend:

                    while True:
                        filedata = fileToSend.read(SIZE)
                        if not filedata:
                            break
                        conn.send(filedata)
                        print(f"Sent chunk of {len(filedata)} bytes.")
                    conn.send(b'EOF')
                    print(f"File {filename} sent successfully.")
            except FileNotFoundError:
                conn.send("ERROR@File not found".encode(FORMAT))
                print(f"File {filename} not found.")

        elif cmd == "TASK":
            send_data += "LOGOUT from the server.\n"
            conn.send(send_data.encode(FORMAT))

    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Used IPV4 and TCP connection
    server.bind(ADDR)  # Bind the address
    server.listen()  # Start listening

    print(f"Server is listening on {IP}: {PORT}")

    # SSL Setup
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="private.key")
    context.set_ciphers('ALL')
    context.set_servername_callback(lambda s, c, h: print(f'SSL Handshake with client: {h}'))

    # Wrap the server socket with SSL
    with context.wrap_socket(server, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()  # Accept a connection from a client
            thread = threading.Thread(target=handle_client, args=(conn, addr))  # Assign a thread for each client
            thread.start()


if __name__ == "__main__":
    main()
