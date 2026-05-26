#==========================
# Expense Tracker
# by Yiranesh
# language: python
#==========================

import json
import os
from datetime import datetime

# Files where all the expenses are saved
DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food",
    "Transport",
    "Education",
    "Entertainment",
    "Shopping",
    "Health",
    "Other"
]


# Load saved expenses from the file
def load_expenses():
    """Load expenses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save the expenses into the file
def save_expenses(expenses):
    """Save expenses to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Let the user choose an expense category
def get_category():
    """Ask the user to select a category."""
    print("\nCategories:")

    for number, category in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {category}")

    while True:
        try:
            choice = int(input("Select category: "))

            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]

            print(f"Please choose between 1 and {len(CATEGORIES)}.")

        except ValueError:
            print("Invalid input. Please enter a number.")

# Get a valid amount from the user
def get_amount():
    """Ask the user to enter a valid expense amount."""
    while True:
        try:
            amount = float(input("Amount (RM): "))

            if amount > 0:
                return amount

            print("Amount must be greater than 0.")

        except ValueError:
            print("Invalid input. Please enter a number.")

# Create the next id for a new expense
def get_next_id(expenses):
    """Generate the next expense ID."""
    if not expenses:
        return 1

    return max(expense["id"] for expense in expenses) + 1

# Add a new expense to the list
def add_expense(expenses):
    """Add a new expense."""
    print("\n--- ADD EXPENSE ---")

    description = input("Description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    category = get_category()
    amount = get_amount()

    expense = {
        "id": get_next_id(expenses),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "description": description,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)

    print(f"\nExpense added: {description} - RM{amount:.2f} [{category}]")

# Show all expenses in a table
def view_all_expenses(expenses):
    """Display all expenses."""
    print("\n--- ALL EXPENSES ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'ID':<5} {'Date':<17} {'Description':<22} {'Category':<14} {'Amount':>10}")
    print("-" * 72)

    for expense in expenses:
        print(
            f"{expense['id']:<5} "
            f"{expense['date']:<17} "
            f"{expense['description']:<22} "
            f"{expense['category']:<14} "
            f"RM{expense['amount']:>8.2f}"
        )

    print("-" * 72)

    total = sum(expense["amount"] for expense in expenses)
    print(f"{'TOTAL':>60} RM{total:>8.2f}")

# Show total spending for each category
def view_by_category(expenses):
    """Show total spending by category."""
    print("\n--- SPENDING BY CATEGORY ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}

    for expense in expenses:
        category = expense["category"]
        summary[category] = summary.get(category, 0) + expense["amount"]

    total_spent = sum(summary.values())

    print(f"\n{'Category':<20} {'Total':>10} {'Percentage':>12}")
    print("-" * 46)

    for category, amount in sorted(summary.items(), key=lambda item: item[1], reverse=True):
        percentage = (amount / total_spent) * 100
        bar = "█" * int(percentage / 5)

        print(f"{category:<20} RM{amount:>8.2f} {percentage:>10.1f}% {bar}")

    print("-" * 46)
    print(f"{'TOTAL':<20} RM{total_spent:>8.2f}")

# Show expenses only for the current month
def monthly_summary(expenses):
    """Show spending for the current month."""
    print("\n--- MONTHLY SUMMARY ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    current_month = datetime.now().strftime("%Y-%m")

    monthly_expenses = [
        expense for expense in expenses
        if expense["date"].startswith(current_month)
    ]

    if not monthly_expenses:
        print("No expenses recorded this month.")
        return

    total = sum(expense["amount"] for expense in monthly_expenses)

    print(f"\nMonth        : {datetime.now().strftime('%B %Y')}")
    print(f"Transactions : {len(monthly_expenses)}")
    print(f"Total Spent  : RM{total:.2f}")

# Delete an expense using its id
def delete_expense(expenses):
    """Delete an expense by ID."""
    print("\n--- DELETE EXPENSE ---")

    if not expenses:
        print("No expenses to delete.")
        return

    view_all_expenses(expenses)

    while True:
        try:
            expense_id = int(input("\nEnter expense ID to delete (0 to cancel): "))

            if expense_id == 0:
                print("Delete cancelled.")
                return

            for expense in expenses:
                if expense["id"] == expense_id:
                    expenses.remove(expense)
                    save_expenses(expenses)

                    print(f"Deleted: {expense['description']} - RM{expense['amount']:.2f}")
                    return

            print("ID not found. Try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")

# Display the main menu
def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("        EXPENSE TRACKER")
    print("=" * 40)
    print("  1. Add Expense")
    print("  2. View All Expenses")
    print("  3. View by Category")
    print("  4. Monthly Summary")
    print("  5. Delete Expense")
    print("  6. Exit")
    print("=" * 40)

# Runs the entire program
def main():
    """Run the expense tracker program."""
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_all_expenses(expenses)
        elif choice == "3":
            view_by_category(expenses)
        elif choice == "4":
            monthly_summary(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            print("\nGoodbye! Keep tracking your expenses!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
    