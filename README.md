# Python Pocket

**Python Pocket** is a secure, lightweight, and extensible personal finance tracker built with `customtkinter`. It provides local encrypted storage, account management, transaction logging, and theming—all behind a password-protected interface.

## Features

### Security
- Password protection with bcrypt hashing
- Local encrypted storage using Fernet symmetric encryption
- Secure session management

### Account Management
- Multiple account types supported:
  - Checking accounts
  - Savings accounts
  - Credit accounts (with credit limits and due dates)
  - Investment accounts
  - Loan accounts (with due dates)
- Real-time balance tracking
- Transaction history per account

### Transaction Management
- Record deposits and withdrawals
- Categorize transactions
- Custom category management
- Transaction editing and deletion
- Date-based transaction tracking

### User Interface
- Modern UI using customtkinter
- Theme customization:
  - Light/Dark mode
  - Multiple accent colors (Blue, Green, Dark-Blue)
  - Customizable fonts
- Responsive design
- Intuitive navigation

### Analytics
- Visual statistics with matplotlib integration
- Expense tracking by category
- Income analysis
- Multiple chart types:
  - Pie charts
  - Bar graphs

## Setup

### Requirements
- Python 3.10 or higher
- Windows OS (tested on Windows 10/11)
- Required packages:
```bash
pip install customtkinter tkcalendar cryptography bcrypt matplotlib
```

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Sisyphus1813/Python-Pocket.git
cd Python-Pocket
```

2. Install dependencies:
```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install project dependencies from uv.lock and pyproject.toml
uv install --system
```

3. Run the application:
```bash
python main.py
```

## Usage

### First Time Setup
1. Launch the application
2. Set up your password when prompted
3. Create your first account

### Managing Accounts
- Create new accounts from the Accounts page
- View account details including balance and transaction history
- Edit or delete transactions as needed

### Recording Transactions
1. Navigate to the Accounts page
2. Click "Post a new Transaction"
3. Select the account, transaction type, category, and amount
4. Choose the transaction date using the calendar widget

### Customizing Categories
1. Go to the Accounts page
2. Click "Manage transaction Categories"
3. Add new categories as needed

### Viewing Statistics
1. Navigate to the Statistics page
2. Choose between Income and Expenses views
3. Toggle between Pie Chart and Graph Chart visualizations

### Customizing Appearance
1. Go to Settings
2. Choose your preferred:
   - Theme (Light/Dark)
   - Accent color
   - Font style

## Security Notes
- All data is stored locally and encrypted
- Password is hashed using bcrypt
- No data is sent to external servers

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
