import time
import customtkinter
from Popups import Popups
from User import User

class TimerFunction:
    def __init__(self, parent, 
        timer_label):

        self.elapsedtime = 0
        self.running = False
        self.starttime = None
        self.parent = parent
        self.timer_label = timer_label
        self.font = ("Arial", 30)
        self.root = self.timer_label.winfo_toplevel()
        self.timerrunningtext = "Timer is not running!"


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
        try:
            self.timer_label.configure(
                text=f"Timer: {self.elapsedtime // 60}:{self.elapsedtime % 60:02d}",
                font=self.font
            )
            self.timer_label.update_idletasks()
        except (customtkinter.CTkTclError, Exception):
            self.running = False  # Widget doesn't exist, stop timer to prevent errors

    def updatetimer(self):
        if self.running:
            self.elapsedtime = int(time.time() - self.starttime)
            try:
                self.timer_label.configure(
                    text=f"Timer: {self.elapsedtime // 60}:{self.elapsedtime % 60:02d}",
                    font=self.font
                )
            except (customtkinter.CTkTclError, Exception):
                self.running = False
                return  # Exit early if widget is gone


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
        try:
            self.timer_label.configure(text="Timer: 0:00", font=self.font)
        except (customtkinter.CTkTclError, Exception):
            pass  # Timer label doesn't exist (view was switched)
