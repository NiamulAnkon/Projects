import sqlite3
from cryptography.fernet import Fernet

# Generate a key (run once, save securely; use same key for decryption)
# Uncomment these lines to generate a new key
key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)

def load_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Encryption key file not found! Generate one and save it as 'key.key'.")
        exit()

key = load_key()
cipher = Fernet(key)

def initialize_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_password(account_name, username, password):
    encrypted_password = cipher.encrypt(password.encode()).decode()
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (account_name, username, password) VALUES (?, ?, ?)",
                   (account_name, username, encrypted_password))
    conn.commit()
    conn.close()
    print("Password saved successfully!")

def fetch_password(account_name):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE account_name=?", (account_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        username, encrypted_password = result
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        return username, decrypted_password
    return None

def main():
    initialize_db()
    print("Welcome to Password Keeper!")
    master_password = input("Enter your master password: ")

    if master_password != "hi":  
        print("Incorrect master password! Exiting...")
        return

    while True:
        print("\nOptions:")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            account_name = input("Enter the account name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(account_name, username, password)

        elif choice == "2":
            account_name = input("Enter the account name to retrieve: ")
            result = fetch_password(account_name)
            if result:
                username, password = result
                print(f"Username: {username}\nPassword: {password}")
            else:
                print("Account not found.")

        elif choice == "3":
            print("Exiting Password Keeper. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
