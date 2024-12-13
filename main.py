import csv
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style

class BudgetTracker:
    def __init__(self):
        self.income = []
        self.expenses = []
        self.savings_goal = 0

    def add_income(self, source, amount):
        """Add income to the tracker."""
        self.income.append({'source': source, 'amount': amount})
        print(Fore.GREEN + f"Income from {source} of GHS {amount} added successfully!" + Style.RESET_ALL)

    def add_expense(self, category, amount, description=""):
        """Add expense to the tracker."""
        self.expenses.append({'category': category, 'amount': amount, 'description': description})
        print(Fore.RED + f"Expense of GHS {amount} in {category} added successfully!" + Style.RESET_ALL)

    def view_summary(self):
        """Display financial summary and breakdown."""
        total_income = sum(item['amount'] for item in self.income)
        total_expenses = sum(item['amount'] for item in self.expenses)
        savings = total_income - total_expenses

        summary = [
            ['Total Income', f"GHS {total_income}"],
            ['Total Expenses', f"GHS {total_expenses}"],
            ['Savings', f"GHS {savings}"]
        ]

        print(Fore.YELLOW + "\nFinancial Summary:" + Style.RESET_ALL)
        print(tabulate(summary, headers=["Category", "Amount"], tablefmt="grid"))
        print("\nCategory Breakdown:")

        categories = {}
        for expense in self.expenses:
            if expense['category'] in categories:
                categories[expense['category']] += expense['amount']
            else:
                categories[expense['category']] = expense['amount']

        for category, amount in categories.items():
            print(f"- {category}: GHS {amount}")

    def set_savings_goal(self, goal):
        """Set a savings goal."""
        self.savings_goal = goal
        print(Fore.CYAN + f"Savings goal of GHS {goal} set successfully!" + Style.RESET_ALL)

    def view_savings_progress(self):
        """Display savings progress."""
        total_income = sum(item['amount'] for item in self.income)
        total_expenses = sum(item['amount'] for item in self.expenses)
        actual_savings = total_income - total_expenses  
        
        # If savings exceed the goal, set remaining to 0
        remaining = max(self.savings_goal - actual_savings, 0)

        print(Fore.GREEN + "\nSavings Progress:" + Style.RESET_ALL)
        print(f"Current Savings: GHS {actual_savings}")
        print(f"Savings Goal: GHS {self.savings_goal}")
        print(f"Remaining Amount: GHS {remaining}")

        # If savings exceed goal, cap progress at 100%
        if actual_savings >= self.savings_goal:
            progress = 100
            remaining = 0  # No remaining amount when savings goal is met or exceeded
        else:
            progress = (actual_savings / self.savings_goal) * 100

        print(f"Savings Progress: [{'#' * int(progress // 5)}{'-' * (20 - int(progress // 5))}] {progress:.2f}% Complete")


    def save_to_csv(self, filename="budget_data.csv"):
        """Save income and expenses to a CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Type", "Description"])
            for income in self.income:
                writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Income", income['amount'], income['source'], ""])
            for expense in self.expenses:
                writer.writerow([datetime.now().strftime("%Y-%m-%d"), expense['category'], expense['amount'], "Expense", expense['description']])

        print(Fore.MAGENTA + f"Data saved to {filename}!" + Style.RESET_ALL)

def main():
    tracker = BudgetTracker()

    while True:
        print("\nWelcome to the Personal Budget Tracker!")
        print("Please select an option:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Set Savings Goal")
        print("5. View Savings Progress")
        print("6. Save Data to CSV")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            source = input("Enter source of income (e.g., Salary, Freelance): ")
            amount = float(input("Enter amount (GHS): "))
            tracker.add_income(source, amount)

        elif choice == "2":
            category = input("Enter category (e.g., Transport, Food, Utilities): ")
            amount = float(input("Enter amount (GHS): "))
            description = input("Enter description (optional): ")
            tracker.add_expense(category, amount, description)

        elif choice == "3":
            tracker.view_summary()

        elif choice == "4":
            goal = float(input("Enter your savings goal (GHS): "))
            tracker.set_savings_goal(goal)

        elif choice == "5":
            tracker.view_savings_progress()

        elif choice == "6":
            tracker.save_to_csv()

        elif choice == "7":
            print(Fore.RED + "Exiting the Personal Budget Tracker. Goodbye!" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid choice! Please enter a number between 1 and 7." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
