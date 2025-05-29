import os
import pickle
import bcrypt
from cryptography.fernet import Fernet

if not os.path.isfile("unlock_key.pkl"):
    with open("unlock_key.pkl", "wb") as f:
        f.write(Fernet.generate_key())
with open("unlock_key.pkl", "rb") as f:
    key = f.read()
fernet = Fernet(key)

def save_accounts(accounts):
    try:
        data = pickle.dumps(accounts)
        encrypted = fernet.encrypt(data)
        with open("accounts.pkl", "wb") as f:
            f.write(encrypted)
    except Exception:
        pass

def save_categories(categories):
    try:
        data = pickle.dumps(categories)
        encrypted = fernet.encrypt(data)
        with open("categories.pkl", "wb") as f:
            f.write(encrypted)
    except Exception:
        pass

def load_accounts():
    try:
        with open("accounts.pkl", "rb") as f:
            encrypted = f.read()
        data = fernet.decrypt(encrypted)
        return pickle.loads(data)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def load_categories():
    try:
        with open("categories.pkl", "rb") as f:
            encrypted = f.read()
        data = fernet.decrypt(encrypted)
        return pickle.loads(data)
    except FileNotFoundError:
        return []
    except Exception:
        return []

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
