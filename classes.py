class Account:
    def __init__(self, name, type, balance):
        self.name = name
        self.type = type
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    def withdrawal(self, amount):
        self.balance -= amount
        return self.balance
    def __str__(self):
        return f"Account: {self.name} | Type: {self.type} | Balance: ${self.balance:.2f}"

class Transaction:
    def __init__(self, reason, type, account, amount, date):
        self.reason = reason
        self.type = type
        self.account = account
        self.amount = amount
        self.date = date
    def __str__(self):
        return f"Reason: {self.reason} | Type: {self.type} | Amount: ${self.amount} | Date: {self.date} | Account: {self.account.name}"