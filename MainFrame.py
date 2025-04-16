import customtkinter
from PIL import Image, ImageTk
from LedFunction import LedFunction

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, graph_frame=None, **kwargs):
        super().__init__(master, **kwargs)

        self.graph_frame = graph_frame  # Will be set later if not passed
        self.ledfunction = None
        self.dashboard_frame = None

        self.configure(fg_color="#00D68F", width=320)
        self.pack_propagate(False)

    
        
        # === Logo ===
        logo_path = 'images/logo.png'
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(logo_path),
                                                 dark_image=Image.open(logo_path),
                                                 size=(100, 100))
        logo_label = customtkinter.CTkLabel(master=self, text="", image=self.logo_image)
        logo_label.pack(pady=20)

        # === Overlay container ===
        overlay = customtkinter.CTkFrame(master=self, corner_radius=15, width=200, height=320, fg_color="#0F172A")
        overlay.pack(pady=10)
        overlay.pack_propagate(False)

        # === LED Buttons ===
        self.led_buttons = []
        led_png = customtkinter.CTkImage(Image.open('images/led.png'))

        for i in range(3):
            led_button = customtkinter.CTkButton(
                master=overlay,
                text=f"Led {i+1}",
                image=led_png,
                compound="left",
                corner_radius=10,
                font=('Arial', 14),
                width=80,
                height=35,
                fg_color="#FF4C4C"
            )
            led_button.pack(pady=(10 if i > 0 else 15, 0))
            self.led_buttons.append(led_button)

        # ✅ Assign toggle commands (will link to LedFunction once it's ready)
        for i, btn in enumerate(self.led_buttons):
            btn.configure(command=lambda idx=i: self.toggle_led_graph(idx))

        # === Settings Button ===
        settings_png = customtkinter.CTkImage(Image.open('images/settings.png'))
        self.settings_button = customtkinter.CTkButton(
            master=overlay,
            text="Settings",
            image=settings_png,
            compound="left",
            corner_radius=10,
            width=80,
            height=35,
            command=self.open_settings
        )
        self.settings_button.pack(pady=20)

        # === Light/Dark Mode Switch ===
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

    def open_settings(self):
        if self.dashboard_frame:
            self.dashboard_frame.settings_clicked()

    def toggle_mode(self):
        if self.modeswitch.get() == 1:
            customtkinter.set_appearance_mode("dark")
            self.modeswitch.configure(text="Dark Mode")
        else:
            customtkinter.set_appearance_mode("light")
            self.modeswitch.configure(text="Light Mode")

    def init_led_function(self, graph_frame):
        """Call this once DashboardFrame has created the graph_frame."""
        self.graph_frame = graph_frame
        self.ledfunction = LedFunction(self.led_buttons, self.graph_frame)

    def toggle_led_graph(self, index):
        """Safe toggle handler that waits for LedFunction to be ready."""
        if self.ledfunction:
            self.ledfunction.toggle_led(index)

    def init_led_function(self, graph_frame):
        if self.ledfunction:
         self.ledfunction.cleanup()
        self.graph_frame = graph_frame
        self.ledfunction = LedFunction(self.led_buttons, self.graph_frame)
