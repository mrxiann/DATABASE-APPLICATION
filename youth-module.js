// Youth Dashboard Initialization
let currentYouthTab = 'home';

function initYouthDashboard() {
    // This line and all others relying on AppState will cause a ReferenceError
    // if the global AppState object is not defined *before* this module loads.
    document.getElementById('youth-user-name').textContent = AppState.currentUser.name;
    renderYouthNav();
    loadYouthTab('home');
}

function renderYouthNav() {
    const unreadCount = AppState.notifications.filter(n => 
        !n.read && (n.recipients.includes('all') || n.recipients.includes(AppState.currentUser.id))
    ).length;

    const navItems = [
        { id: 'home', label: 'Home', icon: 'home' },
        { id: 'events', label: 'Events', icon: 'calendar' },
        { id: 'opportunities', label: 'Opportunities', icon: 'briefcase' },
        { id: 'feedback', label: 'Feedback', icon: 'message-square' },
        { id: 'notifications', label: 'Notifications', icon: 'bell', badge: unreadCount },
        { id: 'profile', label: 'Profile', icon: 'user' },
        { id: 'qrcode', label: 'QR Code', icon: 'qrcode' } // New QR Code Tab
    ];

    const navHTML = navItems.map(item => `
        <button class="nav-item ${currentYouthTab === item.id ? 'active' : ''}" onclick="loadYouthTab('${item.id}')">
            ${getIcon(item.icon)}
            <span>${item.label}</span>
            ${item.badge && item.badge > 0 ? `<span class="nav-badge">${item.badge}</span>` : ''}
        </button>
    `).join('');

    document.getElementById('youth-nav').innerHTML = navHTML;
}

function loadYouthTab(tabId) {
    currentYouthTab = tabId;
    renderYouthNav();

    const contentDiv = document.getElementById('youth-content');
    
    // Clear content and add loading state for a smoother transition
    contentDiv.innerHTML = '<div class="loading">Loading...</div>';

    // Simulate a small delay for content loading (optional, for modern feel)
    setTimeout(() => {
        switch(tabId) {
            case 'home':
                contentDiv.innerHTML = renderYouthHome();
                break;
            case 'events':
                contentDiv.innerHTML = renderYouthEvents();
                break;
            case 'opportunities':
                contentDiv.innerHTML = renderYouthOpportunities();
                break;
            case 'feedback':
                contentDiv.innerHTML = renderYouthFeedback();
                break;
            case 'notifications':
                contentDiv.innerHTML = renderYouthNotifications();
                break;
            case 'profile':
                contentDiv.innerHTML = renderYouthProfile();
                break;
            case 'qrcode':
                contentDiv.innerHTML = renderYouthQRCode();
                // Special handling for QR code generation
                // Check if the tab is being loaded *into* the DOM
                setTimeout(() => {
                    const qrCodeValue = AppState.currentUser.qrCode;
                    if (qrCodeValue) {
                        // initQRCode relies on the global function and the external QRCode library
                        initQRCode(qrCodeValue);
                    }
                }, 0);
                break;
            default:
                contentDiv.innerHTML = '<div class="empty-state"><p>Page not found.</p></div>';
        }
    }, 100); 
}

