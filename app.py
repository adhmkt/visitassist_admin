from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from database.db_operations import DatabaseOperations
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure secret key in production

# Initialize database operations
db = DatabaseOperations()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        print(f"Login attempt for email: {email}")  # Debug log
        
        try:
            # Query the tour_user table
            result = db.supabase.table('tour_user')\
                .select('*')\
                .eq('email', email)\
                .execute()
            
            print(f"Query result: {result.data}")  # Debug log
            
            # First find user by email
            user = result.data[0] if result.data else None
            
            if user and user['password'] == password and user['status'] == 'active':
                # Store user info in session
                session['user'] = {
                    'id': user['id'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role']
                }
                print(f"Login successful for user: {user['email']}")  # Debug log
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            
            print("Login failed: Invalid credentials")  # Debug log
            return jsonify({'success': False, 'message': 'Invalid credentials'})
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug log
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
        
    try:
        # Get user info from session
        user = session['user']
        
        return render_template('dashboard.html',
                             user=user,
                             active_agents=0,  # Placeholder until agents table is created
                             active_users=1)   # Placeholder until we implement user counting
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return redirect(url_for('login'))

@app.route('/edit-agent', methods=['GET', 'POST'])
def edit_agent():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json()
        agent_id = data.get('assistant_id')
        print(f"Received update request for assistant_id: {agent_id}")  # Debug log
        
        agent_data = {
            'assistant_name': data.get('name'),
            'assistant_desc': data.get('description'),
            'assistant_instructions': data.get('prompt'),
            'assistant_type': data.get('type', 'classic'),
            'assistant_img': data.get('image'),
            'sponsor_id': data.get('sponsor_id'),
            'assistant_questions': data.get('questions', {}),
            'assistant_json': data.get('config', {}),
            'assistant_functions': data.get('functions', 'not_defined'),
            'assistant_languages': data.get('languages', {
                "languages": [
                    {
                        "language_code": "en",
                        "language_name": "English",
                        "version": "1.0"
                    }
                ]
            }),
            'subtype': data.get('subtype', 'subtype'),
            'sponsor_logo': data.get('sponsor_logo', 'sponsor_default.png'),
            'sponsor_url': data.get('sponsor_url', 'https://apis-ia.com')
        }
        
        print(f"Prepared update data: {agent_data}")  # Debug log
        
        try:
            if agent_id:
                print(f"Attempting to update assistant with ID: {agent_id}")  # Debug log
                # Update existing agent
                updated_agent = db.update_agent(agent_id, agent_data)
                if updated_agent:
                    print(f"Successfully updated assistant: {updated_agent}")  # Debug log
                    return jsonify({'success': True, 'agent': updated_agent})
                print("Update operation returned None")  # Debug log
                return jsonify({'success': False, 'message': 'Failed to update assistant'})
            else:
                print("Creating new assistant")  # Debug log
                # Create new agent
                new_agent = db.create_agent(agent_data)
                if new_agent:
                    print(f"Successfully created assistant: {new_agent}")  # Debug log
                    return jsonify({'success': True, 'agent': new_agent})
                print("Create operation returned None")  # Debug log
                return jsonify({'success': False, 'message': 'Failed to create assistant'})
        except Exception as e:
            print(f"Error saving assistant: {str(e)}")  # Debug log
            return jsonify({'success': False, 'message': str(e)})
    
    try:
        # Get all agents for the dropdown
        agents = db.get_all_agents()
    except Exception as e:
        print(f"Warning: Could not fetch assistants: {e}")
        agents = []  # Use empty list if no agents exist yet
    
    # Always render the template, even if there are no agents
    return render_template('edit_agent.html', 
                         agents=agents,
                         user=session['user'])

@app.route('/agent/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    try:
        agent = db.get_agent(agent_id)
        if agent:
            return jsonify({'success': True, 'agent': agent})
        return jsonify({'success': False, 'message': 'Agent not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/agent/<agent_id>/delete', methods=['POST'])
def delete_agent(agent_id):
    try:
        success = db.delete_agent(agent_id)
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Failed to delete agent'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/agent/<agent_id>/chat-history')
def chat_history(agent_id):
    try:
        history = db.get_agent_chat_history(agent_id)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/chat/<agent_id>', methods=['POST'])
def chat(agent_id):
    data = request.get_json()
    chat_data = {
        'agent_id': agent_id,
        'user_input': data.get('user_input'),
        'agent_response': data.get('agent_response')
    }
    
    try:
        saved_chat = db.save_chat_history(chat_data)
        return jsonify({'success': True, 'chat': saved_chat})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/agents')
def get_agents():
    """Get all agents for search functionality"""
    # Only require authentication if not accessed from assistant directory
    is_directory_request = request.headers.get('Referer', '').endswith('/assistant-directory')
    if not is_directory_request and 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    try:
        agents = db.get_all_agents()
        return jsonify({
            'success': True,
            'agents': agents
        })
    except Exception as e:
        print(f"Error getting agents: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/assistant-directory')
def assistant_directory():
    return render_template('assistant_cards.html')

@app.route('/api/assistants')
def get_assistants():
    try:
        db = DatabaseOperations()
        assistants = db.get_all_assistants()
        return jsonify({
            'success': True,
            'assistants': assistants
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/assistant-functionalities/<assistant_id>/<functionality_id>/<language>', methods=['GET'])
def get_assistant_functionalities(assistant_id, functionality_id, language):
    try:
        print(f"Fetching functionality for assistant: {assistant_id}, id: {functionality_id}, language: {language}")
        
        # Query assistants_func_text table using Supabase client (note the plural form)
        result = db.supabase.table('assistants_func_text')\
            .select('*')\
            .eq('assistant_id', assistant_id)\
            .eq('functionality_id', functionality_id)\
            .eq('language', language)\
            .execute()
            
        # Get the first result if exists
        functionality = result.data[0] if result.data else None
        
        print("Found functionality:", functionality if functionality else "No result")
        
        return jsonify({
            'success': True,
            'functionality': functionality
        })
    except Exception as e:
        print(f"Error fetching functionality: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update-functionalities', methods=['POST'])
def update_functionalities():
    try:
        data = request.json
        assistant_id = data['assistantId']
        config_updates = data['configUpdates']
        db_updates = data['dbUpdates']

        print(f"Received update request for assistant {assistant_id}")
        print(f"Config updates: {json.dumps(config_updates, indent=2)}")
        print(f"DB updates count: {len(db_updates)}")

        # 1. Get current assistant data
        try:
            current_assistant = db.supabase.table('assistants')\
                .select('assistant_json')\
                .eq('assistant_id', assistant_id)\
                .execute()
            
            if not current_assistant.data:
                raise Exception(f'Assistant {assistant_id} not found')

            # Get current configuration
            current_config = current_assistant.data[0].get('assistant_json', {})
            
            # Merge the new configuration with existing one
            merged_config = current_config.copy()
            if 'languages' in config_updates:
                if 'languages' not in merged_config:
                    merged_config['languages'] = {}
                merged_config['languages'].update(config_updates['languages'])

            # Update assistant configuration
            result = db.supabase.table('assistants')\
                .update({'assistant_json': merged_config})\
                .eq('assistant_id', assistant_id)\
                .execute()
            
            if not result.data:
                raise Exception('Failed to update assistant configuration')
            
            print("Successfully updated assistant configuration")

        except Exception as e:
            print(f"Error updating assistant configuration: {str(e)}")
            raise

        # 2. Update or Insert functionality texts
        for update in db_updates:
            try:
                print(f"Processing update for functionality {update['functionality_id']} in language {update['language']}")
                
                # Check if record exists
                existing = db.supabase.table('assistants_func_text')\
                    .select('*')\
                    .eq('assistant_id', update['assistant_id'])\
                    .eq('language', update['language'])\
                    .eq('functionality_id', update['functionality_id'])\
                    .execute()

                if existing.data:
                    print(f"Updating existing record for functionality {update['functionality_id']}")
                    # Update existing record
                    result = db.supabase.table('assistants_func_text')\
                        .update({
                            'functionality_text': update['functionality_text'],
                            'functionality_value': update['functionality_value'],
                            'functionality_type': update['functionality_type']
                        })\
                        .eq('assistant_id', update['assistant_id'])\
                        .eq('language', update['language'])\
                        .eq('functionality_id', update['functionality_id'])\
                        .execute()
                else:
                    print(f"Inserting new record for functionality {update['functionality_id']}")
                    # Insert new record
                    result = db.supabase.table('assistants_func_text')\
                        .insert({
                            'assistant_id': update['assistant_id'],
                            'language': update['language'],
                            'functionality_id': update['functionality_id'],
                            'functionality_text': update['functionality_text'],
                            'functionality_value': update['functionality_value'],
                            'functionality_type': update['functionality_type']
                        })\
                        .execute()

                if not result.data:
                    raise Exception(f'Failed to update/insert functionality {update["functionality_id"]}')
                
                print(f"Successfully processed functionality {update['functionality_id']}")

            except Exception as e:
                print(f"Error updating functionality {update.get('functionality_id')}: {str(e)}")
                raise

        return jsonify({'success': True})
    except Exception as e:
        error_msg = str(e)
        print(f"Error in update_functionalities: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)