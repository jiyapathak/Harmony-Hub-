#!/usr/bin/env python3
"""
Database Migration Script
Fixes missing columns in existing orders table
"""

import sqlite3
import os

def migrate_database():
    """Add missing columns to orders table if they don't exist"""
    
    db_path = 'music_store.db'
    
    if not os.path.exists(db_path):
        print("✓ Database will be created fresh on app startup")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check what columns exist in orders table
        cursor.execute("PRAGMA table_info(orders)")
        columns = {col[1] for col in cursor.fetchall()}
        
        print("Current orders table columns:")
        for col in columns:
            print(f"  ✓ {col}")
        
        # Add missing columns
        if 'payment_method' not in columns:
            print("\n→ Adding payment_method column...")
            cursor.execute('ALTER TABLE orders ADD COLUMN payment_method TEXT DEFAULT "cash_on_delivery"')
            print("  ✓ payment_method added")
        else:
            print("  ✓ payment_method already exists")
        
        if 'delivery_address' not in columns:
            print("\n→ Adding delivery_address column...")
            cursor.execute('ALTER TABLE orders ADD COLUMN delivery_address TEXT DEFAULT ""')
            print("  ✓ delivery_address added")
        else:
            print("  ✓ delivery_address already exists")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Database migration successful!")
        print("\nUpdated orders table columns:")
        
        # Show updated columns
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(orders)")
        for col in cursor.fetchall():
            print(f"  ✓ {col[1]}")
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        print("\nAlternative: Delete music_store.db and restart the app")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE MIGRATION SCRIPT")
    print("=" * 50)
    print()
    
    success = migrate_database()
    
    if success:
        print("\nYou can now run: python app.py")
    else:
        print("\nFix the issue above or delete music_store.db")
