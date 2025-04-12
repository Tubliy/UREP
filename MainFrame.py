import customtkinter
from PIL import Image, ImageTk
from LedFunction import LedFunction
from DashboardFrame import DashboardFrame

class MainFrame(customtkinter.CTkFrame):
    def __init__(self,master,graph_frame, **kwargs):
        super().__init__(master, corner_radius=15,fg_color = "#00D68F", **kwargs)

        self.configure(width=320)
        self.pack_propagate(False)

        # 2. Overlay on top of background
        overlay = customtkinter.CTkFrame(
            master=self,
            corner_radius=15,
            width=200,
            height=350,
            fg_color="#0F172A"
        )
        overlay.place(relx=0.5, rely=0.5, anchor="center",x=-5)
        overlay.pack_propagate(False)

        # 3. Logo
        logo_path = 'images/logo.png'
        self.logoimage = customtkinter.CTkImage(
            light_image=Image.open(logo_path),
            dark_image=Image.open(logo_path),
            size=(100, 100)
        )
        label = customtkinter.CTkLabel(master=overlay, text="", image=self.logoimage)
        label.pack(pady=12)

        button_width = 80
        button_height = 35
        # 4. Buttons

        self.led_buttons = []
        led_png = customtkinter.CTkImage(Image.open('images/led.png'))
        for i in range(3):
            btn = customtkinter.CTkButton(master=overlay,
            text=f"Led {i+1}", 
            image=led_png, 
            compound="left", 
            corner_radius= 10,
            font=('Arial', 14),
            width=button_width,
            height=button_height,
            fg_color="#FF4C4C",
            )
            btn.pack(pady=10)
            self.led_buttons.append(btn)
            
        self.ledfunction = LedFunction(self.led_buttons, graph_frame)

        for i, btn in enumerate(self.led_buttons):
            btn.configure(command=lambda idx=i: self.ledfunction.toggle_led(idx))
        # 5. Mode Switch
        self.modeswitch = customtkinter.CTkSwitch(
            master=overlay,
            text="",
            progress_color="#00D68F",     
            button_color="#FFFFFF",        
            button_hover_color="#CCCCCC",  
            text_color="white", 
            font=("Arial", 14),
            fg_color="#2E2E2E",            
            command=self.toggle_mode
        )
        self.modeswitch.pack(pady=10)

        if customtkinter.get_appearance_mode() == "Dark":
            self.modeswitch.select()
            self.modeswitch.configure(text="Dark Mode")
        else:
            self.modeswitch.deselect()
            self.modeswitch.configure(text="Light Mode")

    def toggle_mode(self):
        if self.modeswitch.get() == 1:
            customtkinter.set_appearance_mode("dark")
            self.modeswitch.configure(text="Dark Mode")
        else:
            customtkinter.set_appearance_mode("light")
            self.modeswitch.configure(text="Light Mode")
    
