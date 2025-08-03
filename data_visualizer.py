# data_visualizer.py
"""
Data Visualizer Module
Creates charts and graphs for financial data visualization
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, date
import calendar
import numpy as np
from typing import Dict, List

# Set style for better-looking charts
plt.style.use('seaborn-v0_8')

class DataVisualizer:
    def __init__(self, transaction_manager):
        self.transaction_manager = transaction_manager
        
    def plot_monthly_spending_by_category(self, year: int = None, month: int = None):
        """Create a pie chart showing spending by category for a specific month"""
        try:
            current_date = datetime.now().date()
            if not year:
                year = current_date.year
            if not month:
                month = current_date.month
                
            # Get date range for the month
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            
            # Get expense categories for the month
            expense_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            )
            
            if not expense_categories:
                print("No expense data found for the specified month.")
                return
                
            # Prepare data for pie chart
            categories = list(expense_categories.keys())
            amounts = list(expense_categories.values())
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Custom colors
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            
            wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                            colors=colors, startangle=90)
            
            # Customize the chart
            ax.set_title(f'Spending by Category - {calendar.month_name[month]} {year}', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                
            # Add total spending text
            total_spending = sum(amounts)
            ax.text(0, -1.3, f'Total Spending: ${total_spending:,.2f}', 
                   ha='center', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating spending chart: {e}")
            
    def plot_spending_trend(self, months: int = 6):
        """Create a line chart showing spending trend over time"""
        try:
            # Get monthly data
            monthly_data = self.transaction_manager.get_monthly_data_for_chart(months)
            
            if not monthly_data:
                print("No data available for spending trend.")
                return
                
            # Prepare data
            month_names = [data['month_name'] for data in monthly_data]
            expenses = [data['expense'] for data in monthly_data]
            
            # Create line chart
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(month_names, expenses, marker='o', linewidth=2, markersize=8, color='#FF6B6B')
            ax.fill_between(month_names, expenses, alpha=0.3, color='#FF6B6B')
            
            # Customize the chart
            ax.set_title(f'Spending Trend - Last {months} Months', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Amount ($)', fontsize=12)
            
            # Format y-axis to show currency
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            
            # Add grid
            ax.grid(True, alpha=0.3)
            
            # Add trend line
            if len(expenses) > 1:
                z = np.polyfit(range(len(expenses)), expenses, 1)
                p = np.poly1d(z)
                ax.plot(month_names, p(range(len(expenses))), "--", alpha=0.8, color='red', 
                       label=f'Trend: {"📈 Increasing" if z[0] > 0 else "📉 Decreasing"}')
                ax.legend()
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating spending trend chart: {e}")
            
    def plot_yearly_spending_by_category(self, year: int):
        """Create a horizontal bar chart showing yearly spending by category"""
        try:
            # Get date range for the year
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            
            # Get expense categories for the year
            expense_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            )
            
            if not expense_categories:
                print(f"No expense data found for {year}.")
                return
                
            # Sort categories by amount (descending)
            sorted_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
            categories = [item[0] for item in sorted_categories]
            amounts = [item[1] for item in sorted_categories]
            
            # Create horizontal bar chart
            fig, ax = plt.subplots(figsize=(12, 8))
            
            bars = ax.barh(categories, amounts, color='#4ECDC4')
            
            # Customize the chart
            ax.set_title(f'Yearly Spending by Category - {year}', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Amount ($)', fontsize=12)
            ax.set_ylabel('Category', fontsize=12)
            
            # Format x-axis to show currency
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Add value labels on bars
            for i, (bar, amount) in enumerate(zip(bars, amounts)):
                ax.text(bar.get_width() + max(amounts) * 0.01, bar.get_y() + bar.get_height()/2, 
                       f'${amount:,.0f}', ha='left', va='center', fontweight='bold')
            
            # Add grid
            ax.grid(True, alpha=0.3, axis='x')
            
            # Calculate total and add it to the chart
            total_spending = sum(amounts)
            ax.text(0.02, 0.98, f'Total Spending: ${total_spending:,.2f}', 
                   transform=ax.transAxes, fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating yearly spending chart: {e}")
            
    def plot_income_vs_expense(self, months: int = 6):
        """Create a comparison chart of income vs expenses over time"""
        try:
            # Get monthly data
            monthly_data = self.transaction_manager.get_monthly_data_for_chart(months)
            
            if not monthly_data:
                print("No data available for income vs expense chart.")
                return
                
            # Prepare data
            month_names = [data['month_name'] for data in monthly_data]
            income_amounts = [data['income'] for data in monthly_data]
            expense_amounts = [data['expense'] for data in monthly_data]
            net_amounts = [data['net'] for data in monthly_data]
            
            # Create chart
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # Upper chart: Income vs Expenses
            x = np.arange(len(month_names))
            width = 0.35
            
            bars1 = ax1.bar(x - width/2, income_amounts, width, label='Income', color='#2ECC71', alpha=0.8)
            bars2 = ax1.bar(x + width/2, expense_amounts, width, label='Expenses', color='#E74C3C', alpha=0.8)
            
            ax1.set_title('Income vs Expenses Comparison', fontsize=16, fontweight='bold', pad=20)
            ax1.set_xlabel('Month', fontsize=12)
            ax1.set_ylabel('Amount ($)', fontsize=12)
            ax1.set_xticks(x)
            ax1.set_xticklabels(month_names, rotation=45)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Format y-axis
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax1.text(bar.get_x() + bar.get_width()/2., height + max(max(income_amounts), max(expense_amounts)) * 0.01,
                               f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            # Lower chart: Net Income (Income - Expenses)
            colors = ['#2ECC71' if net >= 0 else '#E74C3C' for net in net_amounts]
            bars3 = ax2.bar(month_names, net_amounts, color=colors, alpha=0.8)
            
            ax2.set_title('Net Income (Income - Expenses)', fontsize=16, fontweight='bold', pad=20)
            ax2.set_xlabel('Month', fontsize=12)
            ax2.set_ylabel('Net Amount ($)', fontsize=12)
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            ax2.grid(True, alpha=0.3)
            
            # Format y-axis
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Rotate x-axis labels
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            # Add value labels on bars
            for bar, net in zip(bars3, net_amounts):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., 
                        height + (abs(height) * 0.05 if height >= 0 else -abs(height) * 0.05),
                        f'${height:,.0f}', ha='center', 
                        va='bottom' if height >= 0 else 'top', fontsize=10)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating income vs expense chart: {e}")
            
    def plot_budget_vs_actual(self, budget_manager):
        """Create a chart comparing budgeted vs actual spending"""
        try:
            # Get all budget statuses
            budget_statuses = budget_manager.get_all_budget_statuses(self.transaction_manager)
            
            if not budget_statuses:
                print("No budget data available.")
                return
                
            # Prepare data
            categories = []
            budgeted_amounts = []
            actual_amounts = []
            
            for status in budget_statuses:
                categories.append(f"{status['budget']['category']}\n({status['budget']['period']})")
                budgeted_amounts.append(status['budget']['amount'])
                actual_amounts.append(status['spent_amount'])
            
            # Create chart
            fig, ax = plt.subplots(figsize=(12, 8))
            
            x = np.arange(len(categories))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, budgeted_amounts, width, label='Budgeted', 
                          color='#3498DB', alpha=0.8)
            bars2 = ax.bar(x + width/2, actual_amounts, width, label='Actual', 
                          color='#E74C3C', alpha=0.8)
            
            # Customize the chart
            ax.set_title('Budget vs Actual Spending', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Category', fontsize=12)
            ax.set_ylabel('Amount ($)', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(categories, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Format y-axis
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Add value labels on bars
            for bars, amounts in [(bars1, budgeted_amounts), (bars2, actual_amounts)]:
                for bar, amount in zip(bars, amounts):
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height + max(max(budgeted_amounts), max(actual_amounts)) * 0.01,
                               f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
            
            # Add over-budget indicators
            for i, status in enumerate(budget_statuses):
                if status['is_over_budget']:
                    ax.text(i, max(budgeted_amounts[i], actual_amounts[i]) + max(max(budgeted_amounts), max(actual_amounts)) * 0.1,
                           '⚠️ OVER', ha='center', va='bottom', fontsize=12, fontweight='bold', color='red')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating budget vs actual chart: {e}")
            
    def plot_category_trend(self, category: str, months: int = 12):
        """Create a line chart showing spending trend for a specific category"""
        try:
            current_date = datetime.now().date()
            monthly_amounts = []
            month_labels = []
            
            for i in range(months):
                # Calculate month and year
                month = current_date.month - i
                year = current_date.year
                
                while month <= 0:
                    month += 12
                    year -= 1
                    
                # Get category total for the month
                start_date = date(year, month, 1)
                last_day = calendar.monthrange(year, month)[1]
                end_date = date(year, month, last_day)
                
                amount = self.transaction_manager.get_total_by_category_and_date_range(
                    category, start_date, end_date
                )
                
                monthly_amounts.append(amount)
                month_labels.append(f"{calendar.month_abbr[month]} {year}")
            
            # Reverse to show chronological order
            monthly_amounts.reverse()
            month_labels.reverse()
            
            # Create chart
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(month_labels, monthly_amounts, marker='o', linewidth=2, 
                   markersize=8, color='#9B59B6')
            ax.fill_between(month_labels, monthly_amounts, alpha=0.3, color='#9B59B6')
            
            # Customize the chart
            ax.set_title(f'Spending Trend: {category}', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Amount ($)', fontsize=12)
            
            # Format y-axis
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Rotate x-axis labels
            plt.xticks(rotation=45)
            
            # Add grid
            ax.grid(True, alpha=0.3)
            
            # Calculate and show average
            avg_amount = sum(monthly_amounts) / len(monthly_amounts)
            ax.axhline(y=avg_amount, color='red', linestyle='--', alpha=0.7, 
                      label=f'Average: ${avg_amount:,.2f}')
            ax.legend()
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating category trend chart: {e}")
            
    def plot_financial_overview(self, months: int = 12):
        """Create a comprehensive financial overview dashboard"""
        try:
            # Get monthly data
            monthly_data = self.transaction_manager.get_monthly_data_for_chart(months)
            
            if not monthly_data:
                print("No data available for financial overview.")
                return
                
            # Prepare data
            month_names = [data['month_name'] for data in monthly_data]
            income_amounts = [data['income'] for data in monthly_data]
            expense_amounts = [data['expense'] for data in monthly_data]
            net_amounts = [data['net'] for data in monthly_data]
            
            # Create subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # Chart 1: Income vs Expenses line chart
            ax1.plot(month_names, income_amounts, marker='o', label='Income', color='#2ECC71', linewidth=2)
            ax1.plot(month_names, expense_amounts, marker='s', label='Expenses', color='#E74C3C', linewidth=2)
            ax1.set_title('Income vs Expenses Trend', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Amount ($)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # Chart 2: Net Income bar chart
            colors = ['#2ECC71' if net >= 0 else '#E74C3C' for net in net_amounts]
            ax2.bar(month_names, net_amounts, color=colors, alpha=0.8)
            ax2.set_title('Net Income by Month', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Net Amount ($)')
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            ax2.grid(True, alpha=0.3)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            # Chart 3: Current month spending by category (pie chart)
            current_date = datetime.now().date()
            start_date = current_date.replace(day=1)
            last_day = calendar.monthrange(current_date.year, current_date.month)[1]
            end_date = current_date.replace(day=last_day)
            
            current_month_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            )
            
            if current_month_categories:
                categories = list(current_month_categories.keys())
                amounts = list(current_month_categories.values())
                colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
                
                ax3.pie(amounts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
                ax3.set_title(f'Current Month Spending\n{calendar.month_name[current_date.month]} {current_date.year}', 
                             fontsize=14, fontweight='bold')
            else:
                ax3.text(0.5, 0.5, 'No spending data\nfor current month', 
                        ha='center', va='center', transform=ax3.transAxes, fontsize=12)
                ax3.set_title('Current Month Spending', fontsize=14, fontweight='bold')
            
            # Chart 4: Savings rate over time
            savings_rates = []
            for data in monthly_data:
                if data['income'] > 0:
                    savings_rate = ((data['income'] - data['expense']) / data['income']) * 100
                    savings_rates.append(savings_rate)
                else:
                    savings_rates.append(0)
            
            ax4.plot(month_names, savings_rates, marker='d', color='#F39C12', linewidth=2, markersize=6)
            ax4.fill_between(month_names, savings_rates, alpha=0.3, color='#F39C12')
            ax4.set_title('Savings Rate Trend', fontsize=14, fontweight='bold')
            ax4.set_ylabel('Savings Rate (%)')
            ax4.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            ax4.axhline(y=20, color='green', linestyle='--', alpha=0.7, label='Recommended 20%')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
            
            # Add main title
            fig.suptitle('Personal Finance Dashboard', fontsize=18, fontweight='bold', y=0.98)
            
            plt.tight_layout()
            plt.subplots_adjust(top=0.93)
            plt.show()
            
        except Exception as e:
            print(f"Error creating financial overview: {e}")
            
    def plot_expense_distribution(self, year: int = None):
        """Create a donut chart showing expense distribution"""
        try:
            current_date = datetime.now().date()
            if not year:
                year = current_date.year
                
            # Get yearly expense data
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            
            expense_categories = self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            )
            
            if not expense_categories:
                print(f"No expense data found for {year}.")
                return
                
            # Prepare data
            categories = list(expense_categories.keys())
            amounts = list(expense_categories.values())
            total_expenses = sum(amounts)
            
            # Create donut chart
            fig, ax = plt.subplots(figsize=(10, 10))
            
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                            colors=colors, startangle=90, pctdistance=0.85)
            
            # Create donut effect
            centre_circle = plt.Circle((0,0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
            
            # Add center text
            ax.text(0, 0, f'Total Expenses\n${total_expenses:,.2f}\n{year}', 
                   ha='center', va='center', fontsize=14, fontweight='bold')
            
            # Customize the chart
            ax.set_title(f'Expense Distribution - {year}', fontsize=16, fontweight='bold', pad=20)
            
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating expense distribution chart: {e}")
            
    def create_spending_heatmap(self, year: int = None):
        """Create a heatmap showing spending intensity by month and category"""
        try:
            current_date = datetime.now().date()
            if not year:
                year = current_date.year
                
            # Get all expense categories
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            all_categories = list(self.transaction_manager.get_category_totals_for_period(
                start_date, end_date, 'expense'
            ).keys())
            
            if not all_categories:
                print(f"No expense data found for {year}.")
                return
                
            # Create matrix of spending data
            spending_matrix = []
            month_names = []
            
            for month in range(1, 13):
                month_start = date(year, month, 1)
                last_day = calendar.monthrange(year, month)[1]
                month_end = date(year, month, last_day)
                
                month_categories = self.transaction_manager.get_category_totals_for_period(
                    month_start, month_end, 'expense'
                )
                
                month_row = []
                for category in all_categories:
                    amount = month_categories.get(category, 0)
                    month_row.append(amount)
                    
                spending_matrix.append(month_row)
                month_names.append(calendar.month_abbr[month])
            
            # Create heatmap
            fig, ax = plt.subplots(figsize=(12, 8))
            
            im = ax.imshow(spending_matrix, cmap='Reds', aspect='auto')
            
            # Set ticks and labels
            ax.set_xticks(np.arange(len(all_categories)))
            ax.set_yticks(np.arange(len(month_names)))
            ax.set_xticklabels(all_categories, rotation=45, ha='right')
            ax.set_yticklabels(month_names)
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('Spending Amount ($)', rotation=270, labelpad=20)
            
            # Add text annotations
            for i in range(len(month_names)):
                for j in range(len(all_categories)):
                    amount = spending_matrix[i][j]
                    if amount > 0:
                        text = ax.text(j, i, f'${amount:,.0f}', ha='center', va='center',
                                     color='white' if amount > np.max(spending_matrix) * 0.5 else 'black',
                                     fontsize=8, fontweight='bold')
            
            ax.set_title(f'Spending Heatmap - {year}', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Category', fontsize=12)
            ax.set_ylabel('Month', fontsize=12)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error creating spending heatmap: {e}")
            
    def save_chart_to_file(self, filename: str):
        """Save the current chart to a file"""
        try:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {filename}")
        except Exception as e:
            print(f"Error saving chart: {e}")