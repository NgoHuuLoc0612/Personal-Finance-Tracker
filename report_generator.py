# report_generator.py
"""
Report Generator Module
Generates comprehensive financial reports and summaries
"""

from datetime import datetime, date
from typing import Dict, List
import calendar

class ReportGenerator:
    def __init__(self, transaction_manager):
        self.transaction_manager = transaction_manager
        
    def generate_monthly_report(self, year: int, month: int) -> str:
        """Generate a comprehensive monthly financial report"""
        try:
            # Get monthly totals
            totals = self.transaction_manager.get_monthly_totals(year, month)
            
            # Get date range for the month
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            
            # Get category breakdowns
            income_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'income'
            )
            expense_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            )
            
            # Get transactions for the month
            monthly_transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )
            
            # Build report
            month_name = calendar.month_name[month]
            report = []
            report.append("="*60)
            report.append(f"           MONTHLY FINANCIAL REPORT")
            report.append(f"              {month_name} {year}")
            report.append("="*60)
            
            # Summary section
            report.append("\n📊 FINANCIAL SUMMARY")
            report.append("-" * 30)
            report.append(f"Total Income:     ${totals['income']:>12,.2f}")
            report.append(f"Total Expenses:   ${totals['expense']:>12,.2f}")
            report.append(f"Net Income:       ${totals['income'] - totals['expense']:>12,.2f}")
            
            if totals['expense'] > 0:
                savings_rate = ((totals['income'] - totals['expense']) / totals['income']) * 100
                report.append(f"Savings Rate:     {savings_rate:>12.1f}%")
            
            # Income breakdown
            if income_categories:
                report.append("\n💰 INCOME BREAKDOWN")
                report.append("-" * 30)
                for category, amount in income_categories.items():
                    percentage = (amount / totals['income']) * 100 if totals['income'] > 0 else 0
                    report.append(f"{category:<20} ${amount:>10,.2f} ({percentage:>5.1f}%)")
            
            # Expense breakdown
            if expense_categories:
                report.append("\n💸 EXPENSE BREAKDOWN")
                report.append("-" * 30)
                for category, amount in expense_categories.items():
                    percentage = (amount / totals['expense']) * 100 if totals['expense'] > 0 else 0
                    report.append(f"{category:<20} ${amount:>10,.2f} ({percentage:>5.1f}%)")
            
            # Transaction statistics
            report.append("\n📈 TRANSACTION STATISTICS")
            report.append("-" * 30)
            report.append(f"Total Transactions: {len(monthly_transactions)}")
            
            income_transactions = [t for t in monthly_transactions if t['type'] == 'income']
            expense_transactions = [t for t in monthly_transactions if t['type'] == 'expense']
            
            report.append(f"Income Transactions: {len(income_transactions)}")
            report.append(f"Expense Transactions: {len(expense_transactions)}")
            
            if income_transactions:
                avg_income = sum(t['amount'] for t in income_transactions) / len(income_transactions)
                report.append(f"Average Income Transaction: ${avg_income:.2f}")
                
            if expense_transactions:
                avg_expense = sum(t['amount'] for t in expense_transactions) / len(expense_transactions)
                report.append(f"Average Expense Transaction: ${avg_expense:.2f}")
            
            # Top expenses
            if expense_transactions:
                sorted_expenses = sorted(expense_transactions, key=lambda x: x['amount'], reverse=True)
                report.append("\n🔥 TOP 5 EXPENSES")
                report.append("-" * 30)
                for i, transaction in enumerate(sorted_expenses[:5], 1):
                    report.append(f"{i}. ${transaction['amount']:>8.2f} - {transaction['description']} ({transaction['category']})")
            
            # Month comparison (if previous month data exists)
            if month > 1:
                prev_month = month - 1
                prev_year = year
            else:
                prev_month = 12
                prev_year = year - 1
                
            prev_totals = self.transaction_manager.get_monthly_totals(prev_year, prev_month)
            
            if prev_totals['income'] > 0 or prev_totals['expense'] > 0:
                report.append(f"\n📊 COMPARISON WITH {calendar.month_name[prev_month]} {prev_year}")
                report.append("-" * 30)
                
                income_change = totals['income'] - prev_totals['income']
                expense_change = totals['expense'] - prev_totals['expense']
                
                income_symbol = "📈" if income_change > 0 else "📉" if income_change < 0 else "➡️"
                expense_symbol = "📈" if expense_change > 0 else "📉" if expense_change < 0 else "➡️"
                
                report.append(f"Income Change:    {income_symbol} ${income_change:>+10,.2f}")
                report.append(f"Expense Change:   {expense_symbol} ${expense_change:>+10,.2f}")
                
                if prev_totals['income'] > 0:
                    income_pct_change = (income_change / prev_totals['income']) * 100
                    report.append(f"Income % Change:  {income_pct_change:>+12.1f}%")
                    
                if prev_totals['expense'] > 0:
                    expense_pct_change = (expense_change / prev_totals['expense']) * 100
                    report.append(f"Expense % Change: {expense_pct_change:>+12.1f}%")
            
            report.append("\n" + "="*60)
            report.append(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("="*60)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"Error generating monthly report: {e}"
            
    def generate_yearly_report(self, year: int) -> str:
        """Generate a comprehensive yearly financial report"""
        try:
            # Get yearly totals
            totals = self.transaction_manager.get_yearly_totals(year)
            
            # Get date range for the year
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            
            # Get category breakdowns
            income_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'income'
            )
            expense_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            )
            
            # Get monthly data for trend analysis
            monthly_data = []
            for month in range(1, 13):
                month_totals = self.transaction_manager.get_monthly_totals(year, month)
                monthly_data.append({
                    'month': month,
                    'month_name': calendar.month_name[month],
                    'income': month_totals['income'],
                    'expense': month_totals['expense'],
                    'net': month_totals['income'] - month_totals['expense']
                })
            
            # Get all transactions for the year
            yearly_transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )
            
            # Build report
            report = []
            report.append("="*60)
            report.append(f"            YEARLY FINANCIAL REPORT")
            report.append(f"                   {year}")
            report.append("="*60)
            
            # Summary section
            report.append("\n📊 YEARLY SUMMARY")
            report.append("-" * 30)
            report.append(f"Total Income:     ${totals['income']:>12,.2f}")
            report.append(f"Total Expenses:   ${totals['expense']:>12,.2f}")
            report.append(f"Net Income:       ${totals['income'] - totals['expense']:>12,.2f}")
            
            if totals['expense'] > 0:
                savings_rate = ((totals['income'] - totals['expense']) / totals['income']) * 100
                report.append(f"Savings Rate:     {savings_rate:>12.1f}%")
            
            # Monthly averages
            report.append(f"Avg Monthly Income:  ${totals['income']/12:>9,.2f}")
            report.append(f"Avg Monthly Expense: ${totals['expense']/12:>9,.2f}")
            
            # Income breakdown
            if income_categories:
                report.append("\n💰 INCOME BREAKDOWN")
                report.append("-" * 30)
                for category, amount in income_categories.items():
                    percentage = (amount / totals['income']) * 100 if totals['income'] > 0 else 0
                    report.append(f"{category:<20} ${amount:>10,.2f} ({percentage:>5.1f}%)")
            
            # Expense breakdown
            if expense_categories:
                report.append("\n💸 EXPENSE BREAKDOWN")
                report.append("-" * 30)
                for category, amount in expense_categories.items():
                    percentage = (amount / totals['expense']) * 100 if totals['expense'] > 0 else 0
                    report.append(f"{category:<20} ${amount:>10,.2f} ({percentage:>5.1f}%)")
            
            # Monthly trends
            report.append("\n📈 MONTHLY TRENDS")
            report.append("-" * 50)
            report.append(f"{'Month':<12} {'Income':<12} {'Expenses':<12} {'Net':<12}")
            report.append("-" * 50)
            
            for month_data in monthly_data:
                report.append(f"{month_data['month_name']:<12} "
                            f"${month_data['income']:<11,.0f} "
                            f"${month_data['expense']:<11,.0f} "
                            f"${month_data['net']:<11,.0f}")
            
            # Best and worst months
            best_month = max(monthly_data, key=lambda x: x['net'])
            worst_month = min(monthly_data, key=lambda x: x['net'])
            highest_income_month = max(monthly_data, key=lambda x: x['income'])
            highest_expense_month = max(monthly_data, key=lambda x: x['expense'])
            
            report.append("\n🏆 MONTH HIGHLIGHTS")
            report.append("-" * 30)
            report.append(f"Best Net Income:      {best_month['month_name']} (${best_month['net']:,.2f})")
            report.append(f"Worst Net Income:     {worst_month['month_name']} (${worst_month['net']:,.2f})")
            report.append(f"Highest Income:       {highest_income_month['month_name']} (${highest_income_month['income']:,.2f})")
            report.append(f"Highest Expenses:     {highest_expense_month['month_name']} (${highest_expense_month['expense']:,.2f})")
            
            # Transaction statistics
            report.append("\n📈 TRANSACTION STATISTICS")
            report.append("-" * 30)
            report.append(f"Total Transactions: {len(yearly_transactions)}")
            
            income_transactions = [t for t in yearly_transactions if t['type'] == 'income']
            expense_transactions = [t for t in yearly_transactions if t['type'] == 'expense']
            
            report.append(f"Income Transactions: {len(income_transactions)}")
            report.append(f"Expense Transactions: {len(expense_transactions)}")
            
            if income_transactions:
                avg_income = sum(t['amount'] for t in income_transactions) / len(income_transactions)
                largest_income = max(income_transactions, key=lambda x: x['amount'])
                report.append(f"Average Income Transaction: ${avg_income:.2f}")
                report.append(f"Largest Income: ${largest_income['amount']:.2f} ({largest_income['description']})")
                
            if expense_transactions:
                avg_expense = sum(t['amount'] for t in expense_transactions) / len(expense_transactions)
                largest_expense = max(expense_transactions, key=lambda x: x['amount'])
                report.append(f"Average Expense Transaction: ${avg_expense:.2f}")
                report.append(f"Largest Expense: ${largest_expense['amount']:.2f} ({largest_expense['description']})")
            
            # Year comparison (if previous year data exists)
            prev_year_totals = self.transaction_manager.get_yearly_totals(year - 1)
            
            if prev_year_totals['income'] > 0 or prev_year_totals['expense'] > 0:
                report.append(f"\n📊 COMPARISON WITH {year - 1}")
                report.append("-" * 30)
                
                income_change = totals['income'] - prev_year_totals['income']
                expense_change = totals['expense'] - prev_year_totals['expense']
                
                income_symbol = "📈" if income_change > 0 else "📉" if income_change < 0 else "➡️"
                expense_symbol = "📈" if expense_change > 0 else "📉" if expense_change < 0 else "➡️"
                
                report.append(f"Income Change:    {income_symbol} ${income_change:>+10,.2f}")
                report.append(f"Expense Change:   {expense_symbol} ${expense_change:>+10,.2f}")
                
                if prev_year_totals['income'] > 0:
                    income_pct_change = (income_change / prev_year_totals['income']) * 100
                    report.append(f"Income % Change:  {income_pct_change:>+12.1f}%")
                    
                if prev_year_totals['expense'] > 0:
                    expense_pct_change = (expense_change / prev_year_totals['expense']) * 100
                    report.append(f"Expense % Change: {expense_pct_change:>+12.1f}%")
            
            report.append("\n" + "="*60)
            report.append(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("="*60)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"Error generating yearly report: {e}"
            
    def generate_category_report(self, category: str, start_date: date = None, 
                               end_date: date = None) -> str:
        """Generate a detailed report for a specific category"""
        try:
            if not start_date:
                # Default to current year
                current_date = datetime.now().date()
                start_date = date(current_date.year, 1, 1)
                end_date = current_date
            
            # Get transactions for the category in the date range
            transactions = self.transaction_manager.get_transactions_by_category(category)
            filtered_transactions = [
                t for t in transactions 
                if start_date <= datetime.strptime(t['date'], '%Y-%m-%d').date() <= end_date
            ]
            
            if not filtered_transactions:
                return f"No transactions found for category '{category}' in the specified period."
            
            # Calculate statistics
            total_amount = sum(t['amount'] for t in filtered_transactions)
            avg_amount = total_amount / len(filtered_transactions)
            min_amount = min(t['amount'] for t in filtered_transactions)
            max_amount = max(t['amount'] for t in filtered_transactions)
            
            # Build report
            report = []
            report.append("="*50)
            report.append(f"     CATEGORY REPORT: {category.upper()}")
            report.append(f"     {start_date} to {end_date}")
            report.append("="*50)
            
            report.append("\n📊 SUMMARY")
            report.append("-" * 20)
            report.append(f"Total Amount:    ${total_amount:>10,.2f}")
            report.append(f"Transactions:    {len(filtered_transactions):>10}")
            report.append(f"Average Amount:  ${avg_amount:>10,.2f}")
            report.append(f"Minimum Amount:  ${min_amount:>10,.2f}")
            report.append(f"Maximum Amount:  ${max_amount:>10,.2f}")
            
            # Recent transactions
            recent_transactions = sorted(filtered_transactions, 
                                       key=lambda x: x['date'], reverse=True)[:10]
            
            report.append("\n📝 RECENT TRANSACTIONS")
            report.append("-" * 50)
            report.append(f"{'Date':<12} {'Amount':<10} {'Description'}")
            report.append("-" * 50)
            
            for transaction in recent_transactions:
                report.append(f"{transaction['date']:<12} "
                            f"${transaction['amount']:<9.2f} "
                            f"{transaction['description']}")
            
            report.append("\n" + "="*50)
            report.append(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("="*50)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"Error generating category report: {e}"
            
    def generate_quick_summary(self) -> str:
        """Generate a quick financial summary"""
        try:
            current_date = datetime.now().date()
            current_month_totals = self.transaction_manager.get_monthly_totals(
                current_date.year, current_date.month
            )
            current_year_totals = self.transaction_manager.get_yearly_totals(current_date.year)
            
            # Get overall statistics
            stats = self.transaction_manager.get_transaction_statistics()
            
            report = []
            report.append("="*40)
            report.append("    QUICK FINANCIAL SUMMARY")
            report.append("="*40)
            
            report.append("\n📅 THIS MONTH")
            report.append("-" * 20)
            report.append(f"Income:    ${current_month_totals['income']:>10,.2f}")
            report.append(f"Expenses:  ${current_month_totals['expense']:>10,.2f}")
            report.append(f"Net:       ${current_month_totals['income'] - current_month_totals['expense']:>10,.2f}")
            
            report.append(f"\n📅 THIS YEAR ({current_date.year})")
            report.append("-" * 20)
            report.append(f"Income:    ${current_year_totals['income']:>10,.2f}")
            report.append(f"Expenses:  ${current_year_totals['expense']:>10,.2f}")
            report.append(f"Net:       ${current_year_totals['income'] - current_year_totals['expense']:>10,.2f}")
            
            report.append("\n📊 OVERALL STATISTICS")
            report.append("-" * 20)
            report.append(f"Total Transactions: {stats['total_transactions']}")
            report.append(f"Net Worth: ${stats['net_worth']:>10,.2f}")
            
            if stats['income']['count'] > 0:
                report.append(f"Avg Income: ${stats['income']['average']:>9,.2f}")
            if stats['expense']['count'] > 0:
                report.append(f"Avg Expense: ${stats['expense']['average']:>8,.2f}")
            
            return "\n".join(report)
            
        except Exception as e:
            return f"Error generating quick summary: {e}"