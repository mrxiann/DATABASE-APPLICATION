// Admin Dashboard Initialization
let currentAdminTab = 'home';

function initAdminDashboard() {
    document.getElementById('admin-user-name').textContent = AppState.currentUser.name;
    renderAdminNav();
    loadAdminTab('home');
}

function renderAdminNav() {
    const pendingFeedbacks = AppState.feedbacks.filter(f => f.status === 'pending').length;

    const navItems = [
        { id: 'home', label: 'Dashboard', icon: 'home' },
        { id: 'events', label: 'Events', icon: 'calendar' },
        { id: 'opportunities', label: 'Opportunities', icon: 'briefcase' },
        { id: 'users', label: 'Users', icon: 'users' },
        { id: 'attendance', label: 'Attendance', icon: 'check-square' },
        { id: 'feedback', label: 'Feedback', icon: 'message-square', badge: pendingFeedbacks },
        { id: 'notifications', label: 'Notifications', icon: 'bell' },
        { id: 'posts', label: 'Event Posts', icon: 'image' }
    ];

    const navHTML = navItems.map(item => `
        <button class="nav-item ${currentAdminTab === item.id ? 'active' : ''}" onclick="loadAdminTab('${item.id}')">
            ${getAdminIcon(item.icon)}
            <span>${item.label}</span>
            ${item.badge && item.badge > 0 ? `<span class="nav-badge">${item.badge}</span>` : ''}
        </button>
    `).join('');

    document.getElementById('admin-nav').innerHTML = navHTML;
}

function loadAdminTab(tabId) {
    currentAdminTab = tabId;
    renderAdminNav();

    const contentDiv = document.getElementById('admin-content');
    
    switch(tabId) {
        case 'home':
            contentDiv.innerHTML = renderAdminHome();
            break;
        case 'events':
            contentDiv.innerHTML = renderAdminEvents();
            break;
        case 'opportunities':
            contentDiv.innerHTML = renderAdminOpportunities();
            break;
        case 'users':
            contentDiv.innerHTML = renderAdminUsers();
            break;
        case 'attendance':
            contentDiv.innerHTML = renderAdminAttendance();
            break;
        case 'feedback':
            contentDiv.innerHTML = renderAdminFeedback();
            break;
        case 'notifications':
            contentDiv.innerHTML = renderAdminNotifications();
            break;
        case 'posts':
            contentDiv.innerHTML = renderAdminPosts();
            break;
    }
}

