import csv
from datetime import date
from rich.console import Console
from rich.table import Table
from datetime import datetime
from datetime import timedelta
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

console = Console()
console.clear()
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





def write_daily_summary_to_md():
    # Get today's date
    today = date.today().strftime("%Y-%m-%d")

    # Filter expenses for today
    daily_expenses = [expense for expense in data if expense["Date"] == today]

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

    # Write the daily summary to a markdown file
    with open("finances/daily.md", "w", encoding='utf-8') as file:
        file.write(f"# {today} Daily Summary 💼\n\n")
        for category, total in category_totals.items():
            file.write(f"## {category} 📁\n\n")
            file.write("| Description | Amount 💰|\n")
            file.write("| --- | --- |\n")
            for description, amount in descriptions[category]:
                file.write(f"| {description} | ${amount:.2f} |\n")
            file.write(f"\n**Total**: ${total:.2f} 💵\n\n")

        total_expenses = sum(category_totals.values())
        file.write(f"\n# Total expenses for {today}: ${total_expenses:.2f} 💸\n")







def write_monthly_summary_to_md():
    # Get current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Filter expenses for the current month
    monthly_expenses = [expense for expense in data if expense["Date"].startswith(f"{current_year}-{current_month:02d}")]

    # Calculate the total expenses for each category and collect descriptions
    category_totals = {}
    descriptions = {}
    for expense in monthly_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        description = expense["Description"]
        if category in category_totals:
            category_totals[category] += expense_amount
            descriptions[category].append((description, expense_amount))
        else:
            category_totals[category] = expense_amount
            descriptions[category] = [(description, expense_amount)]

    # Write the monthly summary to a markdown file
    with open("finances/monthly.md", "w", encoding='utf-8') as file:
        file.write(f"# {current_month}/{current_year} Monthly Summary 💼\n\n")
        for category, total in category_totals.items():
            file.write(f"## {category} 📁\n\n")
            file.write("| Description | Amount 💰|\n")
            file.write("| --- | --- |\n")
            for description, amount in descriptions[category]:
                file.write(f"| {description} | ${amount:.2f} |\n")
            file.write(f"\n**Total**: ${total:.2f} 💵\n\n")

        total_expenses = sum(category_totals.values())
        file.write(f"\n# Total expenses for {current_month}/{current_year}: ${total_expenses:.2f} 💸\n")










def write_weekly_summary_to_md():
    # Get today's date
    today = date.today()

    # Find the last Monday
    last_monday = today - timedelta(days=today.weekday())

    # Filter expenses for the current week
    weekly_expenses = [expense for expense in data if last_monday <= datetime.strptime(expense["Date"], "%Y-%m-%d").date() <= today]

    # Calculate the total expenses for each category and collect descriptions
    category_totals = {}
    descriptions = {}
    for expense in weekly_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        description = expense["Description"]
        if category in category_totals:
            category_totals[category] += expense_amount
            descriptions[category].append((description, expense_amount))
        else:
            category_totals[category] = expense_amount
            descriptions[category] = [(description, expense_amount)]

    # Write the weekly summary to a markdown file
    with open("finances/weekly.md", "w", encoding='utf-8') as file:
        file.write(f"# Weekly Summary ({last_monday} to {today}) 💼\n\n")
        for category, total in category_totals.items():
            file.write(f"## {category} 📁\n\n")
            file.write("| Description | Amount 💰|\n")
            file.write("| --- | --- |\n")
            for description, amount in descriptions[category]:
                file.write(f"| {description} | ${amount:.2f} |\n")
            file.write(f"\n**Total**: ${total:.2f} 💵\n\n")

        total_expenses = sum(category_totals.values())
        file.write(f"\n# Total expenses for {last_monday} to {today}: ${total_expenses:.2f} 💸\n")










def write_yearly_summary_to_md():
    # Get current year
    current_year = datetime.now().year

    # Filter expenses for the current year
    yearly_expenses = [expense for expense in data if expense["Date"].startswith(f"{current_year}")]

    # Calculate the total expenses for each category
    category_totals = {}
    for expense in yearly_expenses:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        if category in category_totals:
            category_totals[category] += expense_amount
        else:
            category_totals[category] = expense_amount

    # Write the yearly summary to a markdown file
    with open("finances/yearly.md", "w", encoding='utf-8') as file:
        file.write(f"# {current_year} Yearly Summary 💼\n\n")
        for category, total in category_totals.items():
            file.write(f"## {category} 📁\n\n")
            file.write(f"\n**Total**: ${total:.2f} 💵\n\n")

        total_expenses = sum(category_totals.values())
        file.write(f"\n# Total expenses for {current_year}: ${total_expenses:.2f} 💸\n")



















