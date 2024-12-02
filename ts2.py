#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import threading
import ssl
import time
import json
import matplotlib.pyplot as plt

IP = "localhost"
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
    plt.show()


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
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"Receiving file from {addr} with filename {filename}")

            start_time = time.time()
            bytes_received = 0

            if os.path.exists(f"received_{filename}"):
                base_name, ext = os.path.splitext(filename)
                counter = 1
                new_file_name = f"received_{base_name}_copy{ext}"
                while os.path.exists(new_file_name):
                    new_file_name = f"received_{base_name}_copy{counter}{ext}"
                    counter += 1
                filename = new_file_name

            with open(f"received_{filename}", "wb") as f:
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

            print(f"File {filename} received successfully. Transfer time: {transfer_time}s. Rate: {data_rate} bytes/s.")
            log_to_file()

            plot_graph()
        elif cmd == "DOWNLOAD":
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"Preparing to send file {filename} to {addr}")

            try:
                start_time = time.time()
                bytes_sent = 0

                with open(filename, "rb") as fileToSend:
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

                print(f"File {filename} sent successfully. Transfer time: {transfer_time}s. Rate: {data_rate} bytes/s.")
                log_to_file()
                plot_graph()
            except FileNotFoundError:
                conn.send("ERROR@File not found".encode(FORMAT))
                print(f"File {filename} not found.")

        elif cmd == "DELETE":
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"Deleting file {filename} requested by {addr}")

            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    conn.send("OK".encode(FORMAT))
                    print(f"File {filename} deleted successfully.")
                else:
                    conn.send("ERROR@File not found".encode(FORMAT))
                    print(f"File {filename} not found.")
            except Exception as e:
                conn.send(f"ERROR@{str(e)}".encode(FORMAT))
                print(f"Error deleting file {filename}: {str(e)}")
        elif cmd == "TASK":
            send_data += "LOGOUT from the server.\n"
            conn.send(send_data.encode(FORMAT))

    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print(f"Server is listening on {IP}: {PORT}")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="private.key")
    context.set_ciphers('ALL')
    context.set_servername_callback(lambda s, c, h: print(f'SSL Handshake with client: {h}'))

    with context.wrap_socket(server, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    main()
