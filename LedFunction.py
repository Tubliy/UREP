import winsound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LedFunction:
    def __init__(self,parent,buttons, graph_frame,):
        self.led_states = [False] * len(buttons)
        self.led_buttons = buttons
        self.graph_frame = graph_frame
        self.parent = parent
        

        self.graph_widgets = [None] * len(buttons)
        self.canvases = [None] * len(buttons)
        self.figures = [None] * len(buttons)

        # Prepare grid layout
        if self.graph_frame and self.graph_frame.winfo_exists():
            for col in range(3):
                self.graph_frame.grid_columnconfigure(col, weight=1, uniform="graph")
            self.graph_frame.grid_rowconfigure(0, weight=1)

    def toggle_led(self, index):
        self.led_states[index] = not self.led_states[index]

        if self.led_states[index]:
            self.led_buttons[index].configure(fg_color="#00D68F", hover_color="#CC3B3B")
            if getattr(self.parent, "sound_enabled", True):
                winsound.PlaySound("sounds/c6.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            self.led_buttons[index].configure(fg_color="#FF4C4C", hover_color="#00B37D")

        self.rearrange_graphs()

    def show_graph(self, index):
        if not self.graph_frame or not self.graph_frame.winfo_exists():
            return

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

        # Destroy all current graphs
        for i in range(len(self.graph_widgets)):
            if self.graph_widgets[i]:
                self.graph_widgets[i].destroy()
                self.graph_widgets[i] = None
            if self.canvases[i]:
                try:
                    self.canvases[i].get_tk_widget().destroy()
                    self.canvases[i]._tkcanvas.destroy()
                except:
                    pass
                self.canvases[i] = None
            if self.figures[i]:
                plt.close(self.figures[i])
                self.figures[i] = None

        # Rebuild only active graphs
        visible = [i for i, state in enumerate(self.led_states) if state]

        for idx in visible:
            self.show_graph(idx)

        for i, idx in enumerate(visible):
            widget = self.graph_widgets[idx]
            if not widget:
                continue

            if len(visible) == 1:
                self.figures[idx].set_size_inches(6, 3)
                widget.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=5)
            else:
                row = i // 3
                col = i % 3
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
        self.graph_frame = None
