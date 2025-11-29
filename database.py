import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_path='zone.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        conn = self.get_connection()
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
                zone_gem INTEGER DEFAULT 0,
                defense_level INTEGER DEFAULT 1,
                cyber_level INTEGER DEFAULT 1,
                miner_level INTEGER DEFAULT 1,
                miner_balance INTEGER DEFAULT 0,
                last_miner_claim INTEGER DEFAULT 0,
                last_bronze_box INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول جنگنده‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fighters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                fighter_type TEXT,
                equipped BOOLEAN DEFAULT FALSE,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # جدول موشک‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                missile_type TEXT,
                quantity INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # جدول ترکیب‌های حمله
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attack_combos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                combo_number INTEGER,
                fighter_type TEXT,
                drone_type TEXT,
                missiles_json TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # جدول تاریخچه حملات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attack_history (
                attack_id INTEGER PRIMARY KEY AUTOINCREMENT,
                attacker_id INTEGER,
                defender_id INTEGER,
                attack_type TEXT,
                damage INTEGER,
                loot INTEGER,
                xp_gained INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def create_user(self, user_id, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username) 
            VALUES (?, ?)
        ''', (user_id, username))
        conn.commit()
        conn.close()
    
    def update_user_coin(self, user_id, amount):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET zone_coin = zone_coin + ? 
            WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()
    
    def update_user_gem(self, user_id, amount):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET zone_gem = zone_gem + ? 
            WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()
    
    def update_user_xp(self, user_id, amount):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET xp = xp + ? 
            WHERE user_id = ?
        ''', (amount, user_id))
        
        # بررسی ارتقا سطح
        cursor.execute('SELECT xp, level FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            xp, level = user
            xp_needed = level * 100
            if xp >= xp_needed:
                # ارتقا سطح
                cursor.execute('''
                    UPDATE users SET level = level + 1, xp = xp - ? 
                    WHERE user_id = ?
                ''', (xp_needed, user_id))
        
        conn.commit()
        conn.close()
    
    def update_miner_balance(self, user_id, balance):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET miner_balance = ? 
            WHERE user_id = ?
        ''', (balance, user_id))
        conn.commit()
        conn.close()
    
    def update_last_miner_claim(self, user_id, timestamp):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET last_miner_claim = ? 
            WHERE user_id = ?
        ''', (timestamp, user_id))
        conn.commit()
        conn.close()
    
    def update_miner_level(self, user_id, level):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET miner_level = ? 
            WHERE user_id = ?
        ''', (level, user_id))
        conn.commit()
        conn.close()
    
    def update_user_bronze_box_time(self, user_id, timestamp):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET last_bronze_box = ? 
            WHERE user_id = ?
        ''', (timestamp, user_id))
        conn.commit()
        conn.close()
    
    def update_user_defense_level(self, user_id, level):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET defense_level = ? 
            WHERE user_id = ?
        ''', (level, user_id))
        conn.commit()
        conn.close()
    
    def update_user_cyber_level(self, user_id, level):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET cyber_level = ? 
            WHERE user_id = ?
        ''', (level, user_id))
        conn.commit()
        conn.close()
    
    def get_user_missiles(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT missile_type, quantity FROM missiles 
            WHERE user_id = ?
        ''', (user_id,))
        missiles = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return missiles
    
    def add_missile(self, user_id, missile_type, quantity):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # بررسی آیا از قبل وجود دارد
        cursor.execute('''
            SELECT quantity FROM missiles 
            WHERE user_id = ? AND missile_type = ?
        ''', (user_id, missile_type))
        
        existing = cursor.fetchone()
        
        if existing:
            # آپدیت تعداد
            cursor.execute('''
                UPDATE missiles SET quantity = quantity + ? 
                WHERE user_id = ? AND missile_type = ?
            ''', (quantity, user_id, missile_type))
        else:
            # درج جدید
            cursor.execute('''
                INSERT INTO missiles (user_id, missile_type, quantity) 
                VALUES (?, ?, ?)
            ''', (user_id, missile_type, quantity))
        
        conn.commit()
        conn.close()
    
    def update_missile_quantity(self, user_id, missile_type, change):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE missiles SET quantity = quantity + ? 
            WHERE user_id = ? AND missile_type = ?
        ''', (change, user_id, missile_type))
        conn.commit()
        conn.close()
    
    def get_user_fighters(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT fighter_type FROM fighters 
            WHERE user_id = ?
        ''', (user_id,))
        fighters = [row[0] for row in cursor.fetchall()]
        conn.close()
        return fighters
    
    def add_fighter(self, user_id, fighter_type):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO fighters (user_id, fighter_type) 
            VALUES (?, ?)
        ''', (user_id, fighter_type))
        conn.commit()
        conn.close()
    
    def get_user_combos(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT combo_number, fighter_type, drone_type, missiles_json 
            FROM attack_combos WHERE user_id = ?
        ''', (user_id,))
        
        combos = []
        for row in cursor.fetchall():
            combo_number, fighter_type, drone_type, missiles_json = row
            missiles_data = json.loads(missiles_json) if missiles_json else {}
            combos.append({
                'combo_number': combo_number,
                'fighter_type': fighter_type,
                'drone_type': drone_type,
                'missiles_data': missiles_data
            })
        
        conn.close()
        return combos
    
    def save_combo(self, user_id, combo_number, fighter_type, drone_type, missiles_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        missiles_json = json.dumps(missiles_data)
        
        # حذف ترکیب قبلی اگر وجود دارد
        cursor.execute('''
            DELETE FROM attack_combos 
            WHERE user_id = ? AND combo_number = ?
        ''', (user_id, combo_number))
        
        # درج ترکیب جدید
        cursor.execute('''
            INSERT INTO attack_combos (user_id, combo_number, fighter_type, drone_type, missiles_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, combo_number, fighter_type, drone_type, missiles_json))
        
        conn.commit()
        conn.close()
    
    def add_attack_history(self, attacker_id, defender_id, attack_type, damage, loot, xp_gained):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attack_history (attacker_id, defender_id, attack_type, damage, loot, xp_gained)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (attacker_id, defender_id, attack_type, damage, loot, xp_gained))
        conn.commit()
        conn.close()
