// Global State Management
const AppState = {
    currentUser: null,
    selectedRole: null,
    users: [
        {
            id: '1',
            name: 'Maria Santos',
            email: 'maria@youth.com',
            role: 'youth',
            status: 'verified',
            qrCode: 'QR-MARIA-001',
            activityScore: 85,
            eventsAttended: 12,
            lastActive: '2025-12-07'
        },
        {
            id: '2',
            name: 'Juan Dela Cruz',
            email: 'juan@youth.com',
            role: 'youth',
            status: 'verified',
            qrCode: 'QR-JUAN-002',
            activityScore: 92,
            eventsAttended: 15,
            lastActive: '2025-12-08'
        },
        {
            id: '3',
            name: 'Ana Reyes',
            email: 'ana@youth.com',
            role: 'youth',
            status: 'pending',
            qrCode: 'QR-ANA-003',
            activityScore: 45,
            eventsAttended: 5,
            lastActive: '2025-11-20'
        },
        {
            id: '4',
            name: 'Pedro Garcia',
            email: 'pedro@youth.com',
            role: 'youth',
            status: 'verified',
            qrCode: 'QR-PEDRO-004',
            activityScore: 78,
            eventsAttended: 10,
            lastActive: '2025-12-05'
        },
        {
            id: '5',
            name: 'Lisa Mendoza',
            email: 'lisa@youth.com',
            role: 'youth',
            status: 'verified',
            qrCode: 'QR-LISA-005',
            activityScore: 35,
            eventsAttended: 3,
            lastActive: '2025-10-15'
        },
        {
            id: 'admin1',
            name: 'SK Chairman Rodriguez',
            email: 'admin@sk.gov',
            role: 'admin',
            status: 'verified',
            qrCode: 'QR-ADMIN-001',
            activityScore: 0,
            eventsAttended: 0,
            lastActive: '2025-12-08'
        }
    ],
    events: [
        {
            id: 'evt1',
            title: 'Community Clean-Up Drive',
            description: 'Join us in keeping our barangay clean and green. Volunteers will receive certificates.',
            date: '2025-12-15',
            time: '07:00 AM',
            location: 'Barangay Hall',
            imageUrl: 'https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=800',
            attendees: ['1', '2', '4'],
            maxCapacity: 50,
            category: 'Environment',
            status: 'upcoming'
        },
        {
            id: 'evt2',
            title: 'Youth Leadership Summit 2025',
            description: 'A full-day seminar on leadership, personal development, and community service.',
            date: '2025-12-20',
            time: '09:00 AM',
            location: 'Municipal Covered Court',
            imageUrl: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',
            attendees: ['1', '2'],
            maxCapacity: 100,
            category: 'Leadership',
            status: 'upcoming'
        },
        {
            id: 'evt3',
            title: 'Basketball Tournament',
            description: 'Annual inter-barangay basketball competition. Register your team now!',
            date: '2025-12-10',
            time: '02:00 PM',
            location: 'Barangay Court',
            imageUrl: 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800',
            attendees: ['1', '2', '4'],
            maxCapacity: 200,
            category: 'Sports',
            status: 'completed'
        }
    ],
    opportunities: [
        {
            id: 'opp1',
            title: 'Youth Desk Assistant',
            description: 'Help manage the SK office and assist in administrative tasks.',
            type: 'job',
            deadline: '2025-12-30',
            slots: 2,
            applicants: ['1'],
            requirements: ['Good communication skills', 'Basic computer knowledge', 'Available 3x a week'],
            status: 'open'
        },
        {
            id: 'opp2',
            title: 'Event Photographer',
            description: 'Volunteer to document upcoming SK events and activities.',
            type: 'volunteer',
            deadline: '2025-12-25',
            slots: 5,
            applicants: ['1', '2'],
            requirements: ['Own camera or smartphone', 'Basic photography skills'],
            status: 'open'
        },
        {
            id: 'opp3',
            title: 'Feeding Program Helper',
            description: 'Assist in the monthly feeding program for underprivileged children.',
            type: 'volunteer',
            deadline: '2025-12-18',
            slots: 10,
            applicants: ['2', '4'],
            requirements: ['Compassionate', 'Team player'],
            status: 'open'
        }
    ],
    feedbacks: [
        {
            id: 'fb1',
            userId: '1',
            userName: 'Maria Santos',
            message: 'The last event was amazing! More activities like this please.',
            date: '2025-12-05',
            reply: 'Thank you for your feedback, Maria! We\'re planning more events soon.',
            status: 'replied'
        },
        {
            id: 'fb2',
            userId: '3',
            userName: 'Ana Reyes',
            message: 'Can we have more sports-related activities?',
            date: '2025-12-06',
            status: 'pending'
        },
        {
            id: 'fb3',
            userId: '2',
            userName: 'Juan Dela Cruz',
            message: 'I would like to suggest having coding workshops for interested youth.',
            date: '2025-12-07',
            status: 'pending'
        }
    ],
    notifications: [
        {
            id: 'notif1',
            title: 'New Event Alert',
            message: 'Community Clean-Up Drive scheduled for December 15. Sign up now!',
            date: '2025-12-01',
            recipients: ['all'],
            read: false
        },
        {
            id: 'notif2',
            title: 'Leadership Summit Registration',
            message: 'Limited slots available for the Youth Leadership Summit. Register today!',
            date: '2025-12-03',
            recipients: ['all'],
            read: false
        },
        {
            id: 'notif3',
            title: 'Volunteer Opportunity',
            message: 'We need event photographers for upcoming activities. Check opportunities section.',
            date: '2025-12-05',
            recipients: ['1', '2', '4'],
            read: false
        }
    ],
    eventPosts: [
        {
            id: 'post1',
            eventId: 'evt3',
            images: [
                'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800',
                'https://images.unsplash.com/photo-1606925797300-0b35e9d1794e?w=800'
            ],
            caption: 'Amazing turnout at our Basketball Tournament! Thank you to all participants.',
            date: '2025-12-10'
        }
    ]
};

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check for stored user session
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
        AppState.currentUser = JSON.parse(storedUser);
        showDashboard();
    }
});

