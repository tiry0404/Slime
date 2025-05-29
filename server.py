import socket
import threading

HOST = ''
PORT = 5000
clients = {}
nicknames = {}

def broadcast(msg, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            try:
                client.send(msg.encode('utf-8'))
            except:
                remove_client(client)

def handle_client(client_socket):
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames[client_socket] = nickname
        welcome_message = f"{nickname} has joined the chat."
        print(welcome_message)
        broadcast(welcome_message, client_socket)
        clients[client_socket] = client_socket.getpeername()

        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                full_msg = f"{nickname}: {msg}"
                print(full_msg)
                broadcast(full_msg, client_socket)
            else:
                break
    except:
        pass
    finally:
        remove_client(client_socket)

def remove_client(client_socket):
    if client_socket in clients:
        print(f"{nicknames[client_socket]} has left the chat.")
        broadcast(f"{nicknames[client_socket]} has left the chat.")
        client_socket.close()
        del clients[client_socket]
        del nicknames[client_socket]

def accept_connections():
    server.listen()
    print(f"Server running on port {PORT}")
    while True:
        client_socket, addr = server.accept()
        if addr[0].startswith("192.168."):
            client_socket.send("NICK".encode('utf-8'))
            threading.Thread(target=handle_client, args=(client_socket,)).start()
        else:
            client_socket.send("Access denied. Same WiFi required.".encode('utf-8'))
            client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

accept_connections()