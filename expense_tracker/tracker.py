import json
from datetime import datetime

FILENAME = "data.json"

def load_data():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return[]

def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=2)

def add_expense():
    category = input("Enter Category:")
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD) or leave empty for today:" )
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    expense = {"category": category, "amount": amount, "date": date}
    data = load_data()
    data.append(expense)
    save_data(data)
    print("Expense added!")

def list_expenses():
    data = load_data()
    for exp in data:
        print(f"{exp['date']} | {exp['category']} | ${exp['amount']:.2f}")

def total_spent():
    data = load_data()
    total = sum(exp['amount'] for exp in data)
    print(f"Total spent: ${total:.2f}")

def menu():
    while True:
        print("\n1. Add expense\n2. List expense\n3. Show total\n4. Exit")
        choice = input("Choose an option")
        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif  choice == "3":
            total_spent()
        elif choice == "4":
            break
        else:
            print("Invalid Option Choosen.")

if __name__ == "__main__":
    menu()