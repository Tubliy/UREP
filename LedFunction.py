import winsound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LedFunction:
    def __init__(self, buttons, graph_frame):
        self.led_states = [False] * len(buttons)
        self.led_buttons = buttons
        self.graph_frame = graph_frame

        self.graph_widgets = [None] * len(buttons)
        self.canvases = [None] * len(buttons)
        self.figures = [None] * len(buttons)

        # Grid config for responsive layout (safe check)
        if self.graph_frame and self.graph_frame.winfo_exists():
            for col in range(3):
                self.graph_frame.grid_columnconfigure(col, weight=1, uniform="graph")
            self.graph_frame.grid_rowconfigure(0, weight=1)

    def toggle_led(self, index):
        self.led_states[index] = not self.led_states[index]

        if self.led_states[index]:
            self.led_buttons[index].configure(fg_color="#00D68F", hover_color="#CC3B3B")
            winsound.PlaySound("sounds/c6.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.show_graph(index)
        else:
            self.led_buttons[index].configure(fg_color="#FF4C4C", hover_color="#00B37D")
            self.hide_graph(index)

        self.rearrange_graphs()

    def show_graph(self, index):
        if not self.graph_frame or not self.graph_frame.winfo_exists():
            return

        if self.graph_widgets[index]:
            return  # Already shown

        fig, ax = plt.subplots(figsize=(3, 2), dpi=80)
        ax.plot([0, 1, 2], [0, index + 1, index * 2 + 1],
                color='#00D68F', linewidth=1.5, marker='o', markersize=4)
        ax.set_facecolor('#FAFAFA')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title(f"LED {index + 1}", pad=10, fontsize=10)
        ax.set_xlabel("Time", fontsize=8)
        ax.set_ylabel("Value", fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_ylim(0, 5)
        ax.set_xlim(0, 2)
        fig.tight_layout(pad=1.5)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()

        self.graph_widgets[index] = widget
        self.canvases[index] = canvas
        self.figures[index] = fig

    def hide_graph(self, index):
        self._destroy_graph(index)

    def rearrange_graphs(self):
        if not self.graph_frame or not self.graph_frame.winfo_exists():
            return

        for widget in self.graph_widgets:
            if widget:
                widget.grid_forget()

        visible = [i for i, state in enumerate(self.led_states) if state]
        active_count = len(visible)

        for i, idx in enumerate(visible):
            row = i // 3
            col = i % 3
            widget = self.graph_widgets[idx]
            if widget:
                if active_count == 1:
                    self.figures[idx].set_size_inches(6, 3)
                    widget.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=5)
                else:
                    self.figures[idx].set_size_inches(3, 2)
                    widget.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                self.canvases[idx].draw()

    def _destroy_graph(self, index):
        if self.graph_widgets[index]:
            try:
                self.graph_widgets[index].destroy()
            except:
                pass
            self.graph_widgets[index] = None

        if self.canvases[index]:
            try:
                self.canvases[index].get_tk_widget().destroy()
                self.canvases[index]._tkcanvas.destroy()
                self.canvases[index].close_event()
            except:
                pass
            self.canvases[index] = None

        if self.figures[index]:
            try:
                plt.close(self.figures[index])
            except:
                pass
            self.figures[index] = None

    def cleanup(self):
        for i in range(len(self.led_buttons)):
            self._destroy_graph(i)
        self.graph_frame = None  # prevent reuse after destroy

    