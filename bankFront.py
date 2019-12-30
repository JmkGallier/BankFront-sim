# import requests
# import plaid
# from plaid import Client
# from plaid.errors import APIError, ItemError
import pickle
from datetime import datetime


# Need way to include Expenses
# Introduce formmating for balance information to include commas
# Since the amount of data I want to collect ranges different topics, i may need to use SQL or multiple CSVs
class UserData:
    historical_data_list = []
    menu_options = ["Display User Financials",
                    "Check Accounts",
                    "Add Account",
                    "Update Accounts",
                    "Delete an Account",
                    "Exit Program"]

    def __init__(self):
        fin_data = Holdings.debt_credit_calc()
        self.date = datetime.today().strftime('%m-%d-%Y')
        self.networth = fin_data[2]
        self.liquidable = fin_data[0]
        self.creditcard_bal = fin_data[1]
        self.total_credit_limit = fin_data[4]
        self.min_cash_balance = fin_data[3]
        self.income_monthly = 0  # some way of calculating this
        UserData.historical_data_list.append(self)

    @staticmethod
    def calc_fin_date():
        fin_dict = {}
        fin_data = Holdings.debt_credit_calc()
        fin_dict['Liquidable Cash Balance'] = fin_data[0]
        fin_dict['Total Credit Card Balance'] = fin_data[1]
        fin_dict['Networth'] = fin_data[2]
        fin_dict['Minimum Cash Balance'] = fin_data[3]
        fin_dict['Total Credit Limit'] = fin_data[4]
        return fin_dict

    @staticmethod
    def display_user_financials():
        Holdings.display_hist()
        fin_dict = UserData.calc_fin_date()
        print("\n", "-"*5)
        print("Financial Dashboard")
        print("Liquidable Cash Balance:", fin_dict["Liquidable Cash Balance"],
              "\nTotal Credit Card Balance:", fin_dict["Total Credit Card Balance"],
              "\nTotal Credit Limit", fin_dict["Total Credit Limit"],
              "\nNetworth:", fin_dict["Networth"])
        print("\n", "-" * 5)

    @staticmethod
    def data_retrieval():
        try:
            with open("si_db.txt", "rb") as pull:
                Holdings.holdings_list = pickle.load(pull)  # Load list of account objects
                UserData.historical_data_list = pickle.load(pull)  # Load list of historical data objects

        except FileNotFoundError:
            user_dec = ""
            while user_dec == "":
                user_dec = input("It seems there is no database in the current directory. Create a new one?(Y/n)")
                if user_dec.lower().strip() == "y" or user_dec.lower().strip() == "":
                    with open("si_db.txt", "wb"):
                        pass
                    user_dec = "pass"
                    # Potential Bug, may need to force account creation at this point
                elif user_dec.lower().strip() == "n":
                    print("Please locate a txt file in the form 'si_db.csv' to use this program")
                    raise SystemExit
                else:
                    print("Please enter 'Y or n'.")
                    user_dec = ""

    @staticmethod
    def dump_data():
        UserData()
        with open("si_db.txt", "wb") as push:
            pickle.dump(Holdings.holdings_list, push)
            pickle.dump(UserData.historical_data_list, push)

    @staticmethod
    def menu_tree():
        pro_state = 0
        user_dec = ""
        while user_dec == "":
            method_counter = 1
            print("Main Menu:")
            for j in UserData.menu_options:
                print("%d. %s" % (method_counter, j))
                method_counter += 1
            try:
                user_dec = int(input("Your choice: "))-1
                user_check = ""
                while user_check == "":
                    user_check = input("You entered '%s', is this correct? (Y/n): " % UserData.menu_options[user_dec])
                    if user_check.lower().strip() == "y" or user_check.lower().strip() == "":
                        menu_choice = UserData.menu_options[user_dec]
                        pro_state = UserData.menu_selection(menu_choice)
                        user_check = "fill"
                    elif user_check.lower().strip() == "n":
                        user_check = ""
                        user_dec = ""
                    else:
                        print("Please enter 'Y' or 'N'.")
                        user_check = ""
            except ValueError:
                user_dec = ""
                print("Please select an appropriate menu option")
        return pro_state

    @staticmethod
    def menu_selection(user_dec):
        pro_state = 0
        if user_dec == "Display User Financials":
            UserData.display_user_financials()
        elif user_dec == "Check Accounts":
            Holdings.accounts_check()
        elif user_dec == "Add Account":
            Holdings.add_accounts()
        elif user_dec == "Update Accounts":
            print("Update Accounts")
        elif user_dec == "Delete an Account":
            Holdings.delete_accounts()
        elif user_dec == "Exit Program":
            print("Exiting Program")
            UserData.dump_data()
            pro_state = 1
        else:
            print("That was not an option")
        return pro_state


