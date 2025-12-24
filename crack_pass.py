import hashlib
import itertools
import string

# Hashes that weren't found
missing_hashes = {
    "Youth User 2": "b4a6a2633526e349cf88d8e56203c21e806092014b61335d043ba41d9f2bcc47",
    "Youth User 3": "7db3628dc1a91163a3a3e03efa415c3f8433320118327febe5494745bbda7ca2",
    "Youth User 4": "38fd748d0ed88078fc24e02ed13766041b43a1b094c326c097da983927b57ad8",
    "Youth User 5": "7a723d195dcd9f5f11613909d104df77a4fc4864d0853302d1a5f070b82bd0e2"
}

def brute_force_simple():
    print("🔐 Brute Forcing Simple Passwords (4-6 chars)")
    print("=" * 50)
    
    # Characters to try (lowercase letters and digits)
    chars = string.ascii_lowercase + string.digits
    
    for length in range(4, 7):  # Try 4, 5, 6 character passwords
        print(f"\nTrying {length}-character passwords...")
        
        # Generate all combinations
        for combo in itertools.product(chars, repeat=length):
            password = ''.join(combo)
            hashed = hashlib.sha256(password.encode()).hexdigest()
            
            # Check against each hash
            for user, stored_hash in missing_hashes.items():
                if hashed == stored_hash:
                    print(f"✅ FOUND for {user}: {password}")
                    del missing_hashes[user]
                    
                    # If all found, exit
                    if not missing_hashes:
                        print("\n🎉 All passwords found!")
                        return
    
    print("\n❌ Not found in simple brute force")
    print(f"   Remaining: {len(missing_hashes)} users")

if __name__ == "__main__":
    brute_force_simple()