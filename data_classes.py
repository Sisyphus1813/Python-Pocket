class Account:
    def __init__(self, name, type, balance):
        self.name = name
        self.type = type
        self.balance = balance
        self.transactions = []


class CheckingAccount(Account):
    def __init__(self, name, balance, apy, compounding_frequency):
        super().__init__(name, "Checking", balance)
        self.apy = apy
        self.compounding_frequency = compounding_frequency


class SavingsAccount(Account):
    def __init__(self, name, balance, apy, compounding_frequency):
        super().__init__(name, "Savings", balance)
        self.apy = apy
        self.compounding_frequency = compounding_frequency


class InvestmentAccount(Account):
    def __init__(self, name, balance, apy, compounding_frequency):
        super().__init__(name, "Investment", balance)
        self.compounding_frequency = compounding_frequency


class CreditAccount(Account):
    def __init__(self, name, balance, apr, limit, due_date):
        super().__init__(name, "Credit", balance)
        self.apr = apr
        self.limit = limit
        self.due_date = due_date

    @property
    def available_credit(self):
        return self.limit + self.balance


class LoanAccount(Account):
    def __init__(self, name, balance, apr, compounding_frequency, due_date):
        super().__init__(name, "Loan", balance)
        self.apr = apr
        self.compounding_frequency = compounding_frequency
        self.due_date = due_date


class Transaction:
    def __init__(self, category, type, amount, date, beginning_balance, ending_balance):
        self.category = category
        self.type = type
        self.amount = amount
        self.date = date
        self.beginning_balance = beginning_balance
        self.ending_balance = ending_balance
