import customtkinter
import random

class User(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("User Instructions")
        self.existing = None
        self.existingcolor = None
        self.colors = [
            "#A3D2CA", "#FFB4A2", "#7F95D1", "#D9BF77", "#F67280",
            "#355C7D", "#F8B195", "#99E2B4", "#FFDAC1", "#6A0572",
            "#FFC09F", "#52796F", "#FF6B6B", "#4D96FF", "#C1C8E4"
        ]

        self.configure(fg_color=random.choice(self.colors))

        userwidth = 500
        userheight = 500
        self.instruction = [
            "Do a bicep curl",
            "Do a reverse curl",
            "Hold the dumbbell in place"
        ]

        self.resizable(False, False)
        

        parent.update_idletasks()

        x = parent.winfo_x() + (parent.winfo_width() // 2) - (userwidth // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (userheight // 2)

        self.instruction_label = customtkinter.CTkLabel(
            master=self,
            text=self.choosing_instruction(),
            font=("Arial", 36)
        )
        self.instruction_label.pack(anchor="center", pady=10)

        self.geometry(f"{userwidth}x{userheight}+{x}+{y}")

        # Start updating instructions continuously
        self.cycle_instructions()

    def choosing_instruction(self):
        choice = random.choice(self.instruction)
        while hasattr(self, "existing") and choice == self.existing:
            choice = random.choice(self.instruction)
        self.existing = choice
        return choice

    def cycle_instructions(self):
        self.instruction_label.configure(text=self.choosing_instruction())

    # Pick a new color that's not the same as the last one
        color = random.choice(self.colors)
        while hasattr(self, "existingcolor") and color == self.existingcolor:
            color = random.choice(self.colors)

        self.existingcolor = color
        self.configure(fg_color=color)

        self.after(10000, self.cycle_instructions)  # Change every 10 seconds

