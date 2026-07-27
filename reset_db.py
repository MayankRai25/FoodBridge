#!/usr/bin/env python3
"""
Database reset script to recreate tables with password fields
"""
import os
from app import app, db

def reset_database():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        print("[OK] Dropped old tables")
        
        # Create new tables with password fields
        db.create_all()
        print("[OK] Created new database with password fields")
        print("[INFO] All users must now register again with passwords")

if __name__ == '__main__':
    reset_database()