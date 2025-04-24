from databases import connection, cursor

class User:
    def __init__(self, username, pin):
        self.username = username
        self.pin = pin
    
    def authenticate(self):
        cursor.execute("SELECT * FROM USERS WHERE username=? AND pin=?", (self.username, self.pin))
        return cursor.fetchone()

    @staticmethod
    def register(username, email, pin):
        try:
            cursor.execute("INSERT INTO USERS (username, email, pin) VALUES (?, ?, ?)", (username, email, pin))
            connection.commit()
            print("✅ Account registered successfully!")
        except:
            print("⚠️ Username or Email already exists!")

    @staticmethod
    def reset_pin(email):
        cursor.execute("SELECT * FROM USERS WHERE email=?", (email,))
        user = cursor.fetchone()
        if user:
            new_pin = input("🔑 Enter your new 4-digit PIN: ")
            if len(new_pin) == 4 and new_pin.isdigit():
                cursor.execute("UPDATE USERS SET PIN = ? WHERE EMAIL = ?", (new_pin, email))
                connection.commit()
                print("✅ PIN updated successfully!")
            else:
                print("❌ PIN must be exactly 4 digits.")
        else:
            print("❌ Email not found!")


class Account:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_balance(self):
        cursor.execute("SELECT balance FROM USERS WHERE ID = ?", (self.user_id,))
        return cursor.fetchone()[0]
    
    def get_username(self):
        cursor.execute("SELECT username FROM USERS WHERE ID = ?", (self.user_id,))
        return cursor.fetchone()[0]
    
    def get_email(self):
        cursor.execute("SELECT email FROM USERS WHERE ID = ?", (self.user_id,))
        return cursor.fetchone()[0]
    
    def deposit(self, amount):
        amount = float(amount)
        if amount <= 0:
            print("⚠️ Invalid deposit amount.")
            return
        cursor.execute("UPDATE USERS SET balance = balance + ? WHERE ID = ?", (amount, self.user_id))
        connection.commit()
        print(f"💰 Deposited: ${amount:.2f}")
    
    def withdraw(self, amount):
        amount = float(amount)
        balance = self.get_balance()
        if amount > balance:
            print("❌ Insufficient balance.")
            return
        cursor.execute("UPDATE USERS SET balance = balance - ? WHERE ID = ?", (amount, self.user_id))
        connection.commit()
        print(f"💸 Withdrawn: ${amount:.2f}")

    def get_info(self):
        print("🧾 " + "=" * 35)
        print("📄 USER INFORMATION")
        print(f"👤 Username : {self.get_username()}")
        print(f"📧 Email    : {self.get_email()}")
        print(f"💰 Balance  : ${self.get_balance():.2f}")
        print("=" * 40)

    def __str__(self):
        return f"{self.user_id}'s Account"
