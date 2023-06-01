from services import create_new_file, open_existing_file, add_expense, view_expenses, view_category_summary, view_month_summary
import csv
from time import sleep
from datetime import datetime


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