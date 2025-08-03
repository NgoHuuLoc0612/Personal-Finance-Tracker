# budget_manager.py
"""
Budget Manager Module
Handles budget creation, monitoring, and tracking
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import datetime, date

class BudgetManager:
    def __init__(self, db_path: str = "finance_tracker.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the database and create budgets table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK (amount > 0),
                    period TEXT NOT NULL CHECK (period IN ('monthly', 'yearly')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(category, period)
                )
            ''')
            conn.commit()
            
    def set_budget(self, category: str, amount: float, period: str) -> bool:
        """Set or update a budget for a category"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if budget already exists
                cursor.execute('''
                    SELECT id FROM budgets
                    WHERE category = ? AND period = ?
                ''', (category, period))
                
                existing_budget = cursor.fetchone()
                
                if existing_budget:
                    # Update existing budget
                    cursor.execute('''
                        UPDATE budgets
                        SET amount = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE category = ? AND period = ?
                    ''', (amount, category, period))
                else:
                    # Create new budget
                    cursor.execute('''
                        INSERT INTO budgets (category, amount, period)
                        VALUES (?, ?, ?)
                    ''', (category, amount, period))
                    
                conn.commit()
                return True
        except Exception as e:
            print(f"Error setting budget: {e}")
            return False
            
    def get_budget(self, category: str, period: str) -> Optional[Dict]:
        """Get a specific budget"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, category, amount, period, created_at, updated_at
                FROM budgets
                WHERE category = ? AND period = ?
            ''', (category, period))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'category': row[1],
                    'amount': row[2],
                    'period': row[3],
                    'created_at': row[4],
                    'updated_at': row[5]
                }
            return None
            
    def get_all_budgets(self) -> List[Dict]:
        """Get all budgets"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, category, amount, period, created_at, updated_at
                FROM budgets
                ORDER BY category, period
            ''')
            
            budgets = []
            for row in cursor.fetchall():
                budgets.append({
                    'id': row[0],
                    'category': row[1],
                    'amount': row[2],
                    'period': row[3],
                    'created_at': row[4],
                    'updated_at': row[5]
                })
            return budgets
            
    def get_budgets_by_period(self, period: str) -> List[Dict]:
        """Get budgets filtered by period"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, category, amount, period, created_at, updated_at
                FROM budgets
                WHERE period = ?
                ORDER BY category
            ''', (period,))
            
            budgets = []
            for row in cursor.fetchall():
                budgets.append({
                    'id': row[0],
                    'category': row[1],
                    'amount': row[2],
                    'period': row[3],
                    'created_at': row[4],
                    'updated_at': row[5]
                })
            return budgets
            
    def delete_budget(self, budget_id: int) -> bool:
        """Delete a budget"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting budget: {e}")
            return False
            
    def delete_budget_by_category_and_period(self, category: str, period: str) -> bool:
        """Delete a budget by category and period"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM budgets
                    WHERE category = ? AND period = ?
                ''', (category, period))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting budget: {e}")
            return False
            
    def get_budget_status(self, category: str, period: str, 
                         transaction_manager) -> Optional[Dict]:
        """Get budget status including spent amount and remaining budget"""
        budget = self.get_budget(category, period)
        if not budget:
            return None
            
        current_date = datetime.now().date()
        
        # Calculate date range based on period
        if period == 'monthly':
            start_date = current_date.replace(day=1)
            if current_date.month == 12:
                end_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                end_date = current_date.replace(month=current_date.month + 1, day=1)
        else:  # yearly
            start_date = current_date.replace(month=1, day=1)
            end_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            
        # Get spent amount from transaction manager
        spent_amount = transaction_manager.get_total_by_category_and_date_range(
            category, start_date, end_date
        )
        
        budget_amount = budget['amount']
        remaining = budget_amount - spent_amount
        percentage_used = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
        
        return {
            'budget': budget,
            'spent_amount': spent_amount,
            'remaining_amount': remaining,
            'percentage_used': percentage_used,
            'is_over_budget': spent_amount > budget_amount,
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat()
        }
        
    def get_all_budget_statuses(self, transaction_manager) -> List[Dict]:
        """Get status for all budgets"""
        budgets = self.get_all_budgets()
        statuses = []
        
        for budget in budgets:
            status = self.get_budget_status(
                budget['category'], 
                budget['period'], 
                transaction_manager
            )
            if status:
                statuses.append(status)
                
        return statuses
        
    def get_budget_alerts(self, transaction_manager, 
                         warning_threshold: float = 80.0) -> List[Dict]:
        """Get budget alerts for categories approaching or exceeding budget limits"""
        alerts = []
        statuses = self.get_all_budget_statuses(transaction_manager)
        
        for status in statuses:
            percentage_used = status['percentage_used']
            category = status['budget']['category']
            period = status['budget']['period']
            
            if percentage_used >= 100:
                alerts.append({
                    'type': 'over_budget',
                    'category': category,
                    'period': period,
                    'percentage_used': percentage_used,
                    'message': f"OVER BUDGET: {category} ({period}) - {percentage_used:.1f}% used"
                })
            elif percentage_used >= warning_threshold:
                alerts.append({
                    'type': 'approaching_limit',
                    'category': category,
                    'period': period,
                    'percentage_used': percentage_used,
                    'message': f"WARNING: {category} ({period}) - {percentage_used:.1f}% used"
                })
                
        return alerts
        
    def calculate_recommended_budget(self, category: str, transaction_manager,
                                   months_to_analyze: int = 6) -> Optional[float]:
        """Calculate recommended budget based on historical spending"""
        try:
            current_date = datetime.now().date()
            
            # Calculate start date for analysis
            year = current_date.year
            month = current_date.month - months_to_analyze
            
            while month <= 0:
                month += 12
                year -= 1
                
            start_date = date(year, month, 1)
            end_date = current_date
            
            # Get total spending in the period
            total_spent = transaction_manager.get_total_by_category_and_date_range(
                category, start_date, end_date
            )
            
            if total_spent == 0:
                return None
                
            # Calculate average monthly spending
            average_monthly = total_spent / months_to_analyze
            
            # Add 10% buffer for safety
            recommended_monthly = average_monthly * 1.1
            
            return recommended_monthly
            
        except Exception as e:
            print(f"Error calculating recommended budget: {e}")
            return None