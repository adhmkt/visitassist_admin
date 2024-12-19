# Assistant Configuration Management System

## Database Structure

### Main Assistant Fields
```json
{
    "assistant_id": "string",
    "assistant_name": "string",
    "assistant_desc": "string",
    "assistant_instructions": "string",
    "assistant_type": "string (defaults to 'classic')",
    "assistant_img": "string (direct image path)",
    "sponsor_id": "number",
    "assistant_questions": "JSON object",
    "assistant_json": "JSON object (configuration)",
    "assistant_functions": "string (defaults to 'not_defined')",
    "assistant_languages": {
        "languages": [
            {
                "language_code": "string",
                "language_name": "string",
                "version": "string"
            }
        ]
    },
    "subtype": "string",
    "sponsor_logo": "string (defaults to 'sponsor_default.png')",
    "sponsor_url": "string (defaults to 'https://apis-ia.com')"
}
```

### Configuration Structure (assistant_json)
```json
{
    "languages": {
        "en": {
            "assistant_name": "string",
            "assistant_desc": "string",
            "design_features": {
                "assistant_sidebar_img": "string",
                "assistant_splash_img": "string",
                "bg_image": "string",
                "bubble_bg_color": "string",
                "bubble_font_color": "string"
            },
            "assistant_splash_txt": "string",
            "assistant_splash_mobile_txt": "string",
            "functionalities": [
                {
                    "functionality_id": "number",
                    "functionality_text": "string",
                    "functionality_value": "string"
                }
            ]
        }
        // Additional languages follow the same structure
    }
}
```

## Key Features

### 1. Language Management
- Languages are stored in `assistant_languages` field
- Each language has a code, name, and version
- Configuration data is stored per language in `assistant_json`
- Dynamic language selector based on assistant's supported languages
- Automatic fallback to English (1.0) if no languages defined

### 2. Image Management
- Main assistant image is stored in `assistant_img` field in the database (not in configuration)
- The Assistant Image URL in the Design Features section updates the `assistant_img` field directly
- Images are served from CDN: `https://apis-ia.nyc3.cdn.digitaloceanspaces.com/static/images/assistant_imgs/`
- Additional images (sidebar, splash) are stored per language in configuration

### 3. Configuration Management
- Per-language configuration for:
  - Basic information (name, description)
  - Design features (images, colors)
  - Welcome messages (desktop and mobile)
  - Conversation starters (functionalities)
- Configuration is stored in `assistant_json` column
- Each language maintains its own set of settings

### 4. Conversation Starters
- Managed through modal interface
- Stored per language in configuration
- Supports bulk operations
- Maintains ID, text, and value for each starter
- Tracks count and last update time

## Implementation Details

### 1. Form Structure
- Main assistant fields at the top level
- Configuration section with language selector
- Subsections for different configuration aspects
- Hidden fields for JSON data storage

### 2. Data Flow
1. Assistant selection:
   - Loads basic fields from database (including `assistant_img`)
   - Populates language selector from `assistant_languages`
   - Loads configuration for first available language

2. Language switching:
   - Updates form fields with language-specific configuration
   - Maintains separate configuration per language
   - Preserves existing data when switching languages
   - Keeps `assistant_img` field unchanged as it's language-independent

3. Saving:
   - Collects form data
   - Updates `assistant_img` directly in the database
   - Maintains separate structures for other fields and configuration
   - Updates both database fields and configuration JSON

### 3. Image Handling
- Main assistant image (`assistant_img`):
  - Stored directly in database as a separate field
  - Modified through the Assistant Image URL in Design Features
  - Used for directory and main display
  - Served from CDN
  - Language-independent

- Language-specific images:
  - Stored in configuration JSON
  - Can be different per language
  - Include only sidebar and splash images

## Best Practices

### 1. Data Management
- Keep main assistant image in `assistant_img` field (database field, not in configuration)
- Store only language-specific images in configuration
- Maintain version numbers for languages
- Use proper JSON structure for configuration

### 2. Language Support
- Always provide English as fallback
- Include version numbers with languages
- Keep language codes consistent
- Maintain complete configuration for each language

### 3. Configuration Updates
- Preserve existing data when updating
- Validate JSON structures
- Handle missing or invalid data gracefully
- Maintain backward compatibility

## Security Considerations

1. Input Validation
   - Validate all form inputs
   - Sanitize HTML content
   - Verify image URLs
   - Check JSON structure

2. Access Control
   - Authenticate all edit requests
   - Validate permissions
   - Log configuration changes

3. Data Protection
   - Validate JSON before saving
   - Handle errors gracefully
   - Maintain data integrity

## Future Enhancements

1. Planned Features
   - Image upload capability
   - Version control for configurations
   - Configuration templates
   - Bulk language operations

2. Improvements
   - Enhanced validation
   - Preview capabilities
   - Backup system
   - Change tracking