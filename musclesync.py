import tkinter as tk
import customtkinter
import ctypes
from PIL import Image, ImageTk
from MainFrame import MainFrame
from DashboardFrame import DashboardFrame

ctypes.windll.shcore.SetProcessDpiAwareness(1)
customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("light")

class MuscleSync:
    def __init__(self, root):
        self.root = root
        self.root.title('MuscleSync')
        self.root.iconbitmap('images/logo.ico')

        # App window setup
        self.app_width, self.app_height = 1200, 600
        self.screenwidth, self.screenheight = root.winfo_screenwidth(), root.winfo_screenheight()
        self.x_offset = (self.screenwidth // 2) - (self.app_width // 2)
        self.y_offset = (self.screenheight // 2) - (self.app_height // 2)
        self.root.geometry(f"{self.app_width}x{self.app_height}+{self.x_offset}+{self.y_offset}")
        self.root.resizable(False, False)

        # === Create DashboardFrame (right view)
        self.rightframe = DashboardFrame(master=self.root, controller=self)
        self.rightframe.pack(side="left", fill="both", expand=True)

        # === Create MainFrame (sidebar) WITHOUT graph_frame for now
        self.leftframe = MainFrame(master=self.root)
        self.leftframe.pack(side="left", fill="y")

        # === Link sidebar and main content
        self.leftframe.dashboard_frame = self.rightframe

        # === Now safe to show dashboard view
        self.rightframe.show_dashboard_view()

        # === Once graph_frame is created, init LED system
        self.leftframe.init_led_function(self.rightframe.graph_frame)

        # === Handle graceful exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.rightframe.stop_auto_refresh()
        if self.leftframe.ledfunction:
            self.leftframe.ledfunction.cleanup()
        self.root.update_idletasks()
        self.root.destroy()

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = MuscleSync(root)
    root.mainloop()
