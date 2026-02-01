"""
NANBAN AI - Tamil Conversational Companion
Main Flask Application Server
"""

from flask import Flask, render_template, request, jsonify, session, make_response
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
    session['voice_enabled'] = data.get('voice_enabled', False)
    
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
    image_data = data.get('image_data')
    image_mime = data.get('image_mime')
    mood = data.get('mood')
    reply_mode = data.get('reply_mode')
    
    # Get user context
    user_id = session.get('user_id')
    slang = session.get('slang', 'COMMON')
    persona = session.get('persona', 'JALIANA')
    user_name = session.get('user_name', '')
    voice_enabled = session.get('voice_enabled', False)
    memory = db.get_memory(user_id) if user_id else None
    current_mood = mood or session.get('mood', 'CHILL')
    current_reply_mode = reply_mode or session.get('reply_mode', 'quick')
    memory_facts = ''

    if memory and memory.get('consent') is True:
        memory_facts = memory.get('facts', '')
        if not mood:
            current_mood = memory.get('mood', current_mood)
        if not reply_mode:
            current_reply_mode = memory.get('reply_mode', current_reply_mode)

    session['mood'] = current_mood
    session['reply_mode'] = current_reply_mode
    
    if not user_message and not image_data:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get conversation history
        history = db.get_conversation_history(user_id) if user_id else []
        
        # Generate AI response (image or text)
        if image_data:
            ai_result = brain.chat_with_image(
                user_message=user_message or "இந்த படத்தில என்ன இருக்கு?",
                image_data=image_data,
                image_mime=image_mime,
                slang=slang,
                persona=persona,
                user_name=user_name,
                mood=current_mood,
                reply_mode=current_reply_mode,
                memory_facts=memory_facts
            )
        else:
            ai_result = brain.chat(
                user_message=user_message,
                slang=slang,
                persona=persona,
                user_name=user_name,
                conversation_history=history,
                mood=current_mood,
                reply_mode=current_reply_mode,
                memory_facts=memory_facts
            )

        ai_response = ai_result.get('text') if isinstance(ai_result, dict) else ai_result
        is_fallback = ai_result.get('fallback') if isinstance(ai_result, dict) else False
        suggestions = ai_result.get('suggestions') if isinstance(ai_result, dict) else None
        
        # Save conversation
        if user_id:
            if user_message:
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
            'timestamp': datetime.now().isoformat(),
            'fallback': bool(is_fallback),
            'suggestions': suggestions
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

@app.route('/api/memory/status', methods=['GET'])
def memory_status():
    user_id = session.get('user_id')
    memory = db.get_memory(user_id) if user_id else {
        'consent': None,
        'facts': '',
        'mood': session.get('mood', 'CHILL'),
        'reply_mode': session.get('reply_mode', 'quick')
    }
    return jsonify(memory)

@app.route('/api/memory/update', methods=['POST'])
def memory_update():
    user_id = session.get('user_id')
    data = request.json or {}
    consent = data.get('consent')
    facts = data.get('facts', '')
    mood = data.get('mood', session.get('mood', 'CHILL'))
    reply_mode = data.get('reply_mode', session.get('reply_mode', 'quick'))

    session['mood'] = mood
    session['reply_mode'] = reply_mode
    session['memory_consent'] = consent
    session['memory_facts'] = facts

    if user_id:
        db.set_memory(user_id, consent=consent, facts=facts, mood=mood, reply_mode=reply_mode)

    return jsonify({'success': True})

@app.route('/api/memory/forget', methods=['POST'])
def memory_forget():
    user_id = session.get('user_id')
    session.pop('memory_consent', None)
    session.pop('memory_facts', None)
    session.pop('mood', None)
    session.pop('reply_mode', None)
    if user_id:
        db.clear_memory(user_id)
    return jsonify({'success': True})

@app.route('/api/checkin/status', methods=['GET'])
def checkin_status():
    user_id = session.get('user_id')
    today = datetime.now().date().isoformat()
    data = db.get_checkin(user_id, today) if user_id else None
    return jsonify({'done': bool(data), 'data': data})

@app.route('/api/checkin', methods=['POST'])
def checkin_update():
    user_id = session.get('user_id')
    data = request.json or {}
    mood = data.get('mood', '')
    note = data.get('note', '')
    if not user_id:
        return jsonify({'error': 'No user found'}), 404
    today = datetime.now().date().isoformat()
    db.upsert_checkin(user_id, today, mood, note)
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    # Avoid noisy 404s for favicon
    return make_response('', 204)

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
