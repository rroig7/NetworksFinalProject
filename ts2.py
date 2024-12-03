#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
import os
import socket
import threading
import json
from database import database
import ssl

IP = "10.221.87.26"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"
LOG_FILE = "server_log.json"

network_stats = {
    "uploads": [],
    "downloads": []
}


def log_to_file():
    with open(LOG_FILE, 'w') as log_file:
        json.dump(network_stats, log_file, indent=4)


def plot_graph():
    uploads = [entry["rate"] for entry in network_stats["uploads"]]
    downloads = [entry["rate"] for entry in network_stats["downloads"]]
    upload_times = [entry["time"] for entry in network_stats["uploads"]]
    download_times = [entry["time"] for entry in network_stats["downloads"]]

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    ax[0].plot(upload_times, uploads, label='Upload Rate (bytes/s)', color='b')
    ax[0].set_title("Upload Rate Over Time")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Rate (bytes/s)")
    ax[0].legend()

    ax[1].plot(download_times, downloads, label='Download Rate (bytes/s)', color='r')
    ax[1].set_title("Download Rate Over Time")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Rate (bytes/s)")
    ax[1].legend()

    plt.tight_layout()
    plt.pause()


def handle_client(conn, addr):
    def sendToClient(msg):
        conn.send(msg.encode(FORMAT))


    print(f"[NEW CONNECTION] {addr} connected.")
    sendToClient("OK@Welcome to the server, enter TASK for the list of commands")

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        if cmd == "LOGOUT":  # If LOGOUT is received from client
            print(f"{addr} requested to LOGOUT.")  # This is for the server
            break
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
                sendToClient("OK@Account creation successful.")
            else:
                print(f"[EXISTING USER] {username} account not created.")
                sendToClient("OK@[ERROR] Username already exists.")
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

                    dir_depth = 0

                    while True:
                        # To track how deep the user is in the file tree


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


                        elif user_cmd.startswith("cd"):



                            requested_sub_dir = user_cmd.split(" ", 1)[-1].strip()

                            requested_path = current_dir + "\\" + requested_sub_dir

                            if user_cmd == "cd ..":
                                if dir_depth > 0:
                                    # Split the current_dir by the backslash, remove the last part, and rejoin
                                    temp = current_dir.rstrip("\\").rsplit("\\", 1)
                                    current_dir = temp[0] if len(temp) > 1 else "\\"
                                    dir_depth -= 1
                                    sendToClient("OK@Directory changed.")
                                else:
                                    sendToClient("OK@You are at the root directory already.")


                            else:

                                if os.path.exists(requested_path):
                                    dir_depth += 1
                                    current_dir = requested_path
                                    sendToClient("OK@Directory changed successfully.")

                                else:
                                    sendToClient("OK@File path does not exist.")
                                    continue

                        elif user_cmd == "UPLOAD":
                            filename = conn.recv(SIZE).decode(FORMAT)  # will receive file name from client
                            print(f"Receiving file from {addr} with filename {filename}")  # Prints to server

                            start_time = time.time()  # starts a timer
                            bytes_received = 0  # Will track how many bytes were received from client

                            if os.path.exists(f"{current_dir}/received_{filename}"):  # runs if file already exists
                                base_name, ext = os.path.splitext(
                                    filename)  # splits the file between its extension and name
                                counter = 1
                                new_file_name = f"received_{base_name}_copy{ext}"
                                while os.path.exists(new_file_name):
                                    new_file_name = f"received_{base_name}_copy{counter}{ext}"
                                    counter += 1  # for every copy found, add 1 to the counter
                                filename = new_file_name  # names the copy as "received_filename_copy#.ext"

                            with open(f"{current_dir}/received_{filename}", "wb") as f:
                                while True:
                                    filedata = conn.recv(SIZE)
                                    if filedata == b'EOF':
                                        break
                                    f.write(filedata)
                                    bytes_received += len(filedata)

                            end_time = time.time()
                            transfer_time = end_time - start_time
                            data_rate = bytes_received / transfer_time

                            network_stats["uploads"].append({
                                "filename": filename,
                                "time": transfer_time,
                                "rate": data_rate
                            })

                            sendToClient(
                                f"File {filename} received successfully. Transfer time: {transfer_time}s. Rate: {data_rate} bytes/s.")
                            print(f"File {filename} received successfully. Transfer time: {transfer_time}s.")
                            log_to_file()

                            plot_graph()
                        elif user_cmd == "DOWNLOAD":
                            filename = conn.recv(SIZE).decode(FORMAT)
                            print(f"Preparing to send file {filename} to {addr}")

                            try:
                                start_time = time.time()
                                bytes_sent = 0

                                with open(f"{current_dir}/{filename}", "rb") as fileToSend:
                                    while True:
                                        filedata = fileToSend.read(SIZE)
                                        if not filedata:
                                            break
                                        conn.send(filedata)
                                        bytes_sent += len(filedata)

                                    conn.send(b'EOF')

                                end_time = time.time()
                                transfer_time = end_time - start_time
                                data_rate = bytes_sent / transfer_time

                                network_stats["downloads"].append({
                                    "filename": filename,
                                    "time": transfer_time,
                                    "rate": data_rate
                                })

                                print(
                                    f"File {filename} sent successfully. Transfer time: {transfer_time}s. Rate: {data_rate} bytes/s.")
                                sendToClient(
                                    f"File {filename} sent successfully. Transfer time: {transfer_time}s. Rate: {data_rate} bytes/s.")
                                log_to_file()
                                plot_graph()
                            except FileNotFoundError:
                                conn.send("ERROR@File not found".encode(FORMAT))
                                print(f"File {filename} not found.")

                        elif cmd == "DELETE":
                            filename = conn.recv(SIZE).decode(FORMAT)
                            print(f"Deleting file {filename} requested by {addr}")

                            try:
                                if os.path.exists(f"{current_dir}/{filename}"):
                                    os.remove(f"{current_dir}/{filename}")
                                    conn.send("OK".encode(FORMAT))
                                    print(f"File {filename} deleted successfully.")
                                else:
                                    conn.send("ERROR@File not found".encode(FORMAT))
                                    print(f"File {filename} not found.")
                            except Exception as e:
                                conn.send(f"ERROR@{str(e)}".encode(FORMAT))
                                print(f"Error deleting file {filename}: {str(e)}")

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

        elif cmd == "TASK":  # If TASK is received from client, send the following message
            sendToClient("OK@LOGOUT from the server. \nSIGNUP for the server.\nLOGIN to the server\n"
                         "UPLOAD to the server\nDOWNLOAD from the server\nDELETE from the server\n"
                         "TASK to list these commands")
        else:
            # Catches any cmd that is not explicitly stated
            sendToClient("OK@[ERROR] Invalid command.\n")

    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET is IPV4 and  SOCK_STREAM is TCP connection
    server.bind(ADDR) # This will bind the server to this IP address
    server.listen() # Server starts listening for connections

    print(f"Server is listening on {IP}: {PORT}")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) # ASSUMPTION: A SSL server protocal is called as a framework
    context.load_cert_chain(certfile="cert.pem", keyfile="private.key") # Client receives cert.pem, and server uses private.key

    context.set_ciphers('ALL') # No idea
    context.set_servername_callback(lambda s, c, h: print(f'SSL Handshake with client: {h}')) # No idea

    with context.wrap_socket(server, server_side=True) as ssock: # ASSUMPTION: This will wrap any client-server connection with SSL
        while True:
            conn, addr = ssock.accept() # Accepts a socket connection from client
            thread = threading.Thread(target=handle_client, args=(conn, addr)) # Add a thread to the client
            thread.start() # starts the connection with this thread


if __name__ == "__main__":
    main()
