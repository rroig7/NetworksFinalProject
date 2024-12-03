import time
import os
import socket
import ssl
import logging
import hashlib

# IP = "35.136.49.5"
IP = "localhost"
PORT = 7777
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

logging.basicConfig(level=logging.DEBUG)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a client socket, using IPv4 and TCP
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.load_verify_locations("cert.pem")
    context.set_ciphers('ALL')
    with context.wrap_socket(client, server_hostname=IP) as ssock:
        ssock.connect(ADDR) # connects to server IP address, and port
        while True:
            data = ssock.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split("@")
            if cmd == "OK":
                print(f"{msg}")
            elif cmd == "DISCONNECTED":
                print(f"{msg}")
                break
            elif cmd == "PRINT":
                print(f"{msg}")
                continue

            data = input("> ").strip()  # Strip any leading/trailing spaces

            if data == "":  # if the message from the server is empty, send a message stating it is empty, loop again
                ssock.send("EMPTY".encode(FORMAT))
                continue
            data = data.upper()
            cmd = str(data)

            if cmd == "TASK":
                ssock.send(cmd.encode(FORMAT))
            elif cmd == "UPLOAD":
                fileName = input("Enter the filename to upload: ")
                if os.path.exists(fileName):
                    ssock.send(cmd.encode(FORMAT))
                    ssock.send(fileName.encode(FORMAT))

                    start_time = time.time()
                    with open(fileName, 'rb') as fileToSend:
                        while (filedata := fileToSend.read(SIZE)):
                            ssock.send(filedata)
                        ssock.send(b'EOF')
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    file_size = os.path.getsize(fileName)
                    upload_speed = file_size / elapsed_time / 1024  # KB/s
                    print(f"File '{fileName}' sent successfully in {elapsed_time:.2f} seconds.")
                    print(f"Upload speed: {upload_speed:.2f} KB/s")

            elif cmd == "DOWNLOAD":
                fileName = input("Enter the filename to download: ")
                ssock.send(cmd.encode(FORMAT))
                ssock.send(fileName.encode(FORMAT))
                if os.path.exists(f"downloaded_{fileName}"):
                    base_name, ext = os.path.splitext(fileName)
                    counter = 1
                    new_file_name = f"downloaded_{base_name}_copy{ext}"
                    while os.path.exists(new_file_name):
                        new_file_name = f"downloaded_{base_name}_copy{counter}{ext}"
                        counter += 1
                    fileName = new_file_name
                start_time = time.time()
                with open(f"downloaded_{fileName}", 'wb') as fileToWrite:
                    while True:
                        filedata = ssock.recv(SIZE)
                        if filedata == b'EOF':
                            print(f"Download complete for {fileName}")
                            break
                        fileToWrite.write(filedata)

                end_time = time.time()
                elapsed_time = end_time - start_time
                file_size = os.path.getsize(f"downloaded_{fileName}")
                download_speed = (file_size + 0.0001) / elapsed_time / (1024 * 1024) # MB/s
                print(f"File '{fileName}' downloaded successfully in {elapsed_time:.2f} seconds.")
                print(f"Download speed: {download_speed:.2f} MB/s")

            elif cmd == "DELETE":
                fileName = input("Enter the filename to delete: ")
                ssock.send(cmd.encode(FORMAT))
                ssock.send(fileName.encode(FORMAT))

                response = ssock.recv(SIZE).decode(FORMAT)
                if response == "OK":
                    print(f"File '{fileName}' deleted successfully.")
                else:
                    print(f"Error: {response}")

            elif cmd == "SIGNUP":  # Tells the server, that user is signing up, and sends the username and password used
                ssock.send(cmd.encode(FORMAT))

                username = input(f"Please enter your username: ")
                password = input("Please enter your password: ")
                hashedPassword = hashlib.sha256(password.encode(FORMAT)).hexdigest()

                ssock.send(username.encode(FORMAT))
                ssock.send(hashedPassword.encode(FORMAT))

                print("Waiting for response...")

            elif cmd == "LOGIN":  # Tells the server, that user is signing up, and sends the username and password used
                ssock.send(cmd.encode(FORMAT))

                username = input(f"Please enter your username: ")
                password = input("Please enter your password: ")
                hashedPassword = hashlib.sha256(password.encode(FORMAT)).hexdigest()

                ssock.send(username.encode(FORMAT))
                ssock.send(hashedPassword.encode(FORMAT))

                print("Waiting for response...")

            elif cmd == "LOGOUT":
                ssock.send(cmd.encode(FORMAT))
                break

            else:  # sends a message to server, used to catch any non options
                ssock.send(cmd.encode(FORMAT))
                continue

        print("Disconnected from the server.")
        ssock.close()

if __name__ == "__main__":
    main()
