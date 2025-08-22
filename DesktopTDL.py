import sys, os
import json
import customtkinter as ctk
from tkinter import colorchooser
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import datetime
import functions as fn
from cv2 import imread
from PIL import Image, ImageTk  

# Importing Dictonaries
from themes import ThemeOptions
from translations import translations, LanguageOptions

def FontsFinder():

    if sys.platform.startswith("win"):
        from PIL_CV2 import WindowsFonts
        return WindowsFonts

    elif sys.platform.startswith("linux"):
        from PIL_CV2 import DebianUbuntuFonts
        return DebianUbuntuFonts

    elif algo == "Pillow" or "Pillow + OpenCV" and sys.platform == "darwin":
        pass


class App(ctk.CTk):
    def __init__(self):

        super().__init__()

        ## --------------------------------------
        ## Configure window

        self.title("Desktop TDL App")
        self.geometry("750x550")

        ## --------------------------------------
        ## Icon settings 

        if sys.platform == "darwin":
            icon_path = "./assets/checklist.ico"
            if os.path.exists(icon_path):
                self.iconbitmap("./assets/checklist.ico")
            else: pass

        elif sys.platform.startswith("win"):
            icon_path = "./assets/checklist.ico"
            if os.path.exists(icon_path):
                self.iconbitmap("./assets/checklist.ico")
            else: pass

        elif sys.platform.startswith("linux"):
            icon_path = "./assets/checklist.png"
            if os.path.exists(icon_path):
                self.iconphoto(True,ImageTk.PhotoImage(Image.open(icon_path)))
            else: pass

        
        # configure grid layout (4x4)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ## --------------------------------------
        ## Create Data Folder 

        if sys.platform == "darwin":
            pass

        elif sys.platform.startswith("win"):
            self.data_folder = f"{os.environ.get('LOCALAPPDATA')}\\Desktop TDL"
            self.sub_files =  f"{self.data_folder}\\"

        elif sys.platform.startswith("linux"):
            from pathlib import Path
            self.data_folder = Path.home() / ".local" / "share" / "Desktop_TDL"
            self.sub_files =  f"{self.data_folder}/"

        os.makedirs(self.data_folder, exist_ok=True)

        ## --------------------------------------
        ## Create Settinngs file

        self.settings_file = f"{self.sub_files}settings.json"

        if not os.path.exists(self.settings_file):
            with open(self.settings_file, "w") as f:
                json.dump({}, f) 


        self.default_settings = {
            "Language" : "English",
            "Apperance Mode": "Light",
            "Theme" : "Blue",
            "UI Scaling" : "100%",
            "position": "Top Right",
            "font": "Comic",
            "font size": 14,
            "line_spacing" : 1,
            "font_weight" : 0,
            "textbox_fontsize" : 14,
            "text_color": "#ffffff",
            "box_color": "#000000",
            "text_padding": "30",
            "box_padding": "80",
            "wrap_length" : 60,
            "desktop_wallpaper": fn.get_wallpaper_path(),
        }

        # auto-compute the suggest fonts size for the default settings.
        img = imread(self.default_settings["desktop_wallpaper"])
        img_h, img_w = img.shape[:2]
        self.default_settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

        self.settings = self.load_settings()

        ## --------------------------------------
        ## Create history file

        self.history_file = f"{self.sub_files}history.txt"

        if not os.path.exists(self.history_file):
            open(self.history_file, "w").close()  

        ## --------------------------------------
        ## Initial Settings

        if self.settings["Theme"] in ["Blue", "Dark Blue", "Green"]:
            ctk.set_default_color_theme(self.settings["Theme"].lower().replace(" ", "-"))
        else: pass
            
        ctk.set_appearance_mode(self.settings["Apperance Mode"])
        ctk.set_widget_scaling(int(self.settings["UI Scaling"].replace("%", "")) / 100)

        self.VERSION = "1.0.7"

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
            self.textbox.insert('0.0',"\n".join(f.read().split(f"{'='*50}")[0].split("\n")[2:]))

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
        self.settings_frame = ctk.CTkScrollableFrame(self, corner_radius=0, border_width=0, width =600, fg_color="transparent", orientation="vertical")
        self.settings_frame.grid_rowconfigure(0, weight=0)
        self.settings_frame.grid_columnconfigure(0, minsize=470, weight=0)
        self.settings_frame.grid_columnconfigure(1, minsize=200, weight=0)

        self.settings_frame_title = ctk.CTkLabel(self.settings_frame, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.settings_frame_title.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20,10), sticky="w")

        padx_left_labels = 0
        padx_right_optiosn = 0

        ### Desktop Wallpaper Path
        n_row = 1
        self.desktop_wallpaper_dir_label = ctk.CTkLabel(self.settings_frame, text="Desktop Wallpaper Path:")
        self.desktop_wallpaper_dir_label.grid(row=n_row, column=0, columnspan =2, padx=(10,10), pady=(10,0), sticky="w")

        self.desktop_wallpaper_dir_button = ctk.CTkButton(self.settings_frame, text="Change Wallpaper", command=self.ChangeWallpaper)
        self.desktop_wallpaper_dir_button.grid(row=n_row + 1, column=1, padx=(padx_right_optiosn, 10), pady=(1,10), sticky="e")

        self.desktop_wallpaper_dir_opt = ctk.CTkEntry(self.settings_frame, border_width = 0, bg_color = "transparent")
        self.desktop_wallpaper_dir_opt.grid(row=n_row+1, column=0, padx=(10,10), pady=(1,10), sticky="ew")
        
        self.desktop_wallpaper_dir_opt.insert('end', self.settings["desktop_wallpaper"])

        ### Language
        n_row += 2
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

        ### Font
        n_row += 1
        self.font_label = ctk.CTkLabel(self.settings_frame, text="Font")
        self.font_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        font_options = ["Arial", "Arial2", "Arials"]
        self.font_opt = ctk.CTkOptionMenu(self.settings_frame, values=list(FontsFinder().keys()), command=self.change_font_event)
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

        ### Line Spacing
        n_row += 1
        self.line_spacing_label = ctk.CTkLabel(self.settings_frame, text="Line Spacing")
        self.line_spacing_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.line_spacing_opt = ctk.CTkEntry(self.settings_frame)
        self.line_spacing_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.line_spacing_opt.insert('end', self.settings["line_spacing"])
        self.line_spacing_opt.bind("<FocusOut>", lambda e: self.on_line_spacing_change())
        self.line_spacing_opt.bind("<Return>", lambda e: self.on_line_spacing_change())

        ### Font Weight
        n_row += 1
        self.font_weight_label = ctk.CTkLabel(self.settings_frame, text="Font Weight")
        self.font_weight_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.font_weight_opt = ctk.CTkEntry(self.settings_frame)
        self.font_weight_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.font_weight_opt.insert('end', self.settings["font_weight"])
        self.font_weight_opt.bind("<FocusOut>", lambda e: self.on_font_weight_change())
        self.font_weight_opt.bind("<Return>", lambda e: self.on_font_weight_change())

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

        self.text_color_label_box.configure(text_color=self.settings["text_color"])
        
        ### Box Color
        n_row += 1
        self.box_color_label = ctk.CTkLabel(self.settings_frame, text="Box Color: ")
        self.box_color_label.grid(row=n_row, column=0, padx=(30, padx_left_labels), pady=10, sticky="w")

        self.box_color_label_box = ctk.CTkLabel(self.settings_frame, text="⬤")
        self.box_color_label_box.grid(row=n_row, column=0, padx=(10, 10), pady=10, sticky="w")

        self.box_color_opt = ctk.CTkButton(self.settings_frame, text="Choose Color", command=self.choose_box_color)
        self.box_color_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")

        self.box_color_label_box.configure(text_color=self.settings["box_color"])

        ### Text Padding
        n_row += 1
        self.text_padding_label = ctk.CTkLabel(self.settings_frame, text="Text Padding")
        self.text_padding_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.text_padding_opt = ctk.CTkEntry(self.settings_frame)
        self.text_padding_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.text_padding_opt.insert('end', self.settings["text_padding"])
        self.text_padding_opt.bind("<FocusOut>", lambda e: self.on_text_padding_change())
        self.text_padding_opt.bind("<Return>", lambda e: self.on_text_padding_change())

        ### Text Padding
        n_row += 1
        self.box_padding_label = ctk.CTkLabel(self.settings_frame, text="Box Padding")
        self.box_padding_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.box_padding_opt = ctk.CTkEntry(self.settings_frame)
        self.box_padding_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.box_padding_opt.insert('end', self.settings["box_padding"])
        self.box_padding_opt.bind("<FocusOut>", lambda e: self.on_box_padding_change())
        self.box_padding_opt.bind("<Return>", lambda e: self.on_box_padding_change())

        ### Maximum characters per line
        n_row += 1
        self.wrap_length_label = ctk.CTkLabel(self.settings_frame, text="Wrap Lenght")
        self.wrap_length_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.wrap_length_opt = ctk.CTkEntry(self.settings_frame)
        self.wrap_length_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")
        self.wrap_length_opt.insert('end', self.settings["wrap_length"])
        self.wrap_length_opt.bind("<FocusOut>", lambda e: self.on_wrap_length_change())
        self.wrap_length_opt.bind("<Return>", lambda e: self.on_wrap_length_change())

        ### Check for updates
        n_row += 2
        self.current_version_label = ctk.CTkLabel(self.settings_frame, text=f"Current Version: {self.VERSION}")
        self.current_version_label.grid(row=n_row, column=0, padx=(10, padx_left_labels), pady=10, sticky="w")

        self.check_update_opt = ctk.CTkButton(self.settings_frame, text="Check For Updates", command=self.CheckUpdates)
        self.check_update_opt.grid(row=n_row, column=1, padx=(padx_right_optiosn, 10), pady=10, sticky="e")


        ## Reset Settings Button
        n_row += 3
        self.settings_frame.grid_rowconfigure(n_row, weight=1)
        self.reset_settings_button = ctk.CTkButton(self.settings_frame,text="Reset Settings" ,command=self.ResetSettings)
        self.reset_settings_button.grid(row=n_row, column=0, columnspan=2, padx=(10, 10), pady=(30, 10), sticky="ew")

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
            self.line_spacing_label.configure(text=self.get_text("line_spacing"))
        except Exception:
            pass

        try:
            self.font_weight_label.configure(text=self.get_text("font_weight"))
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
            self.text_color_opt.configure(text=self.get_text("chose_color"))
        except Exception:
            pass

        try:
            self.box_color_label.configure(text=self.get_text("box_color"))
        except Exception:
            pass

        try:
            self.box_color_opt.configure(text=self.get_text("chose_color"))
        except Exception:
            pass

        try:
            self.text_padding_label.configure(text=self.get_text("text_padding"))
        except Exception:
            pass

        try:
            self.box_padding_label.configure(text=self.get_text("box_padding"))
        except Exception:
            pass

        try:
            self.wrap_length_label.configure(text=self.get_text("wrap_length"))
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

        if not messagebox.askyesno("Confirm Reset", "This will reset all settings to defaults. Continue?"):
            return

        try:
            # Preserve current desktop wallpaper selection (if any)
            current_wallpaper = self.settings.get("desktop_wallpaper")

            # Make a fresh independent copy of defaults
            self.settings = self.default_settings.copy()

            # If user had a custom wallpaper before reset, preserve it
            if current_wallpaper:
                self.settings["desktop_wallpaper"] = current_wallpaper

            # Apply UI values from self.settings (use settings, not default_settings)
            self.change_theme_event(self.settings["Theme"])
            ctk.set_appearance_mode(self.settings["Apperance Mode"])
            ctk.set_widget_scaling(int(self.settings["UI Scaling"].replace("%", "")) / 100)
            self.appearance_mode_optionemenu.set(self.settings["Apperance Mode"])
            self.scaling_optionemenu.set(self.settings["UI Scaling"])
            self.theme_optionemenu.set(self.settings["Theme"])
            self.font_opt.set(self.settings["font"])

            self.font_size_opt.delete(0, "end")
            self.font_size_opt.insert("end", self.settings["font size"])

            self.line_spacing_opt.delete(0, "end")
            self.line_spacing_opt.insert("end", self.settings["line_spacing"])

            self.font_weight_opt.delete(0, "end")
            self.font_weight_opt.insert("end", self.settings["font_weight"])

            self.textbox_font_size_opt.delete(0, "end")
            self.textbox_font_size_opt.insert("end", self.settings["textbox_fontsize"])
            self.textbox.configure(font=ctk.CTkFont(size=int(self.settings["textbox_fontsize"])))

            self.position_opt.set(self.settings["position"])
            self.text_color_label_box.configure(text_color=self.settings["text_color"])
            self.box_color_label_box.configure(text_color=self.settings["box_color"])

            self.text_padding_opt.delete(0, "end")
            self.text_padding_opt.insert("end", self.settings["text_padding"])

            self.box_padding_opt.delete(0, "end")
            self.box_padding_opt.insert("end", self.settings["box_padding"])

            self.wrap_length_opt.delete(0, "end")
            self.wrap_length_opt.insert("end", self.settings["wrap_length"])

            # Update the wallpaper entry widget too
            self.desktop_wallpaper_dir_opt.delete(0, "end")
            self.desktop_wallpaper_dir_opt.insert("end", self.settings["desktop_wallpaper"])

            # Persist the reset settings
            self.save_settings()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")


    ### Updating Settings

    def change_font_event(self, new_font: str):
        self.settings["font"] = new_font
        self.save_settings()

    def on_font_size_change(self):

        val = self.font_size_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            try: v = float(val)
            except ValueError:
                self.font_size_opt.delete(0, "end")
                self.font_size_opt.insert("end", str(self.settings.get("font size", "")))
                messagebox.showerror("Invalid Value", "Font size must be a number.")
                return

        self.settings["font size"] = v
        self.save_settings()

    def on_textbox_font_size_change(self):

        val = self.textbox_font_size_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            try: v = float(val)
            except ValueError:
                self.textbox_font_size_opt.delete(0, "end")
                self.textbox_font_size_opt.insert("end", str(self.settings.get("textbox_fontsize", "")))
                messagebox.showerror("Invalid Value", "Textbox font size must be a number.")
                return

        self.settings["textbox_fontsize"] = v
        self.save_settings()

    def on_line_spacing_change(self):

        val = self.line_spacing_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            try: v = float(val)
            except ValueError:
                self.line_spacing_opt.delete(0, "end")
                self.line_spacing_opt.insert("end", str(self.settings.get("line_spacing", "")))
                messagebox.showerror("Invalid Value", "Line spacing must be a number.")
                return

        self.settings["line_spacing"] = v
        self.save_settings()

    def on_font_weight_change(self):

        val = self.font_weight_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            self.font_weight_opt.delete(0, "end")
            self.font_weight_opt.insert("end", str(self.settings.get("font_weight", "")))
            messagebox.showerror("Invalid Value", "Font weight must be an integer.")
            return

        if v > 5 :
            self.font_weight_opt.delete(0, "end")
            self.font_weight_opt.insert("end", str(self.settings.get("font_weight", "")))
            messagebox.showerror("Invalid Value", "Font weight must be > 5.")
            return

        self.settings["font_weight"] = v
        self.save_settings()

    def change_position_event(self, new_position: str):
        self.settings["position"] = new_position
        self.save_settings()

    def on_text_padding_change(self):

        val = self.text_padding_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            try: v = float(val)
            except ValueError:
                self.text_padding_opt.delete(0, "end")
                self.text_padding_opt.insert("end", str(self.settings.get("text_padding", "")))
                messagebox.showerror("Invalid Value", "Text padding must be a number.")
                return

        self.settings["text_padding"] = v
        self.save_settings()

    def on_box_padding_change(self):

        val = self.box_padding_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            try: v = float(val)
            except ValueError:
                self.box_padding_opt.delete(0, "end")
                self.box_padding_opt.insert("end", str(self.settings.get("box_padding", "")))
                messagebox.showerror("Invalid Value", "Box padding must be a number.")
                return

        self.settings["box_padding"] = v
        self.save_settings()

    def on_wrap_length_change(self):

        val = self.wrap_length_opt.get().strip()

        if val == "":
            return

        try: v = int(val)
        except ValueError:
            self.wrap_length_opt.delete(0, "end")
            self.wrap_length_opt.insert("end", str(self.settings.get("wrap_length", "")))
            messagebox.showerror("Invalid Value", "Wrap length must be an integer between 20 and 200.")
            return

        if v < 20 or v > 200 :
            self.wrap_length_opt.delete(0, "end")
            self.wrap_length_opt.insert("end", str(self.settings.get("wrap_length", "")))
            messagebox.showerror("Invalid Value", "Wrap length must be an integer between 20 and 200.")
            return

        self.settings["wrap_length"] = v
        self.save_settings()

    def choose_text_color(self):
        color = colorchooser.askcolor(initialcolor='white')[1]
        self.text_color_label_box.configure(text_color = color)
        self.settings["text_color"] = color
        self.save_settings()

    def choose_box_color(self):
        color = colorchooser.askcolor(initialcolor='black')[1]
        self.box_color_label_box.configure(text_color = color)
        self.settings["box_color"] = color
        self.save_settings()

    def ChangeWallpaper(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:  # if user selected a file
            self.desktop_wallpaper_dir_opt.delete(0, "end")
            self.desktop_wallpaper_dir_opt.insert('end', file_path)
            self.settings["desktop_wallpaper"] = file_path
        
            img = imread(file_path)
            img_h, img_w = img.shape[:2]
            self.settings["font size"] = int((img_w + img_h)/2 * 0.03/1.333)

            self.font_size_opt.delete(0, "end")
            self.font_size_opt.insert('end',int((img_w + img_h)/2 * 0.03/1.333))
            self.save_settings()

    ### App Functionalties
    
    def Save(self):

        entry = self.textbox.get('0.0','end').strip()

        if entry != "" :

            from PIL_CV2 import MixedMethod
            from functions import text_handler

            MixedMethod(
                text_handler(entry, int(self.wrap_length_opt.get())),
                self.desktop_wallpaper_dir_opt.get(),
                self.position_opt.get(), 
                FontsFinder()[self.font_opt.get()],
                float(self.font_size_opt.get()),
                self.settings["text_color"],
                self.settings["box_color"],
                int(self.box_padding_opt.get()),
                int(self.text_padding_opt.get()),
                float(self.line_spacing_opt.get()),
                int(self.font_weight_opt.get()),
                self.sub_files
                    )

        else: pass

        # Save to the history file
        history = f"{datetime.date.today()}  ({datetime.datetime.now().strftime('%I:%M %p')})\n\n{entry}\n{'='*50}\n"

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


    def CheckUpdates(self):
        try:
            import requests
        except Exception:
            messagebox.showerror("Error", "The 'requests' package is required for update checks.")
            return

        latest_url = "https://github.com/ammelsayed/Desktop-TDL/releases/latest"

        try:
            # Don't follow redirects so we can read the Location header
            response = requests.get(latest_url, allow_redirects=False, timeout=6)
            response.raise_for_status()

            # GitHub will redirect to something like:
            # https://github.com/ammelsayed/Desktop-TDL/releases/tag/v1.0.7
            location = response.headers.get("Location", "")
            if not location or "/tag/" not in location:
                raise RuntimeError("Could not determine latest release tag.")

            latest_tag = location.rsplit("/", 1)[-1].lstrip("v")  # e.g. "1.0.7"
            local_version = tuple(map(int, self.VERSION.split('.')))
            remote_version = tuple(map(int, latest_tag.split('.')))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to check for updates: {e}")
            return

        if remote_version > local_version:
            if messagebox.askyesno("Update Available",
                                f"Latest update available: {latest_tag}. Do you wish to open the releases page?"):
                import webbrowser
                webbrowser.open(latest_url)
        else:
            messagebox.showinfo("Up to Date", f"You are running the latest version: {self.VERSION}")



if __name__ == "__main__":
    app = App()
    app.mainloop()