// Admin Home
function renderAdminHome() {
    const totalYouth = AppState.users.filter(u => u.role === 'youth').length;
    const activeYouth = getActiveYouthCount();
    const upcomingEvents = AppState.events.filter(e => e.status === 'upcoming').length;
    const pendingFeedbacks = AppState.feedbacks.filter(f => f.status === 'pending').length;

    return `
        <div class="page-header">
            <h2>Admin Dashboard</h2>
            <p>Overview of SK Youth Management System</p>
        </div>

        <div class="cards-grid">
            <div class="stat-card">
                <div class="stat-icon blue">
                    ${getAdminIcon('users')}
                </div>
                <div class="stat-label">Total Youth</div>
                <div class="stat-value">${totalYouth}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon green">
                    ${getAdminIcon('user-check')}
                </div>
                <div class="stat-label">Active Youth</div>
                <div class="stat-value">${activeYouth}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon orange">
                    ${getAdminIcon('calendar')}
                </div>
                <div class="stat-label">Upcoming Events</div>
                <div class="stat-value">${upcomingEvents}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon blue">
                    ${getAdminIcon('message-square')}
                </div>
                <div class="stat-label">Pending Feedback</div>
                <div class="stat-value">${pendingFeedbacks}</div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Recent Activity</h3>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Event</th>
                            <th>Date</th>
                            <th>Attendees</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${AppState.events.slice(-5).reverse().map(event => `
                            <tr>
                                <td>${event.title}</td>
                                <td>${formatDate(event.date)}</td>
                                <td>${event.attendees.length}/${event.maxCapacity}</td>
                                <td><span class="badge badge-${event.status === 'upcoming' ? 'primary' : event.status === 'ongoing' ? 'warning' : 'success'}">${event.status}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

// Admin Events
function renderAdminEvents() {
    return `
        <div class="page-header">
            <h2>Event Management</h2>
            <p>Create and manage community events</p>
            <button class="btn btn-primary" onclick="showAddEventModal()">Add New Event</button>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">All Events</h3>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Location</th>
                            <th>Category</th>
                            <th>Attendees</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${AppState.events.map(event => `
                            <tr>
                                <td>${event.title}</td>
                                <td>${formatDate(event.date)}</td>
                                <td>${event.location}</td>
                                <td><span class="badge badge-primary">${event.category}</span></td>
                                <td>${event.attendees.length}/${event.maxCapacity}</td>
                                <td><span class="badge badge-${event.status === 'upcoming' ? 'primary' : event.status === 'ongoing' ? 'warning' : 'success'}">${event.status}</span></td>
                                <td>
                                    <div class="action-buttons">
                                        <button class="btn btn-sm btn-secondary" onclick="showEventDetails('${event.id}')">View</button>
                                        <button class="btn btn-sm btn-danger" onclick="handleDeleteEvent('${event.id}')">Delete</button>
                                    </div>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

function showAddEventModal() {
    const content = `
        <form onsubmit="handleAddEvent(event)">
            <div class="form-group">
                <label>Event Title</label>
                <input type="text" id="event-title" required>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="event-description" rows="3" required></textarea>
            </div>
            <div class="form-group">
                <label>Date</label>
                <input type="date" id="event-date" required>
            </div>
            <div class="form-group">
                <label>Time</label>
                <input type="time" id="event-time" required>
            </div>
            <div class="form-group">
                <label>Location</label>
                <input type="text" id="event-location" required>
            </div>
            <div class="form-group">
                <label>Category</label>
                <select id="event-category" required>
                    <option value="">Select category</option>
                    <option value="Environment">Environment</option>
                    <option value="Leadership">Leadership</option>
                    <option value="Sports">Sports</option>
                    <option value="Education">Education</option>
                    <option value="Community">Community</option>
                </select>
            </div>
            <div class="form-group">
                <label>Max Capacity</label>
                <input type="number" id="event-capacity" min="1" required>
            </div>
            <div class="form-group">
                <label>Image URL</label>
                <input type="url" id="event-image" placeholder="https://..." required>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary admin">Add Event</button>
            </div>
        </form>
    `;
    showModal('Add New Event', content);
}

function handleAddEvent(event) {
    event.preventDefault();
    const newEvent = {
        title: document.getElementById('event-title').value,
        description: document.getElementById('event-description').value,
        date: document.getElementById('event-date').value,
        time: document.getElementById('event-time').value,
        location: document.getElementById('event-location').value,
        category: document.getElementById('event-category').value,
        maxCapacity: parseInt(document.getElementById('event-capacity').value),
        imageUrl: document.getElementById('event-image').value,
        status: 'upcoming'
    };
    addEvent(newEvent);
    closeModal();
    loadAdminTab('events');
}

function handleDeleteEvent(eventId) {
    if (confirm('Are you sure you want to delete this event?')) {
        deleteEvent(eventId);
        loadAdminTab('events');
    }
}

function showEventDetails(eventId) {
    const event = getEventById(eventId);
    if (!event) return;

    const attendeesList = event.attendees.map(userId => {
        const user = getUserById(userId);
        return user ? user.name : 'Unknown';
    }).join(', ') || 'No attendees yet';

    const content = `
        <div style="display: grid; gap: 1rem;">
            <img src="${event.imageUrl}" alt="${event.title}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 0.5rem;">
            <div>
                <strong>Description:</strong>
                <p>${event.description}</p>
            </div>
            <div>
                <strong>Date & Time:</strong>
                <p>${formatDate(event.date)} at ${event.time}</p>
            </div>
            <div>
                <strong>Location:</strong>
                <p>${event.location}</p>
            </div>
            <div>
                <strong>Category:</strong>
                <p>${event.category}</p>
            </div>
            <div>
                <strong>Capacity:</strong>
                <p>${event.attendees.length} / ${event.maxCapacity}</p>
            </div>
            <div>
                <strong>Attendees:</strong>
                <p>${attendeesList}</p>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">Close</button>
        </div>
    `;
    showModal(event.title, content);
}

// Admin Opportunities
function renderAdminOpportunities() {
    return `
        <div class="page-header">
            <h2>Opportunities Management</h2>
            <p>Manage volunteer and job opportunities</p>
            <button class="btn btn-primary" onclick="showAddOpportunityModal()">Add New Opportunity</button>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">All Opportunities</h3>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Type</th>
                            <th>Deadline</th>
                            <th>Applicants</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${AppState.opportunities.map(opp => `
                            <tr>
                                <td>${opp.title}</td>
                                <td><span class="badge badge-${opp.type === 'job' ? 'success' : 'warning'}">${opp.type}</span></td>
                                <td>${formatDate(opp.deadline)}</td>
                                <td>${opp.applicants.length}/${opp.slots}</td>
                                <td><span class="badge badge-${opp.status === 'open' ? 'success' : 'danger'}">${opp.status}</span></td>
                                <td>
                                    <button class="btn btn-sm btn-secondary" onclick="showOpportunityDetails('${opp.id}')">View</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

function showAddOpportunityModal() {
    const content = `
        <form onsubmit="handleAddOpportunity(event)">
            <div class="form-group">
                <label>Title</label>
                <input type="text" id="opp-title" required>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="opp-description" rows="3" required></textarea>
            </div>
            <div class="form-group">
                <label>Type</label>
                <select id="opp-type" required>
                    <option value="">Select type</option>
                    <option value="volunteer">Volunteer</option>
                    <option value="job">Job</option>
                </select>
            </div>
            <div class="form-group">
                <label>Deadline</label>
                <input type="date" id="opp-deadline" required>
            </div>
            <div class="form-group">
                <label>Number of Slots</label>
                <input type="number" id="opp-slots" min="1" required>
            </div>
            <div class="form-group">
                <label>Requirements (one per line)</label>
                <textarea id="opp-requirements" rows="3" placeholder="Requirement 1&#10;Requirement 2&#10;Requirement 3" required></textarea>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary admin">Add Opportunity</button>
            </div>
        </form>
    `;
    showModal('Add New Opportunity', content);
}

function handleAddOpportunity(event) {
    event.preventDefault();
    const requirements = document.getElementById('opp-requirements').value
        .split('\n')
        .filter(r => r.trim());
    
    const newOpp = {
        title: document.getElementById('opp-title').value,
        description: document.getElementById('opp-description').value,
        type: document.getElementById('opp-type').value,
        deadline: document.getElementById('opp-deadline').value,
        slots: parseInt(document.getElementById('opp-slots').value),
        requirements,
        status: 'open'
    };
    addOpportunity(newOpp);
    closeModal();
    loadAdminTab('opportunities');
}

function showOpportunityDetails(oppId) {
    const opp = AppState.opportunities.find(o => o.id === oppId);
    if (!opp) return;

    const applicantsList = opp.applicants.map(userId => {
        const user = getUserById(userId);
        return user ? user.name : 'Unknown';
    }).join(', ') || 'No applicants yet';

    const content = `
        <div style="display: grid; gap: 1rem;">
            <div>
                <strong>Description:</strong>
                <p>${opp.description}</p>
            </div>
            <div>
                <strong>Type:</strong>
                <p>${opp.type === 'job' ? 'Job' : 'Volunteer'}</p>
            </div>
            <div>
                <strong>Deadline:</strong>
                <p>${formatDate(opp.deadline)}</p>
            </div>
            <div>
                <strong>Slots:</strong>
                <p>${opp.applicants.length} / ${opp.slots}</p>
            </div>
            <div>
                <strong>Requirements:</strong>
                <ul style="margin-left: 1.5rem;">
                    ${opp.requirements.map(req => `<li>${req}</li>`).join('')}
                </ul>
            </div>
            <div>
                <strong>Applicants:</strong>
                <p>${applicantsList}</p>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">Close</button>
        </div>
    `;
    showModal(opp.title, content);
}

// Admin Users
function renderAdminUsers() {
    const youthUsers = AppState.users.filter(u => u.role === 'youth');
    
    return `
        <div class="page-header">
            <h2>User Management</h2>
            <p>Manage youth users and their accounts</p>
            <button class="btn btn-primary" onclick="showAddUserModal()">Add New User</button>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Youth Users</h3>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>QR Code</th>
                            <th>Activity Score</th>
                            <th>Events Attended</th>
                            <th>Last Active</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${youthUsers.map(user => {
                            const isActive = (new Date() - new Date(user.lastActive)) / (1000 * 60 * 60 * 24) <= 30;
                            return `
                                <tr>
                                    <td>${user.name}</td>
                                    <td>${user.email}</td>
                                    <td><code>${user.qrCode}</code></td>
                                    <td>${user.activityScore}</td>
                                    <td>${user.eventsAttended}</td>
                                    <td>${formatDate(user.lastActive)}</td>
                                    <td>
                                        <span class="badge badge-${user.status === 'verified' ? 'success' : 'warning'}">${user.status}</span>
                                        <span class="badge badge-${isActive ? 'success' : 'danger'}">${isActive ? 'Active' : 'Inactive'}</span>
                                    </td>
                                    <td>
                                        <div class="action-buttons">
                                            ${user.status === 'pending' ? `<button class="btn btn-sm btn-success" onclick="handleVerifyUser('${user.id}')">Verify</button>` : ''}
                                            <button class="btn btn-sm btn-danger" onclick="handleDeleteUser('${user.id}')">Delete</button>
                                        </div>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

function showAddUserModal() {
    const content = `
        <form onsubmit="handleAddUser(event)">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" id="user-name" required>
            </div>
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" id="user-email" required>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select id="user-status" required>
                    <option value="pending">Pending</option>
                    <option value="verified">Verified</option>
                </select>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary admin">Add User</button>
            </div>
        </form>
    `;
    showModal('Add New User', content);
}

function handleAddUser(event) {
    event.preventDefault();
    const newUser = {
        name: document.getElementById('user-name').value,
        email: document.getElementById('user-email').value,
        role: 'youth',
        status: document.getElementById('user-status').value
    };
    addUser(newUser);
    closeModal();
    loadAdminTab('users');
}

function handleVerifyUser(userId) {
    verifyUser(userId);
    loadAdminTab('users');
}

function handleDeleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        deleteUser(userId);
        loadAdminTab('users');
    }
}

// Admin Attendance
function renderAdminAttendance() {
    return `
        <div class="page-header">
            <h2>Attendance Management</h2>
            <p>Record and track event attendance</p>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Scan QR Code for Attendance</h3>
            </div>
            <form onsubmit="handleRecordAttendance(event)">
                
                <div class="qr-scanner-area">
                    <div class="qr-viewfinder"></div>
                    <h4>Point Scanner or Enter Code Below</h4>
                    
                    <div class="form-group qr-input-container">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="youth-color" style="width: 1.5rem; height: 1.5rem;">
                            <path fill-rule="evenodd" d="M3.75 3.75A1.5 1.5 0 0 1 5.25 2.25h13.5c.828 0 1.5.672 1.5 1.5v13.5a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5V3.75ZM6 6.75a.75.75 0 0 1 .75-.75h.75a.75.75 0 0 1 .75.75v.75a.75.75 0 0 1-.75.75H6.75a.75.75 0 0 1-.75-.75v-.75ZM.75 18a.75.75 0 0 1 .75-.75h.75a.75.75 0 0 1 .75.75v.75a.75.75 0 0 1-.75.75h-.75a.75.75 0 0 1-.75-.75v-.75ZM18 18a.75.75 0 0 1 .75-.75h.75a.75.75 0 0 1 .75.75v.75a.75.75 0 0 1-.75.75h-.75a.75.75 0 0 1-.75-.75v-.75Z" clip-rule="evenodd" />
                        </svg>

                        <input type="text" id="attendance-qr" placeholder="QR-MARIA-001" required autofocus style="flex: 1;">
                        
                        <button type="submit" class="btn btn-primary admin btn-sm" style="flex-shrink: 0;">Record</button>
                    </div>
                </div>

                <div class="form-group">
                    <label for="attendance-event">Select Event</label>
                    <select id="attendance-event" required>
                        <option value="">Choose an event</option>
                        ${AppState.events.filter(e => e.status !== 'completed').map(event => `
                            <option value="${event.id}">${event.title} - ${formatDate(event.date)}</option>
                        `).join('')}
                    </select>
                </div>
            </form>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Attendance Reports</h3>
                <button class="btn btn-secondary" onclick="exportAttendanceReport()">Export Report</button>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Event</th>
                            <th>Date</th>
                            <th>Total Attendees</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${AppState.events.map(event => `
                            <tr>
                                <td>${event.title}</td>
                                <td>${formatDate(event.date)}</td>
                                <td>${event.attendees.length}/${event.maxCapacity}</td>
                                <td>
                                    <button class="btn btn-sm btn-secondary" onclick="showAttendanceDetails('${event.id}')">View Details</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

function handleRecordAttendance(event) {
    event.preventDefault();
    const eventId = document.getElementById('attendance-event').value;
    const qrCode = document.getElementById('attendance-qr').value.trim().toUpperCase(); // Normalize input
    
    if (!eventId) {
        alert('Please select an event.');
        return;
    }

    const user = AppState.users.find(u => u.qrCode === qrCode);
    if (!user) {
        alert('Invalid QR Code. User not found.');
        document.getElementById('attendance-qr').value = ''; // Clear input on failure
        document.getElementById('attendance-qr').focus(); // Refocus for next scan
        return;
    }
    
    // Assuming recordAttendance and alert functions are defined elsewhere in the AppState/app logic
    // For this example, we'll keep the existing logic:
    recordAttendance(eventId, user.id);
    alert(`Attendance recorded for ${user.name}`);
    document.getElementById('attendance-qr').value = '';
    document.getElementById('attendance-qr').focus(); // Refocus for next scan
    // loadAdminTab('attendance'); // Re-rendering the tab is optional, depending on performance
}


function showAttendanceDetails(eventId) {
    const event = getEventById(eventId);
    if (!event) return;

    const attendees = event.attendees.map(userId => getUserById(userId)).filter(u => u);

    const content = `
        <div style="display: grid; gap: 1rem;">
            <div>
                <strong>Event:</strong>
                <p>${event.title}</p>
            </div>
            <div>
                <strong>Date:</strong>
                <p>${formatDate(event.date)}</p>
            </div>
            <div>
                <strong>Total Attendees:</strong>
                <p>${attendees.length} / ${event.maxCapacity}</p>
            </div>
            <div>
                <strong>Attendee List:</strong>
                ${attendees.length > 0 ? `
                    <table style="width: 100%; margin-top: 1rem;">
                        <thead>
                            <tr>
                                <th style="text-align: left; padding: 0.5rem; border-bottom: 2px solid var(--gray-200);">Name</th>
                                <th style="text-align: left; padding: 0.5rem; border-bottom: 2px solid var(--gray-200);">Email</th>
                                <th style="text-align: left; padding: 0.5rem; border-bottom: 2px solid var(--gray-200);">QR Code</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${attendees.map(user => `
                                <tr>
                                    <td style="padding: 0.5rem; border-bottom: 1px solid var(--gray-200);">${user.name}</td>
                                    <td style="padding: 0.5rem; border-bottom: 1px solid var(--gray-200);">${user.email}</td>
                                    <td style="padding: 0.5rem; border-bottom: 1px solid var(--gray-200);"><code>${user.qrCode}</code></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                ` : '<p>No attendees yet.</p>'}
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">Close</button>
        </div>
    `;
    showModal('Attendance Details', content);
}

function exportAttendanceReport() {
    let csv = 'Event,Date,Total Attendees,Max Capacity,Attendee Names\n';
    AppState.events.forEach(event => {
        const attendeeNames = event.attendees.map(userId => {
            const user = getUserById(userId);
            return user ? user.name : 'Unknown';
        }).join('; ');
        csv += `"${event.title}","${event.date}",${event.attendees.length},${event.maxCapacity},"${attendeeNames}"\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'attendance-report.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Admin Feedback
function renderAdminFeedback() {
    const pendingFeedbacks = AppState.feedbacks.filter(f => f.status === 'pending');
    const repliedFeedbacks = AppState.feedbacks.filter(f => f.status === 'replied');

    return `
        <div class="page-header">
            <h2>Feedback Management</h2>
            <p>Review and respond to youth feedback</p>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Pending Feedback</h3>
            </div>
            ${pendingFeedbacks.length > 0 ? 
                pendingFeedbacks.map(feedback => `
                    <div class="feedback-item">
                        <div class="feedback-header">
                            <span class="feedback-user">${feedback.userName}</span>
                            <span class="badge badge-warning">${feedback.status}</span>
                        </div>
                        <div class="text-gray text-sm">${formatDate(feedback.date)}</div>
                        <div class="feedback-message">${feedback.message}</div>
                        <button class="btn btn-sm btn-primary admin" onclick="showReplyModal('${feedback.id}')">Reply</button>
                    </div>
                `).join('') 
                : '<p class="text-gray">No pending feedback.</p>'
            }
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Replied Feedback</h3>
            </div>
            ${repliedFeedbacks.length > 0 ? 
                repliedFeedbacks.map(feedback => `
                    <div class="feedback-item">
                        <div class="feedback-header">
                            <span class="feedback-user">${feedback.userName}</span>
                            <span class="badge badge-success">${feedback.status}</span>
                        </div>
                        <div class="text-gray text-sm">${formatDate(feedback.date)}</div>
                        <div class="feedback-message">${feedback.message}</div>
                        <div class="feedback-reply">
                            <div class="feedback-reply-label">Your Reply:</div>
                            <div>${feedback.reply}</div>
                        </div>
                    </div>
                `).join('') 
                : '<p class="text-gray">No replied feedback yet.</p>'
            }
        </div>
    `;
}

function showReplyModal(feedbackId) {
    const feedback = AppState.feedbacks.find(f => f.id === feedbackId);
    if (!feedback) return;

    const content = `
        <div style="margin-bottom: 1rem;">
            <strong>From:</strong> ${feedback.userName}<br>
            <strong>Date:</strong> ${formatDate(feedback.date)}<br>
            <strong>Message:</strong>
            <p style="background: var(--gray-50); padding: 1rem; border-radius: 0.5rem; margin-top: 0.5rem;">
                ${feedback.message}
            </p>
        </div>
        <form onsubmit="handleReplyFeedback(event, '${feedbackId}')">
            <div class="form-group">
                <label>Your Reply</label>
                <textarea id="reply-message" rows="4" required></textarea>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary admin">Send Reply</button>
            </div>
        </form>
    `;
    showModal('Reply to Feedback', content);
}

function handleReplyFeedback(event, feedbackId) {
    event.preventDefault();
    const reply = document.getElementById('reply-message').value;
    replyToFeedback(feedbackId, reply);
    closeModal();
    loadAdminTab('feedback');
}

// Admin Notifications
function renderAdminNotifications() {
    return `
        <div class="page-header">
            <h2>Notification Center</h2>
            <p>Send targeted notifications to youth users</p>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Send New Notification</h3>
            </div>
            <form onsubmit="handleSendNotification(event)">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="notif-title" required>
                </div>
                <div class="form-group">
                    <label>Message</label>
                    <textarea id="notif-message" rows="4" required></textarea>
                </div>
                <div class="form-group">
                    <label>Recipients</label>
                    <select id="notif-recipients" required>
                        <option value="all">All Users</option>
                        <option value="active">Active Users Only (Last 30 days)</option>
                        <option value="inactive">Inactive Users Only (30+ days)</option>
                        <option value="verified">Verified Users Only</option>
                        <option value="pending">Pending Users Only</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary admin">Send Notification</button>
            </form>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Notification History</h3>
            </div>
            ${AppState.notifications.length > 0 ? 
                AppState.notifications.slice().reverse().map(notif => {
                    let recipientText = '';
                    if (notif.recipients.includes('all')) {
                        recipientText = 'All Users';
                    } else {
                        recipientText = `${notif.recipients.length} users`;
                    }
                    
                    return `
                        <div class="notification-item">
                            <div class="notification-header">
                                <div class="notification-title">${notif.title}</div>
                                <div class="notification-date">${formatDate(notif.date)}</div>
                            </div>
                            <div class="notification-message">${notif.message}</div>
                            <div class="text-sm text-gray" style="margin-top: 0.5rem;">
                                Recipients: ${recipientText}
                            </div>
                        </div>
                    `;
                }).join('') 
                : '<p class="text-gray">No notifications sent yet.</p>'
            }
        </div>
    `;
}

function handleSendNotification(event) {
    event.preventDefault();
    const title = document.getElementById('notif-title').value;
    const message = document.getElementById('notif-message').value;
    const recipientType = document.getElementById('notif-recipients').value;
    
    let recipients = [];
    
    if (recipientType === 'all') {
        recipients = ['all'];
    } else if (recipientType === 'active') {
        const activeUsers = AppState.users.filter(u => {
            if (u.role !== 'youth') return false;
            const daysSinceActive = (new Date() - new Date(u.lastActive)) / (1000 * 60 * 60 * 24);
            return daysSinceActive <= 30;
        });
        recipients = activeUsers.map(u => u.id);
    } else if (recipientType === 'inactive') {
        const inactiveUsers = AppState.users.filter(u => {
            if (u.role !== 'youth') return false;
            const daysSinceActive = (new Date() - new Date(u.lastActive)) / (1000 * 60 * 60 * 24);
            return daysSinceActive > 30;
        });
        recipients = inactiveUsers.map(u => u.id);
    } else if (recipientType === 'verified') {
        recipients = AppState.users.filter(u => u.role === 'youth' && u.status === 'verified').map(u => u.id);
    } else if (recipientType === 'pending') {
        recipients = AppState.users.filter(u => u.role === 'youth' && u.status === 'pending').map(u => u.id);
    }
    
    sendNotification(title, message, recipients);
    document.getElementById('notif-title').value = '';
    document.getElementById('notif-message').value = '';
    loadAdminTab('notifications');
}

// Admin Posts
function renderAdminPosts() {
    return `
        <div class="page-header">
            <h2>Event Posts</h2>
            <p>Upload and manage event pictures and updates</p>
            <button class="btn btn-primary" onclick="showAddPostModal()">Add New Post</button>
        </div>

        <div class="cards-grid">
            ${AppState.eventPosts.map(post => {
                const event = getEventById(post.eventId);
                return `
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">${event ? event.title : 'Event'}</h3>
                            <span class="text-sm text-gray">${formatDate(post.date)}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.5rem; margin: 1rem 0;">
                            ${post.images.map(img => `
                                <img src="${img}" alt="Event photo" style="width: 100%; height: 150px; object-fit: cover; border-radius: 0.5rem;">
                            `).join('')}
                        </div>
                        <p>${post.caption}</p>
                    </div>
                `;
            }).join('')}
        </div>

        ${AppState.eventPosts.length === 0 ? '<div class="empty-state"><p>No event posts yet.</p></div>' : ''}
    `;
}

function showAddPostModal() {
    const content = `
        <form onsubmit="handleAddPost(event)">
            <div class="form-group">
                <label>Select Event</label>
                <select id="post-event" required>
                    <option value="">Choose an event</option>
                    ${AppState.events.map(event => `
                        <option value="${event.id}">${event.title}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Image URLs (one per line)</label>
                <textarea id="post-images" rows="3" placeholder="https://example.com/image1.jpg&#10;https://example.com/image2.jpg" required></textarea>
            </div>
            <div class="form-group">
                <label>Caption</label>
                <textarea id="post-caption" rows="3" required></textarea>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary admin">Add Post</button>
            </div>
        </form>
    `;
    showModal('Add Event Post', content);
}

function handleAddPost(event) {
    event.preventDefault();
    const eventId = document.getElementById('post-event').value;
    const images = document.getElementById('post-images').value
        .split('\n')
        .filter(url => url.trim());
    const caption = document.getElementById('post-caption').value;
    
    addEventPost(eventId, images, caption);
    closeModal();
    loadAdminTab('posts');
}

// Admin Icon Helper Function
function getAdminIcon(name) {
    const icons = {
        'home': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
        'calendar': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
        'briefcase': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>',
        'users': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
        'check-square': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>',
        'message-square': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>',
        'bell': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>',
        'image': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>',
        'user-check': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><polyline points="17 11 19 13 23 9"></polyline></svg>'
    };
    return icons[name] || '';
}
