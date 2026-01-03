#!/usr/bin/env python3
"""
Database Reset Script
Use this if you want to completely reset the database with fresh sample data
"""

import os
import sqlite3
import shutil

def reset_database():
    """Backup old database and create a fresh one"""
    
    db_path = 'music_store.db'
    
    if os.path.exists(db_path):
        # Create backup
        backup_path = f'music_store.db.backup'
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backup created: {backup_path}")
        
        # Delete old database
        os.remove(db_path)
        print(f"✓ Old database deleted")
    
    print("\n✓ Fresh database will be created on next app startup")
    print("\nTo start with fresh data:")
    print("  1. Run: python app.py")
    print("  2. The database will auto-create with sample data")
    print("  3. Login with: admin / admin123")

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE RESET SCRIPT")
    print("=" * 50)
    print()
    
    response = input("Are you sure you want to reset the database? (yes/no): ").strip().lower()
    
    if response == 'yes':
        reset_database()
        print("\n✅ Database reset complete!")
    else:
        print("\n✓ Reset cancelled")