// Youth Home
function renderYouthHome() {
    const upcomingEvents = AppState.events.filter(e => e.status === 'upcoming').slice(0, 3);
    const myNotifications = AppState.notifications
        .filter(n => n.recipients.includes('all') || n.recipients.includes(AppState.currentUser.id))
        .slice(0, 3);
    const recentPosts = AppState.eventPosts.slice(-2);

    return `
        <div class="page-header">
            <h2>Welcome back, ${AppState.currentUser.name}!</h2>
            <p>Here's what's happening in your community</p>
        </div>

        <div class="cards-grid">
            <div class="stat-card">
                <div class="stat-icon blue">
                    ${getIcon('calendar')}
                </div>
                <div class="stat-label">Events Attended</div>
                <div class="stat-value">${AppState.currentUser.eventsAttended}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon green">
                    ${getIcon('star')}
                </div>
                <div class="stat-label">Activity Score</div>
                <div class="stat-value">${AppState.currentUser.activityScore}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon orange">
                    ${getIcon('award')}
                </div>
                <div class="stat-label">Status</div>
                <div class="stat-value">${AppState.currentUser.status === 'verified' ? 'Verified' : 'Pending'}</div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Upcoming Events</h3>
                <button class="btn btn-sm btn-primary" onclick="loadYouthTab('events')">View All ${getIcon('arrow-right')}</button>
            </div>
            ${upcomingEvents.length > 0 ? `
                <div class="cards-grid">
                    ${upcomingEvents.map(event => renderEventCard(event, true)).join('')}
                </div>
            ` : '<div class="empty-state"><p>No upcoming events at the moment.</p></div>'}
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Recent Updates</h3>
                <button class="btn btn-sm btn-secondary" onclick="loadYouthTab('notifications')">View Notifications ${getIcon('arrow-right')}</button>
            </div>
            ${myNotifications.length > 0 ? 
                myNotifications.map(notif => `
                    <div class="notification-item ${!notif.read ? 'unread' : ''}" onclick="handleMarkAsRead('${notif.id}', true)">
                        <div class="notification-header">
                            <div class="notification-title">${notif.title}</div>
                            <div class="notification-date">${formatDate(notif.date)}</div>
                        </div>
                        <div class="notification-message">${notif.message}</div>
                    </div>
                `).join('') 
                : '<div class="empty-state"><p>No recent notifications.</p></div>'
            }
        </div>

        ${recentPosts.length > 0 ? `
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Recent Event Posts</h3>
                </div>
                ${recentPosts.map(post => {
                    const event = getEventById(post.eventId);
                    return `
                        <div style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--gray-100); padding-bottom: 1rem;">
                            <h4 style="font-weight: 600; color: var(--gray-800); font-size: 1rem;">${event ? event.title : 'Event'}</h4>
                            <p class="text-gray text-sm">${formatDate(post.date)}</p>
                            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.75rem; margin: 0.75rem 0;">
                                ${post.images.map(img => `
                                    <img src="${img}" alt="Event photo" style="width: 100%; height: 160px; object-fit: cover; border-radius: 0.4rem; border: 1px solid var(--gray-200);">
                                `).join('')}
                            </div>
                            <p class="text-gray text-sm">${post.caption}</p>
                        </div>
                    `;
                }).join('')}
            </div>
        ` : ''}
    `;
}

// Youth Events
function renderYouthEvents() {
    const upcomingEvents = AppState.events.filter(e => e.status === 'upcoming');
    const completedEvents = AppState.events.filter(e => e.status === 'completed');

    return `
        <div class="page-header">
            <h2>Events</h2>
            <p>Browse and join upcoming community events</p>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Upcoming Events</h3>
            </div>
            ${upcomingEvents.length > 0 ? `
                <div class="cards-grid">
                    ${upcomingEvents.map(event => renderEventCard(event, true)).join('')}
                </div>
            ` : '<div class="empty-state"><p>No upcoming events at the moment.</p></div>'}
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Past Events</h3>
            </div>
            ${completedEvents.length > 0 ? `
                <div class="cards-grid">
                    ${completedEvents.map(event => renderEventCard(event, false)).join('')}
                </div>
            ` : '<div class="empty-state"><p>No past events.</p></div>'}
        </div>
    `;
}

