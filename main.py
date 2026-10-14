import csv
import math
import shutil

from datetime import datetime, timezone
from pathlib import Path
from decimal import Decimal, InvalidOperation

# Locate expenses.csv in the same directory as this script, no matter where it's launched from
FILE_PATH = Path(__file__).resolve().parent / "expenses.csv"


def initialize_file():
    if not FILE_PATH.exists():
        with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "description", "category", "amount"])
        print("created new file")


def get_non_empty_input(prompt):
    """Keeps asking until the user provides non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Field cannot be empty. Please try again.")


def load_expenses():
    """Loads expenses from file, reporting malformed rows and backing up the original file if corruption is found."""
    expenses = []
    malformed_found = False

    if FILE_PATH.exists():
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for line_num, row in enumerate(reader, start=2):
                if not row:
                    continue

                try:
                    if len(row) < 4:
                        raise IndexError("Row has missing columns.")

                    date = row[0]
                    description = row[1]
                    category = row[2]
                    amount = Decimal(row[3])

                    if not amount.is_finite() or amount <= 0:
                        raise ValueError(
                            "Amount must be a finite number greater than zero"
                        )

                    expense = {
                        "date": date,
                        "description": description,
                        "category": category,
                        "amount": amount,
                    }
                    expenses.append(expense)

                except (IndexError, ValueError, InvalidOperation) as e:
                    malformed_found = True
                    print(
                        f"Warning: Skipping malformed row {line_num} {row} -> Reason: {e}"
                    )

        # If any malformed rows were found, create a safety backup of the original file
        if malformed_found:
            backup_path = FILE_PATH.with_suffix(".bak")
            shutil.copy(FILE_PATH, backup_path)
            print(
                f"Safety Notice: Original file backed up to '{backup_path}' to prevent data loss."
            )

    return expenses


def get_amount():
    """Helper function to keep asking for amount until a valid number is given"""
    while True:
        amount_input = input("Enter amount: ").strip()
        try:
            amount = Decimal(amount_input)
            if math.isfinite(amount) and amount > 0:
                return amount
            else:
                print("Amount must be greater than zero. Please try again.")
        except (InvalidOperation, ValueError):
            print("Invalid input! Please enter a valid number (e.g., 12.50).")


def save_to_file(expenses):
    """Helper function to write all current expenses to the CSV file immediately."""
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "description", "category", "amount"])

        for item in expenses:
            writer.writerow(
                [item["date"], item["description"], item["category"], item["amount"]]
            )


def get_date():
    while True:
        date_input = input("Enter date (DD/MM/YYYY)").strip()
        try:
            # try parsing the input to ensure its a real, correctly formatted date
            parsed_date = datetime.strptime(date_input, "%d/%m/%Y")
            return parsed_date.strftime("%d/%m/%Y")
        except ValueError:
            print("Invalid date format.")


def add_expense(expenses):
    """Function for choice 1:  Prompts for details and appends to the expenses list."""
    print("\n--- Add new Expense ---")

    date = get_date()
    description = get_non_empty_input("Enter description: ")
    category = get_non_empty_input("Enter category: ")
    amount = get_amount()  # Calls helper that validates the number

    # Create a single expense record (as a dict or list)
    expense = {
        "date": date,
        "description": description,
        "category": category,
        "amount": amount,
    }

    # Add to the expenses list
    expenses.append(expense)

    # Save immediately so it survives crashes or abrupt closures
    save_to_file(expenses)
    print("Expense added successfully!")


def view_expenses(expenses):
    """Function for Choice 2: Views all current expenses."""
    print("\n--- Current Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return
    for idx, item in enumerate(expenses, start=1):
        print(
            f"{idx}. {item['date']} | {item['category']} | {item['description']} | {item['amount']:.2f}"
        )
        print("-" * 30)


def search_by_category(expenses):
    """Function for choice 3: searches by category and prints matches."""
    print("\n--- Search by Category ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    search_term = input("Enter category to search for: ").strip().lower()
    found = False

    for item in expenses:
        # case-insenisitive comparison so Food and food both match
        if item["category"].lower() == search_term:
            print(
                f"-> Date: {item['date']} | Description: {item['description']} | Amount: {item['amount']:.2f}"
            )
            found = True

        # If no matches were found during the loop
    if not found:
        print(f"None matched category '{search_term}'.")


def show_total(expenses):
    """Function for Choice 4: Calculates and displays the total of all expenses."""
    if not expenses:
        print("\nNo expenses recorded yet. Total: 0.00")
        return

    total = Decimal("0.0")
    for item in expenses:
        total += item["amount"]

    print("\n--- Total Expenses ---")
    print(f"Total: {total:.2f}")


def save_and_exit(expenses):
    """Function for Choice 5: Writes expenses to CSV and exits."""
    save_to_file(expenses)
    print("Expenses saved to 'expenses.csv'. Goodbye!")


def show_menu():
    """Prints the menu options."""
    print("\n--- Expense Tracker Menu ---")
    print("1. Add expense")
    print("2. View all")
    print("3. Filter by category")
    print("4. Show total")
    print("5. Save and quit")


def main():
    # Create file with a header if none exists
    initialize_file()

    # Load existing expenses
    expenses = load_expenses()

    # Forever loop
    while True:
        # 1. Display the menu
        show_menu()
        # 2. Get the user's choice
        choice = input("Choose and option: ").strip()

        # 3. Handle the choice
        # choice 1 ask for date, description, category, amount (turn into a number - if not a number ask again), put into one expense
        # add to expenses
        if choice == "1":
            add_expense(expenses)

        # choice 2 if empty show nothing yet. otherwise print each expense neatly
        elif choice == "2":
            view_expenses(expenses)
        # choice 3 ask for a category, for loop expense if matches print if not say none matched
        elif choice == "3":
            search_by_category(expenses)
        # choice 4 show total, for loop expense add amount to total, print total
        elif choice == "4":
            show_total(expenses)
        # choice 5 open the file for writing, write the header row, write each expense as a row
        # stop the loop
        elif choice == "5":
            save_and_exit(expenses)
            break  # exits the forever loop
        # otherwise say invalid choice
        else:
            print("\nInvalid choice! Please try again.")


if __name__ == "__main__":
    main()