class Holdings:
    holdings_list = []
    supp_banks = ["Bank of America",
                  "Syncrony Bank\t",
                  "Citi Bank\t\t",
                  "Capital One",
                  "Venmo\t\t",
                  "SquareCash",
                  "Robinhood\t\t"]

    supp_acc_type = ["Checking\t\t",
                     "Savings\t\t",
                     "Credit Card\t",
                     "Mobile Fin-Tech",
                     "Investment Portfolio"]

    supp_flags = ["Emergency Fund",
                  "High-Yield Savings",
                  "Retirement Savings",
                  "Vacation Savings",
                  "Holiday Savings",
                  "None"]

    def __init__(self):
        self.bankName = Holdings.account_bank()
        self.type = Holdings.account_type(self.bankName)
        self.balance = float(input("What is the balance of this account: "))
        self.flags = Holdings.account_flag()
        self.limit = float(input("What is the 'Minimum Balance' or 'Credit Limit' for this account?: "))
        Holdings.holdings_list.append(self)

    @staticmethod
    def account_bank():
        user_dec = ""
        while user_dec == "":
            print("\nPlease select the bank where this account is located using the number listed.")
            method_counter = 1
            for j in Holdings.supp_banks:
                print("%d. %s" % (method_counter, j))
                method_counter += 1
            try:
                user_dec = (int(input("Your choice: "))-1)
                user_check = ""
                while user_check == "":
                    user_check = input("You entered '%s', is this correct? (Y/n): " % Holdings.supp_banks[user_dec])
                    if user_check.lower().strip() == "y" or user_check.lower().strip() == "":
                        user_check = "y"
                        continue
                    elif user_check.lower().strip() == "n":
                        user_check = ""
                        user_dec = ""
                    else:
                        print("Please enter 'Y' or 'n'.")
                        user_check = ""
            except ValueError:
                print("Please use an integer between 1 and %d" % len(Holdings.supp_banks))
                user_dec = ""
        return Holdings.supp_banks[user_dec]

    @staticmethod
    def account_type(bank_name):
        user_dec = ""
        while user_dec == "":
            print("\nWhat type of account do you have with %s" % bank_name)
            method_counter = 1
            for j in Holdings.supp_acc_type:
                print("%d. %s" % (method_counter, j))
                method_counter += 1
            try:
                user_dec = (int(input("Your choice: "))-1)
                user_check = ""
                while user_check == "":
                    user_check = input("You entered '%s', is this correct? (Y/n): " % Holdings.supp_acc_type[user_dec])
                    if user_check.lower().strip() == "y" or user_check.lower().strip() == "":
                        user_check = 'y'
                        continue
                    elif user_check.lower().strip() == "n":
                        user_check = ""
                        user_dec = ""
                    else:
                        print("Please enter 'Y' or 'N'.")
                        user_check = ""
            except ValueError:
                print("Please use an integer between 1 and %d" % len(Holdings.supp_acc_type))
                user_dec = ""
        return Holdings.supp_acc_type[user_dec]

    @staticmethod
    def account_flag():  # Add ability to add multiple flags, delete repeats after user entry
        user_dec = ""
        while user_dec == "":
            print("\nDoes this account serve any special purpose?")
            method_counter = 1
            for j in Holdings.supp_flags:
                print("%d. %s" % (method_counter, j))
                method_counter += 1
            try:
                user_dec = (int(input("Your choice: "))-1)
                user_check = ""
                while user_check == "":
                    user_check = input("You entered '%s', is this correct? (Y/n): " % Holdings.supp_flags[user_dec])
                    if user_check.lower().strip() == "y" or user_check.lower().strip() == "":
                        user_check = 'y'
                        continue
                    elif user_check.lower().strip() == "n":
                        user_check = ""
                        user_dec = ""
                    else:
                        print("Please enter 'Y' or 'N'.")
                        user_check = ""
            except ValueError:
                print("Please use an integer between 1 and %d" % len(Holdings.supp_flags))
                user_dec = ""
        return Holdings.supp_flags[user_dec]

    @staticmethod
    def accounts_check():
        print("\n", "-"*5)
        print("Current accounts logged:")
        for j in Holdings.holdings_list:
            print(j.bankName, "\t", j.type, "\t", j.balance)
        print("\n", "-"*5)

    @staticmethod
    def add_accounts():
        user_resp = int(input("How many accounts would you like to add?: "))
        for j in range(user_resp):
            Holdings()
            Holdings.accounts_check()

    @staticmethod
    def debt_credit_calc():
        credit_sum = 0
        min_balance = 0
        debt_sum = 0
        total_debt_lim = 0
        for j in Holdings.holdings_list:
            if j.type != "Credit Card\t":
                credit_sum += j.balance
                min_balance += j.limit
            elif j.type == "Credit Card\t":
                debt_sum += j.balance
                total_debt_lim += j.limit
            else:
                print("Hit Else => Class: Holdings, method: debt_credit_calc()")
        return credit_sum, debt_sum, (credit_sum-debt_sum), min_balance, total_debt_lim

    @staticmethod
    def display_hist():
        print("Date\t\t Net-Worth\t\t Monthly Income")
        for j in UserData.historical_data_list:
            print(j.date, "\t", j.networth, '\t\t', j.income_monthly)

    @staticmethod
    def update_accounts():
        pass

    @staticmethod
    def delete_accounts():

        user_dec = ""
        while user_dec == "":
            print("\nWhich Account would you like to delete?")
            method_counter = 1
            for j in Holdings.holdings_list:
                print(method_counter, ".\t", j.bankName, "\t", j.type)
                method_counter += 1
            try:
                user_dec = (int(input("Your choice: ")) - 1)
                user_check = ""
                while user_check == "":
                    user_check = input("You are about to delete '%s', is this correct? (Yes/No): " %
                                       (Holdings.holdings_list[user_dec].bankName +
                                        " - " +
                                        Holdings.holdings_list[user_dec].type))

                    if user_check.lower().strip() == "yes":
                        del Holdings.holdings_list[user_dec]
                        continue
                    elif user_check.lower().strip() == "no":
                        user_check = ""
                        user_dec = ""
                    else:
                        print("Please enter 'Yes' or 'No'.")
                        user_check = ""
            except ValueError:
                print("Please use an integer between 1 and %d" % len(Holdings.supp_flags))
                user_dec = ""


UserData.data_retrieval()

program_state = 0
while program_state == 0:
    program_state = UserData.menu_tree()



# Load data from pickle file
# Display user accounts
# Provide menu
    # Delete Account
    # Update Account


# # API # #
# PLAID_CLIENT_ID=5cf8369c5885ff001239e930
# PLAID_SECRET=5cf80845b2e5c9ddc0b92dc31ec8
# PLAID_PUBLIC_KEY=26d9149377ea5396fbbddd2cbcb6fe
# PLAID_PRODUCTS=transactions
# PLAID_COUNTRY_CODES=US,CA,GB,FR,ES
# PLAID_ENV=sandbox python server.py
# # #
# access_tok = "access-sandbox-554fbd94-3b62-45df-a380-ece66ded18d8"
# item_id = "8Aalnm8RaNcpxgwnPZR5skgN98e18lIwajE4k"
#
# client = Client(client_id="5cf8369c5885ff001239e930",
#                 secret="5cf80845b2e5c9ddc0b92dc31ec8aa",
#                 public_key="26d9149377ea5396fbbddd2cbcb6fe",
#                 environment="sandbox")
#
# text = plaid.api.Accounts(client)
# text.balance
