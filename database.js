// database.js - SQLite Database Connection and Operations
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

class Database {
    constructor() {
        this.db = null;
        this.init();
    }

    init() {
        try {
            // Create database directory if it doesn't exist
            const dbDir = path.join(__dirname, 'data');
            if (!fs.existsSync(dbDir)) {
                fs.mkdirSync(dbDir, { recursive: true });
            }

            // Connect to SQLite database
            const dbPath = path.join(dbDir, 'sk_youth.db');
            this.db = new sqlite3.Database(dbPath, (err) => {
                if (err) {
                    console.error('Error opening database:', err.message);
                    return;
                }
                console.log('Connected to SQLite database');
                this.createTables();
            });
        } catch (error) {
            console.error('Database initialization error:', error);
        }
    }

    createTables() {
        const tables = [
            `CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT CHECK(role IN ('youth', 'admin')) NOT NULL,
                status TEXT CHECK(status IN ('pending', 'verified', 'suspended')) DEFAULT 'pending',
                qr_code TEXT UNIQUE NOT NULL,
                activity_score INTEGER DEFAULT 0,
                events_attended INTEGER DEFAULT 0,
                last_active TEXT,
                profile_image_url TEXT,
                phone_number TEXT,
                address TEXT,
                birth_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )`,

            `CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                location TEXT NOT NULL,
                category TEXT CHECK(category IN ('Environment', 'Leadership', 'Sports', 'Education', 'Community', 'Health', 'Arts')) NOT NULL,
                image_url TEXT,
                max_capacity INTEGER NOT NULL,
                current_attendees INTEGER DEFAULT 0,
                status TEXT CHECK(status IN ('draft', 'upcoming', 'ongoing', 'completed', 'cancelled')) DEFAULT 'upcoming',
                organizer_id TEXT,
                points_reward INTEGER DEFAULT 10,
                requirements TEXT,
                created_by TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organizer_id) REFERENCES users(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )`,

            `CREATE TABLE IF NOT EXISTS event_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                attendance_time TEXT DEFAULT CURRENT_TIMESTAMP,
                check_in_method TEXT CHECK(check_in_method IN ('qr_scan', 'manual', 'online')) DEFAULT 'qr_scan',
                scanned_by TEXT,
                points_earned INTEGER DEFAULT 10,
                status TEXT CHECK(status IN ('present', 'absent', 'late', 'excused')) DEFAULT 'present',
                notes TEXT,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (scanned_by) REFERENCES users(id),
                UNIQUE(event_id, user_id)
            )`,

            `CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT CHECK(type IN ('volunteer', 'job', 'internship')) NOT NULL,
                deadline TEXT NOT NULL,
                slots_available INTEGER NOT NULL,
                slots_filled INTEGER DEFAULT 0,
                requirements TEXT,
                duration TEXT,
                location TEXT,
                contact_person TEXT,
                contact_email TEXT,
                status TEXT CHECK(status IN ('draft', 'open', 'closed', 'filled')) DEFAULT 'open',
                created_by TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )`,

            `CREATE TABLE IF NOT EXISTS opportunity_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                application_date TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT CHECK(status IN ('pending', 'reviewed', 'accepted', 'rejected', 'completed')) DEFAULT 'pending',
                application_notes TEXT,
                admin_notes TEXT,
                reviewed_by TEXT,
                reviewed_at TEXT,
                FOREIGN KEY (opportunity_id) REFERENCES opportunities(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (reviewed_by) REFERENCES users(id),
                UNIQUE(opportunity_id, user_id)
            )`,

            `CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                category TEXT CHECK(category IN ('suggestion', 'complaint', 'question', 'appreciation')) NOT NULL,
                message TEXT NOT NULL,
                status TEXT CHECK(status IN ('pending', 'reviewed', 'resolved', 'archived')) DEFAULT 'pending',
                priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
                reply TEXT,
                replied_by TEXT,
                replied_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (replied_by) REFERENCES users(id)
            )`,

            `CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT CHECK(type IN ('event', 'opportunity', 'system', 'announcement', 'reminder')) NOT NULL,
                recipient_type TEXT CHECK(recipient_type IN ('all', 'youth', 'admin', 'specific')) DEFAULT 'all',
                specific_recipients TEXT,
                related_id TEXT,
                created_by TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                scheduled_for TEXT,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )`,

            `CREATE TABLE IF NOT EXISTS user_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                read_at TEXT,
                FOREIGN KEY (notification_id) REFERENCES notifications(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(notification_id, user_id)
            )`,

            `CREATE TABLE IF NOT EXISTS event_posts (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                caption TEXT,
                created_by TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )`,

            `CREATE TABLE IF NOT EXISTS event_post_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT NOT NULL,
                image_url TEXT NOT NULL,
                display_order INTEGER DEFAULT 0,
                caption TEXT,
                FOREIGN KEY (post_id) REFERENCES event_posts(id) ON DELETE CASCADE
            )`,

            `CREATE TABLE IF NOT EXISTS qr_scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                qr_code TEXT NOT NULL,
                scanned_by TEXT NOT NULL,
                scan_type TEXT CHECK(scan_type IN ('attendance', 'verification', 'checkin', 'checkout')) NOT NULL,
                event_id TEXT,
                scan_time TEXT DEFAULT CURRENT_TIMESTAMP,
                scan_status TEXT CHECK(scan_status IN ('success', 'invalid', 'duplicate', 'error')) DEFAULT 'success',
                scan_data TEXT,
                device_info TEXT,
                location_info TEXT,
                notes TEXT,
                FOREIGN KEY (qr_code) REFERENCES users(qr_code),
                FOREIGN KEY (scanned_by) REFERENCES users(id),
                FOREIGN KEY (event_id) REFERENCES events(id)
            )`,

            `CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action_type TEXT NOT NULL,
                action_details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )`,

            `CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                setting_type TEXT CHECK(setting_type IN ('string', 'number', 'boolean', 'json', 'array')) DEFAULT 'string',
                category TEXT,
                description TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )`
        ];

        // Execute table creation
        tables.forEach((sql, index) => {
            this.db.run(sql, (err) => {
                if (err) {
                    console.error(`Error creating table ${index + 1}:`, err.message);
                }
            });
        });

        // Insert default settings
        this.initializeDefaultSettings();
    }

