import pickle
import datetime
import security
from classes import Account, Transaction
R1 = False
transaction_type = ""
accounts = {}
transactions = {}

def expenses():
    for reason, transaction in transactions.items():
        if transaction.type == "Withdrawal":
            print(transaction)
def income():
    for reason, transaction in transactions.items():
        if transaction.type == "Debit":
            print(transaction)

"""
TODO: Implement loan interest and payment tracking.
TODO: Implement file encryption.
TODO: Preventing withdrawals or deposits from areas not eligible for transactions.
TODO: Look into: Adding data validation for dates, possibly other inputs; Implementing account categories or tags for better organization; Report creating functionality.
"""
def save_accounts():
    try:
        with open("accounts.pkl", "wb") as f:
            pickle.dump(accounts, f)
        print("Accounts saved successfully.\n")
    except Exception as e:
        print(f"An error occurred while saving accounts: {e}")

def save_log():
    try:
        with open("transaction_log.pkl", "wb") as f:
            pickle.dump(transactions, f)
        print("Transactions saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving transactions: {e}")

def load_accounts():
    global accounts
    try:
        with open("accounts.pkl", "rb") as f:
            accounts = pickle.load(f)
        print("Accounts loaded successfully.")
    except FileNotFoundError:
        accounts = {}
        print("No accounts file found. Starting with an empty account dictionary.")

def load_log():
    global transactions
    try:
        with open("transaction_log.pkl", "rb") as f:
            transactions = pickle.load(f)
        print("Transaction log loaded successfully.")
    except FileNotFoundError:
        transactions = {}
        print("No transaction log file found. Starting with an empty transaction dictionary.")
    except Exception as e:
        transactions = {}
        print(f"An error occurred while loading transactions: {e}")

def print_all_accounts():
    if not accounts:
        print("No accounts have been created yet.")
        return
    print("\n===== ALL ACCOUNTS =====")
    for name, account in accounts.items():
        print(account)
    print("=======================\n")
    return

def print_all_transactions():
    if not transactions:
        print("No transactions have been made yet.")
        return
    print("\n===== ALL TRANSACTIONS =====")
    for reason, transaction in transactions.items():
        print(transaction)
    print("=======================\n")
    return

def initial_prompt():
    while True:
        initial_prompt_input = input("What would you like to do today?\n1. Create a new account\n2. Initialize a transaction\n3. View all accounts\n4. View transaction history\n5. Exit\n")
        if initial_prompt_input == "1":
            create_account()
        elif initial_prompt_input == "2":
            select_transaction_type()
        elif initial_prompt_input == "3":
            print_all_accounts()
        elif initial_prompt_input == "4":
            print_all_transactions()
        elif initial_prompt_input == "5":
            save_accounts()
            save_log()
            print("Exiting...")
            break
        elif initial_prompt_input == "6":
            expenses()
        else:
            print("Invalid input. Please select one of the provided options using the number preceding it.")
            continue

def select_transaction_type():
    while True:
        transaction_type_input = input("Select a transaction type from the following options:\n1. (D)eposit\n2. (W)ithdrawl\n3. (T)ransfer\n")
        transaction_type_input = transaction_type_input.upper()
        if transaction_type_input not in ["D", "W", "T"]:
            print(f"You entered {transaction_type_input}. This is not a valid transaction type. Please enter a letter from the given options.")
            continue
        if transaction_type_input == "D":
            deposit()
            break
        elif transaction_type_input == "W":
            withdrawal()
            break
        elif transaction_type_input == "T":
            transfer()
            break

