import os, pickle, bcrypt
from cryptography.fernet import Fernet

if not os.path.isfile("unlock_key.pkl"):
    with open("unlock_key.pkl", "wb") as f:
        f.write(Fernet.generate_key())
with open("unlock_key.pkl", "rb") as f:
    key = f.read()
fernet = Fernet(key)

def find_ui_settings():
    if os.path.isfile("custom_ui.cfg"):
        with open("custom_ui.cfg", "r") as f:
            settings = f.read().strip().split('\n')
            font = settings[0] if len(settings) > 0 else "times"
            accent = settings[1].lower() if len(settings) > 1 else "blue"
            theme = settings[2].lower() if len(settings) > 2 else "dark"
            return font, accent, theme
    else:
        return "times", "blue", "dark"

def save_ui_settings(font, accent, theme):
    try:
        with open("custom_ui.cfg", "w") as f:
            f.write(f"{font}\n{accent if accent else ''}\n{theme if theme else 'dark'}")
    except Exception:
        pass

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