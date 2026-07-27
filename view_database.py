import sqlite3
import pandas as pd

def view_database():
    # Connect to database
    conn = sqlite3.connect('foodbridge.db')
    
    print("=== FOODBRIDGE DATABASE ===\n")
    
    # View Donors
    print("DONORS:")
    donors = pd.read_sql_query("SELECT * FROM donor", conn)
    print(donors)
    print(f"Total Donors: {len(donors)}\n")
    
    # View NGOs
    print("NGOs:")
    ngos = pd.read_sql_query("SELECT * FROM ngo", conn)
    print(ngos)
    print(f"Total NGOs: {len(ngos)}\n")
    
    # View Donations
    print("DONATIONS:")
    donations = pd.read_sql_query("SELECT * FROM donation", conn)
    print(donations)
    print(f"Total Donations: {len(donations)}\n")
    
    conn.close()

if __name__ == "__main__":
    view_database()