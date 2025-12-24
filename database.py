import mysql.connector
import hashlib

def setup_database():
    try:
        print("Setting up database...")
        
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS sk_youth_portal")
        cursor.execute("USE sk_youth_portal")
        
        # Drop all tables in correct order
        tables = [
            'awards', 'opportunity_applications', 'feedback', 
            'event_registrations', 'opportunities', 'events', 'users'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            except:
                pass
        
        # Create users table
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'youth',
                status VARCHAR(20) DEFAULT 'active',
                phone VARCHAR(20),
                address TEXT,
                barangay VARCHAR(50),
                birthdate DATE,
                gender VARCHAR(20),
                youth_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create events table
        cursor.execute("""
            CREATE TABLE events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                event_date DATE NOT NULL,
                event_time TIME NOT NULL,
                location VARCHAR(200),
                event_type VARCHAR(50),
                max_participants INT,
                registered_participants INT DEFAULT 0,
                status VARCHAR(20) DEFAULT 'upcoming',
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Create event registrations
        cursor.execute("""
            CREATE TABLE event_registrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT,
                user_id INT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                attendance_status VARCHAR(20) DEFAULT 'registered',
                check_in_time DATETIME,
                check_out_time DATETIME,
                hours_credited DECIMAL(5,2) DEFAULT 0,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_event_user (event_id, user_id)
            )
        """)
        
        # Create opportunities table
        cursor.execute("""
            CREATE TABLE opportunities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                type VARCHAR(50) NOT NULL,
                description TEXT,
                compensation VARCHAR(100),
                location VARCHAR(200),
                commitment VARCHAR(100),
                deadline DATE,
                max_applicants INT,
                current_applicants INT DEFAULT 0,
                status VARCHAR(20) DEFAULT 'open',
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Create opportunity applications
        cursor.execute("""
            CREATE TABLE opportunity_applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                opportunity_id INT,
                user_id INT,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_opp_user (opportunity_id, user_id)
            )
        """)
        
        # Create feedback table
        cursor.execute("""
            CREATE TABLE feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                subject VARCHAR(200),
                message TEXT,
                feedback_type VARCHAR(50) DEFAULT 'general',
                status VARCHAR(20) DEFAULT 'pending',
                admin_reply TEXT,
                linked_item_id INT,
                linked_item_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create awards table
        cursor.execute("""
            CREATE TABLE awards (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                award_name VARCHAR(100),
                description TEXT,
                award_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Add default admin
        hashed_admin = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (name, email, password, role, youth_id) VALUES (%s, %s, %s, %s, %s)",
            ('Admin Officer', 'admin@sk.ph', hashed_admin, 'admin', 'SK-ADMIN-001')
        )
        admin_id = cursor.lastrowid
        
        # Add sample youth users
        for i in range(1, 6):
            email = f'youth{i}@example.com'
            hashed = hashlib.sha256(f'youth{i}23'.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (name, email, password, role, barangay, youth_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (f'Youth User {i}', email, hashed, 'youth', f'Purok {i}', f'SK-YOUTH-{i:03d}')
            )
        
        # Add sample events
        sample_events = [
            ('Coastal Clean-Up Drive', 'Environmental clean-up activity', '2024-12-20', '09:00:00', 'Beachfront', 'Volunteer', 100),
            ('Youth Leadership Summit', 'Leadership training workshop', '2024-12-25', '10:00:00', 'Barangay Hall', 'Seminar', 150),
            ('Christmas Party', 'Annual youth Christmas celebration', '2024-12-23', '18:00:00', 'Community Center', 'Social', 200),
            ('Basketball Tournament', 'Inter-purok basketball competition', '2024-12-28', '14:00:00', 'Sports Complex', 'Sports', 50),
            ('First Aid Training', 'Basic first aid certification', '2025-01-05', '08:00:00', 'Health Center', 'Training', 30)
        ]
        
        for event in sample_events:
            cursor.execute("""
                INSERT INTO events (title, description, event_date, event_time, location, event_type, max_participants, created_by) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (*event, admin_id))
        
        # Add sample opportunities
        sample_opps = [
            ('SK Admin Assistant (Part-Time)', 'Job', 'Support SK council', 'P50/hr', 'SK Office', '20 hours/week', '2024-12-31', 2),
            ('Barangay Health Volunteer', 'Volunteer', 'Assist health center', 'None', 'Health Center', 'Flexible', None, 5),
            ('Youth IT Intern', 'Internship', 'Website maintenance', 'Allowance', 'SK Office', '3 months', '2025-01-15', 3)
        ]
        
        for opp in sample_opps:
            cursor.execute("""
                INSERT INTO opportunities (title, type, description, compensation, location, commitment, deadline, max_applicants, created_by) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (*opp, admin_id))
        
        # Add sample feedback
        cursor.execute("SELECT id FROM users WHERE role='youth' LIMIT 3")
        youth_ids = [row[0] for row in cursor.fetchall()]
        
        sample_feedback = [
            ('Great event!', 'The clean-up drive was fantastic!', 'appreciation', youth_ids[0]),
            ('Technical issue', 'Website loading slowly', 'technical', youth_ids[1]),
            ('Suggestion', 'More sports events please', 'suggestion', youth_ids[2])
        ]
        
        for subject, message, ftype, user_id in sample_feedback:
            cursor.execute("""
                INSERT INTO feedback (user_id, subject, message, feedback_type) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, subject, message, ftype))
        
        # Add some event registrations
        cursor.execute("SELECT id FROM events LIMIT 2")
        event_ids = [row[0] for row in cursor.fetchall()]
        
        for user_id in youth_ids[:2]:
            for event_id in event_ids:
                cursor.execute("""
                    INSERT INTO event_registrations (event_id, user_id) 
                    VALUES (%s, %s)
                """, (event_id, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("=" * 50)
        print("DATABASE SETUP COMPLETE!")
        print("=" * 50)
        print("Test Accounts:")
        print("Admin: admin@sk.ph / admin123")
        print("Youth: youth1@example.com / youth123")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_database()