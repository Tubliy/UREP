import customtkinter
import winsound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from TimerFunction import TimerFunction
from DataProcess import DataProcess
from SerialFunction import SerialFunction


class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master,**kwargs)
        self.configure(width=500)
        self.pack_propagate(False)
        
        self.data = DataProcess(parent=self)
        
        # Timer frame
        timer_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        timer_frame.pack(fill="both", pady=10, side="bottom")
        self.timer_label = customtkinter.CTkLabel(master=timer_frame, text="Timer: 0:00", font=("Arial",30))
        self.timer = TimerFunction(parent=self, timer_label = self.timer_label)
        self.timer_label.pack(pady=10, anchor="center")
        
            
        # Button frame
        self.button_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.button_frame.pack(anchor="n",pady=20)

        # Port dropdown box
        self.noactive = "No active ports."
        self.selectporttext = "Select Port"
        self.serialfunction = SerialFunction(parent=self)
        self.port_list = self.serialfunction.available_ports
        if not self.port_list:
            self.port_list = [self.noactive]
            self.port_var = customtkinter.StringVar(value="No active ports.")
        else:
            self.port_var = customtkinter.StringVar(value=self.selectporttext)
            
        self.select_port = customtkinter.CTkComboBox(master=self.button_frame,
        values=self.port_list,
        variable=self.port_var)
        self.select_port.grid(row=0, column=0, padx=5, pady=10)
        
        self.auto_refresh_ports()
        
        connect_button = customtkinter.CTkButton(
         master= self.button_frame,
         text="Connect",
         command = self.connect_button_clicked
        )
        connect_button.grid(row=0, column=1, padx=5, pady=10)
        
        disconnect_button = customtkinter.CTkButton(master=self.button_frame,
        text="Disconnect",
        command=self.disconnect_button_clicked)
        disconnect_button.grid(row=0, column=2, padx=5, pady=10)
        
        self.connection_label = customtkinter.CTkLabel(master=self.button_frame, 
        text= "Disconnected:")
        self.connection_label.grid(row=0, column=3,padx=(20,0), pady=10)
        
        self.connection_display = customtkinter.CTkProgressBar(master=self.button_frame,
        width = 40,
        progress_color="#FF0000")
        self.connection_display.set(0)
        self.connection_display.grid(row = 0, column = 4,padx=(0,10), pady=10)
        
        # Buttons (Start,Stop,Reset, and Export)
        start_button = customtkinter.CTkButton(
            master=self.button_frame,
            text="Start",
            command = self.timer.start
            
        )
        start_button.grid(row=1, column=0, padx=5, pady=10)
        stop_button = customtkinter.CTkButton(
            master=self.button_frame,
            text="Stop",
            command = self.timer.stop
        )
        stop_button.grid(row=1, column=1, padx=5, pady=10)
        
        reset_button = customtkinter.CTkButton(
            master=self.button_frame,
            text="Reset",
            command = self.timer.reset
        )
        reset_button.grid(row=1, column=2, padx=5, pady=10)
        
        export_button = customtkinter.CTkButton(
            master=self.button_frame,
            text="Export",
            command=self.data.export
        )
        export_button.grid(row=1,column=3, padx=5, pady=10)
        
        # Graph frame
        self.graph_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.graph_frame.pack(fill="x", expand=True, pady=10)
        
    
    def connect_button_clicked(self):
     self.ser = self.serialfunction.try_connect(self.port_var.get())
     if self.serialfunction.connected:
        winsound.PlaySound("sounds/orb.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.connection_label.configure(text="Connected:")
        self.connection_display.configure(progress_color="#00D68F")
        self.connection_display.set(1.0)
        
     else:
         self.connection_display.set(0)
    
    def disconnect_button_clicked(self):
        success = self.serialfunction.disconnect_serial()
        if success:
            winsound.PlaySound("sounds/hit.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.connection_display.configure(progress_color="#FF0000")
            self.connection_label.configure(text="Disconnected")
            self.port_var.set("Select Port")
            self.connection_display.set(0)
    
    def auto_refresh_ports(self):
        ports = self.serialfunction.get_ports()
        current_ports = self.select_port.cget("values")

        if ports != list(current_ports):
            if not ports:
             ports = [self.noactive]
             self.port_var.set(self.noactive)
            else:
                self.port_var.set(self.selectporttext)
        self.select_port.configure(values=ports)
        
        self.after_id = self.after(3000, self.auto_refresh_ports)  
        
    def stop_auto_refresh(self):
        if hasattr(self, "after_id"):
            self.after_cancel(self.after_id)

    
    