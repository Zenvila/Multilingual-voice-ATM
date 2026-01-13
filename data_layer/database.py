"""
Database Layer - Mock SQLite database for ATM simulation.
Handles account data, balances, and transaction storage.
"""

import sqlite3
import os
import hashlib
from datetime import datetime

class Database:
    """Mock database for ATM simulation."""
    
    def __init__(self, db_path='atm_database.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                pin_hash TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table (for blockchain-style logging)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL,
                previous_hash TEXT,
                current_hash TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def initialize_sample_data(self):
        """Initialize sample accounts for testing."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM accounts')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Create sample accounts
        # PIN: 1234 (hashed)
        pin_hash_1234 = self.hash_pin('1234')
        # PIN: 5678 (hashed)
        pin_hash_5678 = self.hash_pin('5678')
        
        sample_accounts = [
            ('1234567890', pin_hash_1234, 100000.00),  # 100,000 PKR
            ('0987654321', pin_hash_5678, 50000.00),   # 50,000 PKR
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO accounts (account_number, pin_hash, balance)
            VALUES (?, ?, ?)
        ''', sample_accounts)
        
        conn.commit()
        conn.close()
        print("Sample accounts initialized:")
        print("Account: 1234567890, PIN: 1234, Balance: Rs. 100,000.00")
        print("Account: 0987654321, PIN: 5678, Balance: Rs. 50,000.00")
    
    def hash_pin(self, pin):
        """Hash PIN for storage (simple hash, not production-ready)."""
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def account_exists(self, account_number):
        """Check if account number exists."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_number FROM accounts WHERE account_number = ?
        ''', (account_number,))
        
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def verify_pin(self, account_number, pin):
        """Verify PIN against stored hash."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        pin_hash = self.hash_pin(pin)
        cursor.execute('''
            SELECT account_number FROM accounts
            WHERE account_number = ? AND pin_hash = ?
        ''', (account_number, pin_hash))
        
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def get_balance(self, account_number):
        """Get account balance."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT balance FROM accounts WHERE account_number = ?
        ''', (account_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
    
    def update_balance(self, account_number, new_balance):
        """Update account balance."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE accounts SET balance = ? WHERE account_number = ?
        ''', (new_balance, account_number))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def get_last_transaction_hash(self, account_number):
        """Get the hash of the last transaction for blockchain-style chaining."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT current_hash FROM transactions
            WHERE account_number = ?
            ORDER BY id DESC
            LIMIT 1
        ''', (account_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return '0' * 64  # Genesis hash
    
    def insert_transaction(self, account_number, transaction_type, amount, previous_hash, current_hash, data):
        """Insert a new transaction record."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions 
            (account_number, transaction_type, amount, previous_hash, current_hash, data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (account_number, transaction_type, amount, previous_hash, current_hash, data))
        
        conn.commit()
        conn.close()
    
    def get_transactions(self, account_number, limit=10):
        """Get recent transactions for an account."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT transaction_type, amount, timestamp, current_hash, previous_hash, data
            FROM transactions
            WHERE account_number = ?
            ORDER BY id DESC
            LIMIT ?
        ''', (account_number, limit))
        
        transactions = []
        for row in cursor.fetchall():
            transactions.append({
                'type': row[0],
                'amount': row[1],
                'timestamp': row[2],
                'current_hash': row[3],
                'previous_hash': row[4],
                'data': row[5]
            })
        
        conn.close()
        return transactions
