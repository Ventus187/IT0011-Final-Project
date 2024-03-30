import mysql.connector # will enable Python to access MySQL databases
from Bank_Functions import Bank_Functions # imports the Bank_Functions module into Bank_account.py
from datetime import datetime # enables date and time for the transactions 

class Bank_Account: 
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect( # connects to the database
            host="127.0.0.1",
            user="Seoul",
            password="202011279",
            database="FinalProjDB"
        )
        self.cursor = self.connection.cursor()
        self.bank_functions = Bank_Functions(host, user, password, database)  # instantiates Bank_Functions

    def create_account(self, account_number, account_name):
        try:
            self.bank_functions.create_account(account_number, account_name)  # calls create_account from Bank_Functions
            print("Account created successfully")
        except mysql.connector.Error as e:
            print("Error creating account:", e)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def deposit(self, account_number, amount):
        try:
            self.bank_functions.deposit(account_number, amount)  # call deposit from Bank_Functions
            self.record_transaction(account_number, amount, "Deposit")
            print("Amount deposited successfully")
        except ValueError:
            print("Invalid amount")

    def withdraw(self, account_number, amount):
        try:
            self.bank_functions.withdraw(account_number, amount)  # call withdraw from Bank_Functions
            self.record_transaction(account_number, amount, "Withdrawal")
            print("Amount withdrawn successfully")
        except ValueError:
            print("Invalid amount")

    def display_balance(self, account_number):
        try:
            self.bank_functions.display_balance(account_number)  # call display_balance from Bank_Functions
        except mysql.connector.Error as e:
            print("Error displaying balance:", e)

    def display_transactions(self, account_number):
        try:
            self.bank_functions.display_transactions(account_number)  # call display_transactions from Bank_Functions
        except mysql.connector.Error as e:
            print("Error displaying transactions:", e)
    
    def record_transaction(self, account_number, amount, transaction_type):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO transactions (account_number, amount, transaction_type, timestamp) VALUES (%s, %s, %s, %s)",
                                (account_number, amount, transaction_type, timestamp))
            self.connection.commit()
        except mysql.connector.Error as e:
            print("Error recording transaction:", e)
