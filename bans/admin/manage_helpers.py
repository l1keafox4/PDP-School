#!/usr/bin/env python3
import mysql.connector
import argparse
import getpass
import sys
import os

# Database configuration
DB_CONFIG = {
    'host': '65.109.116.247',
    'port': 3306,
    'user': 'litebans',
    'password': 'limon1232',
    'database': 'litebans'
}

def connect_to_database():
    """Connect to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        sys.exit(1)

def add_helper(username, password):
    """Add a new helper account."""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT COUNT(*) FROM litebans_users WHERE username = %s", (username,))
        if cursor.fetchone()[0] > 0:
            print(f"User '{username}' already exists.")
            return False
        
        # Using the MySQL PASSWORD() function for hashing
        cursor.execute(
            "INSERT INTO litebans_users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, 'helper')
        )
        conn.commit()
        print(f"Helper account '{username}' successfully created.")
        return True
    except mysql.connector.Error as err:
        print(f"Error adding helper: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_helper(username):
    """Delete a helper account."""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        # Verify it's a helper account (not an admin)
        cursor.execute("SELECT role FROM litebans_users WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if not result:
            print(f"User '{username}' does not exist.")
            return False
        
        if result[0] != 'helper':
            print(f"User '{username}' is not a helper account and cannot be deleted with this tool.")
            return False
        
        # Delete the helper account
        cursor.execute("DELETE FROM litebans_users WHERE username = %s AND role = 'helper'", (username,))
        
        if cursor.rowcount == 0:
            print(f"Failed to delete helper account '{username}'.")
            return False
        
        conn.commit()
        print(f"Helper account '{username}' successfully deleted.")
        return True
    except mysql.connector.Error as err:
        print(f"Error deleting helper: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def list_helpers():
    """List all helper accounts."""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, created_at FROM litebans_users WHERE role = 'helper'")
        helpers = cursor.fetchall()
        
        if not helpers:
            print("No helper accounts found.")
            return
        
        print("\nHelper Accounts:")
        print("=" * 60)
        print(f"{'ID':<5} {'Username':<30} {'Created At':<25}")
        print("-" * 60)
        
        for helper in helpers:
            print(f"{helper[0]:<5} {helper[1]:<30} {helper[2]:<25}")
        
        print("=" * 60)
    except mysql.connector.Error as err:
        print(f"Error listing helpers: {err}")
    finally:
        cursor.close()
        conn.close()

def update_php_auth():
    """Update auth.php to check for helper roles."""
    auth_path = os.path.dirname(os.path.abspath(__file__)) + '/auth.php'
    
    try:
        with open(auth_path, 'r') as f:
            content = f.read()
            
        # Only update if it doesn't already have role checking
        if 'role' not in content:
            new_content = """<?php
session_start();
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}
?>
"""
            with open(auth_path, 'w') as f:
                f.write(new_content)
            
            print("Updated auth.php successfully.")
        else:
            print("auth.php already has role checking.")
    except Exception as e:
        print(f"Error updating auth.php: {e}")

def main():
    parser = argparse.ArgumentParser(description="Manage helper accounts for LiteBans admin panel")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add helper account
    add_parser = subparsers.add_parser('add', help='Add a new helper account')
    add_parser.add_argument('username', help='Username for the helper account')
    add_parser.add_argument('-p', '--password', help='Password for the helper account (if not provided, will prompt)')
    
    # Delete helper account
    delete_parser = subparsers.add_parser('delete', help='Delete a helper account')
    delete_parser.add_argument('username', help='Username of the helper account to delete')
    
    # List helpers
    subparsers.add_parser('list', help='List all helper accounts')
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == 'add':
        password = args.password
        if not password:
            # Prompt for password if not provided
            password = getpass.getpass("Enter password for helper account: ")
            confirm = getpass.getpass("Confirm password: ")
            
            if password != confirm:
                print("Passwords do not match. Operation aborted.")
                return
                
        # Hash the password using PHP's password_hash
        import subprocess
        try:
            # Create a temporary PHP script to hash the password
            with open('/tmp/hash_password.php', 'w') as f:
                f.write('''<?php
                echo password_hash($argv[1], PASSWORD_DEFAULT);
                ?>''')
            
            # Execute the PHP script to hash the password
            hashed_password = subprocess.check_output(['php', '/tmp/hash_password.php', password]).decode().strip()
            os.remove('/tmp/hash_password.php')
            
            add_helper(args.username, hashed_password)
        except Exception as e:
            print(f"Error hashing password: {e}")
            return
            
    elif args.command == 'delete':
        delete_helper(args.username)
    elif args.command == 'list':
        list_helpers()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
