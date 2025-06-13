import math

class XPSystem:
    def __init__(self):
        self.user_xp = 0
        self.enemy_xp = 0
        self.user_level = 1
        self.enemy_level = 1

    ## Effects: Calculate total XP needed to reach a specific level with 
    ## formula: XP needed = (level - 1) * 30
    def get_xp_for_level(self, level):
        if level <= 1:
            return 0
        return (level - 1) * 30
    
    def get_xp_for_next_level(self, current_level):
        return self.get_xp_for_level(current_level + 1) - self.get_xp_for_level(current_level)
    
    ## Effects: Calculate level based on total xp
    def calculate_level(self, total_xp):
        if total_xp < 0:
            return 1
        # Level = floor(total_xp / 30) + 1
        return min(99, math.floor(total_xp / 30) + 1)  # Cap at level 99
    
    ## Effects: Add user xp and return True if user has leveled up
    def add_user_xp(self, amount):
        if amount <= 0:
            return
        
        old_level = self.user_level
        self.user_xp += amount
        self.user_level = self.calculate_level(self.user_xp)
        
        return self.user_level > old_level  
    
    ## Effects: Add enemy xp and return True if enemy has leveled up
    def add_enemy_xp(self, amount):
        if amount <= 0:
            return
        
        old_level = self.enemy_level
        self.enemy_xp += amount
        self.enemy_level = self.calculate_level(self.enemy_xp)
        
        return self.enemy_level > old_level  
    
    ## Effects: Get user stats dictionary
    def get_user_stats(self):
        current_level_xp = self.get_xp_for_level(self.user_level)
        next_level_xp = self.get_xp_for_level(self.user_level + 1)
        xp_in_current_level = self.user_xp - current_level_xp
        xp_needed_for_next = next_level_xp - current_level_xp
        
        return {
            'level': self.user_level,
            'total_xp': self.user_xp,
            'current_level_xp': xp_in_current_level,
            'xp_needed_for_next': xp_needed_for_next,
            'progress_percentage': (xp_in_current_level / xp_needed_for_next) * 100 if xp_needed_for_next > 0 else 100
        }
    
    ## Effects: Get enemy stats dictionary
    def get_enemy_stats(self):
        current_level_xp = self.get_xp_for_level(self.enemy_level)
        next_level_xp = self.get_xp_for_level(self.enemy_level + 1)
        xp_in_current_level = self.enemy_xp - current_level_xp
        xp_needed_for_next = next_level_xp - current_level_xp
        
        return {
            'level': self.enemy_level,
            'total_xp': self.enemy_xp,
            'current_level_xp': xp_in_current_level,
            'xp_needed_for_next': xp_needed_for_next,
            'progress_percentage': (xp_in_current_level / xp_needed_for_next) * 100 if xp_needed_for_next > 0 else 100
        }

    ## Effects: Get data to save to file
    def get_save_data(self):
        return {
            'user_xp': self.user_xp,
            'enemy_xp': self.enemy_xp,
            'user_level': self.user_level,
            'enemy_level': self.enemy_level
        }
    
    ## Effects: Load data from save file
    def load_data(self, data):
        try:
            self.user_xp = data.get('user_xp', 0)
            self.enemy_xp = data.get('enemy_xp', 0)
            
            # Recalculate levels based on XP to ensure consistency
            self.user_level = self.calculate_level(self.user_xp)
            self.enemy_level = self.calculate_level(self.enemy_xp)
            
        except Exception as e:
            print(f"Error loading XP data: {e}")
            # Reset to defaults if loading fails
            self.user_xp = 0
            self.enemy_xp = 0
            self.user_level = 1
            self.enemy_level = 1

    def reset_progress(self):
        self.user_xp = 0
        self.enemy_xp = 0
        self.user_level = 1
        self.enemy_level = 1