function renderEventCard(event, showJoinButton) {
    const isJoined = event.attendees.includes(AppState.currentUser.id);
    const isFull = event.attendees.length >= event.maxCapacity;

    return `
        <div class="event-card">
            <img src="${event.imageUrl}" alt="${event.title}" class="event-image">
            <div class="event-content">
                <span class="event-category">${event.category}</span>
                <h3 class="event-title">${event.title}</h3>
                <p class="event-description">${event.description.substring(0, 80)}...</p>
                <div class="event-meta">
                    <div class="event-meta-item">
                        ${getIcon('calendar')}
                        <span>${formatDate(event.date)} at ${event.time}</span>
                    </div>
                    <div class="event-meta-item">
                        ${getIcon('map-pin')}
                        <span>${event.location}</span>
                    </div>
                </div>
                <div class="event-footer">
                    <span class="attendees-count">${event.attendees.length}/${event.maxCapacity} attendees</span>
                    ${showJoinButton ? (
                        isJoined 
                            ? '<span class="badge badge-success">Joined</span>'
                            : (isFull 
                                ? '<span class="badge badge-danger">Full</span>'
                                : `<button class="btn btn-sm btn-primary" onclick="handleJoinEvent('${event.id}')">${getIcon('plus-circle')} Join Event</button>`
                            )
                    ) : ''}
                </div>
            </div>
        </div>
    `;
}

function handleJoinEvent(eventId) {
    // joinEvent must be defined globally for this to work
    joinEvent(eventId, AppState.currentUser.id);
    loadYouthTab('events');
}

// Youth Opportunities
function renderYouthOpportunities() {
    const openOpportunities = AppState.opportunities.filter(o => o.status === 'open');

    return `
        <div class="page-header">
            <h2>Opportunities</h2>
            <p>Explore volunteer and job opportunities</p>
        </div>

        <div class="cards-grid">
            ${openOpportunities.map(opp => renderOpportunityCard(opp)).join('')}
        </div>

        ${openOpportunities.length === 0 ? '<div class="empty-state">' + getIcon('alert-triangle') + '<p>No opportunities available at the moment.</p></div>' : ''}
    `;
}

function renderOpportunityCard(opp) {
    const hasApplied = opp.applicants.includes(AppState.currentUser.id);
    const isFull = opp.applicants.length >= opp.slots;

    return `
        <div class="opportunity-card">
            <div class="opportunity-content">
                <span class="opportunity-type ${opp.type}">${opp.type === 'job' ? 'JOB' : 'VOLUNTEER'}</span>
                <h3 class="opportunity-title">${opp.title}</h3>
                <p class="opportunity-description">${opp.description.substring(0, 100)}...</p>
                <div class="opportunity-meta">
                    <div class="opportunity-meta-item">
                        ${getIcon('calendar')}
                        <span>Deadline: ${formatDate(opp.deadline)}</span>
                    </div>
                    <div class="opportunity-meta-item">
                        ${getIcon('users')}
                        <span>Slots: ${opp.applicants.length}/${opp.slots} filled</span>
                    </div>
                </div>
                <div style="margin: 0.75rem 0;">
                    <strong class="text-gray-700 text-sm">Requirements:</strong>
                    <ul style="margin-left: 1rem; margin-top: 0.4rem; font-size: 0.8rem; color: var(--gray-600);">
                        ${opp.requirements.map(req => `<li>${req}</li>`).join('')}
                    </ul>
                </div>
                <div class="opportunity-footer">
                    ${hasApplied 
                        ? '<span class="badge badge-success">Applied</span>'
                        : (isFull 
                            ? '<span class="badge badge-danger">Full</span>'
                            : `<button class="btn btn-sm btn-primary" onclick="handleApplyOpportunity('${opp.id}')">${getIcon('send')} Apply Now</button>`
                        )
                    }
                </div>
            </div>
        </div>
    `;
}

function handleApplyOpportunity(oppId) {
    // applyToOpportunity must be defined globally for this to work
    applyToOpportunity(oppId, AppState.currentUser.id);
    loadYouthTab('opportunities');
}