// Authentication Functions
function selectRole(role) {
    AppState.selectedRole = role;
    document.getElementById('role-selection').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
    
    const loginIcon = document.getElementById('login-icon');
    const loginTitle = document.getElementById('login-title');
    const loginSubmitBtn = document.getElementById('login-submit-btn');
    const loginDemoEmail = document.getElementById('login-demo-email');
    
    if (role === 'youth') {
        loginIcon.className = 'login-form-icon youth';
        loginIcon.innerHTML = `
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
        `;
        loginTitle.textContent = 'Youth User Login';
        loginTitle.className = 'youth-color';
        loginSubmitBtn.className = 'btn btn-primary w-full';
        loginDemoEmail.textContent = 'maria@youth.com or juan@youth.com';
    } else {
        loginIcon.className = 'login-form-icon admin';
        loginIcon.innerHTML = `
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
        `;
        loginTitle.textContent = 'SK Official Login';
        loginTitle.className = 'admin-color';
        loginSubmitBtn.className = 'btn btn-primary admin w-full';
        loginDemoEmail.textContent = 'admin@sk.gov';
    }
}

function backToRoleSelection() {
    AppState.selectedRole = null;
    document.getElementById('role-selection').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('login-error').style.display = 'none';
}

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const role = AppState.selectedRole;
    
    const user = AppState.users.find(u => u.email === email && u.role === role);
    
    if (user) {
        AppState.currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
        document.getElementById('login-error').style.display = 'none';
        showDashboard();
    } else {
        const errorDiv = document.getElementById('login-error');
        errorDiv.textContent = 'Invalid credentials. Please try again.';
        errorDiv.style.display = 'block';
    }
}

function logout() {
    AppState.currentUser = null;
    localStorage.removeItem('currentUser');
    
    // Hide all screens
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('youth-dashboard').classList.remove('active');
    document.getElementById('admin-dashboard').classList.remove('active');
    
    // Show login screen
    document.getElementById('login-screen').classList.add('active');
    backToRoleSelection();
}

function showDashboard() {
    document.getElementById('login-screen').classList.remove('active');
    
    if (AppState.currentUser.role === 'youth') {
        document.getElementById('youth-dashboard').classList.add('active');
        initYouthDashboard();
    } else {
        document.getElementById('admin-dashboard').classList.add('active');
        initAdminDashboard();
    }
}

