import os
import socket
import ssl
import logging
import pprint
import time

# IP = "192.168.1.101"  # Use localhost for testing
IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024  # Buffer size in bytes
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

logging.basicConfig(level=logging.DEBUG)
fileName = 'to_be_chosen.jpg'
fileToSend = open(fileName, 'rb');
filedata = fileToSend.read(1024)



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False  # Skip hostname verification (useful for localhost testing)
    context.load_verify_locations("cert.pem")  # Load the server certificate
    context.set_ciphers('ALL')
    with context.wrap_socket(client, server_hostname='localhost') as ssock:
        ssock.connect(ADDR)
        while True:  ### multiple communications
            data = ssock.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split("@")
            if cmd == "OK":
                print(f"{msg}")
            elif cmd == "DISCONNECTED":
                print(f"{msg}")
                break

            data = input("> ")
            data = data.split(" ")
            cmd = data[0]

            if cmd == "TASK":
                ssock.send(cmd.encode(FORMAT))
            if cmd == "UPLOAD":
                fileName = input("> ")
                if os.path.exists(fileName):
                    fileToSend = open(fileName, 'rb')
                    ssock.send(cmd.encode(FORMAT))  
                    while (filedata := fileToSend.read(SIZE)):  # Read and send file in chunks
                        ssock.send(filedata)
                    print(f"File '{fileName}' sent successfully.")
                else:
                    print(f"File '{fileName}' not found.")
            elif cmd == "LOGOUT":
                ssock.send(cmd.encode(FORMAT))
                break

        print("Disconnected from the server.")
        ssock.close()  ## close the connection


if __name__ == "__main__":
    main()