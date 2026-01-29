from dotenv import load_dotenv
load_dotenv()  # Add this at the start of the file

import os
import openai
import logging
from supabase import create_client

# Initialize logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

# Initialize OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_functionality_blobs(assistant_id, language):
    try:
        table_name = "assistants_func_text"
        response = supabase.table(table_name).select("id, functionality_id, functionality_blob, functionality_text, functionality_value").eq("assistant_id", assistant_id).eq("language", language).execute()
        logger.debug(f"Supabase response: {response}")
        if hasattr(response, 'data') and isinstance(response.data, list) and len(response.data) > 0:
            return response.data
        else:
            logger.warning("No functionality_blob found in the table for the specified assistant_id and language.")
            return []
    except Exception as e:
        logger.error(f"Error fetching functionality_blob from database: {e}")
        return []
    
def translate_functionality_blob(blob, target_language):
    try:
        prompt = f"""
        Translate this to {target_language}.

        Don't modify markup of HTML tags. Only translate the text.
        {blob}
        """
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": blob}
            ],
            temperature=0.2
        )

        
        translated_blob = response.choices[0].message.content
        logger.debug(f"Translation successful. Translated blob length: {len(translated_blob)} characters.")
        return translated_blob
    except Exception as e:
        logger.error(f"Error translating functionality_blob: {e}")
        return None

def insert_functionality_blob(assistant_id, translated_blob, target_language, functionality_id, functionality_text, functionality_value):
    table_name = "assistants_func_text"
    try:
        response = supabase.table(table_name).insert({
            "assistant_id": assistant_id,
            "functionality_id": functionality_id,
            "functionality_text": functionality_text,
            "functionality_value": functionality_value,
            "functionality_blob": translated_blob,
            "language": target_language
        }).execute()

        # Supabase client doesn't return status_code, just check if data exists
        if response and hasattr(response, 'data'):
            logger.info("Successfully inserted translated functionality_blob.")
        else:
            logger.error("Failed to insert translated functionality_blob.")
            logger.debug(f"Response: {response}")  # Log response for debugging
    except Exception as e:
        logger.error(f"Error inserting functionality_blob into database: {e}")

def main():
    try:
        # Get user input for assistant_id and the target language
        assistant_id = input("Enter assistant_id: ").strip()
        source_language = input("Enter the source language (e.g., 'en' for English): ").strip()
        target_language = input("Enter the target language for translation (e.g., 'es' for Spanish): ").strip()
        
        # Ask if user wants to translate a specific functionality_id
        translate_specific = input("Do you want to translate a specific functionality? (y/n): ").strip().lower()
        specific_functionality_id = None
        
        if translate_specific == 'y':
            specific_functionality_id = input("Enter the functionality_id to translate: ").strip()
            try:
                specific_functionality_id = int(specific_functionality_id)
            except ValueError:
                logger.warning("Invalid functionality_id format. Using as string.")

        # Retrieve functionality_blob data from the database based on assistant_id and source language
        rows = get_functionality_blobs(assistant_id, source_language)
        
        if not rows:
            logger.error(f"No functionality blobs found for assistant_id: {assistant_id} and language: {source_language}")
            return

        # Filter rows if specific functionality_id is provided
        if specific_functionality_id is not None:
            # Based on your database screenshot, we need to filter by functionality_id column
            rows = [row for row in rows if row.get('functionality_id') == specific_functionality_id]
            if not rows:
                logger.error(f"No functionality blob found with functionality_id: {specific_functionality_id}")
                return
            logger.info(f"Found {len(rows)} row(s) with functionality_id: {specific_functionality_id}")

        # Insert translated data into the database
        for row in rows:
            functionality_id = row['functionality_id']
            functionality_text = row['functionality_text']
            functionality_value = row['functionality_value']
            blob = row['functionality_blob']
            logger.debug(f"Processing functionality_id: {functionality_id}.")
            logger.debug(f"Original blob length: {len(blob)} characters.")

            translated_blob = translate_functionality_blob(blob, target_language)
            if translated_blob:
                logger.debug(f"Translated blob length: {len(translated_blob)} characters.")
                insert_functionality_blob(
                    assistant_id, 
                    translated_blob, 
                    target_language, 
                    functionality_id,
                    functionality_text, 
                    functionality_value
                )
            else:
                logger.error(f"Translation failed for functionality_id: {functionality_id}.")

    except Exception as e:
        logger.error(f"Error in the main function: {e}")
        # Add this line to see the full error traceback
        import traceback
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    main()