    initializeDefaultSettings() {
        const settings = [
            ['app_name', 'SK Youth Management System', 'string', 'general', 'Application display name'],
            ['attendance_points', '10', 'number', 'points', 'Points awarded per event attendance'],
            ['qr_validity_minutes', '60', 'number', 'qr', 'QR code validity duration in minutes'],
            ['max_event_capacity', '100', 'number', 'events', 'Maximum allowed event capacity'],
            ['inactivity_days_threshold', '30', 'number', 'users', 'Days before marking user as inactive'],
            ['auto_verify_new_users', 'false', 'boolean', 'users', 'Automatically verify new user registrations'],
            ['default_event_points', '10', 'number', 'points', 'Default points for event participation'],
            ['feedback_response_deadline_days', '7', 'number', 'feedback', 'Days to respond to feedback'],
            ['notification_retention_days', '90', 'number', 'notifications', 'Days to keep notifications'],
            ['max_qr_scans_per_minute', '10', 'number', 'security', 'Maximum QR scans per minute per admin']
        ];

        const sql = `INSERT OR IGNORE INTO system_settings (setting_key, setting_value, setting_type, category, description) VALUES (?, ?, ?, ?, ?)`;
        
        settings.forEach(setting => {
            this.db.run(sql, setting, (err) => {
                if (err) console.error('Error inserting setting:', err.message);
            });
        });
    }

    // Generic query method
    query(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    // Run SQL (for INSERT, UPDATE, DELETE)
    run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ id: this.lastID, changes: this.changes });
                }
            });
        });
    }

    // Get single row
    get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    // Initialize with default data
    async initializeDefaultData() {
        try {
            // Check if users already exist
            const users = await this.query('SELECT COUNT(*) as count FROM users');
            
            if (users[0].count === 0) {
                // Insert default users
                const defaultUsers = [
                    ['1', 'Maria Santos', 'maria@youth.com', 'hashed_password', 'youth', 'verified', 'QR-MARIA-001', 85, 12, '2025-12-07', null, null, null, null],
                    ['2', 'Juan Dela Cruz', 'juan@youth.com', 'hashed_password', 'youth', 'verified', 'QR-JUAN-002', 92, 15, '2025-12-08', null, null, null, null],
                    ['3', 'Ana Reyes', 'ana@youth.com', 'hashed_password', 'youth', 'pending', 'QR-ANA-003', 45, 5, '2025-11-20', null, null, null, null],
                    ['4', 'Pedro Garcia', 'pedro@youth.com', 'hashed_password', 'youth', 'verified', 'QR-PEDRO-004', 78, 10, '2025-12-05', null, null, null, null],
                    ['5', 'Lisa Mendoza', 'lisa@youth.com', 'hashed_password', 'youth', 'verified', 'QR-LISA-005', 35, 3, '2025-10-15', null, null, null, null],
                    ['admin1', 'SK Chairman Rodriguez', 'admin@sk.gov', 'hashed_password', 'admin', 'verified', 'QR-ADMIN-001', 0, 0, '2025-12-08', null, null, null, null]
                ];

                for (const user of defaultUsers) {
                    await this.run(
                        `INSERT INTO users (id, name, email, password_hash, role, status, qr_code, activity_score, events_attended, last_active, profile_image_url, phone_number, address, birth_date) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
                        user
                    );
                }

                console.log('Default users inserted');
            }
        } catch (error) {
            console.error('Error initializing default data:', error);
        }
    }

    // Close database connection
    close() {
        return new Promise((resolve, reject) => {
            this.db.close((err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });
    }
}

module.exports = new Database();