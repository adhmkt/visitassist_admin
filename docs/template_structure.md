# Template Structure and Design Standards

## Overview
This document outlines the standard structure for templates in the Admin Panel application, ensuring consistency across all pages and future implementations.

## Base Template Structure
The application uses a modular template system with a consistent layout:

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} - Admin Panel</title>
    <!-- Core CSS (Required) -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
    <!-- Font Awesome Icons (Required) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <!-- Page-specific CSS -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="dashboard-container">
        <!-- Sidebar Module -->
        {% include 'sidebar.html' %}
        <!-- Main Content Area -->
        <div class="content-wrapper">
            {% block content %}{% endblock %}
        </div>
    </div>
    <!-- Core JavaScript (Required) -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <!-- Page-specific JavaScript -->
    {% block scripts %}{% endblock %}
</body>
</html>
```

## Sidebar Module
The sidebar is a reusable component included in all pages:

```html
<!-- sidebar.html -->
<div class="sidebar">
    <div class="sidebar-header">
        <i class="fas fa-robot logo-icon"></i>
        <h3>Admin Panel</h3>
    </div>
    <ul class="nav-links">
        <!-- Navigation Items -->
    </ul>
</div>
```

## Page Template Structure
Each page should follow this structure:

```html
<!-- example_page.html -->
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block extra_css %}
<!-- Only if page needs additional CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/page_specific.css') }}">
{% endblock %}

{% block content %}
<!-- Content Header -->
<div class="content-header">
    <h1>Page Title</h1>
    <!-- Optional Action Buttons -->
</div>

<!-- Main Content -->
<div class="content-body">
    <!-- Page-specific content -->
</div>
{% endblock %}

{% block scripts %}
<!-- Only if page needs additional JavaScript -->
<script src="{{ url_for('static', filename='js/page_specific.js') }}"></script>
{% endblock %}
```

## CSS Structure
The application uses a single core CSS file (`dashboard.css`) for global styles:

### Core Styles (`dashboard.css`)
- Reset and base styles
- CSS variables (theme colors)
- Layout structure (dashboard container, sidebar, content wrapper)
- Common components (buttons, headers)
- Responsive design rules

### Page-specific CSS
- Should only contain styles unique to that page
- Must use the same CSS variables defined in dashboard.css
- Should follow the same naming conventions

## Design Standards

### Layout
- Fixed sidebar (260px width)
- Content wrapper with left margin matching sidebar width
- Responsive design (sidebar collapses to icons on mobile)
- Consistent padding and spacing

### Colors
Use CSS variables for consistency:
```css
:root {
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
}
```

### Typography
- Font family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Consistent heading sizes:
  - Page titles: 1.8rem
  - Section headings: 1.25rem
  - Card titles: 1rem

### Components

#### Content Header
```html
<div class="content-header">
    <h1>Page Title</h1>
    <div class="header-actions">
        <!-- Action buttons -->
    </div>
</div>
```

#### Cards
```html
<div class="card">
    <div class="card-header">
        <h2 class="card-title">Title</h2>
    </div>
    <div class="card-body">
        <!-- Card content -->
    </div>
</div>
```

#### Buttons
```html
<button class="btn btn-primary">
    <i class="fas fa-icon"></i>
    <span>Button Text</span>
</button>
```

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Implementation Guidelines

1. Always extend the base template
2. Include only page-specific styles in extra_css block
3. Use the established CSS variables for colors
4. Follow the component structure for consistency
5. Maintain responsive design considerations
6. Use semantic HTML elements
7. Keep JavaScript modular and page-specific

## Future Considerations

When adding new templates:
1. Review this documentation
2. Use the established structure
3. Reuse existing components when possible
4. Add new components to this documentation if created
5. Maintain consistency with existing pages
6. Test responsive behavior
7. Update documentation if patterns evolve 