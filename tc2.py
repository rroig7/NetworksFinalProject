import os
import socket
import ssl
import logging
import time

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

logging.basicConfig(level=logging.DEBUG)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.load_verify_locations("cert.pem")
    context.set_ciphers('ALL')
    with context.wrap_socket(client, server_hostname='localhost') as ssock:
        ssock.connect(ADDR)
        while True:
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
                download_speed = file_size / elapsed_time / 1024  # KB/s
                print(f"File '{fileName}' downloaded successfully in {elapsed_time:.2f} seconds.")
                print(f"Download speed: {download_speed:.2f} KB/s")

            elif cmd == "DELETE":
                fileName = input("Enter the filename to delete: ")
                ssock.send(cmd.encode(FORMAT))
                ssock.send(fileName.encode(FORMAT))

                response = ssock.recv(SIZE).decode(FORMAT)
                if response == "OK":
                    print(f"File '{fileName}' deleted successfully.")
                else:
                    print(f"Error: {response}")

            elif cmd == "LOGOUT":
                ssock.send(cmd.encode(FORMAT))
                break

        print("Disconnected from the server.")
        ssock.close()

if __name__ == "__main__":
    main()
