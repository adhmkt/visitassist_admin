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
        response = supabase.table(table_name).select("id, functionality_blob, functionality_text, functionality_value").eq("assistant_id", assistant_id).eq("language", language).execute()
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
            model="gpt-4o-mini",
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
            "language": target_language  # assuming you have a language column in your table
        }).execute()

        if response.status_code == 201:
            logger.info("Successfully inserted translated functionality_blob.")
        else:
            logger.error(f"Failed to insert translated functionality_blob. Status code: {response.status_code}.")
            logger.debug(f"Response content: {response.data}")  # Log response data for debugging
    except Exception as e:
        logger.error(f"Error inserting functionality_blob into database: {e}")

def main():
    try:
        # Get user input for assistant_id and the target language
        assistant_id = input("Enter assistant_id: ").strip()
        source_language = input("Enter the source language (e.g., 'en' for English): ").strip()
        target_language = input("Enter the target language for translation (e.g., 'es' for Spanish): ").strip()

        # Retrieve functionality_blob data from the database based on assistant_id and source language
        rows = get_functionality_blobs(assistant_id, source_language)

        # Insert translated data into the database
        for row in rows:
            row_id = row['id']
            blob = row['functionality_blob']
            functionality_text= row['functionality_text']
            functionality_value= row['functionality_value']
            blob = row['functionality_blob']
            logger.debug(f"Processing row id: {row_id}.")
            logger.debug(f"Original blob length: {len(blob)} characters.")

            translated_blob = translate_functionality_blob(blob, target_language)
            if translated_blob:
                logger.debug(f"Translated blob length: {len(translated_blob)} characters.")
                insert_functionality_blob(assistant_id, translated_blob, target_language, functionality_text,functionality_value )
            else:
                logger.error(f"Translation failed for row id: {row_id}.")

    except Exception as e:
        logger.error(f"Error in the main function: {e}")

if __name__ == '__main__':
    main()
