import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os


class StudyBattlesGUI:
     def __init__(self, root, app_controller):
        self.root = root
        self.app = app_controller  ## app_controller is the main app instance that has access to the timer
        self.setup_window()
        self.create_widgets()

    ## Effects: Configures the main window
     def setup_window(self):
        self.root.title("StudyBattles")
        self.root.geometry("600x750")    ## go for 600x900
        self.root.configure(bg="#1a6d74")
        self.root.resizable(True, True)
    
    ## Effects: Creates all GUI widgets
     def create_widgets(self):
        self.create_title()
        self.create_timer_display()
        self.create_duration_selection()
        self.create_control_buttons()
        self.create_characters_section()
        self.create_status_display()

     def create_title(self):
        self.load_ui_image("assets/title.png", pady=20)
    
     def create_timer_display(self):
        timer_frame = tk.Frame(self.root, bg="#1a6d74")
        timer_frame.pack(pady=10)

        self.timer_bg = self.load_ui_image("assets/timer_bg.png", parent=timer_frame)

        # Create frame for digit images
        self.digits_frame = tk.Frame(timer_frame, bg="#1a6d74")
        self.digits_frame.pack(pady=10)

        # Initialize digit labels for MM:SS format (5 characters)
        self.digit_labels = []
        for i in range(5):
            label = tk.Label(self.digits_frame, bg="#1a6d74")
            label.pack(side=tk.LEFT, padx=2)
            self.digit_labels.append(label)

        # Load initial timer display (25:00)
        self.update_timer_display(25 * 60)
    
     def create_duration_selection(self):
        duration_frame = tk.Frame(self.root, bg="#1a6d74")
        duration_frame.pack(pady=10)

        self.load_ui_image("assets/duration_selection.png", parent=duration_frame)

        # Could be replaced with clickable image buttons
        self.duration_var = tk.StringVar(value="25")
        duration_combo = ttk.Combobox(
            duration_frame,
            textvariable=self.duration_var,
            values=["25", "45", "60"],
            state="readonly",
            width=5,
            font=("Courier", 10)
        )
        duration_combo.pack(pady=5)
        duration_combo.bind("<<ComboboxSelected>>", self.app.on_duration_change)


     def create_control_buttons(self):
        button_frame = tk.Frame(self.root, bg="#1a6d74")
        button_frame.pack(pady=20)

          # Track button state
        self.button_state = "start"  # "start" or "stop"

        self.start_button_image = self.load_button_image("assets/start_button.png", button_frame, self.app.toggle_timer)
        self.reset_button_image = self.load_button_image("assets/reset_button.png", button_frame, self.app.reset_timer)

    
     def create_characters_section(self):
        characters_frame = tk.Frame(self.root, bg="#1a6d74")
        characters_frame.pack(pady=30, fill=tk.X)

        # Create user character section
        user_frame = tk.Frame(characters_frame, bg="#1a6d74")
        user_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)
        self.create_character_display(user_frame, "assets/user_character.png", True, "#eadbb3", "LEVEL 1")

        # Create enemy character section
        enemy_frame = tk.Frame(characters_frame, bg="#1a6d74")
        enemy_frame.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=20)
        self.create_character_display(enemy_frame, "assets/enemy_character.png", False, "#b13930", "ENEMY")

     def create_character_display(self, parent_frame, image_path, is_user, level_bg_color, level_text):
        # Load and display character image
        self.load_character_image(parent_frame, image_path, is_user)

        # Character level label
        level_frame = tk.Frame(parent_frame, bg=level_bg_color, relief="solid", bd=2)
        level_frame.pack(pady=5)

        level_label = tk.Label(
            level_frame,
            text=level_text,
            font=("Courier", 10, "bold"),
            fg="#111c24",
            bg=level_bg_color,
            padx=10,
            pady=2
        )
        level_label.pack()

        # XP bar
        xp_frame = tk.Frame(parent_frame, bg="#111c24", relief="solid", bd=2, height=20)
        xp_frame.pack(fill=tk.X, pady=5)
        xp_frame.pack_propagate(False)

        xp_bar_color = "#eadbb3" if is_user else "#b13930"
        xp_bar = tk.Frame(xp_frame, bg=xp_bar_color, height=16)
        xp_bar.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)

        # XP label
        xp_label = tk.Label(
            parent_frame,
            text="0/30 XP",
            font=("Courier", 8),
            fg="#eadbb3",
            bg="#1a6d74"
        )
        xp_label.pack()

        # Store references for updating
        if is_user:
            self.user_level_label = level_label
            self.user_xp_frame = xp_frame
            self.user_xp_bar = xp_bar
            self.user_xp_label = xp_label
        else:
            self.enemy_level_label = level_label
            self.enemy_xp_frame = xp_frame
            self.enemy_xp_bar = xp_bar
            self.enemy_xp_label = xp_label

     def create_status_display(self):
        self.status_label = tk.Label(
            self.root,
            text="Ready to focus! Select duration and press START.",
            font=("Courier", 10),
            fg="#eadbb3",   ## yellow
            bg="#1a6d74",   ## blue
            wraplength=500
        )
        self.status_label.pack(pady=20)

    
     def load_character_image(self, parent, image_path, is_user):
        character_frame = tk.Frame(parent, bg="#1a6d74", width=120, height=120)
        character_frame.pack(pady=10)
        character_frame.pack_propagate(False)

        try:
            png_path = image_path.replace('.svg', '.png')
            if os.path.exists(png_path):
                image = Image.open(png_path)
                # Resize to fit the frame while maintaining aspect ratio
                image = image.resize((120, 120), Image.NEAREST)               ### CHANGE SIZE
                photo = ImageTk.PhotoImage(image)

                label = tk.Label(character_frame, image=photo, bg="#1a6d74")
                label.image = photo  # Keep a reference to prevent garbage collection
                label.pack(expand=True)
            else:
                # Fallback: simple black box
                 self.create_black_box(character_frame)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Fallback to black box on any error
            self.create_black_box(character_frame)

     def create_black_box(self, parent, wdth = 120, hght = 120):
        black_box = tk.Frame(parent, bg="#000000", width=wdth, height=hght, relief="solid", bd=2)
        black_box.pack(expand=True)
        black_box.pack_propagate(False)

    
    ## Effects: Load a UI element image with fallback to black box
     def load_ui_image(self, image_path, parent=None, pady=0, padx=0):
        if parent is None:
            parent = self.root

        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)

                label = tk.Label(parent, image=photo, bg="#1a6d74")
                label.image = photo  
                label.pack(pady=pady, padx=padx)
                return label
            else:
                placeholder = tk.Frame(parent, bg="#000000", width=200, height=60, relief="solid", bd=2)
                placeholder.pack(pady=pady, padx=padx)
                placeholder.pack_propagate(False)
                return placeholder
        except Exception as e:
            print(f"Error loading UI image {image_path}: {e}")
            placeholder = tk.Frame(parent, bg="#000000", width=200, height=60, relief="solid", bd=2)
            placeholder.pack(pady=pady, padx=padx)
            placeholder.pack_propagate(False)
            return placeholder
        

     def load_button_image(self, image_path, parent, command):
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)

                button = tk.Button(parent, image=photo, bg="#1a6d74", bd=0, command=command)
                button.image = photo 
                button.pack(side=tk.LEFT, padx=10)
                return button
            else:
                # Fallback to regular button
                button = tk.Button(
                    parent,
                    text="BUTTON",
                    font=("Courier", 12, "bold"),
                    fg="#eadbb3",
                    bg="#8b4513",
                    command=command
                )
                button.pack(side=tk.LEFT, padx=10)
                return button
        except Exception as e:
            print(f"Error loading button image {image_path}: {e}")
            button = tk.Button(
                parent,
                text="BUTTON", 
                font=("Courier", 12, "bold"),
                fg="#f4e6a1",
                bg="#8b4513",
                command=command
            )
            button.pack(side=tk.LEFT, padx=10)
            return button

     def update_timer_display(self, remaining_time):
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"

        for i, char in enumerate(time_string):
            if i < len(self.digit_labels):
                if char == ':':
                    image_path = "assets/digits/colon.png"
                else:
                    image_path = f"assets/digits/{char}.png"

                self.load_digit_image(self.digit_labels[i], image_path, char)

    
     def load_digit_image(self, label, image_path, fallback_char):
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((40, 60), Image.NEAREST)  # Adjust size as needed
                photo = ImageTk.PhotoImage(image)

                label.config(image=photo, text="")
                label.image = photo  
            else:
                # Fallback to text
                label.config(
                    image="",
                    text=fallback_char,
                    font=("Courier", 36, "bold"),
                    fg="#f4e6a1",
                    bg="#2d5a5a"
                )
        except Exception as e:
            print(f"Error loading digit image {image_path}: {e}")
            # Fallback to text in case of error
            label.config(
                image="",
                text=fallback_char,
                font=("Courier", 36, "bold"),
                fg="#f4e6a1",
                bg="#2d5a5a"
            )

     ## Effects: Updates all display elements
     def update_display(self, user_stats, enemy_stats):
        # Update user stats
        self.user_level_label.config(text=f"LEVEL {user_stats['level']}")
        self.user_xp_label.config(text=f"{user_stats['current_level_xp']}/{user_stats['xp_needed_for_next']} XP")

        # Update user XP bar
        if user_stats['xp_needed_for_next'] > 0:
            user_xp_percentage = user_stats['current_level_xp'] / user_stats['xp_needed_for_next']
            bar_width = int(200 * user_xp_percentage)  # 200 is approximate frame width
            self.user_xp_bar.config(width=max(1, bar_width))

        # Update enemy stats
        self.enemy_level_label.config(text=f"LEVEL {enemy_stats['level']}")
        self.enemy_xp_label.config(text=f"{enemy_stats['current_level_xp']}/{enemy_stats['xp_needed_for_next']} XP")

        # Update enemy XP bar
        if enemy_stats['xp_needed_for_next'] > 0:
            enemy_xp_percentage = enemy_stats['current_level_xp'] / enemy_stats['xp_needed_for_next']
            bar_width = int(200 * enemy_xp_percentage)
            self.enemy_xp_bar.config(width=max(1, bar_width))

    ## Results: Update status message
     def set_status(self, message):
        self.status_label.config(text=message)

    ## Results: Update start button to show appropriate image (start or stop)
     def set_start_button(self, text, color):
        try:
            if text == "START":
                new_state = "start"
                image_path = "assets/start_button.png"
            else:  
                new_state = "stop"
                image_path = "assets/stop_button.png"
                
            # Only update if state actually changed
            if hasattr(self, 'button_state') and self.button_state != new_state:
                self.button_state = new_state
                self.update_button_image(image_path)
        except Exception as e:
            print(f"Error updating button image: {e}")
            # Fallback to regular button behavior if images fail
            try:
                if hasattr(self, 'start_button_image') and hasattr(self.start_button_image, 'config'):
                    self.start_button_image.config(text=text, bg=color)
            except:
                pass

     def get_duration(self):
        return int(self.duration_var.get())

     def show_level_up(self, level):
        messagebox.showinfo(
            "Level Up!",
            f"Congratulations! You reached Level {level}!"
        )

    ## Results: Update the start button with a new image
     def update_button_image(self, image_path):
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                
                self.start_button_image.config(image=photo)
                self.start_button_image.image = photo  
            else:
                print(f"Button image not found: {image_path}")
        except Exception as e:
            print(f"Error loading button image {image_path}: {e}")

     def ask_quit_confirmation(self):
        return messagebox.askokcancel(
            "Quit", 
            "Timer is running! Quitting will give XP to the enemy. Are you sure?"
        )