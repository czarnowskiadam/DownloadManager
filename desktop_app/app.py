import customtkinter
from PIL import Image
import os
from CTkToolTip import *
from CTkTable import *
import time
from tkinter import filedialog

from backend import downloads_dir, log

base_dir = os.path.dirname(os.path.abspath(__file__))

button_fg_color_light = "#dbdbdb"
button_hover_color_light = "#c4c4c4"
button_fg_color_dark = "#2b2b2b"
button_hover_color_dark = "#232323"
### light icon color (206, 206, 206)
### dark icon color (43, 43, 43)

class Button(customtkinter.CTkButton):
    def __init__(self,
                 master=None,
                 height=40,
                 width=40,
                 fg_color=None,
                 hover_color=None,
                 button_text="",
                 light_icon_name=None,
                 dark_icon_name=None,
                 icon_size=32,
                 tooltip_text=None,
                 tooltip_font_size=12,
                 command=None,
                 **kwargs):
        
        if fg_color is None:
            fg_color = (button_fg_color_light, button_fg_color_dark)
        if hover_color is None:
            hover_color = (button_hover_color_light, button_hover_color_dark)
         
        self.icon_image = self.set_button_icon(light_icon_name, dark_icon_name, icon_size)
        
        super().__init__(master,
                         height=height,
                         width=width,
                         fg_color=fg_color,
                         hover_color=hover_color,
                         text=button_text,
                         image=self.icon_image,
                         command=command,
                         **kwargs)

        if tooltip_text:
            self.add_tooltip(tooltip_text, tooltip_font_size)
        else:
            log.write_debug("No tooltip text set")

    def add_tooltip(self,
                    tooltip_text,
                    tooltip_font_size,
                    tooltip_fg_bg_color=(button_hover_color_dark, button_hover_color_light),
                    tooltip_text_color=(button_hover_color_light, button_hover_color_dark)):
        CTkToolTip(self,
                    delay=0.01,
                    message=tooltip_text,
                    fg_color=tooltip_fg_bg_color,
                    bg_color=tooltip_fg_bg_color,
                    text_color=tooltip_text_color,
                    font=("Humanst521 BT", tooltip_font_size, "bold"),
                    corner_radius=5)
        
    def set_button_icon(self, light_icon_name, dark_icon_name, icon_size):

        if not light_icon_name or not dark_icon_name:
            return None

        if bool(light_icon_name) != bool(dark_icon_name):  
            log.write_debug("Both light and dark icons must be provided together, or none at all")
            return None  

        light_icon_path = os.path.join(base_dir, "imgs", "button_icons", f"{light_icon_name}.png")
        dark_icon_path = os.path.join(base_dir, "imgs", "button_icons", f"{dark_icon_name}.png")

        if not os.path.exists(light_icon_path):
            log.write_debug(f"The button icon file '{light_icon_name}' does not exist")
            return None
        elif not os.path.exists(dark_icon_path):
            log.write_debug(f"The button icon file '{dark_icon_name}' does not exist")
            return None       
        

        light_icon = Image.open(light_icon_path)
        dark_icon = Image.open(dark_icon_path)
        icon_image = customtkinter.CTkImage(light_image=dark_icon, dark_image=light_icon, size=(icon_size, icon_size))

        return icon_image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ### APP MAIN SETTINGS ###
        self.geometry("900x600")
        self.title("DownloadManager")

        
        self.icon_path = os.path.join(base_dir, "imgs", "icons_ico", "icon_32.ico")
        self.iconbitmap(self.icon_path)

        self.custom_color_theme = os.path.join(base_dir, "custom_style.json")
        customtkinter.set_default_color_theme(self.custom_color_theme)

        customtkinter.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        ### MENU FRAME SETUP ###
        self.frame_menu = customtkinter.CTkFrame(self, width=80)
        self.frame_menu.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.setup_menu_buttons()

        ### CONTENT FRAME SETUP ###
        self.frame_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.content_frame_font_big = ("Humanst521 BT", 24)
        self.content_frame_font_medium = ("Humanst521 BT", 20)
        self.content_frame_font_small = ("Humanst521 BT", 16)
        self.content_frame_font_mini = ("Humanst521 BT", 14)

        self.current_frame = None
        self.current_frame_name = None
        self.after_id = None

        self.show_frame("downloads")

    def setup_menu_buttons(self):
        menu_buttons = [
            ("home", "HOME", lambda: self.show_frame("home")),
            ("downloads", "DOWNLOADS", lambda: self.show_frame("downloads")),
            ("directory", "DIRECTORIES", lambda: self.show_frame("directory")),
            ("notifications", "NOTIFICATIONS", lambda: self.show_frame("notifications")),
            ("logs", "LOGS", lambda: self.show_frame("logs")),
            ("statistics", "STATISTICS", lambda: self.show_frame("statistics")),

            ### Last two of buttons are placed on the bottom of the menu
            ("appearance", "THEME MODE", self.change_appearance),
            ("settings", "SETTINGS", lambda: self.show_frame("settings"))
        ]

        for icon, tooltip, command in menu_buttons[:-2]:
            Button(self.frame_menu,
                light_icon_name=f"{icon}_light",
                dark_icon_name=f"{icon}_dark",
                tooltip_text=tooltip,
                command=lambda name=icon: self.show_frame(name)).pack(pady=5, padx=10, fill="x")

        self.frame_spacer = customtkinter.CTkFrame(self.frame_menu, fg_color="transparent", width=40, height=10)
        self.frame_spacer.pack(expand=True, fill="both")

        for icon, tooltip, command in menu_buttons[-2:]:  # Dodanie 'appearance' i 'settings'
            Button(self.frame_menu,
                light_icon_name=f"{icon}_light",
                dark_icon_name=f"{icon}_dark",
                tooltip_text=tooltip,
                command=command).pack(pady=5, padx=10, fill="x")

    def horizontal_separator(self, master, height=2, padx=30, pady=10):
        separator = customtkinter.CTkFrame(master,
                                           height=height,
                                           fg_color=(button_fg_color_dark, button_fg_color_light))
        separator.pack(fill="x", padx=padx, pady=pady)

    def create_home_frame(self):
        """Tworzy stronę główną"""
        frame = customtkinter.CTkFrame(self.frame_content)


        logo_label = customtkinter.CTkLabel(frame, 
                                       text="DownloadManager  ",
                                       image=self.set_png_icon(icons_directory="icons_png", color_icon_name="icon_256"),
                                       compound="right", 
                                       font=self.content_frame_font_big)
        logo_label.pack(pady=(20, 0), padx=20)
        desription_text = customtkinter.CTkLabel(frame, 
                                       text="Make managing your download automatic!",
                                       font=self.content_frame_font_medium)
        desription_text.pack(pady=(10, 0), padx=20)

        time_label = customtkinter.CTkLabel(frame, 
                                            font=self.content_frame_font_medium)
        time_label.pack(pady=10)
        self.update_time(time_label)
        
        self.horizontal_separator(frame)

        
        
        return frame
    
    def create_statistics_frame(self):
        """Tworzy widok statystyk"""
        frame = customtkinter.CTkFrame(self.frame_content)
        label = customtkinter.CTkLabel(frame, text="⚙️ Statystyki", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        return frame
    
    def create_downloads_frame(self):
        """Tworzy widok downloads"""
        frame = customtkinter.CTkFrame(self.frame_content)          

        title_label = customtkinter.CTkLabel(frame,
                                       text="Downloads  ",
                                       image=self.set_png_icon(icons_directory="button_icons",light_icon_name="downloads_light", dark_icon_name="downloads_dark"),
                                       compound="right",
                                       font=self.content_frame_font_big)
        title_label.pack(pady=(20, 0), padx=20)

        desription_text = customtkinter.CTkLabel(frame, 
                                       text="Default Downloads directory",
                                       font=self.content_frame_font_medium)
        desription_text.pack(pady=(10, 0), padx=20)

        self.horizontal_separator(frame, pady=(10, 0))

        current_download_directory_frame = customtkinter.CTkFrame(frame,
                                                                  fg_color="transparent",
                                                                  height=50)
        current_download_directory_frame.pack(fill="x", padx=30, pady=10)

        dir = downloads_dir.get_path_to_downloads_directory() if downloads_dir.get_path_to_downloads_directory() is not None else "-"
        current_directory_path = customtkinter.StringVar(value=dir)

        dir_label = customtkinter.CTkLabel(current_download_directory_frame,
                                           text="Downloads directory:",
                                           font=self.content_frame_font_mini,
                                           anchor="w")
        dir_label.pack(side="left", padx=10)

        current_dir_label = customtkinter.CTkLabel(current_download_directory_frame,
                                                   textvariable=current_directory_path,
                                                   font=self.content_frame_font_mini,
                                                   anchor="w")
        current_dir_label.pack(side="left", padx=10)

        info_button = Button(current_download_directory_frame,
                            width=25,
                            height=25,
                            light_icon_name="info_light",
                            dark_icon_name="info_dark",
                            tooltip_text="INFORMATION",
                            command=self.show_info)
        info_button.pack(side="right", padx=(5, 2))

        select_button = Button(current_download_directory_frame,
                                width=25,
                                height=25,
                                light_icon_name="select_dir_light",
                                dark_icon_name="select_dir_dark",
                                tooltip_text="SELECT DIRECTORY",
                                command=lambda: self.select_directory(current_directory_path))
        select_button.pack(side="right", padx=(5, 0))

        downloads_dir_files_frame = customtkinter.CTkFrame(frame,
                                                           fg_color="transparent")
        downloads_dir_files_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        scrollable_files_frame = customtkinter.CTkFrame(downloads_dir_files_frame,
                                                        fg_color="transparent")
        scrollable_files_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=0)

        action_buttons_frame = customtkinter.CTkFrame(downloads_dir_files_frame,
                                                      width=50,
                                                      fg_color="transparent")
        action_buttons_frame.pack(side="right", fill="both", padx=0, pady=0)

        value = [[1,2,3,4],
                [1,2,3,4],
                [1,2,3,4],
                [1,2,3,4],
                [1,2,3,4]]

        table = CTkTable(master=scrollable_files_frame,
                         row=5,
                         column=4,
                         values=value,
                         width=50,
                         colors=["black", "grey"],
                         header_color="red",
                         corner_radius=0)
        table.pack(fill="both", expand=True, padx=5, pady=5)


        return frame

    def create_directory_frame(self):
        """Tworzy widok downloads"""
        frame = customtkinter.CTkFrame(self.frame_content)
        label = customtkinter.CTkLabel(frame, text="⚙️ Directories", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        return frame

    def create_notifications_frame(self):
        """Tworzy widok downloads"""
        frame = customtkinter.CTkFrame(self.frame_content)
        label = customtkinter.CTkLabel(frame, text="⚙️ Notifications", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        return frame

    def create_logs_frame(self):
        """Tworzy widok downloads"""
        frame = customtkinter.CTkFrame(self.frame_content)
        label = customtkinter.CTkLabel(frame, text="⚙️ Logs", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        return frame

    def create_settings_frame(self):
        """Tworzy widok ustawień"""
        frame = customtkinter.CTkFrame(self.frame_content)
        label = customtkinter.CTkLabel(frame, text="⚙️ Ustawienia", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        return frame

    def show_frame(self, name):
        if self.current_frame_name == name:
            return  

        if self.current_frame:
            self.current_frame.destroy()

        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        frame_creators = {
            "home": self.create_home_frame,
            "settings": self.create_settings_frame,
            "statistics": self.create_statistics_frame,
            "downloads": self.create_downloads_frame,
            "notifications": self.create_notifications_frame,
            "directory": self.create_directory_frame,
            "logs": self.create_logs_frame
        }

        self.current_frame = frame_creators.get(name, lambda: log.write_debug(f"'{name}' window cannot be found"))()
        
        if self.current_frame:
            self.current_frame.pack(fill="both", expand=True)
            self.current_frame_name = name

    def change_appearance(self):
        current_mode = customtkinter.get_appearance_mode()
        if current_mode == "Dark":
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")

    def update_time(self, label):
        """Aktualizuje czas co sekundę"""
        current_time = time.strftime("%H:%M:%S")  
        current_date = time.strftime("%d.%m.%Y")  
        current_day = time.strftime("%A") 

        label.configure(text=f"{current_day}, {current_date}\n{current_time}")

        self.after_id = self.after(1000, lambda: self.update_time(label))

    def set_png_icon(self,
                     icons_directory=None,
                     color_icon_name=None,
                     light_icon_name=None,
                     dark_icon_name=None,
                     icon_size=32):
        
        if not icons_directory:
            log.write_debug("Icon directory name was not set")
            return None

        def load_icon(name):
            path = os.path.join(base_dir, "imgs", icons_directory, f"{name}.png") if name else None
            return Image.open(path) if path and os.path.exists(path) else None

        if color_icon_name and (light_icon_name or dark_icon_name):
            log.write_debug("Color and light/dark icons cannot be specified at the same time")
            return None

        color_icon = load_icon(color_icon_name)
        light_icon = load_icon(light_icon_name)
        dark_icon = load_icon(dark_icon_name)

        if color_icon:
            return customtkinter.CTkImage(light_image=color_icon, dark_image=color_icon, size=(icon_size, icon_size))

        if not light_icon or not dark_icon:
            log.write_debug("One of the PNG icons is missing")
            return None

        return customtkinter.CTkImage(light_image=dark_icon, dark_image=light_icon, size=(icon_size, icon_size))

    def select_directory(self, directory_path):
        directory = filedialog.askdirectory()
        if directory:
            directory_path.set(directory)

    def show_info(self):
        customtkinter.CTkMessagebox(title="Informacja", message="Tutaj możesz wybrać folder docelowy.")



# Uruchomienie aplikacji
if __name__ == "__main__":
    app = App()
    app.mainloop()
