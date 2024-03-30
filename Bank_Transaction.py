import mysql.connector # will enable Python to access MySQL databases
import datetime # enables date and time for the transactions 

class Bank_Transaction:
    def __init__(self, amount, transaction_type, balance):
        self.amount = amount
        self.transaction_type = transaction_type
        self.balance = balance
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # %Y-%m-d is year-month-day while %H:%M:%S is hour:minute:seconds

    def record_transaction_to_db(self, account_number, cursor, mydb):
        try:
            self._record_transaction_to_db(account_number, cursor, mydb)
            print("Transaction recorded successfully!")
        except mysql.connector.Error as err: # catches any exception that occurs during the operation and gives out a message 
            print("Error:", err)

    def _record_transaction_to_db(self, account_number, cursor, mydb):
        sql = "INSERT INTO transactions (account_number, amount, transaction_type, balance, date) VALUES (%s, %s, %s, %s, %s)" # %s is just adds the text that is in the parenthesis
        values = (account_number, self.amount, self.transaction_type, self.balance, self.date)
        cursor.execute(sql, values)
        mydb.commit()
