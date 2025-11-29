import random
import time
from datetime import datetime, timedelta

def calculate_power(level, missiles, fighters, defense_level):
    """محاسبه قدرت کاربر"""
    base_power = level * 100
    missile_power = sum(missile['quantity'] * get_missile_power(missile['type']) for missile in missiles)
    fighter_power = len(fighters) * 500
    defense_power = defense_level * 200
    
    return base_power + missile_power + fighter_power + defense_power

def get_missile_power(missile_type):
    """برگرداندن قدرت موشک"""
    power_map = {
        "تیرباران": 10, "رعدآسا": 15, "تندباد": 20, "زلزله": 25,
        "آتشفشان": 100, "توفان‌نو": 150, "خاموش‌کن": 200,
        "عقاب‌توفان": 500, "اژدهای‌آتش": 750, "فینیکس": 1000
    }
    return power_map.get(missile_type, 5)

def calculate_attack_damage(missile_type, attacker_level, defense_level):
    """محاسبه دمیج حمله"""
    base_damage = {
        "تیرباران": 60, "رعدآسا": 90, "تندباد": 120, "زلزله": 130,
        "آتشفشان": 2000, "توفان‌نو": 3000, "خاموش‌کن": 0,  # قطع سیستم
        "عقاب‌توفان": 8000, "اژدهای‌آتش": 12500, "فینیکس": 18000
    }.get(missile_type, 50)
    
    # تاثیر سطح حمله‌کننده
    level_bonus = attacker_level * 10
    
    # کاهش بر اساس پدافند مدافع
    defense_reduction = defense_level * 15
    
    final_damage = base_damage + level_bonus - defense_reduction
    return max(final_damage, 10)  # حداقل 10 دمیج

def check_critical_hit():
    """بررسی حمله بحرانی"""
    return random.random() <= 0.15  # 15% شانس

def calculate_loot(attacker_level, defender_coins, is_critical=False):
    """محاسبه غارت"""
    max_loot = min(defender_coins * 0.3, 1000)  # حداکثر 30% موجودی مدافع
    base_loot = random.randint(50, int(max_loot))
    
    if is_critical:
        base_loot *= 2
    
    return min(base_loot, defender_coins)  # بیشتر از موجودی مدافع نباشد

def format_time(seconds):
    """فرمت کردن زمان به صورت خوانا"""
    if seconds < 60:
        return f"{int(seconds)} ثانیه"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours} ساعت و {minutes} دقیقه"
    else:
        return f"{minutes} دقیقه"

def get_league_info(power):
    """تعیین لیگ بر اساس قدرت"""
    if power >= 20000:
        return "👑 افسانه‌ای", 5
    elif power >= 10000:
        return "💎 تیتان", 4
    elif power >= 6000:
        return "🥇 طلایی", 3
    elif power >= 3000:
        return "🥈 نقره‌ای", 2
    elif power >= 1000:
        return "🥉 برنز", 1
    else:
        return "🎯 مبتدی", 0
