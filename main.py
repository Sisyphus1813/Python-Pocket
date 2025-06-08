from customtkinter import *
from data_handler import (
    load_accounts,
    save_accounts,
    save_categories,
    load_categories,
    hash_password,
    verify_password,
    find_theme,
)
from data_classes import (
    Account,
    CheckingAccount,
    SavingsAccount,
    InvestmentAccount,
    CreditAccount,
    LoanAccount,
    Transaction,
)
from tkcalendar import Calendar
import pickle, datetime, tkinter, time


class LoginPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.welcome_label = CTkLabel(self, text="Welcome to Python Pocket!")
        self.welcome_label.place(relx=0.5, rely=0.3, anchor="center")
        self.pass_input = CTkEntry(
            self, placeholder_text="Enter your password", width=250, show="*"
        )
        self.pass_input.place(relx=0.5, rely=0.35, anchor="center")
        self.pass_input.bind("<Return>", self.verify_password)
        self.error_label = CTkLabel(self, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.42, anchor="center")

    def verify_password(self, event=None):
        entered_password = self.pass_input.get()
        try:
            with open("password.pkl", "rb") as f:
                stored_hash = pickle.load(f)
        except FileNotFoundError:
            self.master.change_page(PasswordSetupPage)
            return
        if verify_password(entered_password, stored_hash):
            self.master.change_page(HomePage)
        else:
            self.error_label.configure(text="Incorrect password. Try again.")


class PasswordSetupPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.info_label = CTkLabel(self, text="No password found. Please set one.")
        self.info_label.place(relx=0.5, rely=0.25, anchor="center")
        self.pass_input_1 = CTkEntry(
            self, placeholder_text="Enter new password", width=250, show="*"
        )
        self.pass_input_1.place(relx=0.5, rely=0.35, anchor="center")
        self.pass_input_2 = CTkEntry(
            self, placeholder_text="Re-enter new password", width=250, show="*"
        )
        self.pass_input_2.place(relx=0.5, rely=0.42, anchor="center")
        self.pass_input_2.bind("<Return>", self.set_password)
        self.error_label = CTkLabel(self, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.49, anchor="center")

    def set_password(self, event=None):
        password1 = self.pass_input_1.get()
        password2 = self.pass_input_2.get()
        if password1 != password2:
            self.error_label.configure(text="Passwords do not match.")
            return
        if not password1:
            self.error_label.configure(text="Password cannot be empty.")
            return
        hashed = hash_password(password1)
        with open("password.pkl", "wb") as f:
            pickle.dump(hashed, f)
        self.error_label.configure(
            text_color="green", text="Password set. Logging in..."
        )
        self.after(1500, lambda: self.master.change_page(HomePage))


class HomePage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_label = CTkLabel(
            self, text="Python Pocket", font=("times", 40, "bold")
        )
        self.main_label.place(relx=0.5, rely=0.1, anchor="center")
        self.accounts_button = CTkButton(
            self, text="Accounts", command=lambda: master.change_page(AccountsPage)
        )
        self.accounts_button.place(relx=0.5, rely=0.2, anchor="center")
        self.statistics_button = CTkButton(
            self, text="Statistics", command=lambda: master.change_page(StatisticsPage)
        )
        self.statistics_button.place(relx=0.5, rely=0.25, anchor="center")
        self.settings_button = CTkButton(
            self, text="Settings", command=lambda: master.change_page(SettingsPage)
        )
        self.settings_button.place(relx=0.5, rely=0.3, anchor="center")


class AccountsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        load_accounts()
        self.accounts_label = CTkLabel(
            self, text="Accounts", font=("times", 30, "bold")
        )
        self.accounts_label.pack(pady=(50, 10))
        self.create_account_button = CTkButton(
            self,
            text="Create a new account",
            command=lambda: master.change_page(CreateAccountPage),
        )
        self.create_account_button.place(relx=0.01, rely=0.85, anchor="w")
        self.post_transaction_button = CTkButton(
            self,
            text="Post a new Transaction",
            command=lambda: master.change_page(PostTransactionPage),
        )
        self.post_transaction_button.place(relx=0.01, rely=0.9, anchor="w")
        self.add_category_button = CTkButton(
            self,
            text="Manage transaction Categories",
            command=lambda: master.change_page(CategoryPage),
        )
        self.add_category_button.place(relx=0.01, rely=0.95, anchor="w")
        self.accounts_panel = CTkFrame(self, fg_color="transparent")
        self.accounts_panel.pack(pady=(0, 10))
        for col, header in enumerate(["", "Name", "Account Type", "Balance"]):
            CTkLabel(self.accounts_panel, text=header).grid(
                row=0, column=col, padx=15, pady=20
            )
        for row, (key, account) in enumerate(accounts.items(), start=1):
            CTkButton(
                self.accounts_panel,
                height=20,
                width=75,
                text="View Details",
                command=lambda account=account: master.change_page(
                    lambda master: AccountDetailsPage(master, account)
                ),
            ).grid(row=row, column=0, padx=10, pady=10)
            CTkLabel(self.accounts_panel, text=account.name).grid(
                row=row, column=1, padx=15, pady=20
            )
            CTkLabel(self.accounts_panel, text=account.type).grid(
                row=row, column=2, padx=15, pady=20
            )
            balance_value = account.balance
            balance_text = f"${balance_value:,.2f}"
            balance_color = "green" if balance_value >= 0 else "red"
            CTkLabel(
                self.accounts_panel, text=balance_text, text_color=balance_color
            ).grid(row=row, column=3, padx=15, pady=10)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(HomePage)
        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="w")


class AccountDetailsPage(CTkFrame):
    def __init__(self, master, account):
        super().__init__(master)
        self.account = account
        self.title = CTkLabel(self, text=f"{account.name}", font=("times", 30, "bold"))
        self.title.pack(pady=(30, 10))
        self.details_frame = CTkFrame(self, fg_color="transparent")
        self.details_frame.pack(pady=(5, 20))
        columns = 6
        fields = [("Account Balance", account.balance)]
        if isinstance(account, CreditAccount):
            fields.append(("Available Credit", account.available_credit))
        fields += [
            (key.replace("_", " ").title(), value)
            for key, value in vars(account).items()
            if key not in {"name", "transactions", "original_balance"}
            and not key.startswith("_")
        ]
        for i, (label_key, value) in enumerate(fields):
            col = i % columns
            row = i // columns
            if isinstance(value, (int, float)):
                if "apr" in label_key.lower() or "apy" in label_key.lower():
                    label_value = f"{value:.2f}%"
                else:
                    label_value = f"${value:,.2f}"
            elif label_key.lower() == "due date":
                try:
                    day = int(value)
                    if 10 <= day % 100 <= 20:
                        suffix = "th"
                    else:
                        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
                    label_value = f"{day}{suffix}"
                except ValueError:
                    label_value = str(value)
            else:
                label_value = str(value).title()
            color = None
            if label_key.lower() == "account balance":
                try:
                    numeric_value = float(str(value).replace("$", "").replace(",", ""))
                    color = "green" if numeric_value > 0 else "red"
                except ValueError:
                    pass
            CTkLabel(
                self.details_frame, text=f"{label_key}:", font=("times", 16, "bold")
            ).grid(row=row * 2, column=col, sticky="w", padx=15, pady=(2, 0))
            CTkLabel(
                self.details_frame,
                text=label_value,
                font=("times", 16),
                text_color=color,
            ).grid(row=row * 2 + 1, column=col, sticky="w", padx=15, pady=(0, 6))
        if not account.transactions:
            CTkLabel(self, text="No transactions found.").pack()
        else:
            self.transactions_label = CTkLabel(
                self, text="Transactions", font=("times", 22, "bold")
            )
            self.transactions_label.pack(pady=(0, 5))
            self.scroll_frame = CTkScrollableFrame(self, fg_color="transparent")
            self.scroll_frame.pack(pady=(0, 5), anchor="s")
            self.bind("<Configure>", self.resize_scroll_frame)
            headers = [
                "",
                "Date",
                "Type",
                "Category",
                "Amount",
                "Start Balance",
                "End Balance",
            ]
            for col, header in enumerate(headers):
                CTkLabel(
                    self.scroll_frame, text=header, font=("times", 18, "bold")
                ).grid(row=0, column=col, padx=15, pady=5)
            for row, transaction in enumerate(account.transactions, start=1):
                CTkButton(
                    self.scroll_frame,
                    text="Edit",
                    width=50,
                    height=20,
                    command=lambda t=transaction, a=account: self.master.change_page(
                        lambda master: EditTransactionPage(master, t, a)
                    ),
                ).grid(row=row, column=0, padx=5, pady=2)
                date_display = (
                    transaction.date.strftime("%Y-%m-%d")
                    if isinstance(transaction.date, (datetime.date, datetime.datetime))
                    else str(transaction.date)
                )
                CTkLabel(self.scroll_frame, text=date_display).grid(row=row, column=1)
                CTkLabel(self.scroll_frame, text=transaction.type).grid(
                    row=row, column=2
                )
                CTkLabel(self.scroll_frame, text=transaction.category).grid(
                    row=row, column=3
                )
                CTkLabel(
                    self.scroll_frame,
                    text=f"${transaction.amount:.2f}",
                    text_color="green" if transaction.type == "Deposit" else "red",
                ).grid(row=row, column=4)
                CTkLabel(
                    self.scroll_frame,
                    text=f"${transaction.beginning_balance:.2f}",
                    text_color="green" if transaction.beginning_balance > 0 else "red",
                ).grid(row=row, column=5)
                CTkLabel(
                    self.scroll_frame,
                    text=f"${transaction.ending_balance:.2f}",
                    text_color="green" if transaction.ending_balance > 0 else "red",
                ).grid(row=row, column=6)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="w")

    def resize_scroll_frame(self, event):
        target_width = int(event.width * 0.65)
        target_height = int(event.height * 0.7)
        self.scroll_frame.configure(width=target_width, height=target_height)


class CreateAccountPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        self.main_label = CTkLabel(self, text="New Account", font=("times", 30, "bold"))
        self.main_label.pack(pady=(50, 15))
        self.account_type_frame = CTkFrame(self, fg_color="transparent")
        self.account_type_frame.pack(pady=(0, 5), padx=(0, 165))
        self.account_type_label = CTkLabel(self.account_type_frame, text="Type: ")
        self.account_type_label.pack(side="left", padx=(0, 10))
        self.account_type = CTkOptionMenu(
            self.account_type_frame,
            values=["Checking", "Savings", "Investment", "Credit", "Loan"],
            command=self.update_page,
        )
        self.account_type.set("")
        self.account_type.pack(side="left")
        self.name_frame = CTkFrame(self, fg_color="transparent")
        self.name_frame.pack(pady=5)
        self.account_name_label = CTkLabel(self.name_frame, text="Name: ")
        self.account_name_label.pack(side="left", padx=(0, 10))
        self.account_name = CTkEntry(
            self.name_frame, placeholder_text="Enter the name of the account", width=300
        )
        self.account_name.pack(side="left")
        self.account_balance_frame = CTkFrame(self, fg_color="transparent")
        self.account_balance_frame.pack(pady=5, padx=(12.5, 0))
        self.account_balance_label = CTkLabel(
            self.account_balance_frame, text="Balance: "
        )
        self.account_balance_label.pack(side="left", padx=(0, 5))
        self.account_balance = CTkEntry(
            self.account_balance_frame,
            placeholder_text="0.00",
            width=300,
            validate="key",
            validatecommand=(vcmd, "%P"),
        )
        self.account_balance.pack(side="left", padx=(2.5, 0))
        self.submit_frame = CTkFrame(self, fg_color="transparent")
        self.submit_frame.pack(pady=10)
        self.submit_button = CTkButton(
            self.submit_frame, text="Submit", command=self.initialize_account
        )
        self.submit_button.pack()
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="w")

    def update_page(self, account_type):
        if hasattr(self, "balance_prefix"):
            self.balance_prefix.destroy()
        if hasattr(self, "apy_frame"):
            self.apy_frame.destroy()
        if hasattr(self, "compounding_freq_frame"):
            self.compounding_freq_frame.destroy()
        if hasattr(self, "apr_frame"):
            self.apr_frame.destroy()
        if hasattr(self, "limit_frame"):
            self.limit_frame.destroy()
        if hasattr(self, "due_date_frame"):
            self.due_date_frame.destroy()
        prefix = "$" if account_type in ["Checking", "Savings", "Investment"] else "-$"
        color = "green" if prefix == "$" else "red"
        self.account_balance.configure(text_color=color)
        self.balance_prefix = CTkLabel(
            self.account_balance_frame, text=prefix, text_color=color
        )
        self.balance_prefix.pack(
            side="left",
            padx=0,
            after=self.account_balance_label,
            before=self.account_balance,
        )
        if self.account_type.get() in ["Checking", "Savings"]:
            self.apy_frame = CTkFrame(self, fg_color="transparent")
            self.apy_frame.pack(
                after=self.account_balance_frame,
                before=self.submit_frame,
                pady=5,
                padx=(0, 10),
            )
            self.apy_label = CTkLabel(self.apy_frame, text="APY: ")
            self.apy_label.pack(side="left", padx=(0, 10))
            self.apy = CTkEntry(self.apy_frame, placeholder_text="Enter %", width=300)
            self.apy.pack(side="left")
            self.compounding_freq_frame = CTkFrame(self, fg_color="transparent")
            self.compounding_freq_frame.pack(
                after=self.apy_frame, before=self.submit_frame, pady=5, padx=(0, 55)
            )
            self.compounding_freq_label = CTkLabel(
                self.compounding_freq_frame, text="Compounding Frequency: "
            )
            self.compounding_freq_label.pack(side="left", padx=(0, 10))
            self.compounding_freq = CTkOptionMenu(
                self.compounding_freq_frame,
                values=["Daily", "Monthly", "Quarterly", "Annually"],
            )
            self.compounding_freq.pack(side="left")
            self.compounding_freq.set("Monthly")
        elif self.account_type.get() == "Credit":
            self.apr_frame = CTkFrame(self, fg_color="transparent")
            self.apr_frame.pack(
                after=self.account_balance_frame,
                before=self.submit_frame,
                pady=5,
                padx=(0, 10),
            )
            self.apr_label = CTkLabel(self.apr_frame, text="APR: ")
            self.apr_label.pack(side="left", padx=(0, 10))
            self.apr = CTkEntry(self.apr_frame, placeholder_text="Enter %", width=300)
            self.apr.pack(side="left")
            self.compounding_freq_frame = CTkFrame(self, fg_color="transparent")
            self.compounding_freq_frame.pack(
                after=self.apr_frame, before=self.submit_frame, pady=5, padx=(0, 55)
            )
            self.compounding_freq_label = CTkLabel(
                self.compounding_freq_frame, text="Compounding Frequency: "
            )
            self.compounding_freq_label.pack(side="left", padx=(0, 10))
            self.compounding_freq = CTkOptionMenu(
                self.compounding_freq_frame,
                values=["Daily", "Monthly", "Quarterly", "Annually"],
            )
            self.compounding_freq.pack(side="left")
            self.compounding_freq.set("Monthly")
            self.limit_frame = CTkFrame(self, fg_color="transparent")
            self.limit_frame.pack(
                after=self.compounding_freq_frame,
                before=self.submit_frame,
                pady=5,
                padx=(25, 0),
            )
            self.limit_label = CTkLabel(self.limit_frame, text="Credit limit: ")
            self.limit_label.pack(side="left", padx=(0, 10))
            self.limit = CTkEntry(self.limit_frame, placeholder_text=0.00, width=300)
            self.limit.pack(side="left")
            self.due_date_frame = CTkFrame(self, fg_color="transparent")
            self.due_date_frame.pack(
                after=self.limit_frame, before=self.submit_frame, pady=5, padx=(5, 0)
            )
            self.due_date_label = CTkLabel(self.due_date_frame, text="Due date: ")
            self.due_date_label.pack(side="left")
            self.due_date_var = tkinter.StringVar()
            self.due_date = CTkEntry(
                self.due_date_frame, textvariable=self.due_date_var, width=300
            )
            self.due_date.pack(side="left")
            self.due_date.bind("<Button-1>", self.open_calendar)
        elif self.account_type.get() == "Loan":
            self.apr_frame = CTkFrame(self, fg_color="transparent")
            self.apr_frame.pack(
                after=self.account_balance_frame,
                before=self.submit_frame,
                pady=5,
                padx=(0, 10),
            )
            self.apr_label = CTkLabel(self.apr_frame, text="APR: ")
            self.apr_label.pack(side="left", padx=(0, 10))
            self.apr = CTkEntry(self.apr_frame, placeholder_text="Enter %", width=300)
            self.apr.pack(side="left")
            self.compounding_freq_frame = CTkFrame(self, fg_color="transparent")
            self.compounding_freq_frame.pack(
                after=self.apr_frame, before=self.submit_frame, pady=5, padx=(0, 55)
            )
            self.compounding_freq_label = CTkLabel(
                self.compounding_freq_frame, text="Compounding Frequency: "
            )
            self.compounding_freq_label.pack(side="left", padx=(0, 10))
            self.compounding_freq = CTkOptionMenu(
                self.compounding_freq_frame,
                values=["Daily", "Monthly", "Quarterly", "Annually"],
            )
            self.compounding_freq.pack(side="left")
            self.compounding_freq.set("Monthly")
            self.due_date_frame = CTkFrame(self, fg_color="transparent")
            self.due_date_frame.pack(
                after=self.compounding_freq_frame,
                before=self.submit_frame,
                pady=5,
                padx=(5, 0),
            )
            self.due_date_label = CTkLabel(self.due_date_frame, text="Due date: ")
            self.due_date_label.pack(side="left")
            self.due_date_var = tkinter.StringVar()
            self.due_date = CTkEntry(
                self.due_date_frame, textvariable=self.due_date_var, width=300
            )
            self.due_date.pack(side="left")
            self.due_date.bind("<Button-1>", self.open_calendar)

    def open_calendar(self, event):
        def select_date():
            selected = cal.selection_get()
            self.due_date_var.set(f"{selected.day:02d}")
            top.destroy()

        top = tkinter.Toplevel(self)
        top.grab_set()
        top.geometry("+%d+%d" % (event.x_root, event.y_root))
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack()
        ok_button = tkinter.Button(top, text="OK", command=select_date)
        ok_button.pack()

    def initialize_account(self):
        account_name = self.account_name.get()
        account_balance = float(self.account_balance.get())
        account_type = self.account_type.get()
        apy = (
            float(self.apy.get()) if hasattr(self, "apy") and self.apy.get() else "None"
        )
        apr = (
            float(self.apr.get()) if hasattr(self, "apr") and self.apr.get() else "None"
        )
        compounding_frequency = (
            self.compounding_frequency.get()
            if hasattr(self, "compounding_frequency")
            else "None"
        )
        limit = (
            float(self.limit.get())
            if hasattr(self, "limit") and self.limit.get()
            else 0.0
        )
        due_date = self.due_date_var.get() if hasattr(self, "due_date") else "None"
        match account_type:
            case "Checking":
                accounts[account_name] = CheckingAccount(
                    name=account_name,
                    balance=account_balance,
                    apy=apy,
                    compounding_frequency=compounding_frequency,
                )
            case "Savings":
                accounts[account_name] = SavingsAccount(
                    name=account_name,
                    balance=account_balance,
                    apy=apy,
                    compounding_frequency=compounding_frequency,
                )
            case "Investment":
                accounts[account_name] = InvestmentAccount(
                    name=account_name,
                    balance=account_balance,
                )
            case "Credit":
                accounts[account_name] = CreditAccount(
                    name=account_name,
                    balance=-account_balance,
                    apr=apr,
                    limit=limit,
                    due_date=due_date,
                )
            case "Loan":
                accounts[account_name] = LoanAccount(
                    name=account_name,
                    balance=-account_balance,
                    apr=apr,
                    compounding_frequency=compounding_frequency,
                    due_date=due_date,
                )
            case _:
                accounts[account_name] = Account(
                    name=account_name, type=account_type, balance=account_balance
                )
        save_accounts(accounts)
        self.notify = CTkLabel(
            self,
            text="Updating accounts...",
            text_color="green",
            font=("times", 25, "bold"),
        )
        self.notify.place(relx=0.5, rely=0.5)
        self.after(1000, lambda: self.master.change_page(CreateAccountPage))


class PostTransactionPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_label = CTkLabel(
            self, text="New Transaction", font=("times", 30, "bold")
        )
        self.main_label.pack(pady=(50, 15))
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        self.transaction_type_frame = CTkFrame(self, fg_color="transparent")
        self.transaction_type_frame.pack(pady=5, padx=(0, 87.5))
        self.transaction_type_label = CTkLabel(
            self.transaction_type_frame, text="Action: "
        )
        self.transaction_type_label.pack(side="left", padx=(0, 10))
        self.transaction_type = CTkOptionMenu(
            self.transaction_type_frame,
            values=["Deposit", "Withdraw"],
            command=self.update_amount_prefix,
        )
        self.transaction_type.pack(side="left")
        self.transaction_type.set("")
        self.account_frame = CTkFrame(self, fg_color="transparent")
        self.account_frame.pack(pady=5, padx=(0, 80))
        self.account_label = CTkLabel(self.account_frame, text="Account: ")
        self.account_label.pack(side="left", padx=(0, 10))
        self.account = CTkOptionMenu(
            self.account_frame, values=[account.name for account in accounts.values()]
        )
        self.account.pack(side="left")
        self.account.set("")
        self.category_frame = CTkFrame(self, fg_color="transparent")
        self.category_frame.pack(pady=5, padx=(0, 80))
        self.category_label = CTkLabel(self.category_frame, text="Category: ")
        self.category_label.pack(side="left", padx=(0, 10))
        self.category = CTkOptionMenu(
            self.category_frame, values=[category for category in categories]
        )
        self.category.pack(side="left")
        self.category.set("")
        self.date_frame = CTkFrame(self, fg_color="transparent")
        self.date_frame.pack(pady=5, padx=(55, 0))
        self.date_label = CTkLabel(self.date_frame, text="Date: ")
        self.date_label.pack(side="left", padx=(0, 10))
        self.date_entry_var = tkinter.StringVar()
        self.date_entry = CTkEntry(
            self.date_frame, textvariable=self.date_entry_var, width=300
        )
        self.date_entry.pack(side="left")
        self.date_entry.bind("<Button-1>", self.open_calendar)
        self.amount_frame = CTkFrame(self, fg_color="transparent")
        self.amount_frame.pack(pady=5, padx=(70, 0))
        self.transaction_amount_label = CTkLabel(self.amount_frame, text="Amount: ")
        self.transaction_amount_label.pack(side="left", padx=(0, 10))
        self.transaction_amount = CTkEntry(
            self.amount_frame,
            placeholder_text="Enter the transaction amount",
            width=300,
            validate="key",
            validatecommand=(vcmd, "%P"),
        )
        self.transaction_amount.pack(side="left", padx=(2.5, 0))
        self.transaction_amount.bind("<Return>", self.post_transaction)
        self.submit_button = CTkButton(
            self, text="Submit", command=self.post_transaction
        )
        self.submit_button.pack()
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.place(relx=0.05, rely=0.05, anchor="center")

    def update_amount_prefix(self, transaction_type):
        if hasattr(self, "amount_prefix"):
            self.amount_prefix.destroy()
        prefix = "$" if transaction_type in ["Deposit"] else "-$"
        color = "green" if prefix == "$" else "red"
        self.transaction_amount.configure(text_color=color)
        self.amount_prefix = CTkLabel(self.amount_frame, text=prefix, text_color=color)
        self.amount_prefix.pack(
            side="left",
            after=self.transaction_amount_label,
            before=self.transaction_amount,
            padx=0,
        )

    def open_calendar(self, event):
        def select_date():
            selected = cal.selection_get()
            self.date_entry_var.set(selected.strftime("%Y-%m-%d"))
            top.destroy()

        top = tkinter.Toplevel(self)
        top.grab_set()
        top.geometry("+%d+%d" % (event.x_root, event.y_root))
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack()
        ok_button = tkinter.Button(top, text="OK", command=select_date)
        ok_button.pack()

    def post_transaction(self, event=None):
        account = self.account.get()
        transaction_type = self.transaction_type.get()
        category = self.category.get()
        amount = float(self.transaction_amount.get())
        date = datetime.datetime.strptime(self.date_entry_var.get(), "%Y-%m-%d").date()
        beginning_amount = accounts[account].balance
        ending_amount = (
            accounts[account].balance + amount
            if transaction_type == "Deposit"
            else accounts[account].balance - amount
        )
        transaction = Transaction(
            category,
            transaction_type,
            amount if transaction_type == "Deposit" else -amount,
            date,
            beginning_amount,
            ending_amount,
        )
        accounts[account].transactions.append(transaction)
        save_accounts(accounts)
        self.notify = CTkLabel(
            self,
            text="Updating accounts...",
            text_color="green",
            font=("times", 25, "bold"),
        )
        self.notify.place(relx=0.5, rely=0.5)
        self.after(1000, lambda: self.master.change_page(PostTransactionPage))


