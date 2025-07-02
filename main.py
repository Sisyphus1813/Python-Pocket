from customtkinter import *
from data_handler import (
    load_accounts,
    load_categories,
    load_ui_settings,
    save_accounts,
    save_categories,
    save_ui_settings,
    hash_password,
    verify_password,
    update_accounts,
)
from data_classes import (
    Account,
    CheckingAccount,
    SavingsAccount,
    InvestmentAccount,
    CreditAccount,
    LoanAccount,
    Transaction,
    RecurringTransaction,
)
from tkcalendar import Calendar
import pickle, datetime, tkinter, os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict


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
            with open(".local/password.pkl", "rb") as f:
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
        with open(".local/password.pkl", "wb") as f:
            pickle.dump(hashed, f)
        self.error_label.configure(
            text_color="green", text="Password set. Logging in..."
        )
        self.after(1500, lambda: self.master.change_page(HomePage))


class HomePage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_label = CTkLabel(
            self, text="Python Pocket", font=(font, MAIN_TITLE_SIZE, "bold")
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
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(HomePage)
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.accounts_label = CTkLabel(
            self, text="Accounts", font=(font, MAIN_TITLE_SIZE, "bold")
        )
        self.accounts_label.pack(pady=(50, 10))
        self.bottom_buttons_frame = CTkFrame(self, fg_color="transparent")
        self.bottom_buttons_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.create_account_button = CTkButton(
            self.bottom_buttons_frame,
            text="Create a new account",
            command=lambda: master.change_page(CreateAccountPage),
        )
        self.create_account_button.pack(side="bottom", anchor="w", pady=2)
        self.post_transaction_button = CTkButton(
            self.bottom_buttons_frame,
            text="Post a new Transaction",
            command=lambda: master.change_page(PostTransactionPage),
        )
        self.post_transaction_button.pack(side="bottom", anchor="w", pady=2)
        self.add_category_button = CTkButton(
            self.bottom_buttons_frame,
            text="Manage transaction Categories",
            command=lambda: master.change_page(CategoryPage),
        )
        self.add_category_button.pack(side="bottom", anchor="w", pady=2)
        self.accounts_panel = CTkFrame(self, fg_color="transparent")
        self.accounts_panel.pack(pady=(0, 10))
        for col, header in enumerate(["", "Name", "Account Type", "Balance"]):
            CTkLabel(
                self.accounts_panel, text=header, font=(font, SECTION_TITLE_SIZE)
            ).grid(row=0, column=col, padx=15, pady=20)
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
            CTkLabel(
                self.accounts_panel, text=account.name, font=(font, NORMAL_TEXT_SIZE)
            ).grid(row=row, column=1, padx=15, pady=20)
            CTkLabel(
                self.accounts_panel, text=account.type, font=(font, NORMAL_TEXT_SIZE)
            ).grid(row=row, column=2, padx=15, pady=20)
            balance_value = account.balance
            balance_text = f"${balance_value:,.2f}"
            balance_color = "green" if balance_value >= 0 else "red"
            CTkLabel(
                self.accounts_panel,
                text=balance_text,
                text_color=balance_color,
                font=(font, NORMAL_TEXT_SIZE),
            ).grid(row=row, column=3, padx=15, pady=10)


class AccountDetailsPage(CTkFrame):
    def __init__(self, master, account):
        super().__init__(master)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.account = account
        self.title = CTkLabel(
            self, text=f"{account.name}", font=(font, MAIN_TITLE_SIZE, "bold")
        )
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
            elif label_key == "Repeating Transactions":
                label_key = "Recurring Transactions"
                label_value = CTkButton(
                    self.details_frame,
                    text="Edit recurring transactions",
                    command=lambda a=account: self.master.change_page(
                        lambda master: RecurringTransactionsPage(master, a)
                    ),
                ).grid(row=row + 1, column=col, pady=(0, 0), sticky="s")
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
                self.details_frame,
                text=f"{label_key}:",
                font=(font, SECTION_TITLE_SIZE, "bold"),
            ).grid(row=row * 2, column=col, sticky="w", padx=15, pady=(2, 0))
            CTkLabel(
                self.details_frame,
                text=label_value,
                font=(font, SECTION_TITLE_SIZE),
                text_color=color,
            ).grid(row=row * 2 + 1, column=col, sticky="w", padx=15, pady=(0, 6))
        if not account.transactions:
            CTkLabel(self, text="No transactions found.").pack()
        else:
            self.transactions_label = CTkLabel(
                self, text="Transactions", font=(font, NORMAL_TEXT_SIZE, "bold")
            )
            self.transactions_label.pack(pady=(0, 5))
            self.scroll_frame = CTkScrollableFrame(self, fg_color="transparent")
            self.scroll_frame.pack(pady=(0, 5), anchor="s")
            self.bind("<Configure>", self.resize_scroll_frame)
            headers = [
                "",
                "Date",
                "Category",
                "Type",
                "Start Balance",
                "Amount",
                "End Balance",
            ]
            for col, header in enumerate(headers):
                CTkLabel(
                    self.scroll_frame, text=header, font=(font, SMALL_TEXT_SIZE, "bold")
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
                ).grid(row=row, column=0, padx=20, pady=2)
                date_display = (
                    transaction.date.strftime("%Y-%m-%d")
                    if isinstance(transaction.date, (datetime.date, datetime.datetime))
                    else str(transaction.date)
                )
                CTkLabel(self.scroll_frame, text=date_display).grid(row=row, column=1)
                CTkLabel(self.scroll_frame, text=transaction.category).grid(
                    row=row, column=2, padx=20
                )
                CTkLabel(self.scroll_frame, text=transaction.type).grid(
                    row=row, column=3, padx=20
                )
                CTkLabel(
                    self.scroll_frame,
                    text=f"${transaction.beginning_balance:.2f}",
                    text_color="green" if transaction.beginning_balance > 0 else "red",
                ).grid(row=row, column=4, padx=10)
                CTkLabel(
                    self.scroll_frame,
                    text=f"${transaction.amount:.2f}",
                    text_color="green" if transaction.type == "Deposit" else "red",
                ).grid(row=row, column=5, padx=10)
                CTkLabel(
                    self.scroll_frame,
                    text=f"${transaction.ending_balance:.2f}",
                    text_color="green" if transaction.ending_balance > 0 else "red",
                ).grid(row=row, column=6, padx=10)

    def resize_scroll_frame(self, event):
        target_width = int(event.width * 0.65)
        target_height = int(event.height * 0.7)
        self.scroll_frame.configure(width=target_width, height=target_height)


