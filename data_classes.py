class Account:
    def __init__(self, name, type, balance):
        self.name = name
        self.type = type
        self.original_balance = balance
        self.transactions = []

    @property
    def balance(self):
        return (
            sum([transaction.amount for transaction in self.transactions])
            + self.original_balance
        )


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
    def __init__(self, name, balance):
        super().__init__(name, "Investment", balance)


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

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return (
            self.category == other.category
            and self.type == other.type
            and self.amount == other.amount
            and self.date == other.date
            and self.beginning_balance == other.beginning_balance
            and self.ending_balance == other.ending_balance
        )

    def __hash__(self):
        return hash(
            (
                self.category,
                self.type,
                self.amount,
                self.date,
                self.beginning_balance,
                self.ending_balance,
            )
        )
