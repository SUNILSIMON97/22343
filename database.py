"""
NANBAN AI - Database Handler
SQLite database for user data and conversation storage
"""

import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='nanban.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                slang TEXT DEFAULT 'COMMON',
                persona TEXT DEFAULT 'JALIANA',
                voice_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                total_messages INTEGER DEFAULT 0,
                total_sessions INTEGER DEFAULT 1,
                favorite_slang TEXT,
                favorite_persona TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully")
    
    def create_user(self, name='', slang='COMMON', persona='JALIANA'):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, slang, persona)
            VALUES (?, ?, ?)
        ''', (name, slang, persona))
        
        user_id = cursor.lastrowid
        
        # Initialize stats
        cursor.execute('''
            INSERT INTO user_stats (user_id, favorite_slang, favorite_persona)
            VALUES (?, ?, ?)
        ''', (user_id, slang, persona))
        
        conn.commit()
        conn.close()
        
        return user_id
    
    def update_user_preferences(self, user_id, slang=None, persona=None, name=None):
        """Update user preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if slang:
            updates.append('slang = ?')
            params.append(slang)
        if persona:
            updates.append('persona = ?')
            params.append(persona)
        if name:
            updates.append('name = ?')
            params.append(name)
        
        if updates:
            updates.append('last_active = CURRENT_TIMESTAMP')
            params.append(user_id)
            
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def save_message(self, user_id, role, content):
        """Save a conversation message"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (user_id, role, content)
            VALUES (?, ?, ?)
        ''', (user_id, role, content))
        
        # Update user stats
        cursor.execute('''
            UPDATE user_stats
            SET total_messages = total_messages + 1
            WHERE user_id = ?
        ''', (user_id,))
        
        # Update last active
        cursor.execute('''
            UPDATE users
            SET last_active = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, user_id, limit=20):
        """Get recent conversation history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, timestamp
            FROM conversations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Reverse to get chronological order
        history = [
            {
                'role': row['role'],
                'content': row['content'],
                'timestamp': row['timestamp']
            }
            for row in reversed(rows)
        ]
        
        return history
    
    def clear_conversation_history(self, user_id):
        """Clear all conversation history for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM conversations
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.name, u.slang, u.persona, u.created_at, u.last_active,
                   s.total_messages, s.total_sessions, s.favorite_slang, s.favorite_persona
            FROM users u
            JOIN user_stats s ON u.id = s.user_id
            WHERE u.id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'name': row['name'],
                'current_slang': row['slang'],
                'current_persona': row['persona'],
                'created_at': row['created_at'],
                'last_active': row['last_active'],
                'total_messages': row['total_messages'],
                'total_sessions': row['total_sessions'],
                'favorite_slang': row['favorite_slang'],
                'favorite_persona': row['favorite_persona']
            }
        
        return None
    
    def get_all_users_count(self):
        """Get total number of users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM users')
        count = cursor.fetchone()['count']
        
        conn.close()
        return count
    
    def get_total_conversations(self):
        """Get total number of conversations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM conversations')
        count = cursor.fetchone()['count']
        
        conn.close()
        return count
