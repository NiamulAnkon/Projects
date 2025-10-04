import json
import os
from config import USER_DB

# Ensure the database file exists
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    
    if username in users:
        return {"status": "error", "message": "Username already exists."}
    
    users[username] = {"password": password}
    save_users(users)
    
    return {"status": "success", "message": "Registration successful!"}

def authenticate_user(username, password):
    users = load_users()
    
    if username in users and users[username]["password"] == password:
        return {"status": "success", "message": "Login successful!"}
    
    return {"status": "error", "message": "Invalid credentials!"}
