#!/usr/bin/env python3
"""
WARNING: This code contains intentional security vulnerabilities for SAST testing.
DO NOT use this code in production.
"""

import os
import subprocess
import sqlite3
import hashlib
import pickle
from flask import Flask, request

app = Flask(__name__)

# ISSUE 1: Hardcoded AWS credentials (CWE-798)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ISSUE 2: SQL Injection (CWE-89)
@app.route('/user')
def get_user():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    # Direct string formatting - VULNERABLE
    query = f"SELECT * FROM users WHERE name = '{username}'"
    return str(conn.execute(query).fetchall())

# ISSUE 3: Command Injection (CWE-78)
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Shell command injection - VULNERABLE
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return output

# ISSUE 4: Weak password hashing (CWE-328)
def store_password(password):
    # Using MD5 for passwords - VULNERABLE
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed

# ISSUE 5: Path Traversal (CWE-22)
@app.route('/file')
def read_file():
    filename = request.args.get('name')
    # No path validation - VULNERABLE
    with open(f"/app/data/{filename}", 'r') as f:
        return f.read()

# ISSUE 6: Code Injection with eval (CWE-95)
@app.route('/calc')
def calculate():
    expr = request.args.get('expression')
    # Using eval on user input - VULNERABLE
    result = eval(expr)
    return str(result)

if __name__ == '__main__':
    # ISSUE 7: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
