import json
from Bank_Functions import Bank_Functions

class Bank_Account:
    def __init__(self, filename):
        self.filename = filename
        self.accounts = self.load_account()
    
    def load_account(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def create_account(self, account_number, account_name, Account):
        if account_number not in self.accounts:
            self.accounts[account_number] = Account(account_number, account_name)
            self.save_account()
            return True
        else:
            print("Account already exists")