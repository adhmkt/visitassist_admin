# Functionality Modal Documentation

## Overview
The Functionality Modal is a component used for managing conversation starters (functionalities) for assistants. It provides a comprehensive interface for viewing, editing, and managing functionalities across different languages.

## Features
- Language-specific functionality management
- Real-time editing capabilities
- Bulk actions support
- Search and sort functionalities
- Side-by-side editing interface

## Component Structure

### Modal Layout
```html
<div class="modal">
    <div class="modal-content">
        <!-- Header Section -->
        <div class="modal-header">
            <div class="header-top">
                <h2>Manage Conversation Starters</h2>
                <div class="language-selector">
                    <label for="languageSelect">Language:</label>
                    <select id="languageSelect"></select>
                </div>
            </div>
            <div class="header-controls">
                <div class="search-filter">
                    <input type="text" placeholder="Search conversation starters...">
                    <select>
                        <option value="id">Sort by ID</option>
                        <option value="text">Sort by Text</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="modal-body">
            <div class="content-layout">
                <!-- Functionalities Table -->
                <div class="table-container">
                    <table>
                        <!-- Table content -->
                    </table>
                </div>
                <!-- Edit Form -->
                <div class="edit-form">
                    <!-- Form content -->
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
            <!-- Action buttons -->
        </div>
    </div>
</div>
```

## Usage

### Opening the Modal
```javascript
// Get the functionality modal instance
const functionalityModal = window.functionalityModal;

// Open the modal with required parameters
functionalityModal.open(
    languages,           // Array of language objects
    functionalitiesByLang,  // Object containing functionalities by language
    assistantId         // String: The ID of the current assistant
);
```

### Data Structures

#### Language Object
```javascript
{
    language_code: "en",
    language_name: "English",
    version: "1.0"
}
```

#### Functionality Object
```javascript
{
    id: number,
    text: string,
    value: string
}
```

## Integration

### Required Files
- `functionality_modal.js` - Main component logic
- `functionality_modal.css` - Component styles

### Template Integration
```html
<!-- Include in your template -->
<script src="{{ url_for('static', filename='js/functionality_modal.js') }}"></script>
<link rel="stylesheet" href="{{ url_for('static', filename='css/functionality_modal.css') }}">
```

## Features

### 1. Language Management
- Switch between different languages
- Maintain separate functionality sets per language
- Automatic content saving when switching languages

### 2. Functionality Editing
- Real-time updates
- Side-by-side editing interface
- Form validation
- Auto-save functionality

### 3. Search and Sort
- Search across all fields
- Sort by ID or text
- Real-time filtering

### 4. Bulk Actions
- Select multiple functionalities
- Copy to other languages
- Delete selected items
- Import/Export capabilities

## API Endpoints

### Get Functionality
```
GET /api/assistant-functionalities/:assistantId/:functionalityId/:language
```

### Update Functionality
```
POST /api/update-functionalities
Body: {
    assistantId: string,
    configUpdates: object,
    dbUpdates: array
}
```

## Best Practices

1. State Management
   - Always use the global modal instance
   - Maintain proper state synchronization
   - Handle language switches properly

2. Error Handling
   - Validate input data
   - Show appropriate error messages
   - Handle API errors gracefully

3. Performance
   - Implement debouncing for search
   - Optimize table rendering
   - Cache functionality data

4. Accessibility
   - Maintain keyboard navigation
   - Provide proper ARIA labels
   - Ensure proper focus management

## CSS Customization

### Layout
```css
.content-layout {
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 20px;
    height: 100%;
}

.table-container {
    height: 600px; /* Shows approximately 12 rows */
}
```

### Responsive Behavior
- Table scrolls horizontally on smaller screens
- Edit form moves below table on mobile
- Maintains usability across devices

## Event Handling

### Form Events
- Input changes trigger auto-save
- Language changes save current state
- Search input triggers filtered view
- Sort selection updates table order

### Modal Events
- Close button resets state
- Save button updates database
- Cancel button reverts changes
- Bulk action triggers batch operations

## Troubleshooting

Common Issues:
1. Invalid Assistant ID
   - Ensure assistant ID is passed correctly
   - Verify assistant exists in database

2. Language Switching
   - Save changes before switching
   - Verify language data structure

3. Functionality Updates
   - Check API endpoint availability
   - Verify data format
   - Handle network errors

## Future Enhancements

1. Planned Features
   - Drag-and-drop reordering
   - Advanced filtering options
   - Batch editing capabilities
   - Version history

2. Improvements
   - Enhanced validation
   - Better error reporting
   - Performance optimizations
   - Accessibility enhancements 