class RecurringTransactionsPage(CTkFrame):
    def __init__(self, master, account):
        super().__init__(master)
        self.account = account
        self.back_button = CTkButton(
            self,
            text="Back",
            command=lambda: master.change_page(
                lambda master: AccountDetailsPage(master, self.account)
            ),
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.title = CTkLabel(
            self,
            text=f"Recurring Transactions for {account.name}",
            font=(font, SECTION_TITLE_SIZE, "bold"),
        )
        self.title.pack(pady=(30, 10))
        if not account.repeating_transactions:
            CTkLabel(self, text="No recurring transactions found.").pack()
        else:
            self.scroll_frame = CTkScrollableFrame(self, fg_color="transparent")
            self.scroll_frame.pack(pady=(0, 5), fill="both", expand=True)
            headers = ["", "Category", "Type", "Amount", "Start Date", "Schedule"]
            for col, header in enumerate(headers):
                CTkLabel(
                    self.scroll_frame,
                    text=header,
                    font=(font, SMALL_TEXT_SIZE, "bold"),
                ).grid(row=0, column=col, padx=15, pady=5)
            for row, transaction in enumerate(account.repeating_transactions, start=1):
                CTkButton(
                    self.scroll_frame,
                    text="Edit",
                    width=50,
                    height=20,
                    command=lambda t=transaction, a=account: self.master.change_page(
                        lambda master: EditRecurringTransactionPage(master, t, a)
                    ),
                ).grid(row=row, column=0, padx=20, pady=2)
                CTkLabel(self.scroll_frame, text=transaction.category).grid(
                    row=row, column=1, padx=20
                )
                CTkLabel(self.scroll_frame, text=transaction.type).grid(
                    row=row, column=2, padx=20
                )
                amount_text = f"${transaction.amount:,.2f}"
                amount_color = "green" if transaction.type == "Deposit" else "red"
                CTkLabel(
                    self.scroll_frame, text=amount_text, text_color=amount_color
                ).grid(row=row, column=3, padx=10)
                date_display = (
                    transaction.date.strftime("%Y-%m-%d")
                    if isinstance(transaction.date, (datetime.date, datetime.datetime))
                    else str(transaction.date)
                )
                CTkLabel(self.scroll_frame, text=date_display).grid(
                    row=row, column=4, padx=20
                )
                CTkLabel(self.scroll_frame, text=transaction.schedule).grid(
                    row=row, column=5, padx=20
                )


class CreateAccountPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        self.main_label = CTkLabel(
            self, text="New Account", font=(font, SECTION_TITLE_SIZE, "bold")
        )
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
        self.submit_button = CTkButton(
            self, text="Submit", command=self.initialize_account
        )
        self.submit_button.pack(pady=5)

    def update_page(self, account_type):
        if hasattr(self, "balance_prefix"):
            self.balance_prefix.destroy()
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
        if self.account_type.get() == "Credit":
            self.limit_frame = CTkFrame(self, fg_color="transparent")
            self.limit_frame.pack(
                after=self.account_balance_frame,
                before=self.submit_button,
                pady=5,
                padx=(25, 0),
            )
            self.limit_label = CTkLabel(self.limit_frame, text="Credit limit: ")
            self.limit_label.pack(side="left", padx=(0, 10))
            self.limit = CTkEntry(self.limit_frame, placeholder_text=0.00, width=300)
            self.limit.pack(side="left")
            self.due_date_frame = CTkFrame(self, fg_color="transparent")
            self.due_date_frame.pack(
                after=self.limit_frame, before=self.submit_button, pady=5, padx=(5, 0)
            )
            self.due_date_label = CTkLabel(self.due_date_frame, text="Due date: ")
            self.due_date_label.pack(side="left", padx=(0, 5))
            self.due_date_var = tkinter.StringVar()
            self.due_date = CTkEntry(
                self.due_date_frame, textvariable=self.due_date_var, width=300
            )
            self.due_date.pack(side="left")
            self.due_date.bind("<Button-1>", self.open_calendar)
        elif self.account_type.get() == "Loan":
            self.due_date_frame = CTkFrame(self, fg_color="transparent")
            self.due_date_frame.pack(
                after=self.account_balance_frame,
                before=self.submit_button,
                pady=5,
                padx=(5, 0),
            )
            self.due_date_label = CTkLabel(self.due_date_frame, text="Due date: ")
            self.due_date_label.pack(side="left", padx=(0, 5))
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
        limit = (
            float(self.limit.get())
            if hasattr(self, "limit") and self.limit.get()
            else 0.0
        )
        due_date = self.due_date_var.get() if hasattr(self, "due_date") else None
        match account_type:
            case "Checking":
                accounts[account_name] = CheckingAccount(
                    name=account_name,
                    balance=account_balance,
                )
            case "Savings":
                accounts[account_name] = SavingsAccount(
                    name=account_name,
                    balance=account_balance,
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
                    limit=limit,
                    due_date=due_date,
                )
            case "Loan":
                accounts[account_name] = LoanAccount(
                    name=account_name,
                    balance=-account_balance,
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
            font=(font, NORMAL_TEXT_SIZE, "bold"),
        )
        self.notify.place(relx=0.5, rely=0.5)
        self.after(1000, lambda: self.master.change_page(CreateAccountPage))


class PostTransactionPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.main_label = CTkLabel(
            self, text="New Transaction", font=(font, SECTION_TITLE_SIZE, "bold")
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
            command=self.update_page,
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
        self.reccurence_frame = CTkFrame(self, fg_color="transparent")
        self.reccurence_frame.pack(pady=5, padx=(0, 75))
        self.recurrence_label = CTkLabel(self.reccurence_frame, text="Repeating: ")
        self.recurrence_label.pack(side="left", padx=(0, 10))
        self.recurrence = CTkOptionMenu(
            self.reccurence_frame,
            values=["Never", "Daily", "Weekly", "Monthly", "Annually"],
        )
        self.recurrence.pack(side="left")
        self.recurrence.set("Never")
        self.submit_button = CTkButton(
            self, text="Submit", command=self.post_transaction
        )
        self.submit_button.pack(pady=5)

    def update_page(self, transaction_type):
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
        reccuring_period = self.recurrence.get()
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
        if reccuring_period != "Never":
            accounts[account].repeating_transactions.append(
                RecurringTransaction(
                    category,
                    transaction_type,
                    amount if transaction_type == "Deposit" else -amount,
                    date,
                    reccuring_period,
                )
            )
        update_accounts(accounts)
        save_accounts(accounts)
        self.notify = CTkLabel(
            self,
            text="Updating accounts...",
            text_color="green",
            font=(font, NORMAL_TEXT_SIZE, "bold"),
        )
        self.notify.place(relx=0.5, rely=0.5)
        self.after(1000, lambda: self.master.change_page(PostTransactionPage))


class EditTransactionPage(PostTransactionPage):
    def __init__(self, master, transaction, account):
        super().__init__(master)
        self.transaction = transaction
        self.account_obj = account
        self.account.configure(state="disabled")
        self.account.set(account.name)
        self.transaction_type.set(transaction.type)
        self.update_page(transaction.type)
        self.category.set(transaction.category)
        self.transaction_amount.delete(0, "end")
        self.transaction_amount.insert(0, f"{abs(transaction.amount):.2f}")
        date_string = (
            transaction.date.strftime("%Y-%m-%d")
            if isinstance(transaction.date, (datetime.date, datetime.datetime))
            else str(transaction.date)
        )
        self.date_entry_var.set(date_string)
        self.recurrence.destroy()
        self.recurrence = CTkLabel(
            self.reccurence_frame,
            text="Editing recurring transactions is not supported on this page.",
            text_color="red",
        )
        self.recurrence.pack(after=self.recurrence_label, padx=(0, 0))
        self.submit_button.configure(command=self.save_edited_transaction)
        self.remove_button = CTkButton(
            self,
            text="Delete this transaction",
            command=lambda: self.delete_transaction(account, transaction),
        )
        self.remove_button.pack(pady=5)

    def delete_transaction(self, account, transaction):
        account.transactions.remove(transaction)
        self.notify = CTkLabel(
            self,
            text="Deleting transaction...",
            text_color="green",
            font=(font, NORMAL_TEXT_SIZE, "bold"),
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
        account_obj = accounts[self.account.get()]
        transaction_index = account_obj.transactions.index(self.transaction)
        account_obj.transactions.pop(transaction_index)
        beginning_balance = self.transaction.beginning_balance
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
        account_obj.transactions.insert(transaction_index, new_transaction)
        update_accounts(accounts)
        save_accounts(accounts)
        self.master.change_page(lambda master: AccountDetailsPage(master, account_obj))


class EditRecurringTransactionPage(PostTransactionPage):
    def __init__(self, master, transaction, account):
        super().__init__(master)
        self.transaction = transaction
        self.account_obj = account
        self.account.configure(state="disabled")
        self.account.set(account.name)
        self.transaction_type.set(transaction.type)
        self.update_page(transaction.type)
        self.category.set(transaction.category)
        self.transaction_amount.delete(0, "end")
        self.transaction_amount.insert(0, f"{abs(transaction.amount):.2f}")
        date_string = (
            transaction.date.strftime("%Y-%m-%d")
            if isinstance(transaction.date, (datetime.date, datetime.datetime))
            else str(transaction.date)
        )
        self.date_entry_var.set(date_string)
        self.recurrence.configure(values=["Daily", "Weekly", "Monthly", "Annually"])
        self.recurrence.set(transaction.schedule)
        self.submit_button.configure(command=self.save_edited_transaction)
        self.remove_button = CTkButton(
            self,
            text="Delete this transaction",
            command=lambda: self.delete_transaction(account, transaction),
        )
        self.remove_button.pack(pady=5)

    def delete_transaction(self, account, transaction):
        account.repeating_transactions.remove(transaction)
        save_accounts(accounts)
        self.notify = CTkLabel(
            self,
            text="Deleting transaction...",
            text_color="green",
            font=(font, NORMAL_TEXT_SIZE, "bold"),
        )
        self.notify.place(relx=0.5, rely=0.5)
        self.after(
            1000,
            lambda: self.master.change_page(
                lambda master: RecurringTransactionsPage(master, account)
            ),
        )

    def save_edited_transaction(self, event=None):
        edited_type = self.transaction_type.get()
        edited_category = self.category.get()
        edited_amount = float(self.transaction_amount.get())
        edited_date = datetime.datetime.strptime(
            self.date_entry_var.get(), "%Y-%m-%d"
        ).date()
        account_obj = self.account_obj
        transaction_index = account_obj.repeating_transactions.index(self.transaction)
        account_obj.repeating_transactions.pop(transaction_index)
        edited_recurrence = self.recurrence.get()
        new_transaction = RecurringTransaction(
            category=edited_category,
            type=edited_type,
            amount=edited_amount if edited_type == "Deposit" else -edited_amount,
            date=edited_date,
            schedule=edited_recurrence,
        )
        account_obj.repeating_transactions.insert(transaction_index, new_transaction)
        update_accounts(accounts)
        save_accounts(accounts)
        self.master.change_page(
            lambda master: RecurringTransactionsPage(master, account_obj)
        )


class CategoryPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(AccountsPage)
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.categories_label = CTkLabel(
            self, text="Categories", font=(font, MAIN_TITLE_SIZE, "bold")
        )
        self.categories_label.pack(pady=(50, 10))
        self.categories_panel = CTkFrame(self)
        self.categories_panel.pack(pady=(0, 20))
        for row, category in enumerate(categories):
            label = CTkLabel(
                self.categories_panel, text=category, font=(font, NORMAL_TEXT_SIZE)
            )
            label.grid(row=row, column=0, pady=15, padx=20)
        self.add_category_label = CTkLabel(
            self, text="Use the box below to enter a new category:"
        )
        self.add_category_label.place(relx=0.2, rely=0.225, anchor="center")
        self.add_category_box = CTkEntry(self, placeholder_text="Enter Category here:")
        self.add_category_box.place(relx=0.2, rely=0.25, anchor="center")
        self.add_category_box.bind("<Return>", self.update)

    def update(self, event=None):
        categories.append(self.add_category_box.get())
        save_categories(categories)
        self.master.change_page(CategoryPage)


class StatisticsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.back_button = CTkButton(
            self, text="Back", command=lambda: master.change_page(HomePage)
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.main_label = CTkLabel(
            self, text="Statistics", font=(font, MAIN_TITLE_SIZE, "bold")
        )
        self.main_label.pack(pady=(15, 10), padx=(160, 0))
        self.chart_container = CTkFrame(self)
        self.chart_container.pack(
            side="right", fill="both", expand=True, padx=20, pady=20
        )
        self.views = CTkFrame(self, fg_color="transparent")
        self.views.pack(side="left", pady=10)
        self.expenses_button = CTkButton(
            self.views, text="Expenses", command=self.show_expenses_chart
        )
        self.expenses_button.pack(side="top", pady=5, padx=10)
        self.income_button = CTkButton(
            self.views, text="Income", command=self.show_income_chart
        )
        self.income_button.pack(after=self.expenses_button, side="top", pady=5, padx=10)
        self.chart_type_frame = CTkFrame(self.chart_container, fg_color="transparent")
        self.chart_type_frame.pack(fill="x", pady=(0, 10))
        self.button_container = CTkFrame(self.chart_type_frame, fg_color="transparent")
        self.button_container.pack(expand=True)
        self.pie_chart_button = CTkButton(
            self.button_container, text="Pie Chart", command=self.show_pie_chart
        )
        self.pie_chart_button.pack(side="left", padx=5)
        self.graph_chart_button = CTkButton(
            self.button_container, text="Graph Chart", command=self.show_graph_chart
        )
        self.graph_chart_button.pack(side="left", padx=5)
        self.current_data = None
        self.current_title = None
        self.current_figure = None
        self.current_canvas = None
        self.show_expenses_chart()

    def clear_chart_container(self):
        if self.current_figure:
            plt.close(self.current_figure)
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
        for widget in self.chart_container.winfo_children():
            if widget != self.chart_type_frame:
                widget.destroy()

    def create_pie_chart(self, data, title):
        try:
            self.clear_chart_container()
            self.current_data = data
            self.current_title = title
            is_dark = get_appearance_mode().lower() == "dark"
            bg_color = "black" if is_dark else "white"
            text_color = "white" if is_dark else "black"
            self.current_figure, ax = plt.subplots(figsize=(8, 6))
            self.current_figure.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            wedges, texts, autotexts = ax.pie(
                data.values(),
                labels=data.keys(),
                autopct="%1.1f%%",
                textprops={"fontsize": 8, "color": text_color},
            )
            ax.set_title(title, pad=20, fontsize=14, color=text_color)
            self.current_canvas = FigureCanvasTkAgg(
                self.current_figure, master=self.chart_container
            )
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error creating pie chart: {e}")

    def create_graph_chart(self, data, title):
        try:
            self.clear_chart_container()
            self.current_data = data
            self.current_title = title
            is_dark = get_appearance_mode().lower() == "dark"
            bg_color = "black" if is_dark else "white"
            text_color = "white" if is_dark else "black"
            self.current_figure, ax = plt.subplots(figsize=(8, 6))
            self.current_figure.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            categories = list(data.keys())
            values = list(data.values())
            bars = ax.bar(categories, values)
            ax.set_title(title, pad=20, fontsize=14, color=text_color)
            ax.set_xticks(range(len(categories)))
            ax.set_xticklabels(categories, rotation=45, ha="right", color=text_color)
            ax.tick_params(axis="y", colors=text_color)
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"${height:,.2f}",
                    ha="center",
                    va="bottom",
                    color=text_color,
                )
            plt.tight_layout()
            self.current_canvas = FigureCanvasTkAgg(
                self.current_figure, master=self.chart_container
            )
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error creating graph chart: {e}")

    def show_pie_chart(self):
        if self.current_data and self.current_title:
            self.create_pie_chart(self.current_data, self.current_title)

    def show_graph_chart(self):
        if self.current_data and self.current_title:
            self.create_graph_chart(self.current_data, self.current_title)

    def show_expenses_chart(self):
        try:
            expenses_by_category = defaultdict(float)
            for account in accounts.values():
                for transaction in account.transactions:
                    if transaction.type == "Withdraw":
                        expenses_by_category[transaction.category] += abs(
                            transaction.amount
                        )
            if not expenses_by_category:
                self.clear_chart_container()
                CTkLabel(
                    self.chart_container,
                    text="No expense data available",
                    font=(font, NORMAL_TEXT_SIZE),
                ).pack(expand=True)
                return
            self.create_pie_chart(expenses_by_category, "Expenses by Category")
        except Exception as e:
            print(f"Error showing expenses chart: {e}")

    def show_income_chart(self):
        try:
            income_by_category = defaultdict(float)
            for account in accounts.values():
                for transaction in account.transactions:
                    if transaction.type == "Deposit":
                        income_by_category[transaction.category] += transaction.amount
            if not income_by_category:
                self.clear_chart_container()
                CTkLabel(
                    self.chart_container,
                    text="No income data available",
                    font=(font, NORMAL_TEXT_SIZE),
                ).pack(expand=True)
                return
            self.create_pie_chart(income_by_category, "Income by Category")
        except Exception as e:
            print(f"Error showing income chart: {e}")

    def destroy(self):
        if self.current_figure:
            plt.close(self.current_figure)
        super().destroy()


class SettingsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.back_button = CTkButton(
            self,
            text="Back",
            command=lambda: master.change_page(self.master.previous_page),
        )
        self.back_button.pack(anchor="w", padx=10, pady=10)
        self.main_label = CTkLabel(
            self, text="Settings", font=(font, MAIN_TITLE_SIZE, "bold")
        )
        self.main_label.pack(pady=(15, 10))
        self.selection_frame = CTkFrame(self, fg_color="transparent")
        self.selection_frame.pack(pady=(10, 0), padx=10)
        self.theme_selection = CTkFrame(self.selection_frame, fg_color="transparent")
        self.theme_selection.pack(side="left", padx=30, anchor="n")
        self.theme_label = CTkLabel(
            self.theme_selection, text="Theme", font=(font, SECTION_TITLE_SIZE, "bold")
        )
        self.theme_label.pack(anchor="w", pady=(0, 10))
        self.light_mode_button = CTkButton(
            self.theme_selection,
            text="Light",
            command=lambda: (
                set_appearance_mode("light"),
                self.save_theme(
                    self.font_select_box.get().lower(),
                    self.accent_select_box.get(),
                    "light",
                ),
            ),
        )
        self.light_mode_button.pack(pady=(0, 10), anchor="w")
        self.dark_mode_button = CTkButton(
            self.theme_selection,
            text="Dark",
            command=lambda: (
                set_appearance_mode("dark"),
                self.save_theme(
                    self.font_select_box.get().lower(),
                    self.accent_select_box.get(),
                    "dark",
                ),
            ),
        )
        self.dark_mode_button.pack(pady=(0, 10), anchor="w")
        self.font_selection = CTkFrame(self.selection_frame, fg_color="transparent")
        self.font_selection.pack(side="left", padx=30, anchor="n")
        self.font_label = CTkLabel(
            self.font_selection, text="Font", font=(font, SECTION_TITLE_SIZE, "bold")
        )
        self.font_label.pack(anchor="w", pady=(0, 10))
        self.font_select_box = CTkOptionMenu(
            self.font_selection,
            values=[
                "Arial",
                "Helvetica",
                "Times New Roman",
                "Verdana",
                "Calibri",
                "Georgia",
            ],
            command=self.preview_font,
        )
        self.font_select_box.pack(anchor="w")
        self.accent_selection = CTkFrame(self.selection_frame, fg_color="transparent")
        self.accent_selection.pack(side="left", padx=30, anchor="n")
        self.accent_label = CTkLabel(
            self.accent_selection,
            text="Accent Color",
            font=(font, SECTION_TITLE_SIZE, "bold"),
        )
        self.accent_label.pack(anchor="w", pady=(0, 10))
        self.accent_select_box = CTkOptionMenu(
            self.accent_selection, values=["Blue", "Green", "Dark-Blue"]
        )
        self.accent_select_box.pack(anchor="w")
        self.apply_button = CTkButton(
            self.accent_selection,
            text="Apply",
            command=lambda: self.save_theme_change(
                self.font_select_box.get().lower(),
                self.accent_select_box.get(),
                get_appearance_mode(),
            ),
        )
        self.apply_button.pack(pady=(10, 20), anchor="w")

    def preview_font(self, font):
        self.font_label.configure(font=(font, SECTION_TITLE_SIZE, "bold"))
        self.font_select_box.configure(font=(font, NORMAL_TEXT_SIZE))

    def save_theme_change(self, font, accent, theme):
        close = True
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
            font=(font, NORMAL_TEXT_SIZE, "bold"),
            wraplength=int(self.winfo_width() * 0.7),
            justify="center",
        )
        self.confirm_text.pack(pady=(30, 40))
        button_frame = CTkFrame(content_frame)
        button_frame.pack(pady=10)
        CTkButton(
            button_frame,
            text="Continue",
            command=lambda: self.save_theme(font, accent, theme, close),
        ).pack(side="left", padx=20)
        CTkButton(
            button_frame, text="Cancel", command=lambda: self.confirm_box.destroy()
        ).pack(side="right", padx=20)

    def save_theme(self, font, accent, theme, close=False):
        save_ui_settings(font, accent, theme)
        if close:
            sys.exit()


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.title("Python Pocket")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.previous_page = None
        if os.path.isfile(".local/password.pkl"):
            self.login_page = LoginPage(self)
            self.current_page = self.login_page
            self.login_page.pack(fill="both", expand=True)
        else:
            self.password_setup_page = PasswordSetupPage(self)
            self.current_page = self.password_setup_page
            self.password_setup_page.pack(fill="both", expand=True)

    def change_page(self, new_page):
        self.previous_page = self.current_page.__class__
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


MAIN_TITLE_SIZE = 28
SECTION_TITLE_SIZE = 22
NORMAL_TEXT_SIZE = 18
SMALL_TEXT_SIZE = 16

if __name__ == "__main__":
    font, accent, theme = load_ui_settings()
    if accent:
        set_default_color_theme(accent)
    if theme:
        set_appearance_mode(theme)
    categories = load_categories()
    accounts = load_accounts()
    update_accounts(accounts)
    app = App()
    app.mainloop()