def menu():
    write_daily_summary_to_md()
    write_monthly_summary_to_md()
    write_weekly_summary_to_md()
    write_yearly_summary_to_md()
    clear_screen()
    console.clear()
    console.print("Finance Expense Tracker\n\n", style="bold")






    finances_data = []
    try:
        with open("finances.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                finances_data.append(row)
    except FileNotFoundError:
        pass

    total_expenses = sum(float(expense["Expense"]) for expense in finances_data)
    categories = list(set(expense["Category"] for expense in finances_data))

    console.print("🎯 Expenses by category:\n")
    for category in categories:
        category_expenses = sum(float(expense["Expense"]) for expense in finances_data if expense["Category"] == category)
        console.print(f"{category}: {category_expenses}\n")

    budget = 0.00
    daily_budget = 0.00
    with open("expenses.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Category"] == "Budget":
                budget = float(row["Expense"])
            elif row["Category"] == "Daily budget":
                daily_budget = float(row["Expense"])

    expenses = 0.00
    with open("expenses.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            expenses += float(row["Expense"])

    console.print(f"\n💵 Total spent: {total_expenses:.2f}")

    remaining_budget = budget - total_expenses
    console.print(f"✅ Budget remaining: {remaining_budget:.2f}")

    today_expenses = sum(float(expense["Expense"]) for expense in finances_data if expense["Date"] == date.today().strftime("%Y-%m-%d"))

    # Check if remaining budget is less than or equal to 0
    if remaining_budget <= 0:
        daily_budget_today = 0.00
    else:
        daily_budget_today = daily_budget - today_expenses

    console.print(f"👉 Budget per day: {daily_budget_today:.2f}\n\n")
    
    
    
    
    # Calculate the total expenses for each category
    category_totals = {}
    for expense in data:
        category = expense["Category"]
        expense_amount = float(expense["Expense"])
        if category in category_totals:
            category_totals[category] += expense_amount
        else:
            category_totals[category] = expense_amount

    # Calculate total expenses and remaining budget
    total_expenses = sum(category_totals.values())
    remaining_budget = budget - total_expenses

    # Write the total summary to a markdown file
    with open("finances/Total.md", "w", encoding='utf-8') as file:
        file.write("# Total Summary 💼\n\n\n\n")
        for category, total in category_totals.items():
            file.write(f"## {category} 📁\n\n")
            file.write(f"**Total**: ${total:.2f} 💵\n\n")

        file.write(f"\n\n\n\n# Total spent: ${total_expenses:.2f} 💸\n")
        file.write(f"# Budget remaining: ${remaining_budget:.2f} ✅\n")    
        file.write(f"# 👉 Budget per day: {daily_budget_today:.2f}\n\n")
    
    
    
    

    console.print("Select an Option:\n", style="bold")

    console.print("1) 📝  Add an Expense  ")
    console.print("2) 📄  Read Expenses from File  ")
    console.print("3) 👀  View Expenses  ")
    console.print("4) 📆  Daily Summary  ")
    console.print("5) 📆  Weekly Summary  ")
    console.print("6) 📆  Monthly Summary  ")
    console.print("7) 📆  Yearly Summary  ")
    console.print("8) 🗑️   Clear Expenses  ")
    console.print("9) 🚪  Exit  \n\n")


    choice = console.input("Enter your choice: ")
    if choice == "1":
        add_expense()
    elif choice == "2":
        read_expenses_from_file()
    elif choice == "3":
        view_expenses()
    elif choice == "4":
        day = console.input("Enter the day as a number (e.g., 01, 02, etc.): ")
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        year = console.input("Enter the year (e.g., 2022): ")
        get_daily_summary(int(day), int(month), year)
    elif choice == "5":
        select_week()
    elif choice == "6":
        month = console.input("Enter the month as a number (e.g., 01 for January, 02 for February, etc.): ")
        year = console.input("Enter the year (e.g., 2022): ")
        get_monthly_summary(int(month), year)
    elif choice == "7":
        select_year()
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
