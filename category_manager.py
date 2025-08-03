# category_manager.py
"""
Category Manager Module
Handles category-related operations for organizing transactions
"""

import sqlite3
from typing import List, Optional

class CategoryManager:
    def __init__(self, db_path: str = "finance_tracker.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the database and create categories table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(type, name)
                )
            ''')
            conn.commit()
            
    def add_category(self, category_type: str, name: str, description: str = "") -> bool:
        """Add a new category"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO categories (type, name, description)
                    VALUES (?, ?, ?)
                ''', (category_type, name, description))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Category already exists
            return False
        except Exception as e:
            print(f"Error adding category: {e}")
            return False
            
    def get_all_categories(self) -> List[dict]:
        """Get all categories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, name, description
                FROM categories
                ORDER BY type, name
            ''')
            
            categories = []
            for row in cursor.fetchall():
                categories.append({
                    'id': row[0],
                    'type': row[1],
                    'name': row[2],
                    'description': row[3]
                })
            return categories
            
    def get_categories_by_type(self, category_type: str) -> List[str]:
        """Get category names filtered by type"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name
                FROM categories
                WHERE type = ?
                ORDER BY name
            ''', (category_type,))
            
            return [row[0] for row in cursor.fetchall()]
            
    def get_category_by_name(self, name: str) -> Optional[dict]:
        """Get a specific category by name"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, type, name, description
                FROM categories
                WHERE name = ?
            ''', (name,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'type': row[1],
                    'name': row[2],
                    'description': row[3]
                }
            return None
            
    def update_category(self, category_id: int, name: str, description: str = "") -> bool:
        """Update an existing category"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE categories
                    SET name = ?, description = ?
                    WHERE id = ?
                ''', (name, description, category_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            # Category name already exists for this type
            return False
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
            
    def delete_category(self, category_id: int) -> bool:
        """Delete a category (only if not used in transactions)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if category is used in transactions
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM transactions t
                    JOIN categories c ON t.category = c.name
                    WHERE c.id = ?
                ''', (category_id,))
                
                if cursor.fetchone()[0] > 0:
                    print("Cannot delete category: it is used in existing transactions.")
                    return False
                    
                # Delete category
                cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
            
    def category_exists(self, category_type: str, name: str) -> bool:
        """Check if a category exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*)
                FROM categories
                WHERE type = ? AND name = ?
            ''', (category_type, name))
            
            return cursor.fetchone()[0] > 0