def find_account():
    while True:
        global R1, transaction_type
        if not accounts:
            print("No accounts available.")
            break
        print("\nSELECT AN ACCOUNT")
        account_list = list(accounts.values())
        for i, account in enumerate(account_list):
            print(f"{i+1}: {account}")
        try:
            if transaction_type == "Transfer" and not R1:
                account_selection = int(input("\nSelect the account you wish to transfer from: "))
            elif transaction_type == "Transfer" and R1 :
                account_selection = int(input("\nSelect the account you wish to transfer to: "))
            else:
                account_selection = int(input("\nSelect the account for this transaction: "))
            if 1 <= account_selection <= len(account_list):
                selected_account = account_list[account_selection-1]
                return selected_account
                break
            else:
                print("Invalid selection. Please try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

def log_details():
    transaction_date = input("Add the date for this transaction: ")
    transaction_reason = input("Add the reason for this transaction: ")
    unique_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_key = f"{transaction_reason}_{unique_id}"
    return transaction_date, transaction_reason, unique_key

def deposit():
    while True:
        global transaction_type
        transaction_type = "Deposit"
        selected_account = find_account()
        transaction_date, transaction_reason, unique_key = log_details()
        try:
            deposit_amount = float(input("Input the debit amount: $"))
            if deposit_amount <= 0:
                print("Deposit amount must be positive.")
                continue
            selected_account.deposit(deposit_amount)
            transactions[unique_key] = Transaction(transaction_reason, transaction_type, selected_account, deposit_amount, transaction_date)
            print(f"Transaction successful. Updated account details:\n{selected_account}")
            save_accounts()
            save_log()
            break
        except ValueError:
            print("Please enter a valid numerical value.")
            continue

def withdrawal():
    while True:
        global transaction_type
        transaction_type = "Withdrawal"
        selected_account = find_account()
        transaction_date, transaction_reason, unique_key = log_details()
        try:
            withdrawal_amount = float(input("Input the withdrawal amount: -$"))
            if withdrawal_amount <= 0:
                print("Please input the credit amount as a positive number.")
                continue
            selected_account.withdrawal(withdrawal_amount)
            transactions[unique_key] = Transaction(transaction_reason, transaction_type, selected_account, withdrawal_amount, transaction_date)
            print(f"Transaction successful. Updated account details:\n{selected_account}")
            save_accounts()
            save_log()
            break
        except ValueError:
            print("Please enter a numerical value.")
            continue

def transfer():
    while True:
        global transaction_type, R1
        transaction_type = "Transfer"
        selected_account = find_account()
        R1 = True
        target_account = find_account()
        R1 = False
        transaction_date, transaction_reason, unique_key = log_details()
        if selected_account is None or target_account is None:
            print("Missing origin or target account. Please try again.")
            continue
        elif selected_account == target_account:
            print("Null transaction. You cannot transfer money from an account to itself.")
            continue
        try:
            transfer_amount = float(input("Input the transfer amount: $"))
            if transfer_amount <= 0:
                print("Transfer amount must be positive.")
                continue
            elif selected_account.balance < transfer_amount:
                print("Insufficient funds in the originating account.")
                continue
            selected_account.withdrawal(transfer_amount)
            target_account.deposit(transfer_amount)
            transactions[unique_key] = Transaction(transaction_reason, transaction_type, selected_account, transfer_amount, transaction_date,)
            unique_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_target"
            unique_key_target = f"{transaction_reason}_{unique_id}"
            transactions[unique_key_target] = Transaction(transaction_reason, transaction_type, target_account, transfer_amount, transaction_date)
            print(f"Transaction successful.\n Originating account:\n{selected_account}\nTarget account:\n{target_account}")
            save_accounts()
            save_log()
            break
        except ValueError:
            print("Please enter a valid amount.")
            continue

def create_account():
    while True:
        balance = 0
        name = input("Enter a name for the account: ")
        if name in accounts:
            print(f"The account with the name {name} already exists. Please enter a different name.")
            continue
        account_type_input = input("Select an account type from the following options:\n1. (C)hecking\n2. (S)avings\n3. (X)Credit\n4. (I)vestment\n5. (L)oan\n")
        account_type_input = account_type_input.upper()
        if account_type_input not in ["C", "S", "X", "I", "L"]:
            print(f"You entered {account_type_input}. This is not a valid account type. Please enter a letter from the given options.")
            continue
        if account_type_input == "C":
            account_type = "Checking"
        elif account_type_input == "S":
            account_type = "Savings"
        elif account_type_input == "X":
            account_type = "Credit"
        elif account_type_input == "I":
            account_type = "Investment"
        elif account_type_input == "L":
            account_type = "Loan"
        def account_balances():
            nonlocal balance
            try:
                if account_type in ["Checking", "Savings", "Investment"]:
                    balance_input = (float(input("Enter an initial balance: ")))
                    if balance_input < 0:
                        print("You entered a negative value for a debit account. Are you sure this is correct?")
                        response = input("(Y)es or (N)o:")
                        response = response.upper()
                        if response == "Y":
                            pass
                        elif response == "N":
                            print("Let's try again.")
                            return account_balances()
                        else:
                            print("You entered an invalid input. Let's try this again")
                            return account_balances()
                if account_type in ["Credit", "Loan"]:
                    balance_input = float(input("Enter initial balance: "))
                    if balance_input > 0:
                        print("You entered a postive value for a credit or loan account. Please enter a negative value.")
                        return account_balances()
                balance = round(balance_input, 2)
            except ValueError:
                print("Please enter a valid number.")
                return
        account_balances()
        accounts[name] = Account(name, account_type, balance)
        print(f"Account created successfully!\nAccount Name: {accounts[name].name}\nAccount Type: {accounts[name].type}\nInitial Balance: ${accounts[name].balance}")
        from main import save_accounts
        save_accounts()
        return


if __name__ == "__main__":
    if security.verify_password():
        load_accounts()
        load_log()
        initial_prompt()
    else:
        exit()