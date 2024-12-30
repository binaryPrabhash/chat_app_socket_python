import socket
import threading
import signal
import sys

def receive_messages():
    try:
        while True:
            message = client.recv(1024).decode("utf-8")
            print("")
            print(message)
    except OSError:
        pass


def signal_handler(sig, frame):
    client.close()
    sys.exit(0)

server_ip = "127.0.0.1" # IP of the server
server_port = 5555      # Port the server is listening on

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

signal.signal(signal.SIGINT, signal_handler) # CTRL+C
signal.signal(signal.SIGTERM, signal_handler) # Termination request
signal.signal(signal.SIGHUP, signal_handler)  # Hangup signal, terminal close

client.connect((server_ip, server_port)) 
print(f"Connected to server {server_ip}:{server_port}")
    
thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

while True:
    message = input("")
    client.send(message.encode("utf-8")) 
