from Bank_Account import Bank_Account
from Bank_Functions import Bank_Functions
from Bank_Transaction import Bank_Transaction

def main():
    filname = "accounts.json"
    bank = Bank_Account(filname)
    
    print("Welcome to the Bank")
    while True:
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Display Balance")
        print("5. Display Transactions")
        print("6. Exit")
        
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            account_number = input("Enter account number: ")
            account_name = input("Enter account name: ")
            if bank.create_account(account_number, account_name, Bank_Functions):
                print("Account created")
            else:
                print("Account already exists")
        elif choice == 2:
            account_number = input("Enter account number: ")
            amount = float(input("Enter amount to deposit: "))
            if account_number in bank.accounts:
                bank.accounts[account_number].deposit(amount)
                bank.save_account()
                print("Amount deposited")
            else:
                print("Account does not exist")
        elif choice == 3:
            account_number = input("Enter account number: ")
            amount = float(input("Enter amount to withdraw: "))
            if account_number in bank.accounts:
                bank.accounts[account_number].withdraw(amount)
                bank.save_account()
                print("Amount withdrawn")
            else:
                print("Account does not exist")
        elif choice == 4:
            account_number = input("Enter account number: ")
            if account_number in bank.accounts:
                bank.accounts[account_number].display_balance()
            else:
                print("Account does not exist")
        elif choice == 5:
            account_number = input("Enter account number: ")
            if account_number in bank.accounts:
                bank.accounts[account_number].display_transactions()
            else:
                print("Account does not exist")
        elif choice == 6:
            break
        else:
            print("Invalid choice")
            
    return()
    
main()
