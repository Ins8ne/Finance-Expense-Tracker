import csv
from datetime import date
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

# Create the header of the table
table = Table(show_header=True, header_style="bold blue")
table.add_column("Date", style="dim", width=10)
table.add_column("Category")
table.add_column("Description")
table.add_column("Expense", justify="right")

# Load existing expenses from the csv file
data = []
try:
    with open("finances.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
except FileNotFoundError:
    pass

def save_data(data):
    # Save the data to a csv file
    with open("finances.csv", "w", newline="") as csvfile:
        fieldnames = ["Date", "Category", "Description", "Expense"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def add_expense():
    console.clear()
    console.print("Add a New Expense\n", style="bold")
    today = date.today().strftime("%Y-%m-%d")

    with open("finances.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        categories = [row[1] for row in reader]
        categories = list(set(categories))

    console.print("Available Categories:\n")
    for i, category in enumerate(categories, start=1):
        console.print(f"{i}) {category}")

    choice = console.input("\nSelect an existing category (enter the number) or enter a new category (enter 'N'): ")

    if choice.isdigit() and int(choice) in range(1, len(categories) + 1):
        category = categories[int(choice) - 1]
    else:
        category = console.input("Enter New Category: ")

    description = console.input("Enter Description: ")
    expense = console.input("Enter Expense: $")

    # Append the new expense to the data list
    data.append({"Date": today, "Category": category, "Description": description, "Expense": expense})
    save_data(data)

    console.print("\nExpense added successfully! 🎉\n", style="bold green")




def view_expenses():
    # Show the table with expenses for today
    console.clear()
    console.print("Expenses Summary for Today\n", style="bold")
    total_expenses = 0.0

    # Recreate the table object
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Date", style="dim", width=10)
    table.add_column("Category")
    table.add_column("Description")
    table.add_column("Expense", justify="right")

    today = date.today().strftime("%Y-%m-%d")
    for row in data:
        if row["Date"] == today:
            table.add_row(row["Date"], row["Category"], row["Description"], f"${row['Expense']}")
            total_expenses += float(row["Expense"])

    console.print(table)
    console.print(f"\nTotal expenses for today: ${total_expenses:.2f}\n", style="bold")


def get_monthly_summary(month, year):
    # Filter expenses for the specified month and year
    monthly_expenses = [expense for expense in data if expense["Date"].startswith(f"{year}-{month:02d}")]

    # Calculate the total expenses for each category
    category_totals = {}
    for expense in monthly_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        if category in category_totals:
            category_totals[category] += expense_amount
        else:
            category_totals[category] = expense_amount

    # Show the monthly summary
    console.clear()
    console.print(f"{month}/{year} Monthly Summary\n", style="bold")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Category")
    table.add_column("Expense", justify="right")
    for category, total in category_totals.items():
        table.add_row(category, f"${total:.2f}")
    console.print(table)

    total_expenses = sum(category_totals.values())
    console.print(f"\nTotal expenses for {month}/{year}: ${total_expenses:.2f}\n", style="bold")


















def get_yearly_summary(year):
    console.clear()
    yearly_expenses = [expense for expense in data if expense["Date"].startswith(f"{year}-")]

    # Calculate the total expenses for each category
    category_totals = {}
    for expense in yearly_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        if category in category_totals:
            category_totals[category] += expense_amount
        else:
            category_totals[category] = expense_amount

    console.print(f"{year} Yearly Summary\n", style="bold")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Category")
    table.add_column("Expense", justify="right")
    for category, total in category_totals.items():
        table.add_row(category, f"${total:.2f}")
    console.print(table)

    total_expenses = sum(category_totals.values())
    console.print(f"\nTotal expenses for {year}: ${total_expenses:.2f}\n", style="bold")












def get_daily_summary(day, month, year):
    # Filter expenses for the specified day, month, and year
    daily_expenses = [expense for expense in data if expense["Date"] == f"{year}-{month:02d}-{day:02d}"]

    # Calculate the total expenses for each category and collect descriptions
    category_totals = {}
    descriptions = {}
    for expense in daily_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        description = expense["Description"]
        if category in category_totals:
            category_totals[category] += expense_amount
            descriptions[category].append((description, expense_amount))
        else:
            category_totals[category] = expense_amount
            descriptions[category] = [(description, expense_amount)]

    # Show the daily summary
    console.clear()
    console.print(f"{day}/{month}/{year} Daily Summary\n", style="bold")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Category", style="bold")
    table.add_column("Description")
    table.add_column("Expense", justify="right")
    for category, total in category_totals.items():
        table.add_row(category, "", "")  # Add empty row for spacing
        for index, (description, amount) in enumerate(descriptions[category]):
            if index == 0:
                table.add_row("", description, f"${amount:.2f}")
            else:
                table.add_row("", description, f"${amount:.2f}")
        table.add_row("", "-"*12, "-"*9)  # Add separator between descriptions
        table.add_row("", "Total", f"${total:.2f}")  # Add category total row
    console.print(table)

    total_expenses = sum(category_totals.values())
    console.print(f"\nTotal expenses for {day}/{month}/{year}: ${total_expenses:.2f}\n", style="bold")





















    
    
def select_year():
    console.clear()
    console.print("Select Yearly, Monthly, and Daily Summary\n", style="bold")
    year = console.input("Enter the year (e.g., 2022): ")
    console.print("\nSelect an Option:\n", style="bold")
    console.print("1) Yearly Summary")
    console.print("2) Monthly Summary")
    console.print("3) Daily Summary")
    console.print("4) Go Back\n")

    choice = console.input("Enter your choice: ")
    if choice == "1":
        get_yearly_summary(year)
    elif choice == "2":
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        get_monthly_summary(int(month), year)
    elif choice == "3":
        day = console.input("Enter the day as a number (e.g., 01, 02, etc.): ")
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        get_daily_summary(int(day), int(month), year)
    elif choice == "4":
        return
    else:
        console.print("\nInvalid choice! Please enter a number from 1 to 4.\n", style="bold red")

    # Wait for the user to press Enter to go back to the menu
    input("\nPress Enter to go back to the menu...")
    menu()
    
    
    
    
def clear_expenses():
    console.clear()
    console.print("Clear Expenses\n", style="bold")
    console.print("Select an Option:\n", style="bold")
    console.print("1) Clear All Expenses")
    console.print("2) Clear Expenses for a Specific Day")
    console.print("3) Clear Expenses for a Specific Month")
    console.print("4) Clear Expenses for a Specific Year")
    console.print("5) Go Back\n")

    choice = console.input("Enter your choice: ")
    if choice == "1":
        data.clear()
        save_data(data)
        console.print("\nAll expenses cleared successfully! 💸\n", style="bold green")
    elif choice == "2":
        day = console.input("Enter the day as a number (e.g., 01, 02, etc.): ")
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        year = console.input("Enter the year (e.g., 2022): ")
        data[:] = [expense for expense in data if expense["Date"] != f"{year}-{month.zfill(2)}-{day.zfill(2)}"]
        save_data(data)
        console.print(f"\nExpenses for {month}/{day}/{year} cleared successfully! 💸\n", style="bold green")
    elif choice == "3":
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        year = console.input("Enter the year (e.g., 2022): ")
        data[:] = [expense for expense in data if not expense["Date"].startswith(f"{year}-{month.zfill(2)}")]
        save_data(data)
        console.print(f"\nExpenses for {month}/{year} cleared successfully! 💸\n", style="bold green")
    elif choice == "4":
        year = console.input("Enter the year (e.g., 2022): ")
        data[:] = [expense for expense in data if not expense["Date"].startswith(f"{year}")]
        save_data(data)
        console.print(f"\nExpenses for {year} cleared successfully! 💸\n", style="bold green")
    elif choice == "5":
        return
    else:
        console.print("\nInvalid choice! Please enter a number from 1 to 5.\n", style="bold red")

    # Wait for the user to press Enter to go back to the menu
    input("\nPress Enter to go back to the menu...")
    menu()

def read_expenses_from_file():
    console.clear()
    console.print("Read Expenses from File\n", style="bold")
    filename = "expensives.md"

    with open(filename, "r") as file:
        lines = file.readlines()

    current_category = None
    for line in lines:
        line = line.strip()
        if line.endswith(":"):
            current_category = line[:-1]
        elif line:
            category = current_category if current_category else "Uncategorized"
            description, expense = line.split(":")
            data.append({"Date": date.today().strftime("%Y-%m-%d"), "Category": category, "Description": description, "Expense": expense})
    save_data(data)

    console.print("\nExpenses read from file and added successfully! 🎉\n", style="bold green")











def get_weekly_summary(start_date, end_date):
    # Filter expenses for the specified week
    weekly_expenses = [expense for expense in data if start_date <= datetime.strptime(expense["Date"], "%Y-%m-%d").date() <= end_date]

    # Calculate the total expenses for each category
    category_totals = {}
    for expense in weekly_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        if category in category_totals:
            category_totals[category] += expense_amount
        else:
            category_totals[category] = expense_amount

    # Show the weekly summary
    console.clear()
    console.print(f"Weekly Summary ({start_date} to {end_date})\n", style="bold")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Category")
    table.add_column("Expense", justify="right")
    for category, total in category_totals.items():
        table.add_row(category, f"${total:.2f}")
    console.print(table)

    total_expenses = sum(category_totals.values())
    console.print(f"\nTotal expenses for {start_date} to {end_date}: ${total_expenses:.2f}\n", style="bold")

def select_week():
    console.clear()
    console.print("Select Weekly Summary\n", style="bold")
    start_date = console.input("Enter the start date (YYYY-MM-DD): ")
    end_date = console.input("Enter the end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError()

        get_weekly_summary(start_date, end_date)
    except ValueError:
        console.print("\nInvalid date range! Please enter valid dates in the format YYYY-MM-DD.\n", style="bold red")

    # Wait for the user to press Enter to go back to the menu
    input("\nPress Enter to go back to the menu...")
    menu()

























def menu():
    # Create a menu to select an option
    console.clear()
    console.print("Finance Expense Tracker\n", style="bold")
    console.print("Select an Option:\n", style="bold")
    console.print("1) Add an Expense  📝")
    console.print("2) Read Expenses from File  📄")
    console.print("3) View Expenses  👀")
    console.print("4) Monthly Summary  📅")
    console.print("5) Yearly Summary  📆")
    console.print("6) Daily Summary  📆")
    console.print("7) Weekly Summary  📆")
    console.print("8) Clear Expenses  🗑️")
    console.print("9) Exit  🚪\n")

    choice = console.input("Enter your choice: ")
    if choice == "1":
        add_expense()
    elif choice == "2":
        read_expenses_from_file()
    elif choice == "3":
        view_expenses()
    elif choice == "4":
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        year = console.input("Enter the year (e.g., 2022): ")
        get_monthly_summary(int(month), year)
    elif choice == "5":
        select_year()
    elif choice == "6":
        day = console.input("Enter the day as a number (e.g., 01, 02, etc.): ")
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        year = console.input("Enter the year (e.g., 2022): ")
        get_daily_summary(int(day), int(month), year)
    elif choice == "7":
        select_week()
    elif choice == "8":
        clear_expenses()
    elif choice == "9":
        console.print("\nThank you for using our finance tracker! Goodbye 👋\n")
        exit()
    else:
        console.print("\nInvalid choice! Please enter a number from 1 to 9.\n", style="bold red")

    # Wait for the user to press Enter to go back to the menu
    input("\nPress Enter to go back to the menu...")
    menu()

if __name__ == "__main__":
    menu()