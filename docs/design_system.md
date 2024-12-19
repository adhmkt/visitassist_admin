# Chatbot Admin Design System

## Color Palette

### Primary Colors
- Primary Blue: `#2563eb` - Used for primary actions, buttons, and key UI elements
- Secondary Blue: `#1e40af` - Used for hover states and secondary elements
- Sidebar Dark: `#1e293b` - Used for sidebar background

### Text Colors
- Primary Text: `#1e293b` - Main text color
- Secondary Text: `#64748b` - Used for subtitles and less important text
- Light Text: `#94a3b8` - Used for sidebar inactive items

### Status Colors
- Success Green: `#10b981` - Used for success states and positive metrics
- Warning Orange: `#f59e0b` - Used for warnings and attention-needed states

### Background Colors
- Main Background: `#f1f5f9` - Used for the main application background
- Card Background: `#ffffff` - Used for cards and elevated elements

## Typography

### Font Family
- Primary Font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Use system font stack for optimal performance and native feel

### Font Sizes
- Large Headings: `2rem` (32px) - Used for main page titles
- Medium Headings: `1.5rem` (24px) - Used for card titles and section headers
- Regular Text: `1rem` (16px) - Used for body text and general content
- Small Text: `0.875rem` (14px) - Used for labels and secondary information

## Layout

### Grid System
- Dashboard uses CSS Grid with `auto-fit` and `minmax`
- Card Grid: `minmax(280px, 1fr)` - Ensures cards are never too small
- Stats Grid: `minmax(240px, 1fr)` - Allows for responsive stat cards

### Spacing
- Large Spacing: `2rem` (32px) - Used for section separation
- Medium Spacing: `1.5rem` (24px) - Used for card padding
- Small Spacing: `1rem` (16px) - Used for element spacing
- Extra Small: `0.5rem` (8px) - Used for tight spacing between related elements

## Components

### Cards
```css
.card {
    background-color: var(--card-color);
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

### Buttons
```css
.action-button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
```

### Icons
- Using Font Awesome 6.4.0
- Standard icon size: `1.5rem` (24px)
- Large icon size: `2rem` (32px)
- Always use with supporting text for accessibility

## Animations

### Transitions
- Button Hover: `background-color 0.3s ease`
- Card Hover: `transform 0.3s ease`
- Navigation Hover: `all 0.3s ease`

### Hover States
- Cards: Scale up slightly (`transform: translateY(-5px)`)
- Buttons: Darken background color
- Navigation: Lighten background with opacity

## Responsive Design

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Mobile Considerations
- Sidebar collapses to hamburger menu
- Cards stack vertically
- Font sizes reduce by ~10%
- Padding/margins reduce by ~25%

## Best Practices

### Accessibility
1. Use semantic HTML elements
2. Maintain color contrast ratios (WCAG 2.1)
3. Include hover and focus states
4. Provide text alternatives for icons

### Performance
1. Use system fonts
2. Optimize transitions for 60fps
3. Lazy load non-critical content
4. Minimize DOM depth

### Code Organization
1. Use CSS variables for theme values
2. Follow BEM naming convention
3. Separate concerns (structure, style, behavior)
4. Comment complex CSS calculations 