// Modal Functions
function showModal(title, content) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-body').innerHTML = content;
    document.getElementById('modal-overlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
    document.getElementById('modal-body').innerHTML = '';
}

// Data Management Functions
function addEvent(event) {
    const newEvent = {
        ...event,
        id: `evt${Date.now()}`,
        attendees: []
    };
    AppState.events.push(newEvent);
    return newEvent;
}

function updateEvent(id, updatedData) {
    const index = AppState.events.findIndex(e => e.id === id);
    if (index !== -1) {
        AppState.events[index] = { ...AppState.events[index], ...updatedData };
    }
}

function deleteEvent(id) {
    AppState.events = AppState.events.filter(e => e.id !== id);
}

function joinEvent(eventId, userId) {
    const event = AppState.events.find(e => e.id === eventId);
    if (event && !event.attendees.includes(userId)) {
        event.attendees.push(userId);
    }
}

function addOpportunity(opportunity) {
    const newOpp = {
        ...opportunity,
        id: `opp${Date.now()}`,
        applicants: []
    };
    AppState.opportunities.push(newOpp);
    return newOpp;
}

function applyToOpportunity(opportunityId, userId) {
    const opp = AppState.opportunities.find(o => o.id === opportunityId);
    if (opp && !opp.applicants.includes(userId)) {
        opp.applicants.push(userId);
    }
}

function submitFeedback(userId, userName, message) {
    const newFeedback = {
        id: `fb${Date.now()}`,
        userId,
        userName,
        message,
        date: new Date().toISOString().split('T')[0],
        status: 'pending'
    };
    AppState.feedbacks.push(newFeedback);
    return newFeedback;
}

function replyToFeedback(feedbackId, reply) {
    const feedback = AppState.feedbacks.find(f => f.id === feedbackId);
    if (feedback) {
        feedback.reply = reply;
        feedback.status = 'replied';
    }
}

function sendNotification(title, message, recipients) {
    const newNotif = {
        id: `notif${Date.now()}`,
        title,
        message,
        date: new Date().toISOString().split('T')[0],
        recipients,
        read: false
    };
    AppState.notifications.push(newNotif);
    return newNotif;
}

function addUser(user) {
    const newUser = {
        ...user,
        id: `user${Date.now()}`,
        qrCode: `QR-${user.name.toUpperCase().replace(/\s/g, '-')}-${Date.now()}`,
        activityScore: 0,
        eventsAttended: 0,
        lastActive: new Date().toISOString().split('T')[0]
    };
    AppState.users.push(newUser);
    return newUser;
}

function deleteUser(userId) {
    AppState.users = AppState.users.filter(u => u.id !== userId);
}

function verifyUser(userId) {
    const user = AppState.users.find(u => u.id === userId);
    if (user) {
        user.status = 'verified';
    }
}

function recordAttendance(eventId, userId) {
    const event = AppState.events.find(e => e.id === eventId);
    if (event && !event.attendees.includes(userId)) {
        event.attendees.push(userId);
    }
    
    const user = AppState.users.find(u => u.id === userId);
    if (user) {
        user.eventsAttended += 1;
        user.activityScore += 10;
        user.lastActive = new Date().toISOString().split('T')[0];
    }
}

function addEventPost(eventId, images, caption) {
    const newPost = {
        id: `post${Date.now()}`,
        eventId,
        images,
        caption,
        date: new Date().toISOString().split('T')[0]
    };
    AppState.eventPosts.push(newPost);
    return newPost;
}

function markNotificationRead(notificationId) {
    const notification = AppState.notifications.find(n => n.id === notificationId);
    if (notification) {
        notification.read = true;
    }
}

// Helper Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

function getActiveYouthCount() {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    return AppState.users.filter(u => {
        if (u.role !== 'youth') return false;
        const lastActive = new Date(u.lastActive);
        return lastActive >= thirtyDaysAgo;
    }).length;
}

function getInactiveYouthCount() {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    return AppState.users.filter(u => {
        if (u.role !== 'youth') return false;
        const lastActive = new Date(u.lastActive);
        return lastActive < thirtyDaysAgo;
    }).length;
}

function getUserById(userId) {
    return AppState.users.find(u => u.id === userId);
}

function getEventById(eventId) {
    return AppState.events.find(e => e.id === eventId);
}