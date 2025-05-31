import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from timer import FocusTimer

class PixelFocusApp:
    def __init__(self, root):
        self.root = root
        self.timer = FocusTimer(25 * 60)  # 25 min default
        self.timer_running = False

        self.user_xp = 0
        self.enemy_xp = 0

        self.setup_ui()

    def setup_ui(self):
        self.root.title("PixelFocus")
        self.root.geometry("600x720")
        self.root.resizable(False, False)

        self.user_img = ImageTk.PhotoImage(file="assets/user.png")
        self.enemy_img = ImageTk.PhotoImage(file="assets/enemy.png")

        tk.Label(self.root, text="You").pack()
        tk.Label(self.root, image=self.user_img).pack()

        self.timer_label = tk.Label(self.root, text="00:00", font=("Courier", 36))
        self.timer_label.pack(pady=10)

        tk.Button(self.root, text="Start Focus Session", command=self.start_session).pack(pady=5)
        tk.Button(self.root, text="End Session", command=self.end_session_early).pack(pady=5)

        tk.Label(self.root, text="Enemy").pack()
        tk.Label(self.root, image=self.enemy_img).pack()

        self.xp_label = tk.Label(self.root, text="Your XP: 0 | Enemy XP: 0", font=("Arial", 12))
        self.xp_label.pack(pady=10)

    def start_session(self):
        if self.timer_running:
            return
        self.timer.start()
        self.timer_running = True
        self.update_ui()

    def update_ui(self):
        if not self.timer_running:
            return
        remaining = self.timer.time_remaining()
        self.timer_label.config(text=self.format_time(remaining))
        if self.timer.is_finished():
            self.complete_session()
        else:
            self.root.after(1000, self.update_ui)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02}:{s:02}"

    def complete_session(self):
        self.timer_running = False
        self.user_xp += 10
        messagebox.showinfo("Focus Complete", f"🎉 You earned 10 XP!\nTotal XP: {self.user_xp}")
        self.update_xp_label()

    def end_session_early(self):
        if not self.timer_running:
            return
        confirm = messagebox.askyesno("Quit Early", "End the session early?")
        if confirm:
            self.timer_running = False
            self.enemy_xp += 5
            messagebox.showwarning("Session Failed", f"💀 Enemy gains 5 XP!\nEnemy XP: {self.enemy_xp}")
            self.update_xp_label()

    def update_xp_label(self):
        self.xp_label.config(text=f"Your XP: {self.user_xp} | Enemy XP: {self.enemy_xp}")
