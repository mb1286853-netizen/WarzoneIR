import time
from database import Database

db = Database()

class MinerSystem:
    def __init__(self):
        self.miner_levels = {
            1: {"production": 100, "upgrade_cost": 100},
            2: {"production": 200, "upgrade_cost": 200},
            3: {"production": 350, "upgrade_cost": 300},
            4: {"production": 550, "upgrade_cost": 400},
            5: {"production": 800, "upgrade_cost": 500},
            6: {"production": 1100, "upgrade_cost": 600},
            7: {"production": 1450, "upgrade_cost": 700},
            8: {"production": 1850, "upgrade_cost": 800},
            9: {"production": 2300, "upgrade_cost": 900},
            10: {"production": 2800, "upgrade_cost": 1000},
            11: {"production": 3400, "upgrade_cost": 1100},
            12: {"production": 4100, "upgrade_cost": 1200},
            13: {"production": 5000, "upgrade_cost": 1300},
            14: {"production": 6100, "upgrade_cost": 1400},
            15: {"production": 7500, "upgrade_cost": 1500}
        }
    
    def calculate_current_balance(self, user_id):
        user = db.get_user(user_id)
        if not user:
            return 0
        
        miner_level = user[10]
        miner_balance = user[11]
        last_claim = user[12]
        
        current_time = int(time.time())
        
        if last_claim == 0:
            return miner_balance
        
        time_since_last_claim = current_time - last_claim
        max_balance = self.miner_levels[miner_level]["production"]
        
        # اگر از 3 ساعت گذشته باشد، بیشتر از ماکسیموم نشود
        if time_since_last_claim >= 10800:  # 3 ساعت
            return max_balance
        
        # محاسبه تولید بر اساس زمان گذاشته
        production_rate = max_balance / 10800  # ZP بر ثانیه
        new_balance = miner_balance + (time_since_last_claim * production_rate)
        
        return min(new_balance, max_balance)
    
    def claim_miner_balance(self, user_id):
        user = db.get_user(user_id)
        if not user:
            return 0
        
        claimable_balance = int(self.calculate_current_balance(user_id))
        
        if claimable_balance > 0:
            # افزودن سکه به کاربر
            db.update_user_coin(user_id, claimable_balance)
            # ریست کردن موجودی ماینر
            db.update_miner_balance(user_id, 0)
            # بروزرسانی زمان آخرین برداشت
            db.update_last_miner_claim(user_id, int(time.time()))
        
        return claimable_balance
    
    def upgrade_miner(self, user_id):
        user = db.get_user(user_id)
        if not user:
            return False, "کاربر یافت نشد"
        
        current_level = user[10]
        user_coins = user[6]
        
        if current_level >= 15:
            return False, "حداکثر سطح ماینر رسیده است"
        
        upgrade_cost = self.miner_levels[current_level + 1]["upgrade_cost"]
        
        if user_coins < upgrade_cost:
            return False, f"موجودی ناکافی! نیاز: {upgrade_cost} ZP"
        
        # کسر هزینه و ارتقا
        db.update_user_coin(user_id, -upgrade_cost)
        db.update_miner_level(user_id, current_level + 1)
        
        return True, f"ماینر به سطح {current_level + 1} ارتقا یافت!"
