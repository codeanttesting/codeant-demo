import json
import csv
import requests
import sqlite3
from utils import validate_user_data, normalize_user_data

AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def load_user_data(source_url):
    response = requests.get(source_url, timeout=5)
    return response.json()

def save_to_database(users):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    ''')

    for user in users:
        cursor.execute("INSERT INTO users (id, name, email, phone) VALUES (?, ?, ?, ?)", (user['id'], user['name'], user['email'], user['phone']))
    
    conn.commit()
    conn.close()

def export_to_csv(users, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'email', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)

def main():
    # Load data 
    source_url = "https://api.codeant.com/users"
    raw_data = load_user_data(source_url)
    
    processed_users = []
    for user in raw_data:
        # Validate user data
        if validate_user_data(user):
            # Normalize user data
            normalized_user = normalize_user_data(user)
            processed_users.append(normalized_user)
    
    
    save_to_database(processed_users)
    
    # Export to CSV
    export_to_csv(processed_users, 'processed_users.csv')

if __name__ == "__main__":
    main()