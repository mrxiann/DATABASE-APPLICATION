import mysql.connector
from mysql.connector import Error

def test_sk_database():
    print("🔍 Testing SK Youth Portal Database")
    print("=" * 50)
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sk_youth_portal"
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Test 1: Check all users
        print("👥 ALL User Accounts in Database:")
        print("-" * 50)
        cursor.execute("SELECT id, name, email, role, status, youth_id FROM users ORDER BY role, id")
        all_users = cursor.fetchall()
        
        for user in all_users:
            print(f"ID: {user['id']}")
            print(f"  Name: {user['name']}")
            print(f"  Email: {user['email']}")
            print(f"  Role: {user['role']}")
            print(f"  Youth ID: {user['youth_id']}")
            print(f"  Status: {user['status']}")
            print("-" * 30)
        
        # Test 2: Test login with correct credentials
        print("\n🔐 Testing Login Credentials:")
        print("-" * 50)
        
        # Test credentials - use emails from your actual database
        test_credentials = [
            ("admin@sk.ph", "admin123"),
            ("youth1@example.com", "youth123"),
            ("youth2@example.com", "youth123"),
            ("youth3@example.com", "youth123"),
            ("youth4@example.com", "youth123"),
            ("youth5@example.com", "youth123"),
        ]
        
        for email, password in test_credentials:
            # Since passwords are SHA-256 hashed, we need to hash the input
            import hashlib
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            query = """
                SELECT id, name, email, role, status, youth_id 
                FROM users 
                WHERE email = %s AND password = %s
            """
            cursor.execute(query, (email, hashed_password))
            user = cursor.fetchone()
            
            if user:
                print(f"✅ SUCCESS: {user['email']}")
                print(f"   Name: {user['name']}")
                print(f"   Role: {user['role']}")
                print(f"   User ID: {user['id']}")
            else:
                # Let's check what hash is actually stored
                cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
                stored_hash = cursor.fetchone()
                if stored_hash:
                    print(f"❌ FAILED: {email}")
                    print(f"   Input hash: {hashed_password[:20]}...")
                    print(f"   Stored hash: {stored_hash['password'][:20]}...")
                    print(f"   Hashes match: {hashed_password == stored_hash['password']}")
                else:
                    print(f"❌ User not found: {email}")
            print("-" * 30)
        
        # Test 3: Verify password hashes
        print("\n🔑 Password Verification:")
        print("-" * 50)
        
        # Get all users with their password hashes
        cursor.execute("SELECT email, password FROM users")
        users_with_passwords = cursor.fetchall()
        
        for user in users_with_passwords:
            email = user['email']
            stored_hash = user['password']
            print(f"{email:25} | {stored_hash[:32]}...")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 50)
        print("✅ SK Youth Portal Database Test Complete!")
        
    except Error as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    test_sk_database()