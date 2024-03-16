import tabulate #pip install tabulate sa cmd para ma run
import Bank_Transaction

class Bank_Functions:
    def __init__(self, account_number, account_name, balance = 0):
        self.acount_number = account_number
        self.account_name = account_name
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Bank_Transaction(amount, "Deposit", self.balance))
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(Bank_Transaction(amount, "Withdraw", self.balance))
    
    def display_balance(self):
        # print(f"Account Number: {self.account_number}")
        # print(f"Account Name: {self.account_name}")
        # print(f"Balance: {self.balance}")
        data_bal = [[self.account_number, self.account_name, self.balance]]
        col_names = ["Account Number", "Account Name", "Balance"]
        print(tabulate.tabulate(data_bal,headers= col_names, tablefmt="fancy_grid", showindex="always"))
    
    def display_transactions(self):
        # for transaction in self.transactions:
        #     print(f"Date: {transaction.date}")
        #     print(f"Amount: {transaction.amount}")
        #     print(f"Type: {transaction.transaction_type}")
        #     print(f"Balance: {transaction.balance}")
        #     print()
        data_trans = [[transaction.date, transaction.amount, transaction.transaction_type, transaction.balance] 
                for transaction in self.transactions]
        col_names = ["Date", "Amount", "Type", "Balance"]
        
        print(tabulate.tabulate(data_trans,headers= col_names, tablefmt="fancy_grid", showindex="always"))