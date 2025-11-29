from database import Database

db = Database()

class ComboCalculator:
    def __init__(self):
        self.missile_damage = {
            "تیرباران": 60, "رعدآسا": 90, "تندباد": 120, "زلزله": 130,
            "آتشفشان": 2000, "توفان‌نو": 3000, "خاموش‌کن": 0,
            "عقاب‌توفان": 8000, "اژدهای‌آتش": 12500, "فینیکس": 18000
        }
        
        self.fighter_bonus = {
            "شب‌پرواز": 1.0, "توفان‌ساز": 1.1, "آذرخش": 1.2, "شبح‌ساحل": 1.3
        }
        
        self.drone_bonus = {
            "زنبورک": 50, "سایفر": 100, "ریزپرنده": 200, "none": 0
        }
    
    def calculate_combo_damage(self, fighter, drone, missiles_data):
        """محاسبه دمیج ترکیب"""
        total_damage = 0
        
        # محاسبه دمیج موشک‌ها
        for missile_type, quantity in missiles_data.items():
            if missile_type in self.missile_damage:
                total_damage += self.missile_damage[missile_type] * quantity
        
        # افزودن بونوس جنگنده
        fighter_multiplier = self.fighter_bonus.get(fighter, 1.0)
        total_damage *= fighter_multiplier
        
        # افزودن بونوس پهپاد
        drone_bonus = self.drone_bonus.get(drone, 0)
        total_damage += drone_bonus
        
        return int(total_damage)
    
    def save_combo(self, user_id, combo_number, fighter, drone, missiles_data):
        """ذخیره ترکیب در دیتابیس"""
        import json
        missiles_json = json.dumps(missiles_data)
        
        conn = db.conn
        cursor = conn.cursor()
        
        # حذف ترکیب قبلی اگر وجود دارد
        cursor.execute('''
            DELETE FROM attack_combos 
            WHERE user_id = ? AND combo_number = ?
        ''', (user_id, combo_number))
        
        # درج ترکیب جدید
        cursor.execute('''
            INSERT INTO attack_combos (user_id, combo_number, fighter_type, drone_type, missiles_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, combo_number, fighter, drone, missiles_json))
        
        conn.commit()