// Youth Feedback
function renderYouthFeedback() {
    const myFeedbacks = AppState.feedbacks.filter(f => f.userId === AppState.currentUser.id);

    return `
        <div class="page-header">
            <h2>Feedback</h2>
            <p>Share your thoughts and suggestions with the administration.</p>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">${getIcon('edit-2')} Submit New Feedback</h3>
            </div>
            <form onsubmit="handleSubmitFeedback(event)">
                <div class="form-group">
                    <label for="feedback-message">Your Message</label>
                    <textarea id="feedback-message" rows="4" placeholder="Share your feedback, suggestions, or concerns..." required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">${getIcon('send')} Submit Feedback</button>
            </form>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">${getIcon('clock')} My Feedback History</h3>
            </div>
            ${myFeedbacks.length > 0 ? 
                myFeedbacks.map(feedback => `
                    <div class="feedback-item">
                        <div class="feedback-header">
                            <span class="feedback-user">${feedback.userName}</span>
                            <span class="badge badge-${feedback.status === 'replied' ? 'success' : 'warning'}">
                                ${feedback.status === 'replied' ? 'Replied' : 'Pending'}
                            </span>
                        </div>
                        <div class="text-gray text-sm">${formatDate(feedback.date)}</div>
                        <div class="feedback-message">${feedback.message}</div>
                        ${feedback.reply ? `
                            <div class="feedback-reply">
                                <div class="feedback-reply-label">Official Reply:</div>
                                <div>${feedback.reply}</div>
                            </div>
                        ` : ''}
                    </div>
                `).join('') 
                : '<div class="empty-state"><p>No feedback submitted yet.</p></div>'
            }
        </div>
    `;
}

function handleSubmitFeedback(event) {
    event.preventDefault();
    const message = document.getElementById('feedback-message').value;
    if (message.trim() === '') return;
    // submitFeedback must be defined globally for this to work
    submitFeedback(AppState.currentUser.id, AppState.currentUser.name, message);
    document.getElementById('feedback-message').value = '';
    loadYouthTab('feedback');
}

// Youth Notifications
function renderYouthNotifications() {
    const myNotifications = AppState.notifications.filter(n => 
        n.recipients.includes('all') || n.recipients.includes(AppState.currentUser.id)
    ).sort((a, b) => new Date(b.date) - new Date(a.date)); // Sort descending by date

    return `
        <div class="page-header">
            <h2>Notifications</h2>
            <p>Stay updated with the latest announcements and important information.</p>
        </div>

        <div class="card" style="padding: 0.5rem;">
            ${myNotifications.length > 0 ? 
                myNotifications.map(notif => `
                    <div class="notification-item ${!notif.read ? 'unread' : ''}" onclick="handleMarkAsRead('${notif.id}')">
                        <div class="notification-header">
                            <div class="notification-title">${notif.title}</div>
                            <div class="notification-date">${formatDate(notif.date)}</div>
                        </div>
                        <div class="notification-message">${notif.message}</div>
                        ${!notif.read ? '<div class="text-sm" style="color: var(--youth-primary); margin-top: 0.4rem; font-weight: 500;">New - Click to mark as read</div>' : ''}
                    </div>
                `).join('') 
                : '<div class="empty-state">' + getIcon('bell') + '<p>No notifications yet. You are all caught up!</p></div>'
            }
        </div>
    `;
}

function handleMarkAsRead(notifId, stayOnHome = false) {
    // markNotificationRead must be defined globally for this to work
    markNotificationRead(notifId);
    if (!stayOnHome) {
        loadYouthTab('notifications');
    }
    renderYouthNav(); // Update badge count
}

