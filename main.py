import tkinter as tk
import json
import os
from timer import FocusTimer
from xp_system import XPSystem
from gui import StudyBattlesGUI

class StudyBattlesApp:
    def __init__(self):
        self.root = tk.Tk()

        # Initialize systems
        self.timer = FocusTimer(self.on_timer_complete, self.on_timer_tick)
        self.xp_system = XPSystem()

        # Load saved data
        self.load_data()

        # Create GUI
        self.gui = StudyBattlesGUI(self.root, self)

        # Update display
        self.update_display()

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_duration_change(self, event=None):
        if not self.timer.is_running:
            duration = self.gui.get_duration()
            self.timer.set_duration(duration)
            self.gui.update_timer_display(self.timer.remaining_time)

    def toggle_timer(self):
        if self.timer.is_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        duration = self.gui.get_duration()
        self.timer.start(duration)
        self.gui.set_start_button("STOP", "#cd5c5c")
        self.gui.set_status("Focus session in progress... Stay strong!")

    ## Effects: Stop the timer because user quit early
    def stop_timer(self):
        if self.timer.is_running:
            self.timer.stop()
            self.gui.set_start_button("START", "#f4e6a1")

            # Penalty for quitting early
            remaining_minutes = self.timer.remaining_time // 60
            penalty_xp = max(5, remaining_minutes // 5)  # Minimum 5 XP penalty

            self.xp_system.add_enemy_xp(penalty_xp)
            self.gui.set_status(f"Session stopped early! Enemy gained {penalty_xp} XP. Try again!")
            self.update_display()
            self.save_data()

    def reset_timer(self):
        self.timer.reset()
        self.gui.set_start_button("START", "#f4e6a1")
        self.gui.update_timer_display(self.timer.remaining_time)
        self.gui.set_status("Timer reset. Ready to start a new session!")

    ## Effects: Called when timer completes successfully, applies xp to user
    def on_timer_complete(self):
        self.gui.set_start_button("START", "#f4e6a1")

        # Reward for completing session
        duration = self.gui.get_duration()
        reward_xp = duration  # 1 XP per minute

        self.xp_system.add_user_xp(reward_xp)

        # Check for level up
        if self.xp_system.user_level > self.previous_user_level:
            self.gui.show_level_up(self.xp_system.user_level)

        self.gui.set_status(f"Session completed! You gained {reward_xp} XP. Well done!")
        self.update_display()
        self.save_data()
        self.previous_user_level = self.xp_system.user_level

    def on_timer_tick(self):
        self.gui.update_timer_display(self.timer.remaining_time)

    def update_display(self):
        user_stats = self.xp_system.get_user_stats()
        enemy_stats = self.xp_system.get_enemy_stats()
        self.gui.update_display(user_stats, enemy_stats)

    def load_data(self):
        try:
            if os.path.exists("data/save_data.json"):
                with open("data/save_data.json", "r") as f:
                    data = json.load(f)
                    self.xp_system.load_data(data)
            self.previous_user_level = self.xp_system.user_level
        except Exception as e:
            print(f"Error loading data: {e}")
            self.previous_user_level = 1

    def save_data(self):
        try:
            os.makedirs("data", exist_ok=True)
            data = self.xp_system.get_save_data()
            with open("data/save_data.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    ## Effects: Handle application closing
    def on_closing(self):
        if self.timer.is_running:
            if self.gui.ask_quit_confirmation():
                self.stop_timer()
                self.root.destroy()
        else:
            self.save_data()
            self.root.destroy()

    ## Effects: Starts the application
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StudyBattlesApp()
    app.run()