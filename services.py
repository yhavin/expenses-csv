import csv
from tabulate import tabulate
from datetime import datetime
import time
from time import sleep


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


from cli import choose_operation, delete_expense, export_menu
