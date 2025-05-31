import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading



user_xp = 0
enemy_xp = 0

FOCUS_DURATION = 1 * 60  # 25 minutes

timer_running = False
timer_thread = None
start_time = None

def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02}:{secs:02}"

def update_timer_ui():
    if not timer_running:
        return
    elapsed = int(time.time() - start_time)
    remaining = FOCUS_DURATION - elapsed
    if remaining <= 0:
        end_session(success=True)
    else:
        timer_label.config(text=format_time(remaining))
        root.after(1000, update_timer_ui)

def start_timer():
    global timer_running, start_time
    if timer_running:
        return
    timer_running = True
    start_time = time.time()
    timer_label.config(text=format_time(FOCUS_DURATION))
    update_timer_ui()

def stop_timer():
    global timer_running
    if not timer_running:
        return
    confirm = messagebox.askyesno("End Session", "End session early?")
    if confirm:
        end_session(success=False)

def end_session(success):
    global timer_running, user_xp, enemy_xp
    timer_running = False
    if success:
        user_xp += 10
        messagebox.showinfo("Session Complete", f"Focus session complete! +10 XP\nTotal XP: {user_xp}")
    else:
        enemy_xp += 5
        messagebox.showwarning("Session Failed", f"You quit early! Enemy gains XP.\nEnemy XP: {enemy_xp}")
    xp_label.config(text=f"Your XP: {user_xp} | Enemy XP: {enemy_xp}")
    timer_label.config(text="00:00")


## UI

root = tk.Tk()
root.title("StudyBuddies")
root.geometry("400x400")
root.resizable(False, False)

user_img = Image.open("assets/user.png").resize((64, 64))
enemy_img = Image.open("assets/enemy.png").resize((64, 64))
user_photo = ImageTk.PhotoImage(user_img)
enemy_photo = ImageTk.PhotoImage(enemy_img)

tk.Label(root, text="You").pack()
tk.Label(root, image=user_photo).pack()

timer_label = tk.Label(root, text="00:00", font=("Courier", 36))
timer_label.pack(pady=10)

tk.Button(root, text="Start Focus Session", command=start_timer).pack(pady=5)
tk.Button(root, text="End Session", command=stop_timer).pack(pady=5)

tk.Label(root, text="Enemy").pack()
tk.Label(root, image=enemy_photo).pack()

xp_label = tk.Label(root, text="Your XP: 0 | Enemy XP: 0", font=("Arial", 12))
xp_label.pack(pady=10)

root.mainloop()