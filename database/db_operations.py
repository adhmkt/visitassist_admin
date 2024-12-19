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
            # Prepare the data according to the table schema
            assistant_data = {
                'assistant_id': agent_data.get('assistant_id'),
                'assistant_name': agent_data.get('name'),  # Map name to assistant_name
                'assistant_desc': agent_data.get('description'),  # Map description to assistant_desc
                'assistant_instructions': agent_data.get('prompt'),  # Map prompt to assistant_instructions
                'assistant_type': agent_data.get('type', 'classic'),  # Default to 'classic'
                'assistant_img': agent_data.get('image'),
                'sponsor_id': agent_data.get('sponsor_id'),
                'assistant_questions': agent_data.get('questions', {}),  # Default to empty JSON
                'assistant_json': agent_data.get('config', {}),  # Default to empty JSONB
                'assistant_functions': agent_data.get('functions', 'not_defined'),
                'assistant_languages': agent_data.get('languages', {
                    "languages": [
                        {
                            "language_code": "en",
                            "language_name": "English",
                            "version": "1.0"
                        }
                    ]
                }),
                'subtype': agent_data.get('subtype', 'subtype'),
                'sponsor_logo': agent_data.get('sponsor_logo', 'sponsor_default.png'),
                'sponsor_url': agent_data.get('sponsor_url', 'https://apis-ia.com')
            }
            
            result = self.supabase.table('assistants').insert(assistant_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating assistant: {e}")
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
            result = self.supabase.table('assistants').select("*").eq('assistant_id', agent_id).execute()
            if result.data:
                # Map the data back to the format expected by the frontend
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
            return None
        except Exception as e:
            print(f"Error getting assistant: {e}")
            raise

    def get_all_agents(self) -> List[Dict]:
        """
        Get all assistants
        
        Returns:
            list: List of all assistants
        """
        try:
            result = self.supabase.table('assistants').select("*").execute()
            # Map each assistant to the format expected by the frontend
            return [{
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
            } for assistant in (result.data or [])]
        except Exception as e:
            print(f"Error getting assistants: {e}")
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
            
            # Remove None values to avoid overwriting with nulls
            update_data = {k: v for k, v in agent_data.items() if v is not None}
            
            # Convert empty strings to None to avoid database errors
            update_data = {k: (None if v == '' else v) for k, v in update_data.items()}
            
            print(f"Cleaned update data: {update_data}")  # Debug log
            
            # Verify the assistant exists before updating
            check_result = self.supabase.table('assistants').select("*").eq('assistant_id', agent_id).execute()
            if not check_result.data:
                print(f"No assistant found with ID: {agent_id}")  # Debug log
                return None
                
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