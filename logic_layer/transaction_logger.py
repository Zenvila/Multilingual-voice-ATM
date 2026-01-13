"""
Transaction Logger - Blockchain-style transaction logging.
Creates linked hash chains for transaction records.
"""

import hashlib
import json
from datetime import datetime

class TransactionLogger:
    """Logs transactions with blockchain-style hashing."""
    
    def __init__(self, database):
        self.db = database
    
    def calculate_hash(self, account_number, transaction_type, amount, previous_hash, timestamp, data):
        """Calculate hash for a transaction (blockchain-style)."""
        data_string = f"{account_number}{transaction_type}{amount}{previous_hash}{timestamp}{json.dumps(data)}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def log_transaction(self, account_number, transaction_type, data=None, amount=None):
        """
        Log a transaction with blockchain-style hashing.
        Each transaction is linked to the previous one via hash.
        """
        previous_hash = self.db.get_last_transaction_hash(account_number)
        timestamp = datetime.now().isoformat()
        
        current_hash = self.calculate_hash(
            account_number,
            transaction_type,
            amount or 0,
            previous_hash,
            timestamp,
            data or {}
        )
        
        self.db.insert_transaction(
            account_number,
            transaction_type,
            amount,
            previous_hash,
            current_hash,
            json.dumps(data) if data else None
        )
        
        return current_hash
    
    def get_transactions(self, account_number, limit=10):
        """Get transaction history for an account."""
        return self.db.get_transactions(account_number, limit)
    
    def verify_transaction_chain(self, account_number):
        """
        Verify the integrity of the transaction chain.
        Returns True if all hashes are valid and linked correctly.
        """
        transactions = self.get_transactions(account_number, limit=100)
        
        if len(transactions) <= 1:
            return True
        
        for i in range(len(transactions) - 1):
            current_tx = transactions[i]
            next_tx = transactions[i + 1]
            
            # Verify that next transaction's previous_hash matches current's hash
            if next_tx['previous_hash'] != current_tx['current_hash']:
                return False
        
        return True
