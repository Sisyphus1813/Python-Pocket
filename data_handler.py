import os, pickle, bcrypt, platform, getpass
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from cryptography.fernet import Fernet
from data_classes import Transaction
from pathlib import Path

platform = platform.system()
user = getpass.getuser()
match platform:
    case "Windows":
        local_dir = Path(os.environ["LOCALAPPDATA"]) / "python-pocket"
    case "Linux":
        local_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "python-pocket"
if not os.path.isdir(local_dir):
    os.mkdirs(local_dir)
if not os.path.isfile(f"{local_dir}/unlock_key.pkl"):
    with open(f"{local_dir}/unlock_key.pkl", "wb") as f:
        f.write(Fernet.generate_key())
with open(f"{local_dir}/unlock_key.pkl", "rb") as f:
    key = f.read()
fernet = Fernet(key)


def load_ui_settings():
    if os.path.isfile(f"{local_dir}/custom_ui.cfg"):
        with open(f"{local_dir}/custom_ui.cfg", "r") as f:
            settings = f.read().strip().split("\n")
            font = settings[0] if len(settings) > 0 else "times"
            accent = settings[1].lower() if len(settings) > 1 else "blue"
            theme = settings[2].lower() if len(settings) > 2 else "dark"
            return font, accent, theme
    else:
        return "times", "blue", "dark"


def save_ui_settings(font, accent, theme):
    try:
        with open(f"{local_dir}/custom_ui.cfg", "w") as f:
            f.write(f"{font}\n{accent if accent else ''}\n{theme if theme else 'dark'}")
    except Exception:
        pass


def save_accounts(accounts):
    try:
        data = pickle.dumps(accounts)
        encrypted = fernet.encrypt(data)
        with open(f"{local_dir}/accounts.pkl", "wb") as f:
            f.write(encrypted)
    except Exception:
        pass


def save_categories(categories):
    try:
        data = pickle.dumps(categories)
        encrypted = fernet.encrypt(data)
        with open(f"{local_dir}/categories.pkl", "wb") as f:
            f.write(encrypted)
    except Exception:
        pass


def load_accounts():
    try:
        with open(f"{local_dir}/accounts.pkl", "rb") as f:
            encrypted = f.read()
        data = fernet.decrypt(encrypted)
        return pickle.loads(data)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def load_categories():
    try:
        with open(f"{local_dir}/categories.pkl", "rb") as f:
            encrypted = f.read()
        data = fernet.decrypt(encrypted)
        return pickle.loads(data)
    except Exception:
        return []


def update_accounts(accounts):
    today = datetime.now().date()
    for account in accounts.values():
        for transaction in account.repeating_transactions:
            if transaction.last_charged is not None:
                last = transaction.last_charged
            else:
                last = transaction.date
            match transaction.schedule:
                case "Daily":
                    delta = timedelta(days=1)
                case "Weekly":
                    delta = timedelta(weeks=1)
                case "Monthly":
                    delta = relativedelta(months=1)
                case "Annually":
                    delta = relativedelta(years=1)
                case _:
                    continue
            current = last + delta
            while current <= today:
                beginning = account.balance
                new_transaction = Transaction(
                    category=transaction.category,
                    type=transaction.type,
                    amount=transaction.amount,
                    date=current,
                    beginning_balance=beginning,
                    ending_balance=beginning + transaction.amount,
                )
                account.transactions.append(new_transaction)
                transaction.last_charged = current
                current += delta


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
