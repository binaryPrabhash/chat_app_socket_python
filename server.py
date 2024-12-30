import socket
import threading
import signal
import sys

def handle_client(client_socket):
    client_socket.send("Enter your username: ".encode("utf-8"))
    username = client_socket.recv(1024).decode("utf-8")

    print(f"{username} joined the chat")
    broadcast(f"{username} joined the chat", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"    {username}: {message}")
            broadcast(f"    {username}: {message}", client_socket)
        except:
            break
    
    client_socket.close()
    print(f"{username} disconnected")
    broadcast(f"{username} left the chat.", client_socket)
    clients.remove(client_socket)

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                clients.remove(client)

def signal_handler(sig, frame):
    for client in clients:
        try:
            client.close()
        except:
            pass

    server.close()
    sys.exit(0)

server_ip = "0.0.0.0" # listen on all available interfaces
server_port = 5555    # port to listen on 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

print(f"Server started on {server_ip}:{server_port}")

clients = []

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

while True:
    try:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    except Exception as e:
        print(f"Error: {e}")
