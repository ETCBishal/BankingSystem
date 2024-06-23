import pyinputplus as inp
from time import sleep
from datetime import datetime
import pandas as pd
import logging
from Utils import CheckPassword, append_to_database, read_database, write_to_json_file

class MuktinathBank:

    LOGIN_STATUS = False  # Class attribute to track login status

    def inputPhone(self, prompt="Phone no. : "):
        """Prompt the user to input their phone number."""
        return inp.inputStr(prompt)

    def sign_up(self, fname, lname, address, phone, email, password):
        """Register a new user by appending their details to the database."""
        DATA_FILE = "Database.json"
        data = {
            "FirstName": fname,
            "LastName": lname,
            "Address": address,
            "Phone_no": phone,
            "Email": email,
            "Password": password,
        }
        append_to_database(DATA_FILE, data)

    def authenticate_user(self, FILE_NAME, phone, password):
        """Authenticate user by checking phone number and password in the database."""
        login_info = read_database(FILE_NAME)
        for info in login_info:
            if info["Phone_no"] == phone and info["Password"] == password:
                self.auth = True
                self.user_data = info
                return self.user_data, True
        return None, False

    def login(self, phone, password):
        """Log in the user if authentication is successful."""
        DATA_FILE = "Database.json"
        user_data, is_authentic_user = self.authenticate_user(DATA_FILE, phone=phone, password=password)
        if is_authentic_user:
            self.LOGIN_STATUS = True
            print(f'Welcome {user_data["FirstName"]}')
            self.read_transactions('transactions.json', phone, password)
            return self.LOGIN_STATUS
        else:
            print("Login failed. Check your phone number and password.")
            return self.LOGIN_STATUS

    def logout(self):
        """Log out the current user."""
        if self.LOGIN_STATUS:
            self.LOGIN_STATUS = False
            print('Logging out.....Success!')
        else:
            print('You are already logged out!')

    def delete_account(self, phone, password):
        """Delete a user account and related transactions from the database."""
        FILE_NAME = 'Database.json'
        TRANSACTIONS_FILE = 'transactions.json'
        try:
            # Read databases
            self.user_informations = read_database(FILE_NAME)
            self.transactions = read_database(TRANSACTIONS_FILE)
            
            # Filter out the user to delete
            self.user_informations = [info for info in self.user_informations if not (info['Phone_no'] == phone and info['Password'] == password)]
            
            # Filter transactions to keep only those not related to the deleted user
            self.transactions_to_keep = [transaction for transaction in self.transactions if transaction['Sender_phone_no'] != phone or transaction['Sender_password'] != password]
            
            # Write the updated data back to the files
            write_to_json_file(FILE_NAME, self.user_informations)
            write_to_json_file(TRANSACTIONS_FILE, self.transactions_to_keep)
            
            logging.info(f"Account with phone {phone} deleted successfully.")
            return True
        except Exception as e:
            logging.error(f"An error occurred while deleting the account: {e}")
            return False

    def read_transactions(self, TRANS_FILE_NAME, phone, password):
        """Read and display all transactions related to the logged-in user."""
        self.user_transactions = []
        if self.LOGIN_STATUS:
            self.transactions_data = read_database(TRANS_FILE_NAME)
            for transaction in self.transactions_data:
                if transaction["Sender_phone_no"] == phone and transaction["Sender_password"] == password:
                    self.user_transactions.append(transaction)
            if self.user_transactions:
                print(pd.DataFrame(self.user_transactions))
                print(f"Total Transactions : {len(self.user_transactions)}")
            else:
                print("No transactions found.")
        else:
            print('Please login first!')

    def transfer_to(self, receiver):
        """Transfer money to another user if logged in."""
        if self.LOGIN_STATUS:
            amount = inp.inputInt("Amount to Transfer : ")
            user_info = self.user_data
            data = {
                "Sender": user_info["FirstName"],
                "Sender_password": user_info["Password"],
                "Sender_phone_no": user_info["Phone_no"],
                "Receiver": receiver,
                "Date-Time": datetime.now().strftime("Date:%d:%m:%Y-Time:%H:%M:%S"),
                "Amount": amount,
            }
            append_to_database("transactions.json", data=data)
            self.read_transactions('transactions.json', phone=user_info['Phone_no'], password=user_info['Password'])
        else:
            print('Please Login!')

    def create_account(self):
        """Create a new user account if not logged in."""
        if not self.LOGIN_STATUS:
            fname = inp.inputStr("First name : ")
            lname = inp.inputStr("Last name : ")
            address = inp.inputStr("Address : ")
            phone = self.inputPhone()
            email = inp.inputEmail("Email : ")
            password = inp.inputPassword("Password : ")

            STATUS = CheckPassword(password=password)
            while STATUS == 0:
                print("[!] Please enter a strong password (like: Password$123)")
                password = inp.inputPassword("Password : ")
                STATUS = CheckPassword(password=password)
            
            print(f"Hi {fname}, Welcome to MuktinathBank!\n")
            sleep(2)
            self.sign_up(fname, lname, address, phone, email, password)
            self.login(phone, password)
        else:
            print("You are already logged in. Please log out first to create a new account.")

if __name__ == "__main__":
    bank = MuktinathBank()
    while True:
        print('\n0.Quit\n1.Create Account\n2.Login\n3.Transfer Money\n4.Logout\n5.Delete Account', end='')
        prompt = int(input(' : '))

        if prompt == 0:
            break
        elif prompt == 1:
            bank.create_account()
        elif prompt == 2:
            phone = input('Phone : ')
            password = input('Password : ')
            bank.login(phone, password)            
        elif prompt == 3:
            receiver = input('Receiver : ')
            bank.transfer_to(receiver)
        elif prompt == 4:
            bank.logout()
        elif prompt == 5:
            phone = input('Phone : ')
            password = input('Password : ')
            if bank.delete_account(phone, password):
                print("Account deleted successfully.")
            else:
                print("Failed to delete account. Check the phone number and password.")
        else:
            print('Error! Invalid option.')