// Youth Profile
function renderYouthProfile() {
    return `
        <div class="page-header">
            <h2>My Profile</h2>
            <p>View and manage your personal and security information.</p>
        </div>

        <div class="cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));"> 
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">${getIcon('user')} Personal Information</h3>
                </div>
                <div style="display: grid; gap: 0.8rem;">
                    
                    <div class="profile-detail-item">
                        <div class="stat-label">Full Name</div>
                        <div class="text-base" style="font-weight: 600;">${AppState.currentUser.name}</div>
                    </div>
                    
                    <div class="profile-detail-item">
                        <div class="stat-label">Email Address</div>
                        <div class="text-base" style="font-weight: 600;">${AppState.currentUser.email}</div>
                    </div>

                    <div class="profile-detail-item">
                        <div class="stat-label">Status</div>
                        <div class="text-base">
                            <span class="badge badge-${AppState.currentUser.status === 'verified' ? 'success' : 'warning'}">
                                ${AppState.currentUser.status === 'verified' ? 'Verified' : 'Pending Verification'}
                            </span>
                        </div>
                    </div>
                    
                    <div class="profile-detail-item">
                        <div class="stat-label">Last Active</div>
                        <div class="text-base" style="font-weight: 600;">${formatDate(AppState.currentUser.lastActive)}</div>
                    </div>

                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">${getIcon('lock')} Account Security</h3>
                </div>
                <p class="text-gray text-sm">Manage your password and security settings.</p>
                <button class="btn btn-secondary" style="margin-top: 1rem;">Change Password</button>
            </div>
        </div>
    `;
}
// Global function to render the Youth QR Code HTML
function renderYouthQRCode() {
    // Note: AppState.currentUser.qrCode is the data we want to encode.
    const qrCodeValue = AppState.currentUser.qrCode;

    return `
        <div class="page-header">
            <h2>My QR Code</h2>
            <p>Show this code for quick check-in at events and activities.</p>
        </div>

        <div class="card qr-code-section">
            <div class="qr-code-display">
                <div id="qrcode-canvas" class="qr-code-placeholder">
                    <p class="text-sm text-gray">Loading QR Code...</p>
                </div>
                <div class="qr-code-text">${qrCodeValue}</div>
                <p class="text-sm text-gray" style="margin-top: 0.5rem;">Unique Youth ID: ${AppState.currentUser.id}</p>
            </div>
            
            <div class="action-buttons">
                <button class="btn btn-success" onclick="downloadQRCode('${qrCodeValue}')">${getIcon('download')} Download QR</button>
                <button class="btn btn-secondary" onclick="shareQRCode('${qrCodeValue}')">${getIcon('share-2')} Share Code</button>
            </div>
        </div>
    `;
}

// NEW FUNCTION: Initializes the QR code using the qrcode.js library
function initQRCode(qrCodeValue) {
    const canvasElement = document.getElementById("qrcode-canvas");
    
    // Check if the qrcode.js library is loaded and the container element exists
    // The issue here is if QRCode is not a globally available object
    if (typeof QRCode !== 'undefined' && canvasElement) {
        // Clear the "Loading..." placeholder text
        canvasElement.innerHTML = '';
        
        // Create a new QR Code instance
        new QRCode(canvasElement, {
            text: qrCodeValue,
            width: 160, // Set the size (match CSS)
            height: 160,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H // High error correction level
        });
    }
}

function downloadQRCode(qrCodeValue) {
    // To implement a real download, you would need to find the canvas 
    // or image element generated by qrcode.js and use its data URL.
    alert(`Simulating download of QR Code for: ${qrCodeValue}`);
}

function shareQRCode(qrCodeValue) {
    // Placeholder for sharing logic (e.g., Web Share API or platform-specific methods)
    if (navigator.share) {
        navigator.share({
            title: 'My Youth Portal QR Code',
            text: `My Youth Portal check-in code is: ${qrCodeValue}.`,
            url: window.location.href, // Or a specific link to the profile
        }).then(() => console.log('Successful share')).catch((error) => console.log('Error sharing', error));
    } else {
        alert(`Simulating share of QR Code. Code: ${qrCodeValue}`);
    }
}


// Icon Helper Function
function getIcon(name) {
    const icons = {
        'home': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
        'calendar': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
        'briefcase': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>',
        'message-square': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>',
        'bell': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>',
        'user': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>',
        'star': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
        'award': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>',
        'map-pin': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>',
        'users': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
        'qrcode': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect><line x1="17" y1="17" x2="17" y2="17"></line><line x1="17" y1="10" x2="17" y2="10"></line><line x1="10" y1="17" x2="10" y2="17"></line><line x1="10" y1="10" x2="10" y2="10"></line></svg>',
        'download': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
        'share-2': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.42" y1="6.51" x2="8.59" y2="10.49"></line></svg>',
        'activity': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>',
        'lock': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
        'edit-2': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>',
        'clock': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
        'plus-circle': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>',
        'send': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>',
        'arrow-right': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>',
        'alert-triangle': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12" y2="17"></line></svg>',
    };
    return icons[name] || '';
}