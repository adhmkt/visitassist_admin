from flask import Flask, render_template, redirect, url_for, session, request, jsonify, Response
import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
from math import cos, pi, radians
import base64

# Load environment variables
load_dotenv()

# Configuration - with debug logging and fallback values
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
print("\n=== API Configuration Debug ===")
print(f"GOOGLE_MAPS_API_KEY present: {'Yes' if GOOGLE_MAPS_API_KEY else 'No'}")
if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Make GOOGLE_MAPS_API_KEY available to templates
@app.context_processor
def inject_google_maps_key():
    return dict(GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Database operations class
class DatabaseOperations:
    def __init__(self):
        self.supabase = supabase

    def get_all_agents(self):
        try:
            response = self.supabase.table('assistants').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching agents: {str(e)}")
            return []

    def get_agent(self, agent_id):
        try:
            response = self.supabase.table('assistants').select('*').eq('assistant_id', agent_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching agent: {str(e)}")
            return None

    def create_agent(self, agent_data):
        try:
            response = self.supabase.table('assistants').insert(agent_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating agent: {str(e)}")
            return None

    def update_agent(self, agent_id, agent_data):
        try:
            response = self.supabase.table('assistants').update(agent_data).eq('assistant_id', agent_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating agent: {str(e)}")
            return None

    def delete_agent(self, agent_id):
        try:
            response = self.supabase.table('assistants').delete().eq('assistant_id', agent_id).execute()
            return True if response.data else False
        except Exception as e:
            print(f"Error deleting agent: {str(e)}")
            return False

    def get_agent_chat_history(self, agent_id):
        try:
            response = self.supabase.table('chat_history').select('*').eq('agent_id', agent_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching chat history: {str(e)}")
            return []

    def save_chat_history(self, chat_data):
        try:
            response = self.supabase.table('chat_history').insert(chat_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving chat history: {str(e)}")
            return None

    def get_all_venues(self):
        try:
            response = self.supabase.table('venues').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching venues: {str(e)}")
            return []

    def get_all_organizers(self):
        try:
            response = self.supabase.table('organizers').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching organizers: {str(e)}")
            return []

    def get_all_tags(self):
        try:
            response = self.supabase.table('tags').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching tags: {str(e)}")
            return []

# Initialize database operations
db = DatabaseOperations()

def process_photos(photos):
    """Helper function to process photo data from Google Places API"""
    if not photos:
        return []
    
    processed_photos = []
    for photo in photos:
        processed_photos.append({
            'photo_reference': photo.get('photo_reference'),
            'height': photo.get('height'),
            'width': photo.get('width'),
            'html_attributions': photo.get('html_attributions', [])
        })
    return processed_photos

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            # Hardcoded credentials
            if email == "fernando@apis-ia.com" and password == "Naopassara0":
                session['user'] = {
                    'id': '1',
                    'email': 'fernando@apis-ia.com',
                    'first_name': 'Fernando',
                    'last_name': 'Admin',
                    'role': 'admin'
                }
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid email or password")
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return render_template('login.html', error="An error occurred during login")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/recommendations')
def recommendations():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('recommendations.html', user=session['user'])

@app.route('/new-recommendation', methods=['GET', 'POST'])
def new_recommendation():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        if request.method == 'POST':
            data = request.get_json()
            print("Received POST data:", data)
            return jsonify({
                'success': True,
                'message': 'Form submitted successfully'
            })
        else:
            # GET request - render the template
            return render_template(
                'new_recommendation.html',
                user=session['user'],
                google_maps_key=GOOGLE_MAPS_API_KEY
            )
            
    except Exception as e:
        print(f"Error in new_recommendation: {str(e)}")
        if request.method == 'POST':
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        else:
            # For GET requests, redirect to recommendations page on error
            return redirect(url_for('recommendations'))

@app.route('/edit-agent')
def edit_agent():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        # Fetch all agents from Supabase
        response = supabase.table("assistants").select("*").execute()
        agents = response.data if response.data else []

        # Get selected agent if provided in query params
        selected_agent_id = request.args.get('id')
        selected_agent = None
        
        if selected_agent_id:
            agent_response = supabase.table("assistants").select("*").eq("assistant_id", selected_agent_id).execute()
            if agent_response.data and len(agent_response.data) > 0:
                selected_agent = agent_response.data[0]

        return render_template('edit_agent.html', 
                            user=session['user'],
                            agents=agents,
                            selected_agent=selected_agent)
                            
    except Exception as e:
        print(f"Error in edit_agent route: {str(e)}")
        # Return empty lists if there's an error
        return render_template('edit_agent.html',
                            user=session['user'],
                            agents=[],
                            selected_agent=None,
                            error="Error loading agents")

@app.route('/api/save-agent', methods=['POST'])
def save_agent():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        agent_data = {
            'assistant_id': data.get('assistant_id'),
            'assistant_name': data.get('name'),
            'assistant_type': data.get('type', 'classic'),
            'assistant_desc': data.get('description'),
            'assistant_instructions': data.get('prompt'),
            'assistant_functions': data.get('functions', 'not_defined'),
            'subtype': data.get('subtype', 'subtype'),
            'assistant_languages': data.get('languages'),
            'sponsor_id': data.get('sponsor_id'),
            'sponsor_logo': data.get('sponsor_logo', 'sponsor_default.png'),
            'sponsor_url': data.get('sponsor_url', 'https://apis-ia.com'),
            'assistant_json': data.get('config')
        }
        
        if agent_data['assistant_id']:
            # Update existing agent
            response = supabase.table("assistants").update(agent_data).eq("assistant_id", agent_data['assistant_id']).execute()
        else:
            # Create new agent
            response = supabase.table("assistants").insert(agent_data).execute()
            
        return jsonify({'success': True, 'message': 'Agent saved successfully', 'data': response.data})
        
    except Exception as e:
        print(f"Error saving agent: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/delete-agent', methods=['POST'])
def delete_agent():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        assistant_id = data.get('assistant_id')
        
        if not assistant_id:
            return jsonify({'success': False, 'message': 'No assistant ID provided'}), 400
            
        response = supabase.table("assistants").delete().eq("assistant_id", assistant_id).execute()
        return jsonify({'success': True, 'message': 'Agent deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting agent: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/add-assistant')
def add_assistant():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('add_assistant.html', user=session['user'])

@app.route('/assistant-directory')
def assistant_directory():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('assistant_directory.html', user=session['user'])

@app.route('/events')
def events_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('events.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/functionalities/<assistant_id>/<language>')
def get_functionalities(assistant_id, language):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        response = supabase.table("assistants_func_text").select("*")\
            .eq("assistant_id", assistant_id)\
            .eq("language", language)\
            .execute()
        functionalities = response.data if response.data else []
        
        return jsonify({
            'success': True,
            'functionalities': functionalities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/save-functionalities', methods=['POST'])
def save_functionalities():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        assistant_id = data.get('assistant_id')
        functionalities = data.get('functionalities', [])
        
        # Delete existing functionalities for this assistant and language
        supabase.table("assistants_func_text")\
            .delete()\
            .eq("assistant_id", assistant_id)\
            .eq("language", functionalities[0]['language'])\
            .execute()
        
        # Insert new functionalities
        for func in functionalities:
            supabase.table("assistants_func_text")\
                .insert({
                    'assistant_id': assistant_id,
                    'functionality_text': func['text'],
                    'language': func['language']
                })\
                .execute()
        
        return jsonify({'success': True, 'message': 'Functionalities saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/recommendations/create', methods=['POST'])
def create_recommendation():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        print("\n=== Create Recommendation Debug ===")
        print("Received data:", data)
        
        # Validate required fields
        required_fields = {
            'title': str,
            'description': str,
            'place': dict
        }
        
        # Validate required fields
        missing_fields = []
        invalid_types = []
        
        for field, expected_type in required_fields.items():
            if field not in data:
                missing_fields.append(field)
            elif not isinstance(data[field], expected_type):
                invalid_types.append(f"{field} (expected {expected_type.__name__})")
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Create recommendation record
        recommendation = {
            'title': data['title'],
            'description': data['description'],
            'place_id': data['place'].get('place_id'),
            'place_name': data['place'].get('name'),
            'latitude': data['place'].get('latitude'),
            'longitude': data['place'].get('longitude'),
            'address': data['place'].get('address'),
            'created_by': session['user']['id'],
            'status': 'active',
            'tags': data.get('tags', []),
            'images': data.get('images', []),
            'category': data.get('category', 'general')
        }
        
        print("Saving recommendation:", recommendation)
        
        result = db.supabase.table('recommendations').insert(recommendation).execute()
        
        if result.data:
            print("Successfully created recommendation:", result.data[0])
            return jsonify({
                'success': True,
                'message': 'Recommendation created successfully',
                'recommendation': result.data[0]
            })
        else:
            print("Failed to create recommendation - no data returned")
            return jsonify({
                'success': False,
                'message': 'Failed to create recommendation'
            }), 500
            
    except Exception as e:
        print(f"Error creating recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error creating recommendation: {str(e)}'
        }), 500

@app.route('/api/recommendations/search', methods=['GET', 'POST'])
def search_recommendations():
    """
    Search endpoint that makes a single call to Google Places API
    """
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        # Handle both GET and POST requests
        if request.method == 'POST':
            data = request.get_json()
            query = data.get('query', '').strip()
        else:  # GET request
            query = request.args.get('query', '').strip()
            
        print(f"\n=== Search Request Debug ===")
        print(f"Method: {request.method}")
        print(f"Query: '{query}'")
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Search query is required'
            }), 400
            
        # Search using Google Places API
        places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        print("\nMaking request to Google Places API:")
        print(f"URL: {places_url}")
        print(f"Params: query={query}, key=...{GOOGLE_MAPS_API_KEY[-6:]}")  # Only show last 6 chars of key
        
        response = requests.get(places_url, params=params)
        
        print(f"\nResponse Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"\nAPI Status: {response_data.get('status')}")
            
            if response.status_code == 200:
                results = response_data.get('results', [])
                print(f"Number of results: {len(results)}")
                
                # Format places
                formatted_places = []
                for place in results:
                    photos = place.get('photos', [])
                    photo_references = [photo.get('photo_reference') for photo in photos]
                    
                    print(f"Photos for {place.get('name')}: {len(photo_references)}") # Debug log
                    
                    formatted_place = {
                        'place_id': place.get('place_id'),
                        'name': place.get('name'),
                        'address': place.get('formatted_address'),
                        'latitude': place.get('geometry', {}).get('location', {}).get('lat'),
                        'longitude': place.get('geometry', {}).get('location', {}).get('lng'),
                        'rating': place.get('rating'),
                        'user_ratings_total': place.get('user_ratings_total'),
                        'price_level': place.get('price_level'),
                        'types': place.get('types', []),
                        'business_status': place.get('business_status'),
                        'photos': photo_references,  # Store all photo references
                        'icon': place.get('icon'),
                        'icon_background_color': place.get('icon_background_color'),
                        'icon_mask_base_uri': place.get('icon_mask_base_uri'),
                        'opening_hours': place.get('opening_hours', {}).get('open_now'),
                        'plus_code': place.get('plus_code', {})
                    }
                    formatted_places.append(formatted_place)
                    print(f"Found place: {formatted_place['name']}")
                
                return jsonify({
                    'success': True,
                    'results': formatted_places
                })
            else:
                error_message = response_data.get('error_message', 'Unknown error')
                print(f"\nAPI Error: {error_message}")
                return jsonify({
                    'success': False,
                    'message': f'Google Places API Error: {error_message}'
                }), response.status_code
                
        except ValueError as e:
            print(f"\nError parsing JSON response: {str(e)}")
            print(f"Raw response: {response.text[:200]}...")  # Show first 200 chars
            return jsonify({
                'success': False,
                'message': 'Invalid response from Google Places API'
            }), 500
            
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        result = db.supabase.table('recommendations')\
            .select('*')\
            .eq('status', 'active')\
            .order('created_at', desc=True)\
            .execute()
            
        return jsonify({
            'success': True,
            'recommendations': result.data if result.data else []
        })
        
    except Exception as e:
        print(f"Error fetching recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error fetching recommendations: {str(e)}'
        }), 500

@app.route('/api/recommendations/<int:recommendation_id>', methods=['DELETE'])
def delete_recommendation(recommendation_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        # Soft delete by updating status
        result = supabase.table('recommendations')\
            .update({'status': 'deleted'})\
            .eq('id', recommendation_id)\
            .execute()
            
        if result.data:
            return jsonify({
                'success': True,
                'message': 'Recommendation deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Recommendation not found'
            }), 404
            
    except Exception as e:
        print(f"Error deleting recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error deleting recommendation: {str(e)}'
        }), 500

@app.route('/api/places', methods=['POST'])
def save_places():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        # Required fields
        required_fields = ['place_id', 'name', 'latitude', 'longitude', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
        
        # Check if place already exists
        existing = db.supabase.table('places')\
            .select('*')\
            .eq('place_id', data['place_id'])\
            .execute()
            
        if existing.data:
            # Update existing place
            result = db.supabase.table('places')\
                .update({
                    'name': data['name'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    'address': data['address'],
                    'types': data.get('types', []),
                    'phone': data.get('phone', ''),
                    'website': data.get('website', ''),
                    'photos': data.get('photos', []),
                    'rating': data.get('rating', 0),
                    'updated_at': 'NOW()'
                })\
                .eq('place_id', data['place_id'])\
                .execute()
        else:
            # Create new place
            result = db.supabase.table('places')\
                .insert({
                    'place_id': data['place_id'],
                    'name': data['name'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    'address': data['address'],
                    'types': data.get('types', []),
                    'phone': data.get('phone', ''),
                    'website': data.get('website', ''),
                    'photos': data.get('photos', []),
                    'rating': data.get('rating', 0),
                    'created_by': session['user']['id']
                })\
                .execute()
        
        if result.data:
            return jsonify({
                'success': True,
                'message': 'Place saved successfully',
                'place': result.data[0]
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save place'
            }), 500
            
    except Exception as e:
        print(f"Error saving place: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error saving place: {str(e)}'
        }), 500

@app.route('/api/places', methods=['GET'])
def get_places():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        # Get query parameters
        search = request.args.get('search', '')
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        radius = request.args.get('radius', 5000)  # Default 5km radius
        
        query = db.supabase.table('places').select('*')
        
        # Add search filter if provided
        if search:
            query = query.ilike('name', f'%{search}%')
        
        # Add location filter if provided
        if lat and lng:
            # Note: This is a simplified distance calculation
            # For more accurate results, consider using PostGIS
            lat, lng = float(lat), float(lng)
            radius = float(radius)
            
            query = query.filter(
                f"(latitude BETWEEN {lat - radius/111000} AND {lat + radius/111000}) AND " +
                f"(longitude BETWEEN {lng - radius/(111000*cos(lat*pi/180))} AND {lng + radius/(111000*cos(lat*pi/180))})"
            )
        
        result = query.execute()
        
        return jsonify({
            'success': True,
            'places': result.data if result.data else []
        })
        
    except Exception as e:
        print(f"Error fetching places: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error fetching places: {str(e)}'
        }), 500

@app.route('/api/places/<place_id>', methods=['GET'])
def get_place(place_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        result = db.supabase.table('places')\
            .select('*')\
            .eq('place_id', place_id)\
            .execute()
            
        if result.data:
            return jsonify({
                'success': True,
                'place': result.data[0]
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Place not found'
            }), 404
            
    except Exception as e:
        print(f"Error fetching place: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error fetching place: {str(e)}'
        }), 500

@app.route('/api/places/search', methods=['GET'])
def search_places():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        # Get search parameters
        query = request.args.get('query', '')
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Search query is required'
            }), 400
            
        # Construct Google Places API request
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        # Add location if provided
        if lat and lng:
            params['location'] = f"{lat},{lng}"
            params['radius'] = 50000  # 50km radius
        
        # Make request to Google Places API
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            
            # Format results
            places = []
            for place in results:
                places.append({
                    'place_id': place.get('place_id'),
                    'name': place.get('name'),
                    'address': place.get('formatted_address'),
                    'latitude': place.get('geometry', {}).get('location', {}).get('lat'),
                    'longitude': place.get('geometry', {}).get('location', {}).get('lng'),
                    'types': place.get('types', []),
                    'rating': place.get('rating'),
                    'photos': [photo.get('photo_reference') for photo in place.get('photos', [])]
                })
            
            return jsonify({
                'success': True,
                'places': places
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to fetch places from Google API'
            }), response.status_code
            
    except Exception as e:
        print(f"Error searching places: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error searching places: {str(e)}'
        }), 500

@app.route('/api/places/details/<place_id>', methods=['GET'])
def get_place_details(place_id):
    try:
        # Get place details from Google Places API directly
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'key': GOOGLE_MAPS_API_KEY,
            'fields': ','.join([
                'place_id', 'name', 'formatted_address', 'formatted_phone_number',
                'geometry', 'icon', 'photos', 'rating', 'reviews', 'types',
                'user_ratings_total', 'website', 'price_level', 'business_status',
                'opening_hours', 'wheelchair_accessible_entrance'
            ])
        }
        
        response = requests.get(url, params=params)
        place = response.json()
        
        if place['status'] == 'OK':
            place_details = place['result']
            
            # Extract latitude and longitude
            latitude = place_details.get('geometry', {}).get('location', {}).get('lat')
            longitude = place_details.get('geometry', {}).get('location', {}).get('lng')
            
            response_data = {
                'place_id': place_details.get('place_id'),
                'name': place_details.get('name'),
                'formatted_address': place_details.get('formatted_address'),
                'formatted_phone_number': place_details.get('formatted_phone_number'),
                'website': place_details.get('website'),
                'rating': place_details.get('rating'),
                'user_ratings_total': place_details.get('user_ratings_total'),
                'price_level': place_details.get('price_level'),
                'business_status': place_details.get('business_status'),
                'types': place_details.get('types', []),
                'latitude': latitude,
                'longitude': longitude,
                'photos': process_photos(place_details.get('photos', [])),
                'opening_hours': place_details.get('opening_hours', {}),
                'wheelchair_accessible': place_details.get('wheelchair_accessible_entrance', False),
                'reviews': place_details.get('reviews', [])
            }
            
            return jsonify({
                'success': True,
                'place': response_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Place not found'
            }), 404
            
    except Exception as e:
        print(f"Error getting place details: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting place details: {str(e)}'
        }), 500

@app.route('/api/places/photo/<photo_reference>', methods=['GET'])
def get_place_photo(photo_reference):
    """
    Proxy endpoint to fetch photos from Google Places Photos API
    """
    try:
        # Google Places Photo API URL
        photo_url = "https://maps.googleapis.com/maps/api/place/photo"
        
        # Parameters for max width/height (adjust as needed)
        params = {
            'maxwidth': '400',  # or maxheight
            'photo_reference': photo_reference,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        # Make request to Google Places Photo API
        response = requests.get(photo_url, params=params)
        
        if response.status_code == 200:
            # Return the image with proper content type
            return Response(
                response.content,
                mimetype=response.headers['Content-Type']
            )
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to fetch photo'
            }), response.status_code
            
    except Exception as e:
        print(f"Error fetching photo: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error fetching photo: {str(e)}'
        }), 500

@app.route('/api/places/save', methods=['POST'])
def save_place():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        # 1. Save main place data
        place_data = data['place']
        place_result = supabase.table('places').upsert(place_data).execute()
        
        if not place_result.data:
            raise Exception('Failed to save place data')
        
        place_id = place_data['place_id']
        
        # 2. Save geometry data
        if 'geometry' in data:
            geometry_data = data['geometry']
            geometry_data['place_id'] = place_id
            supabase.table('place_geometry').upsert(geometry_data).execute()
        
        # 3. Save services data
        if 'services' in data:
            services_data = data['services']
            services_data['place_id'] = place_id
            supabase.table('place_services').upsert(services_data).execute()
        
        # 4. Save opening hours
        if 'opening_hours' in data and data['opening_hours']:
            # First delete existing hours
            supabase.table('place_opening_hours').delete().eq('place_id', place_id).execute()
            # Then insert new hours
            for hours in data['opening_hours']:
                hours['place_id'] = place_id
                supabase.table('place_opening_hours').insert(hours).execute()
        
        # 5. Save reviews
        if 'reviews' in data and data['reviews']:
            # First delete existing reviews
            supabase.table('place_reviews').delete().eq('place_id', place_id).execute()
            # Then insert new reviews
            for review in data['reviews']:
                review['place_id'] = place_id
                supabase.table('place_reviews').insert(review).execute()
        
        # 6. Save photos
        if 'photos' in data and data['photos']:
            print("\n=== Photo Saving Debug ===")
            print(f"Number of photos to save: {len(data['photos'])}")
            
            # First delete existing photos
            delete_result = supabase.table('place_photos').delete().eq('place_id', place_id).execute()
            print(f"Deleted existing photos: {delete_result.data}")
            
            # Download and store each photo
            for index, photo in enumerate(data['photos']):
                print(f"\nProcessing photo {index + 1}/{len(data['photos'])}")
                print(f"Photo data: {photo}")
                
                photo['place_id'] = place_id
                
                # Fetch photo from Google
                photo_url = "https://maps.googleapis.com/maps/api/place/photo"
                params = {
                    'maxwidth': '800',  # Get larger size for storage
                    'photo_reference': photo['photo_reference'],
                    'key': GOOGLE_MAPS_API_KEY
                }
                
                print(f"Fetching photo from Google: {photo_url}")
                response = requests.get(photo_url, params=params)
                print(f"Google API Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Generate unique filename
                    filename = f"{place_id}/{photo['photo_reference']}.jpg"
                    print(f"Generated filename: {filename}")
                    
                    try:
                        # Create folder if it doesn't exist
                        folder = f"{place_id}"
                        print(f"Creating folder in bucket: {folder}")
                        try:
                            folder_result = supabase.storage.from_('place-photos').create_folder(folder)
                            print(f"Folder creation result: {folder_result}")
                        except Exception as folder_error:
                            print(f"Folder creation error (might already exist): {str(folder_error)}")
                        
                        # Upload to Supabase Storage
                        print("Uploading to Supabase Storage...")
                        storage_response = supabase.storage.from_('place-photos').upload(
                            filename,
                            response.content,
                            {'content-type': response.headers['Content-Type'], 'upsert': True}
                        )
                        print(f"Storage upload response: {storage_response}")
                        
                        # Get public URL
                        public_url = supabase.storage.from_('place-photos').get_public_url(filename)
                        print(f"Generated public URL: {public_url}")
                        
                        # Save photo data with storage URL and created_by
                        photo_data = {
                            'place_id': place_id,
                            'photo_reference': photo['photo_reference'],
                            'height': photo.get('height'),
                            'width': photo.get('width'),
                            'html_attributions': photo.get('html_attributions', []),
                            'created_by': session['user']['id'],
                            'storage_url': public_url
                        }
                        print(f"Saving photo data to database: {photo_data}")
                        
                        insert_result = supabase.table('place_photos').insert(photo_data).execute()
                        print(f"Database insert result: {insert_result.data}")
                        
                    except Exception as storage_error:
                        print(f"Error saving photo {filename}: {str(storage_error)}")
                        print(f"Full error details: {storage_error.__class__.__name__}")
                        import traceback
                        print(f"Traceback: {traceback.format_exc()}")
                        continue
                else:
                    print(f"Failed to fetch photo from Google. Status code: {response.status_code}")
                    print(f"Response content: {response.text[:200]}...")  # First 200 chars
        
        return jsonify({
            'success': True,
            'message': 'Place saved successfully',
            'place_id': place_id
        })
            
    except Exception as e:
        print(f"Error saving place: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error saving place: {str(e)}'
        }), 500

@app.route('/api/places/<place_id>', methods=['GET'])
def check_place_exists(place_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        result = supabase.table('places').select('place_id').eq('place_id', place_id).execute()
        return jsonify({
            'success': True,
            'exists': len(result.data) > 0
        })
        
    except Exception as e:
        print(f"Error checking place: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error checking place: {str(e)}'
        }), 500

@app.route('/api/storage/upload', methods=['POST'])
def upload_to_storage():
    try:
        data = request.json
        filename = data.get('filename')
        content_type = data.get('contentType')
        base64_data = data.get('base64Data')

        if not all([filename, content_type, base64_data]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        # Decode base64 data
        binary_data = base64.b64decode(base64_data)

        # Upload to Supabase Storage
        bucket_name = 'place-photos'  # Your Supabase storage bucket name
        storage_client = supabase.storage.from_(bucket_name)
        
        # Extract folder name (place_id) from filename
        folder = filename.split('/')[0]
        
        try:
            # Create folder if it doesn't exist
            try:
                storage_client.create_folder(folder)
            except Exception as folder_error:
                print(f"Folder creation error (might already exist): {str(folder_error)}")

            # Upload the file directly
            result = storage_client.upload(
                path=filename,
                file=binary_data,
                file_options={
                    "content-type": content_type
                }
            )

            # Get the public URL
            public_url = storage_client.get_public_url(filename)

            return jsonify({
                'success': True,
                'url': public_url
            })

        except Exception as storage_error:
            print(f"Storage operation error: {str(storage_error)}")
            raise storage_error

    except Exception as e:
        print('Error uploading to storage:', str(e))
        import traceback
        print('Traceback:', traceback.format_exc())
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)