# Python CLI expense tracker
# Author: Yakir Havin
# GitHub: yhavin


import csv
from tabulate import tabulate
from time import sleep
from datetime import datetime
import time


# Prompt user to choose existing file or create new
def main_menu():
    print("Welcome to the expense tracker.")
    print("  1. Start new expenses file")
    print("  2. Continue from saved file")
    print("  3. Quit")

    choice = int(input("What would you like to do?\n"))

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
    headers = ["id", "date", "category", "description", "amount"]

    if not filename.endswith(".csv"):
        filename += ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        print(headers)
        writer.writerow(headers)

    print(f"New expenses file '{filename}' created.\n")
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
    print("  3. Delete an expense")
    print("  4. View category summary")
    print("  5. View month summary")
    print("  6. Back to main menu")
    print("  7. Quit")

    choice = int(input("What would you like to do?\n"))

    if choice == 1:
        add_expense(filename)
    elif choice == 2:
        view_expenses(filename)
    elif choice == 3:
        view_expenses(filename, True)
    elif choice == 4:
        view_category_summary(filename)
    elif choice == 5:
        view_month_summary(filename)
    elif choice == 6:
        main_menu()
    elif choice == 7:
        quit()


# Add new expense
def add_expense(filename):
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        date = input("Enter the date (YYYY-MM-DD): ")
        category = input("Enter the category: ").capitalize()
        description = input("Enter the description: ").capitalize()
        amount = float(input("Enter the amount: "))

        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

        eid = time.time()

        expense = {
            eid: eid,
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
def view_expenses(filename, is_deleting=False):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        expenses = list(reader)

    headers = [word.title() for word in expenses[0]]
    rows = expenses[1:]
    for i in range(len(rows)):
        rows[i][0] = i

    total = [None, "TOTAL", None, None, sum([float(row[4]) for row in rows])]
    rows.append(total)

    table = tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f")
    print(table, "\n")
    
    if is_deleting:
        delete_expense(filename)
    
    sleep(2)
    choose_operation(filename)


# View category summary
def view_category_summary(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        expenses = list(reader)

    category_totals = {}
    for expense in expenses[1:]:
        category = expense[2]
        amount = float(expense[4])

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    summary_list = [[category, total_spent] for category, total_spent in category_totals.items()]
    total = ["TOTAL", sum([float(row[1]) for row in summary_list])]
    summary_list.append(total)

    headers = ["Category", "Total spent"]
    table = tabulate(summary_list, headers=headers, tablefmt="grid", floatfmt=".2f")
    print(table, "\n")
    export_menu("category", headers, summary_list, filename)


# View month summary
def view_month_summary(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        expenses = list(reader)

    month_totals = {}
    for expense in expenses[1:]:
        date = datetime.strptime(expense[1], "%Y-%m-%d")
        month_year = date.strftime("%B-%Y")
        amount = float(expense[4])

        if month_year in month_totals:
            month_totals[month_year] += amount
        else:
            month_totals[month_year] = amount   

    summary_list = [[month_year, total_spent] for month_year, total_spent in month_totals.items()]
    total = ["TOTAL", sum([float(row[1]) for row in summary_list])]
    summary_list.append(total)

    headers = ["Month-Year", "Total spent"]
    table = tabulate(summary_list, headers=headers, tablefmt="grid", floatfmt=".2f")
    print(table, "\n")
    export_menu("month", headers, summary_list, filename)


# Delete expense menu
def delete_expense(filename):
    choice = int(input("Enter the id of the expense to remove: "))

    with open(filename, "r", newline="") as file:
        rows = list(csv.reader(file))

    if choice < 0 or choice > (len(rows) - 2):
        print("Invalid id. Please try again")
        return
    
    del rows[choice + 1]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Expense id {choice} deleted.")

    sleep(2)
    choose_operation(filename)


# Export summary menu
def export_menu(type, headers, data, filename):
    sleep(2)
    choice = input("Would you like to export this summary? (y/N)\n")

    if choice == "y":
        date_tag = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        export_name = type + "_summary_" + date_tag + ".csv"
        with open(export_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in data:
                writer.writerow([row[0], f"{row[1]:.2f}"])
        
        print(f"Exported to {export_name}.")
        sleep(1)
    choose_operation(filename)


# Driver code
if __name__ == '__main__':
    main_menu()