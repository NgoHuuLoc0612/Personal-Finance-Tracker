# main.py
"""
Personal Finance Tracker - Main Application
A comprehensive tool for tracking income, expenses, and financial goals
"""

import sys
import os
from datetime import datetime
from transaction_manager import TransactionManager
from category_manager import CategoryManager
from budget_manager import BudgetManager
from report_generator import ReportGenerator
from data_visualizer import DataVisualizer

class PersonalFinanceTracker:
    def __init__(self):
        self.transaction_manager = TransactionManager()
        self.category_manager = CategoryManager()
        self.budget_manager = BudgetManager()
        self.report_generator = ReportGenerator(self.transaction_manager)
        self.data_visualizer = DataVisualizer(self.transaction_manager)
        
    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "="*50)
        print("       PERSONAL FINANCE TRACKER")
        print("="*50)
        print("1.  Add Transaction")
        print("2.  View Transactions")
        print("3.  Edit Transaction")
        print("4.  Delete Transaction")
        print("5.  Add Category")
        print("6.  View Categories")
        print("7.  Set Budget")
        print("8.  View Budget Status")
        print("9.  Generate Monthly Report")
        print("10. Generate Yearly Report")
        print("11. View Spending Charts")
        print("12. View Income vs Expense Chart")
        print("13. View Budget vs Actual Chart")
        print("14. Export Data")
        print("15. Import Data")
        print("0.  Exit")
        print("="*50)
        
    def add_transaction(self):
        """Add a new transaction"""
        print("\n--- Add New Transaction ---")
        try:
            transaction_type = input("Type (income/expense): ").lower().strip()
            if transaction_type not in ['income', 'expense']:
                print("Invalid transaction type. Please enter 'income' or 'expense'.")
                return
                
            amount = float(input("Amount: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
                
            description = input("Description: ").strip()
            if not description:
                print("Description cannot be empty.")
                return
                
            # Show available categories
            categories = self.category_manager.get_categories_by_type(transaction_type)
            if not categories:
                print(f"No {transaction_type} categories available. Please add a category first.")
                return
                
            print(f"\nAvailable {transaction_type} categories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
                
            try:
                choice = int(input("Select category number: ")) - 1
                if 0 <= choice < len(categories):
                    category = categories[choice]
                else:
                    print("Invalid category selection.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return
                
            date_input = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_input:
                try:
                    date = datetime.strptime(date_input, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Using today's date.")
                    date = datetime.now().date()
            else:
                date = datetime.now().date()
                
            transaction_id = self.transaction_manager.add_transaction(
                transaction_type, amount, description, category, date
            )
            print(f"Transaction added successfully! ID: {transaction_id}")
            
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
        except Exception as e:
            print(f"Error adding transaction: {e}")
            
    def view_transactions(self):
        """View transactions with filtering options"""
        print("\n--- View Transactions ---")
        print("1. All transactions")
        print("2. Filter by type")
        print("3. Filter by category")
        print("4. Filter by date range")
        
        try:
            choice = int(input("Select option: "))
            transactions = []
            
            if choice == 1:
                transactions = self.transaction_manager.get_all_transactions()
            elif choice == 2:
                transaction_type = input("Type (income/expense): ").lower().strip()
                transactions = self.transaction_manager.get_transactions_by_type(transaction_type)
            elif choice == 3:
                category = input("Category: ").strip()
                transactions = self.transaction_manager.get_transactions_by_category(category)
            elif choice == 4:
                start_date = input("Start date (YYYY-MM-DD): ")
                end_date = input("End date (YYYY-MM-DD): ")
                try:
                    start = datetime.strptime(start_date, "%Y-%m-%d").date()
                    end = datetime.strptime(end_date, "%Y-%m-%d").date()
                    transactions = self.transaction_manager.get_transactions_by_date_range(start, end)
                except ValueError:
                    print("Invalid date format.")
                    return
            else:
                print("Invalid choice.")
                return
                
            if transactions:
                print(f"\n{'ID':<5} {'Date':<12} {'Type':<8} {'Amount':<10} {'Category':<15} {'Description'}")
                print("-" * 75)
                for t in transactions:
                    print(f"{t['id']:<5} {t['date']:<12} {t['type']:<8} ${t['amount']:<9.2f} {t['category']:<15} {t['description']}")
            else:
                print("No transactions found.")
                
        except ValueError:
            print("Invalid input.")
            
    def edit_transaction(self):
        """Edit an existing transaction"""
        print("\n--- Edit Transaction ---")
        try:
            transaction_id = int(input("Enter transaction ID to edit: "))
            transaction = self.transaction_manager.get_transaction_by_id(transaction_id)
            
            if not transaction:
                print("Transaction not found.")
                return
                
            print(f"\nCurrent transaction:")
            print(f"Type: {transaction['type']}")
            print(f"Amount: ${transaction['amount']}")
            print(f"Description: {transaction['description']}")
            print(f"Category: {transaction['category']}")
            print(f"Date: {transaction['date']}")
            
            print("\nEnter new values (press Enter to keep current value):")
            
            # Get new values
            new_type = input(f"Type ({transaction['type']}): ").strip().lower()
            if not new_type:
                new_type = transaction['type']
            elif new_type not in ['income', 'expense']:
                print("Invalid transaction type.")
                return
                
            new_amount_input = input(f"Amount ({transaction['amount']}): ").strip()
            if new_amount_input:
                try:
                    new_amount = float(new_amount_input)
                    if new_amount <= 0:
                        print("Amount must be positive.")
                        return
                except ValueError:
                    print("Invalid amount.")
                    return
            else:
                new_amount = transaction['amount']
                
            new_description = input(f"Description ({transaction['description']}): ").strip()
            if not new_description:
                new_description = transaction['description']
                
            # Show categories for the type
            categories = self.category_manager.get_categories_by_type(new_type)
            if categories:
                print(f"\nAvailable {new_type} categories:")
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                    
                category_input = input(f"Select category number (current: {transaction['category']}): ").strip()
                if category_input:
                    try:
                        choice = int(category_input) - 1
                        if 0 <= choice < len(categories):
                            new_category = categories[choice]
                        else:
                            print("Invalid category selection.")
                            return
                    except ValueError:
                        print("Invalid input.")
                        return
                else:
                    new_category = transaction['category']
            else:
                new_category = transaction['category']
                
            new_date_input = input(f"Date ({transaction['date']}): ").strip()
            if new_date_input:
                try:
                    new_date = datetime.strptime(new_date_input, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format.")
                    return
            else:
                new_date = datetime.strptime(transaction['date'], "%Y-%m-%d").date()
                
            # Update transaction
            success = self.transaction_manager.update_transaction(
                transaction_id, new_type, new_amount, new_description, new_category, new_date
            )
            
            if success:
                print("Transaction updated successfully!")
            else:
                print("Failed to update transaction.")
                
        except ValueError:
            print("Invalid transaction ID.")
        except Exception as e:
            print(f"Error editing transaction: {e}")
            
    def delete_transaction(self):
        """Delete a transaction"""
        print("\n--- Delete Transaction ---")
        try:
            transaction_id = int(input("Enter transaction ID to delete: "))
            transaction = self.transaction_manager.get_transaction_by_id(transaction_id)
            
            if not transaction:
                print("Transaction not found.")
                return
                
            print(f"\nTransaction to delete:")
            print(f"Type: {transaction['type']}")
            print(f"Amount: ${transaction['amount']}")
            print(f"Description: {transaction['description']}")
            print(f"Category: {transaction['category']}")
            print(f"Date: {transaction['date']}")
            
            confirm = input("\nAre you sure you want to delete this transaction? (y/N): ").lower()
            if confirm == 'y':
                success = self.transaction_manager.delete_transaction(transaction_id)
                if success:
                    print("Transaction deleted successfully!")
                else:
                    print("Failed to delete transaction.")
            else:
                print("Transaction deletion cancelled.")
                
        except ValueError:
            print("Invalid transaction ID.")
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            
    def add_category(self):
        """Add a new category"""
        print("\n--- Add New Category ---")
        try:
            category_type = input("Category type (income/expense): ").lower().strip()
            if category_type not in ['income', 'expense']:
                print("Invalid category type. Please enter 'income' or 'expense'.")
                return
                
            name = input("Category name: ").strip()
            if not name:
                print("Category name cannot be empty.")
                return
                
            description = input("Description (optional): ").strip()
            
            success = self.category_manager.add_category(category_type, name, description)
            if success:
                print("Category added successfully!")
            else:
                print("Category already exists or failed to add.")
                
        except Exception as e:
            print(f"Error adding category: {e}")
            
    def view_categories(self):
        """View all categories"""
        print("\n--- Categories ---")
        income_categories = self.category_manager.get_categories_by_type('income')
        expense_categories = self.category_manager.get_categories_by_type('expense')
        
        print("\nIncome Categories:")
        if income_categories:
            for i, category in enumerate(income_categories, 1):
                print(f"{i}. {category}")
        else:
            print("No income categories.")
            
        print("\nExpense Categories:")
        if expense_categories:
            for i, category in enumerate(expense_categories, 1):
                print(f"{i}. {category}")
        else:
            print("No expense categories.")
            
    def set_budget(self):
        """Set budget for a category"""
        print("\n--- Set Budget ---")
        try:
            categories = self.category_manager.get_categories_by_type('expense')
            if not categories:
                print("No expense categories available. Please add expense categories first.")
                return
                
            print("Available expense categories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
                
            choice = int(input("Select category number: ")) - 1
            if not (0 <= choice < len(categories)):
                print("Invalid category selection.")
                return
                
            category = categories[choice]
            amount = float(input("Budget amount: $"))
            if amount <= 0:
                print("Budget amount must be positive.")
                return
                
            period = input("Period (monthly/yearly): ").lower().strip()
            if period not in ['monthly', 'yearly']:
                print("Invalid period. Please enter 'monthly' or 'yearly'.")
                return
                
            success = self.budget_manager.set_budget(category, amount, period)
            if success:
                print("Budget set successfully!")
            else:
                print("Failed to set budget.")
                
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error setting budget: {e}")
            
    def view_budget_status(self):
        """View budget status"""
        print("\n--- Budget Status ---")
        budgets = self.budget_manager.get_all_budgets()
        
        if not budgets:
            print("No budgets set.")
            return
            
        current_date = datetime.now().date()
        
        for budget in budgets:
            category = budget['category']
            budget_amount = budget['amount']
            period = budget['period']
            
            # Calculate spent amount based on period
            if period == 'monthly':
                start_date = current_date.replace(day=1)
                if current_date.month == 12:
                    end_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                else:
                    end_date = current_date.replace(month=current_date.month + 1, day=1)
            else:  # yearly
                start_date = current_date.replace(month=1, day=1)
                end_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                
            spent_amount = self.transaction_manager.get_total_by_category_and_date_range(
                category, start_date, end_date
            )
            
            remaining = budget_amount - spent_amount
            percentage = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
            
            print(f"\nCategory: {category}")
            print(f"Period: {period.title()}")
            print(f"Budget: ${budget_amount:.2f}")
            print(f"Spent: ${spent_amount:.2f}")
            print(f"Remaining: ${remaining:.2f}")
            print(f"Used: {percentage:.1f}%")
            
            if percentage > 100:
                print("⚠️  OVER BUDGET!")
            elif percentage > 80:
                print("⚠️  Approaching budget limit")
            else:
                print("✅ Within budget")
                
    def generate_monthly_report(self):
        """Generate monthly report"""
        print("\n--- Monthly Report ---")
        try:
            year = int(input("Year (YYYY): "))
            month = int(input("Month (1-12): "))
            
            if not (1 <= month <= 12):
                print("Invalid month.")
                return
                
            report = self.report_generator.generate_monthly_report(year, month)
            print(report)
            
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error generating report: {e}")
            
    def generate_yearly_report(self):
        """Generate yearly report"""
        print("\n--- Yearly Report ---")
        try:
            year = int(input("Year (YYYY): "))
            report = self.report_generator.generate_yearly_report(year)
            print(report)
            
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error generating report: {e}")
            
    def view_spending_charts(self):
        """Display spending charts"""
        print("\n--- Spending Charts ---")
        print("1. Current month spending by category")
        print("2. Last 6 months spending trend")
        print("3. Yearly spending by category")
        
        try:
            choice = int(input("Select chart type: "))
            
            if choice == 1:
                self.data_visualizer.plot_monthly_spending_by_category()
            elif choice == 2:
                self.data_visualizer.plot_spending_trend()
            elif choice == 3:
                year = int(input("Enter year (YYYY): "))
                self.data_visualizer.plot_yearly_spending_by_category(year)
            else:
                print("Invalid choice.")
                
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error displaying charts: {e}")
            
    def view_income_vs_expense_chart(self):
        """Display income vs expense chart"""
        print("\n--- Income vs Expense Chart ---")
        try:
            months = int(input("Number of months to display (1-12): "))
            if not (1 <= months <= 12):
                print("Invalid number of months.")
                return
                
            self.data_visualizer.plot_income_vs_expense(months)
            
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error displaying chart: {e}")
            
    def view_budget_vs_actual_chart(self):
        """Display budget vs actual spending chart"""
        print("\n--- Budget vs Actual Chart ---")
        try:
            self.data_visualizer.plot_budget_vs_actual(self.budget_manager)
        except Exception as e:
            print(f"Error displaying chart: {e}")
            
    def export_data(self):
        """Export data to CSV"""
        print("\n--- Export Data ---")
        try:
            filename = input("Enter filename (without extension): ").strip()
            if not filename:
                filename = f"finance_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
            success = self.transaction_manager.export_to_csv(f"{filename}.csv")
            if success:
                print(f"Data exported successfully to {filename}.csv")
            else:
                print("Failed to export data.")
                
        except Exception as e:
            print(f"Error exporting data: {e}")
            
    def import_data(self):
        """Import data from CSV"""
        print("\n--- Import Data ---")
        try:
            filename = input("Enter CSV filename: ").strip()
            if not filename:
                print("Filename cannot be empty.")
                return
                
            if not filename.endswith('.csv'):
                filename += '.csv'
                
            if not os.path.exists(filename):
                print(f"File {filename} not found.")
                return
                
            success = self.transaction_manager.import_from_csv(filename)
            if success:
                print("Data imported successfully!")
            else:
                print("Failed to import data.")
                
        except Exception as e:
            print(f"Error importing data: {e}")
            
    def run(self):
        """Run the main application loop"""
        print("Welcome to Personal Finance Tracker!")
        
        # Initialize with default categories if none exist
        if not self.category_manager.get_categories_by_type('income'):
            default_income_categories = ['Salary', 'Freelance', 'Investment', 'Other Income']
            for category in default_income_categories:
                self.category_manager.add_category('income', category, f'Default {category.lower()} category')
                
        if not self.category_manager.get_categories_by_type('expense'):
            default_expense_categories = ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Healthcare', 'Shopping', 'Other Expenses']
            for category in default_expense_categories:
                self.category_manager.add_category('expense', category, f'Default {category.lower()} category')
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '0':
                    print("Thank you for using Personal Finance Tracker!")
                    break
                elif choice == '1':
                    self.add_transaction()
                elif choice == '2':
                    self.view_transactions()
                elif choice == '3':
                    self.edit_transaction()
                elif choice == '4':
                    self.delete_transaction()
                elif choice == '5':
                    self.add_category()
                elif choice == '6':
                    self.view_categories()
                elif choice == '7':
                    self.set_budget()
                elif choice == '8':
                    self.view_budget_status()
                elif choice == '9':
                    self.generate_monthly_report()
                elif choice == '10':
                    self.generate_yearly_report()
                elif choice == '11':
                    self.view_spending_charts()
                elif choice == '12':
                    self.view_income_vs_expense_chart()
                elif choice == '13':
                    self.view_budget_vs_actual_chart()
                elif choice == '14':
                    self.export_data()
                elif choice == '15':
                    self.import_data()
                else:
                    print("Invalid choice. Please try again.")
                    
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = PersonalFinanceTracker()
    app.run()