class EditTransactionPage(PostTransactionPage):
    def __init__(self, master, transaction, account):
        super().__init__(master)
        self.transaction_type.set(transaction.type)
        self.update_amount_prefix(transaction.type)
        self.account.set(account.name)
        self.category.set(transaction.category)
        date_string = (
            transaction.date.strftime("%Y-%m-%d")
            if isinstance(transaction.date, (datetime.date, datetime.datetime))
            else str(transaction.date)
        )
        self.date_entry_var.set(date_string)
        self.transaction_amount.delete(0, "end")
        self.transaction_amount.insert(0, f"{abs(transaction.amount):.2f}")
        self.submit_button.configure(command=self.save_edited_transaction)
        self.remove_button = CTkButton(
            self,
            text="Delete this transaction",
            command=lambda: self.delete_transaction(account, transaction),
        )
        self.remove_button.pack()

    def delete_transaction(self, account, transaction):
        account.transactions.remove(transaction)
        self.notify = CTkLabel(
            self,
            text="Deleting transaction...",
            text_color="green",
            font=("times", 25, "bold"),
        )
        self.notify.place(relx=0.5, rely=0.5)
        self.after(1000, lambda: self.master.change_page(AccountsPage))

    def save_edited_transaction(self, event=None):
        edited_type = self.transaction_type.get()
        edited_category = self.category.get()
        edited_amount = float(self.transaction_amount.get())
        edited_date = datetime.datetime.strptime(
            self.date_entry_var.get(), "%Y-%m-%d"
        ).date()
        account_obj = accounts[account.name]
        index = account_obj.transactions.index(transaction)
        account_obj.transactions.pop(index)
        beginning_balance = transaction.beginning_balance
        if edited_type == "Deposit":
            ending_balance = beginning_balance + edited_amount
            adj_amount = edited_amount
        else:
            ending_balance = beginning_balance - edited_amount
            adj_amount = -edited_amount
        new_transaction = Transaction(
            edited_category,
            edited_type,
            adj_amount,
            edited_date,
            beginning_balance,
            ending_balance,
        )
        account_obj.transactions.insert(index, new_transaction)
        save_accounts(accounts)
        self.master.change_page(lambda master: AccountDetailsPage(master, account_obj))


class CategoryPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.categories_label = CTkLabel(
            self, text="Categories", font=("times", 30, "bold")
        )
        self.categories_label.pack(pady=(50, 10))
        self.categories_panel = CTkFrame(self)
        self.categories_panel.pack(pady=(0, 20))
        for row, category in enumerate(categories):
            label = CTkLabel(self.categories_panel, text=category)
            label.grid(row=row, column=0, pady=15, padx=20)
        self.add_category_label = CTkLabel(
            self, text="Use the box below to enter a new category:"
        )
        self.add_category_label.place(relx=0.2, rely=0.225, anchor="center")
        self.add_category_box = CTkEntry(self, placeholder_text="Enter Category here:")
        self.add_category_box.place(relx=0.2, rely=0.25, anchor="center")
        self.add_category_box.bind("<Return>", self.update)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.place(relx=0.05, rely=0.05, anchor="center")

    def update(self, event=None):
        categories.append(self.add_category_box.get())
        save_categories(categories)
        self.master.change_page(CategoryPage)


class SettingsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_label = CTkLabel(self, text="Settings", font=("times", 30, "bold"))
        self.main_label.pack(pady=(15, 10))
        self.section_frame = CTkFrame(self, fg_color="transparent")
        self.section_frame.pack(pady=(10, 0), padx=250)
        self.theme_section = CTkFrame(self.section_frame, fg_color="transparent")
        self.theme_section.pack(side="left", padx=30, anchor="n")
        self.theme_label = CTkLabel(
            self.theme_section, text="Theme", font=("times", 20, "bold")
        )
        self.theme_label.pack(anchor="w", pady=(0, 10))
        self.light_mode_button = CTkButton(
            self.theme_section,
            text="Light",
            command=lambda: set_appearance_mode("light"),
        )
        self.light_mode_button.pack(pady=(0, 10), anchor="w")
        self.dark_mode_button = CTkButton(
            self.theme_section, text="Dark", command=lambda: set_appearance_mode("dark")
        )
        self.dark_mode_button.pack(pady=(0, 10), anchor="w")
        self.accent_section = CTkFrame(self.section_frame, fg_color="transparent")
        self.accent_section.pack(side="left", padx=30, anchor="n")
        self.accent_label = CTkLabel(
            self.accent_section, text="Accent Color", font=("times", 20, "bold")
        )
        self.accent_label.pack(anchor="w", pady=(0, 10))
        self.accent_select_box = CTkOptionMenu(
            self.accent_section, values=["Blue", "Green", "Dark-Blue"]
        )
        self.accent_select_box.pack(anchor="w")
        self.apply_button = CTkButton(
            self.accent_section,
            text="Apply",
            command=lambda: self.change_theme(self.accent_select_box.get()),
        )
        self.apply_button.pack(pady=(10, 20), anchor="w")
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(HomePage)
        )
        self.back_button.place(relx=0.05, rely=0.05, anchor="center")

    def change_theme(self, theme):
        self.confirm_box = CTkFrame(self)
        self.confirm_box.pack(expand=True, pady=50, padx=50)
        content_frame = CTkFrame(
            self.confirm_box,
            width=int(self.winfo_width() * 0.75),
            height=int(self.winfo_height() * 0.75),
        )
        content_frame.pack(expand=True)
        content_frame.pack_propagate(False)
        self.confirm_text = CTkLabel(
            content_frame,
            text="Updating the theme settings will require restarting the app.\n"
            "Press continue to close the app and then reopen it, or return to do this later.",
            font=("times", 30, "bold"),
            wraplength=int(self.winfo_width() * 0.7),
            justify="center",
        )
        self.confirm_text.pack(pady=(30, 40))
        button_frame = CTkFrame(content_frame)
        button_frame.pack(pady=10)
        CTkButton(
            button_frame, text="Continue", command=lambda: self.save_theme_change(theme)
        ).pack(side="left", padx=20)
        CTkButton(
            button_frame, text="Cancel", command=lambda: self.confirm_box.destroy()
        ).pack(side="right", padx=20)

    def save_theme_change(self, theme):
        with open("custom_theme.cfg", "w") as f:
            f.write(theme)
        sys.exit()


class StatisticsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.statistics_label = CTkLabel(self, text="Statistics")
        self.statistics_label.place(relx=0.5, rely=0.23, anchor="center")
        self.text = CTkLabel(self, text="More coming soon!")
        self.text.place(relx=0.5, rely=0.5, anchor="center")
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(HomePage)
        )


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.title("Python Pocket")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.login_page = LoginPage(self)
        self.current_page = self.login_page
        if os.path.isfile("password.pkl"):
            self.login_page = LoginPage(self)
            self.current_page = self.login_page
            self.login_page.pack(fill="both", expand=True)
        else:
            self.password_setup_page = PasswordSetupPage(self)
            self.current_page = self.password_setup_page
            self.password_setup_page.pack(fill="both", expand=True)

    def change_page(self, new_page):
        self.current_page.destroy()
        self.current_page = new_page(self)
        self.current_page.pack(fill="both", expand=True)

    def show_login_page(self):
        self.current_page.pack_forget()
        self.current_page = self.login_page
        self.login_page.pass_input.delete(0, "end")
        self.login_page.error_label.configure(text="")
        self.login_page.pack(fill="both", expand=True)

    def on_exit(self):
        save_accounts(accounts)
        save_categories(categories)
        self.destroy()


if __name__ == "__main__":
    theme = find_theme()
    if theme:
        set_default_color_theme(theme)
    categories = load_categories()
    accounts = load_accounts()
    app = App()
    app.mainloop()
