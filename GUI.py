import sys, os
import platform
import json
import customtkinter as ctk
from tkinter import colorchooser
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import datetime
import webbrowser
import functions as fn
from PIL import Image, ImageTk  

# Importing Dictonaries
from directories import WindowsFonts, ThemeOptions


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Desktop TDL App")
        self.geometry("650x500")
        self.resizable(False, False)  # prevent user from manually resizing
        self.iconbitmap("assets/checklist.ico")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ### Default settings
        
        self.default_settings = {
            "Apperance Mode": "Light",
            "Theme" : "Blue",
            "UI Scaling" : "100%",
            "position": "Top Right",
            "font": "Comic",
            "font size": None,
            "textbox_fontsize" : 14,
            "text_color": "white",
            "box_color": "black",
            "text_padding": "30",
            "frame_padding": "80",
            "desktop_wallpaper": fn.get_wallpaper_path()
        }

        img = Image.open(self.default_settings["desktop_wallpaper"])
        img_w, img_h = img.size
        self.default_settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

        data_folder = "./data"
        os.makedirs(data_folder, exist_ok=True) # Ensure folder exists

        self.settings_file = f"{data_folder}/settings.json"
        self.history_file = f"{data_folder}/history.txt"

        # Create files if missing
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, "w") as f:
                json.dump({}, f) 
        self.settings = self.load_settings()

        if not os.path.exists(self.history_file):
            open(self.history_file, "w").close()  

        img = Image.open(self.settings["desktop_wallpaper"])
        img_w, img_h = img.size
        self.settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

        ctk.set_default_color_theme(ThemeOptions[self.settings["Theme"]]) 
        ctk.set_appearance_mode(self.settings["Apperance Mode"])
        ctk.set_widget_scaling(int(self.settings["UI Scaling"].replace("%", "")) / 100)

        # --------------------------------------------------
        #     Side Bar
        # --------------------------------------------------
        
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=120, corner_radius=0, border_width=0, fg_color="transparent")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Desktop TDL", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # To Do List button
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame,text="To Do List", command=self.ToDoListsPage)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # Setting Button
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame,text="Settings", command=self.SettingsPage)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # History Button
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame,text="History", command=self.HistoryPage)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # History Button
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame,text="Console", command=self.ConsolePage)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_version= ctk.CTkLabel(self.sidebar_frame,text="version 1.0.3")
        self.sidebar_version.grid(row=6, column=0, padx=20, pady=10)

        # --------------------------------------------------
        #       Main Frame
        # --------------------------------------------------

        # create the main frame for To Do List
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color="transparent")
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Today Label
        today = (lambda d: f"{d.strftime('%B')} {d.day}{('th' if 11<=d.day<=13 else {1:'st',2:'nd',3:'rd'}.get(d.day%10,'th'))}, {d.year}")(datetime.date.today())
        self.date_label = ctk.CTkLabel(self.main_frame, text=today,font=ctk.CTkFont(size=20, weight="bold"))
        self.date_label.grid(row=0, column=0, padx=(10, 10), pady=(20, 10), sticky="w")

        # Text label
        self.text_label = ctk.CTkLabel(self.main_frame, text="Write your TDL below:")
        self.text_label.grid(row=1, column=0, padx=(10, 10), pady=(0, 0), sticky="w")

        # Clear Button
        self.reset_button = ctk.CTkButton(self.main_frame,text="Clear", command=self.Clear)
        self.reset_button.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="e")

        # Text box
        textbox_fontsize = 14 # This is a variable
        self.textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=textbox_fontsize))
        self.textbox.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky="nsew")
        with open(self.history_file, "r", encoding="utf-8") as f:
            self.textbox.insert('0.0',"\n".join(f.read().split("\n\n")[0].split("\n")[1:]))

        # Rest Button
        self.reset_button = ctk.CTkButton(self.main_frame,text="Reset Desktop Wallpaper", command=self.Reset)
        self.reset_button.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        # Save Button
        self.save_button = ctk.CTkButton(self.main_frame,text="Write On Desktop", command=self.Save)
        self.save_button.grid(row=3, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")

        # --------------------------------------------------
        #       Setting Frame
        # --------------------------------------------------

        # create the settings frame
        self.settings_frame = ctk.CTkScrollableFrame(self, corner_radius=0, border_width=0, fg_color="transparent", orientation="vertical")
        self.settings_frame.grid_rowconfigure(0, weight=0)

        # Label
        self.settings_label = ctk.CTkLabel(self.settings_frame, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.settings_label.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20,10), sticky="w")

        padx_left_labels = 80
        padx_right_optiosn = 20

        ### Apperance Mode Settings
        n_row = 1
        self.appearance_mode_label = ctk.CTkLabel(self.settings_frame, text="Appearance Mode", anchor="w")
        self.appearance_mode_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.appearance_mode_optionemenu.set(self.settings["Apperance Mode"])

        ### UI Scaling
        n_row += 1
        self.ui_scaling_label = ctk.CTkLabel(self.settings_frame, text="UI Scaling", anchor="w")
        self.ui_scaling_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.scaling_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=["80%", "85%" ,"90%", "95%" , "100%", "105%" , "110%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.scaling_optionemenu.set(self.settings["UI Scaling"])

        ### Theme settings
        n_row += 1
        self.theme_label = ctk.CTkLabel(self.settings_frame, text="Theme", anchor="w")
        self.theme_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.theme_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=list(ThemeOptions.keys()),command=self.change_theme_event)
        self.theme_optionemenu.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.theme_optionemenu.set(self.settings["Theme"]) 

        ### Font
        n_row += 1
        self.font_label = ctk.CTkLabel(self.settings_frame, text="Font")
        self.font_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        font_options = ["Arial", "Arial2", "Arials"]
        self.font_opt = ctk.CTkOptionMenu(self.settings_frame, values=list(WindowsFonts.keys()))
        self.font_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")
        
        self.font_opt.set(self.settings["font"])

        ### Font Size
        n_row += 1
        self.font_size_label = ctk.CTkLabel(self.settings_frame, text="Font Size")
        self.font_size_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.font_size_opt = ctk.CTkEntry(self.settings_frame)
        self.font_size_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.font_size_opt.insert('end',self.settings["font size"])

        ### App Textbox Font Size
        n_row += 1
        self.textbox_font_size_label = ctk.CTkLabel(self.settings_frame, text="App Textbox Font Size")
        self.textbox_font_size_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.textbox_font_size_opt = ctk.CTkEntry(self.settings_frame)
        self.textbox_font_size_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.textbox_font_size_opt.insert('end', self.settings["textbox_fontsize"])
        self.textbox.configure(font=ctk.CTkFont(size=self.settings["textbox_fontsize"]))

        ### Position 
        n_row += 1
        self.position_label = ctk.CTkLabel(self.settings_frame, text="Position")
        self.position_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        position_options = ["Top Right", "Top Left", "Bottom Right", "Bottom Left", "Center"]
        self.position_opt = ctk.CTkOptionMenu(self.settings_frame, values=position_options)
        self.position_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.position_opt.set(self.settings["position"])

        ### Text Color
        n_row += 1
        self.text_color_label = ctk.CTkLabel(self.settings_frame, text="Text Color")
        self.text_color_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.text_color_label_box = ctk.CTkLabel(self.settings_frame, text="⬤")
        self.text_color_label_box.grid(row=n_row, column=0, padx=(75, 0), pady=10, sticky="w")

        self.text_color_opt = ctk.CTkButton(self.settings_frame, text="Choose Color", command=self.choose_text_color)
        self.text_color_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        global text_color
        text_color = self.settings["text_color"]
        self.text_color_label_box.configure(text_color=text_color)
        
        ### Box Color
        n_row += 1
        self.box_color_label = ctk.CTkLabel(self.settings_frame, text="Box Color")
        self.box_color_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.box_color_label_box = ctk.CTkLabel(self.settings_frame, text="⬤")
        self.box_color_label_box.grid(row=n_row, column=0, padx=(75, 0), pady=10, sticky="w")

        self.box_color_opt = ctk.CTkButton(self.settings_frame, text="Choose Color", command=self.choose_box_color)
        self.box_color_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        global box_color
        box_color = self.settings["box_color"]
        self.box_color_label_box.configure(text_color=box_color)

        ### Frame Padding
        n_row += 1
        self.frame_padding_label = ctk.CTkLabel(self.settings_frame, text="Text-Box Padding")
        self.frame_padding_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.frame_padding_opt = ctk.CTkEntry(self.settings_frame)
        self.frame_padding_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.frame_padding_opt.insert('end', self.settings["text_padding"])

        ### Text Padding
        n_row += 1
        self.text_padding_label = ctk.CTkLabel(self.settings_frame, text="Box-Frame Padding")
        self.text_padding_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.text_padding_opt = ctk.CTkEntry(self.settings_frame)
        self.text_padding_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.text_padding_opt.insert('end', self.settings["frame_padding"])

        ### Desktop Wallpaper Path
        n_row += 1
        self.desktop_wallpaper_dir_label = ctk.CTkLabel(self.settings_frame, text="Desktop Wallpaper Path:")
        self.desktop_wallpaper_dir_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.desktop_wallpaper_dir_button = ctk.CTkButton(self.settings_frame, text="Change Wallpaper", command=self.ChangeWallpaper)
        self.desktop_wallpaper_dir_button.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        self.desktop_wallpaper_dir_opt = ctk.CTkEntry(self.settings_frame)
        self.desktop_wallpaper_dir_opt.grid(row=n_row+1, column=0, columnspan =2, padx=(10,10), pady=(0,10), sticky="ew")

        self.desktop_wallpaper_dir_opt.insert('end', self.settings["desktop_wallpaper"])

        # ### History File Directory
        # n_row += 2
        # self.histroy_file_dir_label = ctk.CTkLabel(self.settings_frame, text="History File Directory:")
        # self.histroy_file_dir_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        # self.histroy_file_dir_button = ctk.CTkButton(self.settings_frame, text="Browse", command=self.HistoryFileDirectory)
        # self.histroy_file_dir_button.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="w")

        # self.histroy_file_dir_opt = ctk.CTkEntry(self.settings_frame)
        # self.histroy_file_dir_opt.grid(row=n_row+1, column=0, columnspan =2, padx=(10,10), pady=(0,10), sticky="ew")

        # self.histroy_file_dir_opt.insert('end', f'{os.getcwd()}\history.txt')

        # --------------------------------------------------
        #       History Frame
        # --------------------------------------------------

        # create the history frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color="transparent")
        self.history_frame.grid_rowconfigure(1, weight=0)
        self.history_frame.grid_rowconfigure(2, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # Label
        self.history_label = ctk.CTkLabel(self.history_frame, text="History", font=ctk.CTkFont(size=20, weight="bold"))
        self.history_label.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20,10), sticky="w")

        # Label
        self.history_label = ctk.CTkLabel(self.history_frame, text=f"History file size: {fn.FileSize(self.history_file)}")
        self.history_label.grid(row=1, column=0, padx=(10, 10), pady=(0, 0), sticky="w")

        # Text box
        textbox_fontsize = 14 # This is a variable
        self.history_textbox = ctk.CTkTextbox(self.history_frame, font=ctk.CTkFont(size=textbox_fontsize))
        self.history_textbox.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky="nsew")
        with open(self.history_file, "r", encoding="utf-8") as f:
            for line in f:
                self.history_textbox.insert('end', line)
        self.history_textbox.configure(state="disabled") # Make it read-only for user input

        # Rest Button
        self.history_reset_button = ctk.CTkButton(self.history_frame,text="Delete History" ,command=self.DeleteHistory)
        self.history_reset_button.grid(row=3, column=0, columnspan=2, padx=(10, 10), pady=(0, 10), sticky="ew")

        # --------------------------------------------------
        #       Console Frame
        # --------------------------------------------------

        # create the console frame
        self.console_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color="transparent")
        self.console_frame.grid_rowconfigure(2, weight=1)
        self.console_frame.grid_columnconfigure(0, weight=1)

        # Label
        self.console_label = ctk.CTkLabel(self.console_frame, text="Console", font=ctk.CTkFont(size=20, weight="bold"))
        self.console_label.grid(row=0, column=0, padx=(10, 10), pady=(20,10), sticky="w")

        # Text box
        self.console_textbox = ctk.CTkTextbox(self.console_frame, font=ctk.CTkFont(size=12))
        self.console_textbox.grid(row=2, column=0, columnspan=2, pady=(0, 5), padx=(10, 10), sticky="nsew")

        ## Uploading Information to the Console
        self.console_textbox.insert('0.0', f"● Operating System:\n  --->  {platform.system()}\n\n")
        self.console_textbox.insert('end', f"● Desktop Wallpaper Location:\n  --->  {self.desktop_wallpaper_dir_opt.get()}\n\n")
        self.console_textbox.insert('end', f"● Desktop Wallpaper Image Size (using Pillow):\n  ---> {img_w}(w) * {img_h}(h)\n\n")
        self.console_textbox.insert('end', f"● Suggested Text Font Size for TDL:\n  ---> {int((img_w + img_h)/2 * 0.03/1.333)}\n\n")
        self.console_textbox.insert('end', f"● Existing Fonts For Chinese Language Support:\n  ---> Simfang, Simhei, Simkai\n\n")
        self.console_textbox.configure(state="disabled") # Make it read-only for user input

        # Messages
        self.rights = ctk.CTkLabel(self.console_frame, text="© 2025 Desktop TDL. All rights reserved.", font=ctk.CTkFont(size=12, weight="bold"))
        self.rights.grid(row=3, column=0, padx=(10, 10), pady=0, sticky="w")

        self.messages = ctk.CTkLabel(self.console_frame, text="Visit us at:  ammelsayed.github.io\\projects\DesktopTDL", font=ctk.CTkFont(size=12))
        self.messages.grid(row=4, column=0, padx=(10, 10), pady=(0,10), sticky="w")

        # Bind left mouse click to open the URL
        self.messages.bind("<Button-1>", lambda event: webbrowser.open("https://ammelsayed.github.io/projects/DesktopTDL/"))
        self.messages.bind("<Enter>", lambda event: self.messages.configure(cursor="hand2"))
        self.messages.bind("<Leave>", lambda event: self.messages.configure(cursor=""))


        # --------------------------------------------------
        #       Starting The APP
        # --------------------------------------------------

        # Initially show the To Do List frame
        self.show_frame(self.main_frame)


    ### Frame Settings
    def show_frame(self, frame):
        self.main_frame.grid_remove()
        self.settings_frame.grid_remove()
        self.history_frame.grid_remove()
        self.console_frame.grid_remove()
        frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def ToDoListsPage(self):
        self.show_frame(self.main_frame)

    def SettingsPage(self):
        self.show_frame(self.settings_frame)
    
    def HistoryPage(self):
        self.show_frame(self.history_frame)
    
    def ConsolePage(self):
        self.show_frame(self.console_frame)
    
    ### Read Settings
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                # Validate settings
                for key, value in self.default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
            except (json.JSONDecodeError, IOError) as e:
                messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
                return self.default_settings
        return self.default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    ### Updating Settings

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.settings["Apperance Mode"] = new_appearance_mode
        self.save_settings()
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        self.settings["UI Scaling"] = new_scaling
        self.save_settings()
    
    def change_theme_event(self, new_theme: str):
        self.settings["Theme"] = new_theme
        ctk.set_default_color_theme(ThemeOptions[new_theme])
        self.save_settings()

        ## Old Method close and reopen

        ## New method: Auto-update the colors
        # self.update_widget_colors()
        # # App default themes
        # self.sidebar_frame.configure(corner_radius=0, border_width=0, fg_color="transparent")
        # self.main_frame.configure(corner_radius=0, border_width=0, fg_color="transparent")
        # self.settings_frame.configure(corner_radius=0, border_width=0, fg_color="transparent")
        # self.history_frame.configure(corner_radius=0, border_width=0, fg_color="transparent")
        # self.console_frame.configure(corner_radius=0, border_width=0, fg_color="transparent")

    # def update_widget_colors(self):
    #     # Pick correct color for light/dark mode if it's a list

    #     def pick_color(value):
    #         if isinstance(value, list) and len(value) == 2:
    #             return value[0] if ctk.get_appearance_mode() == "Light" else value[1]
    #         return value

    #     def update_widget_recursive(widget):

    #         if isinstance(widget, ctk.CTk):
    #             widget.configure(
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
    #             )
            
    #         if isinstance(widget, ctk.CTkToplevel):
    #             widget.configure(
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
    #             )

    #         # ---- CTkFrame ----
    #         if isinstance(widget, ctk.CTkFrame):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkFrame"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkFrame"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkFrame"]["border_color"]),
    #             )

    #         # ---- CTkButton ----
    #         elif isinstance(widget, ctk.CTkButton):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkButton"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkButton"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkButton"]["fg_color"]),
    #                 hover_color=pick_color(ctk.ThemeManager.theme["CTkButton"]["hover_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkButton"]["border_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkButton"]["text_color"]),
                     
    #             )
            
    #         # ---- CTkLabel ----
    #         elif isinstance(widget, ctk.CTkLabel):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkLabel"]["corner_radius"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkLabel"]["fg_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
    #             )

    #         # ---- CTkEntry ----
    #         elif isinstance(widget, ctk.CTkEntry):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkEntry"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkEntry"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkEntry"]["fg_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkEntry"]["border_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkEntry"]["text_color"]),
    #                 placeholder_text_color=pick_color(ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"]),
    #             )

    #         # ---- CTkCheckBox ----
    #         elif isinstance(widget, ctk.CTkCheckBox):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkCheckBox"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkCheckBox"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkCheckBox"]["border_color"]),
    #                 hover_color=pick_color(ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"]),
    #                 checkmark_color=pick_color(ctk.ThemeManager.theme["CTkCheckBox"]["checkmark_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkCheckBox"]["text_color"]),
    #             )

    #         # ---- CTkSwitch ----
    #         elif isinstance(widget, ctk.CTkSwitch):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkSwitch"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkSwitch"]["border_width"],
    #                 button_length=ctk.ThemeManager.theme["CTkSwitch"]["button_length"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkSwitch"]["fg_color"]),
    #                 progress_color=pick_color(ctk.ThemeManager.theme["CTkSwitch"]["progress_color"]),
    #                 button_color=pick_color(ctk.ThemeManager.theme["CTkSwitch"]["button_color"]),
    #                 button_hover_color=pick_color(ctk.ThemeManager.theme["CTkSwitch"]["button_hover_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkSwitch"]["text_color"]),
    #             )

    #         # ---- CTkRadioButton ----
    #         elif isinstance(widget, ctk.CTkRadioButton):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkRadioButton"]["corner_radius"],
    #                 border_width_checked=ctk.ThemeManager.theme["CTkRadioButton"]["border_width_checked"],
    #                 border_width_unchecked=ctk.ThemeManager.theme["CTkRadioButton"]["border_width_unchecked"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkRadioButton"]["fg_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkRadioButton"]["border_color"]),
    #                 hover_color=pick_color(ctk.ThemeManager.theme["CTkRadioButton"]["hover_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkRadioButton"]["text_color"]),
    #             )

    #         # ---- CTkProgressBar ----
    #         elif isinstance(widget, ctk.CTkProgressBar):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkProgressBar"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkProgressBar"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkProgressBar"]["fg_color"]),
    #                 progress_color=pick_color(ctk.ThemeManager.theme["CTkProgressBar"]["progress_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkProgressBar"]["border_color"]),
    #             )

    #         # ---- CTkSlider ----
    #         elif isinstance(widget, ctk.CTkSlider):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkSlider"]["corner_radius"],
    #                 button_corner_radius=ctk.ThemeManager.theme["CTkSlider"]["button_corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkSlider"]["border_width"],
    #                 button_length=ctk.ThemeManager.theme["CTkSlider"]["button_length"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkSlider"]["fg_color"]),
    #                 progress_color=pick_color(ctk.ThemeManager.theme["CTkSlider"]["progress_color"]),
    #                 button_color=pick_color(ctk.ThemeManager.theme["CTkSlider"]["button_color"]),
    #                 button_hover_color=pick_color(ctk.ThemeManager.theme["CTkSlider"]["button_hover_color"]),
    #             )

    #         # ---- CTkOptionMenu ----
    #         elif isinstance(widget, ctk.CTkOptionMenu):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkOptionMenu"]["corner_radius"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkOptionMenu"]["fg_color"]),
    #                 button_color=pick_color(ctk.ThemeManager.theme["CTkOptionMenu"]["button_color"]),
    #                 button_hover_color=pick_color(ctk.ThemeManager.theme["CTkOptionMenu"]["button_hover_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkOptionMenu"]["text_color"]),
    #             )
    #             # Dropdown menu
    #             if hasattr(widget, "dropdown_menu") and widget.dropdown_menu:
    #                 widget.dropdown_menu.configure(
    #                     fg_color=pick_color(ctk.ThemeManager.theme["DropdownMenu"]["fg_color"]),
    #                     hover_color=pick_color(ctk.ThemeManager.theme["DropdownMenu"]["hover_color"]),
    #                     text_color=pick_color(ctk.ThemeManager.theme["DropdownMenu"]["text_color"]),
    #                 )

    #         # ---- CTkComboBox ----
    #         elif isinstance(widget, ctk.CTkComboBox):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkComboBox"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkComboBox"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkComboBox"]["fg_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkComboBox"]["border_color"]),
    #                 button_color=pick_color(ctk.ThemeManager.theme["CTkComboBox"]["button_color"]),
    #                 button_hover_color=pick_color(ctk.ThemeManager.theme["CTkComboBox"]["button_hover_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkComboBox"]["text_color"]),
    #             )

    #         # ---- CTkScrollbar ----
    #         elif isinstance(widget, ctk.CTkScrollbar):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkScrollbar"]["corner_radius"],
    #                 border_spacing=ctk.ThemeManager.theme["CTkScrollbar"]["border_spacing"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkScrollbar"]["fg_color"]),
    #                 button_color=pick_color(ctk.ThemeManager.theme["CTkScrollbar"]["button_color"]),
    #                 button_hover_color=pick_color(ctk.ThemeManager.theme["CTkScrollbar"]["button_hover_color"]),
    #             )

    #         # ---- CTkSegmentedButton ----
    #         elif isinstance(widget, ctk.CTkSegmentedButton):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkSegmentedButton"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkSegmentedButton"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkSegmentedButton"]["fg_color"]),
    #                 selected_color=pick_color(ctk.ThemeManager.theme["CTkSegmentedButton"]["selected_color"]),
    #                 selected_hover_color=pick_color(ctk.ThemeManager.theme["CTkSegmentedButton"]["selected_hover_color"]),
    #                 unselected_color=pick_color(ctk.ThemeManager.theme["CTkSegmentedButton"]["unselected_color"]),
    #                 unselected_hover_color=pick_color(ctk.ThemeManager.theme["CTkSegmentedButton"]["unselected_hover_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkSegmentedButton"]["text_color"]),
    #             )

    #         # ---- CTkTextbox ----
    #         elif isinstance(widget, ctk.CTkTextbox):
    #             widget.configure(
    #                 corner_radius=ctk.ThemeManager.theme["CTkTextbox"]["corner_radius"],
    #                 border_width=ctk.ThemeManager.theme["CTkTextbox"]["border_width"],
    #                 fg_color=pick_color(ctk.ThemeManager.theme["CTkTextbox"]["fg_color"]),
    #                 border_color=pick_color(ctk.ThemeManager.theme["CTkTextbox"]["border_color"]),
    #                 text_color=pick_color(ctk.ThemeManager.theme["CTkTextbox"]["text_color"]),
    #                 scrollbar_button_color=pick_color(ctk.ThemeManager.theme["CTkTextbox"]["scrollbar_button_color"]),
    #                 scrollbar_button_hover_color=pick_color(ctk.ThemeManager.theme["CTkTextbox"]["scrollbar_button_hover_color"]),
    #             )

    #         # ---- CTkScrollableFrame ----
    #         elif isinstance(widget, ctk.CTkScrollableFrame):
    #             widget.configure(
    #                 label_fg_color=pick_color(ctk.ThemeManager.theme["CTkScrollableFrame"]["label_fg_color"]),
    #             )

    #         # Recursively update children
    #         for child in widget.winfo_children():
    #             update_widget_recursive(child)

    #     # Update main window
    #     self.configure(fg_color=pick_color(ctk.ThemeManager.theme["CTk"]["fg_color"]))

    #     # Update all children
    #     for widget in self.winfo_children():
    #         update_widget_recursive(widget)


    def choose_text_color(self):
        global text_color
        color = colorchooser.askcolor(initialcolor='white')[1]
        self.text_color_label_box.configure(text_color = color)
        if color:
            print(f"Chosen text color: {color}")
        text_color = color
        self.settings["text_color"] = color
        self.save_settings()

    def choose_box_color(self):
        global box_color
        color = colorchooser.askcolor(initialcolor='black')[1]
        self.box_color_label_box.configure(text_color = color)
        if color:
            print(f"Chosen box color: {color}")
        box_color = color
        self.settings["box_color"] = color
        self.save_settings()

    def HistoryFileDirectory(self):
        directory = filedialog.askdirectory(title="Select Directory")
        self.histroy_file_dir_opt.delete(0, "end")
        self.histroy_file_dir_opt.insert('end', f'{directory}\history.txt')

    def ChangeWallpaper(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:  # if user selected a file
            self.desktop_wallpaper_dir_opt.delete(0, "end")
            self.desktop_wallpaper_dir_opt.insert('end', file_path)
            self.settings["desktop_wallpaper"] = file_path

            img = Image.open(file_path)
            img_w, img_h = img.size
            self.settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

            self.font_size_opt.delete(0, "end")
            self.font_size_opt.insert('end',int((img_w + img_h)/2 * 0.03/1.333))

            self.console_textbox.configure(state="normal")
            self.console_textbox.delete("1.0", "end")
            self.console_textbox.insert('0.0', f"● Operating System:\n  --->  {platform.system()}\n\n")
            self.console_textbox.insert('end', f"● Desktop Wallpaper Location:\n  --->  {file_path}\n\n")
            self.console_textbox.insert('end', f"● Desktop Wallpaper Image Size (using Pillow):\n  ---> {img_w}(w) * {img_h}(h)\n\n")
            self.console_textbox.insert('end', f"● Suggested Text Font Size for TDL:\n  ---> {int((img_w + img_h)/2 * 0.03/1.333)}\n\n")
            self.console_textbox.insert('end', f"● Existing Fonts For Chinese Language Support:\n  ---> Simfang, Simhei, Simkai\n\n")
            self.console_textbox.configure(state="disabled") # Make it read-only for user input


            self.save_settings()

    ### App Functionalties
    
    def Save(self):
        global box_color, text_color
        entry = self.textbox.get('0.0','end').strip()

        # read textbox text-size from the settings page
        self.textbox.configure(font=ctk.CTkFont(size=int(self.textbox_font_size_opt.get())))

        if entry != "":
            fn.WriteOnDesktop(entry, 
                            self.desktop_wallpaper_dir_opt.get(),
                            self.position_opt.get(), 
                            self.font_opt.get(),
                            int(self.font_size_opt.get()),
                            text_color,
                            box_color,
                            int(self.text_padding_opt.get()),
                            int(self.frame_padding_opt.get())
                            )

            # Save to the history file
            history = f"{datetime.date.today()}  ({datetime.datetime.now().strftime('%I:%M %p')})\n{entry}\n\n"

            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    existing_content = f.read()
            except FileNotFoundError:
                existing_content = ""

            with open(self.history_file, "w", encoding="utf-8") as f:
                f.write(history + existing_content)

            self.history_textbox.configure(state="normal")  # Temporarily allow writing
            self.history_textbox.insert('0.0', history)
            self.history_textbox.configure(state="disabled") # Lock again
            self.history_label.configure(text=f"History file size: {fn.FileSize(self.history_file)}")
        else: pass
    
    def Reset(self):
        fn.set_wallpaper(self.desktop_wallpaper_dir_opt.get())
    
    def Clear(self):
        self.textbox.delete("1.0", "end")

    def DeleteHistory(self):
        # Show confirmation dialog with a more professional message
        if messagebox.askyesno("Confirm Deletion", 
                               "This action will permanently delete all local history files. Do you wish to proceed?"):
            try:
                # Proceed with deletion if user confirms
                if os.path.exists(self.history_file):
                    with open(self.history_file, "w", encoding="utf-8") as f:
                        f.write("")

                self.history_textbox.configure(state="normal")  # Temporarily allow writing
                self.history_textbox.delete("1.0", "end")
                self.history_textbox.configure(state="disabled") # Lock again

            except (IOError, PermissionError) as e:
                messagebox.showerror("Error", f"Failed to delete history: {str(e)}")
        else:
            # Do nothing if user cancels
            pass
        
        self.history_label.configure(text=f"History file size: {fn.FileSize(self.history_file)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()