import sys, os
import json
import customtkinter as ctk
from tkinter import colorchooser
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import datetime
import functions as fn
from PIL import Image, ImageTk  

# Importing Dictonaries
from directories import WindowsFonts, ThemeOptions
from translations import translations

LanguageOptions = {

    "English": "English",
    "简体中文": "Simplified Chinese",
    "繁體中文": "Traditional Chinese",
    "Bahasa Indonesia": "Indonesian",
    "Bahasa Melayu": "Malay",
    "Español": "Spanish",
    "한국어": "Korean",
    "Italiano": "Italian",
    "日本語": "Japanese",
    "Português": "Portuguese",
    "Русский": "Russian",
    "ไทย": "Thai",
    "Tiếng Việt": "Vietnamese",
    "العربية": "Arabic",
    "Türkçe": "Turkish",
    "Deutsch": "German",
    "Français": "French"
}



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Desktop TDL App")
        self.geometry("750x600")
        # self.resizable(False, False)  # prevent user from manually resizing

        ## Icon settings 
        ## -- load with .png file 
        # icon_path = "./assets/checklist.png"
        # if os.path.exists(icon_path):
        #     self.iconphoto(True,ImageTk.PhotoImage(Image.open(icon_path)))
        # else: pass
        ## -- load with .ico file
        self.iconbitmap("./assets/checklist.ico")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ### Default settings
        
        self.default_settings = {
            "Language" : "English",
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

        # Need to use a quicker way, much quicker than Pillow....
        img = Image.open(self.default_settings["desktop_wallpaper"])
        img_w, img_h = img.size
        self.default_settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

        ## Manage where data is saved (histroy and settings
        if sys.platform == "darwin":
            pass

        elif sys.platform.startswith("win"):
            self.data_folder = f"{os.environ.get('LOCALAPPDATA')}\\Desktop TDL"
            os.makedirs(self.data_folder, exist_ok=True) # Ensure folder exists
            self.settings_file = f"{self.data_folder}\\settings.json"
            self.history_file = f"{self.data_folder}\\history.txt"

        elif sys.platform.startswith("linux"):
            from pathlib import Path
            self.data_folder = Path.home() / ".local" / "share" / "Desktop_TDL"
            os.makedirs(self.data_folder, exist_ok=True) # Ensure folder exists
            self.settings_file = f"{self.data_folder}/settings.json"
            self.history_file = f"{self.data_folder}/history.txt"

        # Create files if missing
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, "w") as f:
                json.dump({}, f) 
        self.settings = self.load_settings()

        if not os.path.exists(self.history_file):
            open(self.history_file, "w").close()  

        # img = Image.open(self.settings["desktop_wallpaper"])
        # img_w, img_h = img.size
        # self.settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

        if self.settings["Theme"] in ["Blue", "Dark Blue", "Green"]:
            ctk.set_default_color_theme(self.settings["Theme"].lower().replace(" ", "-"))
        else: pass
            
        ctk.set_appearance_mode(self.settings["Apperance Mode"])
        ctk.set_widget_scaling(int(self.settings["UI Scaling"].replace("%", "")) / 100)

        self.VERSION = "1.0.8"

        self.current_language = self.settings.get("Language", "English")

        # --------------------------------------------------
        #     Side Bar
        # --------------------------------------------------
        
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=120, corner_radius=0, border_width=0, fg_color="transparent")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

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
        self.clear_button = ctk.CTkButton(self.main_frame,text="Clear", command=self.Clear)
        self.clear_button.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="e")

        # Text box
        textbox_fontsize = 14 # This is a variable
        self.textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=textbox_fontsize))
        self.textbox.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky="nsew")
        with open(self.history_file, "r", encoding="utf-8") as f:
            self.textbox.insert('0.0',"\n".join(f.read().split("\n\n")[0].split("\n")[1:]))

        # Rest Button
        self.reset_button = ctk.CTkButton(self.main_frame,text="Remove from Desktop", command=self.Reset)
        self.reset_button.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        # Save Button
        self.save_button = ctk.CTkButton(self.main_frame,text="Add to Desktop", command=self.Save)
        self.save_button.grid(row=3, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")

        # --------------------------------------------------
        #       Setting Frame
        # --------------------------------------------------

        # create the settings frame
        self.settings_frame = ctk.CTkScrollableFrame(self, corner_radius=0, border_width=0, width =1000, fg_color="transparent", orientation="vertical")
        self.settings_frame.grid_rowconfigure(0, weight=0)
        self.settings_frame.grid_columnconfigure(0, minsize=350, weight=1)
        self.settings_frame.grid_columnconfigure(1, minsize=300, weight=1)

        self.settings_frame_title = ctk.CTkLabel(self.settings_frame, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.settings_frame_title.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20,10), sticky="w")

        padx_left_labels = 10
        padx_right_optiosn = 10

        ### Language
        n_row = 1
        self.language_label = ctk.CTkLabel(self.settings_frame, text="Language", anchor="w")
        self.language_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.language_opt = ctk.CTkOptionMenu(self.settings_frame, values=list(LanguageOptions.keys()), command=self.change_language_event)
        self.language_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        self.language_opt.set(self.settings["Language"])

        ### Apperance Mode Settings
        n_row += 1
        self.appearance_mode_label = ctk.CTkLabel(self.settings_frame, text="Appearance Mode", anchor="w")
        self.appearance_mode_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        self.appearance_mode_optionemenu.set(self.settings["Apperance Mode"])

        ### UI Scaling
        n_row += 1
        self.ui_scaling_label = ctk.CTkLabel(self.settings_frame, text="UI Scaling", anchor="w")
        self.ui_scaling_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.scaling_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=["80%", "85%" ,"90%", "95%" , "100%", "105%" , "110%", "115%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        self.scaling_optionemenu.set(self.settings["UI Scaling"])

        ### Theme settings
        n_row += 1
        self.theme_label = ctk.CTkLabel(self.settings_frame, text="Theme", anchor="w")
        self.theme_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.theme_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=list(ThemeOptions.keys()),command=self.change_theme_event)
        self.theme_optionemenu.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        self.theme_optionemenu.set(self.settings["Theme"]) 

        ### Font
        n_row += 1
        self.font_label = ctk.CTkLabel(self.settings_frame, text="Font")
        self.font_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        font_options = ["Arial", "Arial2", "Arials"]
        self.font_opt = ctk.CTkOptionMenu(self.settings_frame, values=list(WindowsFonts.keys()), command=self.change_font_event)
        self.font_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        
        self.font_opt.set(self.settings["font"])

        ### Font Size
        n_row += 1
        self.font_size_label = ctk.CTkLabel(self.settings_frame, text="Font Size")
        self.font_size_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.font_size_opt = ctk.CTkEntry(self.settings_frame)
        self.font_size_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.font_size_opt.insert('end', self.settings["font size"])
        self.font_size_opt.bind("<FocusOut>", lambda e: self.on_font_size_change())
        self.font_size_opt.bind("<Return>", lambda e: self.on_font_size_change())

        ### App Textbox Font Size
        n_row += 1
        self.textbox_font_size_label = ctk.CTkLabel(self.settings_frame, text="App Textbox Font Size")
        self.textbox_font_size_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.textbox_font_size_opt = ctk.CTkEntry(self.settings_frame)
        self.textbox_font_size_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.textbox_font_size_opt.insert('end', self.settings["textbox_fontsize"])
        self.textbox_font_size_opt.bind("<FocusOut>", lambda e: self.on_textbox_font_size_change())
        self.textbox_font_size_opt.bind("<Return>", lambda e: self.on_textbox_font_size_change())
        self.textbox.configure(font=ctk.CTkFont(size=self.settings["textbox_fontsize"]))

        ### Position 
        n_row += 1
        self.position_label = ctk.CTkLabel(self.settings_frame, text="Position")
        self.position_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        position_options = ["Top Right", "Top Left", "Bottom Right", "Bottom Left", "Center"]
        self.position_opt = ctk.CTkOptionMenu(self.settings_frame, values=position_options, command=self.change_position_event)
        self.position_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.position_opt.set(self.settings["position"])

        ### Text Color
        n_row += 1
        self.text_color_label = ctk.CTkLabel(self.settings_frame, text="Text Color: ")
        self.text_color_label.grid(row=n_row, column=0, padx=(30, padx_left_labels), pady=10, sticky="w")

        self.text_color_label_box = ctk.CTkLabel(self.settings_frame, text="⬤")
        self.text_color_label_box.grid(row=n_row, column=0, padx=(10, 10), pady=10, sticky="w")

        self.text_color_opt = ctk.CTkButton(self.settings_frame, text="Choose Color", command=self.choose_text_color)
        self.text_color_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        global text_color
        text_color = self.settings["text_color"]
        self.text_color_label_box.configure(text_color=text_color)
        
        ### Box Color
        n_row += 1
        self.box_color_label = ctk.CTkLabel(self.settings_frame, text="Box Color: ")
        self.box_color_label.grid(row=n_row, column=0, padx=(30, padx_left_labels), pady=10, sticky="w")

        self.box_color_label_box = ctk.CTkLabel(self.settings_frame, text="⬤")
        self.box_color_label_box.grid(row=n_row, column=0, padx=(10, 10), pady=10, sticky="w")

        self.box_color_opt = ctk.CTkButton(self.settings_frame, text="Choose Color", command=self.choose_box_color)
        self.box_color_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        global box_color
        box_color = self.settings["box_color"]
        self.box_color_label_box.configure(text_color=box_color)

        ### Frame Padding
        n_row += 1
        self.frame_padding_label = ctk.CTkLabel(self.settings_frame, text="Text-Box Padding")
        self.frame_padding_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.frame_padding_opt = ctk.CTkEntry(self.settings_frame)
        self.frame_padding_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.frame_padding_opt.insert('end', self.settings["text_padding"])
        self.frame_padding_opt.bind("<FocusOut>", lambda e: self.on_frame_padding_change())
        self.frame_padding_opt.bind("<Return>", lambda e: self.on_frame_padding_change())

        ### Text Padding
        n_row += 1
        self.text_padding_label = ctk.CTkLabel(self.settings_frame, text="Box-Frame Padding")
        self.text_padding_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.text_padding_opt = ctk.CTkEntry(self.settings_frame)
        self.text_padding_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.text_padding_opt.insert('end', self.settings["frame_padding"])
        self.text_padding_opt.bind("<FocusOut>", lambda e: self.on_text_padding_change())
        self.text_padding_opt.bind("<Return>", lambda e: self.on_text_padding_change())

        ### Desktop Wallpaper Path
        n_row += 1
        self.desktop_wallpaper_dir_label = ctk.CTkLabel(self.settings_frame, text="Desktop Wallpaper Path:")
        self.desktop_wallpaper_dir_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.desktop_wallpaper_dir_button = ctk.CTkButton(self.settings_frame, text="Change Wallpaper", command=self.ChangeWallpaper)
        self.desktop_wallpaper_dir_button.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        self.desktop_wallpaper_dir_opt = ctk.CTkEntry(self.settings_frame, border_width = 0, bg_color = "transparent")
        self.desktop_wallpaper_dir_opt.grid(row=n_row+1, column=0, columnspan =2, padx=(10,10), pady=(10,10), sticky="ew")
        
        self.desktop_wallpaper_dir_opt.insert('end', self.settings["desktop_wallpaper"])
        
        # ### Current Desktop Wallpaper
        # n_row += 2
        # self.desktop_wallpaper_dir_label = ctk.CTkLabel(self.settings_frame, text="Current Desktop Wallpaper:")
        # self.desktop_wallpaper_dir_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=5, sticky="w")

        # ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size = (340,200))
        # self.desktop_wallpaper_image = ctk.CTkLabel(self.settings_frame, text="", image = ctk_img)
        # self.desktop_wallpaper_image.grid(row=n_row+1, column=0, columnspan =2, padx=(10,10), pady=(0,10), sticky="ew")

        ### Check for updates
        n_row += 2
        self.current_version_label = ctk.CTkLabel(self.settings_frame, text=f"Current Version: {self.VERSION}")
        self.current_version_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.check_update_opt = ctk.CTkButton(self.settings_frame, text="Check For Updates", command=self.CheckUpdates)
        self.check_update_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        ## Reset Settings Button
        n_row += 3
        self.settings_frame.grid_columnconfigure(n_row, weight=1)
        self.reset_settings_button = ctk.CTkButton(self.settings_frame,text="Reset Settings" ,command=self.ResetSettings)
        self.reset_settings_button.grid(row=n_row, column=0, columnspan=2, padx=(10, 10), pady=(50, 5), sticky="ew")

        ## Delete Data Button
        n_row += 1
        self.settings_frame.grid_columnconfigure(n_row, weight=1)
        self.delete_all_data_button = ctk.CTkButton(self.settings_frame,text="Delete App Data" , hover_color= "darkred",  command=self.DeleAllData)
        self.delete_all_data_button.grid(row=n_row, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="ew")

        # --------------------------------------------------
        #       History Frame
        # --------------------------------------------------

        # create the history frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color="transparent")
        self.history_frame.grid_rowconfigure(1, weight=0)
        self.history_frame.grid_rowconfigure(2, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)



        # Label
        self.history_page_title = ctk.CTkLabel(self.history_frame, text="History", font=ctk.CTkFont(size=20, weight="bold"))
        self.history_page_title.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20,10), sticky="w")

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
        #       Starting The APP
        # --------------------------------------------------

        # Initially show the To Do List frame
        self.show_frame(self.main_frame)

        if self.settings["Theme"] not in ["Blue", "Dark Blue", "Green"]:
            self.change_theme_event(self.settings["Theme"])
        else: pass

        self.update_texts()

    ### Frame Settings
    def show_frame(self, frame):
        self.main_frame.grid_remove()
        self.settings_frame.grid_remove()
        self.history_frame.grid_remove()
        frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def ToDoListsPage(self):
        self.show_frame(self.main_frame)

    def SettingsPage(self):
        self.show_frame(self.settings_frame)
    
    def HistoryPage(self):
        self.show_frame(self.history_frame)

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
        self.update_widget_colors(new_theme)
        self.save_settings()

    def update_widget_colors(self, new_theme):
                
            def update_widget_recursive(widget):

                if isinstance(widget, ctk.CTkButton):
                    widget.configure(
                        fg_color = ThemeOptions[new_theme]["button_fg_color"],
                        hover_color = ThemeOptions[new_theme]["button_hover_color"],
                        
                    )
                
                elif isinstance(widget, ctk.CTkOptionMenu):
                    widget.configure(
                        fg_color = ThemeOptions[new_theme]["button_fg_color"],
                        button_color = ThemeOptions[new_theme]["button_hover_color"],
                        button_hover_color = ThemeOptions[new_theme]["optionmenu_button_hover_color"],
                    )

                # Recursively update children
                for child in widget.winfo_children():
                    update_widget_recursive(child)

            # Update main window (only buttons and optionmenus, so no need for fg_color here unless it's a button-like)
            
            # Update all children
            for widget in self.winfo_children():
                update_widget_recursive(widget)
    
    ### Language Settings

    def change_language_event(self, new_language: str):
        self.current_language = new_language
        self.settings["Language"] = new_language
        self.save_settings()
        self.update_texts()

    def get_text(self, key) -> str:
        """
        Return the text for current language and fallback to English or the key.
        """
        lang = getattr(self, "current_language", self.settings.get("Language", "English"))
        # try language first
        if lang in translations and key in translations[lang]:
            return translations[lang][key]
        # fallback to English
        if "English" in translations and key in translations["English"]:
            return translations["English"][key]
        # final fallback
        return key

    def update_texts(self):
        """
        Update all widgets' visible text to the current language.
        Safe to call at any time; uses try/except around each widget so missing widgets
        don't break the update flow.
        """

        ## sidebar buttons
        try:
            self.sidebar_button_1.configure(text=self.get_text("todo_list"))
        except Exception:
            pass
        try:
            self.sidebar_button_2.configure(text=self.get_text("settings"))
        except Exception:
            pass
        try:
            self.sidebar_button_3.configure(text=self.get_text("history"))
        except Exception:
            pass

        ## Main Frame

        try:
            self.text_label.configure(text=self.get_text("write_tdl"))
        except Exception:
            pass

        try:
            self.clear_button.configure(text=self.get_text("clear"))
        except Exception:
            pass
        try:
            self.save_button.configure(text=self.get_text("add_to_desktop"))
        except Exception:
            pass

        try:
            self.reset_button.configure(text=self.get_text("remove_from_desktop"))
        except Exception:
            pass

        ## Settings frame

        try:
            self.settings_frame_title.configure(text=self.get_text("settings"))
        except Exception:
            pass

        try:
            self.language_label.configure(text=self.get_text("language"))
        except Exception:
            pass

        try:
            self.appearance_mode_label.configure(text=self.get_text("appearance_mode"))
        except Exception:
            pass

        try:
            self.ui_scaling_label.configure(text=self.get_text("ui_scaling"))
        except Exception:
            pass

        try:
            self.theme_label.configure(text=self.get_text("theme"))
        except Exception:
            pass

        try:
            self.font_label.configure(text=self.get_text("font"))
        except Exception:
            pass

        try:
            self.font_size_label.configure(text=self.get_text("font_size"))
        except Exception:
            pass

        try:
            self.textbox_font_size_label.configure(text=self.get_text("textbox_font_size"))
        except Exception:
            pass

        try:
            self.position_label.configure(text=self.get_text("position"))
        except Exception:
            pass

        try:
            self.text_color_label.configure(text=self.get_text("text_color"))
        except Exception:
            pass

        try:
            self.box_color_label.configure(text=self.get_text("box_color"))
        except Exception:
            pass

        try:
            self.frame_padding_label.configure(text=self.get_text("text_box_padding"))
        except Exception:
            pass

        try:
            self.text_padding_label.configure(text=self.get_text("box_frame_padding"))
        except Exception:
            pass

        try:
            self.desktop_wallpaper_dir_label.configure(text=self.get_text("desktop_wallpaper"))
        except Exception:
            pass

        try:
            self.desktop_wallpaper_dir_button.configure(text=self.get_text("change_wallpaper"))
        except Exception:
            pass

        try:
            self.current_version_label.configure(text=self.get_text("current_version").format(version=self.VERSION))
        except Exception:
            pass

        try:
            self.check_update_opt.configure(text=self.get_text("check_updates"))
        except Exception:
            pass

        try:
            self.reset_settings_button.configure(text=self.get_text("reset_settings"))
        except Exception:
            pass

        try:
            self.delete_all_data_button.configure(text=self.get_text("delete_data"))
        except Exception:
            pass


        # History frame labels
        try:
            self.history_page_title.configure(text=self.get_text("history"))
        except Exception:
            pass

        try:
            size_text = self.get_text("history_file_size").format(size=fn.FileSize(self.history_file))
            self.history_label.configure(text=size_text)
        except Exception:
            pass

        try:
            self.history_reset_button.configure(text=self.get_text("delete_history"))
        except Exception:
            pass


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
    
    def ResetSettings(self):
        """Reset settings to defaults (after user confirmation) and update the UI."""
        if not messagebox.askyesno("Confirm Reset", "This will reset all settings to defaults. Continue?"):
            return

        try:
            # Reset settings dict (shallow copy is fine: values are primitives)

            self.settings = self.default_settings.copy()

            # # Recompute font size if wallpaper image exists (more robust)
            # wp = self.settings.get("desktop_wallpaper") or fn.get_wallpaper_path()
            # img_w, img_h = 0, 0
            # try:
            #     if os.path.exists(wp):
            #         img = Image.open(wp)
            #         img_w, img_h = img.size
            #         self.settings["font size"] = int((img_w + img_h) / 2 * 0.03 / 1.333)
            #         ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size = (340,200))
            #         self.desktop_wallpaper_image.configure(image = ctk_img)
            # except Exception:
            #     # If image read fails, keep existing font size value
            #     img_w, img_h = 0, 0

            # Apply CTk appearance / theme / scaling
            try:
                ctk.set_default_color_theme(ThemeOptions[self.settings["Theme"]])
            except Exception:
                # fallback to current theme if lookup fails
                pass
            ctk.set_appearance_mode(self.settings["Apperance Mode"])
            try:
                ctk.set_widget_scaling(int(self.settings["UI Scaling"].replace("%", "")) / 100)
            except Exception:
                pass

            # Update settings widgets to reflect defaults
            self.appearance_mode_optionemenu.set(self.settings["Apperance Mode"])
            self.scaling_optionemenu.set(self.settings["UI Scaling"])
            self.theme_optionemenu.set(self.settings["Theme"])
            self.font_opt.set(self.settings["font"])

            # Font size entry
            self.font_size_opt.delete(0, "end")
            self.font_size_opt.insert("end", self.settings["font size"])

            # Textbox font size entry + apply to textbox
            self.textbox_font_size_opt.delete(0, "end")
            self.textbox_font_size_opt.insert("end", self.settings["textbox_fontsize"])
            try:
                self.textbox.configure(font=ctk.CTkFont(size=int(self.settings["textbox_fontsize"])))
            except Exception:
                pass

            # Position
            self.position_opt.set(self.settings["position"])

            # Colors (also update globals used by Save)
            global text_color, box_color
            text_color = self.settings.get("text_color", "white")
            box_color = self.settings.get("box_color", "black")
            try:
                self.text_color_label_box.configure(text_color=text_color)
                self.box_color_label_box.configure(text_color=box_color)
            except Exception:
                pass

            # Padding entries (note keys used in your code)
            self.frame_padding_opt.delete(0, "end")
            self.frame_padding_opt.insert("end", self.settings.get("text_padding", "30"))

            self.text_padding_opt.delete(0, "end")
            self.text_padding_opt.insert("end", self.settings.get("frame_padding", "80"))

            # # Desktop wallpaper entry
            # self.desktop_wallpaper_dir_opt.delete(0, "end")
            # self.desktop_wallpaper_dir_opt.insert("end", self.settings.get("desktop_wallpaper", ""))

            # # Update console info (show wallpaper info and suggested font size)
            # self.console_textbox.configure(state="normal")
            # self.console_textbox.delete("1.0", "end")
            # self.console_textbox.insert('0.0', f"● Operating System:\n  --->  {platform.system()}\n\n")
            # self.console_textbox.insert('end', f"● Desktop Wallpaper Location:\n  --->  {self.settings.get('desktop_wallpaper')}\n\n")
            # self.console_textbox.insert('end', f"● Desktop Wallpaper Image Size (using Pillow):\n  ---> {img_w}(w) * {img_h}(h)\n\n")
            # self.console_textbox.insert('end', f"● Suggested Text Font Size for TDL:\n  ---> {self.settings.get('font size')}\n\n")
            # self.console_textbox.insert('end', "● Existing Fonts For Chinese Language Support:\n  ---> Simfang, Simhei, Simkai\n\n")
            # self.console_textbox.configure(state="disabled")

            # Persist defaults to disk
            self.save_settings()

            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")


    ### Updating Settings

    def change_font_event(self, new_font: str):
        """Called when user selects a new font from the OptionMenu."""
        self.settings["font"] = new_font
        self.save_settings()

    def on_font_size_change(self):
        """Validate and save the global font size used for drawing on desktop."""
        val = self.font_size_opt.get().strip()
        if val == "":
            return
        try:
            v = int(val)
            self.settings["font size"] = v
            self.save_settings()
        except ValueError:
            messagebox.showerror("Invalid Value", "Font size must be an integer.")
            # revert entry to saved value
            self.font_size_opt.delete(0, "end")
            self.font_size_opt.insert("end", str(self.settings.get("font size", "")))

    def on_textbox_font_size_change(self):
        """Apply and save the app textbox font size."""
        val = self.textbox_font_size_opt.get().strip()
        if val == "":
            return
        try:
            v = int(val)
            self.settings["textbox_fontsize"] = v
            # apply immediately to textbox
            try:
                self.textbox.configure(font=ctk.CTkFont(size=v))
            except Exception:
                pass
            self.save_settings()
        except ValueError:
            messagebox.showerror("Invalid Value", "Textbox font size must be an integer.")
            self.textbox_font_size_opt.delete(0, "end")
            self.textbox_font_size_opt.insert("end", str(self.settings.get("textbox_fontsize", 14)))

    def change_position_event(self, new_position: str):
        """Save desktop text position selection."""
        self.settings["position"] = new_position
        self.save_settings()

    def on_frame_padding_change(self):
        """Save Text-Box Padding (frame padding)."""
        val = self.frame_padding_opt.get().strip()
        if val == "":
            return
        try:
            v = int(val)
            self.settings["text_padding"] = str(v)   # keep same type as your defaults (strings)
            self.save_settings()
        except ValueError:
            messagebox.showerror("Invalid Value", "Text-Box Padding must be an integer.")
            self.frame_padding_opt.delete(0, "end")
            self.frame_padding_opt.insert("end", str(self.settings.get("text_padding", "30")))

    def on_text_padding_change(self):
        """Save Box-Frame Padding (text padding)."""
        val = self.text_padding_opt.get().strip()
        if val == "":
            return
        try:
            v = int(val)
            self.settings["frame_padding"] = str(v)
            self.save_settings()
        except ValueError:
            messagebox.showerror("Invalid Value", "Box-Frame Padding must be an integer.")
            self.text_padding_opt.delete(0, "end")
            self.text_padding_opt.insert("end", str(self.settings.get("frame_padding", "80")))

    def choose_text_color(self):
        global text_color
        color = colorchooser.askcolor(initialcolor='white')[1]
        self.text_color_label_box.configure(text_color = color)
        text_color = color
        self.settings["text_color"] = color
        self.save_settings()

    def choose_box_color(self):
        global box_color
        color = colorchooser.askcolor(initialcolor='black')[1]
        self.box_color_label_box.configure(text_color = color)
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

            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size = (340,200))
            self.desktop_wallpaper_image.configure(image = ctk_img)

            self.font_size_opt.delete(0, "end")
            self.font_size_opt.insert('end',int((img_w + img_h)/2 * 0.03/1.333))


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

    def DeleAllData(self):

        if messagebox.askyesno("Confirm Deletion", 
                               f"This action will permanently delete all local history and settings files at:\n - {self.settings_file}\n - {self.history_file}\nDo you wish to proceed?"):
            
            # (1) Clean desktop wallpaper
            self.Reset()

            # (2) Reset Settings
            self.ResetSettings()
            
            # (3) Clean history textbox
            self.history_textbox.configure(state="normal")  # Temporarily allow writing
            self.history_textbox.delete("1.0", "end")
            self.history_textbox.configure(state="disabled") # Lock again

            # (4) Clean TDL textbox
            self.textbox.delete("1.0", "end")
            
            # (5) Delete app files
            try:
                if os.path.exists(self.data_folder):
                    from shutil import rmtree
                    rmtree(self.data_folder)
            except (IOError, PermissionError) as e:
                messagebox.showerror("Error", f"Failed to delete history: {str(e)}")

        else:
            # Do nothing if user cancels
            pass

    def CheckUpdates(self):
        import requests, base64
        path = "version.txt"
        branch = "main"
        api_url = f"https://api.github.com/repos/ammelsayed/Desktop-TDL/contents/{path}?ref={branch}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            content = base64.b64decode(data["content"]).decode("utf-8").strip()
            local_version = tuple(map(int, self.VERSION.split('.')))
            remote_version = tuple(map(int, content.split('.')))
            if remote_version > local_version:
                if messagebox.askyesno("Update Available", f"Latest update available: {content}. Do you wish to update?"):
                    
                    from webbrowser import open
                    open("https://ammelsayed.github.io/projects/DesktopTDL/")

                    # update_url = "https://github.com/ammelsayed/Desktop-TDL/releases/download/1.0.7/DesktopTDL.exe"

                    # import tempfile
                    # from glob import glob
                    # from tempfile import gettempdir
                    # from shutil import copy2
                    # from subprocess import Popen

                    # try:
                    #     # 1. Download new exe to a temp file
                    #     tmp_path = os.path.join(gettempdir(), "DesktopTDL_new.exe")
                    #     r = requests.get(update_url, stream=True)
                    #     r.raise_for_status()
                    #     with open(tmp_path, "wb") as f:
                    #         for chunk in r.iter_content(chunk_size=8192):
                    #             f.write(chunk)

                    #     # 2. Find and delete all old DesktopTDL.exe files
                    #     search_paths = [
                    #         f"{os.environ.get('LOCALAPPDATA')}\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs",
                    #     ]

                    #     for path in search_paths:
                    #         if os.path.exists(path):
                    #             for file in glob.glob(path + "\\**\\DesktopTDL.exe", recursive=True):
                    #                 try:
                    #                     if os.path.samefile(file, sys.executable):
                    #                         continue  # don't delete the running one
                    #                     os.remove(file)
                    #                 except Exception:
                    #                     pass

                    #     # 3. Copy the new exe to replace the running one
                    #     new_path = os.path.join(os.path.dirname(sys.executable), "DesktopTDL.exe")
                    #     copy2(tmp_path, new_path)

                    #     # 4. Start the new exe
                    #     Popen([new_path])

                    #     # 5. Exit current app
                    #     self.destroy()
                    #     sys.exit(0)

                    # except Exception as e:
                    #     import tkinter.messagebox as messagebox
                    #     messagebox.showerror("Update Failed", f"Error while updating: {str(e)}")

            else:
                messagebox.showinfo("Up to Date", f"You are running the latest version: {self.VERSION}")
        else:
            messagebox.showerror("Error", f"Failed to check for updates: Error {response.status_code}")

  

if __name__ == "__main__":
    app = App()
    app.mainloop()