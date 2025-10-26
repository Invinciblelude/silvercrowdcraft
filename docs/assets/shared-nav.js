// Shared Navigation for Construction Management System
// This provides consistent header, bottom nav, and FAB across all pages

const SHARED_NAV_HTML = `
<style>
    /* Shared styles for header, sidebar nav, fab */
    body.jsdom-page {
        margin-top: 72px; /* Height of header */
        margin-left: 220px; /* Width of sidebar */
        background: #0a0e27; /* Dark theme background */
        color: #e8eef5;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
    }
    .jsdom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 72px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); /* Purple gradient */
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 1000;
        box-sizing: border-box;
    }
    .jsdom-header h1 {
        margin: 0;
        font-size: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-badge {
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 12px;
        margin-left: 10px;
    }
    .status-badge.online {
        background: #28a745; /* Green */
        color: #fff;
    }
    .status-badge.offline {
        background: #dc3545; /* Red */
        color: #fff;
    }
    .jsdom-sidebar-nav {
        position: fixed;
        left: 0;
        top: 72px; /* Below header */
        width: 220px;
        height: calc(100vh - 72px);
        background: #12161b;
        border-right: 1px solid #1f2630;
        display: flex;
        flex-direction: column;
        padding: 20px 0;
        box-shadow: 2px 0 8px rgba(0,0,0,0.2);
        z-index: 900;
        box-sizing: border-box;
    }
    .jsdom-nav-item {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 24px;
        color: #a9b6c6;
        text-decoration: none;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.2s;
        border-left: 4px solid transparent;
    }
    .jsdom-nav-item:hover {
        background: #1a1f2e;
        color: #9cc1ff;
    }
    .jsdom-nav-item.active {
        color: #9cc1ff;
        background: #1a1f2e;
        border-left-color: #667eea;
    }
    .jsdom-nav-item .icon {
        font-size: 24px;
        width: 28px;
        text-align: center;
    }
    .jsdom-fab {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: #dc3545; /* Red for urgency */
        color: #fff;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        cursor: pointer;
        z-index: 1001;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        body.jsdom-page {
            margin-left: 0;
            margin-bottom: 80px;
        }
        .jsdom-sidebar-nav {
            top: auto;
            bottom: 0;
            width: 100%;
            height: 80px;
            flex-direction: row;
            justify-content: space-around;
            padding: 0;
            border-right: none;
            border-top: 1px solid #1f2630;
        }
        .jsdom-nav-item {
            flex-direction: column;
            justify-content: center;
            gap: 4px;
            padding: 8px 4px;
            font-size: 12px;
            border-left: none;
            border-top: 4px solid transparent;
            flex: 1;
        }
        .jsdom-nav-item.active {
            border-left-color: transparent;
            border-top-color: #667eea;
        }
        .jsdom-fab {
            bottom: 96px;
        }
    }
</style>
<div class="jsdom-header">
    <h1 id="jsdom-page-title"></h1>
    <div id="jsdom-online-status" class="status-badge"></div>
</div>
<div class="jsdom-fab" onclick="JSDOMNav.startProblemLog()">
    🎤
</div>
<nav class="jsdom-sidebar-nav">
    <a href="index.html" class="jsdom-nav-item" data-section="dashboard">
        <span class="icon">🏗️</span>
        <span>Projects</span>
    </a>
    <a href="project.html" class="jsdom-nav-item" data-section="tasks">
        <span class="icon">✓</span>
        <span>Tasks</span>
    </a>
    <a href="blueprints.html" class="jsdom-nav-item" data-section="plans">
        <span class="icon">📐</span>
        <span>Plans</span>
    </a>
    <a href="schedule/baseline.html" class="jsdom-nav-item" data-section="schedule">
        <span class="icon">📅</span>
        <span>Schedule</span>
    </a>
</nav>
`;

// Navigation Controller
window.JSDOMNav = {
    init: function(pageName, pageTitle) {
        // Add body class
        document.body.classList.add('jsdom-page');

        // Create a temporary container
        const temp = document.createElement('div');
        temp.innerHTML = SHARED_NAV_HTML;

        // Extract each element
        const header = temp.querySelector('.jsdom-header');
        const fab = temp.querySelector('.jsdom-fab');
        const bottomNav = temp.querySelector('.jsdom-bottom-nav');

        // Insert header at the beginning
        if (header) {
            document.body.insertBefore(header, document.body.firstChild);
        }

        // Append FAB and bottom nav to the end
        if (fab) {
            document.body.appendChild(fab);
        }
        if (bottomNav) {
            document.body.appendChild(bottomNav);
        }

        // Set page title
        if (pageTitle) {
            const titleEl = document.getElementById('jsdom-page-title');
            if (titleEl) {
                titleEl.textContent = pageTitle;
            }
        }

        // Set active nav item based on current page
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        document.querySelectorAll('.jsdom-nav-item').forEach(item => {
            const href = item.getAttribute('href') || '';
            const hrefPage = href.split('/').pop();
            
            if (hrefPage === currentPage || 
                (currentPage === '' && hrefPage === 'index.html') ||
                (currentPage.includes('sop') && item.dataset.section === 'tasks')) {
                item.classList.add('active');
            }
        });

        // Initialize online status
        this.updateOnlineStatus();
        window.addEventListener('online', () => this.updateOnlineStatus());
        window.addEventListener('offline', () => this.updateOnlineStatus());
    },

    updateOnlineStatus: function() {
        const badge = document.getElementById('jsdom-online-status');
        if (badge) {
            if (navigator.onLine) {
                badge.className = 'status-badge online';
                badge.textContent = '● Online';
            } else {
                badge.className = 'status-badge offline';
                badge.textContent = '● Offline';
            }
        }
    },

    startProblemLog: function() {
        const taskName = prompt('Which task/location is this problem for?', 'Current task');
        if (taskName) {
            const problem = {
                task: taskName,
                timestamp: new Date().toISOString(),
                status: 'queued',
                page: window.location.pathname
            };

            const problems = JSON.parse(localStorage.getItem('problemLogs') || '[]');
            problems.push(problem);
            localStorage.setItem('problemLogs', JSON.stringify(problems));

            alert('🎤 Problem log recorded for: ' + taskName + '\n\nWill sync when online.');
        }
    }
};

// Auto-initialize if data-jsdom-page attribute is set on body
document.addEventListener('DOMContentLoaded', () => {
    const pageAttr = document.body.getAttribute('data-jsdom-page');
    const titleAttr = document.body.getAttribute('data-jsdom-title');
    if (pageAttr) {
        JSDOMNav.init(pageAttr, titleAttr);
    }
});
