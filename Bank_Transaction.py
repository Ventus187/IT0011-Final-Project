import datetime
class Bank_Transaction:
    def __init__(self, amount, transaction_type, balance):
        self.amount = amount
        self.transaction_type = transaction_type
        self.balance = balance
        self.date = datetime.datetime.now().strftime("%x")