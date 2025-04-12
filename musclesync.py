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
    def __init__(self,root):
        self.root = root
        self.root.title('MuscleSync')
        self.root.iconbitmap('images/logo.ico')
        
        
        self.app_width, self.app_height = 1200,600
        self.screenwidth, self.screenheight = root.winfo_screenwidth(), root.winfo_screenheight()
        self.x_offset = (self.screenwidth // 2) - (self.app_width // 2)
        self.y_offset = (self.screenheight // 2) - (self.app_height // 2)
        self.root.geometry(f"{self.app_width}x{self.app_height}+{self.x_offset}+{self.y_offset}")
        self.root.resizable(False, False)
    
        self.rightframe = DashboardFrame(master=self.root)
        self.rightframe.pack(side="left", fill = "both", expand = True)
        
        self.leftframe = MainFrame(master=self.root, graph_frame=self.rightframe.graph_frame)
        self.leftframe.pack(side="left", fill = "y")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
   
    def on_closing(self):
        self.rightframe.stop_auto_refresh()  
        self.leftframe.ledfunction.cleanup()
        self.root.update_idletasks()
        self.root.destroy()

    
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = MuscleSync(root)
    root.mainloop()
