# Component Documentation

## Navigation Components

### Sidebar Navigation
The sidebar navigation provides the main application navigation structure.

```html
<nav class="sidebar">
    <div class="sidebar-header">
        <i class="fas fa-robot logo-icon"></i>
        <h2>Chatbot Admin</h2>
    </div>
    <ul class="nav-links">
        <li class="active">
            <a href="#"><i class="fas fa-home"></i> Dashboard</a>
        </li>
        <!-- Additional nav items -->
    </ul>
</nav>
```

### Top Bar
The top bar contains search functionality and user profile information.

```html
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
```

## Card Components

### Stat Card
Used for displaying metrics and statistics.

```html
<div class="stat-card">
    <div class="stat-icon active-users">
        <i class="fas fa-users"></i>
    </div>
    <div class="stat-details">
        <h3>Active Users</h3>
        <p class="stat-number">1,234</p>
    </div>
</div>
```

### Action Card
Used for primary actions and features.

```html
<div class="action-card">
    <i class="fas fa-plus-circle"></i>
    <h3>Create Agent</h3>
    <p>Create a new chatbot agent</p>
    <button class="action-button">Create New</button>
</div>
```

## Form Components

### Search Input
Standard search input with icon.

```html
<div class="search-bar">
    <i class="fas fa-search"></i>
    <input type="text" placeholder="Search...">
</div>
```

### Login Form
Basic authentication form.

```html
<form id="loginForm">
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
    </div>
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
    </div>
    <button type="submit">Login</button>
</form>
```

## Usage Guidelines

### Stat Cards
- Always include an icon representing the metric
- Use appropriate color coding for different types of metrics
- Keep numbers formatted consistently
- Update numbers in real-time when possible

### Action Cards
- Use clear, action-oriented titles
- Include descriptive icons
- Keep descriptions concise
- Use consistent button styling

### Navigation
- Highlight current section
- Keep items ordered by importance
- Include appropriate icons
- Maintain consistent spacing

### Forms
- Include proper validation
- Show error states clearly
- Use consistent input styling
- Include helper text when needed

## JavaScript Integration

### Event Handling
```javascript
// Example of action button handling
const actionButtons = document.querySelectorAll('.action-button');
actionButtons.forEach(button => {
    button.addEventListener('click', handleActionButton);
});
```

### State Management
```javascript
// Example of component state management
function updateStatCard(cardId, newValue) {
    const statNumber = document.querySelector(`#${cardId} .stat-number`);
    if (statNumber) {
        statNumber.textContent = newValue;
    }
}
```

## Accessibility Features

### ARIA Labels
```html
<!-- Example of ARIA implementation -->
<button class="action-button" aria-label="Create new agent">
    Create New
</button>
```

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Use proper focus states
- Maintain logical tab order

## Responsive Behavior

### Mobile Adaptations
- Cards stack vertically
- Sidebar collapses to menu
- Touch-friendly tap targets
- Adjusted font sizes

### Tablet Adaptations
- Two-column card layout
- Condensed sidebar
- Optimized spacing 