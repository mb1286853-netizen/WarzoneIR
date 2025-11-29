import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_path='zone.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول کاربران
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                language TEXT DEFAULT 'fa',
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                power INTEGER DEFAULT 0,
                zone_coin INTEGER DEFAULT 1000,
                zone_gem INTEGER DEFAULT 
