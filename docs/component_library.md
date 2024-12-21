# Component Library

## Overview
This document catalogs all reusable components in the Admin Panel application, providing examples and usage guidelines.

## Navigation Components

### Sidebar
The main navigation component present in all pages.

```html
<div class="sidebar">
    <div class="sidebar-header">
        <i class="fas fa-robot logo-icon"></i>
        <h3>Admin Panel</h3>
    </div>
    <ul class="nav-links">
        <li class="{{ 'active' if request.endpoint == 'route_name' }}">
            <a href="{{ url_for('route_name') }}">
                <i class="fas fa-icon"></i>
                <span>Link Text</span>
            </a>
        </li>
    </ul>
</div>
```

CSS Dependencies:
```css
.sidebar {
    width: 260px;
    min-height: 100vh;
    background-color: var(--sidebar-color);
    color: white;
    padding: 1.5rem;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
}
```

## Content Components

### Page Header
Standard header for all content pages.

```html
<div class="content-header">
    <h1>Page Title</h1>
    <div class="header-actions">
        <button class="btn btn-primary">
            <i class="fas fa-plus"></i>
            <span>Action</span>
        </button>
    </div>
</div>
```

### Search Section
Reusable search component with filters.

```html
<div class="search-section">
    <div class="search-bar">
        <i class="fas fa-search"></i>
        <input type="text" placeholder="Search...">
    </div>
    <div class="filters">
        <div class="filter-group">
            <label>Filter:</label>
            <select>
                <option value="">All</option>
            </select>
        </div>
    </div>
</div>
```

### Data Table
Standard table for displaying data.

```html
<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Column Header</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Cell Content</td>
            </tr>
        </tbody>
    </table>
</div>
```

### Modal
Reusable modal component.

```html
<div class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Modal Title</h2>
            <button class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
            <!-- Content -->
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary">Cancel</button>
            <button class="btn btn-primary">Save</button>
        </div>
    </div>
</div>
```

## Form Components

### Input Group
Standard form input with label.

```html
<div class="form-group">
    <label for="input-id">Label</label>
    <input type="text" id="input-id" name="input-name">
</div>
```

### Select Group
Dropdown select with label.

```html
<div class="form-group">
    <label for="select-id">Label</label>
    <select id="select-id" name="select-name">
        <option value="">Select option</option>
    </select>
</div>
```

### Form Row
Group multiple form elements horizontally.

```html
<div class="form-row">
    <div class="form-group">
        <label>First Input</label>
        <input type="text">
    </div>
    <div class="form-group">
        <label>Second Input</label>
        <input type="text">
    </div>
</div>
```

## Button Components

### Primary Button
```html
<button class="btn btn-primary">
    <i class="fas fa-icon"></i>
    <span>Button Text</span>
</button>
```

### Secondary Button
```html
<button class="btn btn-secondary">
    <i class="fas fa-icon"></i>
    <span>Button Text</span>
</button>
```

### Icon Button
```html
<button class="btn btn-icon">
    <i class="fas fa-icon"></i>
</button>
```

## Loading States

### Loading Spinner
```html
<div class="loading-message">
    <i class="fas fa-spinner fa-spin"></i>
    <span>Loading...</span>
</div>
```

### Loading Overlay
```html
<div class="loading-overlay">
    <div class="spinner">
        <i class="fas fa-spinner fa-spin"></i>
    </div>
</div>
```

## Status Indicators

### Status Badge
```html
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-danger">Error</span>
```

## Usage Guidelines

1. Component Consistency
   - Use the exact HTML structure as documented
   - Maintain class names for proper styling
   - Follow component nesting patterns

2. Styling Rules
   - Use CSS variables for colors and spacing
   - Maintain responsive behavior
   - Keep component-specific styles modular

3. JavaScript Integration
   - Use data attributes for JavaScript hooks
   - Follow event delegation patterns
   - Maintain component state properly

4. Accessibility
   - Include proper ARIA labels
   - Maintain keyboard navigation
   - Ensure proper contrast ratios

5. Performance
   - Minimize DOM nesting
   - Use efficient selectors
   - Optimize for reflows and repaints

## Component Development

When creating new components:

1. Document the component structure
2. Include usage examples
3. List dependencies
4. Provide styling guidelines
5. Add accessibility requirements
6. Include responsive considerations
7. Update this documentation 