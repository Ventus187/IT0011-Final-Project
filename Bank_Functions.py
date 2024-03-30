import mysql.connector # will enable Python to access MySQL databases
from tabulate import tabulate  # will make the list turn into a formatted table
from datetime import datetime  # enables date and time for the transactions 
from decimal import Decimal # provides support for decimal point since the SQL table for transacitons are made as decimal

class Bank_Functions:
    class AccountAlreadyExistsError(Exception): # this is only use if the account already exists so nothing happens to the account 
        """Exception raised when attempting to create an account that already exists."""
        pass

    def __init__(self, host, user, password, database): # connects to the MySQL database
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="Seoul",
            password="202011279",
            database="FinalProjDB"
        )
        self.cursor = self.mydb.cursor()
        self.create_tables()

    def create_tables(self): 
        # Create accounts table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INT PRIMARY KEY,
                account_name VARCHAR(255),
                balance DECIMAL(10, 2)
            )
        """)

        # Create transactions table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                account_number INT,
                amount DECIMAL(10, 2),
                transaction_type ENUM('Deposit', 'Withdrawal'),
                timestamp DATETIME,
                balance DECIMAL(10, 2),
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        """)
        self.mydb.commit()

    def deposit(self, account_number, amount): 
        try:
            # Update balance in accounts table
            self.cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
            self.mydb.commit()

            # Get the updated balance
            self.cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
            updated_balance = self.cursor.fetchone()[0]

            # Record transaction in transactions table
            self.record_transaction(account_number, amount, "Deposit", updated_balance)
            print("Amount deposited successfully")
        except mysql.connector.Error as e:
            print("Error:", e)

    def withdraw(self, account_number, account_name, amount):
        try:
            # Check if account has sufficient balance
            self.cursor.execute("SELECT balance FROM accounts WHERE account_number = %s AND account_name = %s", (account_number, account_name))
            balance = self.cursor.fetchone()[0]
            if balance < amount:
                print("Insufficient balance")
                return
            
            # Convert amount to Decimal
            amount = Decimal(str(amount))

            # Calculate updated balance after withdrawal
            updated_balance = balance - amount

            # Update balance in accounts table
            self.cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (updated_balance, account_number))
            self.mydb.commit()

            # Record transaction in transactions table
            self.record_transaction(account_number, amount, "Withdrawal", updated_balance)
            print("Amount withdrawn successfully")
        except mysql.connector.Error as e:
            print("Error:", e)
        
    def get_balance(self, account_number): 
        try:
            self.cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
            result = self.cursor.fetchone() # gets the balance from the database based on the account number that is used 
            if result:
                return result[0]
            else:
                return None  # Return None if account not found
        except mysql.connector.Error as e:
            print("Error:", e)
            return None  # Return None in case of an error
        
    def display_balance(self, account_number):
        try:
            # Fetch and display balance from accounts table
            self.cursor.execute("SELECT account_number, account_name, balance FROM accounts WHERE account_number = %s", (account_number,))
            result = self.cursor.fetchone() # displays the balance that came from the database based on the account number that is used 
            if result:
                data_bal = [[result[0], result[1], result[2]]]
                col_names = ["Account Number", "Account Name", "Balance"]
                print(tabulate(data_bal, headers=col_names, tablefmt="fancy_grid", showindex="always"))
            else:
                print("Account not found")
        except mysql.connector.Error as e:
            print("Error:", e)
        
    def display_transactions(self, account_number): 
        try:
            # Fetch and display transactions from transactions table
            self.cursor.execute("SELECT * FROM transactions WHERE account_number = %s", (account_number,))
            transactions = self.cursor.fetchall()

            data_trans = []
            for transaction in transactions:
                data_trans.append([transaction[1], transaction[2], transaction[3], transaction[4]])

            col_names = ["Date", "Amount", "Type", "Balance"]
            return tabulate(data_trans, headers=col_names, tablefmt="fancy_grid", showindex="always")
        except mysql.connector.Error as e:
            print("Error:", e)
            return None

    def record_transaction(self, account_number, amount, transaction_type, balance): # saves transaction records that are made during the program is running using datetime 
        try: 
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO transactions (account_number, amount, transaction_type, timestamp, balance) VALUES (%s, %s, %s, %s, %s)", 
                                (account_number, amount, transaction_type, timestamp, balance))
            self.mydb.commit()
        except mysql.connector.Error as e:
            print("Error:", e)

    def create_account(self, account_number, account_name): # creates an account number and account name to be save to the table in the database
        try:
            # Check if account already exists
            self.cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
            if self.cursor.fetchone():
                raise self.AccountAlreadyExistsError("An account with this account number already exists")

            # Create new account
            self.cursor.execute("INSERT INTO accounts (account_number, account_name, balance) VALUES (%s, %s, 0)", (account_number, account_name))
            self.mydb.commit()
            print("Account created successfully")
        except mysql.connector.Error as e:
            print("Error:", e)
        except self.AccountAlreadyExistsError as e:
            print("Error:", e)
            
    def account_exists(self, account_number, account_name): # checks the database if there is an existing account name and number
        try:
            self.cursor.execute("SELECT * FROM accounts WHERE account_number = %s AND account_name = %s", (account_number, account_name))
            return bool(self.cursor.fetchone())
        except mysql.connector.Error as e:
            print("Error:", e)
            return False
        
    def close_connection(self): # closes connection from the MySQL Database
        self.cursor.close()
        self.mydb.close()

#self.cursor is used to communicate with the database and execute the statement that is made
