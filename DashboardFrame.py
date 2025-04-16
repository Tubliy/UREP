import customtkinter
from PIL import Image, ImageTk
from TimerFunction import TimerFunction
from DataProcess import DataProcess
from SerialFunction import SerialFunction
from LedFunction import LedFunction
from User import User
import winsound
from Popups import Popups
import os
import datetime

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(width=500)
        self.pack_propagate(False)
        
        self.directory = os.path.join(os.path.dirname(__file__), "files")
        
        

        self.content_area = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True)

        self.ledfunction = None  # placeholder
        self.timer = None  # placeholder
        self.sound_enabled = True

        

    def show_dashboard_view(self):
        # Stop timer if returning from settings
        if self.timer and self.timer.running:
            self.timer.stop()

        # Destroy old widgets
        for widget in self.content_area.winfo_children():
            widget.destroy()

        self.data = DataProcess(parent=self)

        # === Timer Section ===
        timer_frame = customtkinter.CTkFrame(master=self.content_area, fg_color="transparent")
        timer_frame.pack(side="top",fill="both", pady=10)

        self.timer_label = customtkinter.CTkLabel(master=timer_frame, text="Timer: 0:00", font=("Arial", 30))

    

        time_label = customtkinter.CTkLabel(master=timer_frame,
        text="Time:",
        font=("Arial",14))
        time_label.grid(row=0, column=0, padx=(10,5), pady=10, sticky="e")
        
       
        self.time_input = customtkinter.CTkEntry(master=timer_frame,
        placeholder_text="e.g. 3:00",
        font=("Arial",14))
        self.time_input.grid(row=0, column=1, padx=5, pady=10)
       
        plan_label = customtkinter.CTkLabel(master=timer_frame,
        text="Exercise Plan:",
        font=("Arial",14))
        plan_label.grid(row=1,column=0,padx=(10,5),pady=10, sticky="e")

        self.plan_input = customtkinter.CTkEntry(master=timer_frame,
        width=150,
        placeholder_text="e.g. Pushups",
        font=("Arial",14))
        self.plan_input.grid(row=1,column=1,padx=5, pady=10)
        
        interval_label = customtkinter.CTkLabel(master=timer_frame,
        text="Interval:",
        font=("Arial",14))
        interval_label.grid(row=2, column=0, padx=(10,5), pady=10, sticky="e")
        
        self.interval_input = customtkinter.CTkEntry(master=timer_frame,
        placeholder_text="e.g. 60s",
        font=("Arial",14))
        self.interval_input.grid(row=2, column=1, padx=5, pady=10)
        
        self.submit_button = customtkinter.CTkButton(master=timer_frame,
        text="Submit",
        command=self.write_file
        )
        self.submit_button.grid(row=2, column=2, padx=5, pady=10)
        
        self.exercise_pick = customtkinter.CTkComboBox(master=timer_frame,
        command=self.load_selected_file,
        values=[])
        
        self.exercise_pick.set(" Choose Exercise")
        self.exercise_pick.grid(row=1, column=2, padx=5, pady=10)
        
        self.timer = TimerFunction(
            parent=self,
            timer_label=self.timer_label
        )

        self.timer_label.grid(row=0, column=5, padx=5, pady=10)


        # === Serial/Port Section ===
        self.button_frame = customtkinter.CTkFrame(master=self.content_area, fg_color="transparent")
        self.button_frame.pack(side="bottom", pady=20)

        self.serialfunction = SerialFunction(parent=self)
        self.noactive = "No active ports."
        self.selectporttext = "Select Port"
        self.port_list = self.serialfunction.available_ports

        self.port_var = customtkinter.StringVar(value=self.port_list[0] if self.port_list else self.noactive)
        if not self.port_list:
            self.port_list = [self.noactive]

        self.select_port = customtkinter.CTkComboBox(master=self.button_frame, values=self.port_list, variable=self.port_var)
        self.select_port.grid(row=0, column=0, padx=5, pady=10)

        self.auto_refresh_ports()

        customtkinter.CTkButton(self.button_frame, text="Connect", command=self.connect_button_clicked).grid(row=0, column=1, padx=5, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Disconnect", command=self.disconnect_button_clicked).grid(row=0, column=2, padx=5, pady=10)

        self.connection_label = customtkinter.CTkLabel(master=self.button_frame, text="Disconnected:")
        self.connection_label.grid(row=0, column=3, padx=(20, 0), pady=10)

        self.connection_display = customtkinter.CTkProgressBar(master=self.button_frame, width=40, progress_color="#FF0000")
        self.connection_display.set(0)
        self.connection_display.grid(row=0, column=4, padx=(0, 10), pady=10)

        customtkinter.CTkButton(self.button_frame, text="Start", command=self.start_timer_and_open_user).grid(row=1, column=0, padx=5, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Stop", command=self.timer.stop).grid(row=1, column=1, padx=5, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Reset", command=self.timer.reset).grid(row=1, column=2, padx=5, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Export", command=self.data.export).grid(row=1, column=3, padx=5, pady=10)

        # === Graph Area ===
        self.graph_frame = customtkinter.CTkFrame(master=self.content_area, fg_color="transparent")
        self.graph_frame.pack(fill="x", expand=True, pady=10)
        

        # === Reinitialize LED Function ===
        if self.ledfunction:
            self.ledfunction.cleanup()

       # === After creating self.graph_frame ===
        if hasattr(self.controller, "leftframe") and self.controller.leftframe:
            self.controller.leftframe.init_led_function(self.graph_frame)
            
        self.update_file_list()


    def show_settings_view(self):
        self.stop_auto_refresh()
        if self.timer and self.timer.running:
            self.timer.stop()

        for widget in self.content_area.winfo_children():
            widget.destroy()

        settings_label = customtkinter.CTkLabel(self.content_area, text="Settings Page", font=("Arial", 24))
        settings_label.grid(row=0, column=1, padx=10, pady=10)

        
        backbuttonpng = customtkinter.CTkImage(Image.open('images/backarrow.png'))
        back_button = customtkinter.CTkButton(
            master=self.content_area,
            text="Back to Dashboard",
            image=backbuttonpng,
            command=self.show_dashboard_view
        )
        back_button.grid(row=0, column=0, padx=10, pady=10)
        
        current_text = "Sound: Off" if not self.sound_enabled else "Sound: On"
        self.sound_button = customtkinter.CTkButton(master=self.content_area,
        text=current_text,
        command=self.no_sound)
        self.sound_button.grid(row=1, column=2, padx=10, pady=10)
        
        
        
    def connect_button_clicked(self):
        self.ser = self.serialfunction.try_connect(self.port_var.get())
        if self.serialfunction.connected:
             if self.sound_enabled:
                 winsound.PlaySound("sounds/orb.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                
             self.connection_label.configure(text="Connected:")
             self.connection_display.configure(progress_color="#00D68F")
             self.connection_display.set(1.0)
        else:
            self.connection_display.set(0)

    def disconnect_button_clicked(self):
        if self.serialfunction.disconnect_serial():
            if self.sound_enabled:
                winsound.PlaySound("sounds/hit.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.connection_label.configure(text="Disconnected")
            self.connection_display.configure(progress_color="#FF0000")
            self.connection_display.set(0)
            self.port_var.set(self.selectporttext)

    def auto_refresh_ports(self):
        ports = self.serialfunction.get_ports()
        current_ports = self.select_port.cget("values")

        if ports != list(current_ports):
            self.select_port.configure(values=ports)
            self.port_var.set(self.noactive if not ports else self.selectporttext)

        self.after_id = self.after(3000, self.auto_refresh_ports)

    def stop_auto_refresh(self):
        if hasattr(self, "after_id"):
            self.after_cancel(self.after_id)

    def settings_clicked(self):
        self.show_settings_view()
        
    def no_sound(self):
       self.sound_enabled = not self.sound_enabled
       new_text = "Sound: Off" if not self.sound_enabled else "Sound: On"
       self.sound_button.configure(text=new_text)
    
    
        
    def write_file(self):
         
        self.timeinput = self.time_input.get()
        self.planinput = self.plan_input.get()
        self.intervalinput = self.interval_input.get()
        
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        safe_plan = "".join(c for c in self.planinput if c.isalnum() or c in (' ',"-","_")).rstrip()
        filename = f"{timestamp}_{safe_plan}.txt"
        
        filepath = os.path.join(self.directory,filename)
        
        with open(filepath, 'w') as f:
            f.write(f"Time: {self.timeinput}\n")
            f.write(f"Plan: {self.planinput}\n")
            f.write(f"Interval: {self.intervalinput}\n")
            
        self.time_input.delete(0, "end")
        self.plan_input.delete(0, "end")
        self.interval_input.delete(0, "end")
        
        self.content_area.focus_set()
        self.update_file_list()
        
    def update_file_list(self):
        if os.path.exists(self.directory):
            files = [f for f in os.listdir(self.directory) if f.endswith(".txt")]
            self.exercise_pick.configure(values=files)
        else:
            self.exercise_pick.configure(values=[])
    
    
    def load_selected_file(self, selected_filename):
        filepath = os.path.join(self.directory, selected_filename)
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
                self.time = lines[0].split(":")[1].strip()
                self.plan = lines[1].split(":")[1].strip()
                self.interval = lines[2].split(":")[1].strip()
                
            if self.interval.lower().endswith("s"):
                self.interval = int(float(self.interval[:-1].strip()) * 1000)
            else:
                self.interval = int(float(self.interval.strip) * 1000)
                
                
            self.time_input.delete(0, "end")
            self.plan_input.delete(0,"end")
            self.interval_input.delete(0,"end")
            self.content_area.focus_set()
                    
            self.time_input.insert(0, self.time)
            self.plan_input.insert(0, self.plan)
            self.interval_input.insert(0, str(self.interval))
                
        except Exception as e:
          print("Error loading files")
                
    def start_timer_and_open_user(self):
        if hasattr(self, "plan") and hasattr(self, "interval"):
            instructions = [f"Do {self.plan}", "Rest"]
            minutes_only = int(self.time.split(":")[0])
            
            actualtime = minutes_only * 60
            self.timer.start(timer= actualtime, instructions=instructions, interval=self.interval)
            
        else:
            self.timer.start()