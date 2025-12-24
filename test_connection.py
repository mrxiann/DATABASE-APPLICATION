import mysql.connector
from mysql.connector import Error

def test_credentials():
    """Test the created user accounts"""
    users = [
        {"email": "admin@sk.ph", "password": "admin123", "role": "admin"},
        {"email": "youth1@example.com", "password": "youth123", "role": "youth"}
    ]
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sk_youth_portal"
        )
        
        cursor = connection.cursor(dictionary=True)
        
        print("🔍 Testing User Credentials:")
        print("=" * 40)
        
        for user in users:
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (user['email'], user['password']))
            result = cursor.fetchone()
            
            if result:
                print(f"✅ {user['role'].upper()}: {user['email']}")
                print(f"   Name: {result['full_name']}")
                print(f"   Role: {result['role']}")
                print(f"   Status: {result['status']}")
            else:
                print(f"❌ {user['role'].upper()}: {user['email']} - NOT FOUND")
            print("-" * 40)
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Database Error: {e}")

def count_records():
    """Count records in each table"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sk_youth_portal"
        )
        
        cursor = connection.cursor()
        tables = ['users', 'youth_profiles', 'programs', 'enrollments', 'attendance', 'assessments']
        
        print("\n📊 Database Statistics:")
        print("=" * 40)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:20} | {count:4} records")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_credentials()
    count_records()