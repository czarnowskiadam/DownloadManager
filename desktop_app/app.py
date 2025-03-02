import customtkinter
from PIL import Image
import os
from CTkToolTip import *
from CTkTable import *
import time
from tkinter import filedialog

from backend import downloads_dir, log

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ### APP MAIN SETTINGS ###
        self.geometry("900x600")
        self.title("DownloadManager")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.base_dir, "imgs", "icons", "icon_32.ico")
        self.iconbitmap(self.icon_path)

        self.custom_color_theme = os.path.join(self.base_dir, "custom_style.json")
        customtkinter.set_default_color_theme(self.custom_color_theme)

        customtkinter.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        ### MENU FRAME SETUP ###
        self.frame_menu = customtkinter.CTkFrame(self, width=80)
        self.frame_menu.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.menu_button_fg_color_light = "#dbdbdb"
        self.menu_button_hover_color_light = "#c4c4c4"
        self.menu_button_fg_color_dark = "#2b2b2b"
        self.menu_button_hover_color_dark = "#232323"
        ### light icon color (206, 206, 206)
        ### dark icon color (43, 43, 43)
        
        self.button_home = customtkinter.CTkButton(self.frame_menu,
                                                   height=40,
                                                   width=40,
                                                   text="",
                                                   image=self.set_button_icon("home_light", "home_dark"),
                                                   fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                   hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                   command=lambda: self.show_frame("home"))
        self.button_home.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_home, "HOME", 12)

        self.button_downloads = customtkinter.CTkButton(self.frame_menu,
                                                   height=40,
                                                   width=40,
                                                   text="",
                                                   image=self.set_button_icon("downloads_light", "downloads_dark"),
                                                   fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                   hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                   command=lambda: self.show_frame("downloads"))
        self.button_downloads.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_downloads, "DOWNLOADS", 12)

        self.button_directory = customtkinter.CTkButton(self.frame_menu,
                                                   height=40,
                                                   width=40,
                                                   text="",
                                                   image=self.set_button_icon("directory_light", "directory_dark"),
                                                   fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                   hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                   command=lambda: self.show_frame("directory"))
        self.button_directory.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_directory, "DIRECTORIES", 12)

        self.button_notifications = customtkinter.CTkButton(self.frame_menu,
                                                   height=40,
                                                   width=40,
                                                   text="",
                                                   image=self.set_button_icon("notifications_light", "notifications_dark"),
                                                   fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                   hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                   command=lambda: self.show_frame("notifications"))
        self.button_notifications.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_notifications, "NOTIFICATIONS", 12)

        self.button_logs = customtkinter.CTkButton(self.frame_menu,
                                                   height=40,
                                                   width=40,
                                                   text="",
                                                   image=self.set_button_icon("logs_light", "logs_dark"),
                                                   fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                   hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                   command=lambda: self.show_frame("logs"))
        self.button_logs.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_logs, "LOGS", 12)

        self.button_statistics = customtkinter.CTkButton(self.frame_menu,
                                                   height=40,
                                                   width=40,
                                                   text="",
                                                   image=self.set_button_icon("statistics_light", "statistics_dark"),
                                                   fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                   hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                   command=lambda: self.show_frame("statistics"))
        self.button_statistics.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_statistics, "STATISTICS", 12)

        self.frame_spacer = customtkinter.CTkFrame(self.frame_menu,
                                                   fg_color="transparent",
                                                   width=40,
                                                   height=10)
        self.frame_spacer.pack(expand=True, fill="both")

        self.button_appearance = customtkinter.CTkButton(self.frame_menu,
                                                       height=40,
                                                       width=40,
                                                       text="",
                                                       image=self.set_button_icon("appearance_light", "appearance_dark"),
                                                       fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                       hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                       command=self.change_appearance)
        self.button_appearance.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_appearance, "THEME MODE", 12)

        self.button_settings = customtkinter.CTkButton(self.frame_menu,
                                                       height=40,
                                                       width=40,
                                                       text="",
                                                       image=self.set_button_icon("settings_light", "settings_dark"),
                                                       fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                       hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                       command=lambda: self.show_frame("settings"))
        self.button_settings.pack(pady=5, padx=10, fill="x")
        self.add_tooltip(self.button_settings, "SETTINGS", 12)

        ### CONTENT FRAME SETUP ###
        self.frame_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.content_frame_font_big = ("Humanst521 BT", 24)
        self.content_frame_font_medium = ("Humanst521 BT", 20)
        self.content_frame_font_small = ("Humanst521 BT", 16)
        self.content_frame_font_mini = ("Humanst521 BT", 14)

        self.current_frame = None
        self.after_id = None

        self.show_frame("downloads")

    def horizontal_separator(self, master, height=2, padx=30, pady=10):
        separator = customtkinter.CTkFrame(master,
                                           height=height,
                                           fg_color=(self.menu_button_fg_color_dark, self.menu_button_fg_color_light))
        separator.pack(fill="x", padx=padx, pady=pady)

    def update_time(self, label):
        """Aktualizuje czas co sekundę"""
        current_time = time.strftime("%H:%M:%S")  
        current_date = time.strftime("%d.%m.%Y")  
        current_day = time.strftime("%A") 

        label.configure(text=f"{current_day}, {current_date}\n{current_time}")

        self.after_id = self.after(1000, lambda: self.update_time(label))

    def create_home_frame(self):
        """Tworzy stronę główną"""
        frame = customtkinter.CTkFrame(self.frame_content)

        title_img_path = Image.open(os.path.join(self.base_dir, "imgs", "img", "icon_256.png"))
        title_img = customtkinter.CTkImage(light_image=title_img_path, dark_image=title_img_path, size=(32, 32))
        logo_label = customtkinter.CTkLabel(frame, 
                                       text="DownloadManager  ",
                                       image=title_img,
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
                                       image=self.set_button_icon("downloads_light", "downloads_dark"),
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

        info_button = customtkinter.CTkButton(current_download_directory_frame,
                                              width=30,
                                              height=30,
                                              image=self.set_button_icon("info_light", "info_dark", 24),
                                              text="",
                                              fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                              hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                              command=self.show_info,
                                              anchor="e")
        info_button.pack(side="right", padx=(5, 5))
        self.add_tooltip(info_button, "INFORMATION", 10)

        select_button = customtkinter.CTkButton(current_download_directory_frame,
                                                width=30,
                                                height=30,
                                                image=self.set_button_icon("choose_dir_light", "choose_dir_dark", 24),
                                                text="",
                                                fg_color=(self.menu_button_fg_color_light, self.menu_button_fg_color_dark),
                                                hover_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                                                command=lambda: self.select_directory(current_directory_path),
                                                anchor="e")
        select_button.pack(side="right", padx=(5, 0))
        self.add_tooltip(select_button, "SELECT DIRECTORY", 10)

        #self.horizontal_separator(frame, pady=(0, 10))

        downloads_dir_files_frame = customtkinter.CTkFrame(frame,
                                                           fg_color="transparent")
        downloads_dir_files_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        scrollable_files_frame = customtkinter.CTkFrame(downloads_dir_files_frame,
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        border_color=(self.menu_button_fg_color_dark, self.menu_button_fg_color_light))
        scrollable_files_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=0)

        action_buttons_frame = customtkinter.CTkFrame(downloads_dir_files_frame,
                                                      width=50,
                                                      fg_color="transparent",
                                                      border_width=2,
                                                      border_color=(self.menu_button_fg_color_dark, self.menu_button_fg_color_light))
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
    
    def select_directory(self, directory_path):
        directory = filedialog.askdirectory()
        if directory:
            directory_path.set(directory)

    def show_info(self):
        customtkinter.CTkMessagebox(title="Informacja", message="Tutaj możesz wybrać folder docelowy.")

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
    
    def add_tooltip(self, widget, text, font_size):
        tooltip_font = ("Humanst521 BT", font_size, "bold")
        CTkToolTip(widget,
                    delay=0.01,
                    message=text,
                    fg_color=(self.menu_button_hover_color_dark, self.menu_button_hover_color_light),
                    bg_color=(self.menu_button_hover_color_dark, self.menu_button_hover_color_light),
                    text_color=(self.menu_button_hover_color_light, self.menu_button_hover_color_dark),
                    font=tooltip_font,
                    corner_radius=5)

    def show_frame(self, name):
        if self.current_frame:
            self.current_frame.destroy()

        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        if name == "home":
            self.current_frame = self.create_home_frame()
        elif name == "settings":
            self.current_frame = self.create_settings_frame()
        elif name == "statistics":
            self.current_frame = self.create_statistics_frame()
        elif name == "downloads":
            self.current_frame = self.create_downloads_frame()
        elif name == "notifications":
            self.current_frame = self.create_notifications_frame()
        elif name == "directory":
            self.current_frame = self.create_directory_frame()
        elif name == "logs":
            self.current_frame = self.create_logs_frame()

        self.current_frame.pack(fill="both", expand=True)

    def change_appearance(self):
        current_mode = customtkinter.get_appearance_mode()
        if current_mode == "Dark":
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")

    def set_button_icon(self, light_icon_name, dark_icon_name, icon_size=32):
        light_icon = Image.open(os.path.join(self.base_dir, "imgs", "button_icons", f"{light_icon_name}.png"))
        dark_icon = Image.open(os.path.join(self.base_dir, "imgs", "button_icons", f"{dark_icon_name}.png"))
        icon_image = customtkinter.CTkImage(light_image=dark_icon, dark_image=light_icon, size=(icon_size, icon_size))

        return icon_image

# Uruchomienie aplikacji
if __name__ == "__main__":
    app = App()
    app.mainloop()
