# ATM Program 

class ATM:

    def __init__(self):
        # initialize users,their PINS,balances and security questions/answers
        self.users = ['user1','user2']
        self.pins = ['1234','0000']
        self.balances = [0,0]
        self.security_questions = [
            'What is your favorite number?',
            'What is your favorite color?',
        ]
        self.security_answers = ['21','white']
        self.current_user = None

    def create_new_account(self):
        # creating new account 
        print("<>"*20)
        username = input("Enter new username: ").lower()
        if username in self.users:
            print("<>" * 20)
            print("USERNAME ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT USERNAME.")
            print("<>" * 20)
            return
        pin = input("Enter a new 4-digit PIN: ")
        if not (pin.isdigit() and len(pin) == 4):
            print("<>" * 20)
            print("PIN MUST BE A 4-DIGIT NUMBER.")
            print("<>" * 20)
            return
        try:
            initial_balance = float(input("Enter initial balance: "))
            if initial_balance < 0 :
                raise ValueError("Balance cannot be negative")
        except ValueError as e :
            print("<>" * 20)
            print(f"INVALID INPUT: {e}")
            print("<>" * 20)
            return 
        security_question = input("choose a security question (e.g.,What is your favorite color ?): ")
        security_answer = input("Enter the answer to your security question validation: ").lower()
        self.users.append(username)
        self.pins.append(pin)
        self.balances.append(initial_balance)
        self.security_questions.append(security_question)
        self.security_answers.append(security_answer)

        print("<>" * 20)
        print("ACCOUNT CREATED SUCCESSFULLY")
        print("<>" * 20)
    
    def authenticate_user(self):
        # authenticate the user by verifying their username and PIN
        print("<>" * 20)
        while True:
            username = input("Enter your username: ").lower()
            if username in self.users:
                self.current_user = self.users.index(username)
                break
            else:
                print("<>" * 20)
                print("INVALID USERNAME. PLEASE TRY AGAIN.")
                print("<>" * 20)
        attempts = 3 
        while attempts > 0 :
            pin = input("Enter your pin number(or type 'FORGET' to reset your pin): ")
            if pin.upper() == 'FORGET':
                self.forget_pin()
                return False
            elif pin == self.pins[self.current_user]:
                print("<>" * 20)
                print("LOGIN SUCCESSFUL. WELCOME!")
                print("<>" * 20)
                return True
            else:
                attempts -= 1
                print("<>" * 20)
                print(f"INVALID PIN. {attempts} ATTEMPTS REMAINING.")
                print("<>" * 20)
            print("<>" * 20)
            print("TOO MANY FAILED ATTEMPTS.\nYOUR ACCOUNT HAS BEEN LOCKED.")
            print("<>" * 20)
            return False
    
    def forget_pin(self):
        # reset the pin number if user forgets the pin 
        print("<>" * 20)
        print("FORGET PIN")
        print("<>" * 20)
        print(f"security question: {self.security_questions[self.current_user]}")
        answer = input("Enter your answer: ").lower()
        if answer == self.security_answers[self.current_user]:
            new_pin = input("ENTER A NEW 4 DIGIT PIN: ")
            if not (new_pin.isdigit() and len(new_pin) == 4):
                print("<>" * 20)
                print("PIN MUST BE A 4-DIGIT NUMBER.")
                print("<>" * 20)
                return
            confirm_pin = input("confirm your new pin: ")
            if new_pin == confirm_pin:
                self.pins[self.current_user] = new_pin
                print("<>" * 20)
                print("PIN RESET SUCCESSFULLY. PLEASE LOGIN WITH YOUR NEW PIN")
                print("<>" * 20)
            else:
                print("<>" * 20)
                print("PINS MISMATCH. PLEASE TRY AGAIN")
                print("<>" * 20)
        else:
            print("<>" * 20)
            print("INCORRECT ANSWER. PIN RESET FAILED")
            print("<>" * 20)

    def show_menu(self):
        # Display the ATM menu and handle user choices
        while True:
            print("\n" + "<>" * 20)
            print("ATM SYSTEM")
            print("<>" * 20)
            print("1. Check Balance (C)")
            print("2. Withdraw Money (W)")
            print("3. Deposit Money (D)")
            print("4. Change PIN (P)")
            print("5. Quit (Q)")
            choice = input("SELECT AN OPTION: ").upper()

            if choice == 'C':
                self.check_balance()
            elif choice == 'W':
                self.withdraw_money()
            elif choice == 'D':
                self.deposit_money()
            elif choice == 'P':
                self.change_pin()
            elif choice == 'Q':
                print("<>" * 20)
                print("THANK YOU FOR USING THE ATM. GOODBYE!")
                print("<>" * 20)
                break
            else:
                print("<>" * 20)
                print("INVALID SELECTION. PLEASE TRY AGAIN.")
                print("<>" * 20)    
    
    def check_balance(self):
        # Display the current balance of the user
        print("<>" * 20)
        print(f"YOUR CURRENT BALANCE: {self.balances[self.current_user]:.2f}")
        print("<>" * 20)
    
    def withdraw_money(self):
        # Withdraw money from the user's account
        try:
            amount = float(input("ENTER AMOUNT TO WITHDRAW: "))
            if amount <= 0:
                print("<>" * 20)
                print("AMOUNT MUST BE GREATER THAN ZERO.")
                print("<>" * 20)
                return
            if amount > self.balances[self.current_user]:
                print("<>" * 20)
                print("INSUFFICIENT BALANCE.")
                print("<>" * 20)
            else:
                self.balances[self.current_user] -= amount
                print("<>" * 20)
                print(f"WITHDRAWAL SUCCESSFUL. NEW BALANCE: {self.balances[self.current_user]:.2f}")
                print("<>" * 20)
        except ValueError:
            print("=" * 40)
            print("INVALID INPUT. PLEASE ENTER A VALID AMOUNT.")
            print("=" * 40)

    def deposit_money(self):
        # Deposit money into the user's account
        try:
            amount = float(input("ENTER AMOUNT TO DEPOSIT: "))
            if amount <= 0:
                print("<>" * 20)
                print("AMOUNT MUST BE GREATER THAN ZERO.")
                print("<>" * 20)
                return
            self.balances[self.current_user] += amount
            print("<>" * 20)
            print(f"DEPOSIT SUCCESSFUL. NEW BALANCE: {self.balances[self.current_user]:.2f}")
            print("<>" * 20)
        except ValueError:
            print("<>" * 20)
            print("INVALID INPUT. PLEASE ENTER A VALID AMOUNT.")
            print("<>" * 20)

    def change_pin(self):
        # change the user pin 
        new_pin = input("ENTER A NEW 4 DIGIT PIN: ")
        if not (new_pin.isdigit() and len(new_pin) == 4):
            print("<>" * 20)
            print("PIN MUST BE A 4 DIGIT NUMBER")
            print("<>" * 20)
            return 
        confirm_pin = input("CONFIRM YOUR NEW PIN: ")
        if new_pin == confirm_pin:
            self.pins[self.current_user] = new_pin
            print("<>" * 20)
            print("PIN CHANGED SUCCESSFULLY")
            print("<>" * 20)
        else:
            print("<>" * 20)
            print("PIN MISMATCH. PLEASE TRY AGAIN")
            print("<>" * 20)

def main():
    # main function to run ATM program 
    atm = ATM()
    while True:
        print("\n" + "<>" * 20)
        choice = input("DO YOU WANT TO OPEN NEW ACCOUNT? (YES/NO): ").lower()
        while choice not in ('yes','no'):
            choice = input("DO YOU WANT TO OPEN NEW ACCOUNT? (YES/NO): ").lower()
        if choice == 'YES':
            atm.create_new_account()
        else:
            break
    if atm.authenticate_user():
        atm.show_menu()

if __name__ == "__main__":
    main()

