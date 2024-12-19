# Template Standards and Implementation Guide

## Base Template Structure

All pages MUST follow this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Admin - [Page Title]</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>

<body>
    <div class="dashboard-container">
        <!-- 1. Sidebar Navigation (Required) -->
        <nav class="sidebar">
            <div class="sidebar-header">
                <i class="fas fa-robot logo-icon"></i>
                <h2>Chatbot Admin</h2>
            </div>
            <ul class="nav-links">
                <li>
                    <a href="/dashboard"><i class="fas fa-home"></i> Dashboard</a>
                </li>
                <!-- Additional nav items -->
            </ul>
        </nav>

        <!-- 2. Main Content Area (Required) -->
        <main class="main-content">
            <!-- Top Bar (Required) -->
            <header class="top-bar">
                <div class="search-bar">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search...">
                </div>
                <div class="user-profile">
                    <span class="user-name">Welcome, Admin</span>
                    <i class="fas fa-user-circle"></i>
                </div>
            </header>

            <!-- Main Content Section -->
            <div class="main-section">
                <!-- Page specific content goes here -->
            </div>
        </main>
    </div>
</body>
</html>
```

## Component Types

### 1. Dashboard Stats Layout
```html
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-icon active-users">
            <i class="fas fa-users"></i>
        </div>
        <div class="stat-details">
            <h3>Title</h3>
            <p class="stat-number">1,234</p>
        </div>
    </div>
</div>
```

### 2. Action Cards Layout
```html
<div class="action-cards">
    <div class="action-card">
        <i class="fas fa-plus-circle"></i>
        <h3>Action Title</h3>
        <p>Description text</p>
        <button class="action-button">Action Text</button>
    </div>
</div>
```

### 3. Simple Form Layout
```html
<div class="main-section">
    <h2>Section Title</h2>
    <select class="form-control">
        <option value="">Select option...</option>
    </select>
</div>
```

## CSS Classes Reference

### 1. Layout Classes
- `.dashboard-container` - Main container with flex layout
- `.sidebar` - Left navigation panel (fixed width: 260px)
- `.main-content` - Right content area (flex: 1)
- `.main-section` - Content wrapper with padding

### 2. Navigation Classes
- `.sidebar-header` - Top logo section
- `.nav-links` - Navigation items list
- `.active` - Current page indicator

### 3. Component Classes
- `.stats-container` - Grid for stat cards
- `.action-cards` - Grid for action cards
- `.form-control` - Form inputs and selects

## Spacing Standards

### Fixed Measurements
- Sidebar width: 260px
- Main padding: 2rem
- Component gaps: 1.5rem
- Form element padding: 0.75rem
- Border radius: 0.5rem (buttons, inputs), 1rem (cards)

### Colors (CSS Variables)
```css
--primary-color: #2563eb;
--secondary-color: #1e40af;
--background-color: #f1f5f9;
--sidebar-color: #1e293b;
--card-color: #ffffff;
--text-primary: #1e293b;
--text-secondary: #64748b;
--success-color: #10b981;
--warning-color: #f59e0b;
--border-color: #e2e8f0;
```

## Implementation Checklist

Before submitting any template:
- [ ] Uses exact HTML structure as shown above
- [ ] Includes all required meta tags and CSS links
- [ ] Has proper sidebar navigation
- [ ] Includes top bar with search and profile
- [ ] Uses correct CSS variables for colors
- [ ] Follows spacing standards
- [ ] Uses appropriate component structure
- [ ] Includes Font Awesome icons

## Common Mistakes to Avoid

1. DO NOT modify the base HTML structure
2. DO NOT change the sidebar width
3. DO NOT use custom colors outside CSS variables
4. DO NOT modify standard component layouts
5. DO NOT change standard padding/margin values
6. DO NOT remove required sections (sidebar, top bar)
7. DO NOT use inline styles
8. DO NOT modify border-radius values

## Responsive Behavior

The layout is designed to be fixed-width with the following structure:
- Sidebar: Fixed 260px width
- Main content: Flexible (remaining space)
- Minimum page width: 1024px