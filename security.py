import hashlib
import getpass
import pickle

"""
from cryptography.fernet import Fernet
import base64

password_hash = None
key = fernet.generate_key()
with open("unlock_key.pkl", "wb") as keys:
    unlock_key.write(key)


with open("unlock_key.pkl", "rb") as keys:
    unlock_key.read(key)
"""

def setup_password():
    global password_hash
    while True:
        print("No password found. Please setup your password.")
        new_password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if new_password != confirm_password:
            print("Passwords do not match.")
            continue
        else:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            try:
                with open("password.pkl", "wb") as f:
                    pickle.dump(password_hash, f)
                print("Password saved successfully.\n")
            except Exception as e:
                print(f"An error occurred while saving your password: {e}")
            break

def verify_password():
    while True:
        global password_hash
        try:
            with open("password.pkl", "rb") as f:
                password_hash = pickle.load(f)
            attempts = 3
            while attempts > 0:
                entered_password = getpass.getpass("Enter password: ")
                entered_password_hash = hashlib.sha256(entered_password.encode()).hexdigest()
                if entered_password_hash == password_hash:
                    print("Access granted.")
                    return True
                    break
                else:
                    print("Password incorrect, please try again.\n")
                    attempts -= 1
                    continue
            else:
                print("Maximum login attempts reached. Please try again later.")
                return False
        except FileNotFoundError:
            setup_password()
            continue
