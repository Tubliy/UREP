import customtkinter 
from PIL import Image, ImageTk
import winsound

class Popups(customtkinter.CTkToplevel):
    def __init__(self,parent,message, type="info"):
        super().__init__(parent)
        self.title("Notice")
        popup_width = 300
        popup_height = 170
        self.resizable(False,False)
        self.grab_set()
        
        parent.update_idletasks()
    
        
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (popup_width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (popup_height // 2)
        
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        self.setimage = None
        
        
        if type == "error":
            error_image = customtkinter.CTkImage(Image.open("images/error.png"), size = (50,50))
            self.setimage = error_image
            winsound.MessageBeep(winsound.MB_ICONHAND)
        elif type == "success":
            success_image = customtkinter.CTkImage(Image.open("images/success.png"), size = (50,50))
            self.setimage = success_image
        else:
            self.setimage = None
            
        if self.setimage:
            self.imagelabel = customtkinter.CTkLabel(self, text= "", image = self.setimage)
            self.imagelabel.pack(pady=10)
        
        
        self.label = customtkinter.CTkLabel(self, text=message, font=("Arial",10))
        self.label.pack(pady=10)
        
        closebutton = customtkinter.CTkButton(master=self,
        text = "Close",
        corner_radius= 15,
        command=self.destroy,
        fg_color="#FF4C4C")
        closebutton.pack(pady=10)
    
        self.after(3000, self.destroy)
    
    
    