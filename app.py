"""
NANBAN AI - Tamil Conversational Companion
Main Flask Application Server
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
import json
from openai_brain import NanbanBrain
from voice_handler import VoiceHandler
from database import Database

# Load local environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nanban-secret-key-change-in-production')
CORS(app)

# Initialize components
brain = NanbanBrain()
voice = VoiceHandler()
db = Database()

@app.route('/')
def home():
    """Landing page"""
    return render_template('home.html')

@app.route('/setup')
def setup():
    """Slang and Persona selection page"""
    return render_template('setup.html')

@app.route('/chat')
def chat():
    """Main chat interface"""
    # Get user preferences from session or use defaults
    slang = session.get('slang', 'COMMON')
    persona = session.get('persona', 'JALIANA')
    user_name = session.get('user_name', '')
    
    return render_template('chat.html', 
                         slang=slang, 
                         persona=persona,
                         user_name=user_name)

@app.route('/api/save-preferences', methods=['POST'])
def save_preferences():
    """Save user's slang and persona preferences"""
    data = request.json
    
    session['slang'] = data.get('slang', 'COMMON')
    session['persona'] = data.get('persona', 'JALIANA')
    session['user_name'] = data.get('name', '')
    session['voice_enabled'] = data.get('voice_enabled', True)
    
    # Save to database
    user_id = session.get('user_id')
    if not user_id:
        user_id = db.create_user(
            name=session['user_name'],
            slang=session['slang'],
            persona=session['persona']
        )
        session['user_id'] = user_id
    else:
        db.update_user_preferences(
            user_id=user_id,
            slang=session['slang'],
            persona=session['persona'],
            name=session['user_name']
        )
    
    return jsonify({
        'success': True,
        'message': 'Preferences saved!'
    })

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '')
    
    # Get user context
    user_id = session.get('user_id')
    slang = session.get('slang', 'COMMON')
    persona = session.get('persona', 'JALIANA')
    user_name = session.get('user_name', '')
    voice_enabled = session.get('voice_enabled', True)
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get conversation history
        history = db.get_conversation_history(user_id) if user_id else []
        
        # Generate AI response
        ai_response = brain.chat(
            user_message=user_message,
            slang=slang,
            persona=persona,
            user_name=user_name,
            conversation_history=history
        )
        
        # Save conversation
        if user_id:
            db.save_message(user_id, 'user', user_message)
            db.save_message(user_id, 'assistant', ai_response)
        
        # Generate voice if enabled
        audio_url = None
        if voice_enabled:
            try:
                audio_url = voice.text_to_speech(
                    text=ai_response,
                    slang=slang,
                    persona=persona
                )
            except Exception as e:
                print(f"Voice generation error: {e}")
                # Continue without voice if it fails
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'audio_url': audio_url,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            'error': 'Sorry, something went wrong. Please try again.',
            'details': str(e)
        }), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    user_id = session.get('user_id')
    if user_id:
        db.clear_conversation_history(user_id)
    
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get user statistics"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user found'}), 404
    
    stats = db.get_user_stats(user_id)
    return jsonify(stats)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create tables if they don't exist
    db.init_db()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True') == 'True'
    
    print(f"""
    🔥 NANBAN AI STARTING... 🔥
    
    நண்பன் AI is now running!
    
    🌐 Open your browser and go to:
    http://localhost:{port}
    
    Press CTRL+C to stop the server.
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
