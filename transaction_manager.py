# transaction_manager.py
"""
Transaction Manager Module
Handles all transaction-related operations including CRUD operations and data persistence
"""

import sqlite3
import csv
from datetime import datetime, date
from typing import List, Dict, Optional

class TransactionManager:
    def __init__(self, db_path: str = "finance_tracker.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    amount REAL NOT NULL CHECK (amount > 0),
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            
    def add_transaction(self, transaction_type: str, amount: float, description: str, 
                       category: str, transaction_date: date) -> int:
        """Add a new transaction and return its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (type, amount, description, category, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction_type, amount, description, category, transaction_date.isoformat()))
            conn.commit()
            return cursor.lastrowid
            
    def get_all_transactions(self) -> List[Dict]:
        """Get all transactions ordered by date (newest first)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, amount, description, category, date
                FROM transactions
                ORDER BY date DESC, id DESC
            ''')
            
            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'category': row[4],
                    'date': row[5]
                })
            return transactions
            
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict]:
        """Get a specific transaction by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, amount, description, category, date
                FROM transactions
                WHERE id = ?
            ''', (transaction_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'category': row[4],
                    'date': row[5]
                }
            return None
            
    def get_transactions_by_type(self, transaction_type: str) -> List[Dict]:
        """Get transactions filtered by type"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, amount, description, category, date
                FROM transactions
                WHERE type = ?
                ORDER BY date DESC, id DESC
            ''', (transaction_type,))
            
            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'category': row[4],
                    'date': row[5]
                })
            return transactions
            
    def get_transactions_by_category(self, category: str) -> List[Dict]:
        """Get transactions filtered by category"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, amount, description, category, date
                FROM transactions
                WHERE category = ?
                ORDER BY date DESC, id DESC
            ''', (category,))
            
            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'category': row[4],
                    'date': row[5]
                })
            return transactions
            
    def get_transactions_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """Get transactions within a date range"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, amount, description, category, date
                FROM transactions
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC, id DESC
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'category': row[4],
                    'date': row[5]
                })
            return transactions
            
    def update_transaction(self, transaction_id: int, transaction_type: str, amount: float,
                          description: str, category: str, transaction_date: date) -> bool:
        """Update an existing transaction"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE transactions
                SET type = ?, amount = ?, description = ?, category = ?, date = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (transaction_type, amount, description, category, 
                  transaction_date.isoformat(), transaction_id))
            conn.commit()
            return cursor.rowcount > 0
            
    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
            conn.commit()
            return cursor.rowcount > 0
            
    def get_total_by_type(self, transaction_type: str) -> float:
        """Get total amount for a specific transaction type"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE type = ?
            ''', (transaction_type,))
            return cursor.fetchone()[0]
            
    def get_total_by_category(self, category: str) -> float:
        """Get total amount for a specific category"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE category = ?
            ''', (category,))
            return cursor.fetchone()[0]
            
    def get_total_by_category_and_date_range(self, category: str, start_date: date, end_date: date) -> float:
        """Get total amount for a category within a date range"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE category = ? AND date BETWEEN ? AND ?
            ''', (category, start_date.isoformat(), end_date.isoformat()))
            return cursor.fetchone()[0]
            
    def get_monthly_totals(self, year: int, month: int) -> Dict[str, float]:
        """Get monthly totals for income and expenses"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT type, COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE date >= ? AND date < ?
                GROUP BY type
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            totals = {'income': 0.0, 'expense': 0.0}
            for row in cursor.fetchall():
                totals[row[0]] = row[1]
            return totals
            
    def get_yearly_totals(self, year: int) -> Dict[str, float]:
        """Get yearly totals for income and expenses"""
        start_date = date(year, 1, 1)
        end_date = date(year + 1, 1, 1)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT type, COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE date >= ? AND date < ?
                GROUP BY type
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            totals = {'income': 0.0, 'expense': 0.0}
            for row in cursor.fetchall():
                totals[row[0]] = row[1]
            return totals
            
    def get_category_totals_for_period(self, start_date: date, end_date: date, 
                                     transaction_type: str = None) -> Dict[str, float]:
        """Get category totals for a specific period"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if transaction_type:
                cursor.execute('''
                    SELECT category, COALESCE(SUM(amount), 0)
                    FROM transactions
                    WHERE date BETWEEN ? AND ? AND type = ?
                    GROUP BY category
                    ORDER BY SUM(amount) DESC
                ''', (start_date.isoformat(), end_date.isoformat(), transaction_type))
            else:
                cursor.execute('''
                    SELECT category, COALESCE(SUM(amount), 0)
                    FROM transactions
                    WHERE date BETWEEN ? AND ?
                    GROUP BY category
                    ORDER BY SUM(amount) DESC
                ''', (start_date.isoformat(), end_date.isoformat()))
            
            return dict(cursor.fetchall())
            
    def get_monthly_data_for_chart(self, months: int) -> List[Dict]:
        """Get monthly data for charts"""
        data = []
        current_date = datetime.now().date()
        
        for i in range(months):
            if i == 0:
                year = current_date.year
                month = current_date.month
            else:
                # Calculate previous months
                month = current_date.month - i
                year = current_date.year
                
                while month <= 0:
                    month += 12
                    year -= 1
                    
            totals = self.get_monthly_totals(year, month)
            data.append({
                'year': year,
                'month': month,
                'month_name': datetime(year, month, 1).strftime('%B %Y'),
                'income': totals['income'],
                'expense': totals['expense'],
                'net': totals['income'] - totals['expense']
            })
            
        return list(reversed(data))  # Return in chronological order
        
    def export_to_csv(self, filename: str) -> bool:
        """Export all transactions to CSV file"""
        try:
            transactions = self.get_all_transactions()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'type', 'amount', 'description', 'category', 'date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for transaction in transactions:
                    writer.writerow(transaction)
                    
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
            
    def import_from_csv(self, filename: str) -> bool:
        """Import transactions from CSV file"""
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                imported_count = 0
                for row in reader:
                    try:
                        # Validate required fields
                        if not all(key in row for key in ['type', 'amount', 'description', 'category', 'date']):
                            continue
                            
                        transaction_type = row['type'].lower().strip()
                        if transaction_type not in ['income', 'expense']:
                            continue
                            
                        amount = float(row['amount'])
                        if amount <= 0:
                            continue
                            
                        description = row['description'].strip()
                        if not description:
                            continue
                            
                        category = row['category'].strip()
                        if not category:
                            continue
                            
                        transaction_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                        
                        # Add transaction
                        self.add_transaction(transaction_type, amount, description, category, transaction_date)
                        imported_count += 1
                        
                    except (ValueError, KeyError):
                        continue  # Skip invalid rows
                        
                print(f"Successfully imported {imported_count} transactions.")
                return imported_count > 0
                
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return False
            
    def get_transaction_statistics(self) -> Dict:
        """Get basic statistics about transactions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total transactions
            cursor.execute('SELECT COUNT(*) FROM transactions')
            total_transactions = cursor.fetchone()[0]
            
            # Total income and expenses
            cursor.execute('''
                SELECT type, COUNT(*), COALESCE(SUM(amount), 0), COALESCE(AVG(amount), 0)
                FROM transactions
                GROUP BY type
            ''')
            
            stats = {
                'total_transactions': total_transactions,
                'income': {'count': 0, 'total': 0.0, 'average': 0.0},
                'expense': {'count': 0, 'total': 0.0, 'average': 0.0}
            }
            
            for row in cursor.fetchall():
                transaction_type = row[0]
                stats[transaction_type] = {
                    'count': row[1],
                    'total': row[2],
                    'average': row[3]
                }
                
            # Calculate net worth
            stats['net_worth'] = stats['income']['total'] - stats['expense']['total']
            
            return stats