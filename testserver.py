
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading
import ssl


IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

### to handle the clients

def client_uploads(stream, f):
	while True:
        	filedata = conn.recv(1024)
	        if not data:
	            break
	        f.write(data)  # Write received data to file
        f.close()


def handle_client (conn,addr):


    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))

    while True:
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        if cmd == "LOGOUT":
            break
        if cmd == "UPLOAD":
            index = 0
            f = open(f'decrypted#{index}.bin', 'wb')
            print(f"Receiving file from {addr}")
            try:
                threading.Thread(target=client_uploads, args=(conn, f)).start()
            except Exception as e:
                print(f"Error: {e}")
                break
          	except Exception:
          			print('\n Error in handling client\n')
          			break

        elif cmd == "TASK":
            send_data += "LOGOUT from the server.\n"

            conn.send(send_data.encode(FORMAT))



    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening

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
