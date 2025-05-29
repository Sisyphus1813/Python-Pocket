# Python Pocket

**Python Pocket** is a secure, lightweight, and extensible personal finance tracker built with `customtkinter`. It provides local encrypted storage, account management, transaction logging, and theming—all behind a password-protected interface.

Note: This project is actively in development. Expect incomplete features and rough edges.

---

## Features

- Encrypted local storage using `cryptography.Fernet`
- Password protection (hashed with `bcrypt`)
- Account management with support for:
  - Checking
  - Savings
  - Credit
  - Investment
  - Loans
- Transaction tracking (Deposits, Withdrawals)
- Category tagging for transactions
- Basic statistics page (placeholder for future analytics)
- Theme switching (light/dark, color accents)

---

## Setup

### Requirements

- Python 3.10 or higher
- Windows (tested on tkinter for Windows)
- Required packages:

```bash
pip install customtkinter tkcalendar cryptography bcrypt
