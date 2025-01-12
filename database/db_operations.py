import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, List, Optional
import traceback

# Load environment variables
load_dotenv()

class DatabaseOperations:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )

    # Assistant Operations
    def create_agent(self, agent_data: Dict) -> Dict:
        """
        Create a new assistant
        
        Args:
            agent_data (dict): Assistant data containing required fields
        
        Returns:
            dict: Created assistant data
        """
        try:
            print(f"Attempting to create assistant with data: {agent_data}")  # Debug log
            
            # Insert the data directly
            result = self.supabase.table('assistants').insert(agent_data).execute()
            
            if not result.data:
                print("No data returned from insert operation")
                return None
                
            print(f"Successfully created assistant: {result.data[0]}")
            return result.data[0]
            
        except Exception as e:
            print(f"Error creating assistant: {str(e)}")  # Debug log
            raise

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """
        Get assistant by ID
        
        Args:
            agent_id (str): Assistant ID
            
        Returns:
            dict: Assistant data if found, None otherwise
        """
        try:
            print(f"Fetching assistant with ID: {agent_id}")  # Debug log
            result = self.supabase.table('assistants').select("*").eq('assistant_id', agent_id).execute()
            print(f"Query result: {result.data}")  # Debug log
            
            if result.data:
                # Map the data directly using the database column names
                assistant = result.data[0]
                return {
                    'assistant_id': assistant.get('assistant_id'),
                    'assistant_name': assistant.get('assistant_name'),
                    'assistant_desc': assistant.get('assistant_desc'),
                    'assistant_instructions': assistant.get('assistant_instructions'),
                    'assistant_type': assistant.get('assistant_type'),
                    'assistant_img': assistant.get('assistant_img'),
                    'sponsor_id': assistant.get('sponsor_id'),
                    'assistant_questions': assistant.get('assistant_questions'),
                    'assistant_json': assistant.get('assistant_json'),
                    'assistant_functions': assistant.get('assistant_functions'),
                    'assistant_languages': assistant.get('assistant_languages'),
                    'subtype': assistant.get('subtype'),
                    'sponsor_logo': assistant.get('sponsor_logo'),
                    'sponsor_url': assistant.get('sponsor_url')
                }
            print(f"No assistant found with ID: {agent_id}")  # Debug log
            return None
        except Exception as e:
            print(f"Error getting assistant: {e}")
            print(f"Traceback: {traceback.format_exc()}")  # Debug log
            raise

    def get_all_agents(self) -> List[Dict]:
        """
        Get all assistants
        
        Returns:
            list: List of all assistants
        """
        try:
            print("Executing get_all_agents query...")  # Debug log
            result = self.supabase.table('assistants').select("*").order('assistant_name').execute()
            print(f"Query returned {len(result.data) if result.data else 0} rows")  # Debug log
            
            if not result.data:
                print("No data returned from query")
                return []
            
            agents = []
            for assistant in result.data:
                try:
                    agent = {
                        'assistant_id': assistant.get('assistant_id'),
                        'assistant_name': assistant.get('assistant_name'),
                        'assistant_desc': assistant.get('assistant_desc'),
                        'assistant_instructions': assistant.get('assistant_instructions'),
                        'assistant_type': assistant.get('assistant_type'),
                        'assistant_img': assistant.get('assistant_img'),
                        'sponsor_id': assistant.get('sponsor_id'),
                        'assistant_questions': assistant.get('assistant_questions'),
                        'assistant_functions': assistant.get('assistant_functions'),
                        'assistant_languages': assistant.get('assistant_languages'),
                        'subtype': assistant.get('subtype'),
                        'sponsor_logo': assistant.get('sponsor_logo'),
                        'sponsor_url': assistant.get('sponsor_url')
                    }
                    agents.append(agent)
                    print(f"Processed agent: {agent['assistant_id']} - {agent['assistant_name']}")  # Debug log
                except Exception as e:
                    print(f"Error processing agent: {e}")  # Debug log
                    continue
            
            print(f"Successfully mapped {len(agents)} agents")  # Debug log
            return agents
            
        except Exception as e:
            print(f"Database error in get_all_agents: {str(e)}")  # Debug log
            print(f"Traceback: {traceback.format_exc()}")  # Debug log
            raise

    def update_agent(self, agent_id: str, agent_data: Dict) -> Optional[Dict]:
        """
        Update assistant data
        
        Args:
            agent_id (str): Assistant ID
            agent_data (dict): Updated assistant data
            
        Returns:
            dict: Updated assistant data
        """
        try:
            print(f"Updating assistant {agent_id} with data: {agent_data}")  # Debug log
            
            # First, get the existing assistant data
            existing_assistant = self.supabase.table('assistants').select("*").eq('assistant_id', agent_id).execute()
            if not existing_assistant.data:
                print(f"No assistant found with ID: {agent_id}")  # Debug log
                return None
            
            existing_data = existing_assistant.data[0]
            
            # Handle assistant_json separately to preserve schema
            if 'assistant_json' in agent_data:
                new_config = agent_data['assistant_json']
                existing_config = existing_data.get('assistant_json', {})
                
                # Merge configurations
                if 'languages' in new_config:
                    if 'languages' not in existing_config:
                        existing_config['languages'] = {}
                    
                    # Update language-specific data while preserving other fields
                    for lang_code, lang_data in new_config['languages'].items():
                        if lang_code not in existing_config['languages']:
                            existing_config['languages'][lang_code] = {}
                        
                        # Update language data while preserving functionalities
                        existing_lang_data = existing_config['languages'][lang_code]
                        functionalities = existing_lang_data.get('functionalities', [])
                        existing_config['languages'][lang_code].update(lang_data)
                        
                        # Restore functionalities if they weren't in the update
                        if 'functionalities' not in lang_data:
                            existing_config['languages'][lang_code]['functionalities'] = functionalities
                
                # Update the merged configuration
                agent_data['assistant_json'] = existing_config
            
            # Remove None values to avoid overwriting with nulls
            update_data = {k: v for k, v in agent_data.items() if v is not None}
            
            # Convert empty strings to None to avoid database errors
            update_data = {k: (None if v == '' else v) for k, v in update_data.items()}
            
            print(f"Cleaned update data: {update_data}")  # Debug log
            
            result = self.supabase.table('assistants').update(update_data).eq('assistant_id', agent_id).execute()
            print(f"Update result: {result.data}")  # Debug log
            
            if result.data:
                # Map the response back to the format expected by the frontend
                assistant = result.data[0]
                return {
                    'id': assistant.get('assistant_id'),
                    'name': assistant.get('assistant_name'),
                    'description': assistant.get('assistant_desc'),
                    'prompt': assistant.get('assistant_instructions'),
                    'type': assistant.get('assistant_type'),
                    'image': assistant.get('assistant_img'),
                    'sponsor_id': assistant.get('sponsor_id'),
                    'questions': assistant.get('assistant_questions'),
                    'config': assistant.get('assistant_json'),
                    'functions': assistant.get('assistant_functions'),
                    'languages': assistant.get('assistant_languages'),
                    'subtype': assistant.get('subtype'),
                    'sponsor_logo': assistant.get('sponsor_logo'),
                    'sponsor_url': assistant.get('sponsor_url')
                }
            print("Update operation returned no data")  # Debug log
            return None
        except Exception as e:
            print(f"Error updating assistant: {str(e)}")  # Debug log
            raise

    def delete_agent(self, agent_id: str) -> bool:
        """
        Delete assistant by ID
        
        Args:
            agent_id (str): Assistant ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            result = self.supabase.table('assistants').delete().eq('assistant_id', agent_id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error deleting assistant: {e}")
            raise

    # Chat History Operations
    def save_chat_history(self, chat_data: Dict) -> Dict:
        """
        Save chat history
        
        Args:
            chat_data (dict): Chat data containing agent_id, user_input, agent_response
            
        Returns:
            dict: Saved chat data
        """
        try:
            result = self.supabase.table('chat_history').insert(chat_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error saving chat history: {e}")
            raise

    def get_agent_chat_history(self, agent_id: str) -> List[Dict]:
        """
        Get chat history for specific assistant
        
        Args:
            agent_id (str): Assistant ID
            
        Returns:
            list: List of chat history entries
        """
        try:
            result = self.supabase.table('chat_history')\
                .select("*")\
                .eq('agent_id', agent_id)\
                .order('created_at', desc=True)\
                .execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting chat history: {e}")
            raise

    # User Operations
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Get user by email
        
        Args:
            email (str): User email
            
        Returns:
            dict: User data if found, None otherwise
        """
        try:
            result = self.supabase.table('users').select("*").eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            raise

    def create_user(self, user_data: Dict) -> Dict:
        """
        Create a new user
        
        Args:
            user_data (dict): User data containing email, name, role
            
        Returns:
            dict: Created user data
        """
        try:
            result = self.supabase.table('users').insert(user_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            raise

    # Event Operations
    def create_event(self, event_data: Dict) -> Dict:
        """
        Create a new event
        
        Args:
            event_data (dict): Event data containing required fields
            
        Returns:
            dict: Created event data
        """
        try:
            result = self.supabase.table('ev_events').insert(event_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating event: {e}")
            raise

    def get_event(self, event_id: int) -> Optional[Dict]:
        """
        Get event by ID with venue and organizer details
        
        Args:
            event_id (int): Event ID
            
        Returns:
            dict: Event data if found, None otherwise
        """
        try:
            result = self.supabase.table('ev_events')\
                .select(
                    "*, ev_venues(*), ev_organizers(*), eventtags(tag_id)"
                )\
                .eq('event_id', event_id)\
                .execute()
            
            if result.data:
                event = result.data[0]
                # Get tags for the event
                tag_ids = [t['tag_id'] for t in event.get('eventtags', [])]
                if tag_ids:
                    tags = self.supabase.table('ev_tags')\
                        .select('*')\
                        .in_('tag_id', tag_ids)\
                        .execute()
                    event['tags'] = tags.data
                return event
            return None
        except Exception as e:
            print(f"Error getting event: {e}")
            raise

    def update_event(self, event_id: int, event_data: Dict) -> Optional[Dict]:
        """
        Update event data
        
        Args:
            event_id (int): Event ID
            event_data (dict): Updated event data
            
        Returns:
            dict: Updated event data
        """
        try:
            result = self.supabase.table('ev_events')\
                .update(event_data)\
                .eq('event_id', event_id)\
                .execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating event: {e}")
            raise

    def delete_event(self, event_id: int) -> bool:
        """
        Delete event by ID
        
        Args:
            event_id (int): Event ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            result = self.supabase.table('ev_events')\
                .delete()\
                .eq('event_id', event_id)\
                .execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error deleting event: {e}")
            raise

    def get_events(self, filters: Dict = None) -> List[Dict]:
        """
        Get events with optional filters
        
        Args:
            filters (dict): Optional filters for events
            
        Returns:
            list: List of events
        """
        try:
            query = self.supabase.table('ev_events')\
                .select("*, ev_venues(name), ev_organizers(name)")
            
            if filters:
                if filters.get('search'):
                    query = query.ilike('title', f"%{filters['search']}%")
                if filters.get('start_date'):
                    query = query.gte('start_date', filters['start_date'])
                if filters.get('end_date'):
                    query = query.lte('end_date', filters['end_date'])
                if filters.get('venue_id'):
                    query = query.eq('venue_id', filters['venue_id'])
                if filters.get('organizer_id'):
                    query = query.eq('organizer_id', filters['organizer_id'])
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting events: {e}")
            raise

    # Venue Operations
    def create_venue(self, venue_data: Dict) -> Dict:
        """Create a new venue"""
        try:
            result = self.supabase.table('ev_venues').insert(venue_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating venue: {e}")
            raise

    def get_venue(self, venue_id: int) -> Optional[Dict]:
        """Get venue by ID"""
        try:
            result = self.supabase.table('ev_venues')\
                .select("*")\
                .eq('venue_id', venue_id)\
                .execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting venue: {e}")
            raise

    def get_venues(self) -> List[Dict]:
        """Get all venues"""
        try:
            result = self.supabase.table('ev_venues').select("*").execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting venues: {e}")
            raise

    # Organizer Operations
    def create_organizer(self, organizer_data: Dict) -> Dict:
        """Create a new organizer"""
        try:
            result = self.supabase.table('ev_organizers').insert(organizer_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating organizer: {e}")
            raise

    def get_organizer(self, organizer_id: int) -> Optional[Dict]:
        """Get organizer by ID"""
        try:
            result = self.supabase.table('ev_organizers')\
                .select("*")\
                .eq('organizer_id', organizer_id)\
                .execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting organizer: {e}")
            raise

    def get_organizers(self) -> List[Dict]:
        """Get all organizers"""
        try:
            result = self.supabase.table('ev_organizers').select("*").execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting organizers: {e}")
            raise

    # Tag Operations
    def create_tag(self, tag_data: Dict) -> Dict:
        """Create a new tag"""
        try:
            result = self.supabase.table('ev_tags').insert(tag_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating tag: {e}")
            raise

    def get_tags(self) -> List[Dict]:
        """Get all tags"""
        try:
            result = self.supabase.table('ev_tags').select("*").execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting tags: {e}")
            raise

    def add_tags_to_event(self, event_id: int, tag_ids: List[int]) -> bool:
        """Add tags to an event"""
        try:
            tag_data = [{'event_id': event_id, 'tag_id': tag_id} for tag_id in tag_ids]
            result = self.supabase.table('eventtags').insert(tag_data).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error adding tags to event: {e}")
            raise

    def remove_tags_from_event(self, event_id: int, tag_ids: List[int]) -> bool:
        """Remove tags from an event"""
        try:
            result = self.supabase.table('eventtags')\
                .delete()\
                .eq('event_id', event_id)\
                .in_('tag_id', tag_ids)\
                .execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error removing tags from event: {e}")
            raise

    def get_event_tags(self, event_id: int) -> List[Dict]:
        """Get all tags for an event"""
        try:
            result = self.supabase.table('eventtags')\
                .select("ev_tags(*)")\
                .eq('event_id', event_id)\
                .execute()
            return [item['ev_tags'] for item in result.data] if result.data else []
        except Exception as e:
            print(f"Error getting event tags: {e}")
            raise

    # Venue Methods
    def get_all_venues(self):
        """Get all venues."""
        try:
            response = self.supabase.table('ev_venues') \
                .select('*') \
                .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting venues: {str(e)}")
            return []

    def get_venue(self, venue_id):
        """Get a specific venue by ID."""
        try:
            response = self.supabase.table('ev_venues') \
                .select('*') \
                .eq('venue_id', venue_id) \
                .single() \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting venue {venue_id}: {str(e)}")
            return None

    # Organizer Methods
    def get_all_organizers(self):
        """Get all organizers."""
        try:
            response = self.supabase.table('ev_organizers') \
                .select('*') \
                .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting organizers: {str(e)}")
            return []

    def get_organizer(self, organizer_id):
        """Get a specific organizer by ID."""
        try:
            response = self.supabase.table('ev_organizers') \
                .select('*') \
                .eq('organizer_id', organizer_id) \
                .single() \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting organizer {organizer_id}: {str(e)}")
            return None

    # Tag Methods
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

    def get_tag(self, tag_id):
        """Get a specific tag by ID."""
        try:
            response = self.supabase.table('tags') \
                .select('*') \
                .eq('tag_id', tag_id) \
                .single() \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting tag {tag_id}: {str(e)}")
            return None

    # Event Methods
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

# Example usage:
# db = DatabaseOperations()
# 
# # Create an assistant
# assistant_data = {
#     "name": "Support Assistant",
#     "description": "Customer support chatbot",
#     "prompt": "You are a helpful customer support assistant...",
#     "temperature": 0.7
# }
# new_assistant = db.create_agent(assistant_data)
#
# # Get all assistants
# assistants = db.get_all_agents()
#
# # Update an assistant
# updated_data = {"temperature": 0.8}
# updated_assistant = db.update_agent(assistant_id, updated_data)
#
# # Delete an assistant
# success = db.delete_agent(assistant_id) 