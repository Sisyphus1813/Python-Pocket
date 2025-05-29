from customtkinter import *
from data_handler import load_accounts, save_accounts, save_categories, load_categories, hash_password, verify_password
from data_classes import Account, Transaction
from tkcalendar import Calendar
import hashlib, pickle, datetime, tkinter, time

class LoginPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.welcome_label = CTkLabel(self, text = "Welcome to Python Pocket!")
        self.welcome_label.place(relx = 0.5, rely = 0.3, anchor = "center")
        self.pass_input = CTkEntry(self, placeholder_text = "Enter your password", width = 250, show = "*")
        self.pass_input.place(relx = 0.5, rely = 0.35, anchor = "center")
        self.pass_input.bind("<Return>", self.verify_password)
        self.error_label = CTkLabel(self, text = "", text_color = "red")
        self.error_label.place(relx = 0.5, rely = 0.42, anchor = "center")

    def verify_password(self, event = None):
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
            self.error_label.configure(text = "Incorrect password. Try again.")


class PasswordSetupPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.info_label = CTkLabel(self, text = "No password found. Please set one.")
        self.info_label.place(relx = 0.5, rely = 0.25, anchor = "center")
        self.pass_input_1 = CTkEntry(self, placeholder_text = "Enter new password", width = 250, show = "*")
        self.pass_input_1.place(relx = 0.5, rely = 0.35, anchor = "center")
        self.pass_input_2 = CTkEntry(self, placeholder_text = "Re-enter new password", width = 250, show = "*")
        self.pass_input_2.place(relx = 0.5, rely = 0.42, anchor = "center")
        self.pass_input_2.bind("<Return>", self.set_password)
        self.error_label = CTkLabel(self, text = "", text_color = "red")
        self.error_label.place(relx = 0.5, rely = 0.49, anchor = "center")

    def set_password(self, event = None):
        password1 = self.pass_input_1.get()
        password2 = self.pass_input_2.get()
        if password1 != password2:
            self.error_label.configure(text = "Passwords do not match.")
            return
        if not password1:
            self.error_label.configure(text = "Password cannot be empty.")
            return
        hashed = hash_password(password1)
        with open("password.pkl", "wb") as f:
            pickle.dump(hashed, f)
        self.error_label.configure(text = "Password set. Returning to login...")
        self.after(1500, self.master.change_page(HomePage))

class HomePage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_label = CTkLabel(self, text = "Python Pocket", font = ("times", 40, "bold"))
        self.main_label.place(relx = 0.5, rely = 0.1, anchor = "center")
        self.accounts_button = CTkButton(self, text = "Accounts", command = lambda: master.change_page(AccountsPage))
        self.accounts_button.place(relx = 0.5, rely = 0.2, anchor = "center")
        self.statistics_button = CTkButton(self, text = "Statistics", command = lambda: master.change_page(StatisticsPage))
        self.statistics_button.place(relx = 0.5, rely = 0.25, anchor = "center")
        self.settings_button = CTkButton(self, text = "Settings", command = lambda: master.change_page(SettingsPage))
        self.settings_button.place(relx = 0.5, rely = 0.3, anchor = "center")

class AccountsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        load_accounts()
        self.accounts_label = CTkLabel(self, text = "Accounts", font = ("times", 30, "bold"))
        self.accounts_label.pack(pady = (50, 10))
        self.create_account_button = CTkButton(self, text = "Create a new account", command = lambda: master.change_page(CreateAccountPage))
        self.create_account_button.place(relx = 0.01, rely = 0.85, anchor = "w")
        self.post_transaction_button = CTkButton(self, text = "Post a new Transaction", command = lambda: master.change_page(PostTransactionPage))
        self.post_transaction_button.place(relx = 0.01, rely = 0.9, anchor = "w")
        self.add_category_button = CTkButton(self, text = "Manage transaction Categories", command = lambda: master.change_page(CategoryPage))
        self.add_category_button.place(relx = 0.01, rely = 0.95, anchor = "w")
        self.accounts_panel = CTkFrame(self)
        self.accounts_panel.pack(pady = (0, 10))
        for col, header in enumerate(["Name", "Account Type", "Balance"]):
            label = CTkLabel(self.accounts_panel, text = header).grid(row = 0, column = col, padx = 15, pady = 20)
        for row, (key, account) in enumerate(accounts.items(), start = 1):
            CTkLabel(self.accounts_panel, text = account.name).grid(row = row, column = 0, padx = 15, pady = 20)
            CTkLabel(self.accounts_panel, text = account.type).grid(row = row, column = 1, padx = 15, pady = 20)
            balance_value = account.balance
            balance_text = f"${balance_value:,.2f}"
            balance_color = "green" if balance_value >= 0 else "red"
            CTkLabel(self.accounts_panel, text = balance_text, text_color = balance_color).grid(row = row, column = 2, padx = 15, pady = 10)
        self.back_button = CTkButton(self, text = "Back", command = lambda: master.change_page(HomePage))
        self.back_button.place(relx = 0.01, rely = 0.05, anchor = "w")

class CreateAccountPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        self.main_label = CTkLabel(self, text = "New Account", font = ("times", 30, "bold"))
        self.main_label.place(relx = 0.5, rely = 0.05, anchor = "center")
        self.account_type_label = CTkLabel(self, text = "Type: ")
        self.account_type_label.place(relx = 0.4, rely = 0.1, anchor = "w")
        self.account_name_label = CTkLabel(self, text = "Name: ")
        self.account_name_label.place(relx = 0.4, rely = 0.15, anchor = "w")
        self.account_balance_label = CTkLabel(self, text = "Balance: ")
        self.account_balance_label.place(relx = 0.4, rely = 0.2, anchor = "w")
        self.account_type = CTkOptionMenu(self, values = ["Checking", "Savings", "Credit", "Investment", "Loan"], command = self.update_balance_prefix)
        self.account_type.place(relx = 0.4425, rely = 0.1, anchor = "w")
        self.account_type.set("")
        self.account_name = CTkEntry(self, placeholder_text = "Enter the name of the account", width = 300)
        self.account_name.place(relx = 0.5, rely = 0.15, anchor = "center")
        self.account_balance = CTkEntry(self, placeholder_text = "0.00", width = 300, validate = "key", validatecommand = (vcmd, "%P"))
        self.account_balance.place(relx = 0.5, rely = 0.2, anchor = "center")
        self.submit_button = CTkButton(self, text = "Submit", command = self.initialize_account)
        self.submit_button.place(relx = 0.56, rely = 0.25, anchor = "e")
        self.back_button = CTkButton(self, text = "Back", command = lambda: master.change_page(AccountsPage))
        self.back_button.place(relx = 0.01, rely = 0.05, anchor = "w")

    def update_balance_prefix(self, account_type):
        if hasattr(self, "balance_prefix"):
            self.balance_prefix.destroy()
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        prefix = "$" if account_type in ["Checking", "Savings", "Investment"] else "-$"
        color = "green" if prefix == "$" else "red"
        self.balance_prefix = CTkLabel(self, text = prefix, text_color = color)
        self.balance_prefix.place(relx = 0.425, rely = 0.2, anchor = "center")
        self.account_balance.destroy()
        self.account_balance = CTkEntry(self, placeholder_text = "0.00", width = 300, validate = "key", validatecommand = (vcmd, "%P"), text_color = color)
        self.account_balance.place(relx = 0.5, rely = 0.2, anchor = "center")

    def initialize_account(self):
        name = self.account_name.get()
        balance = float(self.account_balance.get())
        account_type = self.account_type.get()
        accounts[name] = Account(name, account_type, balance)
        save_accounts(accounts)
        self.notify = CTkLabel(self, text = "Updating accounts...", text_color = "green", font = ("times", 25, "bold"))
        self.notify.place(relx = 0.5, rely = 0.5)
        self.after(1000, lambda: self.master.change_page(CreateAccountPage))

class PostTransactionPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_label = CTkLabel(self, text = "New Transaction", font = ("times", 30, "bold"))
        self.main_label.place(relx = 0.3, rely = 0.05, anchor = "center")
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        self.transaction_type_label = CTkLabel(self, text = "Action: ")
        self.transaction_type_label.place(relx = 0.25, rely = 0.1, anchor = "center")
        self.account_label = CTkLabel(self, text = "Account: ")
        self.account_label.place(relx = 0.25, rely = 0.15, anchor = "center")
        self.category_label = CTkLabel(self, text = "Category: ")
        self.category_label.place(relx = 0.25, rely = 0.2, anchor = "center")
        self.date_label = CTkLabel(self, text = "Date: ")
        self.date_label.place(relx = 0.25, rely = 0.25, anchor = "center")
        self.transaction_amount_label = CTkLabel(self, text = "Amount: ")
        self.transaction_amount_label.place(relx = 0.25, rely = 0.3, anchor = "center")
        self.transaction_type = CTkOptionMenu(self, values = ["Deposit", "Withdraw"], command = self.update_amount_prefix)
        self.transaction_type.place(relx = 0.32, rely = 0.1, anchor = "center")
        self.transaction_type.set("")
        self.account = CTkOptionMenu(self, values = [account.name for account in accounts.values()])
        self.account.place(relx = 0.32, rely = 0.15, anchor = "center")
        self.account.set("")
        self.category = CTkOptionMenu(self, values = [category for category in categories])
        self.category.place(relx = 0.32, rely = 0.2, anchor = "center")
        self.category.set("")
        self.date_entry_var = tkinter.StringVar()
        self.date_entry = CTkEntry(self, textvariable = self.date_entry_var, width = 300)
        self.date_entry.place(relx = 0.35, rely = 0.25, anchor = "center")
        self.date_entry.bind("<Button-1>", self.open_calendar)
        self.transaction_amount = CTkEntry(self, placeholder_text = "Enter the transaction amount", width = 300, validate = "key", validatecommand = (vcmd, "%P"))
        self.transaction_amount.place(relx = 0.35, rely = 0.3, anchor = "center")
        self.transaction_amount.bind("<Return>", self.post_transaction)
        self.submit_button = CTkButton(self, text = "Submit", command = self.post_transaction)
        self.submit_button.place(relx = 0.375, rely = 0.325)
        self.back_button = CTkButton(self, text = "Back", command = lambda: master.change_page(AccountsPage))
        self.back_button.place(relx = 0.05, rely = 0.05, anchor = "center")

    def update_amount_prefix(self, transaction_type):
        if hasattr(self, "balance_prefix"):
            self.balance_prefix.destroy()
        vcmd = self.register(lambda val: val.replace(".", "", 1).isdigit() or val == "")
        prefix = "$" if transaction_type in ["Deposit"] else "-$"
        color = "green" if prefix == "$" else "red"
        self.amount_prefix = CTkLabel(self, text = prefix, text_color = color)
        self.amount_prefix.place(relx = 0.34, rely = 0.3, anchor = "center")
        self.transaction_amount.destroy()
        self.transaction_amount = CTkEntry(self, placeholder_text = "Enter the transaction amount", width = 300, validate = "key", validatecommand = (vcmd, "%P"), text_color = color)
        self.transaction_amount.place(relx = 0.35, rely = 0.3, anchor = "center")
        self.transaction_amount.bind("<Return>", self.post_transaction)

    def open_calendar(self, event):
        def select_date():
            selected = cal.selection_get()
            self.date_entry_var.set(selected.strftime("%Y-%m-%d"))
            top.destroy()
        top = tkinter.Toplevel(self)
        top.grab_set()
        top.geometry("+%d+%d" % (event.x_root, event.y_root))
        cal = Calendar(top, selectmode = 'day', date_pattern = 'yyyy-mm-dd')
        cal.pack()
        ok_button = tkinter.Button(top, text = "OK", command = select_date)
        ok_button.pack()

    def post_transaction(self, event = None):
        account = self.account.get()
        transaction_type = self.transaction_type.get()
        category = self.category.get()
        amount = float(self.transaction_amount.get())
        date = datetime.datetime.strptime(self.date_entry_var.get(), "%Y-%m-%d").date()
        beginning_amount = accounts[account].balance
        match transaction_type:
            case "Withdraw":
                accounts[account].balance -= amount
            case "Deposit":
                accounts[account].balance += amount
            case _:
                pass
        ending_amount = accounts[account].balance
        transaction = Transaction(category, transaction_type, amount, date, beginning_amount, ending_amount)
        accounts[account].transactions.append(transaction)
        save_accounts(accounts)
        self.notify = CTkLabel(self, text = "Updating accounts...", text_color = "green", font = ("times", 25, "bold"))
        self.notify.place(relx = 0.5, rely = 0.5)
        self.after(1000, lambda: self.master.change_page(PostTransactionPage))

class CategoryPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.categories_label = CTkLabel(self, text = "Categories", font = ("times", 30, "bold"))
        self.categories_label.pack(pady=(50, 10))
        self.categories_panel = CTkFrame(self)
        self.categories_panel.pack(pady=(0, 20))
        for row, category in enumerate(categories):
            label = CTkLabel(self.categories_panel, text = category)
            label.grid(row = row, column = 0, pady = 15, padx = 20)
        self.add_category_label = CTkLabel(self, text = "Use the box below to enter a new category:")
        self.add_category_label.place(relx = 0.2, rely = 0.225, anchor = "center")
        self.add_category_box = CTkEntry(self, placeholder_text = "Enter Category here:")
        self.add_category_box.place(relx = 0.2, rely = 0.25, anchor = "center")
        self.add_category_box.bind("<Return>", self.update)
        self.back_button = CTkButton(self, text = "Back", command = lambda: master.change_page(AccountsPage))
        self.back_button.place(relx = 0.05, rely = 0.05, anchor = "center")

    def update(self, event = None):
        categories.append(self.add_category_box.get())
        save_categories(categories)
        self.master.change_page(CategoryPage)

class SettingsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.theme_label = CTkLabel(self, text = "Theme", font = ("times", 30, "bold"))
        self.theme_label.place(relx = 0.5, rely = 0.15, anchor = "center")
        self.light_mode_button = CTkButton(self, text = "Light", command = lambda: set_appearance_mode("light"))
        self.light_mode_button.place(relx = 0.45, rely = 0.2, anchor = "center")
        self.dark_mode_button = CTkButton(self, text = "Dark", command = lambda: set_appearance_mode("dark"))
        self.dark_mode_button.place(relx = 0.45, rely = 0.25, anchor = "center")
        self.theme_select_box = CTkOptionMenu(self, values = ["Blue", "Green", "Dark-Blue"])
        self.theme_select_box.place(relx = 0.55, rely = 0.2, anchor = "center")
        self.apply_button = CTkButton(self, text = "Apply", command = lambda: self.change_theme(self.theme_select_box.get()))
        self.apply_button.place(relx = 0.75, rely = 0.75, anchor = "center")
        self.back_button = CTkButton(self, text = "Back", command = lambda: master.change_page(HomePage))
        self.back_button.place(relx = 0.05, rely = 0.05, anchor = "center")

    def change_theme(self, theme):
        self.confirm_box = CTkFrame(self)
        self.confirm_box.place(relx = 0.5, rely = 0.5, relwidth = 1.0, relheight = 1.0, anchor = "center")
        self.confirm_text = CTkLabel(self.confirm_box, text = "Updating the theme settings will require restarting the app.\nPress continue to close the app and then reopen it, or return to do this later.", font = ("times", 50, "bold"))
        self.confirm_text.place(relx = 0.5, rely = 0.2, anchor = "center")
        self.proceed_button = CTkButton(self.confirm_box, text = "Continue", command = lambda: self.save_theme_change(theme))
        self.proceed_button.place(relx = 0.25, rely = 0.75, anchor = "center")
        self.proceed_button = CTkButton(self.confirm_box, text = "Cancel", command = lambda: self.confirm_box.destroy())
        self.proceed_button.place(relx = 0.75, rely = 0.75, anchor = "center")

    def save_theme_change(self, theme):
        with open("custom_theme.cfg", "w") as f:
            f.write(theme)
        sys.exit()

class StatisticsPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.statistics_label = CTkLabel(self, text = "Statistics")
        self.statistics_label.place(relx = 0.5, rely = 0.23, anchor = "center")
        self.text = CTkLabel(self, text = "More coming soon!")
        self.text.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.back_button = CTkButton(self, text = "Back", command = lambda: master.change_page(HomePage))
        self.back_button.place(relx = 0.05, rely = 0.05, anchor = "center")

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
            self.login_page.pack(fill = "both", expand = True)
        else:
            self.password_setup_page = PasswordSetupPage(self)
            self.current_page = self.password_setup_page
            self.password_setup_page.pack(fill = "both", expand = True)



    def change_page(self, new_page):
        self.current_page.destroy()
        self.current_page = new_page(self)
        self.current_page.pack(fill = "both", expand = True)

    def show_login_page(self):
        self.current_page.pack_forget()
        self.current_page = self.login_page
        self.login_page.pass_input.delete(0, "end")
        self.login_page.error_label.configure(text = "")
        self.login_page.pack(fill = "both", expand = True)

    def on_exit(self):
        save_accounts(accounts)
        save_categories(categories)
        self.destroy()

if __name__ == "__main__":
    if os.path.isfile("custom_theme.cfg"):
        with open("custom_theme.cfg", "r") as f:
            theme = f.read().strip().lower()
            set_default_color_theme(theme)
    categories = load_categories()
    accounts = load_accounts()
    app = App()
    app.mainloop()