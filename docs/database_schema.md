# Places Database Schema Documentation

## Overview
This document outlines the database schema used to store Google Places API data in our Supabase (PostgreSQL) database. The schema is designed to efficiently store and retrieve place information while maintaining data integrity through relationships.

## Tables Structure

### 1. places
Primary table storing core place information.

| Column | Type | Description | Notes |
|--------|------|-------------|--------|
| id | BIGINT | Internal primary key | Auto-incrementing |
| place_id | TEXT | Google Places unique identifier | NOT NULL |
| name | VARCHAR(255) | Place name | NOT NULL |
| rating | NUMERIC | Average rating | Range: 0.0 - 5.0 |
| user_ratings_total | INTEGER | Total number of ratings | |
| formatted_address | TEXT | Full address | |
| formatted_phone_number | VARCHAR(50) | Local format phone | |
| international_phone_number | VARCHAR(50) | International format phone | |
| website | TEXT | Official website URL | |
| business_status | VARCHAR(50) | Operating status | e.g., 'OPERATIONAL' |
| price_level | INTEGER | Price level indicator | Range: 1-4 |
| wheelchair_accessible | BOOLEAN | Accessibility flag | Default: false |
| url | TEXT | Google Maps URL | |
| editorial_summary | TEXT | Place description | |
| latitude | DECIMAL(10,8) | Latitude coordinate | |
| longitude | DECIMAL(11,8) | Longitude coordinate | |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation time | Default: now() |
| updated_at | TIMESTAMP WITH TIME ZONE | Last update time | Default: now() |
| types | TEXT[] | Array of place types | |
| assistant_id | TEXT | Assistant identifier | |
| search_query | TEXT | Search query used | |
| featured_position | INTEGER | Position in featured list | Default: 0 |

### 2. place_services
Tracks available services for each place.

| Column | Type | Description | Notes |
|--------|------|-------------|--------|
| id | BIGSERIAL | Primary key | Auto-incrementing |
| place_id | TEXT | Foreign key to places | |
| delivery | BOOLEAN | Delivery available | Default: false |
| dine_in | BOOLEAN | Dine-in available | Default: false |
| takeout | BOOLEAN | Takeout available | Default: false |
| serves_breakfast | BOOLEAN | Serves breakfast | Default: false |
| serves_lunch | BOOLEAN | Serves lunch | Default: false |
| serves_dinner | BOOLEAN | Serves dinner | Default: false |
| serves_vegetarian | BOOLEAN | Vegetarian options available | Default: false |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation time | Default: now() |

### 3. place_opening_hours
Stores operating hours information.

| Column | Type | Description | Notes |
|--------|------|-------------|--------|
| id | BIGSERIAL | Primary key | Auto-incrementing |
| place_id | TEXT | Foreign key to places | |
| weekday_text | TEXT | Full day and hours text | e.g., "Monday: 9:00 AM - 5:00 PM" |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation time | Default: now() |

### 4. place_reviews
Stores user reviews.

| Column | Type | Description | Notes |
|--------|------|-------------|--------|
| id | BIGSERIAL | Primary key | Auto-incrementing |
| place_id | TEXT | Foreign key to places | |
| author_name | VARCHAR(255) | Reviewer name | |
| rating | INTEGER | Review rating | Range: 1-5 |
| text | TEXT | Review content | |
| time | BIGINT | Review timestamp | Unix timestamp |
| relative_time_description | VARCHAR(100) | Human-readable time | e.g., "a month ago" |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation time | Default: now() |

### 5. place_photos
Stores photo references and metadata.

| Column | Type | Description | Notes |
|--------|------|-------------|--------|
| id | BIGSERIAL | Primary key | Auto-incrementing |
| place_id | TEXT | Foreign key to places | |
| photo_reference | TEXT | Google Photo Reference | |
| height | INTEGER | Photo height | |
| width | INTEGER | Photo width | |
| html_attributions | TEXT[] | Required attributions | Array of attribution strings |
| storage_url | TEXT | Supabase Storage URL | URL to stored image |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation time | Default: now() |

## Indexes
The following indexes are created for query optimization:

- `idx_places_place_id`: On places(place_id)
- `idx_places_types`: On places(types)
- `idx_places_rating`: On places(rating)
- `idx_place_reviews_place_id`: On place_reviews(place_id)
- `idx_place_services_place_id`: On place_services(place_id)
- `idx_place_opening_hours_place_id`: On place_opening_hours(place_id)
- `idx_place_photos_place_id`: On place_photos(place_id)

## Relationships
- All subsidiary tables (place_services, place_opening_hours, place_reviews, place_photos) reference the places table through the place_id foreign key.
- Foreign key constraints ensure referential integrity.
- Cascade delete is not implemented by default to prevent accidental data loss.

## Usage Examples

### Basic Queries

1. Get all information about a specific place: