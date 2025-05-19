import os, json, base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=100_000, backend=default_backend()
    )
    return kdf.derive(password.encode())

def lock_file(path: str, password: str):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    with open(path, 'rb') as f:
        data = f.read()
    ct = aesgcm.encrypt(nonce, data, None)
    payload = {
        'salt': base64.b64encode(salt).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'ciphertext': base64.b64encode(ct).decode(),
    }
    with open(path + '.locked', 'w') as out:
        json.dump(payload, out)
    os.remove(path)

def unlock_file(path_locked: str, password: str):
    with open(path_locked, 'r') as f:
        payload = json.load(f)
    salt = base64.b64decode(payload['salt'])
    nonce = base64.b64decode(payload['nonce'])
    ct = base64.b64decode(payload['ciphertext'])
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    try:
        data = aesgcm.decrypt(nonce, ct, None)
    except Exception:
        raise ValueError("Bad password or corrupted file")
    orig_path = path_locked[:-7]  # strip “.locked”
    with open(orig_path, 'wb') as out:
        out.write(data)
    os.remove(path_locked)


def lock_folder(folder_path: str, password: str):
    # Create a list first to avoid modifying during iteration
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)

    for file_path in file_paths:
        try:
            # print(f"Locking {file_path}...")  # For debugging (can use logging)
            lock_file(file_path, password)
            os.remove(file_path)
        except Exception as e:
            pass
            # print(f"Failed to lock {file_path}: {e}")
            # Optionally continue or break depending on importance

    # Rename folder to indicate it's locked
    if not folder_path.endswith(".locked"):
        try:
            os.rename(folder_path, folder_path + ".locked")
        except Exception as e:
            pass
            # print(f"Could not rename folder: {e}")
    
def unlock_folder(path_locked: str, password: str):
    metadata_file = os.path.join(path_locked, ".lockmeta.json")
    if not os.path.exists(metadata_file):
        # Fallback for old method
        try:
            for root, dirs, files in os.walk(path_locked):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith(".locked"):  # old method
                        unlock_file(file_path, password)
            # Rename folder
            new_name = path_locked.replace(".locked", "")
            os.rename(path_locked, new_name)

            return  
        except Exception as e:
            raise Exception("Old format folder unlock failed: " + str(e))
    # metadata_file = os.path.join(path_locked, ".lockmeta.json")
    # if not os.path.exists(metadata_file):
    #     raise Exception("Invalid locked folder")

    # with open(metadata_file, "r") as f:
    #     payload = json.load(f)

    # salt = base64.b64decode(payload['salt'])
    # nonce = base64.b64decode(payload['nonce'])
    # ct = base64.b64decode(payload['ciphertext'])
    # key = derive_key(password, salt)
    # aesgcm = AESGCM(key)

    # try:
    #     data = aesgcm.decrypt(nonce, ct, None)
    #     info = json.loads(data.decode())
    #     orig_folder_name = info["original_folder"]
    # except Exception:
    #     raise ValueError("Incorrect password or corrupted lock metadata")

    # # Rename folder back
    # parent = os.path.dirname(path_locked)
    # new_path = os.path.join(parent, orig_folder_name)

    # if os.path.exists(new_path):
    #     raise Exception("Cannot unlock, folder with original name already exists.")

    # os.rename(path_locked, new_path)
