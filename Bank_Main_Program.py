import tkinter as tk # imports the Tk GUI toolkit for the python program
from tkinter import messagebox # enables message boxes in the program
import mysql.connector # will enable Python to access MySQL databases
from tabulate import tabulate # will make the list turn into a formatted table
from datetime import datetime # enables date and time for the transactions 
from Bank_Functions import Bank_Functions # imports the Bank_Functions module into Bank_Main.py

class Bank_Account_GUI:
    def __init__(self, master): # master is the main program so that is when changing format it only affects the master parameter not the other parameters
        self.master = master
        master.title("Bank Account Management")
        master.geometry("1600x900") 

        # connects to MySQL database
        self.connect_to_database()

        # instantiates of Bank_Functions
        self.bank_functions = Bank_Functions(
            host="127.0.0.1",
            user="Seoul",
            password="202011279",
            database="FinalProjDB"
        )

        # GUI components 
        font = ("Arial", 16)

        # account number entry box
        self.label_account_number = tk.Label(master, text="Account Number:", font=font)
        self.entry_account_number = tk.Entry(master, font=font)
        # account name entry box
        self.label_account_name = tk.Label(master, text="Account Name:", font=font)
        self.entry_account_name = tk.Entry(master, font=font)
        # amount entry box 
        self.label_amount = tk.Label(master, text="Amount:", font=font)
        self.entry_amount = tk.Entry(master, font=font)
        # deposit button
        self.button_deposit = tk.Button(master, text="Deposit", command=self.deposit, font=font)
        # withdraw button
        self.button_withdraw = tk.Button(master, text="Withdraw", command=self.withdraw, font=font)
        # balance message
        self.button_balance = tk.Button(master, text="Display Balance", command=self.display_balance, font=font)
        self.label_balance = tk.Label(master, text="", font=font)
        # display transaction button
        self.button_transactions = tk.Button(master, text="Display Transactions", command=self.display_transactions, font=font)
        # create account button
        self.button_create_account = tk.Button(master, text="Create Account", command=self.create_account, font=font)

        # .pack organizes the layout of the program, anchor is what alignment, padx and pady is the spacing between the GUI components
        # account number entry box
        self.label_account_number.pack(anchor="center", padx=10, pady=10)
        self.entry_account_number.pack(anchor="center", padx=10, pady=10)
        # account name entry box 
        self.label_account_name.pack(anchor="center", padx=10, pady=10)
        self.entry_account_name.pack(anchor="center", padx=10, pady=10)
        # amount entry box 
        self.label_amount.pack(anchor="center", padx=10, pady=10)
        self.entry_amount.pack(anchor="center", padx=10, pady=10)
        # deposit button
        self.button_deposit.pack(anchor="center", padx=10, pady=10)
        # withdraw button
        self.button_withdraw.pack(anchor="center", padx=10, pady=10)
        # balance message
        self.button_balance.pack(anchor="center", padx=10, pady=10)
        self.label_balance.pack(anchor="center", padx=10, pady=10) 
        # display transaction button
        self.button_transactions.pack(anchor="center", padx=10, pady=10)
        # create accoutn button
        self.button_create_account.pack(anchor="center", padx=10, pady=10)

    def connect_to_database(self):
        try:
            self.mydb = mysql.connector.connect( # connects to the MySQL database
                host="Mykul",
                user="Seoul",
                password="202011279",
                database="FinalProjDB"
            )
            self.cursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Could not connect to database: {err}")
            self.master.destroy()

    def disconnect_from_database(self):
        if hasattr(self, 'mydb') and self.mydb.is_connected(): # checks if the self 'mydb' has all the attributes and if its connected and if its true the cursor and database connection closes
            self.cursor.close()
            self.mydb.close()

    def deposit(self):
        account_number = self.entry_account_number.get() # gets the account number inputed
        amount = float(self.entry_amount.get()) # gets the account name inputed
        try:
            account_name = self.entry_account_name.get()  # get account name
            if self.bank_functions.account_exists(account_number, account_name):  # pass both account number and name
                self.bank_functions.deposit(account_number, amount) # adds the amount inputted into the account that is connected the database 
                messagebox.showinfo("Success", "Amount deposited successfully")
            else:
                messagebox.showerror("Error", "Account does not exist")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def withdraw(self):
        try:
            account_number = self.entry_account_number.get() # gets the account number inputed
            account_name = self.entry_account_name.get()  # gets the account name inputed
            amount = float(self.entry_amount.get()) # converts the the amount as float
            
            if self.bank_functions.account_exists(account_number, account_name):
                self.bank_functions.withdraw(account_number, account_name, amount)  # pass account_number, name and amount 
                messagebox.showinfo("Success", "Amount withdrawn successfully")
            else:
                messagebox.showerror("Error", "Account does not exist")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
        except mysql.connector.Error as e:
            print("Error:", e)
        
    def display_balance(self):
        account_number = self.entry_account_number.get() # gets the account number inputed
        account_name = self.entry_account_name.get()  # gets the account name inputed
        if self.bank_functions.account_exists(account_number, account_name):  # pass both account_number and account_name
            balance = self.bank_functions.get_balance(account_number)  # call the method to retrieve the balance from Bank_Functions
            if balance is not None:
                self.label_balance.config(text=f"Balance: {balance}")  # updates the label with the retrieved balance
            else:
                messagebox.showerror("Error", "Failed to retrieve balance")
        else:
            messagebox.showerror("Error", "Account does not exist")

    def display_transactions(self):
        account_number = self.entry_account_number.get() # gets the account number inputed
        account_name = self.entry_account_name.get()  # gets the account name inputed
        if self.bank_functions.account_exists(account_number, account_name):
            transactions = self.bank_functions.display_transactions(account_number)  # call display_transactions directly from Bank_Functions
            if transactions:
                # formats the transactions to be displayed
                formatted_transactions = "Transactions:\n\n" + transactions
                
                # creates a transaction window pop up message
                transactions_window = tk.Toplevel(self.master)
                transactions_window.title("Transactions")
                transactions_window.geometry("800x600")  # resolution window of the displayed transaction
                
                # display transactions in a label
                label_transactions = tk.Label(transactions_window, text=formatted_transactions, font=("Arial", 12))
                label_transactions.pack(padx=20, pady=20)
            else:
                messagebox.showinfo("Info", "No transactions available for this account.")
        else:
            messagebox.showerror("Error", "Account does not exist.")

    def create_account(self):
        account_number = self.entry_account_number.get()
        account_name = self.entry_account_name.get()
        try:
            self.bank_functions.create_account(account_number, account_name)
            messagebox.showinfo("Success", "Account created successfully")
        except Bank_Functions().AccountAlreadyExistsError:
            messagebox.showerror("Error", "An account with this account number already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not create account: {e}")

    def record_transaction(self, account_number, amount, transaction_type):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO transactions (account_number, amount, transaction_type, timestamp) VALUES (%s, %s, %s, %s)",
                                (account_number, amount, transaction_type, timestamp))
            self.mydb.commit()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to record transaction: {error}")
            

if __name__ == "__main__": # conditional statement that runs the main python program
    root = tk.Tk() # initializes the tk application window
    app = Bank_Account_GUI(root) # root is the main window of the application from the tk module
    root.mainloop() # starts the Tkinter event loop
    app.disconnect_from_database() # disconnects the python program from the MySQL database
