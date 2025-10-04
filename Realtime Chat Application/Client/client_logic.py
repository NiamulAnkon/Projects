import socket
import json
from config import SERVER_IP, SERVER_PORT

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

def authenticate_user(username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))
        
        credentials = {"action": "login", "username": username, "password": password}
        client.send(json.dumps(credentials).encode())

        response = client.recv(1024).decode()
        client.close()

        return json.loads(response)
    except Exception as e:
        return {"status": "error", "message": str(e)}
def signup_user(username, password):
    """ Sends signup request to the server """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))

        # Create signup request
        request = {"action": "signup", "username": username, "password": password}
        client.send(json.dumps(request).encode())

        # Receive response
        response = json.loads(client.recv(1024).decode())
        client.close()
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}

def send_message(username, message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))

        data = {"action": "message", "username": username, "message": message}
        client.send(json.dumps(data).encode())

        response = client.recv(1024).decode()
        client.close()

        return json.loads(response)
    except Exception as e:
        return {"status": "error", "message": str(e)}
