from abc import ABC, abstractmethod
from datetime import datetime

# 1. Abstract Base Class (Abstraction)
class Account(ABC):
    def __init__(self, account_number, holder_name, initial_balance=0.0):
        self._account_number = account_number  # Protected attribute (Encapsulation)
        self._holder_name = holder_name
        self._balance = float(initial_balance)
        self._transaction_history = []
        self._log_transaction("Account Created", initial_balance)

    def _log_transaction(self, trans_type, amount):
        """Helper method to record transaction history with timestamps."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transaction_history.append({
            "time": timestamp,
            "type": trans_type,
            "amount": amount,
            "balance": self._balance
        })

    def deposit(self, amount):
        """Deposit funds into the account."""
        if amount <= 0:
            print("Error: Deposit amount must be greater than zero.")
            return False
        self._balance += amount
        self._log_transaction("Deposit", amount)
        print(f"Success: Deposited ${amount:.2f}. New Balance: ${self._balance:.2f}")
        return True

    @abstractmethod
    def withdraw(self, amount):
        """Abstract method for withdrawal to be implemented by child classes (Polymorphism)."""
        pass

    def get_balance(self):
        return self._balance

    def show_statement(self):
        """Display transaction history."""
        print(f"\n--- Statement for Account #{self._account_number} ({self._holder_name}) ---")
        for tx in self._transaction_history:
            print(f"[{tx['time']}] {tx['type']}: ${tx['amount']:.2f} | Balance: ${tx['balance']:.2f}")
        print(f"Current Balance: ${self._balance:.2f}\n")


# 2. Inheritance: Savings Account
class SavingsAccount(Account):
    MIN_BALANCE = 500.0  # Minimum balance requirement

    def withdraw(self, amount):
        """Polymorphic implementation of withdraw with savings rules."""
        if amount <= 0:
            print("Error: Withdrawal amount must be greater than zero.")
            return False
        if self._balance - amount < self.MIN_BALANCE:
            print(f"Error: Withdrawal denied! Savings account must maintain a minimum balance of ${self.MIN_BALANCE:.2f}.")
            return False
        
        self._balance -= amount
        self._log_transaction("Withdrawal", amount)
        print(f"Success: Withdrew ${amount:.2f}. New Balance: ${self._balance:.2f}")
        return True


# 3. Inheritance: Current/Checking Account
class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 1000.0

    def withdraw(self, amount):
        """Polymorphic implementation of withdraw allowing overdraft."""
        if amount <= 0:
            print("Error: Withdrawal amount must be greater than zero.")
            return False
        if self._balance - amount < -self.OVERDRAFT_LIMIT:
            print(f"Error: Overdraft limit exceeded! Max overdraft is ${self.OVERDRAFT_LIMIT:.2f}.")
            return False
        
        self._balance -= amount
        self._log_transaction("Withdrawal", amount)
        print(f"Success: Withdrew ${amount:.2f}. New Balance: ${self._balance:.2f}")
        return True


# 4. Banking System Application CLI
def main():
    accounts = {}

    while True:
        print("\n=== Object-Oriented Python Banking System ===")
        print("1. Create Savings Account")
        print("2. Create Current Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. View Balance & Statement")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            acc_no = input("Enter Account Number: ").strip()
            name = input("Enter Holder Name: ").strip()
            try:
                bal = float(input("Enter Initial Deposit (Min $500): "))
                if bal < 500:
                    print("Initial deposit must be at least $500 for a Savings Account.")
                    continue
                accounts[acc_no] = SavingsAccount(acc_no, name, bal)
                print(f"Savings Account #{acc_no} created successfully!")
            except ValueError:
                print("Invalid input format.")

        elif choice == "2":
            acc_no = input("Enter Account Number: ").strip()
            name = input("Enter Holder Name: ").strip()
            try:
                bal = float(input("Enter Initial Deposit: "))
                accounts[acc_no] = CurrentAccount(acc_no, name, bal)
                print(f"Current Account #{acc_no} created successfully!")
            except ValueError:
                print("Invalid input format.")

        elif choice == "3":
            acc_no = input("Enter Account Number: ").strip()
            if acc_no in accounts:
                try:
                    amt = float(input("Enter amount to deposit: "))
                    accounts[acc_no].deposit(amt)
                except ValueError:
                    print("Invalid amount.")
            else:
                print("Account not found.")

        elif choice == "4":
            acc_no = input("Enter Account Number: ").strip()
            if acc_no in accounts:
                try:
                    amt = float(input("Enter amount to withdraw: "))
                    accounts[acc_no].withdraw(amt)
                except ValueError:
                    print("Invalid amount.")
            else:
                print("Account not found.")

        elif choice == "5":
            acc_no = input("Enter Account Number: ").strip()
            if acc_no in accounts:
                accounts[acc_no].show_statement()
            else:
                print("Account not found.")

        elif choice == "6":
            print("Exiting application. Thank you!")
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")

if __name__ == "__main__":
    main()
