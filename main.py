# Python CLI expense tracker
# Author: Yakir Havin
# GitHub: yhavin

import csv
from tabulate import tabulate
from time import sleep


# Prompt user to choose existing file or create new
def main_menu():
    print("Welcome to the expense tracker.")
    print("  1. Start new expenses file")
    print("  2. Continue from saved file")
    print("  3. Quit")

    choice = int(input("What would you like to do? "))

    if choice == 1:
        filename = input("Name your new expenses file: ")
        create_new_file(filename)
    elif choice == 2:
        filename = input("What is your current file named? ")
        open_existing_file(filename)
    elif choice == 3:
        quit()


# Create new expenses file
def create_new_file(filename):
    headers = ["date", "category", "description", "amount"]

    if not filename.endswith(".csv"):
        filename += ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        print(headers)
        writer.writerow(headers)

    print(f"New expenses file '{filename}' created.")
    choose_operation(filename)


# Open existing file
def open_existing_file(filename):
    if not filename.endswith(".csv"):
        filename += ".csv"

    choose_operation(filename)


# Choose operation after creating/opening file
def choose_operation(filename):
    print(f"Currently accessing file '{filename}'.")
    print("  1. Add new expense")
    print("  2. View all expenses")
    print("  3. View summary")
    print("  4. Back to main menu")
    print("  5. Quit")

    choice = int(input("What would you like to do? "))

    if choice == 1:
        add_expense(filename)
    elif choice == 2:
        view_expenses(filename)
    elif choice == 3:
        view_summary(filename)
    elif choice == 4:
        main_menu()
    elif choice == 5:
        quit()


# Add new expense
def add_expense(filename):
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        date = input("Enter the date (YYYY-MM-DD): ")
        category = input("Enter the category: ").capitalize()
        description = input("Enter the description: ").capitalize()
        amount = float(input("Enter the amount: "))

        expense = {
            date: date,
            category: category,
            description: description,
            amount: amount
        }

        writer.writerow(expense)

    print("Expense successfully saved.\n")
    sleep(1)
    choose_operation(filename)


# View expenses
def view_expenses(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        expenses = list(reader)

    headers = [word.title() for word in expenses[0]]
    rows = expenses[1:]

    table = tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f")
    print(table, "\n")
    sleep(2)
    choose_operation(filename)


# View summary
def view_summary(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        expenses = list(reader)

    category_totals = {}
    for expense in expenses[1:]:
        category = expense[1]
        amount = float(expense[3])

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    summary_list = [[category, total_spent] for category, total_spent in category_totals.items()]
    headers = ["Category", "Total spent"]
    table = tabulate(summary_list, headers=headers, tablefmt="grid", floatfmt=".2f")
    print(table, "\n")
    sleep(2)
    choose_operation(filename)


# Driver code
if __name__ == '__main__':
    main_menu()