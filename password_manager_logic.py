import json
import os
import bcrypt
import base64
from cryptography.fernet import Fernet
import random
import string

VAULT_FILE = "vault.json"
MASTER_FILE = "master.hash"

# ---------------- MASTER PASSWORD ----------------
def set_master_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(MASTER_FILE, "wb") as f:
        f.write(hashed)

def check_master_password(password):
    if not os.path.exists(MASTER_FILE):
        return False

    with open(MASTER_FILE, "rb") as f:
        stored = f.read()

    return bcrypt.checkpw(password.encode(), stored)

def is_master_password_set():
    return os.path.exists(MASTER_FILE)

# ---------------- KEY GENERATION ----------------
def generate_key(password):
    key = base64.urlsafe_b64encode(password.ljust(32).encode())
    return Fernet(key)

# ---------------- VAULT ----------------
def load_data():
    if not os.path.exists(VAULT_FILE):
        return {}

    try:
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- SAVE PASSWORD ----------------
def save_password(master_password, website, username, password):
    data = load_data()
    fernet = generate_key(master_password)

    encrypted = fernet.encrypt(password.encode()).decode()

    data[website] = {
        "username": username,
        "password": encrypted
    }

    save_data(data)

# ---------------- GET PASSWORD ----------------
def get_password(master_password, website):
    data = load_data()

    if website not in data:
        return None, None

    fernet = generate_key(master_password)

    try:
        decrypted = fernet.decrypt(data[website]["password"].encode()).decode()
        return data[website]["username"], decrypted
    except:
        return None, None

# ---------------- PASSWORD GENERATOR ----------------
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation

    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    password += random.choices(chars, k=length - 4)
    random.shuffle(password)

    return "".join(password)
        