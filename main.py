import json
import datetime
import os

class FinancialWallet:
    def __init__(self, data_file="wallet_data.json"):
        self.data_file = data_file
        self.records = []
        self.load_records()

    def load_records(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, 'r') as file:
            self.records = json.load(file)

    def save_records(self):
        for idx, record in enumerate(self.records):
            record["Index"] = idx  # Add index field
        with open(self.data_file, 'w') as file:
            json.dump(self.records, file, indent=4)

    def add_record(self, date, category, amount, description):
        index = len(self.records)  # Index is the next available index
        self.records.append({
            "Index": index,  # Add index field
            "Date": date,
            "Category": category,
            "Amount": amount,
            "Description": description
        })
        self.save_records()

    def edit_record(self, index, date, category, amount, description):
        # Check if the index exists
        record_exists = any(record["Index"] == index for record in self.records)
        if not record_exists:
            print("Invalid record index.")
            return

        # Prompt for other fields only if the index exists
        new_record = {
            "Index": index,
            "Date": date,
            "Category": category,
            "Amount": amount,
            "Description": description
        }

        # Update the record
        for record in self.records:
            if record["Index"] == index:
                record.update(new_record)
                break

        self.save_records()



    def search_record(self, category=None, date=None, amount=None):
        results = []
        for record in self.records:
            if date:
                record_date = datetime.datetime.strptime(record["Date"], "%Y-%m-%d").date()
                if (category is None or record["Category"].lower() == category.lower()) and \
                        (record_date == date):
                    results.append(record)
            else:
                if (category is None or record["Category"].lower() == category.lower()) and \
                        (amount is None or float(record["Amount"]) == float(amount)):
                    results.append(record)
        return results

    def show_balance(self):
        income = sum(float(record["Amount"]) for record in self.records if record["Category"].lower() == "income")
        expenses = sum(float(record["Amount"]) for record in self.records if record["Category"].lower() == "expense")
        balance = income - expenses
        print(f"Current Balance: {balance}")
        print(f"Income: {income}")
        print(f"Expenses: {expenses}")

# Example usage
wallet = FinancialWallet()

while True:
    print("\nPersonal Financial Wallet")
    print("1. Show Balance")
    print("2. Add Record")
    print("3. Edit Record")
    print("4. Search Record")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        wallet.show_balance()
    elif choice == "2":
        date = input("Enter Date (YYYY-MM-DD): ")
        category = input("Enter Category (Income/Expense): ")
        amount = input("Enter Amount: ")
        description = input("Enter Description: ")
        wallet.add_record(date, category, amount, description)
    elif choice == "3":
        index = int(input("Enter Record Index to Edit: "))
        # Check if the index exists
        if not any(record["Index"] == index for record in wallet.records):
            print("Invalid record index.")
            continue  # Continue to the next iteration of the loop
        # Prompt for other fields only if the index exists
        date = input("Enter Date (YYYY-MM-DD): ")
        category = input("Enter Category (Income/Expense): ")
        amount = input("Enter Amount: ")
        description = input("Enter Description: ")
        wallet.edit_record(index, date, category, amount, description)
    elif choice == "4":
        category = input("Enter Category to Search (Leave blank for any): ")
        date_str = input("Enter Date to Search (YYYY-MM-DD) (Leave blank for any): ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        amount = input("Enter Amount to Search (Leave blank for any): ")
        results = wallet.search_record(category, date, amount)
        if results:
            print("Search Results:")
            for idx, result in enumerate(results):
                print(f"Record {idx+1}:")
                for key, value in result.items():
                    print(f"{key}: {value}")
                print()
        else:
            print("No records found matching the criteria.")
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")