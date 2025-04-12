from Popups import Popups
import winsound
class DataProcess:
    def __init__(self,parent):
        self.data = None
        self.parent = parent
        self.root = parent.winfo_toplevel()
        
    def export(self):
        if not self.data:
            Popups(self.root, "No data to export.", type="error")
        else:
            self.data = None