import mysql.connector
from mysql.connector import Error

def test_sk_database():
    """Test SK Youth Portal Database"""
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
        
        # Test 1: Check database exists
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()['DATABASE()']
        print(f"✅ Connected to database: {db_name}")
        
        # Test 2: List all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n📋 Database Tables:")
        print("-" * 30)
        for table in tables:
            table_name = list(table.values())[0]
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"• {table_name:25} | {count:3} records")
        
        # Test 3: Test user credentials
        print("\n👥 Testing User Accounts:")
        print("-" * 30)
        
        test_users = [
            ("admin@sk.ph", "admin123"),
            ("youth@example.com", "youth123"),
            ("yes@example.com", "123")
        ]
        
        for email, password in test_users:
            query = """
                SELECT id, name, email, role, status, youth_id 
                FROM users 
                WHERE email = %s AND password = SHA2(%s, 256)
            """
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
            if user:
                print(f"✅ {user['role'].upper()}: {user['email']}")
                print(f"   Name: {user['name']}")
                print(f"   Youth ID: {user['youth_id']}")
                print(f"   Status: {user['status']}")
            else:
                print(f"❌ {email} - Invalid credentials")
            print("-" * 30)
        
        # Test 4: Check sample data
        print("\n📊 Sample Data Check:")
        print("-" * 30)
        
        # Check events
        cursor.execute("SELECT COUNT(*) as count FROM events")
        events_count = cursor.fetchone()['count']
        print(f"Events: {events_count} (Sample: 5)")
        
        # Check opportunities
        cursor.execute("SELECT COUNT(*) as count FROM opportunities")
        opp_count = cursor.fetchone()['count']
        print(f"Opportunities: {opp_count} (Sample: 4)")
        
        # Check users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()['count']
        print(f"Users: {users_count} (Sample: 3)")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 50)
        print("✅ SK Youth Portal Database Test Complete!")
        
    except Error as e:
        print(f"❌ Database Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL is running in XAMPP")
        print("2. Check if database 'sk_youth_portal' exists")
        print("3. Import sk_youth_portal.sql if needed")

if __name__ == "__main__":
    test_sk_database()