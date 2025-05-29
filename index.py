import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg == 'NICK':
                sock.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except:
            print("Disconnected from server.")
            sock.close()
            break

def send_messages(sock):
    while True:
        msg = input()
        try:
            sock.send(msg.encode('utf-8'))
        except:
            break

nickname = input("Choose your nickname: ")
host = input("Enter server IP (LAN): ")
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(client_socket,))
send_thread.start()
