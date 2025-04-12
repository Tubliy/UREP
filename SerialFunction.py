import serial
import serial.tools.list_ports
from Popups import Popups

class SerialFunction:
    def __init__(self, parent):
        self.parent = parent
        self.available_ports = self.get_ports()
        self.root = parent.winfo_toplevel()
        self.ser = None
        self.connected = None

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        return [f"{port.device} - {port.description} " for port in ports]
    
    def connect_serial(self,selected_port):
        try:
            self.ser = serial.Serial(selected_port, 
             baudrate=115200,
            timeout=1)
            Popups(self.root, f"Successfully connected to {selected_port}", type="success")
            self.connected = True
            return self.ser
        except serial.SerialException:
            print("Failed to connect", selected_port)
            return None
    
    def try_connect(self, selected_port_string):
        if selected_port_string == "Select Port":
            Popups(self.root,"No Port Selected.", type="error")
            return None
        
        port = selected_port_string.split(" - ")[0]
        return self.connect_serial(port)
    
    def disconnect_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.connected = False
            Popups(self.root, "Successfully disconnected", type="success")
            return True
            
        else:
            Popups(self.root,"No active serial connection to disconnect.", type="error")
            return False
        
        
        