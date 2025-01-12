import json
from supabase import create_client
import os
import logging
import openai  

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to read JSON data from database based on assistant_id
def read_json_from_database(assistant_id):
    try:
        # Connect to Supabase
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        supabase = create_client(supabase_url, supabase_key)

        response = supabase.table("assistants").select("assistant_json").eq("assistant_id", assistant_id).execute()
            
        if hasattr(response, 'data') and isinstance(response.data, list) and len(response.data) > 0:
    
                functionality_blob = response.data[0]['assistant_json']
                
                return functionality_blob
                
        else:
                
        
                return "Ooops... "

        # Query the assistants table for assistant_json where assistant_id matches
        result = supabase.table('assistants').select('assistant_json').eq('assistant_id', assistant_id).limit(1).execute()

        # Extract JSON data from the result
        json_data = result.get['data'][0]

        # Parse the JSON string into Python dictionary
        return json.loads(json_data)

    except Exception as e:
        logger.error(f"Error fetching JSON from database: {e}")
        return None

# Function to save data to Supabase
def save_to_supabase(data, assistant_id, destination):
    try:
        # Connect to Supabase
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        supabase = create_client(supabase_url, supabase_key)

        # Iterate over languages and insert each functionality
        for lang_code, lang_data in data['languages'].items():
            for functionality in lang_data['functionalities']:
                functionality_value = functionality.get('functionality_value')

                # Call LLM function to get functionality_blob (placeholder for now)
                functionality_blob = get_data_from_LLM(functionality_value, destination)
                # functionality_blob = translate_data_from_LLM(functionality_value, destination, lang_code)

                # Insert into Supabase table 'assistants_func_text'
                supabase.table('assistants_func_text').insert({
                    'functionality_id': functionality['functionality_id'],
                    'functionality_text': functionality['functionality_text'],
                    'functionality_value': functionality_value,
                    'language': lang_code,
                    'assistant_id': assistant_id,
                    'functionality_blob': functionality_blob  # Store LLM response here
                }).execute()

                logger.info(f"Inserted functionality for {lang_code}: {functionality['functionality_text']}")

    except Exception as e:
        logger.error(f"Error saving data to Supabase: {e}")

# Function to retrieve data from LLM (Placeholder for now)
my_api_key = os.getenv('OPENAI_API_KEY')
# Initialize OpenAI API client (make sure to set your API key)
openai.api_key = my_api_key

def translate_data_from_LLM(functionality_value, destination, language):
    # Construct messages for OpenAI API call
    instructions = f"""
    Destination: {destination}
    
    Core Objectives:
    
    Translate this to {language}.

    Don't modified markup of html tags. 

    Only translate the text.
    
    """

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": functionality_value},
    ]

    try:
        # Call OpenAI's API for chat completion
        completion = openai.chat.completions.create(
            model="gpt-4o",  # Replace with your preferred model
            messages=messages,
            temperature=0.3,
        )

        # Get the response from the API
        llm_response = completion.choices[0].message.content
        
        return llm_response

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


def get_data_from_LLM(functionality_value, destination):
    # Construct messages for OpenAI API call
    instructions = f"""
    Destination: {destination}


Core Objectives:

Personalized Assistance: Provide detailed and enriched recommendations, incorporating brief, informative descriptions of attractions and experiences to enhance the user's visit to the destination.
Local Expertise: Share comprehensive insights into the destination's hidden gems, culture, and history, with contextually relevant information added where necessary.
Travel Assistance: Act as a knowledgeable concierge, assisting users with all their travel needs while in the destination.
Guidelines:

Ensure responses are detailed, accurate, and enriched with context-specific information. Maintain a friendly and conversational tone to make the user feel welcomed and supported throughout their experience.
Responses should be precise, complete, and respectful. There is no token limit for the responses, so provide as much depth and richness as needed to fully address the user’s queries.
Apply makrdown to present content in a structured and readable way.
Alway offer to answer followup questions the user may have.
Use markdown to enrich the presentation of the content.



    """

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": functionality_value},
    ]

    try:
        # Call OpenAI's API for chat completion
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your preferred model
            messages=messages,
            temperature=0.2,
        )

        # Get the response from the API
        llm_response = completion.choices[0].message.content
        
        return llm_response

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

if __name__ == '__main__':
    try:
        # Get user input for assistant_id and destination
        assistant_id = input("Enter assistant_id: ").strip()
        destination = input("Enter destination: ").strip()

        # Confirmation before proceeding
        confirmation = input(f"Proceed with saving data for assistant_id '{assistant_id}' and destination '{destination}'? (y/n): ").strip().lower()

        if confirmation == 'y':
            # Read JSON data from database based on assistant_id
            json_data = read_json_from_database(assistant_id)

            if json_data:
                # Save data to Supabase
                print(f"Data trying to save: {json_data}")
                save_to_supabase(json_data, assistant_id, destination)
            else:
                print(f"No JSON data found for assistant_id '{assistant_id}'. Operation canceled.")
        else:
            print("Operation canceled.")
    
    except Exception as e:
        print(f"Error: {e}")
