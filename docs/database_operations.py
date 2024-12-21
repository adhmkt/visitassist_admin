import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

class DatabaseOperations:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )

    # Events
    def get_all_events(self):
        """Get all events with their venue and organizer information."""
        try:
            response = self.supabase.table('events') \
                .select('*, venues(name), organizers(name), event_tags(tag_id)') \
                .execute()
            events = response.data
            
            # Format the response
            for event in events:
                event['venue_name'] = event['venues']['name']
                event['organizer_name'] = event['organizers']['name']
                event['tags'] = [tag['tag_id'] for tag in event['event_tags']]
                del event['venues']
                del event['organizers']
                del event['event_tags']
            
            return events
        except Exception as e:
            print(f"Error getting events: {str(e)}")
            return []

    def search_events(self, search_term='', start_date=None, end_date=None, venue_id=None, organizer_id=None):
        """Search events based on various criteria."""
        try:
            query = self.supabase.table('events') \
                .select('*, venues(name), organizers(name), event_tags(tag_id)')
            
            if search_term:
                query = query.ilike('title', f'%{search_term}%')
            
            if start_date:
                query = query.gte('start_date', start_date)
            
            if end_date:
                query = query.lte('end_date', end_date)
            
            if venue_id:
                query = query.eq('venue_id', venue_id)
            
            if organizer_id:
                query = query.eq('organizer_id', organizer_id)
            
            response = query.execute()
            events = response.data
            
            # Format the response
            for event in events:
                event['venue_name'] = event['venues']['name']
                event['organizer_name'] = event['organizers']['name']
                event['tags'] = [tag['tag_id'] for tag in event['event_tags']]
                del event['venues']
                del event['organizers']
                del event['event_tags']
            
            return events
        except Exception as e:
            print(f"Error searching events: {str(e)}")
            return []

    def get_event_by_id(self, event_id):
        """Get a single event by its ID."""
        try:
            response = self.supabase.table('events') \
                .select('*, venues(name), organizers(name), event_tags(tag_id)') \
                .eq('event_id', event_id) \
                .single() \
                .execute()
            
            event = response.data
            if event:
                event['venue_name'] = event['venues']['name']
                event['organizer_name'] = event['organizers']['name']
                event['tags'] = [tag['tag_id'] for tag in event['event_tags']]
                del event['venues']
                del event['organizers']
                del event['event_tags']
            
            return event
        except Exception as e:
            print(f"Error getting event {event_id}: {str(e)}")
            return None

    def create_event(self, event_data):
        """Create a new event."""
        try:
            # Extract tags before creating event
            tags = event_data.pop('tags', [])
            
            # Create event
            response = self.supabase.table('events') \
                .insert(event_data) \
                .execute()
            
            event = response.data[0]
            event_id = event['event_id']
            
            # Add tags
            if tags:
                tag_data = [{'event_id': event_id, 'tag_id': tag_id} for tag_id in tags]
                self.supabase.table('event_tags').insert(tag_data).execute()
            
            return event_id
        except Exception as e:
            print(f"Error creating event: {str(e)}")
            raise

    def update_event(self, event_id, event_data):
        """Update an existing event."""
        try:
            # Extract tags before updating event
            tags = event_data.pop('tags', [])
            
            # Update event
            response = self.supabase.table('events') \
                .update(event_data) \
                .eq('event_id', event_id) \
                .execute()
            
            # Update tags
            if tags is not None:
                # Delete existing tags
                self.supabase.table('event_tags') \
                    .delete() \
                    .eq('event_id', event_id) \
                    .execute()
                
                # Add new tags
                if tags:
                    tag_data = [{'event_id': event_id, 'tag_id': tag_id} for tag_id in tags]
                    self.supabase.table('event_tags').insert(tag_data).execute()
            
            return True
        except Exception as e:
            print(f"Error updating event {event_id}: {str(e)}")
            raise

    def delete_event(self, event_id):
        """Delete an event and its associated tags."""
        try:
            # Delete associated tags first
            self.supabase.table('event_tags') \
                .delete() \
                .eq('event_id', event_id) \
                .execute()
            
            # Delete the event
            self.supabase.table('events') \
                .delete() \
                .eq('event_id', event_id) \
                .execute()
            
            return True
        except Exception as e:
            print(f"Error deleting event {event_id}: {str(e)}")
            raise

    # Venues
    def get_all_venues(self):
        """Get all venues."""
        try:
            response = self.supabase.table('venues') \
                .select('*') \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting venues: {str(e)}")
            return []

    # Organizers
    def get_all_organizers(self):
        """Get all organizers."""
        try:
            response = self.supabase.table('organizers') \
                .select('*') \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting organizers: {str(e)}")
            return []

    # Tags
    def get_all_tags(self):
        """Get all tags."""
        try:
            response = self.supabase.table('ev_tags') \
                .select('*') \
                .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting tags: {str(e)}")
            return []