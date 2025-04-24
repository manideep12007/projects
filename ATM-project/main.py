from models import User, Account
import getpass

class ATM:
    def main_menu(self):
        while True:
            print("\n🏦 Welcome to Python Bank ATM")
            print("1 Login")
            print("2 Register")
            print("3 Forgot PIN")
            print("4 Exit")
            choice = input("Choose option: ")

            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                self.forgot_pin()
            elif choice == '4':
                print("👋 Thank you for using our ATM. Goodbye!")
                break
            else:
                print("❌ Invalid option.")

    def register(self):
        username = input("👤 Enter your username: ")
        email = input("📧 Enter your email (for recovery): ")
        pin = getpass.getpass("🔐 Set a 4-digit PIN: ")
        if len(pin) != 4 or not pin.isdigit():
            print("❌ PIN must be exactly 4 digits.")
            return
        User.register(username=username, email=email, pin=pin)

    def login(self):
        username = input("👤 Username: ")
        pin = getpass.getpass("🔑 PIN: ")
        user = User(username=username, pin=pin)
        auth = user.authenticate()
        if auth:
            print(f"✅ Login successful! Welcome, {username}")
            self.account_menu(auth[0])
        else:
            print("❌ Invalid credentials.")

    def forgot_pin(self):
        email = input("📧 Enter your registered email: ")
        User.reset_pin(email=email)

    def account_menu(self, user_id):
        account = Account(user_id=user_id)
        while True:
            print("\n🔐 Account Menu")
            print("1 Check Balance")
            print("2 Deposit")
            print("3 Withdraw")
            print("4 User Information")
            print("5 Logout")
            choice = input("Choose option: ")

            if choice not in ['1', '2', '3', '4', '5']:
                print("❌ Invalid option.")
                continue

            if choice == '1':
                print(f"💰 Current Balance: ${account.get_balance():.2f}")
            elif choice == '2':
                try:
                    amount = float(input("💵 Enter deposit amount: "))
                    account.deposit(amount=amount)
                except ValueError:
                    print("❌ Invalid amount.")
            elif choice == '3':
                try:
                    amount = float(input("💸 Enter withdrawal amount: "))
                    account.withdraw(amount=amount)
                except ValueError:
                    print("❌ Invalid amount.")
            elif choice == '4':
                account.get_info()
            elif choice == '5':
                print("🔒 Logged out successfully.")
                break

if __name__ == "__main__":
    atm = ATM()
    atm.main_menu()
