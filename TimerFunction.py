import time
import customtkinter
from Popups import Popups
from User import User

class TimerFunction:
    def __init__(self, parent, 
    timer_label, 
    one_minute_test = None, 
    three_minute_test = None,
    five_minute_test = None,
    one_minute_var = None,
    three_minute_var = None,
    five_minute_var = None):
        
        self.elapsedtime = 0
        self.running = False
        self.starttime = None
        self.parent = parent
        self.timer_label = timer_label
        self.font = ("Arial",30)
        self.root = self.timer_label.winfo_toplevel()
        self.timerrunningtext = "Timer is not running!"
        self.one_minute_test = one_minute_test
        self.three_minute_test = three_minute_test
        self.five_minute_test = five_minute_test
        self.one_minute_var = one_minute_var
        self.three_minute_var = three_minute_var
        self.five_minute_var = five_minute_var
       
        
    def start(self):
        if not self.running:
            self.user_window = User(parent=self.root)
            self.starttime = time.time() - self.elapsedtime
            self.running = True
            self.updatenow()
            self.updatetimer()
        else:
            Popups(self.root, "Already started.", type="error")
            
    def updatenow(self):
        self.elapsedtime = int(time.time() - self.starttime)
        self.timer_label.configure(text=f"Timer: {self.elapsedtime // 60}:{self.elapsedtime % 60:02d}", font=self.font)
        self.timer_label.update_idletasks()
            
    def updatetimer(self):
        if self.running:
            self.elapsedtime = int(time.time() - self.starttime)
            self.timer_label.configure(text=f"Timer: {self.elapsedtime // 60}:{self.elapsedtime % 60:02d}", font=self.font)
            
            self.one_minute_function()
            self.three_minute_function()
            self.five_minute_function()
            
            self.parent.after(1000, self.updatetimer)

            
    def stop(self):
        if not self.running:
            Popups(self.root, f"{self.timerrunningtext}", type="error")
        else:
            self.running = False
            if hasattr(self, "user_window") and self.user_window.winfo_exists():
                self.user_window.destroy()
            
    def reset(self):
        self.running = False
        self.elapsedtime = 0
        self.timer_label.configure(text = "Timer: 0:00", font=self.font)
    
    def one_minute_function(self):
       if self.one_minute_var and self.one_minute_var.get():
           if self.elapsedtime == 60:
                self.stop()
                if self.one_minute_test:
                    self.one_minute_test.deselect()
            
    def three_minute_function(self):
        if self.three_minute_var and self.three_minute_var.get():
           if self.elapsedtime == 180:
                self.stop()
                if self.three_minute_test:
                    self.three_minute_test.deselect()
            
    def five_minute_function(self):
        if self.five_minute_var and self.five_minute_var.get():
           if self.elapsedtime == 300:
                self.stop()
                if self.five_minute_test:
                    self.five_minute_test.deselect()
                    

            