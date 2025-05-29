class Account:
    def __init__(self, name, type, balance):
        self.name = name
        self.type = type
        self.balance = balance
        self.transactions = []
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    def withdrawal(self, amount):
        self.balance -= amount
        return self.balance

class Transaction:
    def __init__(self, category, type, amount, date, beginning_balance, ending_balance):
        self.category = category
        self.type = type
        self.amount = amount
        self.date = date
        self.beginning_balance = beginning_balance
        self.ending_balance = ending_balance