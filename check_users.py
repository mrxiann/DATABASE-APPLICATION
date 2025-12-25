import mysql.connector
import hashlib

# Connect to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='sk_youth_portal'
)

cursor = conn.cursor(dictionary=True)

# Check all users
cursor.execute("SELECT id, name, email, role, status, password FROM users")
users = cursor.fetchall()

print("=" * 60)
print("ALL USERS IN DATABASE:")
print("=" * 60)
for user in users:
    print(f"ID: {user['id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user['role']}")
    print(f"Status: {user['status']}")
    print(f"Password hash: {user['password'][:20]}...")
    print("-" * 40)

cursor.close()
conn.close()

# Check what hash 'youth123' produces
hashed_youth = hashlib.sha256('youth123'.encode()).hexdigest()
print(f"\nHash for 'youth123': {hashed_youth}")