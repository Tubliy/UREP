import time
import customtkinter
from Popups import Popups

class TimerFunction:
    def __init__(self, parent, timer_label):
        self.elapsedtime = 0
        self.running = False
        self.starttime = None
        self.parent = parent
        self.timer_label = timer_label
        self.font = ("Arial",30)
        self.root = self.timer_label.winfo_toplevel()
        
    def start(self):
        if not self.running:
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
            self.parent.after(1000, self.updatetimer)

            
    def stop(self):
        if not self.running:
            Popups(self.root, "Timer is not running!", type="error")
        else:
            self.running = False
            
    def reset(self):
        self.running = False
        self.elapsedtime = 0
        self.timer_label.configure(text = "Timer: 0:00", font=self.font)
    
        