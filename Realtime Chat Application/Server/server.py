import socket
import threading
import json
from auth_handler import authenticate_user, register_user
from config import SERVER_IP, SERVER_PORT

clients = []  # Stores active client connections

def broadcast_message(message, sender_socket):
    """Sends a message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    """Handles communication with a single client."""
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            request = json.loads(data)
            action = request.get("action")

            if action == "login":
                response = authenticate_user(request["username"], request["password"])
                client_socket.send(json.dumps(response).encode())

            elif action == "register":
                response = register_user(request["username"], request["password"])
                client_socket.send(json.dumps(response).encode())

            elif action == "message":
                message = f"{request['username']}: {request['message']}"
                print(f"[MESSAGE] {message}")
                broadcast_message(message, client_socket)

        except Exception as e:
            print(f"[ERROR] {addr}: {e}")
            break

    print(f"[DISCONNECTED] {addr} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    """Starts the chat server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    
    print(f"[SERVER STARTED] Listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
